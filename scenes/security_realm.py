"""
MotiBeam Spatial OS - Security & Surveillance Realm
Perimeter Defense, Access Control, Threat Detection
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


class SecurityRealm(SpatialRealm):
    """Security, surveillance, and access control realm"""

    def __init__(self, standalone=False):
        super().__init__(
            realm_name="Security & Surveillance Realm",
            realm_description="Perimeter Defense, Access Control, Threat Detection"
        )
        self.spatial_engine = SpatialEngine()
        self.beam_network = BeamNetworkProtocol()
        self.security_zones = []
        self.access_points = []
        self.detected_threats = []
        self.screen = None
        self.standalone = standalone

    def initialize(self) -> bool:
        """Initialize security systems"""
        print("  🛡️  Initializing Security & Surveillance Systems...")

        # Initialize spatial security mapping
        scan = self.spatial_engine.scan_environment("security_perimeter")
        print(f"  ✓ Security perimeter mapped: {scan['room_dimensions']}")

        # Establish secure mesh network
        self.beam_network.establish_mesh("Security Operations")

        # Initialize security zones
        self.security_zones = [
            {"id": "ZONE-A", "name": "Main Entrance", "level": "Public", "cameras": 4},
            {"id": "ZONE-B", "name": "Server Room", "level": "Restricted", "cameras": 8},
            {"id": "ZONE-C", "name": "Executive Floor", "level": "High Security", "cameras": 12},
            {"id": "ZONE-D", "name": "Perimeter", "level": "Monitored", "cameras": 16}
        ]

        print("  ✓ Security systems armed and ready")
        return True

    def run_demo_cycle(self) -> None:
        """Demonstrate security and surveillance capabilities"""
        self.display_header()

        print("\n🎥 MULTI-ZONE SURVEILLANCE ACTIVE")
        print("  Cameras online: 40")
        print("  AI-powered analysis: ENABLED")
        print("  Facial recognition: ACTIVE")
        print("  Behavior anomaly detection: MONITORING")
        time.sleep(1)

        # Perimeter monitoring
        print("\n🌐 SPATIAL PERIMETER MONITORING")
        scan = self.spatial_engine.scan_environment("perimeter")
        print(f"  Zone coverage: 360° panoramic")
        print(f"  Objects tracked: {scan['objects_detected']}")
        print(f"  Personnel detected: {scan['people_detected']}")
        time.sleep(1)

        # Anomaly detection
        print("\n⚠️  ANOMALY DETECTED")
        print("  Location: Loading Dock (ZONE-D)")
        print("  Event: Unauthorized access attempt")
        print("  Time: " + datetime.now().strftime("%H:%M:%S"))
        time.sleep(1)

        self.simulate_ai_processing("Facial recognition and behavior analysis")
        print("  🔍 Subject: Unknown individual")
        print("  📊 Behavior score: 73/100 (Suspicious)")
        print("  🎯 Threat level: MODERATE")
        time.sleep(1)

        # AR-enhanced surveillance
        print("\n🔮 AR-ENHANCED SURVEILLANCE")
        self.spatial_engine.create_ar_overlay("Subject tracking overlay", "security_HUD")
        print("  ✓ Real-time subject tracking enabled")
        print("  ✓ Movement prediction: 85% confidence")
        print("  ✓ Security team alerted")
        time.sleep(1)

        # Access control
        print("\n🚪 INTELLIGENT ACCESS CONTROL")
        print("  Event: Badge scan at Server Room entrance")
        self.simulate_ai_processing("Multi-factor authentication verification")
        print("  ✓ Badge: VALID (Employee ID: E-7842)")
        print("  ✓ Biometric: MATCH (Fingerprint)")
        print("  ✓ Location context: APPROVED")
        print("  ✓ Time-based access: AUTHORIZED")
        print("  → Access GRANTED")
        time.sleep(1)

        # Predictive security
        print("\n🔮 PREDICTIVE SECURITY ANALYSIS")
        self.simulate_ai_processing("Pattern analysis across security logs")
        print("  📊 Insights:")
        print("    • Peak traffic: 09:00-09:30, 17:30-18:00")
        print("    • Anomaly clusters: Loading dock (Wed-Fri evenings)")
        print("    • Recommendation: Deploy additional cameras at dock area")
        print("    • Predicted risk reduction: 34%")
        time.sleep(1)

        # Threat response
        print("\n✅ AUTOMATED THREAT RESPONSE")
        print("  • Loading dock intruder: Security team dispatched")
        print("  • Zone D lighting: Increased to 100%")
        print("  • Warning broadcast: Issued to subject")
        print("  • Law enforcement: Notified (standby)")
        print("  • Incident logged for pattern analysis")

    def get_status(self) -> dict:
        """Get security realm status"""
        return {
            "realm": self.realm_name,
            "active": self.is_active,
            "security_zones": len(self.security_zones),
            "active_threats": len(self.detected_threats),
            "mesh_strength": self.beam_network.mesh_strength
        }

    def scan_zone(self, zone_id: str) -> dict:
        """Scan specific security zone"""
        return {
            "zone": zone_id,
            "status": "clear",
            "occupancy": random.randint(0, 10),
            "last_scan": datetime.now()
        }

    def run(self, duration=10):
        """Run pygame visual demo with HUD theme"""
        if not PYGAME_AVAILABLE or not self.screen:
            self.run_demo_cycle()
            return

        from core.design_tokens import (
            get_fonts, draw_animated_background, draw_header_bar,
            draw_footer_hud, draw_content_card, REALM_COLORS
        )

        start_time = time.time()
        clock = pygame.time.Clock()
        accent_color = REALM_COLORS.get('security', (150, 100, 255))
        fonts = get_fonts(self.screen)

        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            elapsed = time.time() - start_time
            remaining = int(duration - elapsed)

            draw_animated_background(self.screen, elapsed)
            draw_header_bar(
                self.screen, fonts, "🛡️", "SECURITY & SURVEILLANCE",
                "Perimeter Defense · Access Control · Threat Detection",
                accent_color, "ARMED"
            )

            # Time-based content sections
            if elapsed < duration / 3:
                draw_content_card(
                    self.screen, fonts, "MULTI-ZONE SURVEILLANCE",
                    [
                        "🎥 Cameras online: 40 (AI-powered analysis)",
                        "🔍 Facial recognition: ACTIVE",
                        "📊 Behavior anomaly detection: MONITORING",
                        "🌐 360° panoramic perimeter coverage",
                        "✓ All zones secured and operational"
                    ],
                    280, accent_color
                )
            elif elapsed < duration * 2 / 3:
                draw_content_card(
                    self.screen, fonts, "THREAT DETECTION ALERT",
                    [
                        "⚠️ Unauthorized access attempt - Loading Dock",
                        "🔍 Subject: Unknown individual (no badge)",
                        "📊 Behavior score: 73/100 (Suspicious)",
                        "🎯 Threat level: MODERATE",
                        "✓ Security team dispatched to location"
                    ],
                    280, accent_color
                )
            else:
                draw_content_card(
                    self.screen, fonts, "INTELLIGENT ACCESS CONTROL",
                    [
                        "🚪 Server room entry request detected",
                        "✓ Badge: VALID (Employee ID: E-7842)",
                        "✓ Biometric: MATCH (Fingerprint verified)",
                        "✓ Location context: APPROVED",
                        "→ Multi-factor authentication: ACCESS GRANTED"
                    ],
                    280, accent_color
                )

            draw_footer_hud(
                self.screen, fonts,
                "Security & Surveillance · Operations Realm",
                f"Zones: 4 | Active: {remaining}s",
                "AI-Powered Protection",
                accent_color
            )

            pygame.display.flip()
            clock.tick(30)
