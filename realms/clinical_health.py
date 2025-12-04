"""
MotiBeam Spatial OS - Clinical & Health Realm
⚕️ Realm #2 - Professional healthcare monitoring and biometric visualization

Features:
- Real-time vital signs monitoring (heart rate, BP, oxygen, temperature)
- Breathing biometric visualization with ECG-style waveforms
- Medical alert system with priority levels
- Patient health metrics dashboard
- Professional medical color scheme with breathing animations
- Cinema-quality ambient health monitoring
"""

import pygame
import random
import math
import sys
from typing import List, Tuple

sys.path.insert(0, '/home/user/motibeam-spatial-os')

from realms.base_realm import BaseRealm


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


class ECGWaveform:
    """Simulated ECG waveform generator"""

    def __init__(self):
        self.phase = 0.0
        self.heart_rate = 72  # BPM
        self.points: List[float] = []

    def update(self, dt: float):
        """Generate ECG waveform points"""
        beats_per_second = self.heart_rate / 60.0
        phase_speed = beats_per_second * math.pi * 2

        self.phase += phase_speed * dt

        # Simplified ECG pattern (P-QRS-T waves)
        t = self.phase % (math.pi * 2)

        if t < 0.3:  # P wave
            value = math.sin(t / 0.3 * math.pi) * 0.2
        elif 0.5 < t < 0.9:  # QRS complex
            sub_t = (t - 0.5) / 0.4
            if sub_t < 0.2:
                value = -sub_t * 2  # Q
            elif sub_t < 0.5:
                value = (sub_t - 0.2) * 8 - 0.4  # R
            else:
                value = (1 - (sub_t - 0.5) / 0.5) * 2 - 0.5  # S
        elif 1.2 < t < 1.8:  # T wave
            value = math.sin((t - 1.2) / 0.6 * math.pi) * 0.3
        else:
            value = 0

        self.points.append(value)
        if len(self.points) > 300:
            self.points.pop(0)


class MedicalAlert:
    """Medical alert notification"""

    def __init__(self, title: str, message: str, priority: str, color: Tuple[int, int, int]):
        self.title = title
        self.message = message
        self.priority = priority  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
        self.color = color
        self.age = 0.0
        self.acknowledged = False

    def update(self, dt: float):
        """Update alert age"""
        self.age += dt


