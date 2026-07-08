import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    CAFETERIA_FULL_ENERGY_DIALOGUE,
    CAFETERIA_FINANCE_XP,
    CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE,
    MAX_ENERGY,
    MEAL_ENERGY,
    MEAL_PRICE,
    ROOM_CAFETERIA,
    ROOM_LIBRARY,
    ROOM_PROGRAMMING_LAB,
    ROOM_ELECTRONICS_LAB,
    ROOM_SCHOOL,
    ROOM_SCHOOL_ENTRANCE,
)
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def test_energy_starts_capped(game):
    assert game.energy == MAX_ENERGY
    game.energy = MAX_ENERGY + 10
    assert game.energy == MAX_ENERGY
    game.energy = -5
    assert game.energy == 0


def test_school_has_existing_routes_and_clear_door_to_cafeteria(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()

    assert game.rooms[ROOM_SCHOOL].left.name == ROOM_SCHOOL_ENTRANCE
    assert game.rooms[ROOM_SCHOOL].up.name == ROOM_PROGRAMMING_LAB
    assert game.rooms[ROOM_SCHOOL].right.name == ROOM_ELECTRONICS_LAB
    assert game.rooms[ROOM_SCHOOL].down.name == ROOM_LIBRARY

    cafeteria_door = next(s for s in game.door_sprites if s.target_room == ROOM_CAFETERIA)
    game.player.rect.topleft = cafeteria_door.rect.topleft

    game.update()

    assert game.current_room == ROOM_CAFETERIA
    assert game.player.rect.topleft == cafeteria_door.spawn_pos
    assert hasattr(game, "food_vendor")
    assert not pygame.sprite.spritecollide(game.player, game.obstacle_sprites, False)


def test_cafeteria_exit_returns_to_clear_school_path(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()

    school_door = next(s for s in game.door_sprites if s.target_room == ROOM_SCHOOL)
    game.player.rect.topleft = school_door.rect.topleft

    game.update()

    assert game.current_room == ROOM_SCHOOL
    assert game.player.rect.topleft == school_door.spawn_pos
    assert hasattr(game, "school_desk")
    assert not pygame.sprite.spritecollide(game.player, game.obstacle_sprites, False)


def test_cafeteria_purchase_restores_energy_and_charges_money(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY - MEAL_ENERGY
    game.player.rect.center = game.food_vendor.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.money == 0
    assert game.energy == MAX_ENERGY
    assert game.current_dialogue == [
        f"You bought a meal for {MEAL_PRICE} and restored {MEAL_ENERGY} energy. "
        f"Energy: {MAX_ENERGY}/{MAX_ENERGY}. "
        f"Budgeting practice: +{CAFETERIA_FINANCE_XP} finance XP. "
        f"Total: {CAFETERIA_FINANCE_XP}."
    ]


def test_cafeteria_purchase_caps_energy_restore(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY - 5
    game.player.rect.center = game.food_vendor.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.money == 0
    assert game.energy == MAX_ENERGY
    assert "restored 5 energy" in game.current_dialogue[0]


def test_cafeteria_purchase_blocks_without_enough_money(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE - 1
    game.energy = MAX_ENERGY - MEAL_ENERGY
    game.player.rect.center = game.food_vendor.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.money == MEAL_PRICE - 1
    assert game.energy == MAX_ENERGY - MEAL_ENERGY
    assert game.current_dialogue == CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE


def test_cafeteria_purchase_blocks_at_full_energy(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY
    game.player.rect.center = game.food_vendor.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.money == MEAL_PRICE
    assert game.energy == MAX_ENERGY
    assert game.current_dialogue == CAFETERIA_FULL_ENERGY_DIALOGUE


def test_mobile_action_button_triggers_cafeteria_purchase(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY - MEAL_ENERGY
    game.player.rect.center = game.food_vendor.rect.center
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.money == 0
    assert game.energy == MAX_ENERGY


def test_energy_hud_does_not_overlap_bottom_ui(game):
    game.draw()

    assert game.energy_hud_rect.width > 0
    assert not game.energy_hud_rect.colliderect(game.inventory.rect)
    assert not game.energy_hud_rect.colliderect(game.mobile_controls.rects["action"])
