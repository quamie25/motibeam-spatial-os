"""
Home Realm - Smart Home & Family HUD

Views:
1. Home Overview - Family presence, devices, climate
2. Camera & Deliveries - Security footage and delivery events
3. Scenes & Routines - Morning, Movie Night, Study, Away
4. Ambient Home Loop - Minimal status display
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

        # Sample data
        self.family_members = [
            {"name": "Emma", "location": "Home", "status": "active"},
            {"name": "David", "location": "Office", "status": "away"},
            {"name": "Sophie", "location": "School", "status": "away"},
        ]

        self.devices = {
            "online": random.randint(28, 34),
            "doors_locked": True,
            "temp": random.randint(70, 74),
            "lights_on": random.randint(4, 8),
        }

        self.deliveries = [
            {"time": "10:24 AM", "courier": "Amazon", "item": "Package #1234"},
            {"time": "2:15 PM", "courier": "UPS", "item": "Documents"},
        ]

        self.doorbell_event = None
        self.last_doorbell_time = 0

    @property
    def realm_name(self) -> str:
        return "HOME"

    @property
    def realm_icon(self) -> str:
        return "🏡"

    def get_views(self) -> List[Dict]:
        return [
            {"name": "Home Overview", "render": self.render_home_overview},
            {"name": "Camera & Deliveries", "render": self.render_camera_deliveries},
            {"name": "Scenes & Routines", "render": self.render_scenes_routines},
            {"name": "Ambient Loop", "render": self.render_ambient_loop"},
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

    def render_home_overview(self):
        """View 1: Home Overview with family + devices."""
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        # Left panel - Family presence
        left_w = screen_w // 2 - 100
        self.draw_panel(60, 200, left_w, 500, "FAMILY PRESENCE")

        y = 300
        for member in self.family_members:
            status_icon = "🟢" if member["status"] == "active" else "🔵"
            line = f"{status_icon} {member['name']}: {member['location']}"
            self.draw_content_lines([line], y, 80)
            y += 100

        # Right top - Devices & Status
        right_x = screen_w // 2 + 40
        right_w = screen_w // 2 - 100
        self.draw_panel(right_x, 200, right_w, 240, "HOME STATUS")

        status_lines = [
            f"Devices Online: {self.devices['online']}",
            f"Doors: {'🔒 LOCKED' if self.devices['doors_locked'] else '🔓 UNLOCKED'}",
            f"Temperature: {self.devices['temp']}°F",
            f"Lights On: {self.devices['lights_on']} zones",
        ]
        self.draw_content_lines(status_lines, 300, 50)

        # Right bottom - Deliveries
        self.draw_panel(right_x, 480, right_w, 220, "TODAY'S DELIVERIES")

        del_y = 580
        for delivery in self.deliveries:
            del_line = f"{delivery['time']} - {delivery['courier']}"
            self.draw_content_lines([del_line], del_y, 60)
            del_y += 70

        # Show doorbell event if recent
        if self.doorbell_event and (time.time() - self.last_doorbell_time < 8):
            self.draw_doorbell_panel()

    def render_camera_deliveries(self):
        """View 2: Camera feed and delivery events."""
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        # Big "camera" frame
        cam_w = screen_w - 160
        cam_h = 500
        self.draw_panel(80, 200, cam_w, cam_h, "FRONT DOOR CAMERA")

        # Simulated camera view with gradient
        cam_rect = pygame.Rect(100, 270, cam_w - 40, cam_h - 90)
        brightness = self.global_state.get_brightness_multiplier()
        grad_color = tuple(int(c * brightness * 0.3) for c in (50, 50, 80))
        pygame.draw.rect(self.screen, grad_color, cam_rect)

        # Camera info overlay
        cam_info = [
            "Last Motion: 2 min ago",
            "Recording: ON",
            f"Temp: {self.devices['temp']}°F",
        ]
        self.draw_content_lines(cam_info, 300, 60)

        # Recent events below
        events_y = 750
        event_lines = [
            "10:24 AM - Package delivered",
            "9:15 AM - Motion detected",
            "8:03 AM - Mailbox opened",
        ]

        for event in event_lines:
            self.draw_content_lines([event], events_y, 50)
            events_y += 60

    def render_scenes_routines(self):
        """View 3: Scenes and routines."""
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        # Title
        self.draw_big_text("SCENES & ROUTINES", 180)

        # 2x2 grid of scene tiles
        scenes = [
            {"name": "Morning", "icon": "☀️", "desc": "Lights, coffee, news"},
            {"name": "Movie Night", "icon": "🎬", "desc": "Dim lights, close blinds"},
            {"name": "Study Mode", "icon": "📚", "desc": "Focus lighting, quiet"},
            {"name": "Away", "icon": "🔒", "desc": "Lock all, cameras on"},
        ]

        tile_w = 700
        tile_h = 200
        gap = 60

        start_x = (screen_w - (tile_w * 2 + gap)) // 2
        start_y = 320

        for idx, scene in enumerate(scenes):
            row = idx // 2
            col = idx % 2

            x = start_x + col * (tile_w + gap)
            y = start_y + row * (tile_h + gap)

            self.draw_scene_tile(x, y, tile_w, tile_h, scene)

    def render_ambient_loop(self):
        """View 4: Minimal ambient display."""
        # Very simple display for ambient mode
        brightness = self.global_state.get_brightness_multiplier()

        # Just a few key stats in the center
        lines = [
            f"🏡 HOME STATUS",
            "",
            f"{'🔒 Secure' if self.devices['doors_locked'] else '🔓 Unsecured'}",
            f"{self.devices['lights_on']} lights on",
            f"{self.devices['temp']}°F",
            "",
            f"{self.devices['online']} devices online",
        ]

        start_y = 350
        for line in lines:
            self.draw_big_text(line, start_y)
            start_y += 80

    def draw_doorbell_panel(self):
        """Draw doorbell event overlay."""
        panel_w = 600
        panel_h = 200
        panel_x = self.screen.get_width() - panel_w - 80
        panel_y = 750

        brightness = self.global_state.get_brightness_multiplier()
        alert_color = tuple(int(c * brightness) for c in (255, 200, 0))

        self.draw_panel(panel_x, panel_y, panel_w, panel_h, "🔔 DOORBELL EVENT")

        event_lines = [
            f"{self.doorbell_event['person']}",
            f"{self.doorbell_event['action']}",
            f"Time: {self.doorbell_event['time']}",
        ]

        self.draw_content_lines(event_lines, panel_y + 100, 45)

    def draw_scene_tile(self, x: int, y: int, width: int, height: int, scene: dict):
        """Draw a scene activation tile."""
        self.draw_panel(x, y, width, height)

        brightness = self.global_state.get_brightness_multiplier()
        text_color = tuple(int(c * brightness) for c in self.theme.colors['text'])

        # Icon
        icon_surf = self.theme.fonts['large'].render(scene["icon"], True, text_color)
        icon_x = x + 30
        self.screen.blit(icon_surf, (icon_x, y + 30))

        # Name
        name_surf = self.theme.fonts['panel_title'].render(scene["name"], True, text_color)
        self.screen.blit(name_surf, (icon_x + 100, y + 40))

        # Description
        desc_color = tuple(int(c * brightness) for c in self.theme.colors['text_dim'])
        desc_surf = self.theme.fonts['label'].render(scene["desc"], True, desc_color)
        self.screen.blit(desc_surf, (icon_x + 100, y + 90))

        # "Press SPACE to activate" hint (subtle)
        hint = "SPACE to activate"
        hint_surf = self.theme.fonts['ticker'].render(hint, True, desc_color)
        self.screen.blit(hint_surf, (x + width - hint_surf.get_width() - 20, y + height - 35))
