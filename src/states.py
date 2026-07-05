import pygame
from src.state import State
from src.transport import BUS_TRANSPORT
from src.config import (
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
                    elif self.game.current_room in (ROOM_OUTSIDE, ROOM_SCHOOL, ROOM_INTRAMUROS) and hasattr(self.game, 'bus') and self.game.check_proximity(self.game.player, self.game.bus, 100):
                        self.game.ride_bus()
                    elif self.game.current_room == ROOM_SCHOOL_ENTRANCE and self.game.try_enter_school_gate():
                        pass
                    elif self.game.current_room == ROOM_SCHOOL_ENTRANCE and self.game.talk_to_guard():
                        pass
                    elif self.game.current_room == ROOM_ADMIN_OFFICE and self.game.talk_to_attendant():
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
        
        if self.game.current_room in (ROOM_OUTSIDE, ROOM_SCHOOL, ROOM_INTRAMUROS) and hasattr(self.game, 'bus') and self.game.check_proximity(self.game.player, self.game.bus, 100):
            if self.game.current_room == ROOM_OUTSIDE:
                text = f"Press E to ride to Intramuros ({BUS_TRANSPORT.fare_label()})"
            elif self.game.current_room == ROOM_INTRAMUROS:
                text = f"Press E to ride back to Outside ({BUS_TRANSPORT.fare_label()})"
            else:
                text = f"Press E to ride back ({BUS_TRANSPORT.fare_label()})"
            
            hint_surf = self.game.font.render(text, True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.bus.rect.centerx, self.game.bus.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_SCHOOL and hasattr(self.game, 'school_desk') and self.game.check_proximity(self.game.player, self.game.school_desk, 64):
            hint_surf = self.game.font.render("Press E to study", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.school_desk.rect.centerx, self.game.school_desk.rect.top - 20))
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
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.game.advance_dialogue()

    def draw(self, screen):
        # Draw dialogue box
        if self.game.current_dialogue:
            box_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
            pygame.draw.rect(screen, (30, 30, 30), box_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), box_rect, 2, border_radius=10)
            
            text_surf = self.game.font.render(self.game.current_dialogue[self.game.dialogue_index], True, 'white')
            screen.blit(text_surf, (box_rect.x + 20, box_rect.y + 20))
            
            prompt_surf = self.game.font.render("Press E to continue...", True, (150, 150, 150))
            screen.blit(prompt_surf, (box_rect.right - 180, box_rect.bottom - 30))


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


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Resume", "Quit Game"]
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
        elif selected == "Quit Game":
            self.game.running = False

    def draw(self, screen):
        previous_state = self.game.state_machine.states.get(self.game.previous_state_before_menu)
        if previous_state and previous_state != self:
            previous_state.draw(screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        menu_rect = pygame.Rect(0, 0, 320, 230)
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
