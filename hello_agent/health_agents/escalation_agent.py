"""
Escalation Agent
Handles requests to speak with human support and provides escalation procedures
"""

import json
from datetime import datetime
from typing import Dict, List

class EscalationAgent:
    def __init__(self):
        self.escalation_log_file = "escalation_log.json"
        self.escalation_log = self.load_escalation_log()
        self.support_contacts = {
            "general": {
                "phone": "1-800-HEALTH-1",
                "email": "support@healthcoach.com",
                "hours": "Monday-Friday 9AM-6PM EST"
            },
            "medical": {
                "phone": "1-800-MEDICAL-1",
                "email": "medical@healthcoach.com",
                "hours": "24/7 Emergency Support"
            },
            "nutrition": {
                "phone": "1-800-NUTRITION-1",
                "email": "nutrition@healthcoach.com",
                "hours": "Monday-Friday 8AM-5PM EST"
            },
            "fitness": {
                "phone": "1-800-FITNESS-1",
                "email": "fitness@healthcoach.com",
                "hours": "Monday-Saturday 7AM-8PM EST"
            }
        }
    
    def load_escalation_log(self) -> Dict:
        """Load escalation log from file"""
        try:
            with open(self.escalation_log_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"escalations": [], "created_date": datetime.now().isoformat()}
    
    def save_escalation_log(self):
        """Save escalation log to file"""
        with open(self.escalation_log_file, 'w') as f:
            json.dump(self.escalation_log, f, indent=2)
    
    def handle_escalation_request(self, user_info: Dict, reason: str = "General inquiry") -> str:
        """Handle escalation request and provide human support options"""
        
        # Log the escalation request
        escalation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_info": user_info,
            "reason": reason,
            "status": "pending"
        }
        
        self.escalation_log["escalations"].append(escalation_entry)
        self.save_escalation_log()
        
        response = f"""
🔄 ESCALATION REQUEST HANDLED

I understand you'd like to speak with a human. Here are your options:

📞 **Immediate Support Options:**

1. **General Health & Wellness Support**
   📱 Phone: {self.support_contacts['general']['phone']}
   📧 Email: {self.support_contacts['general']['email']}
   ⏰ Hours: {self.support_contacts['general']['hours']}

2. **Medical Concerns**
   🚨 Phone: {self.support_contacts['medical']['phone']}
   📧 Email: {self.support_contacts['medical']['email']}
   ⏰ Hours: {self.support_contacts['medical']['hours']}

3. **Nutrition Specialist**
   📱 Phone: {self.support_contacts['nutrition']['phone']}
   📧 Email: {self.support_contacts['nutrition']['email']}
   ⏰ Hours: {self.support_contacts['nutrition']['hours']}

4. **Fitness & Training Support**
   📱 Phone: {self.support_contacts['fitness']['phone']}
   📧 Email: {self.support_contacts['fitness']['email']}
   ⏰ Hours: {self.support_contacts['fitness']['hours']}

📋 **Your Request Details:**
• Reason: {reason}
• User Profile: Age {user_info.get('age', 'Not specified')}, Fitness Level {user_info.get('fitness_level', 'Not specified')}
• Request Time: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

💡 **Before calling, please have ready:**
• Your health goals and current concerns
• Any relevant medical history
• Specific questions you'd like addressed

⚠️ **Important:** For medical emergencies, please call 911 or your local emergency services immediately.

Your escalation request has been logged and will be followed up within 24 hours.
"""
        
        return response
    
    def get_escalation_history(self) -> str:
        """Get escalation request history"""
        if not self.escalation_log["escalations"]:
            return "📝 No escalation requests recorded."
        
        history = "📋 ESCALATION REQUEST HISTORY\n\n"
        
        for i, escalation in enumerate(self.escalation_log["escalations"], 1):
            date = datetime.fromisoformat(escalation["timestamp"]).strftime("%B %d, %Y at %I:%M %p")
            history += f"{i}. {date}\n"
            history += f"   Reason: {escalation['reason']}\n"
            history += f"   Status: {escalation['status']}\n"
            history += f"   User: Age {escalation['user_info'].get('age', 'Not specified')}\n\n"
        
        return history

def create_escalation_agent() -> EscalationAgent:
    """Factory function to create an escalation agent instance"""
    return EscalationAgent() 