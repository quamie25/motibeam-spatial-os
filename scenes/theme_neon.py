"""
MotiBeam Spatial OS - Neon HUD Theme
Unified visual theme for all realms (consumer + ops)
"""

import pygame
import math
import os
from core.global_state import get_emoji_font

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

# Realm symbols with emoji and ASCII fallbacks
REALM_SYMBOLS = {
    'home': {'emoji': '🏡', 'fallback': '[H]'},
    'clinical': {'emoji': '⚕️', 'fallback': '[+]'},
    'education': {'emoji': '📚', 'fallback': '[E]'},
    'transport': {'emoji': '🚗', 'fallback': '[T]'},
    'emergency': {'emoji': '🚨', 'fallback': '[!]'},
    'security': {'emoji': '🛡️', 'fallback': '[S]'},
    'enterprise': {'emoji': '🏢', 'fallback': '[B]'},
    'aviation': {'emoji': '✈️', 'fallback': '[A]'},
    'maritime': {'emoji': '⚓', 'fallback': '[M]'},
}

# ============================================================================
# EMOJI FONT LOADING
# ============================================================================

# Global emoji font cache
_EMOJI_FONT = None
_EMOJI_FONT_AVAILABLE = False

def load_emoji_font(size=72):
    """
    Load NotoColorEmoji font for proper emoji rendering
    Returns: (font, is_emoji_font) tuple
    """
    global _EMOJI_FONT, _EMOJI_FONT_AVAILABLE

    # Try to load emoji font
    emoji_font_paths = [
        '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',
        '/usr/share/fonts/truetype/noto-emoji/NotoColorEmoji.ttf',
        '/usr/share/fonts/google-noto-emoji/NotoColorEmoji.ttf',
    ]

    for font_path in emoji_font_paths:
        if os.path.exists(font_path):
            try:
                _EMOJI_FONT = pygame.font.Font(font_path, size)
                _EMOJI_FONT_AVAILABLE = True
                print(f"✓ Emoji font loaded: {font_path}")
                return _EMOJI_FONT, True
            except Exception as e:
                print(f"✗ Failed to load emoji font {font_path}: {e}")
                pass

    # Fallback to default font
    print("⚠ Emoji font not available, using ASCII fallbacks")
    try:
        _EMOJI_FONT = pygame.font.Font(None, size)
        _EMOJI_FONT_AVAILABLE = False
        return _EMOJI_FONT, False
    except:
        _EMOJI_FONT = pygame.font.SysFont('arial', size)
        _EMOJI_FONT_AVAILABLE = False
        return _EMOJI_FONT, False

def render_icon(realm_id, size=72, color=(255, 255, 255)):
    """
    Render realm icon with emoji font support
    Returns pygame surface with the icon
    """
    symbol_data = REALM_SYMBOLS.get(realm_id, {'emoji': '?', 'fallback': '[?]'})

    # Use centralized emoji font
    emoji_font = get_emoji_font(size)
    return emoji_font.render(symbol_data['emoji'], True, color)

# ============================================================================
# FONT HELPERS
# ============================================================================

def get_fonts(screen):
    """
    Get scaled fonts for wall-readable HUD (optimized for 8-10 feet viewing)
    Returns dict with: mega, huge, title, subtitle, header, body, small
    """
    try:
        return {
            'mega': pygame.font.Font(None, 180),      # Extra large numbers/stats
            'huge': pygame.font.Font(None, 120),      # Realm title (was 84)
            'title': pygame.font.Font(None, 80),      # Major section titles (was 64)
            'subtitle': pygame.font.Font(None, 56),   # Subtitle (was 48)
            'header': pygame.font.Font(None, 68),     # Section headers (30-34 → 68)
            'body': pygame.font.Font(None, 48),       # Body text (was 36, now 48 for 22-24px equivalent)
            'small': pygame.font.Font(None, 36),      # Small text (was 28)
        }
    except:
        return {
            'mega': pygame.font.SysFont('arial', 180, bold=True),
            'huge': pygame.font.SysFont('arial', 120, bold=True),
            'title': pygame.font.SysFont('arial', 80, bold=True),
            'subtitle': pygame.font.SysFont('arial', 56),
            'header': pygame.font.SysFont('arial', 68, bold=True),
            'body': pygame.font.SysFont('arial', 48),
            'small': pygame.font.SysFont('arial', 36),
        }

