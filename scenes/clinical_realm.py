#!/usr/bin/env python3
"""
Clinical Realm - Health & Wellness
Simple stub for testing
"""

import pygame
import sys


def run(screen, width, height):
    """
    Run the Clinical realm
    Press ESC to return to launcher
    """
    # Colors
    BG_COLOR = (20, 30, 40)
    TEXT_COLOR = (200, 220, 240)
    ACCENT_COLOR = (100, 160, 130)

    # Fonts
    font_title = pygame.font.SysFont('Arial', 72, bold=True)
    font_body = pygame.font.SysFont('Arial', 36)
    font_instruction = pygame.font.SysFont('Arial', 28)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN:
                # ESC to return to launcher
                if event.key == pygame.K_ESCAPE:
                    return

        # Draw
        screen.fill(BG_COLOR)

        # Title
        title_surf = font_title.render("Clinical Realm", True, ACCENT_COLOR)
        title_x = (width - title_surf.get_width()) // 2
        screen.blit(title_surf, (title_x, 100))

        # Subtitle
        subtitle_surf = font_body.render("Health & Wellness Hub", True, TEXT_COLOR)
        subtitle_x = (width - subtitle_surf.get_width()) // 2
        screen.blit(subtitle_surf, (subtitle_x, 200))

        # Content placeholder
        content_lines = [
            "🧠 Mind",
            "💪 Body",
            "✨ Spirit",
            "",
            "This is a placeholder realm.",
            "Full implementation coming soon."
        ]

        y_offset = 320
        for line in content_lines:
            line_surf = font_body.render(line, True, TEXT_COLOR)
            line_x = (width - line_surf.get_width()) // 2
            screen.blit(line_surf, (line_x, y_offset))
            y_offset += 60

        # Instructions at bottom
        instruction_surf = font_instruction.render(
            "Press ESC to return to launcher",
            True,
            (140, 160, 180)
        )
        instruction_x = (width - instruction_surf.get_width()) // 2
        screen.blit(instruction_surf, (instruction_x, height - 80))

        pygame.display.flip()
        clock.tick(60)


# Alternative class-based approach (both work)
class Realm:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

    def run(self):
        run(self.screen, self.width, self.height)
