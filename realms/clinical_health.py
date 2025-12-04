"""
MotiBeam Spatial OS - Clinical & Health Monitoring Realm
⚕️ Realm #2 - Real-time health monitoring with IoT/cloud integration

Designed for: OEM demos, healthcare providers, elderly monitoring
Focus: VISUAL, INTERACTIVE, MINIMAL TEXT - showcase monitoring capabilities

Features:
- Real-time animated vital signs (Heart Rate, BP, O2, Temp)
- ECG-style waveforms and visual indicators
- Alert system with visual cues
- Scrolling ticker for non-critical messages
- Body/Mind/Spirit subcategories (B/M/S keys)
- Minimal text - big numbers, visual status indicators
"""

import random
import math
from typing import List, Tuple, Dict
from datetime import datetime

# Import base realm (which already imports pygame)
from realms.base_realm import BaseRealm
import pygame


class VitalSign:
    """Animated vital sign with realistic variations"""

    def __init__(self, name: str, base_value: float, unit: str, min_val: float, max_val: float,
                 variation: float, color: Tuple[int, int, int]):
        self.name = name
        self.base_value = base_value
        self.current_value = base_value
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self.variation = variation
        self.color = color
        self.history: List[float] = [base_value] * 100
        self.alert = False
        self.trend = 0.0

    def update(self, dt: float):
        """Update vital sign with realistic variation"""
        # Smooth random walk
        self.trend += (random.random() - 0.5) * 0.1
        self.trend *= 0.95  # Decay

        # Calculate new value
        target = self.base_value + (random.random() - 0.5) * self.variation + self.trend
        self.current_value += (target - self.current_value) * dt * 2

        # Clamp to safe range
        self.current_value = max(self.min_val, min(self.max_val, self.current_value))

        # Update history
        self.history.append(self.current_value)
        if len(self.history) > 100:
            self.history.pop(0)

        # Check for alerts
        safe_range = (self.max_val - self.min_val) * 0.15
        self.alert = (self.current_value < self.min_val + safe_range or
                     self.current_value > self.max_val - safe_range)


class ScrollingTicker:
    """Scrolling text ticker for non-critical messages"""

    def __init__(self, messages: List[str], speed: float = 100.0):
        self.messages = messages
        self.current_message_index = 0
        self.scroll_x = 0.0
        self.speed = speed
        self.message_spacing = 400  # Space between messages

    def update(self, dt: float, width: int):
        """Update ticker scroll position"""
        self.scroll_x -= self.speed * dt

        # Reset when message scrolls off screen
        if self.scroll_x < -self.message_spacing:
            self.scroll_x += self.message_spacing
            self.current_message_index = (self.current_message_index + 1) % len(self.messages)

    def get_visible_messages(self) -> List[Tuple[str, float]]:
        """Get currently visible messages and their positions"""
        messages = []
        for i in range(3):  # Show up to 3 messages at once
            idx = (self.current_message_index + i) % len(self.messages)
            pos = self.scroll_x + (i * self.message_spacing)
            messages.append((self.messages[idx], pos))
        return messages


