# scenes/clinical_realm.py
#
# MotiBeam Spatial OS - Clinical Realm v2
# Distinctive medical HUD with wellness gauge, vitals blocks,
# medication timeline, and ECG-style alert animation.
#
# API matches other realms:
#   ClinicalRealm(screen, clock, global_state, standalone=False)
#   .initialize()
#   .run(duration=None)

import math
import pygame
from datetime import datetime


class ClinicalRealm:
    def __init__(self, screen, clock, global_state, standalone=False):
        self.screen = screen
        self.clock = clock
        self.global_state = global_state
        self.standalone = standalone

        # Runtime state
        self.running = False
        self.current_view = 0  # 0–3
        self.event_active = False
        self.event_start_time = 0

        # Static demo data (can later be wired to real sensors)
        self.wellness_score = 87
        self.vitals = {
            "Heart Rate": ("68 bpm", "green"),
            "Blood Pressure": ("118/76", "green"),
            "SpO₂": ("98%", "green"),
            "Sleep Score": ("87/100", "yellow"),
        }
        self.med_schedule = [
            ("8:00 PM Tonight", "Blood pressure med", "yellow"),
            ("8:00 AM Tomorrow", "Vitamin D", "green"),
            ("12:00 PM Tomorrow", "Lunch supplement", "green"),
            ("8:00 PM Tomorrow", "Blood pressure med", "yellow"),
        ]

        # Fonts & colors are created in initialize()
        self.font_title = None
        self.font_subtitle = None
        self.font_label = None
        self.font_body = None
        self.font_small = None

        self.bg_color = (3, 10, 40)
        self.text_main = (230, 255, 255)
        self.text_soft = (180, 210, 230)
        self.accent_cyan = (0, 255, 200)
        self.accent_yellow = (255, 220, 120)
        self.accent_red = (255, 80, 80)
        self.accent_green = (140, 255, 140)

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    def initialize(self):
        pygame.font.init()

        # Use default system fonts – more reliable on Pi
        self.font_title = pygame.font.SysFont("DejaVu Sans", 48, bold=True)
        self.font_subtitle = pygame.font.SysFont("DejaVu Sans", 24)
        self.font_label = pygame.font.SysFont("DejaVu Sans", 26, bold=True)
        self.font_body = pygame.font.SysFont("DejaVu Sans", 22)
        self.font_small = pygame.font.SysFont("DejaVu Sans", 18)

        # Try to load emoji font just for the header icon (if present)
        self.emoji_font = None
        try:
            self.emoji_font = pygame.font.Font(
                "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 56
            )
            print("✓ ClinicalRealm: Emoji font loaded")
        except Exception:
            self.emoji_font = None
            print("⚠ ClinicalRealm: Emoji font not found, using text only")

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self, duration=None):
        """Run the Clinical Realm. duration in seconds (optional)."""
        self.initialize()
        self.running = True

        start_ticks = pygame.time.get_ticks()
        if duration is not None:
            max_ms = duration * 1000
        else:
            max_ms = None

        while self.running:
            dt = self.clock.tick(60) / 1000.0  # seconds
            now_ms = pygame.time.get_ticks()

            # Optional timeout (used when auto-cycling demo)
            if max_ms is not None and (now_ms - start_ticks) >= max_ms:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Return to launcher
                        self.running = False
                        break
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.current_view = (self.current_view + 1) % 4
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.current_view = (self.current_view - 1) % 4
                    elif event.key == pygame.K_SPACE:
                        # Trigger clinical alert event
                        self.trigger_event()

            self.draw_frame(now_ms)
            pygame.display.flip()

        # If running standalone, make sure we exit cleanly
        if self.standalone:
            pygame.quit()

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------
    def get_mode_brightness(self):
        """Return brightness multiplier based on global mode."""
        mode = getattr(self.global_state, "mode", "NORMAL")
        if mode == "NORMAL":
            return 1.0
        if mode == "STUDY":
            return 0.75
        if mode == "SLEEP":
            return 0.5
        return 1.0

    def apply_brightness(self, color, brightness):
        r, g, b = color
        return (
            max(0, min(255, int(r * brightness))),
            max(0, min(255, int(g * brightness))),
            max(0, min(255, int(b * brightness))),
        )

    def draw_background(self, surface, now_ms):
        w, h = surface.get_size()
        surface.fill(self.bg_color)

        # Soft breathing circles inspired by medical imaging
        t = (now_ms % 4000) / 4000.0  # 4s loop
        phase = math.sin(2 * math.pi * t) * 0.5 + 0.5  # 0–1

        base_alpha = 40 + int(40 * phase)
        circle_color = (0, 180, 220, base_alpha)

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)

        circles = [
            (int(w * 0.18), int(h * 0.7), int(h * 0.35)),
            (int(w * 0.8), int(h * 0.3), int(h * 0.30)),
            (int(w * 0.55), int(h * 0.8), int(h * 0.22)),
        ]
        for cx, cy, radius in circles:
            pygame.draw.circle(overlay, circle_color, (cx, cy), radius, width=2)

        surface.blit(overlay, (0, 0))

    def draw_header(self, surface):
        w, _ = surface.get_size()

        # Emoji icon left (if available)
        icon_offset_x = 32
        icon_y = 32
        if self.emoji_font is not None:
            icon_surface = self.emoji_font.render("⚕️", True, self.text_main)
            surface.blit(icon_surface, (icon_offset_x, icon_y))
            text_x = icon_offset_x + icon_surface.get_width() + 16
        else:
            text_x = icon_offset_x

        # Title
        title_surf = self.font_title.render("CLINICAL REALM", True, self.text_main)
        surface.blit(title_surf, (text_x, icon_y))

        # Subtitle line
        subtitle_text = "Health Monitoring · Wellness · Medical AI"
        subtitle_surf = self.font_subtitle.render(subtitle_text, True, self.text_soft)
        surface.blit(subtitle_surf, (text_x, icon_y + 42))

        # LIVE indicator (top-right)
        live_text = "● LIVE"
        live_color = self.accent_green
        live_surf = self.font_subtitle.render(live_text, True, live_color)
        surface.blit(live_surf, (w - live_surf.get_width() - 30, icon_y))

    def draw_footer(self, surface):
        w, h = surface.get_size()

        # Left: mode
        mode = getattr(self.global_state, "mode", "NORMAL")
        mode_label = f"Mode: {mode}"
        mode_surf = self.font_small.render(mode_label, True, self.text_soft)
        surface.blit(mode_surf, (24, h - mode_surf.get_height() - 16))

        # Center: view indicator
        center_label = f"View {self.current_view + 1}/4"
        center_surf = self.font_small.render(center_label, True, self.text_soft)
        surface.blit(
            center_surf,
            ((w - center_surf.get_width()) // 2, h - center_surf.get_height() - 16),
        )

        # Right: controls
        ctrl_label = "←/→ Views  ·  SPACE Event  ·  ESC Exit"
        ctrl_surf = self.font_small.render(ctrl_label, True, self.text_soft)
        surface.blit(
            ctrl_surf,
            (w - ctrl_surf.get_width() - 24, h - ctrl_surf.get_height() - 16),
        )

    # ------------------------------------------------------------------
    # View rendering
    # ------------------------------------------------------------------
    def draw_frame(self, now_ms):
        brightness = self.get_mode_brightness()

        self.draw_background(self.screen, now_ms)
        self.draw_header(self.screen)

        if self.current_view == 0:
            self.draw_view_vitals_and_score(self.screen, brightness, now_ms)
        elif self.current_view == 1:
            self.draw_view_medications_timeline(self.screen, brightness, now_ms)
        elif self.current_view == 2:
            self.draw_view_trends(self.screen, brightness, now_ms)
        else:
            self.draw_view_summary(self.screen, brightness, now_ms)

        # ECG alert overlay if active
        if self.event_active:
            self.draw_ecg_alert(self.screen, now_ms)

        self.draw_footer(self.screen)

    def draw_view_vitals_and_score(self, surface, brightness, now_ms):
        w, h = surface.get_size()

        # Left column: vitals
        left_x = int(w * 0.08)
        top_y = int(h * 0.25)

        title = "KEY VITALS"
        title_surf = self.font_label.render(
            title, True, self.apply_brightness(self.text_main, brightness)
        )
        surface.blit(title_surf, (left_x, top_y))

        line_y = top_y + 40
        for name, (value, status) in self.vitals.items():
            color = self.status_color(status, brightness)

            # small status circle
            pygame.draw.circle(surface, color, (left_x + 8, line_y + 10), 6)

            name_surf = self.font_body.render(
                name, True, self.apply_brightness(self.text_soft, brightness)
            )
            value_surf = self.font_body.render(
                value, True, self.apply_brightness(self.text_main, brightness)
            )

            surface.blit(name_surf, (left_x + 24, line_y))
            surface.blit(value_surf, (left_x + 260, line_y))

            line_y += 28

        # Center: radial wellness gauge
        center_x = int(w * 0.53)
        center_y = int(h * 0.55)
        radius = int(h * 0.19)

        # Arc background
        arc_rect = pygame.Rect(
            center_x - radius, center_y - radius, radius * 2, radius * 2
        )

        start_angle = math.radians(210)  # left bottom
        end_angle = math.radians(-30)    # right bottom

        bg_color = self.apply_brightness((40, 80, 120), brightness)
        pygame.draw.arc(surface, bg_color, arc_rect, start_angle, end_angle, 10)

        # Active arc based on score
        score_ratio = max(0.0, min(1.0, self.wellness_score / 100.0))
        active_end = start_angle + (end_angle - start_angle) * score_ratio
        active_color = self.status_color(self.score_status(), brightness)
        pygame.draw.arc(surface, active_color, arc_rect, start_angle, active_end, 10)

        # Moving indicator dot along arc
        indicator_angle = active_end
        dot_x = center_x + radius * math.cos(indicator_angle)
        dot_y = center_y + radius * math.sin(indicator_angle)
        pygame.draw.circle(surface, active_color, (int(dot_x), int(dot_y)), 8)

        # Score text
        score_text = str(self.wellness_score)
        score_surf = self.font_title.render(
            score_text, True, self.apply_brightness(self.text_main, brightness)
        )
        score_rect = score_surf.get_rect(center=(center_x, center_y - 10))
        surface.blit(score_surf, score_rect)

        label_surf = self.font_label.render(
            "WELLNESS SCORE",
            True,
            self.apply_brightness(self.text_soft, brightness),
        )
        label_rect = label_surf.get_rect(center=(center_x, center_y + 40))
        surface.blit(label_surf, label_rect)

        # Right: short note
        note = "Stable condition · Monitoring 24/7"
        note_surf = self.font_body.render(
            note, True, self.apply_brightness(self.text_soft, brightness)
        )
        note_rect = note_surf.get_rect(center=(center_x, center_y + 80))
        surface.blit(note_surf, note_rect)

    def draw_view_medications_timeline(self, surface, brightness, now_ms):
        w, h = surface.get_size()

        title = "MEDICATIONS SCHEDULE"
        title_surf = self.font_label.render(
            title, True, self.apply_brightness(self.text_main, brightness)
        )
        surface.blit(title_surf, (int(w * 0.08), int(h * 0.25)))

        # Vertical timeline center
        line_x = int(w * 0.27)
        top_y = int(h * 0.30)
        bottom_y = int(h * 0.78)

        # Timeline line
        line_color = self.apply_brightness((80, 140, 180), brightness)
        pygame.draw.line(surface, line_color, (line_x, top_y), (line_x, bottom_y), 2)

        # Entries along the line
        step = (bottom_y - top_y) / max(1, len(self.med_schedule) - 1)

        for idx, (time_label, med_name, status) in enumerate(self.med_schedule):
            y = int(top_y + idx * step)

            status_col = self.status_color(status, brightness)

            # Node circle
            pygame.draw.circle(surface, status_col, (line_x, y), 7)

            # Horizontal connector
            pygame.draw.line(
                surface,
                status_col,
                (line_x + 10, y),
                (line_x + 40, y),
                2,
            )

            # Text blocks
            time_surf = self.font_body.render(
                time_label, True, self.apply_brightness(self.text_soft, brightness)
            )
            med_surf = self.font_body.render(
                med_name, True, self.apply_brightness(self.text_main, brightness)
            )
            surface.blit(time_surf, (line_x + 50, y - 14))
            surface.blit(med_surf, (line_x + 50, y + 4))

        # Right side note
        right_title = "NEXT ACTION"
        right_surf = self.font_label.render(
            right_title, True, self.apply_brightness(self.text_main, brightness)
        )
        surface.blit(right_surf, (int(w * 0.60), int(h * 0.30)))

        next_text = "Next dose: 8:00 PM Tonight\nBlood pressure medication\nReminder set · Escalate if missed"
        self.draw_multiline(
            surface,
            next_text,
            self.font_body,
            self.apply_brightness(self.text_soft, brightness),
            (int(w * 0.60), int(h * 0.36)),
            line_spacing=4,
        )

    def draw_view_trends(self, surface, brightness, now_ms):
        w, h = surface.get_size()

        title = "7-DAY TRENDS"
        title_surf = self.font_label.render(
            title, True, self.apply_brightness(self.text_main, brightness)
        )
        surface.blit(title_surf, (int(w * 0.08), int(h * 0.25)))

        # Simple textual trend blocks (no charts yet – projection-friendly)
        blocks = [
            ("Heart Rate", "Resting average: 67 bpm", "Trend: Stable"),
            ("Blood Pressure", "Avg: 117/75", "Trend: Improving"),
            ("Sleep Quality", "Avg: 6.9 hours", "Trend: Slight deficit"),
        ]

        y = int(h * 0.32)
        for name, line1, line2 in blocks:
            name_surf = self.font_body.render(
                name, True, self.apply_brightness(self.text_main, brightness)
            )
            surface.blit(name_surf, (int(w * 0.08), y))

            line1_surf = self.font_small.render(
                line1, True, self.apply_brightness(self.text_soft, brightness)
            )
            line2_surf = self.font_small.render(
                line2, True, self.apply_brightness(self.text_soft, brightness)
            )
            surface.blit(line1_surf, (int(w * 0.08), y + 24))
            surface.blit(line2_surf, (int(w * 0.08), y + 44))

            y += 80

        # Right-hand "risk band"
        band_x = int(w * 0.60)
        band_y = int(h * 0.32)
        band_w = int(w * 0.28)
        band_h = int(h * 0.34)

        pygame.draw.rect(
            surface,
            self.apply_brightness((10, 40, 60), brightness),
            (band_x, band_y, band_w, band_h),
            border_radius=10,
        )

        label = "RISK BAND"
        label_surf = self.font_label.render(
            label, True, self.apply_brightness(self.text_main, brightness)
        )
        surface.blit(label_surf, (band_x + 16, band_y + 12))

        levels = [
            ("LOW", self.accent_green),
            ("MODERATE", self.accent_yellow),
            ("ELEVATED", self.accent_red),
        ]
        bar_y = band_y + 60
        bar_h = 26
        bar_gap = 10

        for level_text, col in levels:
            rect = pygame.Rect(band_x + 16, bar_y, band_w - 32, bar_h)
            pygame.draw.rect(
                surface,
                self.apply_brightness(col, brightness),
                rect,
                border_radius=6,
            )

            text_surf = self.font_small.render(
                level_text, True, (0, 0, 0)
            )
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

            bar_y += bar_h + bar_gap

        info = "Current status: LOW\nAI watchlist: Sleep & hydration"
        self.draw_multiline(
            surface,
            info,
            self.font_small,
            self.apply_brightness(self.text_soft, brightness),
            (band_x + 16, bar_y + 10),
            line_spacing=2,
        )

    def draw_view_summary(self, surface, brightness, now_ms):
        w, h = surface.get_size()

        left_x = int(w * 0.08)
        top_y = int(h * 0.25)

        title = "CLINICAL SNAPSHOT"
        title_surf = self.font_label.render(
            title, True, self.apply_brightness(self.text_main, brightness)
        )
        surface.blit(title_surf, (left_x, top_y))

        # Left column summary
        summary_text = (
            "Overall status: Stable\n"
            "Focus areas:\n"
            "  • Maintain blood pressure control\n"
            "  • Improve sleep duration\n"
            "  • Continue hydration reminders"
        )
        self.draw_multiline(
            surface,
            summary_text,
            self.font_body,
            self.apply_brightness(self.text_soft, brightness),
            (left_x, top_y + 40),
            line_spacing=4,
        )

        # Right column: next 24h care plan
        plan_x = int(w * 0.55)
        plan_title = "NEXT 24 HOURS"
        plan_surf = self.font_label.render(
            plan_title, True, self.apply_brightness(self.text_main, brightness)
        )
        surface.blit(plan_surf, (plan_x, top_y))

        plan_text = (
            "• 08:00 PM – Evening medication\n"
            "• 09:30 PM – Wind-down routine\n"
            "• 10:30 PM – Sleep target\n"
            "• Auto-alert if vitals deviate"
        )
        self.draw_multiline(
            surface,
            plan_text,
            self.font_body,
            self.apply_brightness(self.text_soft, brightness),
            (plan_x, top_y + 40),
            line_spacing=4,
        )

    # ------------------------------------------------------------------
    # ECG event overlay
    # ------------------------------------------------------------------
    def trigger_event(self):
        """SPACE key triggers a short ECG alert overlay."""
        self.event_active = True
        self.event_start_time = pygame.time.get_ticks()

    def draw_ecg_alert(self, surface, now_ms):
        elapsed = now_ms - self.event_start_time
        if elapsed > 2000:
            self.event_active = False
            return

        w, h = surface.get_size()
        band_h = 40
        y = int(h * 0.15)

        # Fade in/out alpha
        if elapsed < 200:
            alpha = int(255 * (elapsed / 200.0))
        elif elapsed > 1800:
            alpha = int(255 * ((2000 - elapsed) / 200.0))
        else:
            alpha = 255

        overlay = pygame.Surface((w, band_h), pygame.SRCALPHA)
        bg_col = (*self.accent_cyan, max(40, int(alpha * 0.25)))
        overlay.fill(bg_col)

        # Simple ECG line
        line_color = (*self.accent_cyan, alpha)
        mid_y = band_h // 2
        points = []
        segments = 40
        width = w - 60

        for i in range(segments):
            t = i / (segments - 1)
            x = 30 + int(width * t)
            # Basic pattern: flat, spike, flat
            if 0.45 < t < 0.55:
                # spike
                spike = math.sin((t - 0.45) * math.pi * 10) * 14
            else:
                spike = math.sin(t * math.pi * 2) * 3
            y_pt = mid_y + int(spike)
            points.append((x, y_pt))

        if len(points) >= 2:
            pygame.draw.lines(overlay, line_color, False, points, 2)

        # Label
        label = "Clinical alert acknowledged · Monitoring ECG pattern"
        label_surf = self.font_small.render(label, True, self.text_main)
        overlay.blit(label_surf, (30, 6))

        surface.blit(overlay, (0, y))

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def draw_multiline(
        self, surface, text, font, color, pos, line_spacing=2
    ):
        x, y = pos
        for line in text.split("\n"):
            if not line:
                y += font.get_linesize() + line_spacing
                continue
            surf = font.render(line, True, color)
            surface.blit(surf, (x, y))
            y += font.get_linesize() + line_spacing

    def status_color(self, status, brightness):
        status = status.lower()
        if status.startswith("green") or status == "ok":
            base = self.accent_green
        elif status.startswith("yellow") or "watch" in status:
            base = self.accent_yellow
        elif status.startswith("red") or "urgent" in status:
            base = self.accent_red
        else:
            base = self.accent_cyan
        return self.apply_brightness(base, brightness)

    def score_status(self):
        if self.wellness_score >= 80:
            return "green"
        if self.wellness_score >= 60:
            return "yellow"
        return "red"
