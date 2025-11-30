"""
MotiBeam Spatial OS - Home Realm
Smart Home, Family Management, Ambient Living
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

    def run(self, duration=10):
        """Run pygame visual demo for specified duration"""
        if not PYGAME_AVAILABLE or not self.screen:
            self.run_demo_cycle()
            return

        start_time = time.time()
        clock = pygame.time.Clock()

        # Colors
        BG = (15, 20, 35)
        WHITE = (255, 255, 255)
        ACCENT = (100, 200, 255)
        GREEN = (100, 255, 150)

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
            title = title_font.render("🏡 HOME REALM", True, WHITE)
            self.screen.blit(title, (50, 50))

            subtitle = subtitle_font.render("Smart Home · Family · Ambient Living", True, ACCENT)
            self.screen.blit(subtitle, (50, 150))

            # Content based on elapsed time
            y = 250

            if elapsed < 3:
                section = text_font.render("MORNING ROUTINE AUTOMATION", True, GREEN)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "✓ Sarah waking up detected (6:45 AM)",
                    "✓ Bedroom lights: Gradual warm-up",
                    "✓ Coffee maker: Brewing started",
                    "✓ Personalized news briefing ready"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            elif elapsed < 6:
                section = text_font.render("FAMILY PRESENCE & ACTIVITY", True, GREEN)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "👨 Dad: Home Office (Focus Mode)",
                    "👩 Mom: Kitchen (Meal Prep)",
                    "👧👦 Kids: Playroom (Active Play)",
                    "✓ 47 smart devices synchronized"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            else:
                section = text_font.render("ENERGY & SECURITY", True, GREEN)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "⚡ Solar: 6.8 kW generating",
                    "📊 Usage: 4.2 kW consuming",
                    "💰 Net: +2.6 kW to grid",
                    "🔐 All zones secured · No alerts"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            # Footer
            footer = small_font.render(f"Ambient Intelligence Active · {int(duration - elapsed)}s remaining", True, ACCENT)
            self.screen.blit(footer, (50, 950))

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
