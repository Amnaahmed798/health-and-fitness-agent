import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import re
import json
from datetime import datetime

# Import agents/tools
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from tools import (
    create_goal_analyzer,
    create_meal_planner,
    create_progress_tracker,
    create_workout_recommender
)
from health_agents.escalation_agent import create_escalation_agent
from health_agents.injury_support_agent import create_injury_support_agent
from health_agents.nutrition_expert_agent import create_nutrition_expert_agent
from guardrails import create_health_guardrails

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Setup client and model
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Initialize tools and agents
goal_analyzer = create_goal_analyzer()
meal_planner = create_meal_planner()
progress_tracker = create_progress_tracker()
workout_recommender = create_workout_recommender()
escalation_agent = create_escalation_agent()
injury_support_agent = create_injury_support_agent()
nutrition_expert_agent = create_nutrition_expert_agent()
guardrails = create_health_guardrails()

# In-memory storage for workout logs (replace with file/database for persistence)
workout_logs = []

# Pydantic model for workout log
class WorkoutLogData(BaseModel):
    date: str
    workout_type: str
    notes: Optional[str] = None

# Health coach agent
health_coach_agent = Agent(
        name="Health Coach",
    instructions="""
You are a friendly and knowledgeable health and wellness coach with access to specialized tools and agents. Your role is to:
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

IMPORTANT: Always structure your responses in a clear, readable format:
- Use bullet points (•) for lists
- Use emojis to highlight important sections (💡, ⚠️, 🎯, etc.)
- Break up long paragraphs into smaller, digestible sections
- Use clear headings and subheadings
- Provide actionable steps in numbered or bulleted lists
- Keep responses concise but comprehensive

CRITICAL FORMATTING RULES:
- Use **bold** for section headings (e.g., **Goal Setting**, **Nutrition**, **Exercise**)
- Use bullet points (•) for lists, not dashes (-)
- Keep each section short and to the point
- Maximum 3-4 bullet points per section
- Use emojis to make sections stand out
- Avoid long paragraphs - break them into bullet points
- Be direct and actionable
- Keep total response under 200 words unless specifically asked for detailed information

TOOL USAGE:
- When users state goals (e.g., "I want to gain 2kg in 1 month"), the system will automatically use the Goal Analyzer tool
- When users ask for meal plans, nutrition advice, or dietary questions, the system will use the Meal Planner or Nutrition Expert tools
- When users ask for workouts, exercise routines, or fitness advice, the system will use the Workout Recommender tool
- When users ask to track progress, measurements, or check their status, the system will use the Progress Tracker tool
- When users report injuries or pain, the system will use the Injury Support Agent
- When users want to speak with humans, the system will use the Escalation Agent
- All tools are used automatically based on user intent - no need to manually specify tool usage
""",
        model=model
    )

# Pydantic models
class ChatRequest(BaseModel):
    prompt: str
    userInfo: Optional[Dict[str, Any]] = None
class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None
class UserProfile(BaseModel):
    age: Optional[int] = None
    fitnessLevel: Optional[str] = None
    healthGoals: Optional[str] = None
    equipment: Optional[List[str]] = None
class MealPlanRequest(BaseModel):
    dietaryRestrictions: Optional[List[str]] = None
    userInfo: Optional[Dict[str, Any]] = None
class WorkoutRequest(BaseModel):
    userInfo: Optional[Dict[str, Any]] = None
class ProgressData(BaseModel):
    date: str
    weight: Optional[float] = None
    bodyFat: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    notes: Optional[str] = None
class GoalData(BaseModel):
    goalType: str
    target: str
    timeframe: str
    userInfo: Optional[Dict[str, Any]] = None

# FastAPI app
app = FastAPI(title="Health Coach API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, you can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Health Coach API is running!"}

def extract_calorie_target(prompt: str) -> int:
    """Extract calorie target from the prompt. Returns int or None if not found."""
    match = re.search(r'(\d{3,5})\s*(calories|kcal|cal)', prompt.lower())
    if match:
        return int(match.group(1))
    return None

