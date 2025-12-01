"""
Aviation Control Realm - "ATC Sector Wall"

Air-traffic-control wall HUD with glowing neon radar display.
Displays: Radar sector, Flight paths, Arrivals/Departures, Weather
"""

import pygame
import math
from core.realm_base import RealmBase
from typing import List, Dict


class AviationControlRealm(RealmBase):
    """Aviation Control ATC Sector Wall display."""

    def __init__(self, screen: pygame.Surface, theme):
        super().__init__(screen, theme)

        # Flight data
        self.flights = [
            {
                'callsign': 'AA204',
                'altitude': 'FL320',
                'speed': '460 kts',
                'distance': '8 nm',
                'angle': 45,
                'type': 'departure'
            },
            {
                'callsign': 'DL119',
                'altitude': 'FL280',
                'speed': '425 kts',
                'distance': '12 nm',
                'angle': 120,
                'type': 'arrival'
            },
            {
                'callsign': 'UA877',
                'altitude': 'FL350',
                'speed': '480 kts',
                'distance': '15 nm',
                'angle': 200,
                'type': 'enroute'
            },
            {
                'callsign': 'SW523',
                'altitude': 'FL310',
                'speed': '445 kts',
                'distance': '6 nm',
                'angle': 280,
                'type': 'departure'
            },
            {
                'callsign': 'BA102',
                'altitude': 'FL340',
                'speed': '470 kts',
                'distance': '18 nm',
                'angle': 340,
                'type': 'arrival'
            },
        ]

        self.focus_flight_index = 0

        # Arrival/Departure stack
        self.arrivals = [
            {'callsign': 'AA789', 'eta': '10:45', 'runway': 'RWY 27L'},
            {'callsign': 'DL456', 'eta': '10:52', 'runway': 'RWY 27L'},
            {'callsign': 'UA234', 'eta': '11:08', 'runway': 'RWY 27R'},
            {'callsign': 'SW891', 'eta': '11:15', 'runway': 'RWY 27R'},
        ]

        self.departures = [
            {'callsign': 'AA312', 'std': '10:50', 'runway': 'RWY 09R'},
            {'callsign': 'DL667', 'std': '10:55', 'runway': 'RWY 09R'},
            {'callsign': 'UA445', 'std': '11:02', 'runway': 'RWY 09L'},
        ]

        # Weather and alerts
        self.weather_alerts = [
            'Wind: 270° at 12 kts',
            'Visibility: 10 SM',
            'Ceiling: 8000 ft',
            'Temperature: 18°C',
        ]

        self.ticker_messages = [
            'RWY 27L: Landing traffic heavy',
            'ATIS Info Charlie current',
            'Ground stop cleared - normal ops',
            'Thunderstorm 40 nm west, moving east',
            'Departure rate: 32/hour',
            'Approach spacing: 5 nm in trail',
        ]

    @property
    def realm_name(self) -> str:
        return "AVIATION CONTROL"

    @property
    def realm_key(self) -> str:
        return "A"

    def get_modes(self) -> List[str]:
        return ["SECTOR_OVERVIEW", "APPROACH_FOCUS", "WEATHER_ROUTING"]

    def render_mode(self, mode: str):
        """Render the current mode."""
        # Header
        self.draw_header(
            f"[{self.realm_key}] {self.realm_name}",
            "Airspace · Flight Paths · Collision Avoidance",
            "ACTIVE SECTOR",
            self.theme.colors['success']
        )

        # Render mode-specific content
        if mode == "SECTOR_OVERVIEW":
            self.render_sector_overview()
        elif mode == "APPROACH_FOCUS":
            self.render_approach_focus()
        elif mode == "WEATHER_ROUTING":
            self.render_weather_routing()

        # Ticker
        self.draw_ticker(self.ticker_messages, scroll_offset=pygame.time.get_ticks() * 0.05)

        # Mode indicator
        self.draw_mode_indicator(mode)

    def render_sector_overview(self):
        """Render Sector Overview mode - Full radar with all flights."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Left panel (60%) - Radar display
        radar_width = int(screen_width * 0.6) - 60
        radar_height = screen_height - 280

        self.draw_panel(40, 160, radar_width, radar_height, "RADAR SECTOR")

        # Calculate radar center and radius
        radar_center_x = 40 + radar_width // 2
        radar_center_y = 160 + radar_height // 2
        radar_radius = min(radar_width, radar_height) // 2 - 80

        # Draw radar rings
        self.theme.draw_radar_rings(self.screen, (radar_center_x, radar_center_y), radar_radius, num_rings=5)

        # Draw flights on radar
        for idx, flight in enumerate(self.flights):
            self.draw_flight_on_radar(
                radar_center_x,
                radar_center_y,
                radar_radius,
                flight,
                is_focus=(idx == self.focus_flight_index)
            )

        # Right panel (40%) - Flight stack
        right_x = int(screen_width * 0.6) + 20
        right_width = screen_width - right_x - 40

        # Arrivals
        arrivals_height = (radar_height - 20) // 2
        self.draw_panel(right_x, 160, right_width, arrivals_height, "ARRIVALS")

        arrival_y = 260
        for arrival in self.arrivals:
            self.draw_flight_entry(right_x + 30, arrival_y, arrival, is_arrival=True)
            arrival_y += 90

        # Departures
        departures_y = 160 + arrivals_height + 20
        self.draw_panel(right_x, departures_y, right_width, arrivals_height, "DEPARTURES")

        departure_y = departures_y + 100
        for departure in self.departures:
            self.draw_flight_entry(right_x + 30, departure_y, departure, is_arrival=False)
            departure_y += 90

    def render_approach_focus(self):
        """Render Approach Focus mode - Detailed view of focus aircraft."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        focus_flight = self.flights[self.focus_flight_index]

        # Large focus panel
        self.draw_panel(40, 160, screen_width - 80, 400, "FOCUS AIRCRAFT")

        # Callsign (huge)
        callsign_surf = self.theme.fonts['huge'].render(
            focus_flight['callsign'],
            True,
            self.theme.colors['primary']
        )
        self.screen.blit(callsign_surf, (80, 260))

        # Flight data in columns
        data_y = 420
        data_items = [
            ('ALTITUDE', focus_flight['altitude']),
            ('SPEED', focus_flight['speed']),
            ('DISTANCE', focus_flight['distance']),
            ('TYPE', focus_flight['type'].upper()),
        ]

        for idx, (label, value) in enumerate(data_items):
            x = 80 + (idx % 2) * 600
            y = data_y + (idx // 2) * 100

            label_surf = self.theme.fonts['label'].render(label, True, self.theme.colors['text_dim'])
            self.screen.blit(label_surf, (x, y))

            value_surf = self.theme.fonts['large'].render(value, True, self.theme.colors['text'])
            self.screen.blit(value_surf, (x, y + 40))

        # Radar view (smaller)
        radar_panel_y = 600
        self.draw_panel(40, radar_panel_y, screen_width - 80, screen_height - radar_panel_y - 120, "RADAR VIEW")

        radar_center_x = screen_width // 2
        radar_center_y = radar_panel_y + (screen_height - radar_panel_y - 120) // 2
        radar_radius = 180

        self.theme.draw_radar_rings(self.screen, (radar_center_x, radar_center_y), radar_radius, num_rings=3)

        # Draw focused flight in center with nearby traffic
        self.draw_flight_on_radar(
            radar_center_x,
            radar_center_y,
            radar_radius,
            focus_flight,
            is_focus=True
        )

    def render_weather_routing(self):
        """Render Weather/Rerouting mode - Weather conditions and routing."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Left panel - Weather conditions
        left_width = int(screen_width * 0.6) - 60
        self.draw_panel(40, 160, left_width, 450, "WEATHER CONDITIONS")

        weather_y = 260
        for alert in self.weather_alerts:
            alert_surf = self.theme.fonts['large'].render(alert, True, self.theme.colors['text'])
            self.screen.blit(alert_surf, (80, weather_y))
            weather_y += 80

        # Weather map placeholder
        map_y = 640
        self.draw_panel(40, map_y, left_width, screen_height - map_y - 120, "WEATHER RADAR")

        # Draw weather representation (simple storm cells)
        map_center_x = 40 + left_width // 2
        map_center_y = map_y + (screen_height - map_y - 120) // 2

        # Storm cells
        storm_positions = [(0.3, 0.4), (0.5, 0.6), (0.7, 0.3)]
        for sx, sy in storm_positions:
            storm_x = int(map_center_x + (sx - 0.5) * left_width * 0.6)
            storm_y = int(map_center_y + (sy - 0.5) * 200)

            # Draw storm with glow
            self.theme.draw_glow_circle(
                self.screen,
                (storm_x, storm_y),
                30,
                self.theme.colors['danger'],
                glow_layers=4
            )

        # Right panel - Rerouting information
        right_x = int(screen_width * 0.6) + 20
        right_width = screen_width - right_x - 40

        self.draw_panel(right_x, 160, right_width, screen_height - 280, "ACTIVE REROUTES")

        reroute_y = 260
        reroutes = [
            'AA204: Via FIXXY',
            'DL119: Hold at WALDO',
            'UA877: Direct BRHMA',
            'SW523: Descend FL280',
        ]

        for reroute in reroutes:
            reroute_surf = self.theme.fonts['medium'].render(reroute, True, self.theme.colors['warning'])
            self.screen.blit(reroute_surf, (right_x + 30, reroute_y))
            reroute_y += 80

    def draw_flight_on_radar(self, center_x: int, center_y: int, radius: int,
                            flight: Dict, is_focus: bool = False):
        """Draw a flight on the radar display."""
        # Calculate position based on angle and distance
        # Distance mapping: max distance on radar is at radius
        angle_rad = math.radians(flight['angle'])
        distance_factor = 0.3 + (hash(flight['callsign']) % 40) / 100  # Vary distance

        flight_x = int(center_x + math.cos(angle_rad) * radius * distance_factor)
        flight_y = int(center_y - math.sin(angle_rad) * radius * distance_factor)

        # Draw flight marker
        marker_color = self.theme.colors['accent'] if is_focus else self.theme.colors['primary']
        marker_size = 12 if is_focus else 8

        # Draw glow if focus
        if is_focus:
            self.theme.draw_glow_circle(self.screen, (flight_x, flight_y), marker_size, marker_color)
        else:
            pygame.draw.circle(self.screen, marker_color, (flight_x, flight_y), marker_size)

        # Draw callsign label
        label_font = self.theme.fonts['label'] if is_focus else pygame.font.Font(
            pygame.font.match_font('monospace', bold=True), 22
        )
        callsign_surf = label_font.render(flight['callsign'], True, self.theme.colors['text'])
        self.screen.blit(callsign_surf, (flight_x + 20, flight_y - 10))

        # Draw data tag (altitude, speed)
        if is_focus:
            data_text = f"{flight['altitude']} · {flight['speed']}"
            data_surf = pygame.font.Font(pygame.font.match_font('monospace'), 20).render(
                data_text, True, self.theme.colors['text_dim']
            )
            self.screen.blit(data_surf, (flight_x + 20, flight_y + 20))

    def draw_flight_entry(self, x: int, y: int, flight: Dict, is_arrival: bool):
        """Draw a flight entry in the arrival/departure stack."""
        # Callsign
        callsign_surf = self.theme.fonts['medium'].render(
            flight['callsign'],
            True,
            self.theme.colors['accent'] if is_arrival else self.theme.colors['warning']
        )
        self.screen.blit(callsign_surf, (x, y))

        # Time (ETA or STD)
        time_key = 'eta' if is_arrival else 'std'
        time_surf = self.theme.fonts['label'].render(
            flight[time_key],
            True,
            self.theme.colors['text_dim']
        )
        self.screen.blit(time_surf, (x + 250, y + 5))

        # Runway
        runway_surf = self.theme.fonts['label'].render(
            flight['runway'],
            True,
            self.theme.colors['text']
        )
        self.screen.blit(runway_surf, (x, y + 40))

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
        """Update realm state - animate flights."""
        super().update()

        # Slowly rotate flights around radar
        for flight in self.flights:
            flight['angle'] = (flight['angle'] + 0.1) % 360

        # Cycle focus flight every 8 seconds
        if pygame.time.get_ticks() % 8000 < 50:
            self.focus_flight_index = (self.focus_flight_index + 1) % len(self.flights)
