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
        """Run live HUD demo with enhanced wall-readable two-column layout"""
        if not self.screen:
            self.run_demo_cycle()
            return

        from scenes.theme_neon import (
            get_fonts, draw_background, draw_header,
            draw_two_column_layout, draw_footer_ticker,
            REALM_COLORS, render_icon
        )

        start_time = time.time()
        clock = pygame.time.Clock()
        accent_color = REALM_COLORS.get('home', (100, 200, 255))
        fonts = get_fonts(self.screen)
        w, h = self.screen.get_size()

        # Scrolling ticker updates
        ticker_items = [
            "Laundry done in 12m",
            "Front door locked",
            "Bedtime routine in 2h 15m",
            "Thermostat adjusted to 68°F",
            "Living room lights dimmed",
            "Coffee maker ready for 6:45 AM",
            "Security system armed",
            "Energy grid: selling 2.6 kW"
        ]
        ticker_text = " · ".join(ticker_items) + " · "

        # View cycling (4 different views)
        view_duration = duration / 4

        # Animated breathing neon circles (Home realm specific)
        circles = [
            {"x": w * 0.75, "y": h * 0.35, "r": 90, "dr": 0.25, "base": 90},
            {"x": w * 0.80, "y": h * 0.55, "r": 130, "dr": -0.2, "base": 130},
            {"x": w * 0.78, "y": h * 0.70, "r": 110, "dr": 0.18, "base": 110},
        ]

        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return

            elapsed = time.time() - start_time
            remaining = int(duration - elapsed)
            current_view = int(elapsed / view_duration) % 4

            # Background with living motion
            draw_background(self.screen, elapsed)

            # Draw animated breathing circles (Home realm ambient effect)
            for c in circles:
                # Update radius (breathing effect)
                c["r"] += c["dr"]
                if c["r"] > c["base"] + 15 or c["r"] < c["base"] - 15:
                    c["dr"] *= -1

                # Draw circle with neon glow
                radius = int(c["r"])
                x = int(c["x"])
                y = int(c["y"])

                # Create surface for circle with transparency
                s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

                # Draw glow (outer circle, semi-transparent)
                pygame.draw.circle(s, (*accent_color, 25), (radius, radius), radius)

                # Draw stroke (neon outline)
                pygame.draw.circle(s, (*accent_color, 120), (radius, radius), radius, 3)

                # Blit to screen
                self.screen.blit(s, (x - radius, y - radius), special_flags=pygame.BLEND_ADD)

            # Header band with emoji
            draw_header(
                self.screen, fonts, 'home',
                '🏡 HOME REALM',
                '🏠 Smart Home · 👨‍👩‍👧‍👦 Family · ☀️ Ambient Living',
                accent_color, "● LIVE"
            )

            # Middle band - Four rotating views
            if current_view == 0:
                # View 1: Home Overview
                left_section = {
                    'title': '👨‍👩‍👧‍👦 FAMILY PRESENCE',
                    'items': [
                        "👨 Dad: Home Office (Focus Mode)",
                        "👩 Mom: Kitchen (Meal Prep)",
                        "👧👦 Kids: Playroom (Active Play)",
                        "",
                        "📱 Devices online: 47",
                        "🏠 Today summary: All zones comfortable"
                    ]
                }

                right_section = {
                    'title': '🏡 SMART HOME STATUS',
                    'items': [
                        "🔒 Locks: All secured",
                        "📹 Cameras online: 2",
                        "📦 Deliveries today: 1",
                        "🌙 Quiet hours: 10:00 PM – 6:00 AM",
                        "",
                        "⚡ Rooms active: 3"
                    ]
                }

            elif current_view == 1:
                # View 2: Energy & Climate
                left_section = {
                    'title': '⚡ ENERGY MANAGEMENT',
                    'items': [
                        "☀️ Solar generation: 6.8 kW",
                        "🏠 Current usage: 4.2 kW",
                        "🔋 Net: +2.6 kW (feeding grid)",
                        "",
                        "💰 Today's savings: $12.40",
                        "📊 This month: $287.50"
                    ]
                }

                right_section = {
                    'title': '🌡️ CLIMATE & COMFORT',
                    'items': [
                        "Living Room: 72°F (optimal)",
                        "Bedroom: 68°F (sleep mode)",
                        "Office: 70°F (focus mode)",
                        "",
                        "Air quality: Excellent",
                        "Humidity: 45% (ideal)"
                    ]
                }

            elif current_view == 2:
                # View 3: Automation Routines
                left_section = {
                    'title': '⏰ TODAY\'S AUTOMATIONS',
                    'items': [
                        "☕ 6:45 AM - Morning routine",
                        "  Coffee + gradual lights",
                        "🌞 12:00 PM - Climate optimization",
                        "🍽️ 6:30 PM - Dinner ambiance",
                        "🌙 10:00 PM - Bedtime routine"
                    ]
                }

                right_section = {
                    'title': '🔐 SECURITY EVENTS',
                    'items': [
                        "📦 3:42 PM - USPS delivery",
                        "  Package logged & notified",
                        "🚗 4:15 PM - Garage opened",
                        "  Mom arrived home",
                        "✅ All zones secure"
                    ]
                }

            else:
                # View 4: Ambient Loop (Large centered display)
                left_section = {
                    'title': '🌅 AMBIENT MODE',
                    'items': [
                        "",
                        "🏡 All systems nominal",
                        "👨‍👩‍👧‍👦 Family home & comfortable",
                        "⚡ Energy: Optimal",
                        "🔒 Security: All clear",
                        ""
                    ]
                }

                right_section = {
                    'title': '⏰ UPCOMING',
                    'items': [
                        "",
                        "🍽️ Dinner prep in 45 minutes",
                        "🌙 Bedtime routine in 2h 15m",
                        "☕ Coffee ready tomorrow 6:45 AM",
                        "",
                        ""
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