@app.post("/ask", response_model=ChatResponse)
async def ask_health_coach(request: ChatRequest):
    try:
        validation_result = guardrails.validate_user_input(request.prompt)
        if not validation_result['should_proceed']:
            return ChatResponse(
                response=validation_result['message'],
                success=False,
                error="Invalid input"
            )
        # Escalation
        if any(word in request.prompt.lower() for word in ['human', 'speak to', 'talk to', 'real person', 'agent', 'representative']):
            result = escalation_agent.handle_escalation_request(request.userInfo or {}, request.prompt)
            return ChatResponse(response=result, success=True)
        # Injury
        if any(word in request.prompt.lower() for word in ['injury', 'pain', 'hurt', 'sprain', 'strain', 'broken', 'fracture', 'swelling', 'bruise']):
            result = injury_support_agent.assess_injury(request.userInfo or {}, request.prompt, [])
            return ChatResponse(response=result, success=True)
        # Meal/Nutrition
        meal_nutrition_keywords = [
            'meal plan', 'meal planning', 'weekly meal', 'daily meal', 'food plan', 'eating plan',
            'nutrition', 'diet', 'vitamin', 'mineral', 'supplement', 'protein', 'carbohydrate', 'fat', 'eating',
            'calories', 'macros', 'meal prep', 'diet plan', 'nutrition plan', 'food', 'nutrition advice'
        ]
        if any(keyword in request.prompt.lower() for keyword in meal_nutrition_keywords):
            meal_plan_keywords = ['meal plan', 'meal planning', 'weekly meal', 'daily meal', 'food plan', 'eating plan', 'meal prep', 'diet plan']
            if any(keyword in request.prompt.lower() for keyword in meal_plan_keywords):
                dietary_restrictions = extract_dietary_restrictions(request.prompt)
                calorie_target = extract_calorie_target(request.prompt)
                if not calorie_target or not dietary_restrictions:
                    return ChatResponse(
                        response="To create a personalized meal plan, please tell me your daily calorie target (e.g., 2200 calories) and any dietary restrictions (e.g., vegetarian, vegan, gluten-free, etc.).",
                        success=False
                    )
                # Pass calorie_target and dietary_restrictions to the meal planner if both are provided
                user_info = request.userInfo or {}
                user_info['calorie_target'] = calorie_target
                result = meal_planner.generate_meal_plan(user_info, dietary_restrictions=dietary_restrictions)
                return ChatResponse(response=result, success=True)
            else:
                result = nutrition_expert_agent.provide_nutrition_consultation(request.userInfo or {}, request.prompt, None)
                return ChatResponse(response=result, success=True)
        # Goal
        goal_keywords = ['goal', 'gain', 'lose', 'weight', 'muscle', 'fitness', 'target', 'achieve']
        has_goal_keyword = any(keyword in request.prompt.lower() for keyword in goal_keywords)
        if has_goal_keyword or 'analyze' in request.prompt.lower() or 'set' in request.prompt.lower():
            goal_info = extract_goal_from_prompt(request.prompt)
            print(f"[DEBUG] Extracted goal_info: {goal_info}")  # Log extracted goal info
            if goal_info and 'target' in goal_info and 'timeframe' in goal_info:
                print("[DEBUG] Calling set_smart_goal with:", goal_info)
                # Use set_smart_goal when we have complete goal information
                result = goal_analyzer.set_smart_goal(
                    goal_type=goal_info.get('type', 'general'),
                    target=goal_info['target'],
                    timeframe=goal_info['timeframe']
                )
                return ChatResponse(response=result, success=True)
            elif goal_info:
                print("[DEBUG] Calling analyze_user_input with userInfo:", request.userInfo)
                # Use analyze_user_input when we have partial goal information
                result = goal_analyzer.analyze_user_input(request.userInfo or {})
                return ChatResponse(response=result, success=True)
            else:
                print("[DEBUG] No goal info extracted from prompt.")
                return ChatResponse(response="To set a goal, please specify: goal type, target, and timeframe", success=True)
        # Progress
        if any(word in request.prompt.lower() for word in ['progress', 'track', 'measurement', 'weight', 'body fat', 'measure', 'log', 'record', 'monitor', 'check progress', 'how am i doing', 'my progress']):
            result = progress_tracker.get_progress_summary()
            workout_count = get_logged_workouts_count()
            if "Workouts:" in result:
                result = result.replace("Workouts: 0 sessions", f"Workouts: {workout_count} sessions")
            else:
                result += f"\n💪 Workouts: {workout_count} sessions"
            return ChatResponse(response=result, success=True)
        # Workout
        if any(word in request.prompt.lower() for word in ['workout', 'exercise', 'training', 'routine', 'fitness', 'gym', 'strength', 'cardio', 'aerobics', 'sports', 'activity', 'movement', 'training plan', 'exercise plan']):
            result = workout_recommender.generate_workout_routine(request.userInfo or {})
            return ChatResponse(response=result, success=True)
        # Fallback: use agent
        context = f"User Information: {request.userInfo or 'Not specified'}\n\nUser Question: {request.prompt}"
        result = await Runner.run(health_coach_agent, context, run_config=config)
        return ChatResponse(response=result.final_output, success=True)
    except Exception as e:
        print(f"[ERROR] Exception in /ask endpoint: {str(e)}")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return ChatResponse(
            response="Sorry, I encountered an error. Please try again.",
            success=False,
            error=str(e)
        )