# ============================================================================
# DRAWING FUNCTIONS
# ============================================================================

def draw_background(screen, elapsed=0):
    """
    Draw animated neon background with slow parallax drifting glow circles
    Living wall motion - subtle and continuous
    """
    screen.fill(COLOR_BG)

    w, h = screen.get_size()

    # Slow drifting glow circles with parallax motion
    circles = [
        # x, y, base_radius, speed, drift_x, drift_y, color (lower opacity for readability)
        (0.2, 0.3, 200, 0.15, 0.02, 0.01, (0, 100, 150, 12)),
        (0.8, 0.2, 250, 0.20, -0.015, 0.02, (0, 150, 200, 10)),
        (0.5, 0.7, 300, 0.18, 0.01, -0.015, (50, 100, 180, 11)),
        (0.9, 0.8, 180, 0.25, -0.02, -0.01, (0, 120, 180, 13)),
        (0.1, 0.9, 220, 0.22, 0.018, 0.012, (80, 100, 200, 9)),
    ]

    for base_cx, base_cy, base_r, speed, drift_x, drift_y, color in circles:
        # Subtle breathing animation
        radius = base_r + int(20 * math.sin(elapsed * speed))

        # Parallax drift (very slow)
        cx = base_cx + drift_x * math.sin(elapsed * 0.1)
        cy = base_cy + drift_y * math.cos(elapsed * 0.15)

        x = int(cx * w)
        y = int(cy * h)

        # Draw glow circle (transparent, lower opacity)
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (radius, radius), radius)
        screen.blit(s, (x - radius, y - radius), special_flags=pygame.BLEND_ADD)

def draw_header(screen, fonts, realm_id, title, subtitle, accent_color, status_text="● LIVE"):
    """
    Draw top header bar with:
    - Top-left: Icon TITLE
    - Below: Subtitle
    - Top-right: Status indicator (● LIVE / ● ACTIVE / etc)

    Note: Title should include emoji (e.g., "🏡 HOME REALM")
    This function will render the entire title with proper emoji support
    """
    w, h = screen.get_size()

    # Split title into emoji and text for proper rendering
    # Titles like "🏡 HOME REALM" will be split
    if len(title) > 2 and title[0] in '🏡⚕📚🚗🚨🛡🏢✈⚓🩺️':
        emoji = title[0]
        text_part = title[1:].strip()

        # Render emoji with emoji font
        emoji_font = get_emoji_font(80)
        icon_surf = emoji_font.render(emoji, True, accent_color)
        screen.blit(icon_surf, (50, 35))

        # Render text part
        icon_width = icon_surf.get_width()
        title_surf = fonts['huge'].render(text_part, True, COLOR_TEXT_PRIMARY)
        screen.blit(title_surf, (50 + icon_width + 20, 40))
    else:
        # No emoji, just render title
        title_surf = fonts['huge'].render(title, True, COLOR_TEXT_PRIMARY)
        screen.blit(title_surf, (50, 40))

    # Subtitle (below title)
    subtitle_surf = fonts['subtitle'].render(subtitle, True, accent_color)
    screen.blit(subtitle_surf, (50, 130))

    # Status indicator (top-right) with pulsing effect
    status_surf = fonts['body'].render(status_text, True, accent_color)
    status_w = status_surf.get_width()
    screen.blit(status_surf, (w - status_w - 50, 50))

