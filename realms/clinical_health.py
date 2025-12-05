"""
MotiBeam Spatial OS - Clinical & Health Realm
Visual-first health monitoring with ambient vitals display
THE SHOWCASE FEATURE
"""

import pygame
import random
import math
from realms.base_realm import BaseRealm
from core.ui.framework import (
    Theme, Fonts, draw_text_shadowed, draw_glow_rect,
    BreathingAnimation, Sparkline, ECGWaveform, ScrollingTicker,
    PulseAnimation
)


class VitalCard:
    """Individual vital sign card with animated graph"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 title: str, value: str, unit: str, color: tuple,
                 privacy_mode: bool = False):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.value = value
        self.unit = unit
        self.color = color
        self.privacy_mode = privacy_mode

        # Sparkline for trending
        self.sparkline = Sparkline(width - 60, 80, max_points=30)

        # Breathing animation
        self.breathing = BreathingAnimation(0.8, 1.0, 0.02)

    def update(self, new_value: str = None):
        """Update vital value and animation"""
        if new_value:
            self.value = new_value

        self.breathing.update()

        # Add sparkline data (simulated variation)
        baseline = 0.5
        variation = random.uniform(-0.1, 0.1)
        self.sparkline.add_value(max(0.1, min(0.9, baseline + variation)))

    def draw(self, surface: pygame.Surface, privacy_mode: bool):
        """Draw vital card"""
        # Card background with glow
        breath_val = self.breathing.get_value()
        draw_glow_rect(surface, self.rect, self.color,
                      glow_size=int(15 * breath_val),
                      alpha=Theme.ALPHA_MEDIUM)

        # Title
        title_font = Fonts.get(Fonts.MEDIUM)
        draw_text_shadowed(surface, self.title,
                         (self.rect.x + 30, self.rect.y + 30),
                         title_font, Theme.WHITE, shadow_offset=3)

        # Value (large and centered)
        if privacy_mode:
            display_value = "••••"
        else:
            display_value = self.value

        value_font = Fonts.get(Fonts.HUGE, bold=True)
        value_y = self.rect.y + 90
        draw_text_shadowed(surface, display_value,
                         (self.rect.centerx, value_y),
                         value_font, self.color, shadow_offset=4, center=True)

        # Unit
        unit_font = Fonts.get(Fonts.SMALL)
        unit_y = value_y + 90
        draw_text_shadowed(surface, self.unit,
                         (self.rect.centerx, unit_y),
                         unit_font, Theme.GRAY_LIGHT, shadow_offset=2, center=True)

        # Sparkline
        if not privacy_mode:
            sparkline_y = self.rect.y + self.rect.height - 120
            self.sparkline.draw(surface,
                              (self.rect.x + 30, sparkline_y),
                              self.color, line_width=3)


class ClinicalHealthRealm(BaseRealm):
    """Clinical & Health monitoring realm"""

    def __init__(self, display: pygame.Surface):
        super().__init__(display, "Clinical & Health")

        # Current view mode
        self.view_mode = "dashboard"  # dashboard, body, mind, spirit

        # Vital cards
        card_width = 400
        card_height = 320
        card_spacing = 60
        start_x = (self.width - (card_width * 2 + card_spacing)) // 2
        start_y = 200

        self.vitals = {
            "hr": VitalCard(start_x, start_y, card_width, card_height,
                          "HEART RATE", "72", "BPM",
                          Theme.HEALTH_HR),
            "bp": VitalCard(start_x + card_width + card_spacing, start_y,
                          card_width, card_height,
                          "BLOOD PRESSURE", "120/80", "mmHg",
                          Theme.HEALTH_BP),
            "o2": VitalCard(start_x, start_y + card_height + card_spacing,
                          card_width, card_height,
                          "OXYGEN SAT", "98", "%",
                          Theme.HEALTH_O2),
            "temp": VitalCard(start_x + card_width + card_spacing,
                            start_y + card_height + card_spacing,
                            card_width, card_height,
                            "TEMPERATURE", "98.6", "°F",
                            Theme.HEALTH_TEMP),
        }

        # ECG waveform
        self.ecg = ECGWaveform(width=1200, height=150, bpm=72)

        # Breathing animation
        self.breathing = BreathingAnimation(0.7, 1.0, 0.015)

        # Ticker
        ticker_messages = [
            "All vitals within normal range",
            "Next medication: 2:00 PM",
            "Hydration goal: 6/8 glasses",
            "Activity: 4,250 steps today",
            "Sleep quality: 7.5 hours, good",
            "Heart rate variability: Excellent"
        ]
        self.ticker = ScrollingTicker(self.width, ticker_messages, font_size=Fonts.NORMAL)

        # Body/Mind/Spirit indicators
        self.bms_scores = {
            "body": 0.85,
            "mind": 0.75,
            "spirit": 0.90
        }

        # Caregiver message
        self.show_caregiver = False
        self.caregiver_timer = 0

        # Pulse animation for alerts
        self.pulse = PulseAnimation(duration=40)

    def on_event(self, event: pygame.event.Event):
        """Handle realm-specific events"""
        if event.type == pygame.KEYDOWN:
            # View mode switching
            if event.key == pygame.K_d:
                self.view_mode = "dashboard"
            elif event.key == pygame.K_b:
                self.view_mode = "body"
            elif event.key == pygame.K_m:
                self.view_mode = "mind"
            elif event.key == pygame.K_s:
                self.view_mode = "spirit"

            # Caregiver notification
            elif event.key == pygame.K_c:
                self.show_caregiver = True
                self.caregiver_timer = 180
                self.pulse.trigger()

    def update(self):
        """Update realm state"""
        # Update vitals
        for vital in self.vitals.values():
            vital.update()

        # Update ECG
        self.ecg.update()

        # Update animations
        self.breathing.update()
        self.ticker.update()
        self.pulse.update()

        # Caregiver timer
        if self.show_caregiver:
            self.caregiver_timer -= 1
            if self.caregiver_timer <= 0:
                self.show_caregiver = False

        # Simulate vital changes (very subtle)
        if random.random() < 0.01:  # 1% chance per frame
            hr = int(self.vitals["hr"].value)
            hr = max(60, min(100, hr + random.randint(-2, 2)))
            self.vitals["hr"].value = str(hr)

            o2 = int(self.vitals["o2"].value)
            o2 = max(95, min(100, o2 + random.randint(-1, 1)))
            self.vitals["o2"].value = str(o2)

    def draw(self):
        """Draw realm"""
        # Clear
        self.display.fill(Theme.BG_DEEP)

        # Draw based on view mode
        if self.view_mode == "dashboard":
            self.draw_dashboard()
        elif self.view_mode == "body":
            self.draw_body_focus()
        elif self.view_mode == "mind":
            self.draw_mind_focus()
        elif self.view_mode == "spirit":
            self.draw_spirit_focus()

        # Draw ticker at bottom
        ticker_y = self.height - 80
        self.ticker.draw(self.display, ticker_y)

        # Draw privacy overlay
        self.draw_privacy_overlay()

        # Draw caregiver notification
        if self.show_caregiver:
            self.draw_caregiver_notification()

        # Draw help text
        self.draw_help()

    def draw_dashboard(self):
        """Draw main dashboard with all vitals"""
        # Title
        title_font = Fonts.get(Fonts.GIANT, bold=True)
        draw_text_shadowed(self.display, "CLINICAL & HEALTH",
                         (self.width // 2, 70),
                         title_font, Theme.BLUE_SOFT, shadow_offset=5, center=True)

        # ECG waveform at top
        ecg_y = 140
        self.ecg.draw(self.display,
                     ((self.width - self.ecg.width) // 2, ecg_y),
                     Theme.HEALTH_HR, line_width=3)

        # Vital cards
        for vital in self.vitals.values():
            vital.draw(self.display, self.privacy_mode)

        # Body/Mind/Spirit summary
        self.draw_bms_indicators(self.width - 250, 200)

    def draw_body_focus(self):
        """Draw Body-focused view"""
        # Title
        title_font = Fonts.get(Fonts.HUGE, bold=True)
        draw_text_shadowed(self.display, "BODY",
                         (self.width // 2, 80),
                         title_font, Theme.GREEN_SOFT, shadow_offset=5, center=True)

        # Large body score
        score = int(self.bms_scores["body"] * 100)
        score_font = Fonts.get(200, bold=True)
        draw_text_shadowed(self.display, str(score),
                         (self.width // 2, self.height // 2 - 80),
                         score_font, Theme.GREEN_SOFT, shadow_offset=8, center=True)

        # Details
        details_y = self.height // 2 + 100
        detail_font = Fonts.get(Fonts.MEDIUM)
        details = [
            "Physical wellness optimal",
            "Cardiovascular: Excellent",
            "Mobility: Full range",
            "Energy level: High"
        ]

        for i, detail in enumerate(details):
            y = details_y + (i * 60)
            draw_text_shadowed(self.display, detail,
                             (self.width // 2, y),
                             detail_font, Theme.WHITE, shadow_offset=3, center=True)

    def draw_mind_focus(self):
        """Draw Mind-focused view"""
        # Title
        title_font = Fonts.get(Fonts.HUGE, bold=True)
        draw_text_shadowed(self.display, "MIND",
                         (self.width // 2, 80),
                         title_font, Theme.BLUE_SOFT, shadow_offset=5, center=True)

        # Large mind score
        score = int(self.bms_scores["mind"] * 100)
        score_font = Fonts.get(200, bold=True)
        draw_text_shadowed(self.display, str(score),
                         (self.width // 2, self.height // 2 - 80),
                         score_font, Theme.BLUE_SOFT, shadow_offset=8, center=True)

        # Details
        details_y = self.height // 2 + 100
        detail_font = Fonts.get(Fonts.MEDIUM)
        details = [
            "Mental clarity: Good",
            "Focus level: Moderate",
            "Stress: Low",
            "Cognitive function: Normal"
        ]

        for i, detail in enumerate(details):
            y = details_y + (i * 60)
            draw_text_shadowed(self.display, detail,
                             (self.width // 2, y),
                             detail_font, Theme.WHITE, shadow_offset=3, center=True)

    def draw_spirit_focus(self):
        """Draw Spirit-focused view"""
        # Title
        title_font = Fonts.get(Fonts.HUGE, bold=True)
        draw_text_shadowed(self.display, "SPIRIT",
                         (self.width // 2, 80),
                         title_font, Theme.PURPLE_SOFT, shadow_offset=5, center=True)

        # Large spirit score
        score = int(self.bms_scores["spirit"] * 100)
        score_font = Fonts.get(200, bold=True)
        draw_text_shadowed(self.display, str(score),
                         (self.width // 2, self.height // 2 - 80),
                         score_font, Theme.PURPLE_SOFT, shadow_offset=8, center=True)

        # Details
        details_y = self.height // 2 + 100
        detail_font = Fonts.get(Fonts.MEDIUM)
        details = [
            "Emotional balance: Excellent",
            "Purpose: Strong",
            "Connection: Deep",
            "Inner peace: High"
        ]

        for i, detail in enumerate(details):
            y = details_y + (i * 60)
            draw_text_shadowed(self.display, detail,
                             (self.width // 2, y),
                             detail_font, Theme.WHITE, shadow_offset=3, center=True)

    def draw_bms_indicators(self, x: int, y: int):
        """Draw Body/Mind/Spirit indicator bars"""
        bar_width = 180
        bar_height = 40
        bar_spacing = 60

        indicators = [
            ("BODY", self.bms_scores["body"], Theme.GREEN_SOFT),
            ("MIND", self.bms_scores["mind"], Theme.BLUE_SOFT),
            ("SPIRIT", self.bms_scores["spirit"], Theme.PURPLE_SOFT)
        ]

        for i, (label, score, color) in enumerate(indicators):
            bar_y = y + (i * (bar_height + bar_spacing))

            # Label
            label_font = Fonts.get(Fonts.SMALL)
            draw_text_shadowed(self.display, label,
                             (x, bar_y - 30),
                             label_font, Theme.GRAY_LIGHT, shadow_offset=2)

            # Bar background
            bg_rect = pygame.Rect(x, bar_y, bar_width, bar_height)
            pygame.draw.rect(self.display, Theme.BG_MID, bg_rect, border_radius=8)

            # Bar fill (animated)
            breath_val = self.breathing.get_value()
            fill_width = int(bar_width * score * breath_val)
            fill_rect = pygame.Rect(x, bar_y, fill_width, bar_height)

            # Glow
            glow_surf = pygame.Surface((fill_width + 20, bar_height + 20),
                                      pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*color, Theme.ALPHA_MEDIUM),
                           (10, 10, fill_width, bar_height), border_radius=8)
            self.display.blit(glow_surf, (x - 10, bar_y - 10))

            # Fill
            pygame.draw.rect(self.display, color, fill_rect, border_radius=8)

            # Score
            score_text = f"{int(score * 100)}"
            score_font = Fonts.get(Fonts.SMALL, bold=True)
            draw_text_shadowed(self.display, score_text,
                             (x + bar_width + 20, bar_y + 10),
                             score_font, color, shadow_offset=2)

    def draw_caregiver_notification(self):
        """Draw caregiver notification"""
        font = Fonts.get(Fonts.LARGE, bold=True)
        text = "CAREGIVER NOTIFIED"

        # Pulsing effect
        pulse_intensity = self.pulse.get_intensity()
        alpha = int(Theme.ALPHA_VISIBLE + (pulse_intensity * 95))

        text_surf = font.render(text, True, Theme.GREEN_SOFT)
        text_rect = text_surf.get_rect(center=(self.width // 2, 150))

        # Background
        bg_rect = text_rect.inflate(60, 30)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (*Theme.GREEN_SOFT, alpha),
                        (0, 0, bg_rect.width, bg_rect.height), border_radius=15)
        self.display.blit(bg_surf, bg_rect)

        self.display.blit(text_surf, text_rect)

    def draw_help(self):
        """Draw control help"""
        help_font = Fonts.get(Fonts.SMALL - 4)
        help_texts = [
            "D:Dashboard  B:Body  M:Mind  S:Spirit  C:Caregiver  P:Privacy  ESC:Exit"
        ]

        help_y = 20
        for text in help_texts:
            help_surf = help_font.render(text, True, Theme.GRAY_DARK)
            help_rect = help_surf.get_rect(center=(self.width // 2, help_y))
            self.display.blit(help_surf, help_rect)
