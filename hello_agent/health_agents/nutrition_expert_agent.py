"""
Nutrition Expert Agent
Provides detailed nutritional advice, meal planning, and dietary recommendations
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class NutritionExpertAgent:
    def __init__(self):
        self.nutrition_log_file = "nutrition_log.json"
        self.nutrition_log = self.load_nutrition_log()
        self.nutrition_database = self.load_nutrition_database()
    
    def load_nutrition_log(self) -> Dict:
        """Load nutrition log from file"""
        try:
            with open(self.nutrition_log_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"consultations": [], "created_date": datetime.now().isoformat()}
    
    def save_nutrition_log(self):
        """Save nutrition log to file"""
        with open(self.nutrition_log_file, 'w') as f:
            json.dump(self.nutrition_log, f, indent=2)
    
    def load_nutrition_database(self) -> Dict:
        """Load nutrition database"""
        return {
            "macronutrients": {
                "protein": {
                    "function": "Building and repairing tissues, muscle growth",
                    "sources": ["lean meats", "fish", "eggs", "dairy", "legumes", "nuts"],
                    "daily_intake": "0.8-2.2g per kg body weight",
                    "calories_per_gram": 4
                },
                "carbohydrates": {
                    "function": "Primary energy source, brain fuel",
                    "sources": ["whole grains", "fruits", "vegetables", "legumes"],
                    "daily_intake": "45-65% of total calories",
                    "calories_per_gram": 4
                },
                "fats": {
                    "function": "Energy storage, hormone production, nutrient absorption",
                    "sources": ["avocados", "nuts", "olive oil", "fatty fish", "seeds"],
                    "daily_intake": "20-35% of total calories",
                    "calories_per_gram": 9
                }
            },
            "micronutrients": {
                "vitamins": {
                    "A": {"function": "Vision, immune system", "sources": ["carrots", "sweet potatoes", "spinach"]},
                    "C": {"function": "Immune system, collagen production", "sources": ["citrus fruits", "bell peppers", "broccoli"]},
                    "D": {"function": "Bone health, immune system", "sources": ["sunlight", "fatty fish", "fortified dairy"]},
                    "E": {"function": "Antioxidant, cell protection", "sources": ["nuts", "seeds", "vegetable oils"]},
                    "K": {"function": "Blood clotting, bone health", "sources": ["leafy greens", "broccoli", "soybeans"]},
                    "B12": {"function": "Nerve function, red blood cells", "sources": ["meat", "fish", "dairy", "fortified foods"]}
                },
                "minerals": {
                    "calcium": {"function": "Bone health, muscle function", "sources": ["dairy", "leafy greens", "fortified foods"]},
                    "iron": {"function": "Oxygen transport, energy production", "sources": ["red meat", "beans", "fortified cereals"]},
                    "zinc": {"function": "Immune system, wound healing", "sources": ["meat", "shellfish", "legumes"]},
                    "magnesium": {"function": "Muscle function, energy production", "sources": ["nuts", "seeds", "whole grains"]}
                }
            },
            "dietary_patterns": {
                "mediterranean": {
                    "description": "Heart-healthy diet rich in fruits, vegetables, whole grains, and healthy fats",
                    "benefits": ["Heart health", "Longevity", "Brain health"],
                    "key_foods": ["olive oil", "fish", "vegetables", "whole grains", "nuts"]
                },
                "plant_based": {
                    "description": "Diet focused on plant foods with limited or no animal products",
                    "benefits": ["Heart health", "Environmental impact", "Lower cholesterol"],
                    "key_foods": ["legumes", "whole grains", "vegetables", "fruits", "nuts"]
                },
                "keto": {
                    "description": "High-fat, low-carbohydrate diet for weight loss and metabolic health",
                    "benefits": ["Weight loss", "Blood sugar control", "Mental clarity"],
                    "key_foods": ["meat", "fish", "eggs", "dairy", "nuts", "low-carb vegetables"]
                },
                "paleo": {
                    "description": "Diet based on foods presumed to be available to Paleolithic humans",
                    "benefits": ["Weight loss", "Inflammation reduction", "Blood sugar control"],
                    "key_foods": ["lean meats", "fish", "fruits", "vegetables", "nuts", "seeds"]
                }
            }
        }
    
    def provide_nutrition_consultation(self, user_info: Dict, nutrition_question: str, 
                                     dietary_restrictions: List[str] = None) -> str:
        """Provide comprehensive nutrition consultation"""
        
        # Log the consultation
        consultation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_info": user_info,
            "nutrition_question": nutrition_question,
            "dietary_restrictions": dietary_restrictions or [],
            "status": "consulted"
        }
        
        self.nutrition_log["consultations"].append(consultation_entry)
        self.save_nutrition_log()
        
        response = f"""
🥗 NUTRITION EXPERT CONSULTATION

