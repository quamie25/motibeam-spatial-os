"""
Emergency Response Realm - Cinematic 911 Response System

Narrative phases:
1. INCOMING 911 CALL
2. SPATIAL INCIDENT MAPPING
3. RESOURCE ALLOCATION
4. REAL-TIME COORDINATION
5. PREDICTIVE CRISIS ANALYSIS
6. INCIDENT RESOLUTION
"""

import random
from typing import List, Dict
from core.cinematic_realm import CinematicRealm


class EmergencyResponseRealm(CinematicRealm):
    """Emergency Response - 911 call to resolution narrative."""

    def __init__(self, screen, theme):
        super().__init__(screen, theme)

        # Randomize some values to feel alive
        self.confidence = random.randint(92, 97)
        self.eta_minutes = random.randint(3, 5)
        self.eta_seconds = random.randint(10, 55)
        self.response_units = random.randint(2, 4)

    @property
    def realm_name(self) -> str:
        return "EMERGENCY RESPONSE"

    @property
    def realm_key(self) -> str:
        return "E"

    @property
    def realm_icon(self) -> str:
        return "🚨"

    def get_phases(self) -> List[Dict]:
        """Define the 6-phase emergency response narrative."""
        return [
            {
                "title": "INCOMING 911 CALL",
                "icon": "📞",
                "lines": [
                    "Caller: Elderly male, chest pain, difficulty breathing",
                    "Location: 42.3601° N, 71.0589° W (Boston, MA)",
                    f"AI triage: CRITICAL – suspected cardiac event",
                    f"Confidence: {self.confidence}%",
                ],
                "accent": (255, 80, 80),
                "duration": 4.5,
                "ticker": "Emergency call received • AI triage in progress • Location confirmed • Medical history accessed"
            },
            {
                "title": "SPATIAL INCIDENT MAPPING",
                "icon": "🗺️",
                "lines": [
                    "Residential building – 3rd floor, unit 304",
                    "Access points: 2 entrances, elevator operational",
                    "Nearest AED: 150m (CVS Pharmacy, Main St)",
                    "Building layout: 6-story apartment complex",
                ],
                "accent": (255, 140, 60),
                "duration": 4.5,
                "ticker": "3D mapping complete • Access routes calculated • AED locations identified • Floor plan loaded"
            },
            {
                "title": "RESOURCE ALLOCATION",
                "icon": "🚑",
                "lines": [
                    f"Unit AMB-01: Dispatched – ETA {self.eta_minutes}m {self.eta_seconds}s",
                    "Paramedic team: 2 EMT-Advanced certified",
                    "Equipment: Cardiac monitor, defibrillator, oxygen",
                    "Backup unit: AMB-04 on standby (8 min)",
                ],
                "accent": (100, 200, 255),
                "duration": 4.5,
                "ticker": f"AMB-01 en route • ETA {self.eta_minutes}m {self.eta_seconds}s • Cardiac equipment loaded • Hospital alerted"
            },
            {
                "title": "REAL-TIME COORDINATION",
                "icon": "📡",
                "lines": [
                    "Live GPS tracking: Unit 2.4 km away, optimal route",
                    "Traffic control: Green corridor activated",
                    "Hospital: Mass General ER bed reserved",
                    "Caller support: CPR instructions provided via phone",
                ],
                "accent": (150, 100, 255),
                "duration": 4.5,
                "ticker": "Unit AMB-01 2.4km away • Traffic lights synchronized • ER bed 7 reserved • Caller receiving CPR guidance"
            },
            {
                "title": "PREDICTIVE CRISIS ANALYSIS",
                "icon": "🔮",
                "lines": [
                    "AI prediction: 78% probability of cardiac arrest",
                    "Recommended: Immediate defibrillation upon arrival",
                    "Risk factors: Age 72, hypertension, prior MI",
                    "Optimal hospital: Mass General (cardiac specialist on-site)",
                ],
                "accent": (200, 80, 255),
                "duration": 4.5,
                "ticker": "AI analysis complete • Cardiac arrest risk 78% • Treatment protocol loaded • Specialist notified"
            },
            {
                "title": "INCIDENT RESOLUTION",
                "icon": "✅",
                "lines": [
                    "Paramedics on scene: Patient stabilized",
                    "Vitals: BP 130/85, HR 88 bpm, SpO2 95%",
                    "Transport initiated: En route to Mass General ER",
                    f"Total response time: {self.eta_minutes + 1}m {self.eta_seconds + 15}s – Target: <8 min",
                ],
                "accent": (80, 255, 120),
                "duration": 5.0,
                "ticker": "Patient stabilized • Transport in progress • ETA hospital 6 minutes • Family notified • Case logged successfully"
            },
        ]
