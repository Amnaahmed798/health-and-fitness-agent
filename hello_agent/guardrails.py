"""
Guardrails System
Filters user input to ensure only health and fitness related questions are processed
"""

import re
from typing import Dict, List, Tuple

class HealthGuardrails:
    def __init__(self):
        self.health_keywords = self.load_health_keywords()
        self.fitness_keywords = self.load_fitness_keywords()
        self.nutrition_keywords = self.load_nutrition_keywords()
        self.off_topic_keywords = self.load_off_topic_keywords()
        
    def load_health_keywords(self) -> List[str]:
        """Load health-related keywords"""
        return [
            # General health
            'health', 'wellness', 'wellbeing', 'healthy', 'medical', 'doctor', 'hospital',
            'symptoms', 'pain', 'injury', 'recovery', 'healing', 'treatment',
            
            # Body and physical health
            'body', 'weight', 'height', 'bmi', 'fat', 'muscle', 'strength', 'energy',
            'sleep', 'rest', 'tired', 'fatigue', 'stress', 'anxiety', 'depression',
            'blood pressure', 'heart', 'lungs', 'digestion', 'immune', 'immune system',
            
            # Fitness and exercise
            'exercise', 'workout', 'training', 'gym', 'running', 'walking', 'cycling',
            'swimming', 'yoga', 'pilates', 'strength training', 'cardio', 'flexibility',
            'endurance', 'stamina', 'fitness level', 'physical activity', 'sports',
            
            # Nutrition and diet
            'nutrition', 'diet', 'food', 'eating', 'meal', 'calories', 'protein',
            'carbohydrates', 'fats', 'vitamins', 'minerals', 'supplements',
            'vegetarian', 'vegan', 'plant-based', 'gluten-free', 'dairy-free',
            'breakfast', 'lunch', 'dinner', 'snack', 'hydration', 'water',
            
            # Goals and progress
            'goal', 'target', 'progress', 'improve', 'lose weight', 'gain muscle',
            'build strength', 'get fit', 'stay healthy', 'maintain', 'achieve',
            
            # Lifestyle
            'lifestyle', 'routine', 'habit', 'schedule', 'balance', 'motivation',
            'consistency', 'discipline', 'commitment', 'challenge', 'transformation',
            
            # Age and life stages
            'age', 'young', 'old', 'senior', 'teenager', 'adult', 'pregnancy',
            'menopause', 'aging', 'elderly', 'children', 'kids',
            
            # Specific health conditions
            'diabetes', 'hypertension', 'obesity', 'arthritis', 'back pain',
            'knee pain', 'shoulder pain', 'joint', 'bone', 'spine', 'posture',
            
            # Mental health
            'mental health', 'mind', 'brain', 'cognitive', 'memory', 'focus',
            'concentration', 'mood', 'happiness', 'confidence', 'self-esteem',
            
            # Preventive health
            'prevention', 'prevent', 'screening', 'checkup', 'vaccination',
            'immunization', 'safety', 'protection', 'risk', 'precaution'
        ]
    
    def load_fitness_keywords(self) -> List[str]:
        """Load fitness-related keywords"""
        return [
            # Exercise types
            'workout', 'exercise', 'training', 'fitness', 'gym', 'cardio',
            'strength', 'weightlifting', 'bodybuilding', 'powerlifting',
            'crossfit', 'hiit', 'interval', 'circuit', 'functional',
            
            # Cardio exercises
            'running', 'jogging', 'walking', 'cycling', 'biking', 'swimming',
            'rowing', 'elliptical', 'treadmill', 'stairmaster', 'jump rope',
            'dancing', 'aerobic', 'zumba', 'spinning',
            
            # Strength exercises
            'squat', 'deadlift', 'bench press', 'push-up', 'pull-up',
            'dumbbell', 'barbell', 'kettlebell', 'resistance', 'weight',
            'curl', 'press', 'row', 'lunge', 'plank', 'crunch',
            
            # Flexibility and mobility
            'yoga', 'pilates', 'stretching', 'flexibility', 'mobility',
            'balance', 'stability', 'core', 'abs', 'posture',
            
            # Sports and activities
            'sports', 'basketball', 'football', 'soccer', 'tennis', 'golf',
            'baseball', 'volleyball', 'hiking', 'climbing', 'martial arts',
            'boxing', 'kickboxing', 'wrestling', 'gymnastics',
            
            # Fitness equipment
            'treadmill', 'elliptical', 'bike', 'rower', 'weights',
            'machines', 'free weights', 'cables', 'bands', 'balls',
            
            # Fitness metrics
            'reps', 'sets', 'weight', 'distance', 'time', 'pace',
            'heart rate', 'calories', 'intensity', 'volume', 'frequency',
            
            # Training concepts
            'progressive overload', 'periodization', 'recovery', 'rest',
            'overtraining', 'plateau', 'adaptation', 'specificity'
        ]
    
    def load_nutrition_keywords(self) -> List[str]:
        """Load nutrition-related keywords"""
        return [
            # Food groups
            'protein', 'carbohydrates', 'carbs', 'fats', 'fiber', 'vitamins',
            'minerals', 'antioxidants', 'omega', 'fatty acids', 'amino acids',
            
            # Food types
            'meat', 'chicken', 'beef', 'pork', 'fish', 'seafood', 'eggs',
            'dairy', 'milk', 'cheese', 'yogurt', 'vegetables', 'fruits',
            'grains', 'bread', 'rice', 'pasta', 'nuts', 'seeds', 'legumes',
            'beans', 'lentils', 'tofu', 'tempeh', 'quinoa', 'oats',
            
            # Dietary patterns
            'vegetarian', 'vegan', 'plant-based', 'keto', 'paleo',
            'mediterranean', 'dash', 'low-carb', 'high-protein', 'balanced',
            'organic', 'natural', 'whole foods', 'processed foods',
            
            # Nutrition concepts
            'calories', 'macros', 'micronutrients', 'portion', 'serving',
            'meal timing', 'fasting', 'intermittent', 'supplements',
            'vitamins', 'minerals', 'probiotics', 'prebiotics',
            
            # Health conditions and nutrition
            'diabetes', 'heart disease', 'cholesterol', 'blood sugar',
            'gluten', 'lactose', 'allergies', 'intolerances', 'sensitivities',
            
            # Weight management
            'weight loss', 'weight gain', 'maintenance', 'bulking',
            'cutting', 'body composition', 'metabolism', 'thermogenesis'
        ]
    
    def load_off_topic_keywords(self) -> List[str]:
        """Load keywords that indicate off-topic questions"""
        return [
            # Technology
            'ai', 'artificial intelligence', 'machine learning', 'programming',
            'coding', 'software', 'computer', 'technology', 'app', 'website',
            'internet', 'social media', 'facebook', 'instagram', 'twitter',
            
            # Business and finance
            'business', 'money', 'finance', 'investment', 'stock', 'trading',
            'cryptocurrency', 'bitcoin', 'crypto', 'banking', 'insurance',
            'mortgage', 'loan', 'credit', 'debt', 'tax', 'salary',
            
            # Politics and current events
            'politics', 'government', 'election', 'president', 'congress',
            'news', 'current events', 'world', 'country', 'economy',
            'climate change', 'environment', 'global warming',
            
            # Entertainment
            'movie', 'film', 'tv', 'television', 'show', 'series',
            'music', 'song', 'artist', 'actor', 'actress', 'celebrity',
            'game', 'gaming', 'video game', 'sports team', 'team',
            
            # Education and academics
            'school', 'college', 'university', 'education', 'study',
            'homework', 'exam', 'test', 'assignment', 'research',
            'science', 'math', 'history', 'literature', 'philosophy',
            
            # Travel and location
            'travel', 'vacation', 'trip', 'hotel', 'flight', 'airline',
            'destination', 'country', 'city', 'place', 'location',
            'weather', 'climate', 'temperature',
            
            # Personal relationships
            'relationship', 'dating', 'marriage', 'family', 'friend',
            'boyfriend', 'girlfriend', 'husband', 'wife', 'partner',
            'love', 'romance', 'breakup', 'divorce',
            
            # Religion and spirituality
            'religion', 'god', 'prayer', 'church', 'temple', 'mosque',
            'spiritual', 'meditation', 'zen', 'buddhism', 'christianity',
            'islam', 'judaism', 'hinduism', 'faith', 'belief',
            
            # Other off-topic subjects
            'fashion', 'style', 'clothing', 'shopping', 'beauty',
            'cosmetics', 'makeup', 'skincare', 'hair', 'furniture',
            'home', 'house', 'car', 'vehicle', 'transportation'
        ]
    
    def is_health_fitness_related(self, user_input: str) -> Tuple[bool, str]:
        """
        Check if user input is health and fitness related
        Returns: (is_related, reason)
        """
        input_lower = user_input.lower()
        
        # Check for health, fitness, or nutrition keywords
        health_score = sum(1 for keyword in self.health_keywords if keyword in input_lower)
        fitness_score = sum(1 for keyword in self.fitness_keywords if keyword in input_lower)
        nutrition_score = sum(1 for keyword in self.nutrition_keywords if keyword in input_lower)
        
        total_health_score = health_score + fitness_score + nutrition_score
        
        # Check for off-topic keywords
        off_topic_score = sum(1 for keyword in self.off_topic_keywords if keyword in input_lower)
        
        # Much more lenient approach - if there's ANY health/fitness content, allow it
        if total_health_score > 0:
            return True, "Health/fitness related question"
        
        # Check for common health-related words that might be misspelled
        health_indicators = [
            'calorie', 'calories', 'burn', 'burning', 'weight', 'exercise', 'workout',
            'diet', 'food', 'eat', 'eating', 'health', 'fit', 'fitness', 'body',
            'muscle', 'fat', 'lose', 'gain', 'train', 'training', 'gym', 'run',
            'walk', 'jog', 'swim', 'bike', 'cycle', 'yoga', 'stretch', 'strength',
            'cardio', 'protein', 'vitamin', 'mineral', 'supplement', 'meal', 'snack',
            'breakfast', 'lunch', 'dinner', 'water', 'drink', 'hydration'
        ]
        
        if any(word in input_lower for word in health_indicators):
            return True, "Health/fitness related (including common variations)"
        
        # Check for general inquiry patterns that might be health-related
        inquiry_words = ['help', 'advice', 'recommend', 'suggest', 'what', 'how', 'why', 'when', 'where']
        if any(word in input_lower for word in inquiry_words):
            # If it's a question and doesn't contain obvious off-topic keywords, allow it
            if off_topic_score == 0:
                return True, "General inquiry - likely health-related"
        
        # Only block if it's clearly off-topic
        if off_topic_score > 0 and total_health_score == 0:
            return False, "Clearly off-topic question"
        
        # Default to allowing the question
        return True, "General question - allowing for health coaching"
    
    def get_redirection_message(self, user_input: str) -> str:
        """Generate a polite redirection message for off-topic questions"""
        
        # Check what type of off-topic question it is
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['ai', 'artificial intelligence', 'programming', 'coding']):
            return """
🤖 I'm a specialized Health & Wellness Coach, so I can't help with AI or programming questions.

💡 I can help you with:
• Fitness and exercise routines
• Nutrition and meal planning
• Health goals and progress tracking
• Injury prevention and recovery
• Mental health and wellness
• Weight management and body composition

🎯 Please ask me about health, fitness, nutrition, or wellness topics!
"""
        
        elif any(word in input_lower for word in ['business', 'money', 'finance', 'investment']):
            return """
💰 I'm a Health & Wellness Coach, not a financial advisor.

💡 I can help you with:
• Physical fitness and exercise
• Nutrition and healthy eating
• Mental health and stress management
• Weight loss or muscle gain goals
• Injury prevention and recovery
• Overall wellness and lifestyle

🎯 Please ask me about health, fitness, or wellness topics!
"""
        
        elif any(word in input_lower for word in ['politics', 'government', 'news', 'current events']):
            return """
📰 I'm a Health & Wellness Coach, so I can't discuss politics or current events.

💡 I can help you with:
• Exercise and fitness routines
• Healthy eating and nutrition
• Stress management and mental health
• Physical health and wellness
• Weight management and body goals
• Injury prevention and recovery

🎯 Please ask me about health, fitness, or wellness topics!
"""
        
        elif any(word in input_lower for word in ['movie', 'tv', 'music', 'entertainment', 'game']):
            return """
🎬 I'm a Health & Wellness Coach, not an entertainment expert.

💡 I can help you with:
• Fitness and exercise programs
• Nutrition and meal planning
• Health goals and progress tracking
• Mental health and stress relief
• Physical wellness and lifestyle
• Injury prevention and recovery

🎯 Please ask me about health, fitness, or wellness topics!
"""
        
        else:
            return """
🤔 I'm a specialized Health & Wellness Coach, so I can only help with health and fitness related questions.

💡 I can help you with:
• Exercise and fitness routines
• Nutrition and healthy eating
• Weight management and body goals
• Mental health and stress management
• Injury prevention and recovery
• Overall wellness and lifestyle

🎯 Please ask me about health, fitness, nutrition, or wellness topics!
"""
    
    def validate_user_input(self, user_input: str) -> Dict:
        """
        Validate user input and provide appropriate response
        Returns: {
            'is_valid': bool,
            'message': str,
            'should_proceed': bool
        }
        """
        # Skip validation for very short inputs or empty inputs
        if len(user_input.strip()) < 3:
            return {
                'is_valid': True,
                'message': "Short input - proceeding with health coaching",
                'should_proceed': True
            }
        
        is_related, reason = self.is_health_fitness_related(user_input)
        
        if is_related:
            return {
                'is_valid': True,
                'message': f"✅ {reason} - proceeding with health coaching",
                'should_proceed': True
            }
        else:
            return {
                'is_valid': False,
                'message': self.get_redirection_message(user_input),
                'should_proceed': False
            }

def create_health_guardrails() -> HealthGuardrails:
    """Factory function to create a health guardrails instance"""
    return HealthGuardrails() 