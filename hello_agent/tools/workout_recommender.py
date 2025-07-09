"""
Workout Recommendation Tool
Generates personalized workout routines based on user goals, fitness level, and equipment
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import random

class WorkoutRecommender:
    def __init__(self):
        self.workouts_file = "workout_routines.json"
        self.workout_routines = self.load_workout_routines()
        self.exercises = self.load_exercises()
    
    def load_workout_routines(self) -> Dict:
        """Load existing workout routines from file"""
        try:
            with open(self.workouts_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"routines": [], "created_date": datetime.now().isoformat()}
    
    def save_workout_routines(self):
        """Save workout routines to file"""
        with open(self.workouts_file, 'w') as f:
            json.dump(self.workout_routines, f, indent=2)
    
    def load_exercises(self) -> Dict:
        """Load exercise database"""
        return {
            "cardio": {
                "beginner": [
                    {"name": "Walking", "duration": 30, "calories": 150, "equipment": "none"},
                    {"name": "Light Jogging", "duration": 20, "calories": 180, "equipment": "none"},
                    {"name": "Cycling (Stationary)", "duration": 25, "calories": 200, "equipment": "bike"},
                    {"name": "Swimming", "duration": 30, "calories": 250, "equipment": "pool"},
                    {"name": "Dancing", "duration": 30, "calories": 200, "equipment": "none"}
                ],
                "intermediate": [
                    {"name": "Running", "duration": 30, "calories": 300, "equipment": "none"},
                    {"name": "Cycling (Outdoor)", "duration": 45, "calories": 350, "equipment": "bike"},
                    {"name": "Rowing", "duration": 25, "calories": 280, "equipment": "rower"},
                    {"name": "Elliptical", "duration": 30, "calories": 320, "equipment": "elliptical"},
                    {"name": "Jump Rope", "duration": 20, "calories": 250, "equipment": "rope"}
                ],
                "advanced": [
                    {"name": "HIIT Running", "duration": 25, "calories": 400, "equipment": "none"},
                    {"name": "Mountain Biking", "duration": 60, "calories": 500, "equipment": "bike"},
                    {"name": "Sprint Intervals", "duration": 20, "calories": 350, "equipment": "none"},
                    {"name": "Stair Master", "duration": 30, "calories": 380, "equipment": "stair master"},
                    {"name": "Boxing", "duration": 45, "calories": 450, "equipment": "punching bag"}
                ]
            },
            "strength": {
                "beginner": [
                    {"name": "Push-ups", "sets": 3, "reps": 10, "equipment": "none", "muscle": "chest"},
                    {"name": "Squats", "sets": 3, "reps": 15, "equipment": "none", "muscle": "legs"},
                    {"name": "Plank", "sets": 3, "duration": 30, "equipment": "none", "muscle": "core"},
                    {"name": "Lunges", "sets": 3, "reps": 10, "equipment": "none", "muscle": "legs"},
                    {"name": "Wall Sit", "sets": 3, "duration": 30, "equipment": "none", "muscle": "legs"}
                ],
                "intermediate": [
                    {"name": "Dumbbell Press", "sets": 4, "reps": 12, "equipment": "dumbbells", "muscle": "chest"},
                    {"name": "Deadlifts", "sets": 4, "reps": 8, "equipment": "barbell", "muscle": "back"},
                    {"name": "Pull-ups", "sets": 3, "reps": 8, "equipment": "pull-up bar", "muscle": "back"},
                    {"name": "Dumbbell Rows", "sets": 4, "reps": 12, "equipment": "dumbbells", "muscle": "back"},
                    {"name": "Shoulder Press", "sets": 4, "reps": 10, "equipment": "dumbbells", "muscle": "shoulders"}
                ],
                "advanced": [
                    {"name": "Bench Press", "sets": 5, "reps": 5, "equipment": "barbell", "muscle": "chest"},
                    {"name": "Squats", "sets": 5, "reps": 5, "equipment": "barbell", "muscle": "legs"},
                    {"name": "Overhead Press", "sets": 4, "reps": 8, "equipment": "barbell", "muscle": "shoulders"},
                    {"name": "Romanian Deadlifts", "sets": 4, "reps": 8, "equipment": "barbell", "muscle": "back"},
                    {"name": "Weighted Pull-ups", "sets": 4, "reps": 6, "equipment": "pull-up bar", "muscle": "back"}
                ]
            },
            "flexibility": {
                "beginner": [
                    {"name": "Cat-Cow Stretch", "duration": 5, "equipment": "none"},
                    {"name": "Child's Pose", "duration": 3, "equipment": "none"},
                    {"name": "Forward Fold", "duration": 3, "equipment": "none"},
                    {"name": "Butterfly Stretch", "duration": 3, "equipment": "none"},
                    {"name": "Cobra Stretch", "duration": 3, "equipment": "none"}
                ],
                "intermediate": [
                    {"name": "Downward Dog", "duration": 5, "equipment": "none"},
                    {"name": "Pigeon Pose", "duration": 5, "equipment": "none"},
                    {"name": "Triangle Pose", "duration": 5, "equipment": "none"},
                    {"name": "Warrior Pose", "duration": 5, "equipment": "none"},
                    {"name": "Bridge Pose", "duration": 5, "equipment": "none"}
                ],
                "advanced": [
                    {"name": "Splits", "duration": 10, "equipment": "none"},
                    {"name": "Handstand", "duration": 5, "equipment": "wall"},
                    {"name": "Wheel Pose", "duration": 5, "equipment": "none"},
                    {"name": "Crow Pose", "duration": 5, "equipment": "none"},
                    {"name": "Headstand", "duration": 5, "equipment": "wall"}
                ]
            }
        }
    
    def generate_workout_routine(self, user_info: Dict, workout_type: str = "balanced") -> str:
        """Generate a personalized workout routine"""
        age = user_info.get('age', 25)
        fitness_level = user_info.get('fitness_level', 'beginner')
        health_goals = user_info.get('health_goals', 'general fitness')
        available_equipment = user_info.get('equipment', ['none'])
        
        # Normalize fitness level to ensure it exists in our database
        valid_fitness_levels = ['beginner', 'intermediate', 'advanced']
        if fitness_level.lower() not in valid_fitness_levels:
            # Map similar terms to valid levels
            if fitness_level.lower() in ['novice', 'new', 'start']:
                fitness_level = 'beginner'
            elif fitness_level.lower() in ['advance', 'expert', 'pro']:
                fitness_level = 'advanced'
            else:
                fitness_level = 'beginner'  # Default to beginner if unknown
        
        # Determine workout focus based on goals
        if 'weight loss' in health_goals.lower():
            focus = "cardio_heavy"
        elif 'muscle gain' in health_goals.lower():
            focus = "strength_heavy"
        else:
            focus = "balanced"
        
        routine = {
            "user_info": user_info,
            "workout_type": workout_type,
            "focus": focus,
            "created_date": datetime.now().isoformat(),
            "exercises": {}
        }
        
        workout_text = f"""
