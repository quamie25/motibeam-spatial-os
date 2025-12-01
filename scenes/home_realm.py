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

    def run(self, duration=15):
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
                'title': 'MORNING ROUTINE AUTOMATION',
                'items': [
                    "Sarah waking up detected (6:45 AM)",
                    "Bedroom lights: Gradual warm-up started",
                    "Coffee maker: Brewing started",
                    "Personalized news briefing ready",
                    "47 smart devices synchronized"
                ]
            },
            {
                'title': 'FAMILY PRESENCE & ACTIVITY',
                'items': [
                    "Dad: Home Office (Focus Mode)",
                    "Mom: Kitchen (Meal Prep)",
                    "Kids: Playroom (Active Play)",
                    "Adjusted lighting, climate, audio zones",
                    "Activity patterns learned and optimized"
                ]
            },
            {
                'title': 'ENERGY & SECURITY OPTIMIZATION',
                'items': [
                    "Solar generation: 6.8 kW",
                    "Current usage: 4.2 kW",
                    "Net: +2.6 kW to grid",
                    "All zones secured, no alerts",
                    "Today's energy savings: $12.40"
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
                realm_id='home',
                title='HOME REALM',
                subtitle='Smart Home · Family · Ambient Living',
                mode='Consumer Mode',
                content_sections=content_sections,
                elapsed=elapsed,
                duration=duration
            )

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
