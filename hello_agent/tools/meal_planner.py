"""
Meal Planner Tool
Generates personalized meal plans based on user goals, preferences, and dietary restrictions
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class MealPlanner:
    def __init__(self):
        self.meal_plans_file = "meal_plans.json"
        self.meal_plans = self.load_meal_plans()
        self.recipes = self.load_recipes()
    
    def load_meal_plans(self) -> Dict:
        """Load existing meal plans from file"""
        try:
            with open(self.meal_plans_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"plans": [], "created_date": datetime.now().isoformat()}
    
    def save_meal_plans(self):
        """Save meal plans to file"""
        with open(self.meal_plans_file, 'w') as f:
            json.dump(self.meal_plans, f, indent=2)
    
    def load_recipes(self) -> Dict:
        """Load recipe database"""
        return {
            "breakfast": {
                "protein_pancakes": {
                    "name": "Protein Pancakes",
                    "calories": 350,
                    "protein": 25,
                    "carbs": 30,
                    "fat": 12,
                    "ingredients": ["oats", "protein powder", "eggs", "banana"],
                    "instructions": "Blend ingredients, cook on griddle",
                    "dietary": ["vegetarian"]
                },
                "greek_yogurt_bowl": {
                    "name": "Greek Yogurt Bowl",
                    "calories": 280,
                    "protein": 20,
                    "carbs": 25,
                    "fat": 8,
                    "ingredients": ["greek yogurt", "berries", "honey", "nuts"],
                    "instructions": "Mix yogurt with toppings",
                    "dietary": ["vegetarian"]
                },
                "oatmeal_banana": {
                    "name": "Banana Oatmeal",
                    "calories": 320,
                    "protein": 12,
                    "carbs": 55,
                    "fat": 6,
                    "ingredients": ["oats", "banana", "milk", "cinnamon"],
                    "instructions": "Cook oats with milk, add banana",
                    "dietary": ["vegetarian"]
                },
                "tofu_scramble": {
                    "name": "Tofu Scramble",
                    "calories": 300,
                    "protein": 20,
                    "carbs": 15,
                    "fat": 18,
                    "ingredients": ["tofu", "vegetables", "turmeric", "olive oil"],
                    "instructions": "Scramble tofu with vegetables and spices",
                    "dietary": ["vegetarian", "vegan"]
                },
                "chia_pudding": {
                    "name": "Chia Pudding",
                    "calories": 250,
                    "protein": 8,
                    "carbs": 35,
                    "fat": 10,
                    "ingredients": ["chia seeds", "almond milk", "berries", "honey"],
                    "instructions": "Mix chia with milk, refrigerate overnight",
                    "dietary": ["vegetarian", "vegan"]
                }
            },
            "lunch": {
                "grilled_chicken_salad": {
                    "name": "Grilled Chicken Salad",
                    "calories": 420,
                    "protein": 35,
                    "carbs": 15,
                    "fat": 18,
                    "ingredients": ["chicken breast", "mixed greens", "olive oil", "vegetables"],
                    "instructions": "Grill chicken, assemble salad",
                    "dietary": ["none"]
                },
                "quinoa_bowl": {
                    "name": "Quinoa Protein Bowl",
                    "calories": 380,
                    "protein": 18,
                    "carbs": 45,
                    "fat": 12,
                    "ingredients": ["quinoa", "black beans", "vegetables", "avocado"],
                    "instructions": "Cook quinoa, mix with beans and vegetables",
                    "dietary": ["vegetarian", "vegan"]
                },
                "tuna_sandwich": {
                    "name": "Tuna Sandwich",
                    "calories": 340,
                    "protein": 22,
                    "carbs": 35,
                    "fat": 10,
                    "ingredients": ["tuna", "whole grain bread", "mayo", "vegetables"],
                    "instructions": "Mix tuna with mayo, serve on bread",
                    "dietary": ["none"]
                },
                "chickpea_salad": {
                    "name": "Chickpea Salad",
                    "calories": 320,
                    "protein": 15,
                    "carbs": 40,
                    "fat": 12,
                    "ingredients": ["chickpeas", "vegetables", "olive oil", "lemon"],
                    "instructions": "Mix chickpeas with vegetables and dressing",
                    "dietary": ["vegetarian", "vegan"]
                },
                "tempeh_wrap": {
                    "name": "Tempeh Wrap",
                    "calories": 360,
                    "protein": 20,
                    "carbs": 35,
                    "fat": 15,
                    "ingredients": ["tempeh", "whole grain wrap", "vegetables", "hummus"],
                    "instructions": "Grill tempeh, wrap with vegetables and hummus",
                    "dietary": ["vegetarian", "vegan"]
                }
            },
            "dinner": {
                "salmon_vegetables": {
                    "name": "Baked Salmon with Vegetables",
                    "calories": 450,
                    "protein": 40,
                    "carbs": 20,
                    "fat": 22,
                    "ingredients": ["salmon", "broccoli", "sweet potato", "olive oil"],
                    "instructions": "Bake salmon with vegetables",
                    "dietary": ["none"]
                },
                "lean_beef_stirfry": {
                    "name": "Lean Beef Stir Fry",
                    "calories": 380,
                    "protein": 35,
                    "carbs": 25,
                    "fat": 15,
                    "ingredients": ["lean beef", "brown rice", "vegetables", "soy sauce"],
                    "instructions": "Stir fry beef with vegetables and rice",
                    "dietary": ["none"]
                },
                "vegetarian_lentils": {
                    "name": "Lentil Curry",
                    "calories": 320,
                    "protein": 18,
                    "carbs": 50,
                    "fat": 8,
                    "ingredients": ["lentils", "brown rice", "vegetables", "spices"],
                    "instructions": "Cook lentils with spices and vegetables",
                    "dietary": ["vegetarian", "vegan"]
                },
                "tofu_stirfry": {
                    "name": "Tofu Stir Fry",
                    "calories": 350,
                    "protein": 20,
                    "carbs": 30,
                    "fat": 15,
                    "ingredients": ["tofu", "brown rice", "vegetables", "soy sauce"],
                    "instructions": "Stir fry tofu with vegetables and rice",
                    "dietary": ["vegetarian", "vegan"]
                },
                "chickpea_curry": {
                    "name": "Chickpea Curry",
                    "calories": 340,
                    "protein": 16,
                    "carbs": 45,
                    "fat": 12,
                    "ingredients": ["chickpeas", "quinoa", "vegetables", "coconut milk"],
                    "instructions": "Cook chickpeas in coconut curry sauce",
                    "dietary": ["vegetarian", "vegan"]
                }
            },
            "snacks": {
                "protein_smoothie": {
                    "name": "Protein Smoothie",
                    "calories": 220,
                    "protein": 25,
                    "carbs": 20,
                    "fat": 5,
                    "ingredients": ["protein powder", "banana", "milk", "peanut butter"],
                    "instructions": "Blend all ingredients",
                    "dietary": ["vegetarian"]
                },
                "nuts_fruit": {
                    "name": "Nuts and Fruit",
                    "calories": 180,
                    "protein": 6,
                    "carbs": 25,
                    "fat": 8,
                    "ingredients": ["almonds", "apple", "dried fruit"],
                    "instructions": "Mix nuts with fruit",
                    "dietary": ["vegetarian", "vegan"]
                },
                "hummus_veggies": {
                    "name": "Hummus with Vegetables",
                    "calories": 150,
                    "protein": 8,
                    "carbs": 20,
                    "fat": 6,
                    "ingredients": ["hummus", "carrots", "cucumber", "bell peppers"],
                    "instructions": "Serve hummus with fresh vegetables",
                    "dietary": ["vegetarian", "vegan"]
                }
            }
        }
    
    def generate_meal_plan(self, user_info: Dict, days: int = 7, dietary_restrictions: List[str] = None) -> str:
        """Generate a personalized meal plan"""
        age = user_info.get('age', 25)
        fitness_level = user_info.get('fitness_level', 'beginner')
        health_goals = user_info.get('health_goals', 'general fitness')
        
        # Check for dietary restrictions in user question or info
        if not dietary_restrictions:
            dietary_restrictions = []
            # Check if user mentioned dietary preferences
            if 'vegetarian' in str(user_info).lower():
                dietary_restrictions.append('vegetarian')
            if 'vegan' in str(user_info).lower():
                dietary_restrictions.append('vegan')
        
        # Calculate daily calorie needs based on age and goals
        base_calories = 2000 if age < 30 else 1800
        
        if 'weight loss' in health_goals.lower():
            daily_calories = base_calories - 300
        elif 'muscle gain' in health_goals.lower():
            daily_calories = base_calories + 300
        else:
            daily_calories = base_calories
        
        meal_plan = {
            "user_info": user_info,
            "daily_calories": daily_calories,
            "days": days,
            "dietary_restrictions": dietary_restrictions,
            "created_date": datetime.now().isoformat(),
            "meals": {}
        }
        
        plan_text = f"""