💪 PERSONALIZED WORKOUT ROUTINE

📊 Your Profile:
• Age: {age} years old
• Fitness Level: {fitness_level}
• Goals: {health_goals}
• Focus: {focus.replace('_', ' ').title()}

"""
        
        try:
            # Generate exercises based on focus and fitness level
            if focus == "cardio_heavy":
                workout_text += self.generate_cardio_heavy_routine(fitness_level, available_equipment)
            elif focus == "strength_heavy":
                workout_text += self.generate_strength_heavy_routine(fitness_level, available_equipment)
            else:
                workout_text += self.generate_balanced_routine(fitness_level, available_equipment)
        except Exception as e:
            # Fallback to beginner level if there's an error
            print(f"⚠️ Error generating routine for {fitness_level} level, using beginner level instead.")
            fitness_level = 'beginner'
            if focus == "cardio_heavy":
                workout_text += self.generate_cardio_heavy_routine(fitness_level, available_equipment)
            elif focus == "strength_heavy":
                workout_text += self.generate_strength_heavy_routine(fitness_level, available_equipment)
            else:
                workout_text += self.generate_balanced_routine(fitness_level, available_equipment)
        
        # Save the routine
        self.workout_routines["routines"].append(routine)
        self.save_workout_routines()
        
        workout_text += f"""
💡 Tips for Success:
• Warm up for 5-10 minutes before each workout
• Stay hydrated throughout your session
• Listen to your body and rest when needed
• Progress gradually - don't rush the process
• Consistency is key to seeing results