def draw_footer_ticker(screen, fonts, mode_label, seconds_remaining, realm_id, accent_color, ticker_text="", elapsed=0):
    """
    Draw bottom footer bar with scrolling ticker:
    - Top line: Mode label (left), realm ID (center), time (right)
    - Bottom line: Scrolling ticker with live updates
    """
    w, h = screen.get_size()
    footer_y = h - 100  # Start higher to fit two lines

    # Top line - status bar
    mode_surf = fonts['small'].render(mode_label, True, accent_color)
    screen.blit(mode_surf, (50, footer_y))

    realm_surf = fonts['small'].render(f"[{realm_id.upper()}]", True, COLOR_TEXT_SECONDARY)
    realm_w = realm_surf.get_width()
    screen.blit(realm_surf, ((w - realm_w) // 2, footer_y))

    time_text = f"{seconds_remaining}s remaining"
    time_surf = fonts['small'].render(time_text, True, accent_color)
    time_w = time_surf.get_width()
    screen.blit(time_surf, (w - time_w - 50, footer_y))

    # Bottom line - scrolling ticker
    if ticker_text:
        ticker_y = footer_y + 45
        # Draw semi-transparent background bar
        ticker_bg = pygame.Surface((w, 50), pygame.SRCALPHA)
        pygame.draw.rect(ticker_bg, (0, 0, 0, 80), (0, 0, w, 50))
        screen.blit(ticker_bg, (0, ticker_y - 5))

        # Render ticker text
        ticker_surf = fonts['small'].render(ticker_text, True, COLOR_TEXT_SECONDARY)
        ticker_w = ticker_surf.get_width()

        # Scroll effect (moves right to left)
        scroll_speed = 120  # pixels per second
        offset = int(elapsed * scroll_speed) % (ticker_w + w)
        x_pos = w - offset

        screen.blit(ticker_surf, (x_pos, ticker_y))

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

def draw_two_column_layout(screen, fonts, left_section, right_section, y_start, accent_color):
    """
    Draw full-width two-column layout for maximum screen usage

    Args:
        left_section: {'title': str, 'items': [str]}
        right_section: {'title': str, 'items': [str]}
        y_start: Y position to start
        accent_color: Accent color
    """
    w, h = screen.get_size()
    margin = 80  # Outer margins
    col_spacing = 60  # Space between columns
    col_width = (w - 2 * margin - col_spacing) // 2

    # Left column
    left_x = margin
    title_surf = fonts['header'].render(left_section['title'], True, accent_color)
    screen.blit(title_surf, (left_x, y_start))

    y = y_start + 85
    for item in left_section['items']:
        item_surf = fonts['body'].render(item, True, COLOR_TEXT_PRIMARY)
        screen.blit(item_surf, (left_x + 20, y))
        y += 60  # Increased line spacing for wall readability

    # Right column
    right_x = margin + col_width + col_spacing
    title_surf = fonts['header'].render(right_section['title'], True, accent_color)
    screen.blit(title_surf, (right_x, y_start))

    y = y_start + 85
    for item in right_section['items']:
        item_surf = fonts['body'].render(item, True, COLOR_TEXT_PRIMARY)
        screen.blit(item_surf, (right_x + 20, y))
        y += 60

def draw_full_width_content(screen, fonts, title, items, y_start, accent_color):
    """
    Draw full-width content section (85-90% of screen width)

    Args:
        screen: pygame screen
        fonts: font dict
        title: Section title
        items: List of content items
        y_start: Y position
        accent_color: Accent color
    """
    w, h = screen.get_size()
    margin = int(w * 0.07)  # 7% margins = 86% content width

    # Title
    title_surf = fonts['header'].render(title, True, accent_color)
    screen.blit(title_surf, (margin, y_start))

    # Items with increased line spacing
    y = y_start + 85
    for item in items:
        item_surf = fonts['body'].render(item, True, COLOR_TEXT_PRIMARY)
        screen.blit(item_surf, (margin + 20, y))
        y += 60  # Increased from 45 for better readability

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
    draw_footer_ticker(screen, fonts, mode, seconds_remaining, realm_id, accent_color, "", elapsed)

    pygame.display.flip()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_realm_accent_color(realm_id):
    """Get the accent color for a specific realm"""
    return REALM_COLORS.get(realm_id, COLOR_ACCENT_CYAN)

def get_realm_symbol(realm_id, prefer_emoji=True):
    """
    Get the symbol for a specific realm
    Args:
        realm_id: Realm identifier
        prefer_emoji: If True, return emoji; if False, return ASCII fallback
    Returns:
        Symbol string
    """
    symbol_data = REALM_SYMBOLS.get(realm_id, {'emoji': '?', 'fallback': '[?]'})

    if prefer_emoji and _EMOJI_FONT_AVAILABLE:
        return symbol_data['emoji']
    else:
        return symbol_data['fallback']
