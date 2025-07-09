import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio
from datetime import datetime

# Import tools
from tools import (
    create_goal_analyzer,
    create_meal_planner,
    create_progress_tracker,
    create_workout_recommender
)

# Import specialized agents
from health_agents.escalation_agent import create_escalation_agent
from health_agents.injury_support_agent import create_injury_support_agent
from health_agents.nutrition_expert_agent import create_nutrition_expert_agent

# Import guardrails
from guardrails import create_health_guardrails

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present
if not gemini_api_key:
    st.error("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
    st.stop()

# Setup client 
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Preferred model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Runner config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Initialize session state
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'tools_initialized' not in st.session_state:
    st.session_state.tools_initialized = False

def initialize_tools():
    """Initialize all tools and agents"""
    if not st.session_state.tools_initialized:
        st.session_state.goal_analyzer = create_goal_analyzer()
        st.session_state.meal_planner = create_meal_planner()
        st.session_state.progress_tracker = create_progress_tracker()
        st.session_state.workout_recommender = create_workout_recommender()
        st.session_state.escalation_agent = create_escalation_agent()
        st.session_state.injury_support_agent = create_injury_support_agent()
        st.session_state.nutrition_expert_agent = create_nutrition_expert_agent()
        st.session_state.guardrails = create_health_guardrails()
        st.session_state.agent = Agent(
            name="Health Coach",
            instructions="""You are a friendly and knowledgeable health and wellness coach with access to specialized tools and agents. Your role is to:

1. Provide personalized health, fitness, and wellness advice based on the user's age and health information
2. Use the available tools to help users:
   - Analyze and set SMART goals (goal_analyzer)
   - Create personalized meal plans (meal_planner)
   - Track progress and measurements (progress_tracker)
   - Generate workout routines (workout_recommender)
3. Direct users to specialized agents when appropriate:
   - Escalation Agent: When users want to speak with humans
   - Injury Support Agent: When users report injuries or pain
   - Nutrition Expert Agent: When users need detailed nutrition advice
4. Always be encouraging, supportive, and motivating
5. Give practical, actionable advice for nutrition, exercise, mental health, and lifestyle
6. Consider the user's age when recommending exercises, diets, and wellness practices
7. Be mindful of safety and always recommend consulting healthcare professionals for serious health concerns
8. Use a warm, friendly tone while maintaining professionalism

Available Tools:
- Goal Analyzer: For setting and tracking SMART goals
- Meal Planner: For creating personalized meal plans
- Progress Tracker: For tracking measurements and workouts
- Workout Recommender: For generating personalized workout routines

Specialized Agents:
- Escalation Agent: For human support requests
- Injury Support Agent: For injury assessment and guidance
- Nutrition Expert Agent: For detailed nutrition consultations

Remember: You are a coach, not a doctor. For medical concerns, always recommend consulting healthcare professionals.""",
            model=model
        )
        st.session_state.tools_initialized = True

def add_to_chat_history(role, content):
    """Add message to chat history"""
    st.session_state.chat_history.append({"role": role, "content": content})

def display_chat_history():
    """Display chat history"""
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

async def process_user_input(user_question):
    """Process user input and return response"""
    user_info = st.session_state.user_info
    
    # Apply guardrails
    validation_result = st.session_state.guardrails.validate_user_input(user_question)
    
    if not validation_result['should_proceed']:
        return validation_result['message']
    
    # Check for escalation requests
    if any(word in user_question.lower() for word in ['human', 'speak to', 'talk to', 'real person', 'agent', 'representative']):
        result = st.session_state.escalation_agent.handle_escalation_request(user_info, user_question)
        return f"🔄 **Escalation Agent Response:**\n\n{result}"
    
    # Check for injury-related queries
    if any(word in user_question.lower() for word in ['injury', 'pain', 'hurt', 'sprain', 'strain', 'broken', 'fracture', 'swelling', 'bruise']):
        result = st.session_state.injury_support_agent.assess_injury(user_info, user_question, [])
        return f"🏥 **Injury Support Response:**\n\n{result}"
    
    # Check for meal planning
    if any(word in user_question.lower() for word in ['meal plan', 'meal planning', '7 days', 'weekly meal', 'daily meal', 'food plan', 'eating plan']):
        dietary_restrictions = []
        if 'vegetarian' in user_question.lower():
            dietary_restrictions.append('vegetarian')
        if 'vegan' in user_question.lower():
            dietary_restrictions.append('vegan')
        if 'plant-based' in user_question.lower():
            dietary_restrictions.append('vegetarian')
        
        result = st.session_state.meal_planner.generate_meal_plan(user_info, dietary_restrictions=dietary_restrictions)
        return f"🍽️ **Meal Plan Generated:**\n\n{result}"
    
    # Check for nutrition expert queries
    elif any(word in user_question.lower() for word in ['nutrition', 'diet', 'vitamin', 'mineral', 'supplement', 'protein', 'carbohydrate', 'fat', 'eating']):
        result = st.session_state.nutrition_expert_agent.provide_nutrition_consultation(user_info, user_question, None)
        return f"🥗 **Nutrition Expert Response:**\n\n{result}"
    
    # Check for goal analysis
    if 'goal' in user_question.lower() and ('analyze' in user_question.lower() or 'set' in user_question.lower()):
        if 'analyze' in user_question.lower():
            result = st.session_state.goal_analyzer.analyze_user_input(user_info)
            return f"🎯 **Goal Analysis:**\n\n{result}"
        else:
            return "To set a goal, please specify: goal type, target, and timeframe\nExample: 'set goal weight loss 10 pounds 3 months'"
    
    # Check for progress tracking
    elif 'progress' in user_question.lower() or 'track' in user_question.lower():
        result = st.session_state.progress_tracker.get_progress_summary()
        return f"📊 **Progress Summary:**\n\n{result}"
    
    # Check for workout recommendations
    elif 'workout' in user_question.lower() or 'exercise' in user_question.lower():
        result = st.session_state.workout_recommender.generate_workout_routine(user_info)
        return f"💪 **Workout Recommendation:**\n\n{result}"
    
    # Default: Use the main agent
    context = f"User Information: Age: {user_info.get('age', 'Not specified')}, Fitness Level: {user_info.get('fitness_level', 'Not specified')}, Goals: {user_info.get('health_goals', 'Not specified')}\n\nUser Question: {user_question}"
    
    result = await Runner.run(st.session_state.agent, context, run_config=config)
    return result.final_output

# Streamlit UI
st.set_page_config(
    page_title="Health & Wellness Coach",
    page_icon="🏃‍♀️",
    layout="wide"
)

st.title("🏃‍♀️ Your Personal Health & Wellness Coach")
st.markdown("I'm here to help you with fitness, nutrition, mental health, and overall wellness!")

# Initialize tools
initialize_tools()

# Sidebar for user information
with st.sidebar:
    st.header("📊 Your Profile")
    
    # User information form
    with st.form("user_info_form"):
        age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
        fitness_level = st.selectbox(
            "Fitness Level",
            ["beginner", "intermediate", "advanced"],
            index=0
        )
        health_goals = st.text_input("Health Goals", placeholder="e.g., weight loss, muscle gain, general fitness")
        equipment = st.selectbox(
            "Available Equipment",
            ["none", "home", "gym"],
            index=0
        )
        
        if st.form_submit_button("Update Profile"):
            st.session_state.user_info = {
                'age': age,
                'fitness_level': fitness_level,
                'health_goals': health_goals,
                'equipment': ['gym', 'barbell', 'dumbbells', 'machines'] if equipment == 'gym' else 
                            ['dumbbells', 'resistance bands', 'none'] if equipment == 'home' else 
                            ['none']
            }
            st.success("Profile updated!")
    
    # Quick actions
    st.header("⚡ Quick Actions")
    if st.button("🎯 Analyze Goals"):
        add_to_chat_history("user", "analyze my goals")
        with st.spinner("Analyzing your goals..."):
            try:
                # Ensure user_info has default values
                user_info = st.session_state.user_info.copy() if st.session_state.user_info else {}
                if not user_info:
                    user_info = {
                        'age': 25,
                        'fitness_level': 'beginner',
                        'health_goals': 'general fitness',
                        'equipment': ['none']
                    }
                
                result = st.session_state.goal_analyzer.analyze_user_input(user_info)
                add_to_chat_history("assistant", f"🎯 **Goal Analysis:**\n\n{result}")
                st.rerun()
            except Exception as e:
                st.error(f"Error analyzing goals: {str(e)}")
                st.error("Please update your profile in the sidebar first!")
    
    if st.button("🍽️ Generate Meal Plan"):
        add_to_chat_history("user", "create a meal plan")
        with st.spinner("Creating your meal plan..."):
            try:
                # Ensure user_info has default values
                user_info = st.session_state.user_info.copy() if st.session_state.user_info else {}
                if not user_info:
                    user_info = {
                        'age': 25,
                        'fitness_level': 'beginner',
                        'health_goals': 'general fitness',
                        'equipment': ['none']
                    }
                
                result = st.session_state.meal_planner.generate_meal_plan(user_info)
                add_to_chat_history("assistant", f"🍽️ **Meal Plan:**\n\n{result}")
                st.rerun()
            except Exception as e:
                st.error(f"Error generating meal plan: {str(e)}")
                st.error("Please update your profile in the sidebar first!")
    
    if st.button("💪 Get Workout"):
        add_to_chat_history("user", "recommend a workout")
        with st.spinner("Generating workout routine..."):
            try:
                # Ensure user_info has default values
                user_info = st.session_state.user_info.copy() if st.session_state.user_info else {}
                if not user_info:
                    user_info = {
                        'age': 25,
                        'fitness_level': 'beginner',
                        'health_goals': 'general fitness',
                        'equipment': ['none']
                    }
                
                result = st.session_state.workout_recommender.generate_workout_routine(user_info)
                add_to_chat_history("assistant", f"💪 **Workout Recommendation:**\n\n{result}")
                st.rerun()
            except Exception as e:
                st.error(f"Error generating workout: {str(e)}")
                st.error("Please update your profile in the sidebar first!")
    
    if st.button("📊 Check Progress"):
        add_to_chat_history("user", "show my progress")
        with st.spinner("Loading your progress..."):
            try:
                result = st.session_state.progress_tracker.get_progress_summary()
                add_to_chat_history("assistant", f"📊 **Progress Summary:**\n\n{result}")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading progress: {str(e)}")
                st.error("Please update your profile in the sidebar first!")

# Main chat interface
st.header("💬 Chat with Your Health Coach")

# Display chat history
display_chat_history()

# Chat input
if prompt := st.chat_input("Ask me anything about health, fitness, nutrition, or wellness!"):
    # Add user message to chat
    add_to_chat_history("user", prompt)
    st.chat_message("user").write(prompt)
    
    # Process the input
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = asyncio.run(process_user_input(prompt))
                add_to_chat_history("assistant", response)
                st.write(response)
            except Exception as e:
                error_msg = f"❌ Error processing your request: {str(e)}"
                add_to_chat_history("assistant", error_msg)
                st.error(error_msg)

# Footer
st.markdown("---")
st.markdown("💡 **Tips:** Ask me about exercise, nutrition, goal setting, progress tracking, or any health-related topic!") 