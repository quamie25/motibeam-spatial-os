"""
MotiBeam Spatial OS - Realms Configuration
Central configuration for all available realms
"""

REALMS_CONFIG = {
    "home": {
        "label": "🏡 Home",
        "module": "scenes.home_realm",
        "class_name": "HomeRealm",
        "description": "Main dashboard and navigation hub",
    },
    "clinical": {
        "label": "⚕️ Clinical",
        "module": "scenes.clinical_realm",
        "class_name": "ClinicalRealm",
        "description": "Health monitoring and medical HUD",
    },
    "education": {
        "label": "📚 Education",
        "module": "scenes.education_realm",
        "class_name": "EducationRealm",
        "description": "Learning and knowledge management",
    },
    "security": {
        "label": "🔒 Security",
        "module": "scenes.security_realm",
        "class_name": "SecurityRealm",
        "description": "Security monitoring and access control",
    },
    "emergency": {
        "label": "🚨 Emergency",
        "module": "scenes.emergency_realm",
        "class_name": "EmergencyRealm",
        "description": "Emergency response and crisis management",
    },
    "transport": {
        "label": "🚗 Transport",
        "module": "scenes.transport_realm",
        "class_name": "TransportRealm",
        "description": "Transportation and logistics management",
    },
}
