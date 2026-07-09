import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from src.config import (
    CAFETERIA_FULL_ENERGY_DIALOGUE,
    CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE,
    MAX_ENERGY,
    MEAL_ENERGY,
    MEAL_HEALTH_XP,
    MEAL_PRICE,
    ROOM_BEDROOM,
    ROOM_CAFETERIA,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKILL_HEALTH,
    SLEEP_HEALTH_XP,
    SLEEP_STRESS_RECOVERY,
    STATE_PLAY,
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


def place_player_at_food_vendor(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.player.rect.center = game.food_vendor.rect.center


def place_player_at_bed(game):
    game.current_room = ROOM_BEDROOM
    game.create_map()
    game.player.rect.center = game.bed.rect.center


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=key)])


def press_mobile_action(game):
    action_pos = game.mobile_controls.rects["action"].center
    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )


def test_health_is_initialized_as_tracked_skill(game):
    assert SKILL_HEALTH in TRACKED_SKILLS
    assert SKILL_HEALTH in game.skill_xp_manager.xp_by_skill
    assert game.get_skill_xp(SKILL_HEALTH) == 0


def test_successful_cafeteria_meal_grants_health_xp_without_energy_regression(game):
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY - MEAL_ENERGY
    starting_stress = game.stress
    place_player_at_food_vendor(game)

    press_key(game, pygame.K_e)

    assert game.money == 0
    assert game.energy == MAX_ENERGY
    assert game.stress == starting_stress
    assert game.get_skill_xp(SKILL_HEALTH) == MEAL_HEALTH_XP


def test_failed_cafeteria_meal_grants_no_health_xp(game):
    game.money = MEAL_PRICE - 1
    game.energy = MAX_ENERGY - MEAL_ENERGY
    place_player_at_food_vendor(game)

    press_key(game, pygame.K_e)

    assert game.money == MEAL_PRICE - 1
    assert game.energy == MAX_ENERGY - MEAL_ENERGY
    assert game.get_skill_xp(SKILL_HEALTH) == 0
    assert game.current_dialogue == CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE


def test_full_energy_cafeteria_attempt_grants_no_health_xp(game):
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY
    place_player_at_food_vendor(game)

    press_key(game, pygame.K_e)

    assert game.money == MEAL_PRICE
    assert game.energy == MAX_ENERGY
    assert game.get_skill_xp(SKILL_HEALTH) == 0
    assert game.current_dialogue == CAFETERIA_FULL_ENERGY_DIALOGUE


def test_sleep_grants_health_xp_and_preserves_rest_effects(game):
    game.energy = 1
    game.stress = SLEEP_STRESS_RECOVERY + 3

    game.sleep_until_next_day()

    assert game.current_day == 2
    assert game.energy == MAX_ENERGY
    assert game.stress == 3
    assert game.get_skill_xp(SKILL_HEALTH) == SLEEP_HEALTH_XP


def test_cancel_sleep_grants_no_health_xp(game):
    place_player_at_bed(game)

    press_key(game, pygame.K_e)
    press_key(game, pygame.K_RIGHT)
    press_key(game, pygame.K_e)

    assert game.current_day == 1
    assert game.state_machine.current_state_name == STATE_PLAY
    assert game.get_skill_xp(SKILL_HEALTH) == 0


def test_mobile_cafeteria_meal_grants_health_xp(game):
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY - MEAL_ENERGY
    place_player_at_food_vendor(game)

    press_mobile_action(game)

    assert game.energy == MAX_ENERGY
    assert game.get_skill_xp(SKILL_HEALTH) == MEAL_HEALTH_XP
