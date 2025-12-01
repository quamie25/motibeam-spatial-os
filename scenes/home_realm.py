"""
Home Realm - Smart Home & Family HUD (Polished for Wall Display)

Enhanced with:
- Larger fonts readable from 8-10 feet
- Emojis in headers and content
- Wider layout using 50-60% screen width
- Comfortable spacing
"""

import pygame
import random
import time
from typing import List, Dict
from core.spatial_realm import SpatialRealm


class HomeRealm(SpatialRealm):
    """Smart home and family presence HUD."""

    def __init__(self, screen, theme, global_state):
        super().__init__(screen, theme, global_state)

        # Initialize custom fonts for wall readability (upgraded sizes)
        pygame.font.init()
        self.title_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 40, bold=False)
        self.body_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.label_font = pygame.font.SysFont("Arial", 30)
        self.emoji_font = pygame.font.SysFont(None, 80)

        # Sample data
        self.family_members = [
            {"name": "Quamie", "location": "home office", "emoji": "🧑‍💻"},
            {"name": "Kids", "location": "living room", "emoji": "🧒"},
        ]

        self.devices = [
            {"name": "Lights", "status": "7 active scenes", "emoji": "💡"},
            {"name": "Thermostat", "status": "72° Eco mode", "emoji": "🌡️"},
            {"name": "Speakers", "status": "idle", "emoji": "🔊"},
        ]

        self.today_items = [
            {"text": "1 package out for delivery", "emoji": "📦"},
            {"text": "2 upcoming reminders", "emoji": "⏰"},
        ]

        self.doorbell_event = None
        self.last_doorbell_time = 0

        # View emoji mapping
        self.view_emojis = ["🏠", "📹", "🎛️", "🌙"]

        # Animated breathing circles (positioned dynamically based on screen size)
        w, h = self.screen.get_width(), self.screen.get_height()
        self.circles = [
            {"x": w * 0.65, "y": h * 0.35, "base_r": 90, "r": 90, "dr": 0.25},
            {"x": w * 0.75, "y": h * 0.50, "base_r": 130, "r": 130, "dr": -0.2},
            {"x": w * 0.70, "y": h * 0.65, "base_r": 110, "r": 110, "dr": 0.18},
        ]

    @property
    def realm_name(self) -> str:
        return "HOME"

    @property
    def realm_icon(self) -> str:
        return "🏡"

    def get_views(self) -> List[Dict]:
        return [
            {"name": "Home Overview", "render": self.render_home_overview},
            {"name": "Cameras & Deliveries", "render": self.render_camera_deliveries},
            {"name": "Scenes & Routines", "render": self.render_scenes_routines},
            {"name": "Ambient Loop", "render": self.render_ambient_loop},
        ]

    def update(self):
        """Update animations - breathing circles."""
        super().update()

        # Animate circle radii (breathing effect)
        for circle in self.circles:
            circle["r"] += circle["dr"]
            # Reverse direction if we hit the limits
            if circle["r"] > circle["base_r"] + 15 or circle["r"] < circle["base_r"] - 15:
                circle["dr"] *= -1

    def on_interact(self):
        """Simulate doorbell/Ring event."""
        super().on_interact()
        self.doorbell_event = {
            "time": time.strftime("%I:%M %p"),
            "person": random.choice(["Delivery person", "Visitor", "Mail carrier"]),
            "action": random.choice(["rang doorbell", "left package", "waiting at door"]),
        }
        self.last_doorbell_time = time.time()
        print(f"  🔔 Doorbell: {self.doorbell_event['person']} {self.doorbell_event['action']}")

    def render(self):
        """Override render to add custom header and footer."""
        # Background
        bg_color = self.global_state.get_background_color()
        self.screen.fill(bg_color)

        # Background effects
        if self.global_state.should_show_animations():
            self.draw_background_effects()

        # Breathing circles
        self.draw_breathing_circles()

        # Custom header with emoji
        self.draw_custom_header()

        # Render current view
        self.render_current_view()

        # Custom footer with controls
        self.draw_custom_footer()

    def draw_custom_header(self):
        """Draw custom header with emoji and view name."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        # Main title: 🏡 HOME REALM
        title_text = "🏡 HOME REALM"
        title_surf = self.title_font.render(title_text, True, color)
        title_x = (w - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, 40))

        # Subtitle: Current view with emoji
        views = self.get_views()
        if views and self.current_view_index < len(views):
            view_emoji = self.view_emojis[self.current_view_index]
            view_name = views[self.current_view_index]["name"]
            subtitle_text = f"{view_emoji} {view_name}"

            subtitle_surf = self.subtitle_font.render(subtitle_text, True, tuple(int(c * 0.8) for c in color))
            subtitle_x = (w - subtitle_surf.get_width()) // 2
            self.screen.blit(subtitle_surf, (subtitle_x, 120))

    def draw_custom_footer(self):
        """Draw footer with control hints."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness * 0.6) for c in (200, 200, 200))

        footer_text = "← → change view  •  SPACE ring doorbell  •  ESC back"
        footer_surf = self.label_font.render(footer_text, True, color)
        footer_x = (w - footer_surf.get_width()) // 2
        footer_y = int(h * 0.92)
        self.screen.blit(footer_surf, (footer_x, footer_y))

    def draw_breathing_circles(self):
        """Draw animated breathing circles in the background."""
        if not self.global_state.should_show_animations():
            return

        brightness = self.global_state.get_brightness_multiplier()
        # Neon cyan circles with low alpha
        circle_color = tuple(int(c * brightness * 0.4) for c in (0, 200, 255))

        for circle in self.circles:
            # Draw circle with thin border
            pygame.draw.circle(
                self.screen,
                circle_color,
                (int(circle["x"]), int(circle["y"])),
                int(circle["r"]),
                3  # Border width
            )

    def render_home_overview(self):
        """View 1: Home Overview - 2-column layout with stats."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        # Left column: 35% width, text blocks
        left_margin = int(w * 0.08)
        left_col_width = int(w * 0.35)
        top = int(h * 0.25)
        line_h = 48

        y = top

        # Section: Family Presence
        section_text = "👨‍👩‍👧 Family Presence"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        for member in self.family_members:
            line = f"  {member['emoji']} {member['name']} – {member['location']}"
            line_surf = self.label_font.render(line, True, color)
            self.screen.blit(line_surf, (left_margin + 40, y))
            y += line_h

        y += 40

        # Section: Devices
        section_text = "🔌 Smart Devices"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        for device in self.devices:
            line = f"  {device['emoji']} {device['name']} – {device['status']}"
            line_surf = self.label_font.render(line, True, color)
            self.screen.blit(line_surf, (left_margin + 40, y))
            y += line_h

        y += 40

        # Section: Today
        section_text = "📅 Today's Items"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        for item in self.today_items:
            line = f"  {item['emoji']} {item['text']}"
            line_surf = self.label_font.render(line, True, color)
            self.screen.blit(line_surf, (left_margin + 40, y))
            y += line_h

        # Right column: 60% width, large stats cards
        right_col_x = int(w * 0.50)
        right_col_width = int(w * 0.42)
        right_y = top

        # Stats: Home Status
        stats = [
            {"emoji": "🏠", "label": "Rooms Active", "value": "3 of 8"},
            {"emoji": "🔒", "label": "Security", "value": "All Locked"},
            {"emoji": "📹", "label": "Cameras", "value": "2 Online"},
            {"emoji": "📦", "label": "Deliveries", "value": "1 Today"},
            {"emoji": "🌡️", "label": "Climate", "value": "72°F Eco"},
            {"emoji": "🌙", "label": "Quiet Hours", "value": "10PM–6AM"},
        ]

        for stat in stats:
            # Draw stat card
            card_height = 60
            stat_text = f"{stat['emoji']}  {stat['label']}: {stat['value']}"
            stat_surf = self.label_font.render(stat_text, True, color)
            self.screen.blit(stat_surf, (right_col_x, right_y))
            right_y += card_height + 15

        # Show doorbell event if recent
        if self.doorbell_event and (time.time() - self.last_doorbell_time < 8):
            self.draw_doorbell_overlay()

    def render_camera_deliveries(self):
        """View 2: Cameras & Deliveries - 2-column card layout."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        # Left column: Cameras
        left_margin = int(w * 0.08)
        top = int(h * 0.25)
        line_h = 50

        y = top

        # Section: Front Door Camera
        section_text = "📹 Front Door Camera"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        cam_info = [
            "  📡 Recording: ON",
            "  👁️ Last motion: 2 min ago",
            "  🌡️ Temperature: 68°F",
        ]

        for line in cam_info:
            line_surf = self.label_font.render(line, True, color)
            self.screen.blit(line_surf, (left_margin + 40, y))
            y += line_h

        y += 40

        # Section: Recent Events
        section_text = "📋 Recent Events"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        events = [
            "  📦 10:24 AM - Package delivered",
            "  👤 9:15 AM - Motion detected",
            "  🚪 8:03 AM - Mailbox opened",
        ]

        for event in events:
            event_surf = self.label_font.render(event, True, color)
            self.screen.blit(event_surf, (left_margin + 40, y))
            y += line_h

        # Right column: Deliveries
        right_col_x = int(w * 0.50)
        right_y = top

        section_text = "🚚 Deliveries Today"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (right_col_x, right_y))
        right_y += line_h + 20

        deliveries = [
            {"emoji": "📦", "carrier": "Amazon", "status": "Expected 2:00 PM"},
            {"emoji": "📮", "carrier": "USPS", "status": "Delivered 10:24 AM"},
            {"emoji": "📦", "carrier": "FedEx", "status": "Out for delivery"},
        ]

        for delivery in deliveries:
            delivery_line = f"  {delivery['emoji']} {delivery['carrier']}"
            delivery_surf = self.label_font.render(delivery_line, True, color)
            self.screen.blit(delivery_surf, (right_col_x + 40, right_y))
            right_y += 40

            status_line = f"     {delivery['status']}"
            status_surf = self.label_font.render(status_line, True, tuple(int(c * 0.6) for c in color))
            self.screen.blit(status_surf, (right_col_x + 40, right_y))
            right_y += line_h + 10

    def render_scenes_routines(self):
        """View 3: Scenes & Routines - Larger scene cards."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        # Center the scene cards
        center_x = int(w * 0.15)
        top = int(h * 0.25)
        line_h = 60

        y = top

        # Section title
        section_text = "🎛️ Quick Scenes & Routines"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (center_x, y))
        y += line_h + 40

        scenes = [
            {"icon": "🌅", "name": "Morning Boost", "desc": "Lights on, coffee maker, blinds up"},
            {"icon": "🎬", "name": "Movie Night", "desc": "Dim lights, close blinds, sound on"},
            {"icon": "📚", "name": "Study Focus", "desc": "Focus lighting, quiet mode, no distractions"},
            {"icon": "🛫", "name": "Travel / Away", "desc": "Lock all, cameras active, eco mode"},
        ]

        for scene in scenes:
            # Scene name with icon (larger)
            scene_line = f"  {scene['icon']}  {scene['name']}"
            scene_surf = self.body_font.render(scene_line, True, color)
            self.screen.blit(scene_surf, (center_x + 40, y))
            y += line_h

            # Description (indented, dimmer)
            desc_line = f"       {scene['desc']}"
            desc_surf = self.label_font.render(desc_line, True, tuple(int(c * 0.6) for c in color))
            self.screen.blit(desc_surf, (center_x + 40, y))
            y += line_h + 20

    def render_ambient_loop(self):
        """View 4: Ambient Loop - Large centered status display."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        # Big centered emoji
        emoji_text = "🏡"
        emoji_surf = self.emoji_font.render(emoji_text, True, color)
        emoji_x = (w - emoji_surf.get_width()) // 2
        emoji_y = int(h * 0.30)
        self.screen.blit(emoji_surf, (emoji_x, emoji_y))

        # Big clock below emoji
        current_time = time.strftime("%I:%M %p")
        time_surf = self.title_font.render(current_time, True, color)
        time_x = (w - time_surf.get_width()) // 2
        time_y = emoji_y + 120
        self.screen.blit(time_surf, (time_x, time_y))

        # Status line
        status_text = "All systems secure • 3 rooms active"
        status_surf = self.subtitle_font.render(status_text, True, tuple(int(c * 0.7) for c in color))
        status_x = (w - status_surf.get_width()) // 2
        status_y = time_y + 100
        self.screen.blit(status_surf, (status_x, status_y))

        # Date line
        current_date = time.strftime("%A, %B %d, %Y")
        date_surf = self.label_font.render(current_date, True, tuple(int(c * 0.5) for c in color))
        date_x = (w - date_surf.get_width()) // 2
        date_y = status_y + 70
        self.screen.blit(date_surf, (date_x, date_y))

    def draw_doorbell_overlay(self):
        """Draw doorbell event overlay (right side)."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()

        # Panel on right side
        panel_w = int(w * 0.35)
        panel_h = 250
        panel_x = w - panel_w - 80
        panel_y = int(h * 0.3)

        # Draw semi-transparent panel
        panel_color = tuple(int(c * brightness * 0.2) for c in (255, 200, 0))
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, panel_color, panel_rect)
        border_color = tuple(int(c * brightness * 0.8) for c in (255, 200, 0))
        pygame.draw.rect(self.screen, border_color, panel_rect, 3)

        # Title
        title_text = "🔔 Doorbell Event"
        title_color = tuple(int(c * brightness) for c in (255, 200, 0))
        title_surf = self.body_font.render(title_text, True, title_color)
        self.screen.blit(title_surf, (panel_x + 20, panel_y + 20))

        # Event details
        y = panel_y + 80
        text_color = tuple(int(c * brightness) for c in (255, 255, 255))

        details = [
            f"👤 {self.doorbell_event['person']}",
            f"📍 {self.doorbell_event['action']}",
            f"🕐 {self.doorbell_event['time']}",
        ]

        for detail in details:
            detail_surf = self.label_font.render(detail, True, text_color)
            self.screen.blit(detail_surf, (panel_x + 30, y))
            y += 45
