"""
Security & Surveillance Realm - Intelligent Security Operations

Narrative phases:
1. THREAT SNAPSHOT
2. SPATIAL PERIMETER MONITORING
3. ACCESS CONTROL
4. PREDICTIVE SECURITY ANALYSIS
5. AUTOMATED THREAT RESPONSE
6. SECURITY STATUS CONFIRMED
"""

import random
from typing import List, Dict
from core.cinematic_realm import CinematicRealm


class SecuritySurveillanceRealm(CinematicRealm):
    """Security & Surveillance - Threat detection to resolution."""

    def __init__(self, screen, theme):
        super().__init__(screen, theme)

        # Randomize values
        self.threat_score = random.randint(72, 88)
        self.active_cameras = random.randint(42, 48)
        self.false_positive_rate = round(random.uniform(2.1, 4.8), 1)
        self.response_time = round(random.uniform(1.2, 2.8), 1)

    @property
    def realm_name(self) -> str:
        return "SECURITY & SURVEILLANCE"

    @property
    def realm_key(self) -> str:
        return "S"

    @property
    def realm_icon(self) -> str:
        return "🛡️"

    def get_phases(self) -> List[Dict]:
        """Define the security surveillance narrative."""
        return [
            {
                "title": "THREAT SNAPSHOT",
                "icon": "⚠️",
                "lines": [
                    "Anomaly detected: Sector 7-B, Loading Dock entrance",
                    "Time: 02:47 AM - Outside authorized hours",
                    "Subject: Unrecognized individual, male, 30-40 years",
                    "Behavior: Attempting door access, no valid credentials",
                ],
                "accent": (255, 200, 80),
                "duration": 4.5,
                "ticker": "Motion detected • Facial recognition running • Access logs checked • Alert level elevated"
            },
            {
                "title": "SPATIAL PERIMETER MONITORING",
                "icon": "📡",
                "lines": [
                    f"Active surveillance: {self.active_cameras} cameras online",
                    "3D tracking: Subject tracked across 4 camera zones",
                    "Perimeter status: All zones secure except 7-B",
                    "Nearby assets: Server room (15m), Executive offices (30m)",
                ],
                "accent": (100, 180, 255),
                "duration": 4.5,
                "ticker": "Multi-camera tracking active • 3D position mapped • Asset proximity calculated • Patrol units alerted"
            },
            {
                "title": "ACCESS CONTROL",
                "icon": "🔐",
                "lines": [
                    "Badge scan attempted: INVALID - Badge not in system",
                    "Biometric check: No match in authorized personnel",
                    "Access history: No prior entries from this individual",
                    "Security protocol: Automatic lockdown initiated for Sector 7",
                ],
                "accent": (255, 100, 100),
                "duration": 4.5,
                "ticker": "Access denied • Biometric mismatch • Sector 7 locked down • Security team dispatched"
            },
            {
                "title": "PREDICTIVE SECURITY ANALYSIS",
                "icon": "🔮",
                "lines": [
                    f"AI threat assessment: {self.threat_score}% probability of intrusion attempt",
                    "Behavior pattern: Consistent with reconnaissance activity",
                    f"Model confidence: High (false positive rate: {self.false_positive_rate}%)",
                    "Recommendation: Immediate security response + Law enforcement alert",
                ],
                "accent": (255, 80, 200),
                "duration": 4.5,
                "ticker": f"AI threat score: {self.threat_score}% • Pattern analysis complete • Response protocol engaged • Police notified"
            },
            {
                "title": "AUTOMATED THREAT RESPONSE",
                "icon": "🚨",
                "lines": [
                    f"Security team: Unit SEC-03 on scene - Response time {self.response_time}m",
                    "Subject status: Detained for questioning",
                    "Area secured: Full perimeter sweep completed",
                    "Evidence collected: Video footage, badge scan logs, biometric data",
                ],
                "accent": (255, 150, 50),
                "duration": 4.5,
                "ticker": "Security on scene • Subject detained • Area swept • Evidence secured • Incident logged"
            },
            {
                "title": "SECURITY STATUS CONFIRMED",
                "icon": "✅",
                "lines": [
                    "Threat neutralized: Subject identified - Former contractor",
                    "Motivation: Attempted unauthorized data access",
                    "Facility status: All clear - Normal operations resumed",
                    "System update: Badge revocation confirmed, access logs flagged",
                ],
                "accent": (80, 255, 150),
                "duration": 5.0,
                "ticker": "All clear • Threat resolved • Access updated • Report filed • Normal monitoring restored"
            },
        ]