class ClinicalHealthPro(BaseRealm):
    """Clinical & Health Realm - Professional healthcare monitoring"""

    def __init__(self):
        super().__init__(
            realm_id=2,
            realm_name="CLINICAL & HEALTH",
            realm_color=(80, 255, 120)
        )

        # Initialize vital signs
        self.vital_signs = [
            VitalSign("HEART RATE", 72, "BPM", 45, 100, 8, (255, 100, 120)),
            VitalSign("BLOOD PRESSURE", 120, "mmHg", 90, 140, 5, (100, 200, 255)),
            VitalSign("OXYGEN SAT", 98, "%", 88, 100, 2, (100, 255, 150)),
            VitalSign("TEMPERATURE", 98.6, "°F", 97.0, 99.5, 0.5, (255, 200, 100)),
        ]

        # ECG waveform
        self.ecg = ECGWaveform()
        self.ecg.heart_rate = self.vital_signs[0].current_value

        # Medical alerts
        self.alerts: List[MedicalAlert] = []
        self.alert_timer = 0.0

        # Biometric visualization
        self.bio_particles: List[dict] = []
        self.particle_timer = 0.0

        # Patient info (simulated)
        self.patient_name = "PATIENT 7429"
        self.patient_status = "STABLE"

        print("🩺 Clinical & Health Realm initialized")

    def update(self, dt: float):
        """Update clinical monitoring system"""
        # Update vital signs
        for vital in self.vital_signs:
            vital.update(dt)

        # Sync ECG with heart rate
        self.ecg.heart_rate = self.vital_signs[0].current_value
        self.ecg.update(dt)

        # Generate alerts occasionally
        self.alert_timer += dt
        if self.alert_timer > 15.0:  # Every 15 seconds
            self.alert_timer = 0.0
            if random.random() < 0.3:  # 30% chance
                self.generate_random_alert()

        # Update alerts
        for alert in self.alerts[:]:
            alert.update(dt)
            if alert.age > 30.0:  # Remove after 30 seconds
                self.alerts.remove(alert)

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

    def render(self):
        """Render clinical monitoring interface"""
        # Background
        self.screen.fill(self.theme.BG_DEEP)

        # Render biometric particles (ambient background)
        self.render_bio_particles()

        # Header
        self.draw_header("CLINICAL & HEALTH MONITORING", f"Patient: {self.patient_name}")

        # Main content area
        content_y = 280
        content_height = self.height - content_y - 100

        # Left side: Vital signs grid (4 panels)
        self.render_vital_signs_grid(60, content_y, 900, content_height)

        # Center: ECG waveform
        self.render_ecg_waveform(1000, content_y, 800, 400)

        # Right: Medical alerts
        self.render_medical_alerts(1000, content_y + 450, 800, content_height - 450)

        # Footer
        self.draw_footer("ESC: Exit  │  SPACE: Acknowledge Alerts  │  R: Reset Vitals")

        # Status indicator
        self.render_status_indicator()

    def render_vital_signs_grid(self, x: int, y: int, width: int, height: int):
        """Render 2x2 grid of vital sign panels"""
        panel_width = (width - 30) // 2
        panel_height = (height - 30) // 2

        positions = [
            (x, y),  # Top-left
            (x + panel_width + 30, y),  # Top-right
            (x, y + panel_height + 30),  # Bottom-left
            (x + panel_width + 30, y + panel_height + 30),  # Bottom-right
        ]

        for i, vital in enumerate(self.vital_signs):
            px, py = positions[i]
            rect = pygame.Rect(px, py, panel_width, panel_height)

            # Draw panel with alert flash
            color = vital.color
            if vital.alert:
                flash = (math.sin(self.time * 8) + 1) / 2
                color = tuple(min(255, int(c * (0.5 + flash * 0.5))) for c in color)

            # Panel background
            pulse = self.anim.pulse(self.time + i * 0.5, 1.5)
            alpha = int(40 * pulse)
            bg_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            bg_surf.fill((*self.theme.BG_MID, alpha))
            self.screen.blit(bg_surf, (px, py))

            # Border
            border_width = 4 if vital.alert else 2
            pygame.draw.rect(self.screen, color, rect, border_width)

            # Title
            self.ui.draw_text_with_shadow(
                self.screen, vital.name, self.font_normal,
                (rect.centerx, py + 40), self.theme.TEXT_DIM, 2, True
            )

            # Value
            value_text = f"{int(vital.current_value)}"
            self.ui.draw_text_with_shadow(
                self.screen, value_text, self.font_huge,
                (rect.centerx, rect.centery), color, 4, True
            )

            # Unit
            self.ui.draw_text_with_shadow(
                self.screen, vital.unit, self.font_medium,
                (rect.centerx, py + panel_height - 50), self.theme.TEXT_DIM, 2, True
            )

            # Mini trend graph
            self.render_mini_trend(vital, px + 20, py + panel_height - 120, panel_width - 40, 60)

    def render_mini_trend(self, vital: VitalSign, x: int, y: int, width: int, height: int):
        """Render mini trend graph for vital sign"""
        if len(vital.history) < 2:
            return

        # Normalize history to graph bounds
        min_val = min(vital.history)
        max_val = max(vital.history)
        value_range = max_val - min_val if max_val != min_val else 1

        points = []
        for i, value in enumerate(vital.history):
            px = x + int((i / len(vital.history)) * width)
            normalized = (value - min_val) / value_range
            py = y + height - int(normalized * height)
            points.append((px, py))

        # Draw trend line with glow
        if len(points) > 1:
            self.ui.draw_glowing_line(self.screen, points[0], points[0], vital.color, 1, 0)
            for i in range(1, len(points)):
                pygame.draw.line(self.screen, vital.color, points[i - 1], points[i], 2)

    def render_ecg_waveform(self, x: int, y: int, width: int, height: int):
        """Render ECG waveform visualization"""
        # Panel background
        rect = pygame.Rect(x, y, width, height)
        pulse = self.anim.pulse(self.time, 1.5)
        alpha = int(35 * pulse)
        bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, alpha))
        self.screen.blit(bg_surf, (x, y))

        # Border
        pygame.draw.rect(self.screen, (255, 100, 120), rect, 2)

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "ELECTROCARDIOGRAM (ECG)", self.font_medium,
            (rect.centerx, y + 40), self.theme.TEXT_DIM, 2, True
        )

        # Grid lines (medical chart style)
        grid_color = (40, 60, 80)
        for i in range(0, width, 40):
            pygame.draw.line(self.screen, grid_color, (x + i, y + 80), (x + i, y + height - 20), 1)
        for i in range(80, height - 20, 40):
            pygame.draw.line(self.screen, grid_color, (x, y + i), (x + width, y + i), 1)

        # Waveform
        if len(self.ecg.points) > 1:
            waveform_y = y + height // 2
            scale = 100

            points = []
            for i, value in enumerate(self.ecg.points):
                px = x + width - (len(self.ecg.points) - i) * (width // len(self.ecg.points))
                py = waveform_y - int(value * scale)
                points.append((px, py))

            # Draw waveform with glow
            for i in range(1, len(points)):
                self.ui.draw_glowing_line(self.screen, points[i - 1], points[i], (100, 255, 120), 3, 2)

        # Heart rate display
        hr_text = f"{int(self.ecg.heart_rate)} BPM"
        self.ui.draw_text_with_shadow(
            self.screen, hr_text, self.font_large,
            (rect.centerx, y + height - 80), (255, 100, 120), 3, True
        )

    def render_medical_alerts(self, x: int, y: int, width: int, height: int):
        """Render medical alerts panel"""
        # Panel background
        rect = pygame.Rect(x, y, width, height)
        bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 35))
        self.screen.blit(bg_surf, (x, y))

        # Border
        pygame.draw.rect(self.screen, self.theme.ACCENT_PRIMARY, rect, 2)

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "MEDICAL ALERTS", self.font_medium,
            (rect.centerx, y + 30), self.theme.TEXT_DIM, 2, True
        )

        # Alerts
        if not self.alerts:
            no_alert_text = "✓ NO ACTIVE ALERTS"
            self.ui.draw_text_with_shadow(
                self.screen, no_alert_text, self.font_normal,
                (rect.centerx, rect.centery), self.theme.STATUS_SUCCESS, 2, True
            )
        else:
            alert_y = y + 80
            for alert in self.alerts[:3]:  # Show max 3 alerts
                # Alert background with pulse
                pulse = (math.sin(self.time * 4 + alert.age) + 1) / 2
                alert_rect = pygame.Rect(x + 20, alert_y, width - 40, 80)
                alpha = int(50 + pulse * 30)
                alert_bg = pygame.Surface((width - 40, 80), pygame.SRCALPHA)
                alert_bg.fill((*alert.color, alpha))
                self.screen.blit(alert_bg, (x + 20, alert_y))

                # Alert border
                pygame.draw.rect(self.screen, alert.color, alert_rect, 2)

                # Alert text
                self.ui.draw_text_with_shadow(
                    self.screen, f"[{alert.priority}] {alert.title}", self.font_normal,
                    (x + 40, alert_y + 20), alert.color, 2, False
                )

                self.ui.draw_text_with_shadow(
                    self.screen, alert.message, self.font_small,
                    (x + 40, alert_y + 55), self.theme.TEXT_DIM, 2, False
                )

                alert_y += 100

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

    def render_status_indicator(self):
        """Render patient status indicator in top-right"""
        status_x = self.width - 300
        status_y = 100

        # Status color
        if self.patient_status == "STABLE":
            status_color = self.theme.STATUS_SUCCESS
        elif self.patient_status == "MONITORING":
            status_color = self.theme.STATUS_WARNING
        else:
            status_color = self.theme.STATUS_ERROR

        # Pulsing circle
        self.ui.draw_breathing_circle(self.screen, (status_x, status_y), 20, status_color, self.time)

        # Status text
        self.ui.draw_text_with_shadow(
            self.screen, self.patient_status, self.font_medium,
            (status_x + 40, status_y), status_color, 2, False
        )

    def spawn_bio_particle(self):
        """Spawn ambient biometric particle"""
        self.bio_particles.append({
            'x': random.randint(0, self.width),
            'y': random.randint(280, self.height - 100),
            'vx': random.uniform(-20, 20),
            'vy': random.uniform(-20, 20),
            'life': 1.0,
            'size': random.randint(2, 6),
        })

    def generate_random_alert(self):
        """Generate a random medical alert"""
        alert_types = [
            ("Vitals Check", "Routine vital signs within normal range", "LOW", self.theme.STATUS_INFO),
            ("Medication Due", "Next medication scheduled in 15 minutes", "MEDIUM", self.theme.STATUS_WARNING),
            ("Elevated Heart Rate", "Heart rate slightly elevated, monitoring", "MEDIUM", self.theme.STATUS_WARNING),
            ("Lab Results Ready", "Recent lab work available for review", "LOW", self.theme.STATUS_INFO),
        ]

        alert_data = random.choice(alert_types)
        alert = MedicalAlert(*alert_data)
        self.alerts.append(alert)

    def handle_key(self, key: int):
        """Handle realm-specific controls"""
        if key == pygame.K_SPACE:
            # Acknowledge all alerts
            self.alerts.clear()
        elif key == pygame.K_r:
            # Reset vitals to baseline
            for vital in self.vital_signs:
                vital.current_value = vital.base_value
                vital.trend = 0.0


def main():
    """Run Clinical & Health Realm standalone"""
    realm = ClinicalHealthPro()
    realm.run()


if __name__ == "__main__":
    main()
