"""
Enterprise Workspace Realm - Intelligent Workplace Management

Narrative phases:
1. INTELLIGENT WORKSPACE MANAGEMENT
2. MEETING ORCHESTRATION
3. AR-ENHANCED COLLABORATION
4. PRODUCTIVITY & WELLNESS ANALYTICS
5. RESOURCE OPTIMIZATION
6. WORKPLACE INSIGHTS SUMMARY
"""

import random
from typing import List, Dict
from core.cinematic_realm import CinematicRealm


class EnterpriseWorkspaceRealm(CinematicRealm):
    """Enterprise Workspace - Intelligent workplace operations."""

    def __init__(self, screen, theme):
        super().__init__(screen, theme)

        # Randomize metrics
        self.desk_occupancy = random.randint(73, 89)
        self.meeting_efficiency = random.randint(82, 94)
        self.collab_score = random.randint(88, 96)
        self.energy_savings = random.randint(18, 28)

    @property
    def realm_name(self) -> str:
        return "ENTERPRISE WORKSPACE"

    @property
    def realm_key(self) -> str:
        return "W"

    @property
    def realm_icon(self) -> str:
        return "🏢"

    def get_phases(self) -> List[Dict]:
        """Define the enterprise workspace narrative."""
        return [
            {
                "title": "INTELLIGENT WORKSPACE MANAGEMENT",
                "icon": "🏢",
                "lines": [
                    f"Real-time desk occupancy: {self.desk_occupancy}% across 3 floors",
                    "Hot-desking: 47 available workstations dynamically allocated",
                    "Climate control: AI-optimized for occupancy patterns",
                    "Smart booking: Conference rooms auto-assigned based on team proximity",
                ],
                "accent": (100, 200, 255),
                "duration": 4.5,
                "ticker": f"Workspace utilization: {self.desk_occupancy}% • Smart allocation active • Climate optimized • Booking system online"
            },
            {
                "title": "MEETING ORCHESTRATION",
                "icon": "📅",
                "lines": [
                    "Active meetings: 8 in progress, 12 scheduled today",
                    "AR meeting room: 3D holographic display active (Conf Room B)",
                    f"Meeting efficiency score: {self.meeting_efficiency}% (above target)",
                    "Auto-transcription: 6 meetings captured, notes distributed",
                ],
                "accent": (255, 150, 80),
                "duration": 4.5,
                "ticker": "8 meetings active • AR holograms live • Transcription running • Calendar optimized"
            },
            {
                "title": "AR-ENHANCED COLLABORATION",
                "icon": "🥽",
                "lines": [
                    "Spatial computing: 15 AR sessions active (design, planning, review)",
                    "Virtual whiteboards: 3D sketches shared across 4 office locations",
                    "Remote presence: 23 holographic participants in hybrid meetings",
                    "Gesture controls: Hand-tracking enabled for 12 workstations",
                ],
                "accent": (200, 100, 255),
                "duration": 4.5,
                "ticker": "15 AR sessions live • 3D collaboration active • 23 remote holograms • Gesture tracking enabled"
            },
            {
                "title": "PRODUCTIVITY & WELLNESS ANALYTICS",
                "icon": "📊",
                "lines": [
                    f"Team collaboration score: {self.collab_score}% (trending up 4%)",
                    "Focus time: Avg 3.2 hours deep work per employee today",
                    "Wellness alerts: 8 break reminders sent, 12 ergonomic adjustments made",
                    "Stress indicators: 94% of staff in optimal productivity zone",
                ],
                "accent": (80, 255, 150),
                "duration": 4.5,
                "ticker": f"Collab score: {self.collab_score}% • 3.2h avg focus time • Wellness checks active • Productivity optimal"
            },
            {
                "title": "RESOURCE OPTIMIZATION",
                "icon": "⚡",
                "lines": [
                    f"Energy efficiency: {self.energy_savings}% reduction via smart sensors",
                    "Lighting: Auto-dimming based on natural light + occupancy",
                    "HVAC optimization: Zone-based climate control saving 340 kWh today",
                    "Print reduction: 67% less paper via digital workflows",
                ],
                "accent": (255, 200, 50),
                "duration": 4.5,
                "ticker": f"{self.energy_savings}% energy saved • Smart lighting active • HVAC optimized • Digital workflows scaling"
            },
            {
                "title": "WORKPLACE INSIGHTS SUMMARY",
                "icon": "✅",
                "lines": [
                    "Daily summary: 156 employees, 94% satisfaction score",
                    "Space utilization: Conference rooms at 78% capacity (optimal)",
                    "Predictive maintenance: 3 IoT sensors flagged for service next week",
                    "Tomorrow's forecast: 142 employees expected, 2 events scheduled",
                ],
                "accent": (150, 255, 200),
                "duration": 5.0,
                "ticker": "94% satisfaction • 78% space utilization • Maintenance scheduled • Tomorrow's workspace pre-configured"
            },
        ]
