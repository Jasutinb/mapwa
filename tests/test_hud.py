import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def test_default_hud_shows_only_urgent_state(game):
    game.draw()

    assert game.money_hud_rect.width > 0
    assert game.objective_hud_rect.width > 0
    assert game.energy_hud_rect.width > 0
    assert game.stress_hud_rect.width > 0
    assert game.get_current_objective_summary().startswith("Objective: ")
    assert game.schedule_hud_rect.size == (0, 0)
    assert game.assignment_hud_rect.size == (0, 0)
    assert game.exam_hud_rect.size == (0, 0)
    assert game.grade_hud_rect.size == (0, 0)


def test_default_objective_uses_active_quest(game):
    assert game.get_current_objective_summary() == "Objective: Pick up your Student ID."


def test_urgent_hud_avoids_controls_and_inventory(game):
    game.draw()

    urgent_rects = (
        game.money_hud_rect,
        game.objective_hud_rect,
        game.energy_hud_rect,
        game.stress_hud_rect,
    )
    for hud_rect in urgent_rects:
        assert not hud_rect.colliderect(game.inventory.rect)
        assert not hud_rect.colliderect(game.mobile_controls.rects["action"])

    assert not game.objective_hud_rect.colliderect(game.energy_hud_rect)
    assert not game.objective_hud_rect.colliderect(game.stress_hud_rect)
    assert not game.energy_hud_rect.colliderect(game.stress_hud_rect)
