"""
MotiBeam Spatial OS - Enhanced Clinical & Health Realm
⚕️ Realm #2 - Comprehensive wellness monitoring with Body/Mind/Spirit approach

Categories:
- BODY: Vitals, activity, nutrition, medication
- MIND: Mental wellness, stress, cognition
- SPIRIT: Purpose, connection, gratitude

Features:
- Real-time vital signs monitoring
- Daily wellness recommendations
- Medication reminders with notifications
- Caregiver notification system
- Holistic health tracking
"""

import random
import math
from typing import List, Tuple, Dict
from datetime import datetime, timedelta

# Import base realm (which already imports pygame)
from realms.base_realm import BaseRealm
import pygame  # Re-import for type hints and direct usage


class WellnessRecommendation:
    """Daily wellness recommendation"""

    def __init__(self, category: str, title: str, description: str, icon: str):
        self.category = category  # BODY, MIND, or SPIRIT
        self.title = title
        self.description = description
        self.icon = icon
        self.completed = False


class Medication:
    """Medication reminder"""

    def __init__(self, name: str, dosage: str, time_str: str, color: Tuple[int, int, int]):
        self.name = name
        self.dosage = dosage
        self.time_str = time_str
        self.color = color
        self.taken = False
        self.notified = False


class VitalSign:
    """Animated vital sign with realistic variations"""

    def __init__(self, name: str, base_value: float, unit: str, min_val: float, max_val: float,
                 variation: float, color: Tuple[int, int, int]):
        self.name = name
        self.base_value = base_value
        self.current_value = base_value
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self.variation = variation
        self.color = color
        self.history: List[float] = [base_value] * 100
        self.alert = False
        self.trend = 0.0

    def update(self, dt: float):
        """Update vital sign with realistic variation"""
        # Smooth random walk
        self.trend += (random.random() - 0.5) * 0.1
        self.trend *= 0.95  # Decay

        # Calculate new value
        target = self.base_value + (random.random() - 0.5) * self.variation + self.trend
        self.current_value += (target - self.current_value) * dt * 2

        # Clamp to safe range
        self.current_value = max(self.min_val, min(self.max_val, self.current_value))

        # Update history
        self.history.append(self.current_value)
        if len(self.history) > 100:
            self.history.pop(0)

        # Check for alerts
        safe_range = (self.max_val - self.min_val) * 0.15
        self.alert = (self.current_value < self.min_val + safe_range or
                     self.current_value > self.max_val - safe_range)


