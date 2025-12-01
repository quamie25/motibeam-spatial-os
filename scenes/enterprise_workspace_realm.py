"""
Enterprise Workspace Realm - "Operations War Room"

Large-format "Enterprise Command Wall" readable from 8-10 ft.
Displays: KPIs, Team Focus, Upcoming Events, Operations Updates
"""

import pygame
from core.realm_base import RealmBase
from typing import List
import random


class EnterpriseWorkspaceRealm(RealmBase):
    """Enterprise Operations War Room display."""

    def __init__(self, screen: pygame.Surface, theme):
        super().__init__(screen, theme)

        # Sample data (in real implementation, this would come from APIs)
        self.kpi_data = {
            'sales': {'value': '$847K', 'label': 'SALES TODAY'},
            'tickets': {'value': '127', 'label': 'TICKETS CLOSED'},
            'uptime': {'value': '99.8%', 'label': 'SYSTEM UPTIME'},
            'meetings': {'value': '18', 'label': 'MEETINGS HELD'},
        }

        self.team_data = {
            'engineering': {
                'status': 'BUILDING',
                'focus': 'API v3 Migration',
                'progress': 68,
                'members': 12
            },
            'support': {
                'status': 'ACTIVE',
                'focus': 'Incident #2847',
                'progress': 45,
                'members': 8
            },
            'sales': {
                'status': 'ENGAGED',
                'focus': 'Q4 Pipeline',
                'progress': 82,
                'members': 15
            }
        }

        self.upcoming_events = [
            {'time': '10:00', 'event': 'Engineering Standup'},
            {'time': '11:30', 'event': 'Product Demo - Client X'},
            {'time': '14:00', 'event': 'Security Review Board'},
            {'time': '15:30', 'event': 'Sprint Retrospective'},
        ]

        self.ticker_messages = [
            'Production deploy completed successfully',
            'Customer satisfaction: 94% (↑2%)',
            'New hire onboarding: 3 engineers starting Monday',
            'Server maintenance scheduled for Saturday 2AM',
            'Q3 revenue target exceeded by 12%',
            'New feature: Dark mode released to 50% of users',
        ]

        self.load_status = random.choice(['STABLE', 'HIGH LOAD'])

    @property
    def realm_name(self) -> str:
        return "ENTERPRISE WORKSPACE"

    @property
    def realm_key(self) -> str:
        return "W"

    def get_modes(self) -> List[str]:
        return ["PERFORMANCE", "TEAM_HEALTH", "MEETING_CONTROL"]

    def render_mode(self, mode: str):
        """Render the current mode."""
        # Header (same for all modes)
        status_color = self.theme.get_status_color(self.load_status)
        self.draw_header(
            f"[{self.realm_key}] {self.realm_name}",
            "Operations · Productivity · Team Health",
            self.load_status,
            status_color
        )

        # Render mode-specific content
        if mode == "PERFORMANCE":
            self.render_performance_view()
        elif mode == "TEAM_HEALTH":
            self.render_team_health_view()
        elif mode == "MEETING_CONTROL":
            self.render_meeting_control_view()

        # Ticker (same for all modes)
        self.draw_ticker(self.ticker_messages, scroll_offset=pygame.time.get_ticks() * 0.05)

        # Mode indicator
        self.draw_mode_indicator(mode)

    def render_performance_view(self):
        """Render Performance View mode - TODAY'S PERFORMANCE KPIs."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Left column (50%) - TODAY'S PERFORMANCE
        left_panel_width = screen_width // 2 - 60
        self.draw_panel(40, 160, left_panel_width, screen_height - 280, "TODAY'S PERFORMANCE")

        # Draw 4 KPIs in 2x2 grid
        kpis = ['sales', 'tickets', 'uptime', 'meetings']
        kpi_start_y = 250

        for idx, kpi_key in enumerate(kpis):
            kpi = self.kpi_data[kpi_key]
            row = idx // 2
            col = idx % 2

            x = 80 + col * 350
            y = kpi_start_y + row * 180

            # Alternate colors for visual interest
            color = self.theme.colors['primary'] if idx % 2 == 0 else self.theme.colors['accent']
            self.draw_big_kpi(x, y, kpi['label'], kpi['value'], color)

        # Right column (50%) - Split into two sections
        right_x = screen_width // 2 + 20

        # Top right (Team Summary)
        self.draw_panel(right_x, 160, screen_width // 2 - 60, 300, "TEAM SUMMARY")

        team_y = 270
        team_names = list(self.team_data.keys())
        for idx, team_name in enumerate(team_names):
            team = self.team_data[team_name]
            y = team_y + idx * 70

            # Team name and status
            label_surf = self.theme.fonts['medium'].render(
                f"{team_name.upper()}: {team['members']} members",
                True,
                self.theme.colors['text']
            )
            self.screen.blit(label_surf, (right_x + 30, y))

            # Progress bar
            bar_x = right_x + 30
            bar_y = y + 45
            bar_width = 400
            bar_height = 12

            # Background
            pygame.draw.rect(self.screen, self.theme.colors['panel_bg'],
                           (bar_x, bar_y, bar_width, bar_height))

            # Progress
            progress_width = int(bar_width * (team['progress'] / 100))
            pygame.draw.rect(self.screen, self.theme.colors['success'],
                           (bar_x, bar_y, progress_width, bar_height))

            # Border
            pygame.draw.rect(self.screen, self.theme.colors['border'],
                           (bar_x, bar_y, bar_width, bar_height), 2)

        # Bottom right (Quick Stats)
        self.draw_panel(right_x, 500, screen_width // 2 - 60, screen_height - 620, "QUICK STATS")

        stats = [
            f"Active Projects: 24",
            f"Deploy Pipeline: 3 queued",
            f"Incidents: 0 critical",
            f"API Health: 99.2%",
        ]

        stat_y = 590
        for stat in stats:
            stat_surf = self.theme.fonts['medium'].render(stat, True, self.theme.colors['text'])
            self.screen.blit(stat_surf, (right_x + 30, stat_y))
            stat_y += 60

    def render_team_health_view(self):
        """Render Team Health mode - Detailed team status."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Three team panels
        panel_height = (screen_height - 280) // 3 - 20
        panel_y = 160

        for idx, (team_name, team_data) in enumerate(self.team_data.items()):
            y = panel_y + idx * (panel_height + 20)

            self.draw_panel(40, y, screen_width - 80, panel_height, team_name.upper())

            # Status
            status_x = 80
            status_y = y + 80
            status_surf = self.theme.fonts['large'].render(
                f"STATUS: {team_data['status']}",
                True,
                self.theme.colors['success']
            )
            self.screen.blit(status_surf, (status_x, status_y))

            # Focus
            focus_y = status_y + 60
            focus_surf = self.theme.fonts['medium'].render(
                f"FOCUS: {team_data['focus']}",
                True,
                self.theme.colors['text']
            )
            self.screen.blit(focus_surf, (status_x, focus_y))

            # Progress
            progress_y = focus_y + 60
            progress_surf = self.theme.fonts['medium'].render(
                f"PROGRESS: {team_data['progress']}%",
                True,
                self.theme.colors['accent']
            )
            self.screen.blit(progress_surf, (status_x, progress_y))

            # Members
            members_x = screen_width - 400
            members_surf = self.theme.fonts['large'].render(
                f"{team_data['members']}",
                True,
                self.theme.colors['primary']
            )
            self.screen.blit(members_surf, (members_x, status_y))

            members_label = self.theme.fonts['label'].render(
                "MEMBERS",
                True,
                self.theme.colors['text_dim']
            )
            self.screen.blit(members_label, (members_x, status_y + 60))

    def render_meeting_control_view(self):
        """Render Meeting Control mode - Upcoming events and meeting status."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Left panel - Current meeting status
        left_width = screen_width // 2 - 60
        self.draw_panel(40, 160, left_width, 400, "CURRENT MEETING")

        current_time_surf = self.theme.fonts['huge'].render("10:23", True, self.theme.colors['primary'])
        self.screen.blit(current_time_surf, (80, 260))

        current_meeting_surf = self.theme.fonts['large'].render(
            "Engineering Standup",
            True,
            self.theme.colors['text']
        )
        self.screen.blit(current_meeting_surf, (80, 400))

        status_surf = self.theme.fonts['medium'].render(
            "IN PROGRESS · 23 min remaining",
            True,
            self.theme.colors['success']
        )
        self.screen.blit(status_surf, (80, 470))

        # Left bottom panel - Meeting stats
        self.draw_panel(40, 600, left_width, screen_height - 720, "TODAY'S STATS")

        stats_y = 690
        meeting_stats = [
            "Meetings: 8 / 18 complete",
            "Avg Duration: 28 min",
            "Rooms Booked: 12 / 15",
        ]

        for stat in meeting_stats:
            stat_surf = self.theme.fonts['medium'].render(stat, True, self.theme.colors['text'])
            self.screen.blit(stat_surf, (80, stats_y))
            stats_y += 60

        # Right panel - Upcoming meetings
        right_x = screen_width // 2 + 20
        self.draw_panel(right_x, 160, screen_width // 2 - 60, screen_height - 280, "UPCOMING TODAY")

        event_y = 260
        for event in self.upcoming_events:
            # Time
            time_surf = self.theme.fonts['large'].render(
                event['time'],
                True,
                self.theme.colors['accent']
            )
            self.screen.blit(time_surf, (right_x + 40, event_y))

            # Event name
            event_surf = self.theme.fonts['medium'].render(
                event['event'],
                True,
                self.theme.colors['text']
            )
            self.screen.blit(event_surf, (right_x + 200, event_y + 10))

            # Separator line
            pygame.draw.line(
                self.screen,
                self.theme.colors['border'],
                (right_x + 40, event_y + 70),
                (right_x + screen_width // 2 - 100, event_y + 70),
                1
            )

            event_y += 100

    def draw_mode_indicator(self, mode: str):
        """Draw current mode indicator."""
        mode_x = self.screen.get_width() // 2 - 200
        mode_y = 120

        mode_text = mode.replace('_', ' ')
        mode_surf = self.theme.fonts['label'].render(
            f"MODE: {mode_text}",
            True,
            self.theme.colors['accent']
        )
        self.screen.blit(mode_surf, (mode_x, mode_y))
