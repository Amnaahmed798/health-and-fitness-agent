"""
Injury Support Agent
Provides guidance for injuries, pain management, and when to seek medical attention
"""

import json
from datetime import datetime
from typing import Dict, List

class InjurySupportAgent:
    def __init__(self):
        self.injury_log_file = "injury_log.json"
        self.injury_log = self.load_injury_log()
        self.injury_guidelines = self.load_injury_guidelines()
    
    def load_injury_log(self) -> Dict:
        """Load injury log from file"""
        try:
            with open(self.injury_log_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"injuries": [], "created_date": datetime.now().isoformat()}
    
    def save_injury_log(self):
        """Save injury log to file"""
        with open(self.injury_log_file, 'w') as f:
            json.dump(self.injury_log, f, indent=2)
    
    def load_injury_guidelines(self) -> Dict:
        """Load injury assessment guidelines"""
        return {
            "emergency": {
                "symptoms": [
                    "severe pain", "unable to move", "deformity", "numbness", 
                    "tingling", "severe swelling", "bruising", "popping sound",
                    "unable to bear weight", "loss of consciousness"
                ],
                "action": "🚨 IMMEDIATE MEDICAL ATTENTION REQUIRED - Call 911 or go to ER",
                "description": "These symptoms indicate a serious injury requiring immediate medical evaluation."
            },
            "urgent": {
                "symptoms": [
                    "moderate to severe pain", "swelling", "limited range of motion",
                    "pain that worsens", "pain that interferes with daily activities",
                    "pain lasting more than 48 hours", "weakness", "instability"
                ],
                "action": "🏥 SEEK MEDICAL ATTENTION WITHIN 24 HOURS",
                "description": "These symptoms should be evaluated by a healthcare professional."
            },
            "self_care": {
                "symptoms": [
                    "mild pain", "slight swelling", "minor discomfort",
                    "pain that improves with rest", "pain that responds to ice/heat"
                ],
                "action": "🏠 SELF-CARE APPROPRIATE",
                "description": "These symptoms can typically be managed with self-care measures."
            }
        }
    
    def assess_injury(self, user_info: Dict, injury_description: str, symptoms: List[str]) -> str:
        """Assess injury severity and provide appropriate guidance"""
        
        # Log the injury report
        injury_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_info": user_info,
            "injury_description": injury_description,
            "symptoms": symptoms,
            "status": "assessed"
        }
        
        self.injury_log["injuries"].append(injury_entry)
        self.save_injury_log()
        
        # Assess severity based on symptoms
        severity_level = self.determine_severity(symptoms)
        guidance = self.injury_guidelines[severity_level]
        
        response = f"""
🏥 INJURY ASSESSMENT REPORT

📋 **Injury Description:** {injury_description}
👤 **User Profile:** Age {user_info.get('age', 'Not specified')}, Fitness Level {user_info.get('fitness_level', 'Not specified')}
📅 **Assessment Date:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

🔍 **Reported Symptoms:**
"""
        
        for symptom in symptoms:
            response += f"• {symptom}\n"
        
        response += f"""
📊 **Severity Assessment:** {severity_level.upper()}

{guidance['action']}

📝 **Assessment Details:**
{guidance['description']}

"""
        
        if severity_level == "emergency":
            response += self.get_emergency_guidance()
        elif severity_level == "urgent":
            response += self.get_urgent_guidance()
        else:
            response += self.get_self_care_guidance()
        
        response += f"""
⚠️ **Important Disclaimers:**
• This assessment is for informational purposes only
• Always consult with healthcare professionals for proper diagnosis
• When in doubt, seek medical attention
• This does not replace professional medical advice

📞 **Emergency Contacts:**
• Emergency Services: 911
• Poison Control: 1-800-222-1222
• Your Primary Care Physician
"""
        
        return response
    
    def determine_severity(self, symptoms: List[str]) -> str:
        """Determine injury severity based on symptoms"""
        emergency_symptoms = self.injury_guidelines["emergency"]["symptoms"]
        urgent_symptoms = self.injury_guidelines["urgent"]["symptoms"]
        
        # Check for emergency symptoms
        for symptom in symptoms:
            if any(emergency_symptom in symptom.lower() for emergency_symptom in emergency_symptoms):
                return "emergency"
        
        # Check for urgent symptoms
        for symptom in symptoms:
            if any(urgent_symptom in symptom.lower() for urgent_symptom in urgent_symptoms):
                return "urgent"
        
        return "self_care"
    
    def get_emergency_guidance(self) -> str:
        """Get emergency guidance"""
        return """
🚨 **EMERGENCY PROTOCOL:**

1. **IMMEDIATE ACTION REQUIRED:**
   • Call 911 or go to the nearest emergency room
   • Do not attempt to move the injured area
   • Keep the person calm and still
   • Apply ice if possible without moving the injury

2. **What to Expect:**
   • Emergency medical evaluation
   • X-rays or imaging tests
   • Immediate treatment or referral to specialist
   • Follow-up care instructions

3. **After Emergency Care:**
   • Follow all medical instructions
   • Attend all follow-up appointments
   • Complete prescribed rehabilitation
   • Gradually return to activity as cleared by medical professionals
"""
    
    def get_urgent_guidance(self) -> str:
        """Get urgent care guidance"""
        return """
🏥 **URGENT CARE PROTOCOL:**

1. **IMMEDIATE ACTION:**
   • Contact your healthcare provider within 24 hours
   • Apply RICE protocol (Rest, Ice, Compression, Elevation)
   • Avoid activities that worsen pain
   • Consider urgent care clinic if primary care unavailable

2. **RICE Protocol:**
   • **Rest:** Avoid activities that cause pain
   • **Ice:** Apply ice for 15-20 minutes every 2-3 hours
   • **Compression:** Use elastic bandage for support
   • **Elevation:** Keep injured area elevated above heart

3. **Monitor Symptoms:**
   • Watch for worsening pain, swelling, or new symptoms
   • Seek immediate care if symptoms worsen
   • Follow up with healthcare provider as recommended
"""
    
    def get_self_care_guidance(self) -> str:
        """Get self-care guidance"""
        return """
🏠 **SELF-CARE PROTOCOL:**

1. **IMMEDIATE CARE:**
   • Apply RICE protocol (Rest, Ice, Compression, Elevation)
   • Take over-the-counter pain relievers if needed
   • Avoid activities that cause pain
   • Gentle stretching if tolerated

2. **Recovery Timeline:**
   • Monitor symptoms for 48-72 hours
   • Gradually return to activity as pain decreases
   • If symptoms persist beyond 1 week, consult healthcare provider

3. **Prevention Tips:**
   • Warm up properly before exercise
   • Use proper form and technique
   • Gradually increase intensity
   • Listen to your body's signals
   • Include rest days in your routine
"""
    
    def get_injury_history(self) -> str:
        """Get injury history"""
        if not self.injury_log["injuries"]:
            return "📝 No injury reports recorded."
        
        history = "📋 INJURY HISTORY\n\n"
        
        for i, injury in enumerate(self.injury_log["injuries"], 1):
            date = datetime.fromisoformat(injury["timestamp"]).strftime("%B %d, %Y at %I:%M %p")
            history += f"{i}. {date}\n"
            history += f"   Injury: {injury['injury_description']}\n"
            history += f"   Symptoms: {', '.join(injury['symptoms'])}\n"
            history += f"   Status: {injury['status']}\n\n"
        
        return history

def create_injury_support_agent() -> InjurySupportAgent:
    """Factory function to create an injury support agent instance"""
    return InjurySupportAgent() 