📋 **Consultation Details:**
• Question: {nutrition_question}
• User Profile: Age {user_info.get('age', 'Not specified')}, Fitness Level {user_info.get('fitness_level', 'Not specified')}
• Goals: {user_info.get('health_goals', 'Not specified')}
• Dietary Restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None specified'}
• Consultation Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

"""
        
        # Add specific nutrition advice based on the question
        if any(word in nutrition_question.lower() for word in ['protein', 'muscle', 'strength']):
            response += self.get_protein_advice(user_info)
        elif any(word in nutrition_question.lower() for word in ['weight loss', 'lose weight', 'calories']):
            response += self.get_weight_loss_advice(user_info)
        elif any(word in nutrition_question.lower() for word in ['vitamin', 'mineral', 'supplement']):
            response += self.get_micronutrient_advice(user_info)
        elif any(word in nutrition_question.lower() for word in ['diet', 'meal plan', 'eating']):
            response += self.get_dietary_pattern_advice(user_info, dietary_restrictions)
        else:
            response += self.get_general_nutrition_advice(user_info)
        
        response += f"""
💡 **General Nutrition Tips:**

1. **Hydration:** Drink 8-10 glasses of water daily
2. **Meal Timing:** Eat every 3-4 hours to maintain energy
3. **Portion Control:** Use your hand as a guide for portions
4. **Food Quality:** Choose whole, unprocessed foods when possible
5. **Consistency:** Focus on sustainable habits over quick fixes

⚠️ **Important Notes:**
• This advice is for general health and wellness
• Consult a registered dietitian for personalized meal plans
• Consider medical conditions and medications
• Always consult healthcare providers for medical nutrition therapy
"""
        
        return response
    
    def get_protein_advice(self, user_info: Dict) -> str:
        """Get protein-specific nutrition advice"""
        age = user_info.get('age', 25)
        fitness_level = user_info.get('fitness_level', 'beginner')
        health_goals = user_info.get('health_goals', 'general fitness')
        
        protein_advice = f"""
💪 **PROTEIN NUTRITION GUIDE**

📊 **Your Protein Needs:**
"""
        
        if 'muscle gain' in health_goals.lower():
            protein_advice += "• Target: 1.6-2.2g protein per kg body weight\n"
            protein_advice += "• Focus: Muscle building and recovery\n"
        elif 'weight loss' in health_goals.lower():
            protein_advice += "• Target: 1.2-1.6g protein per kg body weight\n"
            protein_advice += "• Focus: Preserving muscle mass during weight loss\n"
        else:
            protein_advice += "• Target: 0.8-1.2g protein per kg body weight\n"
            protein_advice += "• Focus: General health and maintenance\n"
        
        protein_advice += f"""
🥩 **Best Protein Sources:**

**Animal Sources:**
• Lean chicken breast (31g protein per 100g)
• Turkey breast (29g protein per 100g)
• Fish (salmon, tuna, cod)
• Eggs (6g protein per egg)
• Greek yogurt (17g protein per 170g)

**Plant Sources:**
• Lentils (9g protein per 100g cooked)
• Chickpeas (9g protein per 100g cooked)
• Quinoa (4g protein per 100g cooked)
• Tofu (8g protein per 100g)
• Nuts and seeds (almonds, chia seeds)

⏰ **Timing Recommendations:**
• Distribute protein intake throughout the day
• Include protein in every meal
• Consume protein within 30 minutes after workouts
• Aim for 20-30g protein per meal
"""
        
        return protein_advice
    
    def get_weight_loss_advice(self, user_info: Dict) -> str:
        """Get weight loss nutrition advice"""
        age = user_info.get('age', 25)
        
        weight_loss_advice = f"""
⚖️ **WEIGHT LOSS NUTRITION STRATEGY**

📊 **Calorie Management:**
• Create a 300-500 calorie daily deficit
• Focus on nutrient-dense, low-calorie foods
• Track your intake to ensure consistency

🥗 **Food Choices for Weight Loss:**

**High-Volume, Low-Calorie Foods:**
• Vegetables (especially leafy greens)
• Fruits (berries, apples, citrus)
• Lean proteins (chicken, fish, eggs)
• Whole grains (quinoa, oats, brown rice)

**Foods to Limit:**
• Processed foods and added sugars
• Refined carbohydrates
• High-calorie beverages
• Excessive portion sizes

⏰ **Meal Timing:**
• Eat breakfast within 1 hour of waking
• Include protein and fiber in every meal
• Don't skip meals to avoid overeating later
• Consider intermittent fasting if appropriate

💧 **Hydration:**
• Drink water before meals to reduce hunger
• Aim for 8-10 glasses daily
• Limit sugary beverages
"""
        
        return weight_loss_advice
    
    def get_micronutrient_advice(self, user_info: Dict) -> str:
        """Get micronutrient advice"""
        
        micronutrient_advice = f"""
