"""
MotiBeam Spatial OS - Home Realm
Smart Home, Family Management, Ambient Living
"""

import random
import time
from datetime import datetime
from core.base_realm import SpatialRealm
from core.spatial_engine import SpatialEngine, BeamNetworkProtocol

import pygame


class HomeRealm(SpatialRealm):
    """Smart home and family ambient computing realm"""

    def __init__(self, standalone=False):
        super().__init__(
            realm_name="Home Realm",
            realm_description="Smart Home, Family Management, Ambient Living"
        )
        self.spatial_engine = SpatialEngine()
        self.beam_network = BeamNetworkProtocol()
        self.smart_devices = []
        self.family_members = []
        self.screen = None
        self.standalone = standalone

    def initialize(self) -> bool:
        """Initialize home realm systems"""
        print("  🏡 Initializing Home Realm Systems...")

        scan = self.spatial_engine.scan_environment("home")
        print(f"  ✓ Home mapped: {scan['room_dimensions']}")

        self.beam_network.establish_mesh("Home Network")

        self.smart_devices = [
            {"id": "LIGHT-01", "type": "Smart Lights", "room": "Living Room", "status": "On"},
            {"id": "THERM-01", "type": "Thermostat", "room": "Main", "status": "Auto"},
            {"id": "CAM-01", "type": "Security Camera", "room": "Front Door", "status": "Active"},
            {"id": "LOCK-01", "type": "Smart Lock", "room": "Front Door", "status": "Locked"}
        ]

        print("  ✓ Home systems online")
        return True

    def run_demo_cycle(self) -> None:
        """Demonstrate home realm capabilities (text mode)"""
        self.display_header()

        print("\n🏡 SMART HOME OVERVIEW")
        print("  Connected devices: 47")
        print("  Family members home: 3/4")
        print("  Energy usage: Optimal")
        print("  Security: All zones secured")
        time.sleep(1)

        print("\n🌅 MORNING ROUTINE AUTOMATION")
        print("  Detected: Sarah waking up (6:45 AM)")
        self.simulate_ai_processing("Personalized morning routine")
        print("  ✓ Bedroom lights: Gradual warm-up started")
        print("  ✓ Thermostat: Raised to 72°F")
        print("  ✓ Coffee maker: Brewing started")
        print("  ✓ News briefing: Queued on kitchen display")
        time.sleep(1)

        print("\n👨‍👩‍👧‍👦 FAMILY PRESENCE & ACTIVITY")
        print("  • Dad: Home office (focused work mode)")
        print("  • Mom: Kitchen (meal prep detected)")
        print("  • Kids: Playroom (active play mode)")
        print("  ✓ Adjusted lighting, climate, and audio zones")
        time.sleep(1)

        print("\n🔐 PROACTIVE SECURITY")
        print("  Event: Package delivered at front door")
        self.simulate_ai_processing("Facial recognition and authorization")
        print("  ✓ Delivery person recognized (USPS)")
        print("  ✓ Package logged and family notified")
        print("  ✓ No action needed - expected delivery")
        time.sleep(1)

        print("\n⚡ ENERGY OPTIMIZATION")
        print("  Current usage: 4.2 kW")
        print("  Solar generation: 6.8 kW")
        print("  Net: +2.6 kW (feeding grid)")
        print("  💰 Today's savings: $12.40")

    def run(self, duration=12):
        """Run live HUD demo with two-column layout and scrolling ticker"""
        if not self.screen:
            self.run_demo_cycle()
            return

        from scenes.theme_neon import (
            get_fonts, draw_background, draw_header,
            draw_two_column_layout, draw_footer_ticker,
            REALM_COLORS
        )

        start_time = time.time()
        clock = pygame.time.Clock()
        accent_color = REALM_COLORS.get('home', (100, 200, 255))
        fonts = get_fonts(self.screen)

        # Scrolling ticker updates
        ticker_items = [
            "Laundry done in 12m",
            "Front door locked",
            "Bedtime routine in 2h 15m",
            "Thermostat adjusted to 68F",
            "Living room lights dimmed",
            "Coffee maker ready for 6:45 AM",
            "Security system armed",
            "Energy grid: selling 2.6 kW"
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

            # Background with living motion
            draw_background(self.screen, elapsed)

            # Header band
            draw_header(
                self.screen, fonts, 'home',
                'HOME REALM',
                'Smart Home · Family · Ambient Living',
                accent_color, "● LIVE"
            )

            # Middle band - Two columns
            left_section = {
                'title': 'FAMILY PRESENCE',
                'items': [
                    "Dad: Home Office (Focus Mode)",
                    "Mom: Kitchen (Meal Prep)",
                    "Kids: Playroom (Active Play)",
                    "",
                    "47 devices synchronized",
                    "All zones comfortable"
                ]
            }

            right_section = {
                'title': 'TODAY\'S AUTOMATIONS',
                'items': [
                    "Morning: Coffee + lights (6:45 AM)",
                    "Midday: Climate optimization",
                    "Evening: Dinner ambiance (6:30 PM)",
                    "",
                    "Energy: Solar 6.8 kW → Grid 2.6 kW",
                    "Savings today: $12.40"
                ]
            }

            draw_two_column_layout(
                self.screen, fonts,
                left_section, right_section,
                y_start=250, accent_color=accent_color
            )

            # Bottom band - Scrolling ticker
            draw_footer_ticker(
                self.screen, fonts,
                "Consumer Mode", remaining, 'home',
                accent_color, ticker_text, elapsed
            )

            pygame.display.flip()
            clock.tick(30)

    def get_status(self) -> dict:
        """Get home realm status"""
        return {
            "realm": self.realm_name,
            "active": self.is_active,
            "smart_devices": len(self.smart_devices),
            "family_members": len(self.family_members),
            "mesh_strength": self.beam_network.mesh_strength
        }
