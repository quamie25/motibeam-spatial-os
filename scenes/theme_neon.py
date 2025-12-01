"""
MotiBeam Spatial OS - Neon HUD Theme
Unified visual theme for all realms (consumer + ops)
"""

import pygame
import math

# ============================================================================
# COLOR PALETTE
# ============================================================================

COLOR_BG = (15, 20, 35)  # Dark bluish background
COLOR_TEXT_PRIMARY = (255, 255, 255)  # White
COLOR_TEXT_SECONDARY = (180, 190, 210)  # Light gray-blue
COLOR_ACCENT_CYAN = (100, 200, 255)  # Cyan/teal HUD accent
COLOR_ACCENT_GREEN = (100, 255, 150)  # Success/positive
COLOR_ACCENT_ORANGE = (255, 180, 80)  # Warning
COLOR_ACCENT_RED = (255, 100, 100)  # Critical/alert

# Realm-specific accent colors
REALM_COLORS = {
    'home': (100, 200, 255),      # Cyan
    'clinical': (100, 255, 200),   # Mint green
    'education': (150, 150, 255),  # Light purple
    'transport': (100, 180, 255),  # Sky blue
    'emergency': (255, 100, 100),  # Red alert
    'security': (150, 100, 255),   # Purple
    'enterprise': (100, 180, 255), # Corporate blue
    'aviation': (100, 200, 255),   # Cyan
    'maritime': (100, 220, 255),   # Aqua
}

# ASCII fallback symbols (no emoji)
REALM_SYMBOLS = {
    'home': '[H]',
    'clinical': '[+]',
    'education': '[E]',
    'transport': '[T]',
    'emergency': '[!]',
    'security': '[S]',
    'enterprise': '[B]',
    'aviation': '[A]',
    'maritime': '[M]',
}

# ============================================================================
# FONT HELPERS
# ============================================================================

def get_fonts(screen):
    """
    Get scaled fonts for consistent HUD rendering
    Returns dict with: mega, huge, title, subtitle, body, small
    """
    try:
        return {
            'mega': pygame.font.Font(None, 120),
            'huge': pygame.font.Font(None, 84),
            'title': pygame.font.Font(None, 64),
            'subtitle': pygame.font.Font(None, 48),
            'body': pygame.font.Font(None, 36),
            'small': pygame.font.Font(None, 28),
        }
    except:
        return {
            'mega': pygame.font.SysFont('arial', 120, bold=True),
            'huge': pygame.font.SysFont('arial', 84, bold=True),
            'title': pygame.font.SysFont('arial', 64, bold=True),
            'subtitle': pygame.font.SysFont('arial', 48),
            'body': pygame.font.SysFont('arial', 36),
            'small': pygame.font.SysFont('arial', 28),
        }

# ============================================================================
# DRAWING FUNCTIONS
# ============================================================================

def draw_background(screen, elapsed=0):
    """
    Draw animated neon background with soft overlapping glow circles
    """
    screen.fill(COLOR_BG)

    w, h = screen.get_size()

    # Create animated glow circles
    circles = [
        # x, y, base_radius, speed, color
        (0.2, 0.3, 200, 0.3, (0, 100, 150, 20)),
        (0.8, 0.2, 250, 0.5, (0, 150, 200, 15)),
        (0.5, 0.7, 300, 0.4, (50, 100, 180, 18)),
        (0.9, 0.8, 180, 0.6, (0, 120, 180, 22)),
    ]

    for cx, cy, base_r, speed, color in circles:
        # Animate radius
        radius = base_r + int(30 * math.sin(elapsed * speed))
        x = int(cx * w)
        y = int(cy * h)

        # Draw glow circle (transparent)
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (radius, radius), radius)
        screen.blit(s, (x - radius, y - radius), special_flags=pygame.BLEND_ADD)

def draw_header(screen, fonts, realm_id, title, subtitle, accent_color, status_text="● LIVE"):
    """
    Draw top header bar with:
    - Top-left: [Symbol] TITLE
    - Below: Subtitle
    - Top-right: Status indicator (● LIVE / ● ACTIVE / etc)
    """
    w, h = screen.get_size()

    # Get realm symbol
    symbol = REALM_SYMBOLS.get(realm_id, '[?]')

    # Title (top-left)
    title_text = f"{symbol} {title}"
    title_surf = fonts['huge'].render(title_text, True, COLOR_TEXT_PRIMARY)
    screen.blit(title_surf, (50, 40))

    # Subtitle (below title)
    subtitle_surf = fonts['subtitle'].render(subtitle, True, accent_color)
    screen.blit(subtitle_surf, (50, 130))

    # Status indicator (top-right) with pulsing effect
    status_surf = fonts['body'].render(status_text, True, accent_color)
    status_w = status_surf.get_width()
    screen.blit(status_surf, (w - status_w - 50, 50))

