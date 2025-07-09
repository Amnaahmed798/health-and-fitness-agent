"""
Specialized Health Agents Package
A collection of specialized agents for different health and wellness needs
"""

from .escalation_agent import create_escalation_agent, EscalationAgent
from .injury_support_agent import create_injury_support_agent, InjurySupportAgent
from .nutrition_expert_agent import create_nutrition_expert_agent, NutritionExpertAgent

__all__ = [
    'create_escalation_agent',
    'EscalationAgent',
    'create_injury_support_agent',
    'InjurySupportAgent',
    'create_nutrition_expert_agent',
    'NutritionExpertAgent'
] 