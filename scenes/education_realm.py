"""
MotiBeam Spatial OS - Education Realm
Learning Environments, Study Focus, Knowledge Management
"""

import random
import time
from datetime import datetime
from core.base_realm import SpatialRealm
from core.spatial_engine import SpatialEngine, BeamNetworkProtocol

import pygame


class EducationRealm(SpatialRealm):
    """Education and learning ambient computing realm"""

    def __init__(self, standalone=False):
        super().__init__(
            realm_name="Education Realm",
            realm_description="Learning Environments, Study Focus, Knowledge Management"
        )
        self.spatial_engine = SpatialEngine()
        self.beam_network = BeamNetworkProtocol()
        self.learning_sessions = []
        self.students = []
        self.screen = None
        self.standalone = standalone

    def initialize(self) -> bool:
        """Initialize education realm systems"""
        print("  📚 Initializing Education Realm Systems...")

        scan = self.spatial_engine.scan_environment("education")
        print(f"  ✓ Learning space mapped: {scan['room_dimensions']}")

        self.beam_network.establish_mesh("Education Network")

        self.learning_sessions = [
            {"id": "MATH-101", "subject": "Calculus", "student": "Alex", "progress": 67},
            {"id": "PHYS-201", "subject": "Quantum Mechanics", "student": "Sam", "progress": 82},
            {"id": "LANG-FR", "subject": "French", "student": "Emma", "progress": 45}
        ]

        print("  ✓ Education systems online")
        return True

    def run_demo_cycle(self) -> None:
        """Demonstrate education realm capabilities (text mode)"""
        self.display_header()

        print("\n📚 LEARNING ENVIRONMENT OVERVIEW")
        print("  Active students: 4")
        print("  Study sessions today: 3")
        print("  Focus score: 88/100")
        print("  Knowledge retention: High")
        time.sleep(1)

        print("\n🎯 ADAPTIVE LEARNING SESSION")
        print("  Student: Alex (Studying Calculus)")
        self.simulate_ai_processing("Personalized learning path optimization")
        print("  Current topic: Integration by parts")
        print("  Comprehension level: 73%")
        print("  ✓ Adjusted difficulty: Medium → Advanced")
        print("  ✓ Recommended: 3 practice problems")
        time.sleep(1)

        print("\n🧠 FOCUS & ATTENTION MANAGEMENT")
        print("  Environment optimization:")
        print("  • Lighting: Adjusted to focus mode (cool white)")
        print("  • Audio: Background noise cancellation active")
        print("  • Distractions blocked: 12 notifications silenced")
        print("  ⏱️  Pomodoro timer: 22 minutes remaining")
        time.sleep(1)

        print("\n📊 LEARNING ANALYTICS")
        self.simulate_ai_processing("Knowledge gap analysis")
        print("  Strengths:")
        print("  • Differential equations: 92% mastery")
        print("  • Linear algebra: 88% mastery")
        print("  Focus areas:")
        print("  • Integration techniques: 65% (practice needed)")
        print("  ✓ Personalized practice set generated")
        time.sleep(1)

        print("\n🎓 STUDY GROUP COORDINATION")
        print("  Detected: 3 students studying related topics")
        print("  ✓ Suggested collaborative session at 3:00 PM")
        print("  ✓ Shared AR whiteboard prepared")
        print("  ✓ Study materials synchronized")

    def run(self, duration=12):
        """Run teacher's assistant display with big flashcard concepts"""
        if not self.screen:
            self.run_demo_cycle()
            return

        from scenes.theme_neon import (
            get_fonts, draw_background, draw_header,
            draw_footer_ticker, REALM_COLORS, COLOR_TEXT_PRIMARY,
            COLOR_TEXT_SECONDARY
        )

        start_time = time.time()
        clock = pygame.time.Clock()
        accent_color = REALM_COLORS.get('education', (150, 150, 255))
        fonts = get_fonts(self.screen)
        w, h = self.screen.get_size()

        # Flashcard concepts that cycle every 4 seconds
        concepts = [
            {
                'title': 'Concept: Photosynthesis',
                'content': 'Process by which plants convert',
                'content2': 'light energy into chemical energy',
                'detail': 'Uses: CO₂ + H₂O + Light → Glucose + O₂'
            },
            {
                'title': 'Question: Why are plants green?',
                'content': 'Plants reflect green wavelengths',
                'content2': 'while absorbing red and blue light',
                'detail': 'Answer: Chlorophyll pigment reflects green'
            },
            {
                'title': 'Concept: Cell Division - Mitosis',
                'content': 'Process where one cell divides',
                'content2': 'into two identical daughter cells',
                'detail': 'Phases: Prophase → Metaphase → Anaphase → Telophase'
            }
        ]

        # Ticker for learning stats
        ticker_items = [
            "Session: Calculus Study (Advanced)",
            "Focus time: 22 minutes remaining",
            "Mastery: Differential Equations 92%",
            "Next up: Integration Techniques",
            "Comprehension level: 73% (Good pace)",
            "Pomodoro break in 18 minutes"
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
                self.screen, fonts, 'education',
                'EDUCATION REALM',
                'Adaptive Learning · Focus · Knowledge Management',
                accent_color, "● LIVE"
            )

            # === MIDDLE BAND: Big centered flashcard ===
            y_center = 280

            # Determine which concept to show (cycle every 4 seconds)
            concept_index = int(elapsed / 4) % len(concepts)
            concept = concepts[concept_index]

            # Draw concept title (huge)
            title_surf = fonts['title'].render(concept['title'], True, accent_color)
            title_w = title_surf.get_width()
            self.screen.blit(title_surf, ((w - title_w) // 2, y_center))

            # Draw content lines (mega font for maximum readability)
            y_content = y_center + 120
            content_surf = fonts['huge'].render(concept['content'], True, COLOR_TEXT_PRIMARY)
            content_w = content_surf.get_width()
            self.screen.blit(content_surf, ((w - content_w) // 2, y_content))

            content2_surf = fonts['huge'].render(concept['content2'], True, COLOR_TEXT_PRIMARY)
            content2_w = content2_surf.get_width()
            self.screen.blit(content2_surf, ((w - content2_w) // 2, y_content + 100))

            # Draw detail/answer (smaller, below)
            detail_surf = fonts['body'].render(concept['detail'], True, COLOR_TEXT_SECONDARY)
            detail_w = detail_surf.get_width()
            self.screen.blit(detail_surf, ((w - detail_w) // 2, y_content + 220))

            # Progress indicator (right side)
            progress_x = w - 350
            progress_y = y_center + 50

            current_card = concept_index + 1
            total_cards = len(concepts)

            progress_text = f"Card {current_card} / {total_cards}"
            progress_surf = fonts['body'].render(progress_text, True, accent_color)
            self.screen.blit(progress_surf, (progress_x, progress_y))

            # Progress bar
            bar_width = 280
            bar_height = 20
            bar_x = progress_x
            bar_y = progress_y + 60

            # Background bar
            pygame.draw.rect(self.screen, (40, 40, 60),
                           (bar_x, bar_y, bar_width, bar_height), border_radius=10)

            # Filled portion
            fill_width = int(bar_width * (current_card / total_cards))
            pygame.draw.rect(self.screen, accent_color,
                           (bar_x, bar_y, fill_width, bar_height), border_radius=10)

            # Mode indicator
            mode_surf = fonts['body'].render("CONCEPT MODE", True, accent_color)
            self.screen.blit(mode_surf, (progress_x, bar_y + 50))

            # Bottom ticker
            draw_footer_ticker(
                self.screen, fonts,
                "Consumer Mode", remaining, 'education',
                accent_color, ticker_text, elapsed
            )

            pygame.display.flip()
            clock.tick(30)

    def get_status(self) -> dict:
        """Get education realm status"""
        return {
            "realm": self.realm_name,
            "active": self.is_active,
            "learning_sessions": len(self.learning_sessions),
            "students": len(self.students),
            "mesh_strength": self.beam_network.mesh_strength
        }
