import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE,
    LIBRARY_STUDY_ENERGY_COST,
    LOW_ENERGY_STRESS_DIALOGUE,
    LOW_ENERGY_STRESS_INCREASE,
    MAX_ENERGY,
    MAX_STRESS,
    MEAL_ENERGY,
    MEAL_PRICE,
    MIN_STRESS,
    ROOM_CAFETERIA,
    ROOM_LIBRARY,
    ROOM_SCHOOL,
    SCHOOL_STUDY_ENERGY_COST,
    SLEEP_STRESS_RECOVERY,
    STARTING_STRESS,
)
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def test_stress_starts_at_configured_baseline(game):
    assert game.stress == STARTING_STRESS


def test_stress_is_clamped(game):
    game.stress = MAX_STRESS + 10
    assert game.stress == MAX_STRESS

    game.stress = MIN_STRESS - 10
    assert game.stress == MIN_STRESS


def test_stress_helpers_return_actual_change(game):
    game.stress = MAX_STRESS - 2

    increased = game.increase_stress(LOW_ENERGY_STRESS_INCREASE)

    assert increased == 2
    assert game.stress == MAX_STRESS

    recovered = game.reduce_stress(MAX_STRESS + 10)

    assert recovered == MAX_STRESS
    assert game.stress == MIN_STRESS


def test_sleep_reduces_stress_and_restores_energy(game):
    game.stress = SLEEP_STRESS_RECOVERY + 3
    game.energy = 1

    game.sleep_until_next_day()

    assert game.current_day == 2
    assert game.stress == 3
    assert game.energy == MAX_ENERGY


def test_low_energy_school_study_increases_stress(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.energy = SCHOOL_STUDY_ENERGY_COST - 1
    game.player.rect.center = game.school_desk.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.stress == LOW_ENERGY_STRESS_INCREASE
    assert game.energy == SCHOOL_STUDY_ENERGY_COST - 1
    assert game.player.studying is False
    assert game.current_dialogue[-1] == LOW_ENERGY_STRESS_DIALOGUE.format(
        amount=LOW_ENERGY_STRESS_INCREASE
    )


def test_mobile_low_energy_library_study_increases_stress(game):
    game.current_room = ROOM_LIBRARY
    game.create_map()
    game.energy = LIBRARY_STUDY_ENERGY_COST - 1
    game.player.rect.center = game.library_math_station.rect.center
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.stress == LOW_ENERGY_STRESS_INCREASE
    assert game.energy == LIBRARY_STUDY_ENERGY_COST - 1


def test_insufficient_money_does_not_increase_stress(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE - 1
    game.energy = MAX_ENERGY - MEAL_ENERGY
    game.stress = 7

    game.buy_cafeteria_meal()

    assert game.stress == 7
    assert game.current_dialogue == CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE


def test_stress_hud_does_not_overlap_existing_ui(game):
    game.draw()

    assert game.stress_hud_rect.width > 0
    assert not game.stress_hud_rect.colliderect(game.energy_hud_rect)
    assert not game.stress_hud_rect.colliderect(game.inventory.rect)
    assert not game.stress_hud_rect.colliderect(game.mobile_controls.rects["action"])