🎯 Remember: This routine is designed for your {fitness_level} level. 
   Adjust intensity as needed and consult a trainer if you're unsure about any exercises.
"""
        
        return workout_text
    
    def generate_cardio_heavy_routine(self, fitness_level: str, equipment: List[str]) -> str:
        """Generate a cardio-focused workout routine"""
        routine_text = "🏃‍♀️ CARDIO-FOCUSED WORKOUT\n\n"
        
        # Ensure fitness level exists in our database
        if fitness_level not in self.exercises["cardio"]:
            fitness_level = 'beginner'  # Fallback to beginner
        
        # Select cardio exercises
        cardio_exercises = self.exercises["cardio"][fitness_level]
        available_cardio = [ex for ex in cardio_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]
        
        if not available_cardio:
            available_cardio = [ex for ex in cardio_exercises if ex["equipment"] == "none"]
        
        selected_cardio = random.sample(available_cardio, min(3, len(available_cardio)))
        
        routine_text += "🔥 CARDIO SESSION (45-60 minutes):\n"
        routine_text += "=" * 40 + "\n"
        
        for i, exercise in enumerate(selected_cardio, 1):
            routine_text += f"\n{i}. {exercise['name']}\n"
            routine_text += f"   Duration: {exercise['duration']} minutes\n"
            routine_text += f"   Calories: ~{exercise['calories']} burned\n"
            routine_text += f"   Equipment: {exercise['equipment']}\n"
        
        # Add some strength exercises
        if fitness_level not in self.exercises["strength"]:
            fitness_level = 'beginner'  # Fallback to beginner
            
        strength_exercises = self.exercises["strength"][fitness_level]
        available_strength = [ex for ex in strength_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]
        
        if available_strength:
            selected_strength = random.sample(available_strength, min(3, len(available_strength)))
            
            routine_text += f"\n💪 STRENGTH COMPONENT (15-20 minutes):\n"
            routine_text += "=" * 40 + "\n"
            
            for i, exercise in enumerate(selected_strength, 1):
                routine_text += f"\n{i}. {exercise['name']}\n"
                if 'reps' in exercise:
                    routine_text += f"   Sets: {exercise['sets']} | Reps: {exercise['reps']}\n"
                elif 'duration' in exercise:
                    routine_text += f"   Sets: {exercise['sets']} | Duration: {exercise['duration']} seconds\n"
                else:
                    routine_text += f"   Sets: {exercise['sets']}\n"
                routine_text += f"   Muscle: {exercise['muscle']}\n"
                routine_text += f"   Equipment: {exercise['equipment']}\n"
        
        return routine_text
    
    def generate_strength_heavy_routine(self, fitness_level: str, equipment: List[str]) -> str:
        """Generate a strength-focused workout routine"""
        routine_text = "🏋️‍♂️ STRENGTH-FOCUSED WORKOUT\n\n"
        
        # Ensure fitness level exists in our database
        if fitness_level not in self.exercises["strength"]:
            fitness_level = 'beginner'  # Fallback to beginner
        
        # Select strength exercises
        strength_exercises = self.exercises["strength"][fitness_level]
        available_strength = [ex for ex in strength_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]
        
        if not available_strength:
            available_strength = [ex for ex in strength_exercises if ex["equipment"] == "none"]
        
        selected_strength = random.sample(available_strength, min(5, len(available_strength)))
        
        routine_text += "💪 STRENGTH SESSION (45-60 minutes):\n"
        routine_text += "=" * 40 + "\n"
        
        for i, exercise in enumerate(selected_strength, 1):
            routine_text += f"\n{i}. {exercise['name']}\n"
            if 'reps' in exercise:
                routine_text += f"   Sets: {exercise['sets']} | Reps: {exercise['reps']}\n"
            elif 'duration' in exercise:
                routine_text += f"   Sets: {exercise['sets']} | Duration: {exercise['duration']} seconds\n"
            else:
                routine_text += f"   Sets: {exercise['sets']}\n"
            routine_text += f"   Muscle: {exercise['muscle']}\n"
            routine_text += f"   Equipment: {exercise['equipment']}\n"
        
        # Add some cardio
        if fitness_level not in self.exercises["cardio"]:
            fitness_level = 'beginner'  # Fallback to beginner
            
        cardio_exercises = self.exercises["cardio"][fitness_level]
        available_cardio = [ex for ex in cardio_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]
        
        if available_cardio:
            selected_cardio = random.sample(available_cardio, min(2, len(available_cardio)))
            
            routine_text += f"\n🔥 CARDIO FINISHER (10-15 minutes):\n"
            routine_text += "=" * 40 + "\n"
            
            for i, exercise in enumerate(selected_cardio, 1):
                routine_text += f"\n{i}. {exercise['name']}\n"
                routine_text += f"   Duration: {exercise['duration']} minutes\n"
                routine_text += f"   Equipment: {exercise['equipment']}\n"
        
        return routine_text
    
    def generate_balanced_routine(self, fitness_level: str, equipment: List[str]) -> str:
        """Generate a balanced workout routine"""
        routine_text = "⚖️ BALANCED WORKOUT\n\n"
        
        # Ensure fitness level exists in our database
        if fitness_level not in self.exercises["cardio"]:
            fitness_level = 'beginner'  # Fallback to beginner
        
        # Cardio component
        cardio_exercises = self.exercises["cardio"][fitness_level]
        available_cardio = [ex for ex in cardio_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]
        selected_cardio = random.sample(available_cardio, min(2, len(available_cardio)))
        
        routine_text += "🔥 CARDIO (20-25 minutes):\n"
        routine_text += "=" * 30 + "\n"
        
        for i, exercise in enumerate(selected_cardio, 1):
            routine_text += f"\n{i}. {exercise['name']}\n"
            routine_text += f"   Duration: {exercise['duration']} minutes\n"
            routine_text += f"   Equipment: {exercise['equipment']}\n"
        
        # Strength component
        if fitness_level not in self.exercises["strength"]:
            fitness_level = 'beginner'  # Fallback to beginner
            
        strength_exercises = self.exercises["strength"][fitness_level]
        available_strength = [ex for ex in strength_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]
        selected_strength = random.sample(available_strength, min(4, len(available_strength)))
        
        routine_text += f"\n💪 STRENGTH (25-30 minutes):\n"
        routine_text += "=" * 30 + "\n"
        
        for i, exercise in enumerate(selected_strength, 1):
            routine_text += f"\n{i}. {exercise['name']}\n"
            if 'reps' in exercise:
                routine_text += f"   Sets: {exercise['sets']} | Reps: {exercise['reps']}\n"
            elif 'duration' in exercise:
                routine_text += f"   Sets: {exercise['sets']} | Duration: {exercise['duration']} seconds\n"
            else:
                routine_text += f"   Sets: {exercise['sets']}\n"
            routine_text += f"   Muscle: {exercise['muscle']}\n"
            routine_text += f"   Equipment: {exercise['equipment']}\n"
        
        # Flexibility component
        if fitness_level not in self.exercises["flexibility"]:
            fitness_level = 'beginner'  # Fallback to beginner
            
        flexibility_exercises = self.exercises["flexibility"][fitness_level]
        selected_flexibility = random.sample(flexibility_exercises, min(3, len(flexibility_exercises)))
        
        routine_text += f"\n🧘‍♀️ FLEXIBILITY (10-15 minutes):\n"
        routine_text += "=" * 30 + "\n"
        
        for i, exercise in enumerate(selected_flexibility, 1):
            routine_text += f"\n{i}. {exercise['name']}\n"
            routine_text += f"   Duration: {exercise['duration']} minutes\n"
            routine_text += f"   Equipment: {exercise['equipment']}\n"
        
        return routine_text
    
    def get_workout_history(self) -> str:
        """Get history of workout routines"""
        if not self.workout_routines["routines"]:
            return "📝 No workout routines created yet. Use 'generate_routine' to create your first workout!"
        
        history = "📋 WORKOUT ROUTINE HISTORY\n\n"
        
        for i, routine in enumerate(self.workout_routines["routines"], 1):
            history += f"{i}. {routine['created_date'][:10]}\n"
            history += f"   Type: {routine['workout_type']}\n"
            history += f"   Focus: {routine['focus'].replace('_', ' ').title()}\n"
            history += f"   Goal: {routine['user_info'].get('health_goals', 'Not specified')}\n\n"
        
        return history

def create_workout_recommender() -> WorkoutRecommender:
    """Factory function to create a workout recommender instance"""
    return WorkoutRecommender() 