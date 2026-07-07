import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.assignments import ASSIGNMENT_STATUS_COMPLETED, ASSIGNMENT_STATUS_MISSED
from src.config import (
    ASSIGNMENT_MISSED_STRESS,
    ASSIGNMENT_NONE_AVAILABLE_DIALOGUE,
    ASSIGNMENT_REWARD_XP,
    GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE,
    LIBRARY_STUDY_XP,
    MAX_ENERGY,
    ROOM_LIBRARY,
    SKILL_ACADEMICS,
    SKILL_MATH,
)
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, {"key": key})])


def move_to_assignment_marker(game):
    game.current_room = ROOM_LIBRARY
    game.create_map()
    game.visible_sprites.add(game.player)
    game.player.rect.center = game.assignment_marker.rect.center


def test_assignments_initialize_with_required_fields(game):
    assignments = game.state.assignments

    assert assignments
    for assignment in assignments:
        assert assignment.assignment_id
        assert assignment.title
        assert assignment.skill
        assert assignment.assigned_day <= assignment.due_day
        assert assignment.reward_xp == ASSIGNMENT_REWARD_XP
        assert assignment.is_active


def test_assignment_summary_returns_next_due_assignment(game):
    assert game.get_assignment_summary() == (
        "Assignments: Academics Reflection due Day 2"
    )


def test_assignment_marker_is_non_blocking_in_library(game):
    game.current_room = ROOM_LIBRARY
    game.create_map()

    assert game.assignment_marker in game.visible_sprites
    assert game.assignment_marker in game.assignment_marker_sprites
    assert game.assignment_marker not in game.obstacle_sprites


def test_complete_assignment_at_marker_grants_reward(game):
    move_to_assignment_marker(game)

    press_key(game, pygame.K_e)

    assignment = game.state.assignments[0]
    assert assignment.status == ASSIGNMENT_STATUS_COMPLETED
    assert game.get_skill_xp(SKILL_ACADEMICS) == ASSIGNMENT_REWARD_XP
    assert game.current_dialogue == [
        (
            "You completed Academics Reflection and gained "
            f"{ASSIGNMENT_REWARD_XP} academics XP! Total: {ASSIGNMENT_REWARD_XP}."
        )
    ]


def test_completed_assignment_does_not_reward_twice(game):
    move_to_assignment_marker(game)

    assert game.complete_assignment() is True
    assert game.complete_assignment() is False

    assert game.get_skill_xp(SKILL_ACADEMICS) == ASSIGNMENT_REWARD_XP
    assert game.current_dialogue == [ASSIGNMENT_NONE_AVAILABLE_DIALOGUE]


def test_sleep_marks_missed_assignment_and_increases_stress(game):
    game.current_day = 2

    game.sleep_until_next_day()

    assignment = game.state.assignments[0]
    assert game.current_day == 3
    assert assignment.status == ASSIGNMENT_STATUS_MISSED
    assert assignment.missed_stress_applied is True
    assert game.stress == ASSIGNMENT_MISSED_STRESS
    assert game.current_dialogue == [
        "You slept through the night. Day 3 begins.",
        (
            "You missed 1 assignment deadline(s). "
            f"Stress increased by {ASSIGNMENT_MISSED_STRESS}. "
            f"Grade Standing decreased by {GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE}."
        ),
    ]


def test_missed_assignment_stress_applies_once(game):
    game.current_day = 2

    game.sleep_until_next_day()
    stress_after_miss = game.stress
    game.sleep_until_next_day()

    assert game.stress == max(0, stress_after_miss - 20)
    assert game.current_dialogue == ["You slept through the night. Day 4 begins."]


def test_mobile_action_completes_assignment(game):
    move_to_assignment_marker(game)
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.state.assignments[0].status == ASSIGNMENT_STATUS_COMPLETED
    assert game.get_skill_xp(SKILL_ACADEMICS) == ASSIGNMENT_REWARD_XP


def test_assignment_hud_is_not_persistent_in_default_view(game):
    game.draw()

    assert game.assignment_hud_rect.size == (0, 0)


def test_library_study_station_still_studies(game):
    game.current_room = ROOM_LIBRARY
    game.create_map()
    game.energy = MAX_ENERGY
    game.player.rect.center = game.library_math_station.rect.center

    press_key(game, pygame.K_e)

    assert game.get_skill_xp(SKILL_MATH) == LIBRARY_STUDY_XP
    assert game.get_skill_xp(SKILL_ACADEMICS) == 0
    assert game.state.assignments[0].is_active
