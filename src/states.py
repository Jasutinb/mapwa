import pygame
from src.state import State
from src.config import (
    ROOM_INTRAMUROS,
    ROOM_MAIN,
    ROOM_OUTSIDE,
    ROOM_SCHOOL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
)

class PlayState(State):
    def handle_events(self, events):
        if self.game.player.studying:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # Try to start interaction
                    if self.game.current_room == ROOM_MAIN and hasattr(self.game, 'mom') and self.game.mom in self.game.visible_sprites and self.game.check_proximity(self.game.player, self.game.mom, 64):
                        self.game.talk_to_mom()
                    elif self.game.current_room in (ROOM_OUTSIDE, ROOM_SCHOOL, ROOM_INTRAMUROS) and hasattr(self.game, 'bus') and self.game.check_proximity(self.game.player, self.game.bus, 100):
                        self.game.ride_bus()
                    elif self.game.current_room == ROOM_SCHOOL and hasattr(self.game, 'school_desk') and self.game.check_proximity(self.game.player, self.game.school_desk, 64):
                        self.game.study_at_school()
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
            self.game.show_dialogue(["You studied hard and gained 10 XP!"])
        
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
                text = "Press E to ride to Intramuros (20)"
            elif self.game.current_room == ROOM_INTRAMUROS:
                if self.game.player.rect.centerx < self.game.bus.rect.centerx:
                    text = "Press E to ride back to Outside"
                else:
                    text = "Press E to ride to School"
            else:
                text = "Press E to ride back"
            
            hint_surf = self.game.font.render(text, True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.bus.rect.centerx, self.game.bus.rect.top - 20))
            screen.blit(hint_surf, hint_rect)

        if self.game.current_room == ROOM_SCHOOL and hasattr(self.game, 'school_desk') and self.game.check_proximity(self.game.player, self.game.school_desk, 64):
            hint_surf = self.game.font.render("Press E to study", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.game.school_desk.rect.centerx, self.game.school_desk.rect.top - 20))
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
