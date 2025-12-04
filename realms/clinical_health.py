"""
MotiBeam Spatial OS - Clinical Mental Wellness & PTSD Support App
⚕️ Realm #2 - Mental wellness, PTSD support, and holistic health

Designed for: Elderly, veterans, caregivers
Focus: MIND first (mood, breathing, grounding), then BODY (simple reminders), then SPIRIT

Features:
- Mood check-in (1-10 scale)
- Guided breathing sessions
- Grounding techniques (5-4-3-2-1 method for PTSD)
- "Calm Mode" with ambient breathing visuals
- Rotating affirmations
- Simple medication/water/sleep reminders
- Daily encouragement messages
"""

import random
import math
from typing import List, Tuple
from datetime import datetime

# Import base realm (which already imports pygame)
from realms.base_realm import BaseRealm
import pygame


class ClinicalHealthPro(BaseRealm):
    """Mental Wellness & PTSD Support Realm"""

    def __init__(self):
        super().__init__(
            realm_id=2,
            realm_name="MENTAL WELLNESS & SUPPORT",
            realm_color=(100, 180, 255)  # Calming blue
        )

        # Current view mode - START with MIND (not dashboard)
        self.view_mode = "MIND"  # MIND, BODY, SPIRIT, CALM_MODE

        # MIND - Mental wellness state
        self.mood_level = 5  # 1-10 scale, default neutral
        self.mood_just_set = False
        self.breathing_active = False
        self.breathing_phase = "inhale"  # inhale, hold, exhale
        self.breathing_timer = 0.0
        self.breathing_duration = {"inhale": 4.0, "hold": 7.0, "exhale": 8.0}

        # Affirmations - rotate through these
        self.affirmations = [
            "You are safe right now",
            "This moment is all that matters",
            "You are strong and resilient",
            "Peace is available to you",
            "You have survived 100% of your worst days",
            "Progress, not perfection",
            "You are doing your best",
            "Breathe. You are here. You are okay.",
            "One moment at a time",
            "You deserve peace and calm",
        ]
        self.current_affirmation_index = 0
        self.affirmation_change_timer = 0.0

        # Grounding technique state (5-4-3-2-1 method)
        self.grounding_active = False
        self.grounding_step = 0  # 0-4 for the 5 steps
        self.grounding_prompts = [
            "Name 5 things you can SEE around you",
            "Name 4 things you can TOUCH right now",
            "Name 3 things you can HEAR at this moment",
            "Name 2 things you can SMELL nearby",
            "Name 1 thing you can TASTE",
        ]

        # BODY - Simple wellness reminders (non-medical)
        self.water_intake = 4  # Glasses today
        self.water_goal = 8
        self.medication_reminders = [
            {"time": "08:00", "name": "Morning medication", "taken": True},
            {"time": "12:00", "name": "Afternoon medication", "taken": False},
            {"time": "20:00", "name": "Evening medication", "taken": False},
        ]
        self.sleep_reminder = "Bedtime routine at 22:00"
        self.activity_minutes = 15  # Simple step count
        self.activity_goal = 30

        # SPIRIT - Emotional support
        self.daily_encouragement = [
            "Today is a new beginning. You've got this.",
            "Your presence matters. You make a difference.",
            "Be gentle with yourself. Healing takes time.",
            "You are worthy of peace and happiness.",
            "Every small step forward is progress.",
        ]
        self.current_encouragement = random.choice(self.daily_encouragement)
        self.gratitude_prompt = "What are you grateful for today?"
        self.gratitude_items = []  # User can add mentally

        # Calm Mode particles
        self.calm_particles: List[dict] = []
        self.calm_particle_timer = 0.0

        # Veteran-specific support flags
        self.ptsd_support_active = True  # Always available
        self.hypervigilance_check_timer = 0.0

        print("🧠 Mental Wellness & PTSD Support Realm initialized")
        print("   Default view: MIND (mood check-in)")
        print("   Press SPACE for Calm Mode | G for Grounding")

    def update(self, dt: float):
        """Update mental wellness system"""

        # Update affirmation rotation (every 10 seconds)
        self.affirmation_change_timer += dt
        if self.affirmation_change_timer > 10.0:
            self.affirmation_change_timer = 0.0
            self.current_affirmation_index = (self.current_affirmation_index + 1) % len(self.affirmations)

        # Update breathing animation in Calm Mode
        if self.view_mode == "CALM_MODE":
            self.update_breathing(dt)

            # Spawn calm particles
            self.calm_particle_timer += dt
            if self.calm_particle_timer > 0.05:
                self.calm_particle_timer = 0.0
                self.spawn_calm_particle()

            # Update particles
            for particle in self.calm_particles[:]:
                particle['y'] -= particle['vy'] * dt
                particle['x'] += math.sin(particle['y'] * 0.01 + particle['offset']) * dt * 20
                particle['life'] -= dt * 0.3

                if particle['life'] <= 0 or particle['y'] < 0:
                    self.calm_particles.remove(particle)

    def update_breathing(self, dt: float):
        """Update breathing exercise timer"""
        self.breathing_timer += dt

        # Cycle through breathing phases
        phase_duration = self.breathing_duration[self.breathing_phase]

        if self.breathing_timer >= phase_duration:
            self.breathing_timer = 0.0

            # Move to next phase
            if self.breathing_phase == "inhale":
                self.breathing_phase = "hold"
            elif self.breathing_phase == "hold":
                self.breathing_phase = "exhale"
            elif self.breathing_phase == "exhale":
                self.breathing_phase = "inhale"

    def render(self):
        """Render mental wellness interface"""
        # Background
        self.screen.fill(self.theme.BG_DEEP)

        # Header with view mode indicator
        self.draw_header(f"MENTAL WELLNESS - {self.view_mode}", "You are safe. You are supported.")

        # Render based on current view mode
        if self.view_mode == "MIND":
            self.render_mind_view()
        elif self.view_mode == "BODY":
            self.render_body_view()
        elif self.view_mode == "SPIRIT":
            self.render_spirit_view()
        elif self.view_mode == "CALM_MODE":
            self.render_calm_mode()

        # Footer with navigation
        if self.view_mode == "CALM_MODE":
            controls = "ESC: Exit Calm Mode  │  SPACE: Return to MIND"
        else:
            controls = "ESC: Exit  │  M: Mind  │  B: Body  │  S: Spirit  │  SPACE: Calm Mode  │  G: Grounding  │  C: Caregiver"
        self.draw_footer(controls)

    def render_mind_view(self):
        """Render MIND view - mood check-in, breathing, grounding"""
        y_start = 280

        # Show grounding technique if active
        if self.grounding_active:
            self.render_grounding_technique(y_start)
            return

        # Section title
        self.ui.draw_text_with_shadow(
            self.screen, "MIND - Mental Well-Being", self.font_large,
            (self.width // 2, y_start), (100, 180, 255), 3, True
        )

        # Rotating affirmation at top
        affirmation_y = y_start + 80
        current_affirmation = self.affirmations[self.current_affirmation_index]
        pulse = self.anim.breathe(self.time, 3.0)
        affirmation_alpha = int(150 + 105 * pulse)
        self.ui.draw_text_with_shadow(
            self.screen, f'"{current_affirmation}"', self.font_medium,
            (self.width // 2, affirmation_y), (*self.realm_color, affirmation_alpha), 3, True
        )

        # Mood check-in (large, prominent)
        mood_y = affirmation_y + 120
        self.ui.draw_text_with_shadow(
            self.screen, "How are you feeling today?", self.font_medium,
            (self.width // 2, mood_y), self.theme.TEXT_BRIGHT, 2, True
        )

        # Mood scale (1-10) with visual slider
        self.render_mood_scale(self.width // 2, mood_y + 80)

        # Quick actions (left side)
        actions_x = 120
        actions_y = mood_y + 280

        self.ui.draw_text_with_shadow(
            self.screen, "QUICK CALMING TOOLS", self.font_normal,
            (actions_x, actions_y), (100, 200, 255), 2, False
        )

        actions = [
            "[SPACE] Calm Mode - Guided breathing with visuals",
            "[G] Grounding - 5-4-3-2-1 technique for anxiety",
            "[C] Contact Caregiver - Get support now",
        ]
        for i, action in enumerate(actions):
            self.ui.draw_text_with_shadow(
                self.screen, action, self.font_small,
                (actions_x + 20, actions_y + 60 + i * 50), self.theme.TEXT_NORMAL, 2, False
            )

        # Anxiety reduction tips (right side)
        tips_x = self.width // 2 + 100
        tips_y = actions_y

        self.ui.draw_text_with_shadow(
            self.screen, "WHEN YOU FEEL ANXIOUS", self.font_normal,
            (tips_x, tips_y), (255, 150, 100), 2, False
        )

        tips = [
            "• Focus on your breath - slow and steady",
            "• Ground yourself - feel your feet on floor",
            "• Name what you see, hear, feel around you",
            "• Remind yourself: This feeling will pass",
        ]
        for i, tip in enumerate(tips):
            self.ui.draw_text_with_shadow(
                self.screen, tip, self.font_small,
                (tips_x + 20, tips_y + 60 + i * 50), self.theme.TEXT_NORMAL, 2, False
            )

    def render_mood_scale(self, center_x: int, y: int):
        """Render interactive mood scale (1-10)"""
        scale_width = 800
        scale_height = 60
        start_x = center_x - scale_width // 2

        # Draw scale background
        scale_rect = pygame.Rect(start_x, y, scale_width, scale_height)
        bg_surf = pygame.Surface((scale_width, scale_height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 80))
        self.screen.blit(bg_surf, (start_x, y))
        pygame.draw.rect(self.screen, self.realm_color, scale_rect, 2)

        # Draw scale markers (1-10)
        for i in range(1, 11):
            marker_x = start_x + (i - 0.5) * (scale_width / 10)
            marker_y = y + scale_height // 2

            # Number
            num_color = self.theme.TEXT_BRIGHT if i == self.mood_level else self.theme.TEXT_DIM
            self.ui.draw_text_with_shadow(
                self.screen, str(i), self.font_normal,
                (int(marker_x), int(marker_y)), num_color, 2, True
            )

        # Draw current mood indicator (breathing circle)
        indicator_x = start_x + (self.mood_level - 0.5) * (scale_width / 10)
        indicator_y = y + scale_height + 50
        pulse = self.anim.breathe(self.time, 2.0)
        indicator_radius = int(20 + 10 * pulse)

        # Mood color gradient (red -> yellow -> green)
        if self.mood_level <= 3:
            mood_color = (255, 100, 100)  # Red (low mood)
        elif self.mood_level <= 7:
            mood_color = (255, 200, 100)  # Yellow (neutral)
        else:
            mood_color = (100, 255, 150)  # Green (good mood)

        self.ui.draw_breathing_circle(self.screen, (int(indicator_x), indicator_y), indicator_radius, mood_color, self.time)

        # Mood labels
        label_y = y + scale_height + 120
        self.ui.draw_text_with_shadow(
            self.screen, "Struggling", self.font_small,
            (start_x + 80, label_y), (255, 100, 100), 2, True
        )
        self.ui.draw_text_with_shadow(
            self.screen, "Neutral", self.font_small,
            (center_x, label_y), (255, 200, 100), 2, True
        )
        self.ui.draw_text_with_shadow(
            self.screen, "Feeling Good", self.font_small,
            (start_x + scale_width - 80, label_y), (100, 255, 150), 2, True
        )

        # Instruction
        self.ui.draw_text_with_shadow(
            self.screen, "Use LEFT/RIGHT arrows to adjust your mood", self.font_small,
            (center_x, y - 40), self.theme.TEXT_DIM, 2, True
        )

    def render_grounding_technique(self, y_start: int):
        """Render 5-4-3-2-1 grounding technique for PTSD/anxiety"""
        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "GROUNDING TECHNIQUE - 5-4-3-2-1 Method", self.font_large,
            (self.width // 2, y_start + 40), (100, 255, 150), 3, True
        )

        # Instruction
        self.ui.draw_text_with_shadow(
            self.screen, "Take your time. Breathe slowly. Focus on the present moment.", self.font_normal,
            (self.width // 2, y_start + 120), self.theme.TEXT_DIM, 2, True
        )

        # Show all 5 steps, highlight current one
        steps_y = y_start + 220
        for i, prompt in enumerate(self.grounding_prompts):
            step_y = steps_y + i * 100

            # Step number and prompt
            step_num = 5 - i
            is_current = (i == self.grounding_step)

            if is_current:
                # Highlight current step with breathing glow
                pulse = self.anim.breathe(self.time, 2.0)
                glow_alpha = int(80 * pulse)

                # Glow background
                glow_rect = pygame.Rect(200, step_y - 30, self.width - 400, 80)
                glow_surf = pygame.Surface((self.width - 400, 80), pygame.SRCALPHA)
                glow_surf.fill((*self.realm_color, glow_alpha))
                self.screen.blit(glow_surf, (200, step_y - 30))
                pygame.draw.rect(self.screen, self.realm_color, glow_rect, 3)

                text_color = self.theme.TEXT_BRIGHT
                font = self.font_medium
            else:
                text_color = self.theme.TEXT_DIM
                font = self.font_normal

            # Render step
            step_text = f"{step_num}. {prompt}"
            self.ui.draw_text_with_shadow(
                self.screen, step_text, font,
                (self.width // 2, step_y), text_color, 2, True
            )

        # Navigation
        nav_y = steps_y + 550
        self.ui.draw_text_with_shadow(
            self.screen, "Press UP/DOWN to navigate  │  ESC to exit grounding", self.font_normal,
            (self.width // 2, nav_y), self.theme.TEXT_DIM, 2, True
        )

    def render_body_view(self):
        """Render BODY view - simple reminders (non-medical)"""
        y_start = 280

        # Section title
        self.ui.draw_text_with_shadow(
            self.screen, "BODY - Simple Wellness Reminders", self.font_large,
            (self.width // 2, y_start), (100, 255, 150), 3, True
        )

        # Water intake (left side)
        water_x = 150
        water_y = y_start + 120

        self.ui.draw_text_with_shadow(
            self.screen, "WATER INTAKE", self.font_medium,
            (water_x, water_y), (100, 200, 255), 2, False
        )

        # Visual water tracker
        water_text = f"{self.water_intake} / {self.water_goal} glasses today"
        self.ui.draw_text_with_shadow(
            self.screen, water_text, self.font_large,
            (water_x, water_y + 70), (100, 200, 255), 3, False
        )

        # Water glasses visualization
        glasses_y = water_y + 150
        for i in range(self.water_goal):
            glass_x = water_x + i * 60
            filled = i < self.water_intake
            color = (100, 200, 255) if filled else self.theme.TEXT_DIM

            # Simple rectangle for glass
            glass_rect = pygame.Rect(glass_x, glasses_y, 40, 60)
            if filled:
                pygame.draw.rect(self.screen, color, glass_rect)
            else:
                pygame.draw.rect(self.screen, color, glass_rect, 2)

        # Medication reminders (left side, below water)
        med_y = glasses_y + 120
        self.ui.draw_text_with_shadow(
            self.screen, "MEDICATION REMINDERS", self.font_medium,
            (water_x, med_y), (255, 200, 100), 2, False
        )

        for i, med in enumerate(self.medication_reminders):
            med_text_y = med_y + 60 + i * 50
            status = "[✓]" if med["taken"] else "[ ]"
            color = self.theme.TEXT_DIM if med["taken"] else (255, 200, 100)

            med_text = f"{status} {med['time']} - {med['name']}"
            self.ui.draw_text_with_shadow(
                self.screen, med_text, self.font_small,
                (water_x + 20, med_text_y), color, 2, False
            )

        # Light activity reminder (right side)
        activity_x = self.width // 2 + 100
        activity_y = y_start + 120

        self.ui.draw_text_with_shadow(
            self.screen, "LIGHT ACTIVITY", self.font_medium,
            (activity_x, activity_y), (150, 255, 150), 2, False
        )

        activity_text = f"{self.activity_minutes} / {self.activity_goal} minutes today"
        self.ui.draw_text_with_shadow(
            self.screen, activity_text, self.font_normal,
            (activity_x, activity_y + 70), self.theme.TEXT_NORMAL, 2, False
        )

        activity_tips = [
            "• Short walk around the house",
            "• Gentle stretching in chair",
            "• Stand up every hour",
            "• Light mobility exercises",
        ]
        for i, tip in enumerate(activity_tips):
            self.ui.draw_text_with_shadow(
                self.screen, tip, self.font_small,
                (activity_x, activity_y + 140 + i * 50), self.theme.TEXT_NORMAL, 2, False
            )

        # Sleep hygiene (right side, below activity)
        sleep_y = activity_y + 380
        self.ui.draw_text_with_shadow(
            self.screen, "SLEEP HYGIENE", self.font_medium,
            (activity_x, sleep_y), (200, 150, 255), 2, False
        )

        self.ui.draw_text_with_shadow(
            self.screen, self.sleep_reminder, self.font_normal,
            (activity_x, sleep_y + 70), (200, 150, 255), 2, False
        )

        sleep_tips = [
            "• Dim lights 1 hour before bed",
            "• No screens 30 min before sleep",
            "• Keep bedroom cool and dark",
        ]
        for i, tip in enumerate(sleep_tips):
            self.ui.draw_text_with_shadow(
                self.screen, tip, self.font_small,
                (activity_x, sleep_y + 130 + i * 50), self.theme.TEXT_NORMAL, 2, False
            )

    def render_spirit_view(self):
        """Render SPIRIT view - encouragement, gratitude, reflection"""
        y_start = 280

        # Section title
        self.ui.draw_text_with_shadow(
            self.screen, "SPIRIT - Encouragement & Peace", self.font_large,
            (self.width // 2, y_start), (255, 200, 150), 3, True
        )

        # Daily encouragement (large, centered)
        encourage_y = y_start + 120
        pulse = self.anim.breathe(self.time, 3.0)
        glow_alpha = int(100 * pulse)

        # Glow box around encouragement
        encourage_rect = pygame.Rect(200, encourage_y - 40, self.width - 400, 140)
        glow_surf = pygame.Surface((self.width - 400, 140), pygame.SRCALPHA)
        glow_surf.fill((255, 200, 150, glow_alpha))
        self.screen.blit(glow_surf, (200, encourage_y - 40))
        pygame.draw.rect(self.screen, (255, 200, 150), encourage_rect, 3)

        self.ui.draw_text_with_shadow(
            self.screen, self.current_encouragement, self.font_large,
            (self.width // 2, encourage_y + 30), (255, 200, 150), 3, True
        )

        # Gratitude prompt
        gratitude_y = encourage_y + 240
        self.ui.draw_text_with_shadow(
            self.screen, "GRATITUDE PRACTICE", self.font_medium,
            (self.width // 2, gratitude_y), (150, 255, 200), 2, True
        )

        self.ui.draw_text_with_shadow(
            self.screen, self.gratitude_prompt, self.font_normal,
            (self.width // 2, gratitude_y + 70), self.theme.TEXT_NORMAL, 2, True
        )

        # Example gratitude items
        gratitude_examples = [
            "• A warm home",
            "• People who care about you",
            "• This moment of peace",
        ]
        gratitude_list_y = gratitude_y + 150
        for i, example in enumerate(gratitude_examples):
            self.ui.draw_text_with_shadow(
                self.screen, example, self.font_small,
                (self.width // 2, gratitude_list_y + i * 50), self.theme.TEXT_DIM, 2, True
            )

        # Quiet reflection prompt
        reflection_y = gratitude_list_y + 200
        self.ui.draw_text_with_shadow(
            self.screen, "QUIET REFLECTION", self.font_medium,
            (self.width // 2, reflection_y), (200, 180, 255), 2, True
        )

        self.ui.draw_text_with_shadow(
            self.screen, "Take a moment to simply be present.", self.font_normal,
            (self.width // 2, reflection_y + 70), self.theme.TEXT_DIM, 2, True
        )

        self.ui.draw_text_with_shadow(
            self.screen, "No need to do anything. Just breathe and exist.", self.font_small,
            (self.width // 2, reflection_y + 120), self.theme.TEXT_DIM, 2, True
        )

    def render_calm_mode(self):
        """Render Calm Mode - immersive breathing exercise with ambient visuals"""
        # Dark, calming background
        self.screen.fill((5, 10, 20))

        # Render floating particles
        for particle in self.calm_particles:
            if particle['life'] > 0:
                alpha = int(particle['life'] * 120)
                color = (*particle['color'], alpha)
                size = int(particle['size'])

                s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, color, (size, size), size)
                self.screen.blit(s, (int(particle['x']) - size, int(particle['y']) - size))

        # Central breathing orb
        center_x = self.width // 2
        center_y = self.height // 2 - 100

        # Calculate breathing animation
        phase_duration = self.breathing_duration[self.breathing_phase]
        progress = self.breathing_timer / phase_duration

        # Orb size based on breathing phase
        if self.breathing_phase == "inhale":
            base_radius = 80
            max_radius = 180
            radius = int(base_radius + (max_radius - base_radius) * progress)
        elif self.breathing_phase == "hold":
            radius = 180  # Stay large
        elif self.breathing_phase == "exhale":
            base_radius = 80
            max_radius = 180
            radius = int(max_radius - (max_radius - base_radius) * progress)

        # Draw breathing orb with glow
        self.ui.draw_breathing_circle(
            self.screen, (center_x, center_y), radius,
            (100, 180, 255), self.time
        )

        # Breathing instruction text
        instruction_y = center_y + 250

        if self.breathing_phase == "inhale":
            instruction = "Breathe in slowly..."
            count_text = f"{int(self.breathing_timer + 1)} / {int(self.breathing_duration['inhale'])}"
        elif self.breathing_phase == "hold":
            instruction = "Hold your breath..."
            count_text = f"{int(self.breathing_timer + 1)} / {int(self.breathing_duration['hold'])}"
        elif self.breathing_phase == "exhale":
            instruction = "Breathe out slowly..."
            count_text = f"{int(self.breathing_timer + 1)} / {int(self.breathing_duration['exhale'])}"

        self.ui.draw_text_with_shadow(
            self.screen, instruction, self.font_huge,
            (center_x, instruction_y), (150, 200, 255), 4, True
        )

        self.ui.draw_text_with_shadow(
            self.screen, count_text, self.font_large,
            (center_x, instruction_y + 100), self.theme.TEXT_DIM, 3, True
        )

        # Calming message at top
        self.ui.draw_text_with_shadow(
            self.screen, "You are safe. Focus on your breath.", self.font_medium,
            (center_x, 150), self.theme.TEXT_DIM, 2, True
        )

        # Current affirmation at bottom
        affirmation = self.affirmations[self.current_affirmation_index]
        self.ui.draw_text_with_shadow(
            self.screen, f'"{affirmation}"', self.font_normal,
            (center_x, self.height - 180), (150, 200, 255), 2, True
        )

    def spawn_calm_particle(self):
        """Spawn ambient particle for Calm Mode"""
        self.calm_particles.append({
            'x': random.randint(0, self.width),
            'y': self.height,
            'vy': random.uniform(30, 80),
            'life': random.uniform(0.8, 1.2),
            'size': random.randint(3, 8),
            'offset': random.uniform(0, math.pi * 2),
            'color': random.choice([
                (100, 180, 255),  # Blue
                (150, 200, 255),  # Light blue
                (100, 200, 200),  # Cyan
            ])
        })

    def handle_key(self, key: int):
        """Handle realm-specific controls"""
        # View mode navigation
        if key == pygame.K_m:
            self.view_mode = "MIND"
            self.grounding_active = False
            print("   Switching to MIND view")
        elif key == pygame.K_b:
            self.view_mode = "BODY"
            self.grounding_active = False
            print("   Switching to BODY view")
        elif key == pygame.K_s:
            self.view_mode = "SPIRIT"
            self.grounding_active = False
            print("   Switching to SPIRIT view")

        # Calm Mode toggle
        elif key == pygame.K_SPACE:
            if self.view_mode == "CALM_MODE":
                self.view_mode = "MIND"
                print("   Exiting Calm Mode")
            else:
                self.view_mode = "CALM_MODE"
                self.breathing_phase = "inhale"
                self.breathing_timer = 0.0
                self.calm_particles = []
                print("   Entering Calm Mode - Guided breathing")

        # Grounding technique toggle
        elif key == pygame.K_g:
            if self.view_mode == "MIND":
                self.grounding_active = not self.grounding_active
                if self.grounding_active:
                    self.grounding_step = 0
                    print("   Starting 5-4-3-2-1 Grounding Technique")
                else:
                    print("   Exiting Grounding Technique")

        # Grounding navigation
        elif key == pygame.K_UP:
            if self.grounding_active and self.grounding_step > 0:
                self.grounding_step -= 1
        elif key == pygame.K_DOWN:
            if self.grounding_active and self.grounding_step < 4:
                self.grounding_step += 1

        # Mood adjustment
        elif key == pygame.K_LEFT:
            if self.view_mode == "MIND" and not self.grounding_active:
                self.mood_level = max(1, self.mood_level - 1)
                print(f"   Mood level: {self.mood_level}/10")
        elif key == pygame.K_RIGHT:
            if self.view_mode == "MIND" and not self.grounding_active:
                self.mood_level = min(10, self.mood_level + 1)
                print(f"   Mood level: {self.mood_level}/10")

        # Caregiver notification
        elif key == pygame.K_c:
            print("   🔔 CAREGIVER NOTIFICATION SENT")
            print("      Message: User requested support")
            # In production: would send real notification


def main():
    """Run Mental Wellness & PTSD Support Realm standalone"""
    realm = ClinicalHealthPro()
    realm.run()


if __name__ == "__main__":
    main()
