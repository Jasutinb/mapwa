import pygame
from src.config import (
    BUS_FARE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STUDY_DURATION_FRAMES,
    TILE_SIZE,
)
from src.state import State


class PlayState(State):
    def handle_events(self, events):
        if self.game.player.studying:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # Try to start interaction
                    if (
                        self.game.current_room == "main"
                        and hasattr(self.game, "mom")
                        and self.game.mom in self.game.visible_sprites
                        and self.game.check_proximity(
                            self.game.player, self.game.mom, 64
                        )
                    ):
                        self.game.current_dialogue = self.game.mom.interact()
                        self.game.current_dialogue_source = "mom"
                        self.game.dialogue_index = 0
                        self.game.state_machine.change_state("dialogue")
                    elif (
                        (
                            self.game.current_room == "outside"
                            or self.game.current_room == "school"
                            or self.game.current_room == "intramuros"
                        )
                        and hasattr(self.game, "bus")
                        and self.game.check_proximity(
                            self.game.player, self.game.bus, 100
                        )
                    ):
                        current_node = self.game.rooms.get(self.game.current_room)
                        if self.game.current_room == "outside":
                            if self.game.money >= BUS_FARE:
                                self.game.money -= BUS_FARE
                                if current_node and current_node.right:
                                    self.game.current_room = current_node.right.name
                                else:
                                    self.game.current_room = "intramuros"
                                self.game.create_map()
                                self.game.player.rect.center = (
                                    SCREEN_WIDTH // 2,
                                    SCREEN_HEIGHT // 2,
                                )
                                self.game.visible_sprites.add(self.game.player)
                            else:
                                self.game.current_dialogue = [
                                    f"I don't have enough money for the bus... (Need {BUS_FARE})"
                                ]
                                self.game.current_dialogue_source = "bus"
                                self.game.dialogue_index = 0
                                self.game.state_machine.change_state("dialogue")
                        elif self.game.current_room == "intramuros":
                            # To distinguish between going to school or going back to outside
                            if (
                                self.game.player.rect.centerx
                                < self.game.bus.rect.centerx
                            ):
                                if current_node and current_node.left:
                                    self.game.current_room = current_node.left.name
                                else:
                                    self.game.current_room = "outside"
                            else:
                                if current_node and current_node.right:
                                    self.game.current_room = current_node.right.name
                                else:
                                    self.game.current_room = "school"

                            self.game.create_map()
                            self.game.player.rect.center = (
                                SCREEN_WIDTH // 2,
                                SCREEN_HEIGHT // 2,
                            )
                            self.game.visible_sprites.add(self.game.player)
                        else:  # From school
                            if current_node and current_node.left:
                                self.game.current_room = current_node.left.name
                            else:
                                self.game.current_room = "intramuros"
                            self.game.create_map()
                            self.game.player.rect.center = (
                                SCREEN_WIDTH // 2,
                                SCREEN_HEIGHT // 2,
                            )
                            self.game.visible_sprites.add(self.game.player)
                    elif (
                        self.game.current_room in {"outside", "intramuros"}
                        and hasattr(self.game, "interactable_sprites")
                    ):
                        hits = [
                            sprite
                            for sprite in self.game.interactable_sprites
                            if self.game.check_proximity(self.game.player, sprite, 64)
                        ]
                        if hits:
                            interactable = hits[0]
                            self.game.current_dialogue = interactable.interact()
                            self.game.current_dialogue_source = getattr(
                                interactable, "kind", self.game.current_room
                            )
                            self.game.dialogue_index = 0
                            self.game.state_machine.change_state("dialogue")
                        else:
                            self.try_pick_up_item()
                    elif (
                        self.game.current_room == "school"
                        and hasattr(self.game, "school_desk")
                        and self.game.check_proximity(
                            self.game.player, self.game.school_desk, 64
                        )
                    ):
                        self.game.experience += 10
                        self.game.player.start_study(STUDY_DURATION_FRAMES)
                    else:
                        self.try_pick_up_item()

    def try_pick_up_item(self):
        hits = pygame.sprite.spritecollide(
            self.game.player, self.game.item_sprites, False
        )
        for item in hits:
            if self.game.inventory.add_item(item):
                self.game.mark_item_collected(item)
                item.kill()
                self.game.current_dialogue = [f"You picked up a {item.name}!"]
                self.game.current_dialogue_source = "item"
                self.game.dialogue_index = 0
                self.game.state_machine.change_state("dialogue")
                break

    def update(self):
        # Store previous studying state to detect when it finishes
        was_studying = self.game.player.studying

        self.game.visible_sprites.update()
        self.game.check_transitions()

        # If studying just finished, show dialogue
        if was_studying and not self.game.player.studying:
            self.game.current_dialogue = ["You studied hard and gained 10 XP!"]
            self.game.current_dialogue_source = "study"
            self.game.dialogue_index = 0
            self.game.state_machine.change_state("dialogue")

        # Constrain Mom within boundaries if she's in the current room
        if (
            self.game.current_room == "main"
            and hasattr(self.game, "mom")
            and self.game.mom in self.game.visible_sprites
        ):
            self.game.mom.rect.left = max(
                0, min(self.game.mom.rect.left, SCREEN_WIDTH - self.game.mom.rect.width)
            )
            self.game.mom.rect.top = max(
                TILE_SIZE * 2,
                min(self.game.mom.rect.top, SCREEN_HEIGHT - self.game.mom.rect.height),
            )

    def draw(self, screen):
        # Draw proximity hint
        if self.game.current_room == "main" and self.game.check_proximity(
            self.game.player, self.game.mom, 64
        ):
            hint_surf = self.game.font.render("Press E to talk", True, "white")
            hint_rect = hint_surf.get_rect(
                center=(self.game.mom.rect.centerx, self.game.mom.rect.top - 20)
            )
            screen.blit(hint_surf, hint_rect)

        if (
            (
                self.game.current_room == "outside"
                or self.game.current_room == "school"
                or self.game.current_room == "intramuros"
            )
            and hasattr(self.game, "bus")
            and self.game.check_proximity(self.game.player, self.game.bus, 100)
        ):
            if self.game.current_room == "outside":
                text = f"Press E to ride to Intramuros ({BUS_FARE})"
            elif self.game.current_room == "intramuros":
                if self.game.player.rect.centerx < self.game.bus.rect.centerx:
                    text = "Press E to ride back to Outside"
                else:
                    text = "Press E to ride to School"
            else:
                text = "Press E to ride back"

            hint_surf = self.game.font.render(text, True, "white")
            hint_rect = hint_surf.get_rect(
                center=(self.game.bus.rect.centerx, self.game.bus.rect.top - 20)
            )
            screen.blit(hint_surf, hint_rect)

        if (
            self.game.current_room == "school"
            and hasattr(self.game, "school_desk")
            and self.game.check_proximity(self.game.player, self.game.school_desk, 64)
        ):
            hint_surf = self.game.font.render("Press E to study", True, "white")
            hint_rect = hint_surf.get_rect(
                center=(
                    self.game.school_desk.rect.centerx,
                    self.game.school_desk.rect.top - 20,
                )
            )
            screen.blit(hint_surf, hint_rect)

        if (
            self.game.current_room in {"outside", "intramuros"}
            and hasattr(self.game, "interactable_sprites")
        ):
            interactable_hits = [
                sprite
                for sprite in self.game.interactable_sprites
                if self.game.check_proximity(self.game.player, sprite, 64)
            ]
            if interactable_hits:
                interactable = interactable_hits[0]
                if getattr(interactable, "kind", None) in {
                    "shop",
                    "bus_stop",
                    "vendor",
                    "guard_booth",
                    "school_gate",
                }:
                    text = f"Press E to check {interactable.name}"
                else:
                    text = "Press E to talk"
                hint_surf = self.game.font.render(text, True, "white")
                hint_rect = hint_surf.get_rect(
                    center=(interactable.rect.centerx, interactable.rect.top - 20)
                )
                screen.blit(hint_surf, hint_rect)

        # Draw item interaction hint
        item_hits = pygame.sprite.spritecollide(
            self.game.player, self.game.item_sprites, False
        )
        if item_hits:
            item = item_hits[0]
            hint_surf = self.game.font.render(
                f"Press E to pick up {item.name}", True, "white"
            )
            hint_rect = hint_surf.get_rect(
                center=(item.rect.centerx, item.rect.top - 20)
            )
            screen.blit(hint_surf, hint_rect)