@app.get("/profile", response_model=UserProfile)
async def get_user_profile():
    return UserProfile()

@app.post("/profile")
async def update_user_profile(profile: UserProfile):
    return {"message": "Profile updated successfully"}

@app.post("/meal-plan")
async def get_meal_plan(request: MealPlanRequest):
    try:
        dietary_restrictions = request.dietaryRestrictions or []
        result = meal_planner.generate_meal_plan(request.userInfo or {}, dietary_restrictions=dietary_restrictions)
        return {"mealPlan": result, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

@app.post("/workout")
async def get_workout_routine(request: WorkoutRequest):
    try:
        result = workout_recommender.generate_workout_routine(request.userInfo or {})
        return {"workout": result, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

@app.post("/progress")
async def track_progress(data: ProgressData):
    try:
        result = progress_tracker.add_measurement(
            data.date, 
            data.weight, 
            data.bodyFat, 
            data.chest, 
            data.waist, 
            notes=data.notes
        )
        return {"message": result, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

@app.post("/goal")
async def set_goal(data: GoalData):
    try:
        result = goal_analyzer.set_smart_goal(
            goal_type=data.goalType,
            target=data.target,
            timeframe=data.timeframe
        )
        return {"message": result, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

@app.post("/log-workout")
async def log_workout(data: WorkoutLogData):
    # Optionally, validate date format
    try:
        datetime.strptime(data.date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD.", "success": False}
    # Store the workout log
    workout_logs.append(data.dict())
    return {"message": "Workout logged successfully!", "success": True}

# --- Helper functions ---
def extract_dietary_restrictions(prompt: str) -> list:
    prompt_lower = prompt.lower()
    restrictions = []
    restriction_keywords = {
        'vegetarian': ['vegetarian', 'veggie'],
        'vegan': ['vegan', 'plant-based'],
        'gluten-free': ['gluten-free', 'gluten free', 'celiac'],
        'dairy-free': ['dairy-free', 'dairy free', 'lactose-free', 'lactose free'],
        'keto': ['keto', 'ketogenic', 'low-carb'],
        'paleo': ['paleo', 'paleolithic'],
        'mediterranean': ['mediterranean', 'med diet'],
        'low-sodium': ['low-sodium', 'low sodium', 'low salt'],
        'low-fat': ['low-fat', 'low fat'],
        'high-protein': ['high-protein', 'high protein', 'protein-rich']
    }
    for restriction, keywords in restriction_keywords.items():
        if any(keyword in prompt_lower for keyword in keywords):
            restrictions.append(restriction)
    return restrictions

def extract_goal_from_prompt(prompt: str) -> dict:
    prompt_lower = prompt.lower()
    goal_info = {}
    if any(word in prompt_lower for word in ['gain', 'gain weight', 'gain muscle', 'build muscle']):
        goal_info['type'] = 'muscle_gain'
    elif any(word in prompt_lower for word in ['lose', 'lose weight', 'lose fat', 'slim down']):
        goal_info['type'] = 'weight_loss'
    elif any(word in prompt_lower for word in ['maintain', 'stay', 'keep']):
        goal_info['type'] = 'maintenance'
    elif any(word in prompt_lower for word in ['fitness', 'get fit', 'improve fitness']):
        goal_info['type'] = 'fitness'
    else:
        goal_info['type'] = 'general'
    weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|pounds?|lbs?)', prompt_lower)
    if weight_match:
        goal_info['target'] = f"{weight_match.group(1)} {weight_match.group(2)}"
    time_keywords = {
        'week': ['week', 'weeks'],
        'month': ['month', 'months'],
        'day': ['day', 'days'],
        'year': ['year', 'years']
    }
    for time_unit, keywords in time_keywords.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                time_match = re.search(r'(\d+)\s*' + keyword, prompt_lower)
                if time_match:
                    goal_info['timeframe'] = f"{time_match.group(1)} {time_unit}"
                    break
        if 'timeframe' in goal_info:
            break
    return goal_info

# Update the progress summary in progress_tracker.get_progress_summary if possible
# For now, add a helper to count logged workouts in the last 30 days
def get_logged_workouts_count():
    now = datetime.now()
    count = 0
    for log in workout_logs:
        try:
            log_date = datetime.strptime(log["date"], "%Y-%m-%d")
            if (now - log_date).days <= 30:
                count += 1
        except Exception:
            continue
    return count

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)