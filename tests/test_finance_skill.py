import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from src.config import (
    CAFETERIA_FINANCE_XP,
    CAFETERIA_FULL_ENERGY_DIALOGUE,
    CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE,
    MAX_ENERGY,
    MEAL_ENERGY,
    MEAL_PRICE,
    ROOM_CAFETERIA,
    ROOM_SCHOOL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKILL_FINANCE,
    TRACKED_SKILLS,
)
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    g = Game()
    yield g
    pygame.quit()


def buy_meal(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY - MEAL_ENERGY
    game.player.rect.center = game.food_vendor.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])


def test_finance_is_initialized_as_tracked_skill(game):
    assert SKILL_FINANCE in TRACKED_SKILLS
    assert SKILL_FINANCE in game.skill_xp_manager.xp_by_skill
    assert game.get_skill_xp(SKILL_FINANCE) == 0


def test_successful_cafeteria_purchase_grants_finance_xp(game):
    buy_meal(game)

    assert game.money == 0
    assert game.energy == MAX_ENERGY
    assert game.get_skill_xp(SKILL_FINANCE) == CAFETERIA_FINANCE_XP
    assert game.current_dialogue == [
        f"You bought a meal for {MEAL_PRICE} and restored {MEAL_ENERGY} energy. "
        f"Energy: {MAX_ENERGY}/{MAX_ENERGY}. "
        f"Budgeting practice: +{CAFETERIA_FINANCE_XP} finance XP. "
        f"Total: {CAFETERIA_FINANCE_XP}."
    ]


def test_failed_cafeteria_purchase_without_money_grants_no_finance_xp(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE - 1
    game.energy = MAX_ENERGY - MEAL_ENERGY
    game.player.rect.center = game.food_vendor.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.money == MEAL_PRICE - 1
    assert game.energy == MAX_ENERGY - MEAL_ENERGY
    assert game.get_skill_xp(SKILL_FINANCE) == 0
    assert game.current_dialogue == CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE


def test_full_energy_cafeteria_attempt_grants_no_finance_xp(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY
    game.player.rect.center = game.food_vendor.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.money == MEAL_PRICE
    assert game.energy == MAX_ENERGY
    assert game.get_skill_xp(SKILL_FINANCE) == 0
    assert game.current_dialogue == CAFETERIA_FULL_ENERGY_DIALOGUE


def test_finance_xp_persists_through_room_transition(game):
    buy_meal(game)
    game.finish_dialogue()

    game.travel_to_room(ROOM_SCHOOL)

    assert game.current_room == ROOM_SCHOOL
    assert game.get_skill_xp(SKILL_FINANCE) == CAFETERIA_FINANCE_XP


def test_mobile_cafeteria_purchase_grants_finance_xp(game):
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
    assert game.get_skill_xp(SKILL_FINANCE) == CAFETERIA_FINANCE_XP
