"""
MotiBeam Spatial OS - TeleBeam Realm
Ambient telecommunications - visual caller ID system
"""

import pygame
import random
import math
from typing import Optional, Dict, List
from realms.base_realm import BaseRealm
from core.ui.framework import (
    Theme, Fonts, draw_text_shadowed, draw_glow_circle, draw_glow_rect,
    BreathingAnimation, PulseAnimation, ScrollingTicker
)


# Demo caller data
DEMO_CALLERS = [
    {
        "name": "Dr. Sarah Chen",
        "phone": "(555) 234-5678",
        "type": "trusted",
        "reason": "Telehealth Appointment",
        "priority": "normal",
        "trust_score": 1.0
    },
    {
        "name": "Caregiver - Emily",
        "phone": "(555) 987-6543",
        "type": "trusted",
        "reason": "Daily Check-In",
        "priority": "normal",
        "trust_score": 1.0
    },
    {
        "name": "Unknown Number",
        "phone": "(555) 123-4567",
        "type": "unknown",
        "reason": "Unknown",
        "priority": "low",
        "trust_score": 0.5
    },
    {
        "name": "Pharmacy Reminder",
        "phone": "(555) 456-7890",
        "type": "trusted",
        "reason": "Prescription Ready",
        "priority": "normal",
        "trust_score": 0.9
    },
    {
        "name": "VA Hotline",
        "phone": "1-800-273-8255",
        "type": "emergency",
        "reason": "Veterans Crisis Line",
        "priority": "high",
        "trust_score": 1.0
    },
    {
        "name": "Potential Spam",
        "phone": "(555) 000-0000",
        "type": "spam",
        "reason": "Unknown",
        "priority": "low",
        "trust_score": 0.1
    }
]