class DialogueState(State):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.game.current_dialogue:
                        # Advance dialogue
                        self.game.dialogue_index += 1
                        if self.game.dialogue_index >= len(self.game.current_dialogue):
                            dialogue_source = self.game.current_dialogue_source
                            self.game.current_dialogue = None
                            self.game.current_dialogue_source = None
                            self.game.dialogue_index = 0
                            # Update Mom's dialogue after the first talk
                            if (
                                dialogue_source == "mom"
                                and self.game.has_talked_to_mom
                            ):
                                self.game.mom.dialogue = [
                                    "Hi sweetie!",
                                    "Make sure to study hard!",
                                    "I'll see you later.",
                                ]
                            self.game.state_machine.change_state("play")
                        elif (
                            self.game.current_dialogue_source == "mom"
                            and not self.game.has_talked_to_mom
                            and self.game.dialogue_index
                            == len(self.game.current_dialogue) - 1
                        ):
                            # If it's the last line of the first talk, give money
                            self.game.money += 250
                            self.game.has_talked_to_mom = True

    def draw(self, screen):
        # Draw dialogue box
        if self.game.current_dialogue:
            box_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
            pygame.draw.rect(screen, (30, 30, 30), box_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), box_rect, 2, border_radius=10)

            text_surf = self.game.font.render(
                self.game.current_dialogue[self.game.dialogue_index], True, "white"
            )
            screen.blit(text_surf, (box_rect.x + 20, box_rect.y + 20))

            prompt_surf = self.game.font.render(
                "Press E to continue...", True, (150, 150, 150)
            )
            screen.blit(prompt_surf, (box_rect.right - 180, box_rect.bottom - 30))
