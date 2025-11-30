"""
MotiBeam Spatial OS - Emergency Response Realm
911 Dispatch, Crisis Response, Medical Emergency Management
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


class EmergencyRealm(SpatialRealm):
    """Emergency response and crisis management realm"""

    def __init__(self, standalone=False):
        super().__init__(
            realm_name="Emergency Response Realm",
            realm_description="911 Dispatch, Crisis Response, Medical Emergency Management"
        )
        self.spatial_engine = SpatialEngine()
        self.beam_network = BeamNetworkProtocol()
        self.active_incidents = []
        self.emergency_units = []
        self.screen = None
        self.standalone = standalone

    def initialize(self) -> bool:
        """Initialize emergency response systems"""
        print("  🚨 Initializing Emergency Response Systems...")

        # Initialize spatial awareness
        scan = self.spatial_engine.scan_environment("emergency")
        print(f"  ✓ Emergency zone mapped: {scan['room_dimensions']}")

        # Establish emergency mesh network
        self.beam_network.establish_mesh("Emergency Response")

        # Initialize emergency units
        self.emergency_units = [
            {"id": "AMB-01", "type": "Ambulance", "status": "Ready", "location": "Station 3"},
            {"id": "FIRE-02", "type": "Fire Engine", "status": "Ready", "location": "Station 1"},
            {"id": "POL-05", "type": "Police", "status": "Patrol", "location": "Sector 7"}
        ]

        print("  ✓ Emergency response systems online")
        return True

    def run_demo_cycle(self) -> None:
        """Demonstrate emergency response capabilities"""
        self.display_header()

        print("\n📞 INCOMING 911 CALL")
        print("  Caller: Elderly male, chest pain, difficulty breathing")
        print("  Location: 42.3601° N, 71.0589° W (Boston, MA)")
        time.sleep(1)

        # AI Triage
        self.simulate_ai_processing("Emergency triage and classification")
        print("  🎯 Priority: CRITICAL - Suspected cardiac event")
        print("  📊 Confidence: 94%")
        time.sleep(1)

        # Spatial mapping of incident
        print("\n🗺️  SPATIAL INCIDENT MAPPING")
        scan = self.spatial_engine.scan_environment("incident_location")
        print(f"  Location: Residential building, 3rd floor")
        print(f"  Access points: 2 entrances, elevator available")
        print(f"  Nearest AED: 150m (CVS Pharmacy)")
        time.sleep(1)

        # Resource allocation
        print("\n🚑 RESOURCE ALLOCATION")
        self.simulate_ai_processing("Optimal unit dispatch calculation")

        print("  Dispatching:")
        print("    • AMB-01 (ETA: 3m 45s) - Priority 1")
        print("    • FIRE-02 (ETA: 4m 12s) - Support")
        print("    • Alerting nearby civilian AED carriers")
        time.sleep(1)

        # Real-time coordination
        print("\n📡 REAL-TIME COORDINATION")
        self.spatial_engine.create_ar_overlay("Route optimization", "responder_HUD")
        print("  ✓ AR navigation overlay sent to AMB-01")
        print("  ✓ Building access codes transmitted")
        print("  ✓ Patient vitals streaming to paramedics")
        time.sleep(1)

        # Predictive analysis
        print("\n🔮 PREDICTIVE CRISIS ANALYSIS")
        self.simulate_ai_processing("Pattern recognition across city incidents")
        print("  ⚠️  Alert: Traffic congestion detected on Route 9")
        print("  ✓ Auto-routing AMB-01 via alternate path")
        print("  📉 ETA reduced by 47 seconds")
        time.sleep(1)

        # Outcome
        print("\n✅ INCIDENT RESOLUTION")
        print("  • Paramedics arrived: 3m 28s")
        print("  • Patient stabilized on-scene")
        print("  • En route to Mass General Hospital")
        print("  • Family members notified")
        print("  • Incident logged and analyzed for system improvement")

    def get_status(self) -> dict:
        """Get emergency realm status"""
        return {
            "realm": self.realm_name,
            "active": self.is_active,
            "active_incidents": len(self.active_incidents),
            "available_units": len([u for u in self.emergency_units if u["status"] == "Ready"]),
            "mesh_strength": self.beam_network.mesh_strength
        }

    def dispatch_unit(self, unit_id: str, incident_id: str) -> None:
        """Dispatch emergency unit to incident"""
        print(f"  🚨 Dispatching {unit_id} to incident {incident_id}")

    def simulate_emergency_call(self) -> dict:
        """Simulate an incoming emergency call"""
        emergency_types = [
            "Cardiac arrest",
            "Structure fire",
            "Armed robbery",
            "Vehicle accident",
            "Medical emergency"
        ]

        return {
            "type": random.choice(emergency_types),
            "severity": random.choice(["Critical", "High", "Medium"]),
            "location": f"{random.uniform(42.0, 43.0):.4f}° N, {random.uniform(-71.5, -70.5):.4f}° W",
            "timestamp": datetime.now()
        }

    def run(self, duration=10):
        """Run pygame visual demo for specified duration"""
        if not PYGAME_AVAILABLE or not self.screen:
            self.run_demo_cycle()
            return

        start_time = time.time()
        clock = pygame.time.Clock()

        # Colors
        BG = (30, 10, 10)
        WHITE = (255, 255, 255)
        ACCENT = (255, 100, 100)
        CRITICAL = (255, 50, 50)

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
            title = title_font.render("🚨 EMERGENCY RESPONSE", True, WHITE)
            self.screen.blit(title, (50, 50))

            subtitle = subtitle_font.render("911 Dispatch · Crisis Management · Medical AI", True, ACCENT)
            self.screen.blit(subtitle, (50, 150))

            # Content based on elapsed time
            y = 250

            if elapsed < 3:
                section = text_font.render("INCOMING 911 CALL", True, CRITICAL)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "📞 Elderly male, chest pain",
                    "📍 Boston, MA (42.3601° N)",
                    "🎯 Priority: CRITICAL - Cardiac event",
                    "📊 AI Confidence: 94%"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            elif elapsed < 6:
                section = text_font.render("RESOURCE ALLOCATION", True, ACCENT)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "🚑 AMB-01 dispatched (ETA: 3m 45s)",
                    "🚒 FIRE-02 backup (ETA: 4m 12s)",
                    "📡 AR navigation → responders",
                    "✓ Building access codes sent"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            else:
                section = text_font.render("INCIDENT RESOLUTION", True, ACCENT)
                self.screen.blit(section, (50, y))
                y += 60

                items = [
                    "✓ Paramedics arrived: 3m 28s",
                    "✓ Patient stabilized on-scene",
                    "✓ En route to hospital",
                    "✓ Incident logged for AI learning"
                ]
                for item in items:
                    text = small_font.render(item, True, WHITE)
                    self.screen.blit(text, (80, y))
                    y += 45

            # Footer
            footer = small_font.render(f"Emergency Units Ready · Real-time Coordination · {int(duration - elapsed)}s", True, ACCENT)
            self.screen.blit(footer, (50, 950))

            pygame.display.flip()
            clock.tick(30)
