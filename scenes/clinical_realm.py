"""
MotiBeam Spatial OS - Clinical Realm
Health Monitoring, Wellness Tracking, Medical Assistance
"""

import random
import time
from datetime import datetime
from core.base_realm import SpatialRealm
from core.spatial_engine import SpatialEngine, BeamNetworkProtocol
from core.global_state import global_state

import pygame


class ClinicalRealm(SpatialRealm):
    """Health and wellness ambient computing realm"""

    def __init__(self, screen=None, global_state_ref=None, standalone=False, **kwargs):
        super().__init__(
            realm_name="Clinical Realm",
            realm_description="Health Monitoring, Wellness Tracking, Medical Assistance"
        )
        self.screen = screen
        self.global_state = global_state_ref if global_state_ref is not None else global_state
        self.standalone = standalone
        self.spatial_engine = SpatialEngine()
        self.beam_network = BeamNetworkProtocol()
        self.health_devices = []
        self.patients = []

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
        """Run ambient care dashboard with wellness score and vitals"""
        if not self.screen:
            self.run_demo_cycle()
            return

        from scenes.theme_neon import (
            get_fonts, draw_background, draw_header,
            draw_footer_ticker, REALM_COLORS, COLOR_TEXT_PRIMARY,
            COLOR_ACCENT_GREEN, COLOR_ACCENT_ORANGE
        )

        start_time = time.time()
        clock = pygame.time.Clock()
        accent_color = REALM_COLORS.get('clinical', (100, 255, 200))
        fonts = get_fonts(self.screen)
        w, h = self.screen.get_size()

        # Ticker for gentle reminders
        ticker_items = [
            "Next checkup: Dr. Smith Thu 2:00 PM",
            "Medication due: 8:00 PM tonight",
            "Sleep quality: 87/100 (excellent)",
            "Hydration reminder: Drink water",
            "Activity goal: 8,240/10,000 steps (82%)",
            "Heart rate trending: Normal range all day"
        ]
        ticker_text = " · ".join(ticker_items) + " · "

        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return

            elapsed = time.time() - start_time
            remaining = int(duration - elapsed)

            # Background
            draw_background(self.screen, elapsed)

            # Header
            draw_header(
                self.screen, fonts, 'clinical',
                '⚕️ CLINICAL REALM',
                '🏥 Health Monitoring · 💊 Wellness · 🧬 Medical AI',
                accent_color, "● LIVE"
            )

            # === MIDDLE BAND: Three-section layout ===
            y_top = 250
            margin = 100

            # CENTER: Big Wellness Score
            wellness_score = 87
            # Color based on score
            if wellness_score >= 80:
                score_color = COLOR_ACCENT_GREEN
            elif wellness_score >= 60:
                score_color = COLOR_ACCENT_ORANGE
            else:
                score_color = (255, 100, 100)

            # Draw wellness score in center
            score_text = str(wellness_score)
            score_surf = fonts['mega'].render(score_text, True, score_color)
            score_w = score_surf.get_width()
            score_x = (w - score_w) // 2
            self.screen.blit(score_surf, (score_x, y_top + 100))

            # Label below score
            label_surf = fonts['header'].render("WELLNESS SCORE", True, accent_color)
            label_w = label_surf.get_width()
            self.screen.blit(label_surf, ((w - label_w) // 2, y_top + 300))

            # LEFT: Vitals
            left_x = margin
            left_y = y_top + 50

            vitals_title = fonts['header'].render("KEY VITALS", True, accent_color)
            self.screen.blit(vitals_title, (left_x, left_y))

            left_y += 90
            vitals = [
                ("Heart Rate", "68 bpm", COLOR_ACCENT_GREEN),
                ("Blood Pressure", "118/76", COLOR_ACCENT_GREEN),
                ("SpO₂", "98%", COLOR_ACCENT_GREEN),
                ("", "", None),  # Spacer
                ("Sleep Score", "87/100", accent_color),
            ]

            for label, value, color in vitals:
                if label:  # Skip spacers
                    label_surf = fonts['body'].render(label, True, COLOR_TEXT_PRIMARY)
                    self.screen.blit(label_surf, (left_x, left_y))

                    value_surf = fonts['body'].render(value, True, color if color else accent_color)
                    self.screen.blit(value_surf, (left_x + 350, left_y))
                left_y += 60

            # RIGHT: Medication Schedule
            right_x = w - margin - 600
            right_y = y_top + 50

            meds_title = fonts['header'].render("MEDICATIONS", True, accent_color)
            self.screen.blit(meds_title, (right_x, right_y))

            right_y += 90
            medications = [
                ("8:00 PM Tonight", "Blood pressure med"),
                ("Tomorrow 8:00 AM", "Vitamin D"),
                ("Tomorrow 12:00 PM", "Lunch supplement"),
                ("Tomorrow 8:00 PM", "Blood pressure med"),
            ]

            for time_str, med_name in medications:
                time_surf = fonts['body'].render(time_str, True, accent_color)
                self.screen.blit(time_surf, (right_x, right_y))
                right_y += 50

                med_surf = fonts['body'].render(med_name, True, COLOR_TEXT_PRIMARY)
                self.screen.blit(med_surf, (right_x + 20, right_y))
                right_y += 60

            # Bottom ticker
            draw_footer_ticker(
                self.screen, fonts,
                "Consumer Mode", remaining, 'clinical',
                accent_color, ticker_text, elapsed
            )

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
