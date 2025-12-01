"""
Maritime Operations Realm - "Port Command Board"

Harbor/port operations wall like a marine control center.
Displays: Harbor zones, Vessel traffic, Port operations, Weather routing
"""

import pygame
import math
from core.realm_base import RealmBase
from typing import List, Dict


class MaritimeOperationsRealm(RealmBase):
    """Maritime Operations Port Command Board display."""

    def __init__(self, screen: pygame.Surface, theme):
        super().__init__(screen, theme)

        # Vessel data organized by zone
        self.vessels = [
            {
                'name': 'ATLANTIC STAR',
                'type': 'Container',
                'zone': 'INNER HARBOR',
                'eta': '13:22',
                'berth': 'B3',
                'status': 'BERTHING',
                'angle': 45
            },
            {
                'name': 'PACIFIC DREAM',
                'type': 'Tanker',
                'zone': 'OUTER CHANNEL',
                'eta': '14:15',
                'berth': 'T1',
                'status': 'INBOUND',
                'angle': 120
            },
            {
                'name': 'NORDIC WAVE',
                'type': 'Bulk Carrier',
                'zone': 'ANCHORAGE',
                'eta': '15:30',
                'berth': 'A2',
                'status': 'ANCHORED',
                'angle': 200
            },
            {
                'name': 'LIBERTY EXPRESS',
                'type': 'RoRo',
                'zone': 'INNER HARBOR',
                'eta': '12:45',
                'berth': 'R5',
                'status': 'LOADING',
                'angle': 280
            },
            {
                'name': 'OCEAN MONARCH',
                'type': 'Container',
                'zone': 'OUTER CHANNEL',
                'eta': '16:00',
                'berth': 'B7',
                'status': 'APPROACHING',
                'angle': 340
            },
        ]

        # Port operations data
        self.operations = {
            'tug_ops': [
                'TUG-1: Assisting ATLANTIC STAR',
                'TUG-2: Standing by at B3',
                'TUG-3: Available',
            ],
            'berth_activity': [
                'B3: ATLANTIC STAR berthing',
                'B7: CRYSTAL SEAS departing',
                'T1: Available 14:00',
                'R5: LIBERTY EXPRESS loading',
            ],
            'customs': [
                'ATLANTIC STAR: Cleared',
                'PACIFIC DREAM: Pending',
                'NORDIC WAVE: Inspection req.',
            ],
            'security': [
                'Security Level: MARSEC 1',
                'Active Patrols: 4',
                'Access Control: Normal',
            ]
        }

        # Weather data
        self.weather_data = {
            'tide': 'High tide 14:23 (3.2m)',
            'wind': '15 kts NW',
            'swell': '1.2m / 8s',
            'visibility': '12 nm',
            'conditions': 'Clear',
        }

        # Ticker messages
        self.ticker_messages = [
            'Berth B7: Departure complete - clear for next vessel',
            'Tide turning in 90 minutes',
            'Pilot boat en route to PACIFIC DREAM',
            'Channel dredging: Complete ahead of schedule',
            'Container terminal: 87% capacity',
            'Next high tide: 02:47 (3.4m)',
        ]

    @property
    def realm_name(self) -> str:
        return "MARITIME OPERATIONS"

    @property
    def realm_key(self) -> str:
        return "M"

    def get_modes(self) -> List[str]:
        return ["VESSEL_TRAFFIC", "PORT_OPERATIONS", "WEATHER_ROUTING"]

    def render_mode(self, mode: str):
        """Render the current mode."""
        # Header
        self.draw_header(
            f"[{self.realm_key}] {self.realm_name}",
            "Vessels · Port Traffic · Weather Routing",
            "PORT ACTIVE",
            self.theme.colors['success']
        )

        # Render mode-specific content
        if mode == "VESSEL_TRAFFIC":
            self.render_vessel_traffic()
        elif mode == "PORT_OPERATIONS":
            self.render_port_operations()
        elif mode == "WEATHER_ROUTING":
            self.render_weather_routing()

        # Ticker
        self.draw_ticker(self.ticker_messages, scroll_offset=pygame.time.get_ticks() * 0.05)

        # Mode indicator
        self.draw_mode_indicator(mode)

    def render_vessel_traffic(self):
        """Render Vessel Traffic mode - Harbor view with vessel positions."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Left panel (60%) - Harbor view
        harbor_width = int(screen_width * 0.6) - 60
        harbor_height = screen_height - 280

        self.draw_panel(40, 160, harbor_width, harbor_height, "HARBOR VIEW")

        # Draw harbor zones
        harbor_center_x = 40 + harbor_width // 2
        harbor_center_y = 160 + harbor_height // 2
        harbor_radius = min(harbor_width, harbor_height) // 2 - 80

        # Draw zones (concentric areas)
        zones = [
            ('INNER HARBOR', 0.4, self.theme.colors['accent']),
            ('OUTER CHANNEL', 0.7, self.theme.colors['primary']),
            ('ANCHORAGE', 1.0, self.theme.colors['secondary']),
        ]

        for zone_name, zone_factor, zone_color in zones:
            zone_radius = int(harbor_radius * zone_factor)

            # Draw zone circle
            zone_surf = pygame.Surface((zone_radius * 2, zone_radius * 2), pygame.SRCALPHA)
            zone_alpha_color = (*zone_color, 30)
            pygame.draw.circle(zone_surf, zone_alpha_color, (zone_radius, zone_radius), zone_radius, 3)
            self.screen.blit(zone_surf, (harbor_center_x - zone_radius, harbor_center_y - zone_radius))

            # Draw zone label
            if zone_factor < 1.0:
                label_surf = self.theme.fonts['label'].render(zone_name, True, zone_color)
                label_x = harbor_center_x - label_surf.get_width() // 2
                label_y = harbor_center_y - int(zone_radius * 0.7)
                self.screen.blit(label_surf, (label_x, label_y))

        # Draw vessels in harbor
        for vessel in self.vessels:
            self.draw_vessel_on_harbor(
                harbor_center_x,
                harbor_center_y,
                harbor_radius,
                vessel
            )

        # Right panel (40%) - Vessel list
        right_x = int(screen_width * 0.6) + 20
        right_width = screen_width - right_x - 40

        self.draw_panel(right_x, 160, right_width, harbor_height, "VESSEL STACK")

        vessel_y = 260
        for vessel in self.vessels:
            self.draw_vessel_entry(right_x + 30, vessel_y, vessel)
            vessel_y += 140

    def render_port_operations(self):
        """Render Port Operations mode - Detailed operations status."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Four panels for different operations
        panel_width = (screen_width - 120) // 2
        panel_height = (screen_height - 320) // 2

        ops_sections = [
            ('TUG OPERATIONS', 'tug_ops', 0, 0),
            ('BERTH ACTIVITY', 'berth_activity', 1, 0),
            ('CUSTOMS STATUS', 'customs', 0, 1),
            ('SECURITY', 'security', 1, 1),
        ]

        for title, data_key, col, row in ops_sections:
            x = 40 + col * (panel_width + 40)
            y = 160 + row * (panel_height + 40)

            self.draw_panel(x, y, panel_width, panel_height, title)

            # Draw operation items
            item_y = y + 100
            for item in self.operations[data_key]:
                item_surf = self.theme.fonts['medium'].render(item, True, self.theme.colors['text'])
                self.screen.blit(item_surf, (x + 30, item_y))
                item_y += 60

    def render_weather_routing(self):
        """Render Weather Routing mode - Weather conditions and sea state."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Left panel - Sea state and weather
        left_width = int(screen_width * 0.6) - 60
        self.draw_panel(40, 160, left_width, 500, "SEA STATE & WEATHER")

        weather_y = 260
        weather_items = [
            ('TIDE', self.weather_data['tide']),
            ('WIND', self.weather_data['wind']),
            ('SWELL', self.weather_data['swell']),
            ('VISIBILITY', self.weather_data['visibility']),
            ('CONDITIONS', self.weather_data['conditions']),
        ]

        for label, value in weather_items:
            label_surf = self.theme.fonts['label'].render(label, True, self.theme.colors['text_dim'])
            self.screen.blit(label_surf, (80, weather_y))

            value_surf = self.theme.fonts['large'].render(value, True, self.theme.colors['text'])
            self.screen.blit(value_surf, (80, weather_y + 35))

            weather_y += 90

        # Weather chart placeholder
        chart_y = 700
        self.draw_panel(40, chart_y, left_width, screen_height - chart_y - 120, "TIDE CHART")

        # Draw simple tide curve
        chart_x = 80
        chart_width = left_width - 80
        chart_center_y = chart_y + (screen_height - chart_y - 120) // 2

        points = []
        for i in range(50):
            x = chart_x + i * (chart_width // 50)
            # Simple sine wave for tide
            y = chart_center_y + int(math.sin(i * 0.3) * 40)
            points.append((x, y))

        if len(points) > 1:
            pygame.draw.lines(self.screen, self.theme.colors['primary'], False, points, 3)

        # Right panel - Routing and delays
        right_x = int(screen_width * 0.6) + 20
        right_width = screen_width - right_x - 40

        # Top: Routing advisories
        self.draw_panel(right_x, 160, right_width, 400, "ROUTING ADVISORIES")

        advisory_y = 260
        advisories = [
            'Channel clear',
            'No traffic restrictions',
            'Optimal entry window',
            'Pilot availability: High',
        ]

        for advisory in advisories:
            advisory_surf = self.theme.fonts['medium'].render(advisory, True, self.theme.colors['success'])
            self.screen.blit(advisory_surf, (right_x + 30, advisory_y))
            advisory_y += 80

        # Bottom: Delays and backlogs
        delay_y = 600
        self.draw_panel(right_x, delay_y, right_width, screen_height - delay_y - 120, "DELAYS & BACKLOGS")

        delay_items_y = delay_y + 100
        delays = [
            'Average wait: 15 min',
            'Backlog: 2 vessels',
            'Customs delay: None',
        ]

        for delay in delays:
            delay_surf = self.theme.fonts['medium'].render(delay, True, self.theme.colors['text'])
            self.screen.blit(delay_surf, (right_x + 30, delay_items_y))
            delay_items_y += 60

    def draw_vessel_on_harbor(self, center_x: int, center_y: int, radius: int, vessel: Dict):
        """Draw a vessel on the harbor view."""
        # Determine zone radius based on vessel zone
        zone_factors = {
            'INNER HARBOR': 0.4,
            'OUTER CHANNEL': 0.7,
            'ANCHORAGE': 1.0,
        }
        zone_factor = zone_factors.get(vessel['zone'], 0.7)

        # Calculate position
        angle_rad = math.radians(vessel['angle'])
        distance = radius * zone_factor * 0.85

        vessel_x = int(center_x + math.cos(angle_rad) * distance)
        vessel_y = int(center_y - math.sin(angle_rad) * distance)

        # Draw vessel icon (triangle for ship)
        vessel_color = self.theme.colors['accent']
        size = 15

        # Triangle points (pointing in direction of angle)
        points = [
            (vessel_x + int(math.cos(angle_rad) * size),
             vessel_y - int(math.sin(angle_rad) * size)),
            (vessel_x + int(math.cos(angle_rad + 2.5) * size * 0.6),
             vessel_y - int(math.sin(angle_rad + 2.5) * size * 0.6)),
            (vessel_x + int(math.cos(angle_rad - 2.5) * size * 0.6),
             vessel_y - int(math.sin(angle_rad - 2.5) * size * 0.6)),
        ]

        pygame.draw.polygon(self.screen, vessel_color, points)
        pygame.draw.polygon(self.screen, self.theme.colors['border'], points, 2)

        # Draw vessel name
        name_surf = pygame.font.Font(pygame.font.match_font('monospace', bold=True), 20).render(
            vessel['name'].split()[0],  # First word only for space
            True,
            self.theme.colors['text']
        )
        self.screen.blit(name_surf, (vessel_x + 25, vessel_y - 10))

    def draw_vessel_entry(self, x: int, y: int, vessel: Dict):
        """Draw a vessel entry in the vessel stack."""
        # Vessel name (larger)
        name_surf = self.theme.fonts['medium'].render(vessel['name'], True, self.theme.colors['accent'])
        self.screen.blit(name_surf, (x, y))

        # ETA and berth
        info_y = y + 45
        info_text = f"ETA {vessel['eta']} · Berth {vessel['berth']}"
        info_surf = self.theme.fonts['label'].render(info_text, True, self.theme.colors['text_dim'])
        self.screen.blit(info_surf, (x, info_y))

        # Status
        status_y = info_y + 35
        status_color = self.theme.colors['success'] if vessel['status'] in ['BERTHING', 'LOADING'] else self.theme.colors['warning']
        status_surf = self.theme.fonts['label'].render(vessel['status'], True, status_color)
        self.screen.blit(status_surf, (x, status_y))

    def draw_mode_indicator(self, mode: str):
        """Draw current mode indicator."""
        mode_x = self.screen.get_width() // 2 - 250
        mode_y = 120

        mode_text = mode.replace('_', ' ')
        mode_surf = self.theme.fonts['label'].render(
            f"MODE: {mode_text}",
            True,
            self.theme.colors['accent']
        )
        self.screen.blit(mode_surf, (mode_x, mode_y))

    def update(self):
        """Update realm state - animate vessels."""
        super().update()

        # Slowly move vessels around harbor
        for vessel in self.vessels:
            vessel['angle'] = (vessel['angle'] + 0.08) % 360
