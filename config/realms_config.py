"""
MotiBeam Spatial OS - Realms Configuration
Configuration for all available realms in the system
"""

REALMS_CONFIG = {
    "emergency": {
        "name": "Emergency Response Realm",
        "description": "911 Dispatch, Crisis Response, Medical Emergency",
        "icon": "🚨",
        "priority": "CRITICAL",
        "sensors": ["thermal", "audio", "motion", "vital_signs", "location"],
        "ai_modules": ["triage", "resource_allocation", "crisis_prediction"]
    },
    "security": {
        "name": "Security & Surveillance Realm",
        "description": "Perimeter Defense, Access Control, Threat Detection",
        "icon": "🛡️",
        "priority": "HIGH",
        "sensors": ["cameras", "motion", "biometric", "acoustic", "radar"],
        "ai_modules": ["facial_recognition", "behavior_analysis", "threat_assessment"]
    },
    "enterprise": {
        "name": "Enterprise Workspace Realm",
        "description": "Office Environments, Collaboration, Productivity",
        "icon": "🏢",
        "priority": "NORMAL",
        "sensors": ["presence", "activity", "environmental", "devices"],
        "ai_modules": ["scheduling", "resource_optimization", "collaboration_assist"]
    },
    "aviation": {
        "name": "Aviation Control Realm",
        "description": "Air Traffic Control, Cockpit Integration, Flight Safety",
        "icon": "✈️",
        "priority": "CRITICAL",
        "sensors": ["radar", "altimeter", "weather", "collision_avoidance", "navigation"],
        "ai_modules": ["traffic_control", "flight_path_optimization", "weather_prediction"]
    },
    "maritime": {
        "name": "Maritime Operations Realm",
        "description": "Vessel Navigation, Port Operations, Marine Safety",
        "icon": "⚓",
        "priority": "HIGH",
        "sensors": ["sonar", "gps", "weather", "collision_radar", "depth"],
        "ai_modules": ["navigation", "traffic_management", "weather_routing"]
    }
}

# System-wide settings
SYSTEM_CONFIG = {
    "version": "MOS-1.0",
    "codename": "Kickstarter Demo",
    "demo_cycle_duration": 5,  # seconds per demo cycle
    "auto_loop_delay": 2,  # seconds between realms in auto-loop
    "max_sensor_refresh": 1.0,  # seconds
    "ai_processing_delay": 0.5  # seconds
}
