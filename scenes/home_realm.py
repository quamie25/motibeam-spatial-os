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

        # Initialize custom fonts for wall readability
        pygame.font.init()
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 34, bold=False)
        self.body_font = pygame.font.SysFont("Arial", 32)
        self.label_font = pygame.font.SysFont("Arial", 26)

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

    def render_home_overview(self):
        """View 1: Home Overview - Family, Devices, Today."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        left_margin = int(w * 0.12)
        top = int(h * 0.25)
        line_h = 40

        y = top

        # Section: Family Presence
        section_text = "👨‍👩‍👧 Family Presence"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        for member in self.family_members:
            line = f"  {member['emoji']} {member['name']} – {member['location']}"
            line_surf = self.body_font.render(line, True, color)
            self.screen.blit(line_surf, (left_margin + 40, y))
            y += line_h

        y += 30

        # Section: Devices
        section_text = "🔌 Devices"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        for device in self.devices:
            line = f"  {device['emoji']} {device['name']} – {device['status']}"
            line_surf = self.body_font.render(line, True, color)
            self.screen.blit(line_surf, (left_margin + 40, y))
            y += line_h

        y += 30

        # Section: Today
        section_text = "📅 Today"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        for item in self.today_items:
            line = f"  {item['emoji']} {item['text']}"
            line_surf = self.body_font.render(line, True, color)
            self.screen.blit(line_surf, (left_margin + 40, y))
            y += line_h

        # Show doorbell event if recent
        if self.doorbell_event and (time.time() - self.last_doorbell_time < 8):
            self.draw_doorbell_overlay()

    def render_camera_deliveries(self):
        """View 2: Cameras & Deliveries - Security feed events."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        left_margin = int(w * 0.12)
        top = int(h * 0.25)
        line_h = 40

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
            line_surf = self.body_font.render(line, True, color)
            self.screen.blit(line_surf, (left_margin + 40, y))
            y += line_h

        y += 30

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
            event_surf = self.body_font.render(event, True, color)
            self.screen.blit(event_surf, (left_margin + 40, y))
            y += line_h

        y += 30

        # Section: Deliveries
        section_text = "🚚 Deliveries Today"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 20

        deliveries = [
            "  📦 Amazon - Expected 2:00 PM",
            "  📮 USPS - Delivered at 10:24 AM",
        ]

        for delivery in deliveries:
            delivery_surf = self.body_font.render(delivery, True, color)
            self.screen.blit(delivery_surf, (left_margin + 40, y))
            y += line_h

    def render_scenes_routines(self):
        """View 3: Scenes & Routines - Quick actions."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        left_margin = int(w * 0.12)
        top = int(h * 0.25)
        line_h = 50

        y = top

        # Section title
        section_text = "🎛️ Quick Scenes"
        section_surf = self.body_font.render(section_text, True, tuple(int(c * 0.9) for c in (100, 200, 255)))
        self.screen.blit(section_surf, (left_margin, y))
        y += line_h + 30

        scenes = [
            {"icon": "🌅", "name": "Morning Boost", "desc": "Lights, coffee, blinds up"},
            {"icon": "🎬", "name": "Movie Night", "desc": "Dim lights, close blinds, sound on"},
            {"icon": "📚", "name": "Study Focus", "desc": "Focus lighting, quiet mode"},
            {"icon": "🛫", "name": "Travel / Away", "desc": "Lock all, cameras active, eco mode"},
        ]

        for scene in scenes:
            # Scene name with icon
            scene_line = f"  {scene['icon']} {scene['name']}"
            scene_surf = self.body_font.render(scene_line, True, color)
            self.screen.blit(scene_surf, (left_margin + 40, y))
            y += line_h

            # Description (smaller, indented)
            desc_line = f"     {scene['desc']}"
            desc_surf = self.label_font.render(desc_line, True, tuple(int(c * 0.6) for c in color))
            self.screen.blit(desc_surf, (left_margin + 40, y))
            y += line_h + 10

    def render_ambient_loop(self):
        """View 4: Ambient Loop - Minimal status."""
        w, h = self.screen.get_width(), self.screen.get_height()
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in (255, 255, 255))

        # Big clock in center
        current_time = time.strftime("%I:%M %p")
        time_surf = self.title_font.render(current_time, True, color)
        time_x = (w - time_surf.get_width()) // 2
        time_y = int(h * 0.35)
        self.screen.blit(time_surf, (time_x, time_y))

        # Status line below
        status_text = "🏡 All systems normal"
        status_surf = self.subtitle_font.render(status_text, True, tuple(int(c * 0.7) for c in color))
        status_x = (w - status_surf.get_width()) // 2
        status_y = time_y + 100
        self.screen.blit(status_surf, (status_x, status_y))

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