class CallerCard:
    """Visual caller card with all info"""

    def __init__(self, width: int, height: int, caller_data: Dict):
        self.width = width
        self.height = height
        self.caller_data = caller_data

        # Animation
        self.breathing = BreathingAnimation(0.85, 1.0, 0.03)
        self.pulse = PulseAnimation(duration=60)
        self.pulse.trigger()  # Start with pulse

        # Button states
        self.hovered_button = None  # "accept", "decline", "message"

    def get_color(self) -> tuple:
        """Get color based on caller type"""
        caller_type = self.caller_data["type"]
        if caller_type == "trusted":
            return Theme.TELEBEAM_TRUSTED
        elif caller_type == "unknown":
            return Theme.TELEBEAM_UNKNOWN
        elif caller_type == "spam":
            return Theme.TELEBEAM_SPAM
        elif caller_type == "emergency":
            return Theme.TELEBEAM_EMERGENCY
        return Theme.GRAY_MID

    def update(self):
        """Update animations"""
        self.breathing.update()
        self.pulse.update()

    def draw(self, surface: pygame.Surface, pos: tuple, privacy_mode: bool = False):
        """Draw caller card"""
        x, y = pos
        card_rect = pygame.Rect(x, y, self.width, self.height)

        color = self.get_color()
        breath_val = self.breathing.get_value()
        pulse_val = self.pulse.get_intensity()

        # Card background with glow
        glow_intensity = breath_val + (pulse_val * 0.5)
        draw_glow_rect(surface, card_rect, color,
                      glow_size=int(30 * glow_intensity),
                      alpha=Theme.ALPHA_VISIBLE)

        # Caller name
        if privacy_mode:
            name = "PRIVATE CALLER"
        else:
            name = self.caller_data["name"]

        name_font = Fonts.get(Fonts.HUGE, bold=True)
        name_y = y + 80
        draw_text_shadowed(surface, name,
                         (x + self.width // 2, name_y),
                         name_font, Theme.WHITE, shadow_offset=5, center=True)

        # Phone number
        if not privacy_mode:
            phone_font = Fonts.get(Fonts.MEDIUM)
            phone_y = name_y + 90
            draw_text_shadowed(surface, self.caller_data["phone"],
                             (x + self.width // 2, phone_y),
                             phone_font, Theme.GRAY_LIGHT, shadow_offset=3, center=True)

            # Reason/context
            reason_font = Fonts.get(Fonts.NORMAL)
            reason_y = phone_y + 70
            draw_text_shadowed(surface, self.caller_data["reason"],
                             (x + self.width // 2, reason_y),
                             reason_font, color, shadow_offset=3, center=True)

        # Trust indicator
        trust_y = y + 280
        self.draw_trust_indicator(surface, (x + self.width // 2, trust_y),
                                 self.caller_data["trust_score"], privacy_mode)

        # Action buttons
        buttons_y = y + self.height - 180
        self.draw_action_buttons(surface, (x, buttons_y))

    def draw_trust_indicator(self, surface: pygame.Surface, pos: tuple,
                            trust_score: float, privacy_mode: bool):
        """Draw trust level indicator"""
        if privacy_mode:
            return

        x, y = pos

        # Label
        label_font = Fonts.get(Fonts.SMALL)
        label = "Trust Level"
        draw_text_shadowed(surface, label, (x, y - 40),
                         label_font, Theme.GRAY_LIGHT, shadow_offset=2, center=True)

        # Trust bar
        bar_width = 400
        bar_height = 30
        bar_x = x - bar_width // 2
        bar_y = y

        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, Theme.BG_MID, bg_rect, border_radius=8)

        # Fill based on trust score
        fill_width = int(bar_width * trust_score)
        fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)

        # Color based on trust
        if trust_score >= 0.8:
            fill_color = Theme.TELEBEAM_TRUSTED
        elif trust_score >= 0.5:
            fill_color = Theme.TELEBEAM_UNKNOWN
        else:
            fill_color = Theme.TELEBEAM_SPAM

        pygame.draw.rect(surface, fill_color, fill_rect, border_radius=8)

        # Trust label
        if trust_score >= 0.8:
            trust_text = "KNOWN CONTACT"
        elif trust_score >= 0.5:
            trust_text = "UNKNOWN"
        else:
            trust_text = "LIKELY SPAM"

        trust_font = Fonts.get(Fonts.SMALL - 4, bold=True)
        draw_text_shadowed(surface, trust_text, (x, bar_y + bar_height + 30),
                         trust_font, fill_color, shadow_offset=2, center=True)

    def draw_action_buttons(self, surface: pygame.Surface, pos: tuple):
        """Draw Accept/Decline/Message buttons"""
        x, y = pos
        button_width = 250
        button_height = 80
        button_spacing = 60

        buttons = [
            ("ACCEPT", Theme.GREEN_SOFT, "accept"),
            ("MESSAGE", Theme.BLUE_SOFT, "message"),
            ("DECLINE", Theme.RED_SOFT, "decline")
        ]

        total_width = (button_width * 3) + (button_spacing * 2)
        start_x = x + (self.width - total_width) // 2

        for i, (label, color, button_id) in enumerate(buttons):
            button_x = start_x + (i * (button_width + button_spacing))
            button_rect = pygame.Rect(button_x, y, button_width, button_height)

            # Highlight if hovered
            alpha = Theme.ALPHA_VISIBLE
            glow_size = 15
            if self.hovered_button == button_id:
                alpha = Theme.ALPHA_SOLID
                glow_size = 25

            # Button background
            draw_glow_rect(surface, button_rect, color,
                         glow_size=glow_size, alpha=alpha)

            # Button label
            label_font = Fonts.get(Fonts.MEDIUM, bold=True)
            draw_text_shadowed(surface, label,
                             (button_rect.centerx, button_rect.centery - 10),
                             label_font, Theme.WHITE, shadow_offset=3, center=True)

            # Keyboard hint
            hint_font = Fonts.get(Fonts.SMALL - 8)
            hints = ["A", "M", "D"]
            hint_surf = hint_font.render(f"({hints[i]})", True, Theme.GRAY_DARK)
            hint_rect = hint_surf.get_rect(center=(button_rect.centerx,
                                                   button_rect.centery + 25))
            surface.blit(hint_surf, hint_rect)


class TeleBeamRealm(BaseRealm):
    """TeleBeam ambient telecommunications realm"""

    def __init__(self, display: pygame.Surface, incoming_call: bool = False):
        super().__init__(display, "TeleBeam")

        # State
        self.view_mode = "main"  # main, incoming, history
        self.incoming_call = incoming_call
        self.current_caller = None

        if incoming_call:
            # Start with random incoming call
            self.current_caller = random.choice(DEMO_CALLERS)
            self.view_mode = "incoming"

        # Call history (demo data)
        self.call_history = [
            {"caller": DEMO_CALLERS[1], "status": "answered", "time": "2 hours ago"},
            {"caller": DEMO_CALLERS[0], "status": "answered", "time": "Yesterday"},
            {"caller": DEMO_CALLERS[2], "status": "missed", "time": "2 days ago"},
            {"caller": DEMO_CALLERS[3], "status": "answered", "time": "3 days ago"},
        ]

        # Caller card for incoming calls
        self.caller_card = None
        if self.current_caller:
            card_width = 1200
            card_height = 700
            self.caller_card = CallerCard(card_width, card_height, self.current_caller)

        # Animations
        self.breathing = BreathingAnimation(0.7, 1.0, 0.02)

        # Ticker
        ticker_messages = [
            "TeleBeam: Ambient telecommunications for the living wall",
            "Never miss important calls again",
            "Visual caller ID from across the room",
            "PTSD-friendly, senior-friendly, hands-free"
        ]
        self.ticker = ScrollingTicker(self.width, ticker_messages, font_size=Fonts.NORMAL)

    def on_event(self, event: pygame.event.Event):
        """Handle realm-specific events"""
        if event.type == pygame.KEYDOWN:
            # View switching
            if event.key == pygame.K_h:
                self.view_mode = "history"
                self.current_caller = None
                self.caller_card = None

            elif event.key == pygame.K_m and self.view_mode == "main":
                self.view_mode = "main"
                self.current_caller = None
                self.caller_card = None

            # Incoming call actions
            if self.view_mode == "incoming" and self.caller_card:
                if event.key == pygame.K_a:
                    # Accept call
                    print(f"Accepting call from {self.current_caller['name']}")
                    self.running = False  # Exit to homescreen

                elif event.key == pygame.K_d:
                    # Decline call
                    print(f"Declining call from {self.current_caller['name']}")
                    self.view_mode = "main"
                    self.current_caller = None
                    self.caller_card = None

                elif event.key == pygame.K_m:
                    # Send message
                    print(f"Sending message to {self.current_caller['name']}")
                    self.view_mode = "main"
                    self.current_caller = None
                    self.caller_card = None

            # Simulate new incoming call
            if event.key == pygame.K_i and self.view_mode == "main":
                self.current_caller = random.choice(DEMO_CALLERS)
                card_width = 1200
                card_height = 700
                self.caller_card = CallerCard(card_width, card_height, self.current_caller)
                self.view_mode = "incoming"

    def update(self):
        """Update realm state"""
        self.breathing.update()
        self.ticker.update()

        if self.caller_card:
            self.caller_card.update()

    def draw(self):
        """Draw realm"""
        # Clear
        self.display.fill(Theme.BG_DEEP)

        # Draw based on view mode
        if self.view_mode == "incoming":
            self.draw_incoming_call()
        elif self.view_mode == "history":
            self.draw_call_history()
        else:
            self.draw_main()

        # Draw ticker
        ticker_y = self.height - 80
        self.ticker.draw(self.display, ticker_y)

        # Draw privacy overlay
        self.draw_privacy_overlay()

        # Draw help
        self.draw_help()

    def draw_main(self):
        """Draw main TeleBeam view"""
        # Title
        title_font = Fonts.get(Fonts.GIANT, bold=True)
        draw_text_shadowed(self.display, "TELEBEAM",
                         (self.width // 2, 120),
                         title_font, Theme.CYAN_SOFT, shadow_offset=6, center=True)

        # Subtitle
        subtitle_font = Fonts.get(Fonts.MEDIUM)
        draw_text_shadowed(self.display, "Ambient Telecommunications",
                         (self.width // 2, 220),
                         subtitle_font, Theme.GRAY_LIGHT, shadow_offset=3, center=True)

        # Status indicators
        status_y = 400
        self.draw_status_card("No Active Calls", Theme.BLUE_SOFT,
                            (self.width // 2, status_y))

        # Call history summary
        history_y = status_y + 180
        self.draw_history_summary(history_y)

        # Instructions
        instructions_y = self.height - 300
        instruction_font = Fonts.get(Fonts.NORMAL)
        instructions = [
            "Press I to simulate incoming call",
            "Press H to view call history"
        ]

        for i, text in enumerate(instructions):
            y = instructions_y + (i * 60)
            draw_text_shadowed(self.display, text,
                             (self.width // 2, y),
                             instruction_font, Theme.GRAY_MID, shadow_offset=2, center=True)

    def draw_incoming_call(self):
        """Draw incoming call screen"""
        if not self.caller_card:
            return

        # Title
        title_font = Fonts.get(Fonts.LARGE, bold=True)
        title_text = "INCOMING CALL"

        # Pulsing title
        breath_val = self.breathing.get_value()
        alpha = int(Theme.ALPHA_VISIBLE + (breath_val * 95))
        title_surf = title_font.render(title_text, True, Theme.CYAN_SOFT)
        title_rect = title_surf.get_rect(center=(self.width // 2, 80))

        # Title glow
        glow_surf = pygame.Surface((title_rect.width + 40, title_rect.height + 40),
                                   pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*Theme.CYAN_SOFT, alpha // 2),
                        (0, 0, glow_surf.get_width(), glow_surf.get_height()),
                        border_radius=15)
        self.display.blit(glow_surf, (title_rect.x - 20, title_rect.y - 20))
        self.display.blit(title_surf, title_rect)

        # Caller card (centered)
        card_x = (self.width - self.caller_card.width) // 2
        card_y = 180
        self.caller_card.draw(self.display, (card_x, card_y), self.privacy_mode)

    def draw_call_history(self):
        """Draw call history view"""
        # Title
        title_font = Fonts.get(Fonts.HUGE, bold=True)
        draw_text_shadowed(self.display, "CALL HISTORY",
                         (self.width // 2, 100),
                         title_font, Theme.BLUE_SOFT, shadow_offset=5, center=True)

        # History entries
        entry_height = 120
        start_y = 250

        for i, entry in enumerate(self.call_history[:6]):  # Show max 6
            y = start_y + (i * entry_height)
            self.draw_history_entry(entry, y, i)

    def draw_history_entry(self, entry: Dict, y: int, index: int):
        """Draw single call history entry"""
        caller = entry["caller"]
        status = entry["status"]
        time = entry["time"]

        # Entry background
        entry_width = 1400
        entry_height = 100
        entry_x = (self.width - entry_width) // 2
        entry_rect = pygame.Rect(entry_x, y, entry_width, entry_height)

        # Status color
        if status == "answered":
            status_color = Theme.GREEN_SOFT
        elif status == "missed":
            status_color = Theme.RED_SOFT
        else:
            status_color = Theme.GRAY_MID

        # Background
        bg_surf = pygame.Surface((entry_width, entry_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (*Theme.BG_MID, Theme.ALPHA_VISIBLE),
                        (0, 0, entry_width, entry_height), border_radius=12)
        self.display.blit(bg_surf, (entry_x, y))

        # Status indicator
        indicator_radius = 15
        indicator_x = entry_x + 40
        indicator_y = y + entry_height // 2
        pygame.draw.circle(self.display, status_color,
                         (indicator_x, indicator_y), indicator_radius)

        # Caller name
        if not self.privacy_mode:
            name_font = Fonts.get(Fonts.MEDIUM, bold=True)
            name_x = entry_x + 80
            name_y = y + 25
            draw_text_shadowed(self.display, caller["name"],
                             (name_x, name_y),
                             name_font, Theme.WHITE, shadow_offset=2)

            # Time
            time_font = Fonts.get(Fonts.SMALL)
            time_y = name_y + 45
            draw_text_shadowed(self.display, time,
                             (name_x, time_y),
                             time_font, Theme.GRAY_LIGHT, shadow_offset=2)

        # Status text (right side)
        status_font = Fonts.get(Fonts.SMALL, bold=True)
        status_text = status.upper()
        status_surf = status_font.render(status_text, True, status_color)
        status_rect = status_surf.get_rect(
            midright=(entry_x + entry_width - 40, y + entry_height // 2)
        )
        self.display.blit(status_surf, status_rect)

    def draw_status_card(self, message: str, color: tuple, pos: tuple):
        """Draw status card"""
        card_width = 800
        card_height = 120
        x = pos[0] - card_width // 2
        y = pos[1]

        card_rect = pygame.Rect(x, y, card_width, card_height)

        # Background with glow
        breath_val = self.breathing.get_value()
        draw_glow_rect(self.display, card_rect, color,
                      glow_size=int(20 * breath_val),
                      alpha=Theme.ALPHA_VISIBLE)

        # Message
        font = Fonts.get(Fonts.MEDIUM, bold=True)
        draw_text_shadowed(self.display, message,
                         (pos[0], y + card_height // 2 - 20),
                         font, Theme.WHITE, shadow_offset=3, center=True)

    def draw_history_summary(self, y: int):
        """Draw call history summary"""
        summary_font = Fonts.get(Fonts.NORMAL)

        # Count calls
        missed = sum(1 for entry in self.call_history if entry["status"] == "missed")
        answered = sum(1 for entry in self.call_history if entry["status"] == "answered")

        summary_text = f"Recent: {answered} answered  •  {missed} missed"

        draw_text_shadowed(self.display, summary_text,
                         (self.width // 2, y),
                         summary_font, Theme.GRAY_LIGHT, shadow_offset=2, center=True)

    def draw_help(self):
        """Draw control help"""
        help_font = Fonts.get(Fonts.SMALL - 4)

        if self.view_mode == "incoming":
            help_text = "A:Accept  M:Message  D:Decline  P:Privacy  ESC:Exit"
        else:
            help_text = "I:Simulate Call  H:History  P:Privacy  ESC:Exit"

        help_surf = help_font.render(help_text, True, Theme.GRAY_DARK)
        help_rect = help_surf.get_rect(center=(self.width // 2, 20))
        self.display.blit(help_surf, help_rect)
