"""
Goal Analyzer Tool
Helps users set, analyze, and track their health and fitness goals
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class GoalAnalyzer:
    def __init__(self):
        self.goals_file = "user_goals.json"
        self.goals = self.load_goals()
    
    def load_goals(self) -> Dict:
        """Load existing goals from file"""
        try:
            with open(self.goals_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"goals": [], "created_date": datetime.now().isoformat()}
    
    def save_goals(self):
        """Save goals to file"""
        with open(self.goals_file, 'w') as f:
            json.dump(self.goals, f, indent=2)
    
    def analyze_user_input(self, user_info: Dict) -> str:
        """Analyze user information and provide goal recommendations"""
        age = user_info.get('age', 25)
        fitness_level = user_info.get('fitness_level', 'beginner')
        health_goals = user_info.get('health_goals', 'general fitness')
        
        analysis = f"""
🎯 GOAL ANALYSIS REPORT

📊 Your Profile:
• Age: {age} years old
• Fitness Level: {fitness_level}
• Current Goals: {health_goals}

💡 Recommended SMART Goals:
"""
        
        # Age-based recommendations
        if age < 30:
            analysis += "• High-intensity workouts 3-4 times per week\n"
            analysis += "• Focus on building strength and endurance\n"
        elif age < 50:
            analysis += "• Moderate cardio 3-4 times per week\n"
            analysis += "• Strength training 2-3 times per week\n"
        else:
            analysis += "• Low-impact cardio 4-5 times per week\n"
            analysis += "• Focus on flexibility and balance\n"
        
        # Fitness level recommendations
        if fitness_level == 'beginner':
            analysis += "• Start with 20-30 minute sessions\n"
            analysis += "• Focus on form and consistency\n"
        elif fitness_level == 'intermediate':
            analysis += "• 45-60 minute sessions\n"
            analysis += "• Mix of cardio and strength training\n"
        else:
            analysis += "• Advanced training programs\n"
            analysis += "• Consider hiring a personal trainer\n"
        
        # Goal-specific recommendations
        if 'weight loss' in health_goals.lower():
            analysis += "• Create a 300-500 calorie daily deficit\n"
            analysis += "• Combine cardio and strength training\n"
        elif 'muscle gain' in health_goals.lower():
            analysis += "• Progressive overload in strength training\n"
            analysis += "• Adequate protein intake (1.6-2.2g per kg body weight)\n"
        elif 'general fitness' in health_goals.lower():
            analysis += "• Balanced routine of cardio, strength, and flexibility\n"
            analysis += "• Focus on overall health and well-being\n"
        
        analysis += "\n📈 Success Metrics to Track:\n"
        analysis += "• Weekly progress photos\n"
        analysis += "• Body measurements every 2 weeks\n"
        analysis += "• Workout consistency (aim for 80%+)\n"
        analysis += "• Energy levels and mood improvements\n"
        
        return analysis
    
    def set_smart_goal(self, goal_type: str, target: str, timeframe: str) -> str:
        """Set a SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goal"""
        goal = {
            "type": goal_type,
            "target": target,
            "timeframe": timeframe,
            "created_date": datetime.now().isoformat(),
            "status": "active",
            "progress": 0
        }
        
        self.goals["goals"].append(goal)
        self.save_goals()
        
        return f"""
✅ SMART Goal Set Successfully!

🎯 Goal: {goal_type}
📊 Target: {target}
⏰ Timeframe: {timeframe}
📅 Created: {datetime.now().strftime('%B %d, %Y')}

💪 Tips for Success:
• Break down your goal into smaller milestones
• Track your progress weekly
• Celebrate small wins along the way
• Stay consistent with your routine
"""
    
    def get_goal_progress(self) -> str:
        """Get current goal progress"""
        if not self.goals["goals"]:
            return "📝 No goals set yet. Use 'set_goal' to create your first goal!"
        
        progress_report = "📊 GOAL PROGRESS REPORT\n\n"
        
        for i, goal in enumerate(self.goals["goals"], 1):
            progress_report += f"{i}. {goal['type']}\n"
            progress_report += f"   Target: {goal['target']}\n"
            progress_report += f"   Timeframe: {goal['timeframe']}\n"
            progress_report += f"   Progress: {goal['progress']}%\n"
            progress_report += f"   Status: {goal['status']}\n\n"
        
        return progress_report
    
    def update_progress(self, goal_index: int, progress_percentage: int) -> str:
        """Update goal progress"""
        if 0 <= goal_index < len(self.goals["goals"]):
            self.goals["goals"][goal_index]["progress"] = progress_percentage
            
            if progress_percentage >= 100:
                self.goals["goals"][goal_index]["status"] = "completed"
            
            self.save_goals()
            return f"✅ Progress updated! Goal {goal_index + 1} is now {progress_percentage}% complete."
        else:
            return "❌ Invalid goal index. Please check your goal list."

def create_goal_analyzer() -> GoalAnalyzer:
    """Factory function to create a goal analyzer instance"""
    return GoalAnalyzer() 