🔬 **MICRONUTRIENT GUIDE**

**Essential Vitamins:**

**Vitamin D:**
• Function: Bone health, immune system
• Sources: Sunlight, fatty fish, fortified dairy
• Daily: 600-800 IU (15-20 mcg)

**Vitamin C:**
• Function: Immune system, collagen production
• Sources: Citrus fruits, bell peppers, broccoli
• Daily: 75-90mg

**B Vitamins:**
• Function: Energy production, nerve function
• Sources: Whole grains, meat, dairy, legumes
• Daily: Varies by specific B vitamin

**Essential Minerals:**

**Calcium:**
• Function: Bone health, muscle function
• Sources: Dairy, leafy greens, fortified foods
• Daily: 1000-1200mg

**Iron:**
• Function: Oxygen transport, energy
• Sources: Red meat, beans, fortified cereals
• Daily: 8-18mg (varies by gender)

**Magnesium:**
• Function: Muscle function, energy production
• Sources: Nuts, seeds, whole grains
• Daily: 310-420mg

💊 **Supplementation:**
• Focus on food sources first
• Consider supplements only if deficient
• Consult healthcare provider before starting supplements
• Get blood work to check levels if concerned
"""
        
        return micronutrient_advice
    
    def get_dietary_pattern_advice(self, user_info: Dict, dietary_restrictions: List[str] = None) -> str:
        """Get dietary pattern advice"""
        
        dietary_advice = f"""
🍽️ **DIETARY PATTERN RECOMMENDATIONS**

**Based on your profile and restrictions, here are suitable dietary patterns:**

**1. Mediterranean Diet:**
• Best for: Heart health, longevity, general wellness
• Key foods: Olive oil, fish, vegetables, whole grains, nuts
• Benefits: Reduced heart disease risk, brain health

**2. Plant-Based Diet:**
• Best for: Heart health, environmental impact
• Key foods: Legumes, whole grains, vegetables, fruits
• Benefits: Lower cholesterol, reduced inflammation

**3. Balanced Macronutrient Diet:**
• Best for: General fitness, sustainable weight management
• Key foods: Mix of proteins, carbs, and healthy fats
• Benefits: Sustainable, flexible, meets most needs

**4. High-Protein Diet:**
• Best for: Muscle building, weight loss, satiety
• Key foods: Lean meats, fish, eggs, dairy, legumes
• Benefits: Muscle preservation, increased metabolism

📋 **Personalized Recommendations:**
• Start with small changes
• Focus on whole, unprocessed foods
• Include variety for nutrient adequacy
• Consider your lifestyle and preferences
• Monitor how you feel and adjust accordingly
"""
        
        return dietary_advice
    
    def get_general_nutrition_advice(self, user_info: Dict) -> str:
        """Get general nutrition advice"""
        
        general_advice = f"""
🥗 **GENERAL NUTRITION GUIDELINES**

**Daily Nutrition Goals:**

**1. Macronutrient Balance:**
• Carbohydrates: 45-65% of total calories
• Protein: 10-35% of total calories
• Fats: 20-35% of total calories

**2. Food Groups to Include:**
• Fruits and vegetables (5-9 servings daily)
• Whole grains (3-6 servings daily)
• Lean proteins (2-3 servings daily)
• Healthy fats (2-4 servings daily)
• Dairy or alternatives (2-3 servings daily)

**3. Hydration:**
• Water: 8-10 glasses daily
• More if exercising or in hot weather
• Limit sugary beverages

**4. Meal Planning Tips:**
• Plan meals ahead of time
• Include protein and fiber in every meal
• Eat mindfully and slowly
• Listen to hunger and fullness cues
• Don't skip meals

**5. Healthy Eating Habits:**
• Eat breakfast daily
• Include variety in your diet
• Limit processed foods
• Cook at home when possible
• Practice portion control
"""
        
        return general_advice
    
    def get_nutrition_history(self) -> str:
        """Get nutrition consultation history"""
        if not self.nutrition_log["consultations"]:
            return "📝 No nutrition consultations recorded."
        
        history = "📋 NUTRITION CONSULTATION HISTORY\n\n"
        
        for i, consultation in enumerate(self.nutrition_log["consultations"], 1):
            date = datetime.fromisoformat(consultation["timestamp"]).strftime("%B %d, %Y at %I:%M %p")
            history += f"{i}. {date}\n"
            history += f"   Question: {consultation['nutrition_question']}\n"
            history += f"   Restrictions: {', '.join(consultation['dietary_restrictions']) if consultation['dietary_restrictions'] else 'None'}\n"
            history += f"   Status: {consultation['status']}\n\n"
        
        return history

def create_nutrition_expert_agent() -> NutritionExpertAgent:
    """Factory function to create a nutrition expert agent instance"""
    return NutritionExpertAgent() 