🍽️ PERSONALIZED MEAL PLAN

📊 Daily Target: {daily_calories} calories
🎯 Goal: {health_goals}
⏰ Duration: {days} days
🥗 Dietary Restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}

"""
        
        for day in range(1, days + 1):
            day_meals = self.generate_daily_meals(daily_calories, health_goals, dietary_restrictions)
            meal_plan["meals"][f"day_{day}"] = day_meals
            
            plan_text += f"\n📅 DAY {day}:\n"
            plan_text += "=" * 30 + "\n"
            
            for meal_type, meal in day_meals.items():
                plan_text += f"\n🌅 {meal_type.upper()}:\n"
                plan_text += f"   {meal['name']}\n"
                plan_text += f"   Calories: {meal['calories']}\n"
                plan_text += f"   Protein: {meal['protein']}g | Carbs: {meal['carbs']}g | Fat: {meal['fat']}g\n"
                plan_text += f"   Ingredients: {', '.join(meal['ingredients'])}\n"
                plan_text += f"   Instructions: {meal['instructions']}\n"
                if 'dietary' in meal:
                    plan_text += f"   Dietary: {', '.join(meal['dietary'])}\n"
        
        # Save the meal plan
        self.meal_plans["plans"].append(meal_plan)
        self.save_meal_plans()
        
        plan_text += f"\n💡 Tips:\n"
        plan_text += "• Prep meals in advance to save time\n"
        plan_text += "• Drink 8-10 glasses of water daily\n"
        plan_text += "• Adjust portions based on your hunger levels\n"
        plan_text += "• Listen to your body's signals\n"
        
        if dietary_restrictions:
            plan_text += f"\n🥗 Dietary Notes:\n"
            if 'vegetarian' in dietary_restrictions:
                plan_text += "• Focus on plant-based proteins like legumes, tofu, and quinoa\n"
                plan_text += "• Include dairy and eggs for additional protein\n"
            if 'vegan' in dietary_restrictions:
                plan_text += "• Ensure adequate B12 intake through fortified foods or supplements\n"
                plan_text += "• Combine grains and legumes for complete protein\n"
        
        return plan_text
    
    def generate_daily_meals(self, daily_calories: int, health_goals: str, dietary_restrictions: List[str] = None) -> Dict:
        """Generate meals for one day"""
        import random
        
        # Calorie distribution
        breakfast_calories = int(daily_calories * 0.25)
        lunch_calories = int(daily_calories * 0.35)
        dinner_calories = int(daily_calories * 0.30)
        snack_calories = int(daily_calories * 0.10)
        
        # Select meals based on calorie targets, goals, and dietary restrictions
        breakfast = self.select_meal("breakfast", breakfast_calories, health_goals, dietary_restrictions)
        lunch = self.select_meal("lunch", lunch_calories, health_goals, dietary_restrictions)
        dinner = self.select_meal("dinner", dinner_calories, health_goals, dietary_restrictions)
        snack = self.select_meal("snacks", snack_calories, health_goals, dietary_restrictions)
        
        return {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "snack": snack
        }
    
    def select_meal(self, meal_type: str, target_calories: int, health_goals: str, dietary_restrictions: List[str] = None) -> Dict:
        """Select appropriate meal based on calories, goals, and dietary restrictions"""
        available_meals = self.recipes[meal_type]
        
        # Filter meals based on dietary restrictions
        suitable_meals = []
        for meal_id, meal in available_meals.items():
            # Check dietary restrictions
            if dietary_restrictions:
                meal_dietary = meal.get('dietary', ['none'])
                if not any(diet in meal_dietary for diet in dietary_restrictions):
                    continue
            
            # Filter meals based on goals
            if 'weight loss' in health_goals.lower():
                if meal['calories'] <= target_calories + 50:
                    suitable_meals.append(meal)
            elif 'muscle gain' in health_goals.lower():
                if meal['protein'] >= 15:  # High protein for muscle gain
                    suitable_meals.append(meal)
            else:
                suitable_meals.append(meal)
        
        if not suitable_meals:
            # Fallback to any meals that match dietary restrictions
            for meal_id, meal in available_meals.items():
                if dietary_restrictions:
                    meal_dietary = meal.get('dietary', ['none'])
                    if any(diet in meal_dietary for diet in dietary_restrictions):
                        suitable_meals.append(meal)
                else:
                    suitable_meals.append(meal)
        
        if not suitable_meals:
            suitable_meals = list(available_meals.values())
        
        # Select random meal from suitable options
        import random
        return random.choice(suitable_meals)
    
    def get_meal_plan_history(self) -> str:
        """Get history of meal plans"""
        if not self.meal_plans["plans"]:
            return "📝 No meal plans created yet. Use 'generate_plan' to create your first meal plan!"
        
        history = "📋 MEAL PLAN HISTORY\n\n"
        
        for i, plan in enumerate(self.meal_plans["plans"], 1):
            history += f"{i}. Plan created on {plan['created_date'][:10]}\n"
            history += f"   Daily calories: {plan['daily_calories']}\n"
            history += f"   Duration: {plan['days']} days\n"
            history += f"   Goal: {plan['user_info'].get('health_goals', 'Not specified')}\n\n"
        
        return history
    
    def get_shopping_list(self, plan_index: int = -1) -> str:
        """Generate shopping list for a meal plan"""
        if not self.meal_plans["plans"]:
            return "📝 No meal plans available to generate shopping list."
        
        plan = self.meal_plans["plans"][plan_index]
        all_ingredients = set()
        
        for day_meals in plan["meals"].values():
            for meal in day_meals.values():
                all_ingredients.update(meal['ingredients'])
        
        shopping_list = "🛒 SHOPPING LIST\n\n"
        shopping_list += "📦 Ingredients needed:\n"
        
        for ingredient in sorted(all_ingredients):
            shopping_list += f"• {ingredient}\n"
        
        shopping_list += f"\n📊 For {plan['days']} days of meals\n"
        shopping_list += f"🎯 Target: {plan['daily_calories']} calories per day\n"
        
        return shopping_list

def create_meal_planner() -> MealPlanner:
    """Factory function to create a meal planner instance"""
    return MealPlanner() 