class ClinicalHealthPro(BaseRealm):
    """Clinical & Health Monitoring Realm - Visual, Interactive, Demo-Ready"""

    def __init__(self):
        super().__init__(
            realm_id=2,
            realm_name="CLINICAL & HEALTH MONITORING",
            realm_color=(80, 255, 120)
        )

        # Current view mode
        self.view_mode = "DASHBOARD"  # DASHBOARD, BODY, MIND, SPIRIT

        # Initialize vital signs (animated, real-time looking)
        self.vital_signs = [
            VitalSign("HEART RATE", 72, "BPM", 45, 100, 8, (255, 100, 120)),
            VitalSign("BLOOD PRESSURE", 120, "mmHg", 90, 140, 5, (100, 200, 255)),
            VitalSign("OXYGEN", 98, "%", 88, 100, 2, (100, 255, 150)),
            VitalSign("TEMPERATURE", 98.6, "°F", 97.0, 99.5, 0.5, (255, 200, 100)),
        ]

        # ECG simulation (for visual effect)
        self.ecg_data: List[float] = []
        self.ecg_timer = 0.0
        self.heart_beat_phase = 0.0

        # Health status indicators
        self.overall_status = "HEALTHY"
        self.wellness_score = 87

        # Scrolling ticker for non-critical messages
        ticker_messages = [
            "💊 Medication reminder: Blood pressure medication at 12:00 PM",
            "💧 Hydration goal: 6/8 glasses completed",
            "🚶 Activity: 20 minutes walking completed today",
            "😌 Stress level: LOW - Good work on relaxation exercises",
            "🌞 Vitamin D: 10 minutes sunlight recommended",
            "🧠 Cognitive exercise: Crossword puzzle completed",
            "❤️ Heart health: All readings normal",
        ]
        self.ticker = ScrollingTicker(ticker_messages, speed=150.0)

        # Body/Mind/Spirit wellness metrics (subcategories)
        self.body_score = 85
        self.mind_score = 78
        self.spirit_score = 92

        # Ambient particles
        self.bio_particles: List[dict] = []
        self.particle_timer = 0.0

        # Alert system
        self.active_alerts = []

        # Caregiver contact
        self.caregiver_contact = "Dr. Smith"

        print("🩺 Clinical & Health Monitoring Realm initialized")
        print("   Real-time vitals monitoring active")
        print("   IoT/cloud integration ready for demo")

    def update(self, dt: float):
        """Update health monitoring system"""
        # Update vital signs
        for vital in self.vital_signs:
            vital.update(dt)

        # Update ECG simulation
        self.update_ecg(dt)

        # Update scrolling ticker
        self.ticker.update(dt, self.width)

        # Update biometric particles
        self.particle_timer += dt
        if self.particle_timer > 0.1:
            self.particle_timer = 0.0
            self.spawn_bio_particle()

        for particle in self.bio_particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['life'] -= dt * 0.5

            if particle['life'] <= 0:
                self.bio_particles.remove(particle)

    def update_ecg(self, dt: float):
        """Update ECG waveform simulation"""
        self.ecg_timer += dt
        self.heart_beat_phase += dt * 1.2  # Heart rate ~72 BPM

        # Generate ECG-style waveform
        if len(self.ecg_data) > 200:
            self.ecg_data.pop(0)

        # Simplified ECG pattern (P-QRS-T wave simulation)
        t = self.heart_beat_phase % 1.0

        if 0.0 <= t < 0.1:  # P wave
            value = math.sin(t * 20 * math.pi) * 0.2
        elif 0.15 <= t < 0.25:  # QRS complex
            value = math.sin((t - 0.15) * 40 * math.pi) * 1.5
        elif 0.3 <= t < 0.5:  # T wave
            value = math.sin((t - 0.3) * 10 * math.pi) * 0.4
        else:  # Baseline
            value = 0.0

        # Add slight noise for realism
        value += (random.random() - 0.5) * 0.05
        self.ecg_data.append(value)

    def render(self):
        """Render clinical monitoring interface"""
        # Background
        self.screen.fill(self.theme.BG_DEEP)

        # Render ambient particles
        self.render_bio_particles()

        # Header
        self.draw_header(f"CLINICAL MONITORING - {self.overall_status}", f"Wellness Score: {self.wellness_score}%")

        # Render based on current view mode
        if self.view_mode == "DASHBOARD":
            self.render_dashboard_view()
        elif self.view_mode == "BODY":
            self.render_body_view()
        elif self.view_mode == "MIND":
            self.render_mind_view()
        elif self.view_mode == "SPIRIT":
            self.render_spirit_view()

        # Scrolling ticker at bottom
        self.render_scrolling_ticker()

        # Footer with navigation (minimal)
        controls = "ESC: Exit  │  B: Body  │  M: Mind  │  S: Spirit  │  C: Caregiver"
        self.draw_footer(controls)

    def render_dashboard_view(self):
        """Render main dashboard - VISUAL, MINIMAL TEXT"""
        y_start = 200

        # Large vital signs (2x2 grid) - BIG NUMBERS, VISUAL INDICATORS
        vital_positions = [
            (240, y_start + 100),      # Heart Rate (top left)
            (960, y_start + 100),      # Blood Pressure (top right)
            (240, y_start + 400),      # Oxygen (bottom left)
            (960, y_start + 400),      # Temperature (bottom right)
        ]

        for vital, (x, y) in zip(self.vital_signs, vital_positions):
            self.render_vital_sign_card(vital, x, y)

        # ECG waveform display (center, between vitals)
        self.render_ecg_display(self.width // 2, y_start + 250, 800, 150)

        # Body/Mind/Spirit indicators (small, top right)
        self.render_wellness_indicators(self.width - 300, y_start - 50)

    def render_vital_sign_card(self, vital: VitalSign, x: int, y: int):
        """Render single vital sign with visual indicator - MINIMAL TEXT"""
        card_width = 400
        card_height = 240

        # Card background
        bg_surf = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 60))
        self.screen.blit(bg_surf, (x, y))

        # Alert border if needed
        border_color = self.theme.STATUS_ERROR if vital.alert else vital.color
        pygame.draw.rect(self.screen, border_color, (x, y, card_width, card_height), 3)

        # Vital name (small)
        self.ui.draw_text_with_shadow(
            self.screen, vital.name, self.font_small,
            (x + 20, y + 20), self.theme.TEXT_DIM, 2, False
        )

        # BIG VALUE (main focus)
        value_str = f"{int(vital.current_value)}"
        self.ui.draw_text_with_shadow(
            self.screen, value_str, self.font_huge,
            (x + card_width // 2, y + 100), vital.color, 4, True
        )

        # Unit (small, next to value)
        self.ui.draw_text_with_shadow(
            self.screen, vital.unit, self.font_normal,
            (x + card_width // 2 + 80, y + 100), self.theme.TEXT_DIM, 2, False
        )

        # Breathing circle indicator (visual status)
        pulse = self.anim.breathe(self.time, 2.0)
        circle_radius = int(15 + 8 * pulse)
        status_color = self.theme.STATUS_ERROR if vital.alert else self.theme.STATUS_OK

        self.ui.draw_breathing_circle(
            self.screen, (x + card_width - 40, y + 40),
            circle_radius, status_color, self.time
        )

        # Mini sparkline (history graph)
        self.render_sparkline(vital.history, x + 20, y + 160, card_width - 40, 60, vital.color)

    def render_sparkline(self, data: List[float], x: int, y: int, width: int, height: int, color: Tuple[int, int, int]):
        """Render small sparkline graph"""
        if len(data) < 2:
            return

        # Normalize data
        min_val = min(data)
        max_val = max(data)
        value_range = max_val - min_val if max_val > min_val else 1.0

        # Draw line graph
        points = []
        for i, value in enumerate(data):
            px = x + (i / len(data)) * width
            normalized = (value - min_val) / value_range
            py = y + height - (normalized * height)
            points.append((int(px), int(py)))

        if len(points) > 1:
            pygame.draw.lines(self.screen, color, False, points, 2)

    def render_ecg_display(self, center_x: int, center_y: int, width: int, height: int):
        """Render ECG-style waveform - VISUAL, NO TEXT"""
        x = center_x - width // 2
        y = center_y - height // 2

        # Background
        bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 40))
        self.screen.blit(bg_surf, (x, y))
        pygame.draw.rect(self.screen, (255, 100, 120), (x, y, width, height), 2)

        # ECG label (minimal)
        self.ui.draw_text_with_shadow(
            self.screen, "ECG", self.font_small,
            (x + 20, y + 20), (255, 100, 120), 2, False
        )

        # Draw ECG waveform
        if len(self.ecg_data) > 1:
            points = []
            for i, value in enumerate(self.ecg_data):
                px = x + 20 + (i / len(self.ecg_data)) * (width - 40)
                py = center_y - (value * 50)  # Scale for visibility
                points.append((int(px), int(py)))

            # Draw waveform with glow effect
            for offset in range(3, 0, -1):
                alpha = 80 // offset
                glow_color = (*self.vital_signs[0].color, alpha)
                if offset == 1:
                    pygame.draw.lines(self.screen, self.vital_signs[0].color, False, points, 3)
                else:
                    # Glow effect (simplified)
                    pass

            pygame.draw.lines(self.screen, self.vital_signs[0].color, False, points, 2)

    def render_wellness_indicators(self, x: int, y: int):
        """Render Body/Mind/Spirit indicators - SMALL, VISUAL"""
        indicators = [
            ("B", "BODY", self.body_score, (100, 200, 255)),
            ("M", "MIND", self.mind_score, (200, 100, 255)),
            ("S", "SPIRIT", self.spirit_score, (255, 150, 100)),
        ]

        for i, (key, name, score, color) in enumerate(indicators):
            ind_y = y + i * 60

            # Key indicator
            self.ui.draw_text_with_shadow(
                self.screen, f"[{key}]", self.font_small,
                (x, ind_y), color, 2, False
            )

            # Score bar (visual)
            bar_x = x + 60
            bar_width = 150
            bar_height = 20

            # Background bar
            pygame.draw.rect(self.screen, self.theme.BG_MID, (bar_x, ind_y - 10, bar_width, bar_height))

            # Filled bar (score percentage)
            fill_width = int((score / 100) * bar_width)
            pygame.draw.rect(self.screen, color, (bar_x, ind_y - 10, fill_width, bar_height))

            # Border
            pygame.draw.rect(self.screen, color, (bar_x, ind_y - 10, bar_width, bar_height), 2)

            # Score number
            self.ui.draw_text_with_shadow(
                self.screen, f"{score}", self.font_small,
                (bar_x + bar_width + 30, ind_y), color, 2, False
            )

    def render_body_view(self):
        """Render BODY subcategory - VISUAL, MINIMAL TEXT"""
        y_start = 280

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "BODY WELLNESS", self.font_large,
            (self.width // 2, y_start), (100, 200, 255), 3, True
        )

        # Visual activity tracker
        self.render_activity_circle(300, y_start + 150, 120)

        # Visual water intake
        self.render_water_tracker(900, y_start + 150)

        # Visual sleep quality
        self.render_sleep_quality(self.width // 2, y_start + 450)

    def render_mind_view(self):
        """Render MIND subcategory - VISUAL, MINIMAL TEXT"""
        y_start = 280

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "MIND WELLNESS", self.font_large,
            (self.width // 2, y_start), (200, 100, 255), 3, True
        )

        # Visual stress meter
        self.render_stress_meter(self.width // 2, y_start + 200)

        # Breathing exercise indicator
        self.render_breathing_indicator(self.width // 2, y_start + 450)

    def render_spirit_view(self):
        """Render SPIRIT subcategory - VISUAL, MINIMAL TEXT"""
        y_start = 280

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "SPIRIT WELLNESS", self.font_large,
            (self.width // 2, y_start), (255, 150, 100), 3, True
        )

        # Visual connection meter
        self.render_connection_meter(self.width // 2, y_start + 200)

        # Purpose indicator
        self.render_purpose_indicator(self.width // 2, y_start + 450)

    def render_activity_circle(self, x: int, y: int, radius: int):
        """Visual activity tracker - circular progress"""
        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "ACTIVITY", self.font_medium,
            (x, y - radius - 40), (100, 200, 255), 2, True
        )

        # Progress circle (20/30 minutes)
        progress = 20 / 30  # Demo value
        self.render_progress_circle(x, y, radius, progress, (100, 200, 255))

        # Center text
        self.ui.draw_text_with_shadow(
            self.screen, "20", self.font_huge,
            (x, y), (100, 200, 255), 4, True
        )
        self.ui.draw_text_with_shadow(
            self.screen, "min", self.font_small,
            (x, y + 50), self.theme.TEXT_DIM, 2, True
        )

    def render_water_tracker(self, x: int, y: int):
        """Visual water intake tracker"""
        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "HYDRATION", self.font_medium,
            (x, y - 60), (100, 200, 255), 2, True
        )

        # Visual glasses (6/8)
        glasses_completed = 6
        glasses_goal = 8

        for i in range(glasses_goal):
            glass_x = x - 200 + (i * 50)
            glass_y = y
            filled = i < glasses_completed

            color = (100, 200, 255) if filled else self.theme.TEXT_DIM
            glass_rect = pygame.Rect(glass_x, glass_y, 35, 50)

            if filled:
                pygame.draw.rect(self.screen, color, glass_rect)
            else:
                pygame.draw.rect(self.screen, color, glass_rect, 2)

    def render_sleep_quality(self, x: int, y: int):
        """Visual sleep quality indicator"""
        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "SLEEP", self.font_medium,
            (x, y - 40), (200, 150, 255), 2, True
        )

        # Sleep hours bar
        sleep_hours = 7.5
        self.ui.draw_text_with_shadow(
            self.screen, f"{sleep_hours} hrs", self.font_large,
            (x, y + 30), (200, 150, 255), 3, True
        )

    def render_stress_meter(self, x: int, y: int):
        """Visual stress level meter"""
        stress_level = 3  # 1-10 scale

        # Meter (visual bar)
        bar_width = 600
        bar_height = 60
        bar_x = x - bar_width // 2

        # Background
        pygame.draw.rect(self.screen, self.theme.BG_MID, (bar_x, y, bar_width, bar_height))

        # Fill based on stress
        fill_width = int((stress_level / 10) * bar_width)
        stress_color = (100, 255, 100) if stress_level < 4 else (255, 200, 100) if stress_level < 7 else (255, 100, 100)
        pygame.draw.rect(self.screen, stress_color, (bar_x, y, fill_width, bar_height))

        # Border
        pygame.draw.rect(self.screen, stress_color, (bar_x, y, bar_width, bar_height), 3)

        # Value
        self.ui.draw_text_with_shadow(
            self.screen, f"STRESS: {stress_level}/10", self.font_large,
            (x, y - 60), stress_color, 3, True
        )

    def render_breathing_indicator(self, x: int, y: int):
        """Visual breathing exercise indicator"""
        pulse = self.anim.breathe(self.time, 3.0)
        radius = int(80 + 40 * pulse)

        self.ui.draw_breathing_circle(self.screen, (x, y), radius, (200, 100, 255), self.time)

        self.ui.draw_text_with_shadow(
            self.screen, "BREATHE", self.font_medium,
            (x, y + 150), (200, 100, 255), 2, True
        )

    def render_connection_meter(self, x: int, y: int):
        """Visual social connection meter"""
        connection_score = 92

        # Circular progress
        radius = 100
        self.render_progress_circle(x, y, radius, connection_score / 100, (255, 150, 100))

        # Center value
        self.ui.draw_text_with_shadow(
            self.screen, f"{connection_score}", self.font_huge,
            (x, y), (255, 150, 100), 4, True
        )

    def render_purpose_indicator(self, x: int, y: int):
        """Visual purpose/gratitude indicator"""
        self.ui.draw_text_with_shadow(
            self.screen, "GRATITUDE STREAK", self.font_medium,
            (x, y - 40), (255, 200, 150), 2, True
        )

        self.ui.draw_text_with_shadow(
            self.screen, "18 days", self.font_huge,
            (x, y + 30), (255, 200, 150), 4, True
        )

    def render_progress_circle(self, x: int, y: int, radius: int, progress: float, color: Tuple[int, int, int]):
        """Render circular progress indicator"""
        # Background circle
        pygame.draw.circle(self.screen, self.theme.BG_MID, (x, y), radius, 8)

        # Progress arc
        if progress > 0:
            start_angle = -math.pi / 2
            end_angle = start_angle + (2 * math.pi * progress)

            # Draw arc segments
            segments = int(progress * 60)
            for i in range(segments):
                angle = start_angle + (i / 60) * 2 * math.pi
                next_angle = start_angle + ((i + 1) / 60) * 2 * math.pi

                start_pos = (x + int(radius * math.cos(angle)), y + int(radius * math.sin(angle)))
                end_pos = (x + int(radius * math.cos(next_angle)), y + int(radius * math.sin(next_angle)))

                pygame.draw.line(self.screen, color, start_pos, end_pos, 8)

    def render_scrolling_ticker(self):
        """Render scrolling ticker at bottom - NON-CRITICAL INFO"""
        ticker_y = self.height - 120
        ticker_height = 50

        # Background
        bg_surf = pygame.Surface((self.width, ticker_height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 100))
        self.screen.blit(bg_surf, (0, ticker_y))

        # Render scrolling messages
        for message, pos_x in self.ticker.get_visible_messages():
            if 0 <= pos_x < self.width:
                self.ui.draw_text_with_shadow(
                    self.screen, message, self.font_small,
                    (int(pos_x), ticker_y + 25), self.theme.TEXT_NORMAL, 2, False
                )

    def render_bio_particles(self):
        """Render ambient biometric particles"""
        for particle in self.bio_particles:
            if particle['life'] > 0:
                alpha = int(particle['life'] * 60)
                color = (*self.realm_color, alpha)
                size = int(particle['size'] * (particle['life'] + 0.5))
                s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, color, (size, size), size)
                self.screen.blit(s, (int(particle['x']) - size, int(particle['y']) - size))

    def spawn_bio_particle(self):
        """Spawn ambient biometric particle"""
        self.bio_particles.append({
            'x': random.randint(0, self.width),
            'y': random.randint(200, self.height - 200),
            'vx': random.uniform(-20, 20),
            'vy': random.uniform(-20, 20),
            'life': 1.0,
            'size': random.randint(2, 6),
        })

    def handle_key(self, key: int):
        """Handle realm-specific controls"""
        if key == pygame.K_b:
            self.view_mode = "BODY"
            print("   Switching to BODY view")
        elif key == pygame.K_m:
            self.view_mode = "MIND"
            print("   Switching to MIND view")
        elif key == pygame.K_s:
            self.view_mode = "SPIRIT"
            print("   Switching to SPIRIT view")
        elif key == pygame.K_d:
            self.view_mode = "DASHBOARD"
            print("   Switching to DASHBOARD view")
        elif key == pygame.K_c:
            # Caregiver notification
            print("   🔔 CAREGIVER NOTIFICATION SENT")
            print(f"      Contacting: {self.caregiver_contact}")
            print("      Message: User requested assistance")


def main():
    """Run Clinical & Health Monitoring Realm standalone"""
    realm = ClinicalHealthPro()
    realm.run()


if __name__ == "__main__":
    main()
