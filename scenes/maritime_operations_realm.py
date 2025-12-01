"""
Maritime Operations Realm - Intelligent Port & Vessel Management

Narrative phases:
1. PORT OPERATIONS CENTER
2. 3D MARITIME TRACKING
3. AUTONOMOUS NAVIGATION ASSISTANCE
4. COLLISION AVOIDANCE
5. INTELLIGENT WEATHER ROUTING
6. AUTOMATED PORT OPERATIONS
"""

import random
from typing import List, Dict
from core.cinematic_realm import CinematicRealm


class MaritimeOperationsRealm(CinematicRealm):
    """Maritime Operations - Port and vessel management narrative."""

    def __init__(self, screen, theme):
        super().__init__(screen, theme)

        # Randomize values
        self.active_vessels = random.randint(18, 27)
        self.berth_efficiency = random.randint(84, 94)
        self.safety_score = round(random.uniform(96.3, 99.2), 1)
        self.fuel_optimization = round(random.uniform(14.2, 22.8), 1)

    @property
    def realm_name(self) -> str:
        return "MARITIME OPERATIONS"

    @property
    def realm_key(self) -> str:
        return "M"

    @property
    def realm_icon(self) -> str:
        return "⚓"

    def get_phases(self) -> List[Dict]:
        """Define the maritime operations narrative."""
        return [
            {
                "title": "PORT OPERATIONS CENTER",
                "icon": "⚓",
                "lines": [
                    f"Active vessel management: {self.active_vessels} ships in port jurisdiction",
                    "Harbor zones: Inner Harbor (8 ships), Outer Channel (6), Anchorage (4)",
                    "Berth allocation: 12 of 15 berths occupied, 3 available",
                    "Port authority: 4 pilots on duty, 6 tug boats operational",
                ],
                "accent": (100, 200, 255),
                "duration": 4.5,
                "ticker": f"{self.active_vessels} vessels tracked • 12/15 berths occupied • 4 pilots active • 6 tugs operational"
            },
            {
                "title": "3D MARITIME TRACKING",
                "icon": "🗺️",
                "lines": [
                    "Real-time 3D positions: All vessels tracked via AIS + radar fusion",
                    "Key vessels: ATLANTIC STAR (berth B3), PACIFIC DREAM (inbound)",
                    "Route monitoring: NORDIC WAVE at anchorage, LIBERTY EXPRESS loading",
                    "Depth sensors: Channel depth confirmed 12.5m, safe for deep-draft vessels",
                ],
                "accent": (255, 150, 80),
                "duration": 4.5,
                "ticker": "3D tracking active • ATLANTIC STAR berthing • PACIFIC DREAM inbound • NORDIC WAVE anchored"
            },
            {
                "title": "AUTONOMOUS NAVIGATION ASSISTANCE",
                "icon": "🤖",
                "lines": [
                    "AI navigation: 6 vessels using auto-docking assistance",
                    "ATLANTIC STAR: Autonomous berthing sequence initiated at B3",
                    "Precision guidance: GPS-RTK + LiDAR achieving ±5cm accuracy",
                    "Pilot oversight: Human monitoring autonomous systems, ready to intervene",
                ],
                "accent": (200, 100, 255),
                "duration": 4.5,
                "ticker": "6 vessels auto-docking • ATLANTIC STAR autonomous berthing • ±5cm precision • Pilot monitoring"
            },
            {
                "title": "COLLISION AVOIDANCE",
                "icon": "🚨",
                "lines": [
                    f"AI collision detection: {self.safety_score}% accuracy, zero incidents this month",
                    "Alert: PACIFIC DREAM and tug TUG-2 converging in outer channel",
                    "Auto-resolution: PACIFIC DREAM reduce speed to 4 kts, TUG-2 alter course 15°",
                    "Confirmation: Safe separation re-established, 300m clearance maintained",
                ],
                "accent": (255, 100, 100),
                "duration": 4.5,
                "ticker": "Collision risk detected • Auto-resolution applied • PACIFIC DREAM slowing • 300m clearance restored"
            },
            {
                "title": "INTELLIGENT WEATHER ROUTING",
                "icon": "⛈️",
                "lines": [
                    "Weather integration: Real-time wind, swell, tide, visibility data",
                    "Conditions: Wind 15 kts NW, swell 1.2m / 8s, high tide 14:23 (3.2m)",
                    f"Route optimization: AI-calculated paths saving {self.fuel_optimization}% fuel",
                    "Forecast: Next weather window optimal for 4 scheduled arrivals",
                ],
                "accent": (150, 255, 200),
                "duration": 4.5,
                "ticker": f"Weather optimal • High tide 14:23 • {self.fuel_optimization}% fuel savings • 4 arrivals scheduled"
            },
            {
                "title": "AUTOMATED PORT OPERATIONS",
                "icon": "✅",
                "lines": [
                    f"Operational efficiency: {self.berth_efficiency}% berth utilization (above target)",
                    "ATLANTIC STAR: Berthing complete, cargo operations commenced",
                    "Container terminal: 847 containers processed today, 94% on schedule",
                    "Customs clearance: 12 vessels cleared, average processing time 42 min",
                ],
                "accent": (80, 255, 180),
                "duration": 5.0,
                "ticker": f"{self.berth_efficiency}% berth efficiency • ATLANTIC STAR berthed • 847 containers processed • All systems optimal"
            },
        ]