class ClinicalHealthPro(BaseRealm):
    """Enhanced Clinical & Health Realm with Body/Mind/Spirit approach"""

    def __init__(self):
        super().__init__(
            realm_id=2,
            realm_name="CLINICAL & HEALTH WELLNESS",
            realm_color=(80, 255, 120)
        )

        # Current view mode
        self.view_mode = "DASHBOARD"  # DASHBOARD, BODY, MIND, SPIRIT

        # Initialize vital signs (BODY)
        self.vital_signs = [
            VitalSign("HEART RATE", 72, "BPM", 45, 100, 8, (255, 100, 120)),
            VitalSign("BLOOD PRESSURE", 120, "mmHg", 90, 140, 5, (100, 200, 255)),
            VitalSign("OXYGEN SAT", 98, "%", 88, 100, 2, (100, 255, 150)),
            VitalSign("TEMPERATURE", 98.6, "°F", 97.0, 99.5, 0.5, (255, 200, 100)),
        ]

        # Daily wellness recommendations
        self.recommendations = self.generate_daily_recommendations()

        # Medication reminders
        self.medications = [
            Medication("Vitamin D", "1000 IU", "08:00", (255, 200, 100)),
            Medication("Blood Pressure Med", "10mg", "12:00", (100, 200, 255)),
            Medication("Evening Supplement", "1 capsule", "20:00", (150, 255, 150)),
        ]

        # Wellness metrics (demo values)
        self.activity_minutes = 20  # Daily activity minutes
        self.activity_goal = 30
        self.water_intake = 6  # Glasses of water
        self.water_goal = 8
        self.stress_level = 3  # 1-10 scale
        self.sleep_hours = 7.5
        self.sunlight_minutes = 10  # Minutes of sunlight today
        self.sunlight_goal = 15

        # Caregiver notification system
        self.caregiver_notifications = []
        self.caregiver_contact = "Dr. Smith"

        # Biometric particles
        self.bio_particles: List[dict] = []
        self.particle_timer = 0.0

        # Patient info
        self.patient_name = "WELLNESS USER"
        self.patient_status = "HEALTHY"

        print("🩺 Enhanced Clinical & Health Realm initialized")
        print("   Body/Mind/Spirit wellness tracking active")

    def generate_daily_recommendations(self) -> List[WellnessRecommendation]:
        """Generate daily wellness recommendations across Body/Mind/Spirit"""
        return [
            # BODY recommendations with specific metrics
            WellnessRecommendation(
                "BODY", "20 min walk (10/30 min done)",
                "Complete 30 min walk in sunlight for vitamin D and cardiovascular health",
                "+"
            ),
            WellnessRecommendation(
                "BODY", "Water 8/10 bottles (80% done)",
                "Drink 2 more glasses - Stay hydrated for optimal body function",
                "~"
            ),
            WellnessRecommendation(
                "BODY", "15 min sunlight (Vitamin D low)",
                "Get 5 more minutes of sunlight - Vitamin D levels need boost",
                "*"
            ),

            # MIND recommendations
            WellnessRecommendation(
                "MIND", "Mindful Breathing",
                "Practice 5 minutes of deep breathing to reduce stress and improve focus",
                "o"
            ),
            WellnessRecommendation(
                "MIND", "Mental Stimulation",
                "Engage in a puzzle, read, or learn something new to keep mind sharp",
                "#"
            ),
            WellnessRecommendation(
                "MIND", "Digital Detox",
                "Take 1 hour away from screens to reduce mental fatigue",
                "-"
            ),

            # SPIRIT recommendations
            WellnessRecommendation(
                "SPIRIT", "Gratitude Practice",
                "Write down 3 things you're grateful for to foster positive mindset",
                "*"
            ),
            WellnessRecommendation(
                "SPIRIT", "Social Connection",
                "Reach out to a friend or family member for meaningful conversation",
                "+"
            ),
            WellnessRecommendation(
                "SPIRIT", "Purpose Reflection",
                "Spend time on an activity that aligns with your values and brings joy",
                "~"
            ),
        ]

    def update(self, dt: float):
        """Update clinical monitoring system"""
        # Update vital signs
        for vital in self.vital_signs:
            vital.update(dt)

        # Check medications
        current_time = datetime.now()
        for med in self.medications:
            # Check if it's time for medication (simplified)
            if not med.taken and not med.notified:
                # In real app, would check actual time
                if random.random() < 0.001:  # Random notification for demo
                    med.notified = True
                    self.notify_medication(med)

        # Update biometric particles
        self.particle_timer += dt
        if self.particle_timer > 0.1:
            self.particle_timer = 0.0
            self.spawn_bio_particle()

        for particle in self.bio_particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['life'] -= dt * 0.5

            if particle['life'] <= 0:
                self.bio_particles.remove(particle)

    def render(self):
        """Render clinical wellness interface"""
        # Background
        self.screen.fill(self.theme.BG_DEEP)

        # Render biometric particles
        self.render_bio_particles()

        # Header with view mode indicator
        self.draw_header(f"CLINICAL WELLNESS - {self.view_mode}", f"Patient: {self.patient_name}")

        # Render based on current view mode
        if self.view_mode == "DASHBOARD":
            self.render_dashboard_view()
        elif self.view_mode == "BODY":
            self.render_body_view()
        elif self.view_mode == "MIND":
            self.render_mind_view()
        elif self.view_mode == "SPIRIT":
            self.render_spirit_view()

        # Footer with navigation
        controls = "ESC: Exit  │  B: Body  │  M: Mind  │  S: Spirit  │  D: Dashboard  │  C: Call Caregiver"
        self.draw_footer(controls)

    def render_dashboard_view(self):
        """Render main dashboard with overview"""
        y_start = 280

        # Category buttons at top
        self.render_category_buttons(60, y_start)

        # Quick vitals summary
        self.render_quick_vitals(60, y_start + 100, 600, 200)

        # Today's recommendations
        self.render_recommendations_summary(700, y_start + 100, 1160, 200)

        # Medication reminders
        self.render_medication_panel(60, y_start + 340, 900, 300)

        # Wellness score
        self.render_wellness_score(1000, y_start + 340, 860, 240)

        # Caregiver button (separate, below wellness score)
        self.render_caregiver_button(1050, y_start + 610)

    def render_category_buttons(self, x: int, y: int):
        """Render Body/Mind/Spirit category buttons"""
        categories = [
            ("B", "BODY", (100, 200, 255)),
            ("M", "MIND", (200, 100, 255)),
            ("S", "SPIRIT", (255, 150, 100)),
        ]

        button_width = 200
        spacing = 40

        for i, (key, name, color) in enumerate(categories):
            bx = x + i * (button_width + spacing)

            # Button background
            pulse = self.anim.pulse(self.time + i * 0.5, 1.5)
            alpha = int(50 * pulse)
            rect = pygame.Rect(bx, y, button_width, 60)

            bg_surf = pygame.Surface((button_width, 60), pygame.SRCALPHA)
            bg_surf.fill((*color, alpha))
            self.screen.blit(bg_surf, (bx, y))

            # Border
            pygame.draw.rect(self.screen, color, rect, 3)

            # Text
            text = f"[{key}] {name}"
            self.ui.draw_text_with_shadow(
                self.screen, text, self.font_normal,
                (rect.centerx, rect.centery), color, 2, True
            )

    def render_quick_vitals(self, x: int, y: int, width: int, height: int):
        """Render quick vitals summary"""
        rect = pygame.Rect(x, y, width, height)

        # Background
        bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 40))
        self.screen.blit(bg_surf, (x, y))
        pygame.draw.rect(self.screen, self.realm_color, rect, 2)

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "VITALS", self.font_normal,
            (x + 20, y + 30), self.theme.TEXT_DIM, 2, False
        )

        # Quick vital values (2x2 grid)
        for i, vital in enumerate(self.vital_signs):
            col = i % 2
            row = i // 2
            vx = x + 40 + col * 280
            vy = y + 80 + row * 50

            value_text = f"{vital.name[:3]}: {int(vital.current_value)}{vital.unit}"
            color = vital.color if not vital.alert else self.theme.STATUS_ERROR

            self.ui.draw_text_with_shadow(
                self.screen, value_text, self.font_small,
                (vx, vy), color, 2, False
            )

    def render_recommendations_summary(self, x: int, y: int, width: int, height: int):
        """Render daily recommendations summary"""
        rect = pygame.Rect(x, y, width, height)

        # Background
        bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 40))
        self.screen.blit(bg_surf, (x, y))
        pygame.draw.rect(self.screen, (255, 200, 100), rect, 2)

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "TODAY'S WELLNESS GOALS", self.font_normal,
            (x + 20, y + 30), self.theme.TEXT_DIM, 2, False
        )

        # Show first 3 uncompleted recommendations
        ry = y + 80
        count = 0
        for rec in self.recommendations:
            if not rec.completed and count < 3:
                status = "[✓]" if rec.completed else "[ ]"
                text = f"{status} {rec.category}: {rec.title}"

                self.ui.draw_text_with_shadow(
                    self.screen, text, self.font_small,
                    (x + 40, ry), self.theme.TEXT_NORMAL, 2, False
                )
                ry += 40
                count += 1

    def render_medication_panel(self, x: int, y: int, width: int, height: int):
        """Render medication reminders"""
        rect = pygame.Rect(x, y, width, height)

        # Background
        bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 40))
        self.screen.blit(bg_surf, (x, y))
        pygame.draw.rect(self.screen, (100, 200, 255), rect, 2)

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "MEDICATION REMINDERS", self.font_normal,
            (x + 20, y + 30), self.theme.TEXT_DIM, 2, False
        )

        # Medications
        my = y + 80
        for med in self.medications:
            status = "[✓]" if med.taken else "[!]"
            text = f"{status} {med.time_str} - {med.name} ({med.dosage})"
            color = self.theme.TEXT_DIM if med.taken else med.color

            self.ui.draw_text_with_shadow(
                self.screen, text, self.font_small,
                (x + 40, my), color, 2, False
            )
            my += 50

    def render_wellness_score(self, x: int, y: int, width: int, height: int):
        """Render overall wellness score"""
        rect = pygame.Rect(x, y, width, height)

        # Background
        bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_surf.fill((*self.theme.BG_MID, 40))
        self.screen.blit(bg_surf, (x, y))
        pygame.draw.rect(self.screen, self.realm_color, rect, 2)

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, "WELLNESS SCORE", self.font_normal,
            (x + 20, y + 30), self.theme.TEXT_DIM, 2, False
        )

        # Demo wellness score set to 87%
        score = 87

        # Big score number
        score_text = f"{score}"
        self.ui.draw_text_with_shadow(
            self.screen, score_text, self.font_huge,
            (rect.centerx - 100, rect.centery + 20), self.realm_color, 4, False
        )

        # Percent sign
        self.ui.draw_text_with_shadow(
            self.screen, "%", self.font_large,
            (rect.centerx + 100, rect.centery + 20), self.theme.TEXT_DIM, 3, False
        )

    def render_caregiver_button(self, x: int, y: int):
        """Render caregiver notification button separately"""
        btn_width = 400
        btn_height = 70
        btn_rect = pygame.Rect(x, y, btn_width, btn_height)

        # Button background with pulse
        pulse = self.anim.pulse(self.time, 2.0)
        alpha = int(40 * pulse)
        bg_surf = pygame.Surface((btn_width, btn_height), pygame.SRCALPHA)
        bg_surf.fill((255, 100, 100, alpha))
        self.screen.blit(bg_surf, (x, y))

        # Border
        pygame.draw.rect(self.screen, (255, 100, 100), btn_rect, 3)

        # Text
        self.ui.draw_text_with_shadow(
            self.screen, "[C] NOTIFY CAREGIVER", self.font_medium,
            (btn_rect.centerx, btn_rect.centery), (255, 100, 100), 2, True
        )

    def render_body_view(self):
        """Render detailed BODY view with exercise and meal plans"""
        y_start = 280

        self.ui.draw_text_with_shadow(
            self.screen, "BODY - Physical Health & Wellness", self.font_large,
            (self.width // 2, y_start), (100, 200, 255), 3, True
        )

        # Daily exercise plan
        ex_y = y_start + 100
        self.ui.draw_text_with_shadow(
            self.screen, "TODAY'S EXERCISE PLAN", self.font_medium,
            (120, ex_y), (100, 200, 255), 2, False
        )

        exercises = [
            "[ ] Morning: 20-min brisk walk (Vitamin D boost)",
            "[ ] Afternoon: 10 squats, 10 push-ups (Strength)",
            "[✓] Evening: 15-min yoga stretching (Flexibility)",
        ]
        for i, ex in enumerate(exercises):
            self.ui.draw_text_with_shadow(
                self.screen, ex, self.font_small,
                (140, ex_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Weekly goals
        week_y = ex_y + 240
        self.ui.draw_text_with_shadow(
            self.screen, "WEEKLY GOALS", self.font_medium,
            (120, week_y), (100, 200, 255), 2, False
        )

        weekly = [
            "Activity: 150 mins (100/150 done - 67%)",
            "Strength training: 2 sessions (1/2 done)",
            "Water intake: 56 glasses (42/56 done - 75%)",
        ]
        for i, item in enumerate(weekly):
            self.ui.draw_text_with_shadow(
                self.screen, item, self.font_small,
                (140, week_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Meal plan (right side)
        meal_x = self.width // 2 + 100
        self.ui.draw_text_with_shadow(
            self.screen, "TODAY'S MEAL PLAN", self.font_medium,
            (meal_x, ex_y), (100, 255, 150), 2, False
        )

        meals = [
            "[✓] Breakfast: Oatmeal + berries + almonds",
            "[ ] Lunch: Grilled chicken salad + quinoa",
            "[ ] Snack: Greek yogurt + apple slices",
            "[ ] Dinner: Salmon + broccoli + sweet potato",
        ]
        for i, meal in enumerate(meals):
            self.ui.draw_text_with_shadow(
                self.screen, meal, self.font_small,
                (meal_x + 20, ex_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Nutrition goals
        nutr_y = week_y
        self.ui.draw_text_with_shadow(
            self.screen, "NUTRITION GOALS", self.font_medium,
            (meal_x, nutr_y), (100, 255, 150), 2, False
        )

        nutrition = [
            "Protein: 120g (85/120g done - 71%)",
            "Vegetables: 5 servings (3/5 done)",
            "Fiber: 30g (22/30g done - 73%)",
        ]
        for i, item in enumerate(nutrition):
            self.ui.draw_text_with_shadow(
                self.screen, item, self.font_small,
                (meal_x + 20, nutr_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Navigation
        self.ui.draw_text_with_shadow(
            self.screen, "Press D to return to Dashboard", self.font_normal,
            (self.width // 2, self.height - 150), self.theme.TEXT_DIM, 2, True
        )

    def render_mind_view(self):
        """Render detailed MIND view with mental wellness activities"""
        y_start = 280

        self.ui.draw_text_with_shadow(
            self.screen, "MIND - Mental Wellness & Cognitive Health", self.font_large,
            (self.width // 2, y_start), (200, 100, 255), 3, True
        )

        # Daily mental exercises
        mind_y = y_start + 100
        self.ui.draw_text_with_shadow(
            self.screen, "TODAY'S MENTAL EXERCISES", self.font_medium,
            (120, mind_y), (200, 100, 255), 2, False
        )

        exercises = [
            "[✓] Morning: 10-min guided meditation",
            "[ ] Afternoon: Crossword puzzle (15 min)",
            "[ ] Evening: Gratitude journaling (5 min)",
        ]
        for i, ex in enumerate(exercises):
            self.ui.draw_text_with_shadow(
                self.screen, ex, self.font_small,
                (140, mind_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Stress management
        stress_y = mind_y + 240
        self.ui.draw_text_with_shadow(
            self.screen, "STRESS MANAGEMENT", self.font_medium,
            (120, stress_y), (200, 100, 255), 2, False
        )

        stress_info = [
            f"Current stress level: {self.stress_level}/10 (Moderate)",
            "Breathing exercises: 3/3 completed today",
            "Digital detox: 2 hours screen-free achieved",
        ]
        for i, item in enumerate(stress_info):
            self.ui.draw_text_with_shadow(
                self.screen, item, self.font_small,
                (140, stress_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Weekly cognitive goals (right side)
        cog_x = self.width // 2 + 100
        self.ui.draw_text_with_shadow(
            self.screen, "WEEKLY COGNITIVE GOALS", self.font_medium,
            (cog_x, mind_y), (255, 150, 255), 2, False
        )

        cognitive = [
            "[ ] Read 30 pages (18/30 done - 60%)",
            "[✓] Learn new skill (completed: cooking)",
            "[ ] Social interaction: 3 conversations",
            "[ ] Creative activity: 1 hour art/music",
        ]
        for i, goal in enumerate(cognitive):
            self.ui.draw_text_with_shadow(
                self.screen, goal, self.font_small,
                (cog_x + 20, mind_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Navigation
        self.ui.draw_text_with_shadow(
            self.screen, "Press D to return to Dashboard", self.font_normal,
            (self.width // 2, self.height - 150), self.theme.TEXT_DIM, 2, True
        )

    def render_spirit_view(self):
        """Render detailed SPIRIT view with purpose and connection activities"""
        y_start = 280

        self.ui.draw_text_with_shadow(
            self.screen, "SPIRIT - Purpose, Connection & Inner Peace", self.font_large,
            (self.width // 2, y_start), (255, 150, 100), 3, True
        )

        # Daily spiritual practices
        spirit_y = y_start + 100
        self.ui.draw_text_with_shadow(
            self.screen, "TODAY'S SPIRITUAL PRACTICES", self.font_medium,
            (120, spirit_y), (255, 150, 100), 2, False
        )

        practices = [
            "[✓] Morning: Gratitude reflection (3 things)",
            "[ ] Afternoon: Nature walk & mindfulness",
            "[ ] Evening: Purpose journaling (5 min)",
        ]
        for i, practice in enumerate(practices):
            self.ui.draw_text_with_shadow(
                self.screen, practice, self.font_small,
                (140, spirit_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Connection goals
        conn_y = spirit_y + 240
        self.ui.draw_text_with_shadow(
            self.screen, "SOCIAL CONNECTION", self.font_medium,
            (120, conn_y), (255, 150, 100), 2, False
        )

        connections = [
            "[✓] Called Mom - 20 min conversation",
            "[ ] Video chat with grandkids (scheduled 4pm)",
            "[ ] Community group meeting tomorrow 10am",
        ]
        for i, conn in enumerate(connections):
            self.ui.draw_text_with_shadow(
                self.screen, conn, self.font_small,
                (140, conn_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Purpose activities (right side)
        purp_x = self.width // 2 + 100
        self.ui.draw_text_with_shadow(
            self.screen, "PURPOSE & VALUES", self.font_medium,
            (purp_x, spirit_y), (255, 200, 150), 2, False
        )

        purpose = [
            "Weekly volunteer work: 2 hours (Done!)",
            "Hobby time: Gardening 30 min daily",
            "Teaching grandkids: Cooking lesson Saturday",
            "Personal growth: Reading philosophy",
        ]
        for i, item in enumerate(purpose):
            self.ui.draw_text_with_shadow(
                self.screen, item, self.font_small,
                (purp_x + 20, spirit_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Monthly goals
        month_y = conn_y
        self.ui.draw_text_with_shadow(
            self.screen, "MONTHLY SPIRITUAL GOALS", self.font_medium,
            (purp_x, month_y), (255, 200, 150), 2, False
        )

        monthly = [
            "Gratitude entries: 22/30 days (73%)",
            "Acts of kindness: 8/10 done",
            "Meditation streak: 18 consecutive days",
        ]
        for i, item in enumerate(monthly):
            self.ui.draw_text_with_shadow(
                self.screen, item, self.font_small,
                (purp_x + 20, month_y + 60 + i * 45), self.theme.TEXT_NORMAL, 2, False
            )

        # Navigation
        self.ui.draw_text_with_shadow(
            self.screen, "Press D to return to Dashboard", self.font_normal,
            (self.width // 2, self.height - 150), self.theme.TEXT_DIM, 2, True
        )

    def render_bio_particles(self):
        """Render ambient biometric particles"""
        for particle in self.bio_particles:
            if particle['life'] > 0:
                alpha = int(particle['life'] * 60)
                color = (*self.realm_color, alpha)
                size = int(particle['size'] * (particle['life'] + 0.5))
                s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, color, (size, size), size)
                self.screen.blit(s, (int(particle['x']) - size, int(particle['y']) - size))

    def spawn_bio_particle(self):
        """Spawn ambient biometric particle"""
        self.bio_particles.append({
            'x': random.randint(0, self.width),
            'y': random.randint(280, self.height - 100),
            'vx': random.uniform(-20, 20),
            'vy': random.uniform(-20, 20),
            'life': 1.0,
            'size': random.randint(2, 6),
        })

    def notify_medication(self, med: Medication):
        """Send medication reminder notification"""
        print(f"   💊 Medication reminder: {med.name} ({med.dosage})")

    def notify_caregiver(self, message: str):
        """Notify caregiver"""
        print(f"   📞 Notifying caregiver: {self.caregiver_contact}")
        print(f"      Message: {message}")
        self.caregiver_notifications.append({
            'time': datetime.now(),
            'message': message
        })

    def handle_key(self, key: int):
        """Handle realm-specific controls"""
        if key == pygame.K_b:
            self.view_mode = "BODY"
            print("   Switching to BODY view")
        elif key == pygame.K_m:
            self.view_mode = "MIND"
            print("   Switching to MIND view")
        elif key == pygame.K_s:
            self.view_mode = "SPIRIT"
            print("   Switching to SPIRIT view")
        elif key == pygame.K_d:
            self.view_mode = "DASHBOARD"
            print("   Switching to DASHBOARD view")
        elif key == pygame.K_c:
            # Notify caregiver
            print("   🔔 CAREGIVER BUTTON PRESSED!")
            self.notify_caregiver("Wellness check requested by user")
            # Flash notification on screen briefly
            print(f"   ✓ Notification sent to {self.caregiver_contact}")


def main():
    """Run Enhanced Clinical & Health Realm standalone"""
    realm = ClinicalHealthPro()
    realm.run()


if __name__ == "__main__":
    main()
