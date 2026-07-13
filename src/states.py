import pygame
from src.state import State
from src.transport import BUS_TRANSPORT
from src.config import (
    CLASSMATE_HINT_TEXT,
    ROOM_INTRAMUROS,
    ROOM_ADMIN_OFFICE,
    ROOM_CAFETERIA,
    ROOM_ELECTRONICS_LAB,
    ROOM_LIBRARY,
    ROOM_MAIN,
    ROOM_OUTSIDE,
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL_ENTRANCE,
    ROOM_SCHOOL,
    ROOM_BEDROOM,
    MAX_GRADE_STANDING,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKILL_ACADEMICS,
    SKILL_DISCIPLINE,
    SKILL_MATH,
    STATE_PLAY,
    STUDY_XP,
    TILE_SIZE,
)

class PlayState(State):
    def handle_events(self, events):
        if self.game.player.studying:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    self.game.use_inventory_slot(event.key - pygame.K_1)
                    continue

                if event.key == pygame.K_e:
                    # Try to start interaction
                    if self.game.current_room == ROOM_MAIN and hasattr(self.game, 'mom') and self.game.mom in self.game.visible_sprites and self.game.check_proximity(self.game.player, self.game.mom, 64):
                        self.game.talk_to_mom()
                    elif self.game.current_room in (ROOM_OUTSIDE, ROOM_INTRAMUROS) and hasattr(self.game, 'bus') and self.game.check_proximity(self.game.player, self.game.bus, 100):
                        self.game.ride_bus()
                    elif self.game.current_room == ROOM_SCHOOL_ENTRANCE and self.game.try_enter_school_gate():
                        pass
                    elif self.game.current_room == ROOM_SCHOOL_ENTRANCE and self.game.talk_to_guard():
                        pass
                    elif self.game.current_room == ROOM_ADMIN_OFFICE and self.game.talk_to_attendant():
                        pass
                    elif self.game.current_room == ROOM_SCHOOL and self.game.talk_to_classmate():
                        pass
                    elif self.game.current_room == ROOM_SCHOOL and hasattr(self.game, 'school_desk') and self.game.check_proximity(self.game.player, self.game.school_desk, 64):
                        self.game.study_at_school()
                    elif self.game.current_room == ROOM_PROGRAMMING_LAB and hasattr(self.game, 'programming_station') and self.game.check_proximity(self.game.player, self.game.programming_station, 64):
                        self.game.practice_programming()
                    elif self.game.current_room == ROOM_ELECTRONICS_LAB and hasattr(self.game, 'electronics_station') and self.game.check_proximity(self.game.player, self.game.electronics_station, 64):
                        self.game.practice_electronics()
                    elif self.game.current_room == ROOM_LIBRARY and hasattr(self.game, 'library_academics_station') and self.game.check_proximity(self.game.player, self.game.library_academics_station, 64):
                        self.game.study_at_library(SKILL_ACADEMICS, "academics")
                    elif self.game.current_room == ROOM_LIBRARY and hasattr(self.game, 'library_math_station') and self.game.check_proximity(self.game.player, self.game.library_math_station, 64):
                        self.game.study_at_library(SKILL_MATH, "math")
                    elif self.game.current_room == ROOM_LIBRARY and hasattr(self.game, 'library_discipline_station') and self.game.check_proximity(self.game.player, self.game.library_discipline_station, 64):
                        self.game.study_at_library(SKILL_DISCIPLINE, "discipline")
                    elif self.game.get_exam_marker_near_player():
                        self.game.take_exam()
                    elif self.game.get_class_marker_near_player():
                        self.game.attend_class()
                    elif self.game.get_assignment_marker_near_player():
                        self.game.complete_assignment()
                    elif self.game.current_room == ROOM_CAFETERIA and hasattr(self.game, 'food_vendor') and self.game.check_proximity(self.game.player, self.game.food_vendor, 64):
                        self.game.buy_cafeteria_meal()
                    elif self.game.current_room == ROOM_BEDROOM and hasattr(self.game, 'bed') and self.game.check_proximity(self.game.player, self.game.bed, 64):
                        self.game.open_sleep_confirmation()
                    else:
                        # Try to pick up items
                        hits = pygame.sprite.spritecollide(self.game.player, self.game.item_sprites, False)
                        for item in hits:
                            if self.game.pick_up_item(item):
                                break

    def update(self):
        # Store previous studying state to detect when it finishes
        was_studying = self.game.player.studying
        
        self.game.visible_sprites.update()
        self.game.check_transitions()
        
        # If studying just finished, show dialogue
        if was_studying and not self.game.player.studying:
            skill_xp = self.game.get_skill_xp(SKILL_ACADEMICS)
            self.game.show_dialogue([f"You studied hard and gained {STUDY_XP} academics XP! Total: {skill_xp}."])
        
        # Constrain Mom within boundaries if she's in the current room
        if self.game.current_room == ROOM_MAIN and hasattr(self.game, 'mom') and self.game.mom in self.game.visible_sprites:
            self.game.mom.rect.left = max(0, min(self.game.mom.rect.left, SCREEN_WIDTH - self.game.mom.rect.width))
            self.game.mom.rect.top = max(TILE_SIZE * 2, min(self.game.mom.rect.top, SCREEN_HEIGHT - self.game.mom.rect.height))

    def draw(self, screen):
        # Draw proximity hint
        if self.game.current_room == ROOM_MAIN and self.game.check_proximity(self.game.player, self.game.mom, 64):
            hint_surf = self.game.font.render("Press E to talk", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.mom.rect.centerx, self.game.mom.rect.top - 20))
            screen.blit(hint_surf, hint_rect)
        
        if self.game.current_room in (ROOM_OUTSIDE, ROOM_INTRAMUROS) and hasattr(self.game, 'bus') and self.game.check_proximity(self.game.player, self.game.bus, 100):
            if self.game.current_room == ROOM_OUTSIDE:
                text = f"Press E to ride to Intramuros ({BUS_TRANSPORT.fare_label()})"
            else:
                text = f"Press E to ride back to Outside ({BUS_TRANSPORT.fare_label()})"
            
            hint_surf = self.game.font.render(text, True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.bus.rect.centerx, self.game.bus.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_SCHOOL and hasattr(self.game, 'school_desk') and self.game.check_proximity(self.game.player, self.game.school_desk, 64):
            hint_surf = self.game.font.render("Press E to study", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.school_desk.rect.centerx, self.game.school_desk.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_SCHOOL:
            classmate = self.game.get_classmate_near_player()
            if classmate:
                hint_surf = self.game.font.render(CLASSMATE_HINT_TEXT, True, 'white')
                hint_rect = hint_surf.get_rect(center=(classmate.rect.centerx, classmate.rect.top - 20))
                screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_PROGRAMMING_LAB and hasattr(self.game, 'programming_station') and self.game.check_proximity(self.game.player, self.game.programming_station, 64):
            hint_surf = self.game.font.render("Press E to practice programming", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.programming_station.rect.centerx, self.game.programming_station.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_ELECTRONICS_LAB and hasattr(self.game, 'electronics_station') and self.game.check_proximity(self.game.player, self.game.electronics_station, 64):
            hint_surf = self.game.font.render("Press E to practice electronics", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.electronics_station.rect.centerx, self.game.electronics_station.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_LIBRARY:
            library_hints = (
                ("library_academics_station", "Press E to study academics"),
                ("library_math_station", "Press E to study math"),
                ("library_discipline_station", "Press E to study discipline"),
            )
            for station_name, text in library_hints:
                station = getattr(self.game, station_name, None)
                if station and self.game.check_proximity(self.game.player, station, 64):
                    hint_surf = self.game.font.render(text, True, 'white')
                    hint_rect = hint_surf.get_rect(center=(station.rect.centerx, station.rect.top - 20))
                    screen.blit(hint_surf, hint_rect)
                    break

        if self.game.current_room == ROOM_CAFETERIA and hasattr(self.game, 'food_vendor') and self.game.check_proximity(self.game.player, self.game.food_vendor, 64):
            hint_surf = self.game.font.render("Press E to buy food", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.food_vendor.rect.centerx, self.game.food_vendor.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        class_marker = self.game.get_class_marker_near_player()
        if class_marker:
            hint_surf = self.game.font.render("Press E to attend class", True, 'white')
            hint_rect = hint_surf.get_rect(center=(class_marker.rect.centerx, class_marker.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        exam_marker = self.game.get_exam_marker_near_player()
        if exam_marker:
            hint_surf = self.game.font.render("Press E to take exam", True, 'white')
            hint_rect = hint_surf.get_rect(center=(exam_marker.rect.centerx, exam_marker.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        assignment_marker = self.game.get_assignment_marker_near_player()
        if assignment_marker:
            hint_surf = self.game.font.render("Press E to submit assignment", True, 'white')
            hint_rect = hint_surf.get_rect(center=(assignment_marker.rect.centerx, assignment_marker.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_BEDROOM and hasattr(self.game, 'bed') and self.game.check_proximity(self.game.player, self.game.bed, 64):
            hint_surf = self.game.font.render("Press E to sleep", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.bed.rect.centerx, self.game.bed.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_ADMIN_OFFICE:
            attendant = next((sprite for sprite in self.game.attendant_sprites if self.game.check_proximity(self.game.player, sprite, 64)), None)
            if attendant:
                hint_surf = self.game.font.render("Press E to talk", True, 'white')
                hint_rect = hint_surf.get_rect(center=(attendant.rect.centerx, attendant.rect.top - 20))
                screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_SCHOOL_ENTRANCE:
            gate = next((sprite for sprite in self.game.gate_sprites if self.game.check_proximity(self.game.player, sprite, 80)), None)
            if gate:
                hint_surf = self.game.font.render("Press E to use gate", True, 'white')
                hint_rect = hint_surf.get_rect(center=(gate.rect.centerx, gate.rect.top - 20))
                screen.blit(hint_surf, hint_rect)
            else:
                guard = next((sprite for sprite in self.game.guard_sprites if self.game.check_proximity(self.game.player, sprite, 64)), None)
                if guard:
                    hint_surf = self.game.font.render("Press E to talk", True, 'white')
                    hint_rect = hint_surf.get_rect(center=(guard.rect.centerx, guard.rect.top - 20))
                    screen.blit(hint_surf, hint_rect)

        # Draw item interaction hint
        item_hits = pygame.sprite.spritecollide(self.game.player, self.game.item_sprites, False)
        if item_hits:
            item = item_hits[0]
            hint_surf = self.game.font.render(f"Press E to pick up {item.name}", True, 'white')
            hint_rect = hint_surf.get_rect(center=(item.rect.centerx, item.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

class DialogueState(State):
    BOX_MARGIN_X = 50
    BOX_HEIGHT = 130
    BOX_BOTTOM_MARGIN = 20
    BOX_PADDING_X = 20
    BOX_PADDING_TOP = 18
    PROMPT_BOTTOM_MARGIN = 26

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.game.advance_dialogue()

    @staticmethod
    def wrap_text(text, font, max_width, max_lines):
        words = text.split()
        if not words:
            return [""]

        lines = []
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
                continue

            if current:
                lines.append(current)
            current = word

            while font.size(current)[0] > max_width:
                split_at = len(current)
                while split_at > 1 and font.size(current[:split_at])[0] > max_width:
                    split_at -= 1
                lines.append(current[:split_at])
                current = current[split_at:]

            if len(lines) >= max_lines:
                return DialogueState.truncate_lines([*lines, current], font, max_width, max_lines)

        if current:
            lines.append(current)

        return DialogueState.truncate_lines(lines, font, max_width, max_lines)

    @staticmethod
    def truncate_lines(lines, font, max_width, max_lines):
        if len(lines) <= max_lines:
            return lines

        visible = lines[:max_lines]
        ellipsis = "..."
        last = visible[-1]
        while last and font.size(last + ellipsis)[0] > max_width:
            last = last[:-1].rstrip()
        visible[-1] = (last + ellipsis) if last else ellipsis
        return visible

    def draw(self, screen):
        # Draw dialogue box
        if self.game.current_dialogue:
            box_rect = pygame.Rect(
                self.BOX_MARGIN_X,
                SCREEN_HEIGHT - self.BOX_HEIGHT - self.BOX_BOTTOM_MARGIN,
                SCREEN_WIDTH - self.BOX_MARGIN_X * 2,
                self.BOX_HEIGHT,
            )
            pygame.draw.rect(screen, (30, 30, 30), box_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), box_rect, 2, border_radius=10)

            text_area_width = box_rect.width - self.BOX_PADDING_X * 2
            prompt_surf = self.game.font.render("Press E to continue...", True, (150, 150, 150))
            prompt_pos = (box_rect.right - prompt_surf.get_width() - 20, box_rect.bottom - self.PROMPT_BOTTOM_MARGIN)
            line_height = self.game.font.get_linesize()
            available_height = prompt_pos[1] - (box_rect.y + self.BOX_PADDING_TOP) - 8
            max_lines = max(1, available_height // line_height)

            lines = self.wrap_text(
                self.game.current_dialogue[self.game.dialogue_index],
                self.game.font,
                text_area_width,
                max_lines,
            )
            for line_index, line in enumerate(lines):
                text_surf = self.game.font.render(line, True, 'white')
                screen.blit(
                    text_surf,
                    (
                        box_rect.x + self.BOX_PADDING_X,
                        box_rect.y + self.BOX_PADDING_TOP + line_index * line_height,
                    ),
                )
            
            screen.blit(prompt_surf, prompt_pos)


class SleepConfirmState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Sleep", "Cancel"]
        self.selected_index = 0
        self.joystick_latched = False

    def enter(self):
        self.selected_index = 0
        self.joystick_latched = False

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_UP, pygame.K_w):
                self.selected_index = 0
            elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN, pygame.K_s):
                self.selected_index = 1
            elif event.key in (pygame.K_e, pygame.K_RETURN, pygame.K_SPACE):
                self.select_current_option()

    def update(self):
        direction = self.game.mobile_controls.direction
        if direction.length_squared() < 0.16:
            self.joystick_latched = False
            return

        if self.joystick_latched:
            return

        if abs(direction.x) >= abs(direction.y):
            self.selected_index = 0 if direction.x < 0 else 1
        else:
            self.selected_index = 0 if direction.y < 0 else 1
        self.joystick_latched = True

    def select_current_option(self):
        selected = self.options[self.selected_index]
        if selected == "Sleep":
            self.game.sleep_until_next_day()
        elif selected == "Cancel":
            self.game.cancel_sleep_confirmation()

    def draw(self, screen):
        play_state = self.game.state_machine.states.get(STATE_PLAY)
        if play_state:
            play_state.draw(screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        prompt_rect = pygame.Rect(0, 0, 380, 210)
        prompt_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, (30, 30, 30), prompt_rect, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), prompt_rect, 2, border_radius=8)

        title_surf = self.game.font.render("Sleep until tomorrow?", True, "white")
        title_rect = title_surf.get_rect(center=(prompt_rect.centerx, prompt_rect.top + 55))
        screen.blit(title_surf, title_rect)

        button_width = 130
        button_height = 44
        button_gap = 22
        total_width = button_width * 2 + button_gap
        start_x = prompt_rect.centerx - total_width // 2
        y = prompt_rect.top + 115

        for index, option in enumerate(self.options):
            option_rect = pygame.Rect(start_x + index * (button_width + button_gap), y, button_width, button_height)
            is_selected = index == self.selected_index
            bg_color = (70, 120, 180) if is_selected else (45, 45, 45)
            border_color = (240, 240, 240) if is_selected else (100, 100, 100)
            pygame.draw.rect(screen, bg_color, option_rect, border_radius=6)
            pygame.draw.rect(screen, border_color, option_rect, 2, border_radius=6)

            text_surf = self.game.font.render(option, True, "white")
            text_rect = text_surf.get_rect(center=option_rect.center)
            screen.blit(text_surf, text_rect)


class ExamConfirmState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Take Exam", "Cancel"]
        self.selected_index = 0
        self.joystick_latched = False

    def enter(self):
        self.selected_index = 0
        self.joystick_latched = False

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_UP, pygame.K_w):
                self.selected_index = 0
            elif event.key in (
                pygame.K_RIGHT,
                pygame.K_d,
                pygame.K_DOWN,
                pygame.K_s,
            ):
                self.selected_index = 1
            elif event.key in (pygame.K_e, pygame.K_RETURN, pygame.K_SPACE):
                self.select_current_option()

    def update(self):
        direction = self.game.mobile_controls.direction
        if direction.length_squared() < 0.16:
            self.joystick_latched = False
            return

        if self.joystick_latched:
            return

        if abs(direction.x) >= abs(direction.y):
            self.selected_index = 0 if direction.x < 0 else 1
        else:
            self.selected_index = 0 if direction.y < 0 else 1
        self.joystick_latched = True

    def select_current_option(self):
        if self.options[self.selected_index] == "Take Exam":
            self.game.confirm_exam_attempt()
        else:
            self.game.cancel_exam_confirmation()

    def draw(self, screen):
        play_state = self.game.state_machine.states.get(STATE_PLAY)
        if play_state:
            play_state.draw(screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        prompt_rect = pygame.Rect(0, 0, 480, 270)
        prompt_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, (30, 30, 30), prompt_rect, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), prompt_rect, 2, border_radius=8)

        exam = self.game.get_pending_exam()
        if exam is None:
            return
        readiness = self.game.get_exam_readiness(exam)
        title_surf = self.game.font.render(exam.title, True, "white")
        title_rect = title_surf.get_rect(
            center=(prompt_rect.centerx, prompt_rect.top + 42)
        )
        screen.blit(title_surf, title_rect)

        recommended_surf = self.game.font.render(
            f"Recommended: {readiness['recommended_xp']} {exam.skill} XP",
            True,
            (190, 210, 235),
        )
        recommended_rect = recommended_surf.get_rect(
            center=(prompt_rect.centerx, prompt_rect.top + 78)
        )
        screen.blit(recommended_surf, recommended_rect)

        current_surf = self.game.font.render(
            f"Current: {readiness['current_xp']} {exam.skill} XP",
            True,
            (190, 210, 235),
        )
        current_rect = current_surf.get_rect(
            center=(prompt_rect.centerx, prompt_rect.top + 108)
        )
        screen.blit(current_surf, current_rect)

        status_text = (
            "This attempt is risky."
            if readiness["is_risky"]
            else "You meet the recommendation."
        )
        status_color = (255, 184, 108) if readiness["is_risky"] else (142, 220, 150)
        status_surf = self.game.font.render(status_text, True, status_color)
        status_rect = status_surf.get_rect(
            center=(prompt_rect.centerx, prompt_rect.top + 143)
        )
        screen.blit(status_surf, status_rect)

        button_width = 150
        button_height = 44
        button_gap = 24
        total_width = button_width * 2 + button_gap
        start_x = prompt_rect.centerx - total_width // 2
        y = prompt_rect.top + 185

        for index, option in enumerate(self.options):
            option_rect = pygame.Rect(
                start_x + index * (button_width + button_gap),
                y,
                button_width,
                button_height,
            )
            is_selected = index == self.selected_index
            bg_color = (70, 120, 180) if is_selected else (45, 45, 45)
            border_color = (240, 240, 240) if is_selected else (100, 100, 100)
            pygame.draw.rect(screen, bg_color, option_rect, border_radius=6)
            pygame.draw.rect(screen, border_color, option_rect, 2, border_radius=6)

            text_surf = self.game.font.render(option, True, "white")
            text_rect = text_surf.get_rect(center=option_rect.center)
            screen.blit(text_surf, text_rect)


class PlannerState(State):
    PANEL_RECT = pygame.Rect(32, 24, SCREEN_WIDTH - 64, SCREEN_HEIGHT - 48)
    SECTION_RECTS = {
        "Today's Schedule": pygame.Rect(56, 170, 332, 130),
        "Assignments": pygame.Rect(56, 312, 332, 220),
        "Upcoming Exams": pygame.Rect(412, 170, 332, 160),
        "Grade Standing": pygame.Rect(412, 342, 332, 85),
        "Current Objective": pygame.Rect(412, 439, 332, 105),
    }

    def __init__(self, game):
        super().__init__(game)
        self.panel_rect = self.PANEL_RECT.copy()
        self.section_rects = {
            title: rect.copy() for title, rect in self.SECTION_RECTS.items()
        }
        self.title_font = self.create_font(34, bold=True)
        self.section_font = self.create_font(20, bold=True)
        self.body_font = self.create_font(18)
        self.small_font = self.create_font(16)

    @staticmethod
    def create_font(size, bold=False):
        try:
            return pygame.font.SysFont("Arial", size, bold=bold)
        except pygame.error:
            return pygame.font.Font(None, size)

    def get_sections(self):
        classes = self.game.get_today_classes()
        schedule_lines = [entry.summary_label() for entry in classes]
        if not schedule_lines:
            schedule_lines = ["No classes scheduled today."]

        assignments = sorted(
            (
                assignment
                for assignment in self.game.state.assignments
                if assignment.is_active
                and assignment.assigned_day <= self.game.current_day
            ),
            key=lambda assignment: (assignment.due_day, assignment.assigned_day),
        )
        assignment_lines = [assignment.summary_label() for assignment in assignments]
        if not assignment_lines:
            assignment_lines = ["No active assignments."]

        exams = sorted(
            (exam for exam in self.game.state.exams if exam.is_pending),
            key=lambda exam: (exam.scheduled_day, exam.title),
        )
        exam_lines = [exam.summary_label() for exam in exams]
        if not exam_lines:
            exam_lines = ["No upcoming exams."]

        objective = self.game.quest_manager.current_objective
        objective_lines = [objective] if objective else ["No active objective."]

        return {
            "Today's Schedule": schedule_lines,
            "Assignments": assignment_lines,
            "Upcoming Exams": exam_lines,
            "Grade Standing": [
                f"{self.game.grade_standing}/{MAX_GRADE_STANDING}"
            ],
            "Current Objective": objective_lines,
        }

    def draw(self, screen):
        play_state = self.game.state_machine.states.get(STATE_PLAY)
        if play_state:
            play_state.draw(screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 10, 22, 235))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (20, 31, 52), self.panel_rect, border_radius=18)
        pygame.draw.rect(screen, (121, 174, 255), self.panel_rect, 2, border_radius=18)

        title = self.title_font.render("Student Planner", True, "white")
        screen.blit(title, (self.panel_rect.left + 24, self.panel_rect.top + 18))

        day_text = f"Day {self.game.current_day} - {self.game.current_weekday}"
        day_surf = self.body_font.render(day_text, True, (177, 204, 240))
        screen.blit(day_surf, (self.panel_rect.left + 26, self.panel_rect.top + 62))

        close_surf = self.small_font.render(
            "P / Esc / Planner button to close", True, (177, 204, 240)
        )
        close_rect = close_surf.get_rect(
            bottomleft=(self.panel_rect.left + 24, self.panel_rect.bottom - 10)
        )
        screen.blit(close_surf, close_rect)

        for title_text, lines in self.get_sections().items():
            self.draw_section(screen, title_text, lines, self.section_rects[title_text])

    def draw_section(self, screen, title, lines, rect):
        pygame.draw.rect(screen, (31, 47, 75), rect, border_radius=10)
        pygame.draw.rect(screen, (77, 112, 158), rect, 1, border_radius=10)

        title_surf = self.section_font.render(title, True, (151, 202, 255))
        screen.blit(title_surf, (rect.left + 14, rect.top + 10))

        line_y = rect.top + 42
        max_width = rect.width - 28
        max_bottom = rect.bottom - 10
        for line in lines:
            wrapped = DialogueState.wrap_text(line, self.body_font, max_width, 2)
            for wrapped_line in wrapped:
                if line_y + self.body_font.get_linesize() > max_bottom:
                    ellipsis = self.body_font.render("...", True, "white")
                    screen.blit(ellipsis, (rect.left + 14, line_y))
                    return
                line_surf = self.body_font.render(wrapped_line, True, "white")
                screen.blit(line_surf, (rect.left + 14, line_y))
                line_y += self.body_font.get_linesize()
            line_y += 4


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Resume", "Save Game", "Load Game", "Quit Game"]
        self.selected_index = 0

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                self.select_current_option()

    def select_current_option(self):
        selected = self.options[self.selected_index]
        if selected == "Resume":
            self.game.close_menu()
        elif selected == "Save Game":
            self.game.save_game()
        elif selected == "Load Game":
            self.game.load_game()
        elif selected == "Quit Game":
            self.game.running = False

    def draw(self, screen):
        previous_state = self.game.state_machine.states.get(self.game.previous_state_before_menu)
        if previous_state and previous_state != self:
            previous_state.draw(screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        menu_rect = pygame.Rect(0, 0, 320, 340)
        menu_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, (30, 30, 30), menu_rect, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), menu_rect, 2, border_radius=8)

        try:
            title_font = pygame.font.SysFont('Arial', 36, bold=True)
        except pygame.error:
            title_font = pygame.font.Font(None, 36)

        title_surf = title_font.render("Paused", True, 'white')
        title_rect = title_surf.get_rect(center=(menu_rect.centerx, menu_rect.top + 45))
        screen.blit(title_surf, title_rect)

        for index, option in enumerate(self.options):
            option_rect = pygame.Rect(menu_rect.left + 40, menu_rect.top + 95 + index * 55, menu_rect.width - 80, 40)
            is_selected = index == self.selected_index
            bg_color = (70, 120, 180) if is_selected else (45, 45, 45)
            border_color = (240, 240, 240) if is_selected else (100, 100, 100)
            pygame.draw.rect(screen, bg_color, option_rect, border_radius=6)
            pygame.draw.rect(screen, border_color, option_rect, 2, border_radius=6)

            text_surf = self.game.font.render(option, True, 'white')
            text_rect = text_surf.get_rect(center=option_rect.center)
            screen.blit(text_surf, text_rect)
