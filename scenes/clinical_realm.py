"""
MotiBeam Spatial OS - Clinical Realm
Health Monitoring, Wellness Tracking, Medical Assistance
"""

import random
import time
from datetime import datetime
from core.base_realm import SpatialRealm
from core.spatial_engine import SpatialEngine, BeamNetworkProtocol

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


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

    def run(self, duration=10):
        """Run pygame visual demo for specified duration"""
        if not PYGAME_AVAILABLE or not self.screen:
            self.run_demo_cycle()
            return

        start_time = time.time()
        clock = pygame.time.Clock()

        # Colors
        BG = (20, 15, 30)
        WHITE = (255, 255, 255)
        ACCENT = (150, 220, 255)
        HEALTH = (100, 255, 180)
        WARNING = (255, 200, 100)

        try:
            title_font = pygame.font.Font(None, 84)
            subtitle_font = pygame.font.Font(None, 48)
            text_font = pygame.font.Font(None, 36)
            small_font = pygame.font.Font(None, 28)
        except:
            title_font = pygame.font.SysFont('arial', 84, bold=True)
            subtitle_font = pygame.font.SysFont('arial', 48)
            text_font = pygame.font.SysFont('arial', 36)
            small_font = pygame.font.SysFont('arial', 28)

        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.screen.fill(BG)
            elapsed = time.time() - start_time

            # Title
            title = title_font.render("⚕️  CLINICAL REALM", True, WHITE)
            self.screen.blit(title, (50, 50))

            subtitle = subtitle_font.render("Health Monitoring · Wellness · Medical AI", True, ACCENT)
            self.screen.blit(subtitle, (50, 150))

            # Content based on elapsed time
            y = 250

            if elapsed < 3:
                section = text_font.render("CONTINUOUS VITAL MONITORING", True, HEALTH)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "💓 Heart Rate: 68 bpm (Normal)",
                    "🩸 Blood Pressure: 118/76 mmHg (Optimal)",
                    "🫁 SpO2: 98% (Excellent)",
                    "😴 Sleep Score: 87/100"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            elif elapsed < 6:
                section = text_font.render("ACTIVITY & FITNESS TRACKING", True, HEALTH)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "🏃 Steps: 8,240 / 10,000 (82%)",
                    "⏱️  Active Minutes: 45 min",
                    "🔥 Calories: 420 kcal burned",
                    "✓ On track to meet daily goals"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            else:
                section = text_font.render("PREDICTIVE HEALTH AI", True, WARNING)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "⚠️  Irregular sleep pattern (3 days)",
                    "📊 Recommend: Earlier bedtime 10:30 PM",
                    "🎯 Predicted improvement: +8% wellness",
                    "💊 Medication reminder: 8:00 PM today"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            # Footer
            footer = small_font.render(f"12 Health Devices Connected · Wellness Score: 94/100 · {int(duration - elapsed)}s", True, ACCENT)
            self.screen.blit(footer, (50, 950))

            pygame.display.flip()
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
