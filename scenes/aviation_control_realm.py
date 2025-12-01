"""
Aviation Control Realm - Intelligent Air Traffic Management

Narrative phases:
1. AIR TRAFFIC CONTROL CENTER
2. 3D AIRSPACE MAPPING
3. COLLISION AVOIDANCE
4. PREDICTIVE WEATHER ANALYSIS
5. FLIGHT OPTIMIZATION
6. AUTOMATED LANDING SEQUENCE
"""

import random
from typing import List, Dict
from core.cinematic_realm import CinematicRealm


class AviationControlRealm(CinematicRealm):
    """Aviation Control - Air traffic management narrative."""

    def __init__(self, screen, theme):
        super().__init__(screen, theme)

        # Randomize values
        self.active_flights = random.randint(42, 58)
        self.conflict_detection = round(random.uniform(94.2, 98.9), 1)
        self.weather_accuracy = random.randint(91, 97)
        self.fuel_savings = round(random.uniform(12.3, 18.7), 1)

    @property
    def realm_name(self) -> str:
        return "AVIATION CONTROL"

    @property
    def realm_key(self) -> str:
        return "A"

    @property
    def realm_icon(self) -> str:
        return "✈️"

    def get_phases(self) -> List[Dict]:
        """Define the aviation control narrative."""
        return [
            {
                "title": "AIR TRAFFIC CONTROL CENTER",
                "icon": "✈️",
                "lines": [
                    f"Active airspace: {self.active_flights} aircraft under management",
                    "Sectors: North, South, East, West - All operational",
                    "Controllers: 8 stations online, 2 supervisors monitoring",
                    "Radio frequency: Guard channel clear, normal communications",
                ],
                "accent": (100, 180, 255),
                "duration": 4.5,
                "ticker": f"{self.active_flights} aircraft tracked • All sectors nominal • Communications clear • Spacing optimal"
            },
            {
                "title": "3D AIRSPACE MAPPING",
                "icon": "🗺️",
                "lines": [
                    "Real-time 3D tracking: All aircraft positions, altitudes, vectors",
                    "Key flights: AA204 FL320, DL119 FL280, UA877 FL350",
                    "Separation monitoring: All aircraft maintaining 5+ nm spacing",
                    "Restricted zones: Military airspace MOA-7 active, avoidance vectors set",
                ],
                "accent": (255, 140, 80),
                "duration": 4.5,
                "ticker": "3D tracking active • AA204, DL119, UA877 on course • Separation optimal • Restricted zones avoided"
            },
            {
                "title": "COLLISION AVOIDANCE",
                "icon": "🚨",
                "lines": [
                    f"AI conflict detection: {self.conflict_detection}% accuracy, zero incidents today",
                    "Alert: Potential conflict - AA204 and SW523 converging",
                    "Auto-resolution: AA204 climb to FL330, SW523 maintain FL310",
                    "Confirmation: Separation re-established, 8 nm horizontal, 2000ft vertical",
                ],
                "accent": (255, 100, 100),
                "duration": 4.5,
                "ticker": "Conflict detected • Auto-resolution applied • AA204 climbing FL330 • Separation restored 8nm"
            },
            {
                "title": "PREDICTIVE WEATHER ANALYSIS",
                "icon": "⛈️",
                "lines": [
                    f"AI weather modeling: {self.weather_accuracy}% accuracy, 4-hour forecast window",
                    "Storm system: Thunderstorms developing 40 nm west, moving east 15 kts",
                    "Impact analysis: 6 flights rerouted, avg delay 8 minutes",
                    "Optimal routing: New flight paths calculated, fuel impact minimal",
                ],
                "accent": (200, 120, 255),
                "duration": 4.5,
                "ticker": "Weather system tracked • 6 flights rerouted • Delays minimal • Fuel impact optimized"
            },
            {
                "title": "FLIGHT OPTIMIZATION",
                "icon": "⚡",
                "lines": [
                    f"Route efficiency: AI-optimized paths saving {self.fuel_savings}% fuel per flight",
                    "Wind optimization: Upper-level winds analyzed, FL340-360 preferred",
                    "Direct routing: 12 flights cleared direct to destination waypoints",
                    "Arrival sequencing: Landing slots optimized, reducing hold time by 40%",
                ],
                "accent": (100, 255, 150),
                "duration": 4.5,
                "ticker": f"{self.fuel_savings}% fuel savings • 12 flights direct routing • Arrival sequencing optimized • Hold times reduced 40%"
            },
            {
                "title": "AUTOMATED LANDING SEQUENCE",
                "icon": "🛬",
                "lines": [
                    "Approach control: 8 aircraft in landing sequence, ILS established",
                    "Runway allocation: RWY 27L and 27R active, optimal for wind 270° at 12 kts",
                    "Auto-spacing: AI maintains 5 nm separation on final approach",
                    "Touchdown: AA204 landed safely, total flight time 3h 42m, on schedule",
                ],
                "accent": (150, 255, 200),
                "duration": 5.0,
                "ticker": "8 aircraft landing sequence • ILS locked • 5nm spacing maintained • AA204 safely landed"
            },
        ]
