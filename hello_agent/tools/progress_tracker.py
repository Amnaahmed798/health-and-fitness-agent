"""
Progress Tracker Tool
Tracks fitness progress, measurements, and achievements over time
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ProgressTracker:
    def __init__(self):
        self.progress_file = "user_progress.json"
        self.progress_data = self.load_progress()
    
    def load_progress(self) -> Dict:
        """Load existing progress data from file"""
        try:
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "user_info": {},
                "measurements": [],
                "workouts": [],
                "achievements": [],
                "created_date": datetime.now().isoformat()
            }
    
    def save_progress(self):
        """Save progress data to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)
    
    def add_measurement(self, date: str, weight: float = None, body_fat: float = None,
                       chest: float = None, waist: float = None, arms: float = None,
                       thighs: float = None, notes: str = "") -> str:
        """Add a new measurement entry"""
        measurement = {
            "date": date,
            "weight": weight,
            "body_fat": body_fat,
            "chest": chest,
            "waist": waist,
            "arms": arms,
            "thighs": thighs,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        self.progress_data["measurements"].append(measurement)
        self.save_progress()
        
        return f"""
✅ Measurement recorded for {date}!

📊 Measurements:
• Weight: {weight} kg (if provided)
• Body Fat: {body_fat}% (if provided)
• Chest: {chest} cm (if provided)
• Waist: {waist} cm (if provided)
• Arms: {arms} cm (if provided)
• Thighs: {thighs} cm (if provided)

📝 Notes: {notes}
"""
    
    def add_workout(self, date: str, workout_type: str, duration: int, 
                   calories_burned: int = None, notes: str = "") -> str:
        """Add a new workout entry"""
        workout = {
            "date": date,
            "workout_type": workout_type,
            "duration": duration,  # in minutes
            "calories_burned": calories_burned,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        self.progress_data["workouts"].append(workout)
        self.save_progress()
        
        return f"""
💪 Workout logged for {date}!

🏃‍♀️ Workout Details:
• Type: {workout_type}
• Duration: {duration} minutes
• Calories Burned: {calories_burned} (if tracked)
• Notes: {notes}

Keep up the great work! 💪
"""
    
    def add_achievement(self, achievement_type: str, description: str, date: str = None) -> str:
        """Add a new achievement"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        achievement = {
            "type": achievement_type,
            "description": description,
            "date": date,
            "timestamp": datetime.now().isoformat()
        }
        
        self.progress_data["achievements"].append(achievement)
        self.save_progress()
        
        return f"""
🏆 Achievement Unlocked!

🎉 {achievement_type}
📝 {description}
📅 {date}

Congratulations! You're making amazing progress! 🎊
"""
    
    def get_progress_summary(self, days: int = 30) -> str:
        """Get a summary of progress over the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter recent measurements
        recent_measurements = [
            m for m in self.progress_data["measurements"]
            if datetime.fromisoformat(m["date"]) >= start_date
        ]
        
        # Filter recent workouts
        recent_workouts = [
            w for w in self.progress_data["workouts"]
            if datetime.fromisoformat(w["date"]) >= start_date
        ]
        
        # Filter recent achievements
        recent_achievements = [
            a for a in self.progress_data["achievements"]
            if datetime.fromisoformat(a["date"]) >= start_date
        ]
        
        summary = f"""
📊 PROGRESS SUMMARY (Last {days} days)

📈 Measurements: {len(recent_measurements)} entries
💪 Workouts: {len(recent_workouts)} sessions
🏆 Achievements: {len(recent_achievements)} unlocked

"""
        
        if recent_measurements:
            summary += "\n📏 Recent Measurements:\n"
            for m in recent_measurements[-3:]:  # Show last 3
                summary += f"• {m['date']}: "
                if m['weight']:
                    summary += f"Weight: {m['weight']}kg "
                if m['body_fat']:
                    summary += f"Body Fat: {m['body_fat']}% "
                summary += "\n"
        
        if recent_workouts:
            total_duration = sum(w['duration'] for w in recent_workouts)
            total_calories = sum(w.get('calories_burned', 0) for w in recent_workouts)
            summary += f"\n💪 Workout Stats:\n"
            summary += f"• Total sessions: {len(recent_workouts)}\n"
            summary += f"• Total duration: {total_duration} minutes\n"
            summary += f"• Total calories burned: {total_calories}\n"
            summary += f"• Average session: {total_duration//len(recent_workouts)} minutes\n"
        
        if recent_achievements:
            summary += f"\n🏆 Recent Achievements:\n"
            for a in recent_achievements[-3:]:  # Show last 3
                summary += f"• {a['date']}: {a['description']}\n"
        
        return summary
    
    def get_measurement_trends(self) -> str:
        """Analyze measurement trends"""
        if len(self.progress_data["measurements"]) < 2:
            return "📝 Need at least 2 measurements to show trends."
        
        measurements = sorted(self.progress_data["measurements"], key=lambda x: x["date"])
        
        trends = "📈 MEASUREMENT TRENDS\n\n"
        
        # Weight trends
        weight_measurements = [m for m in measurements if m.get('weight')]
        if len(weight_measurements) >= 2:
            first_weight = weight_measurements[0]['weight']
            last_weight = weight_measurements[-1]['weight']
            weight_change = last_weight - first_weight
            
            trends += f"⚖️ Weight Trend:\n"
            trends += f"• Started: {first_weight} kg\n"
            trends += f"• Current: {last_weight} kg\n"
            trends += f"• Change: {weight_change:+.1f} kg\n"
            
            if weight_change > 0:
                trends += "📈 Weight increased\n"
            elif weight_change < 0:
                trends += "📉 Weight decreased\n"
            else:
                trends += "➡️ Weight maintained\n"
        
        # Body fat trends
        body_fat_measurements = [m for m in measurements if m.get('body_fat')]
        if len(body_fat_measurements) >= 2:
            first_bf = body_fat_measurements[0]['body_fat']
            last_bf = body_fat_measurements[-1]['body_fat']
            bf_change = last_bf - first_bf
            
            trends += f"\n📊 Body Fat Trend:\n"
            trends += f"• Started: {first_bf}%\n"
            trends += f"• Current: {last_bf}%\n"
            trends += f"• Change: {bf_change:+.1f}%\n"
        
        return trends
    
    def get_workout_analytics(self) -> str:
        """Analyze workout patterns"""
        if not self.progress_data["workouts"]:
            return "📝 No workouts recorded yet."
        
        workouts = self.progress_data["workouts"]
        
        # Workout type frequency
        workout_types = {}
        for workout in workouts:
            workout_type = workout['workout_type']
            workout_types[workout_type] = workout_types.get(workout_type, 0) + 1
        
        analytics = "💪 WORKOUT ANALYTICS\n\n"
        analytics += f"📊 Total workouts: {len(workouts)}\n"
        
        total_duration = sum(w['duration'] for w in workouts)
        total_calories = sum(w.get('calories_burned', 0) for w in workouts)
        
        analytics += f"⏱️ Total time: {total_duration} minutes ({total_duration//60} hours)\n"
        analytics += f"🔥 Total calories burned: {total_calories}\n"
        analytics += f"📈 Average session: {total_duration//len(workouts)} minutes\n\n"
        
        analytics += "🏃‍♀️ Workout Type Breakdown:\n"
        for workout_type, count in sorted(workout_types.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(workouts)) * 100
            analytics += f"• {workout_type}: {count} sessions ({percentage:.1f}%)\n"
        
        return analytics

def create_progress_tracker() -> ProgressTracker:
    """Factory function to create a progress tracker instance"""
    return ProgressTracker() 