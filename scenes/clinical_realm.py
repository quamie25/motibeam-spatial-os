"""
MotiBeam Spatial OS - Clinical Realm
Health Monitoring, Wellness Tracking, Medical Assistance
"""

import random
import time
from datetime import datetime
from core.base_realm import SpatialRealm
from core.spatial_engine import SpatialEngine, BeamNetworkProtocol

import pygame


class ClinicalRealm(SpatialRealm):
    """Health and wellness ambient computing realm"""

    def __init__(self, standalone=False):
        super().__init__(
            realm_name="Clinical Realm",
            realm_description="Health Monitoring, Wellness Tracking, Medical Assistance"
        )
        self.spatial_engine = SpatialEngine()
        self.beam_network = BeamNetworkProtocol()
        self.health_devices = []
        self.patients = []
        self.screen = None
        self.standalone = standalone

    def initialize(self) -> bool:
        """Initialize clinical realm systems"""
        print("  ⚕️  Initializing Clinical Realm Systems...")

        scan = self.spatial_engine.scan_environment("clinical")
        print(f"  ✓ Clinical space mapped: {scan['room_dimensions']}")

        self.beam_network.establish_mesh("Clinical Network")

        self.health_devices = [
            {"id": "WATCH-01", "type": "Smart Watch", "patient": "John", "status": "Active"},
            {"id": "SCALE-01", "type": "Smart Scale", "patient": "Sarah", "status": "Synced"},
            {"id": "BP-01", "type": "Blood Pressure", "patient": "John", "status": "Ready"},
            {"id": "GLUCOSE-01", "type": "Glucose Monitor", "patient": "Mary", "status": "Active"}
        ]

        print("  ✓ Clinical systems online")
        return True

    def run_demo_cycle(self) -> None:
        """Demonstrate clinical realm capabilities (text mode)"""
        self.display_header()

        print("\n⚕️  HEALTH MONITORING OVERVIEW")
        print("  Connected devices: 12")
        print("  Patients monitored: 3")
        print("  Alerts: None")
        print("  Wellness score: 94/100")
        time.sleep(1)

        print("\n💓 CONTINUOUS VITAL MONITORING")
        print("  Patient: John (Age 45)")
        self.simulate_ai_processing("Real-time vital signs analysis")
        print("  Heart rate: 68 bpm (normal)")
        print("  Blood pressure: 118/76 mmHg (optimal)")
        print("  SpO2: 98% (excellent)")
        print("  Sleep quality: 87/100")
        time.sleep(1)

        print("\n🏃 ACTIVITY & WELLNESS")
        print("  Today's activity:")
        print("  • Steps: 8,240 / 10,000 goal")
        print("  • Active minutes: 45 min")
        print("  • Calories burned: 420 kcal")
        print("  ✓ On track to meet daily goals")
        time.sleep(1)

        print("\n🔬 PREDICTIVE HEALTH INSIGHTS")
        self.simulate_ai_processing("Pattern analysis and health prediction")
        print("  ⚠️  Irregular sleep pattern detected (last 3 days)")
        print("  📊 Recommendation: Earlier bedtime (10:30 PM)")
        print("  🎯 Predicted wellness improvement: +8%")
        time.sleep(1)

        print("\n💊 MEDICATION & CARE")
        print("  Reminder: Blood pressure medication due at 8:00 PM")
        print("  ✓ Appointment scheduled: Dr. Smith (Thu 2:00 PM)")
        print("  ✓ Lab results: Normal range (uploaded to portal)")

    def run(self, duration=12):
        """Run pygame visual demo with unified Neon HUD theme"""
        if not self.screen:
            self.run_demo_cycle()
            return

        from scenes.theme_neon import render_realm_hud

        start_time = time.time()
        clock = pygame.time.Clock()

        # Define content sections that rotate over time
        content_sections = [
            {
                'title': 'CONTINUOUS VITAL MONITORING',
                'items': [
                    "Heart Rate: 68 bpm (Normal)",
                    "Blood Pressure: 118/76 mmHg (Optimal)",
                    "SpO2: 98% (Excellent)",
                    "Sleep Score: 87/100",
                    "All vitals within healthy range"
                ]
            },
            {
                'title': 'ACTIVITY & FITNESS TRACKING',
                'items': [
                    "Steps: 8,240 / 10,000 (82% complete)",
                    "Active Minutes: 45 min",
                    "Calories burned: 420 kcal",
                    "On track to meet daily goals",
                    "Exercise recommendation: 15min walk"
                ]
            },
            {
                'title': 'PREDICTIVE HEALTH AI',
                'items': [
                    "Irregular sleep pattern detected (3 days)",
                    "Recommendation: Earlier bedtime (10:30 PM)",
                    "Predicted wellness improvement: +8%",
                    "Medication reminder: 8:00 PM today",
                    "Next checkup: Dr. Smith (Thu 2:00 PM)"
                ]
            }
        ]

        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return

            elapsed = time.time() - start_time

            render_realm_hud(
                screen=self.screen,
                realm_id='clinical',
                title='CLINICAL REALM',
                subtitle='Health Monitoring · Wellness · Medical AI',
                mode='Consumer Mode',
                content_sections=content_sections,
                elapsed=elapsed,
                duration=duration
            )

            clock.tick(30)

    def get_status(self) -> dict:
        """Get clinical realm status"""
        return {
            "realm": self.realm_name,
            "active": self.is_active,
            "health_devices": len(self.health_devices),
            "patients": len(self.patients),
            "mesh_strength": self.beam_network.mesh_strength
        }
