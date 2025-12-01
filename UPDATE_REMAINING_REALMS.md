# Template for Updating Remaining Realms

This guide shows how to update each remaining realm (Clinical, Transport, Emergency, Security, Enterprise, Aviation, Maritime) with the unified control system.

## Standard Pattern

Each realm needs these updates:

### 1. Import global_state
```python
from core.global_state import global_state
```

### 2. Change duration to 60 seconds
```python
def run(self, duration=60):
```

### 3. Add view state variables
```python
# View state (manual control with LEFT/RIGHT)
current_view = 0
num_views = 3  # or 4, depending on realm

# Event state (triggered by SPACE)
show_event = False
event_time = 0
event_text = ""
```

### 4. Update event handling
```python
while time.time() - start_time < duration:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return

            # LEFT/RIGHT to cycle views
            elif event.key == pygame.K_LEFT:
                current_view = (current_view - 1) % num_views
            elif event.key == pygame.K_RIGHT:
                current_view = (current_view + 1) % num_views

            # SPACE to trigger realm-specific event
            elif event.key == pygame.K_SPACE:
                show_event = True
                event_time = time.time()
                event_text = "🚨 [Realm-specific event message]"

    elapsed = time.time() - start_time

    # Hide event after 3 seconds
    if show_event and (time.time() - event_time > 3):
        show_event = False

    # Get mode configuration
    mode_config = global_state.get_mode_config()
```

### 5. Add mode-aware circles (if realm has them)
```python
# Position circles away from text areas
circles = [
    {"x": w * 0.10, "y": h * 0.25, "r": 80, "dr": 0.2, "base": 80},
    {"x": w * 0.90, "y": h * 0.60, "r": 100, "dr": -0.15, "base": 100},
]

# Later in render loop:
for c in circles:
    # Update radius with mode speed multiplier
    speed = c["dr"] * mode_config['circle_speed_multiplier']
    c["r"] += speed
    if c["r"] > c["base"] + 15 or c["r"] < c["base"] - 15:
        c["dr"] *= -1

    # Draw with mode-dimmed alpha
    radius = int(c["r"])
    x, y = int(c["x"]), int(c["y"])
    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    glow_alpha = int(20 * mode_config['circle_alpha_multiplier'])
    pygame.draw.circle(s, (*accent_color, glow_alpha), (radius, radius), radius)

    stroke_alpha = int(100 * mode_config['circle_alpha_multiplier'])
    pygame.draw.circle(s, (*accent_color, stroke_alpha), (radius, radius), radius, 3)

    self.screen.blit(s, (x - radius, y - radius), special_flags=pygame.BLEND_ADD)
```

### 6. Add event notification display
```python
# Event notification (before footer)
if show_event:
    event_y = h - 180
    event_surf = pygame.Surface((w - 200, 80), pygame.SRCALPHA)
    pygame.draw.rect(event_surf, (0, 0, 0, 180), (0, 0, w - 200, 80), border_radius=10)
    pygame.draw.rect(event_surf, accent_color, (0, 0, w - 200, 80), 3, border_radius=10)
    self.screen.blit(event_surf, (100, event_y))

    event_text_surf = fonts['body'].render(event_text, True, (255, 255, 255))
    event_text_rect = event_text_surf.get_rect(center=(w // 2, event_y + 40))
    self.screen.blit(event_text_surf, event_text_rect)
```

### 7. Replace footer with standard controls
```python
# Bottom footer with controls
footer_y = h - 90
mode_text = f"Mode: {global_state.mode}"
mode_surf = fonts['small'].render(mode_text, True, accent_color)
self.screen.blit(mode_surf, (50, footer_y))

view_text = f"View {current_view + 1}/{num_views}"
view_surf = fonts['small'].render(view_text, True, (180, 190, 210))
view_rect = view_surf.get_rect(center=(w // 2, footer_y))
self.screen.blit(view_surf, view_rect)

controls_text = "← → : Views · SPACE: Event · ESC: Exit"
controls_surf = fonts['small'].render(controls_text, True, (180, 190, 210))
controls_rect = controls_surf.get_rect(right=w - 50, centery=footer_y)
self.screen.blit(controls_surf, controls_rect)
```

## Realm-Specific Event Messages

- **Clinical**: "🏥 Patient vitals logged"
- **Transport**: "🚗 Lane assist activated"
- **Emergency**: "🚨 Unit dispatched to location"
- **Security**: "🛡️ Perimeter scan complete"
- **Enterprise**: "📊 Meeting scheduled"
- **Aviation**: "✈️ Altitude adjusted"
- **Maritime**: "⚓ Course correction applied"

## Circle Positioning Guidelines

- **Clinical**: Corners and edges (avoid center vitals display)
- **Transport**: Minimal/none (HUD style, keep glass clear)
- **Emergency**: Edges only (don't cover command info)
- **Security**: Behind camera feeds
- **Enterprise**: Subtle, behind content
- **Aviation**: Corners (avoid airspace display)
- **Maritime**: Behind vessel info

## Mode Behavior

- **NORMAL**: Full animations, bright colors
- **STUDY**: Dimmed (0.5-0.7 alpha), slower animations
- **SLEEP**: Very dim (0.2-0.3 alpha), minimal animation or hidden circles

### Special: Education Realm
- Circles ONLY visible in NORMAL mode
- STUDY/SLEEP modes: no circles at all (pure focus on concept)