def draw_footer(screen, fonts, mode_label, seconds_remaining, realm_id, accent_color):
    """
    Draw bottom footer bar with:
    - Left: Mode label (e.g., "Consumer Mode" / "Ops Mode")
    - Center: Realm ID
    - Right: Time remaining
    """
    w, h = screen.get_size()
    y = h - 70

    # Left: Mode label
    mode_surf = fonts['small'].render(mode_label, True, accent_color)
    screen.blit(mode_surf, (50, y))

    # Center: Realm tag
    realm_surf = fonts['small'].render(f"[{realm_id.upper()}]", True, COLOR_TEXT_SECONDARY)
    realm_w = realm_surf.get_width()
    screen.blit(realm_surf, ((w - realm_w) // 2, y))

    # Right: Time remaining
    time_text = f"{seconds_remaining}s remaining"
    time_surf = fonts['small'].render(time_text, True, accent_color)
    time_w = time_surf.get_width()
    screen.blit(time_surf, (w - time_w - 50, y))

def draw_content_box(screen, fonts, title, items, y_start, accent_color, glow=True):
    """
    Draw a rounded content box with title and bullet items

    Args:
        screen: pygame screen
        fonts: font dict
        title: Section title (e.g., "MORNING ROUTINE")
        items: List of bullet point strings
        y_start: Y position to start drawing
        accent_color: Color for title and accents
        glow: Whether to draw glow effect
    """
    w, h = screen.get_size()

    # Draw glow border if enabled
    if glow:
        border_rect = pygame.Rect(40, y_start - 10, w - 80, 60 + len(items) * 45)
        glow_surf = pygame.Surface((border_rect.w, border_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*accent_color, 30), (0, 0, border_rect.w, border_rect.h), border_radius=10)
        screen.blit(glow_surf, (border_rect.x, border_rect.y))
        pygame.draw.rect(screen, accent_color, border_rect, 2, border_radius=10)

    # Title
    title_surf = fonts['body'].render(title, True, accent_color)
    screen.blit(title_surf, (60, y_start))

    # Items
    y = y_start + 50
    for item in items:
        item_surf = fonts['small'].render(item, True, COLOR_TEXT_PRIMARY)
        screen.blit(item_surf, (80, y))
        y += 45

def draw_live_indicator(screen, elapsed, x, y, color):
    """
    Draw a pulsing live indicator dot
    """
    # Pulse effect
    alpha = int(128 + 127 * math.sin(elapsed * 3))
    radius = 8 + int(3 * math.sin(elapsed * 3))

    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (*color, alpha), (radius, radius), radius)
    screen.blit(s, (x - radius, y - radius), special_flags=pygame.BLEND_ADD)

# ============================================================================
# COMPLETE HUD RENDERING
# ============================================================================

def render_realm_hud(screen, realm_id, title, subtitle, mode, content_sections, elapsed, duration, accent_color=None):
    """
    Render complete realm HUD with animated background, header, content, footer

    Args:
        screen: pygame screen
        realm_id: Realm identifier (e.g., 'home', 'emergency')
        title: Main realm title
        subtitle: Subtitle description
        mode: "Consumer Mode" or "Ops Mode"
        content_sections: List of dicts with 'title' and 'items' keys
        elapsed: Elapsed time
        duration: Total duration
        accent_color: Override accent color (optional)
    """
    if accent_color is None:
        accent_color = REALM_COLORS.get(realm_id, COLOR_ACCENT_CYAN)

    fonts = get_fonts(screen)

    # Background
    draw_background(screen, elapsed)

    # Header
    status_text = "● LIVE" if mode == "Consumer Mode" else "● ACTIVE"
    draw_header(screen, fonts, realm_id, title, subtitle, accent_color, status_text)

    # Content sections (rotating based on time)
    y_start = 250
    num_sections = len(content_sections)
    if num_sections > 0:
        section_duration = duration / num_sections
        current_section = min(int(elapsed / section_duration), num_sections - 1)
        section = content_sections[current_section]
        draw_content_box(
            screen, fonts,
            section['title'],
            section['items'],
            y_start,
            accent_color,
            glow=True
        )

    # Footer
    seconds_remaining = int(duration - elapsed)
    draw_footer(screen, fonts, mode, seconds_remaining, realm_id, accent_color)

    pygame.display.flip()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_realm_accent_color(realm_id):
    """Get the accent color for a specific realm"""
    return REALM_COLORS.get(realm_id, COLOR_ACCENT_CYAN)

def get_realm_symbol(realm_id):
    """Get the ASCII symbol for a specific realm"""
    return REALM_SYMBOLS.get(realm_id, '[?]')
