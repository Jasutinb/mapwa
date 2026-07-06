import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    EXAM_ENERGY_COST,
    EXAM_REWARD_XP,
    EXAM_STRESS_PENALTY,
    MAX_ENERGY,
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL,
    SKILL_ACADEMICS,
    SKILL_PROGRAMMING,
)
from src.exams import EXAM_STATUS_PASSED
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


def move_to_exam_marker(game, room, day):
    game.current_day = day
    game.current_room = room
    game.create_map()
    game.visible_sprites.add(game.player)
    marker = next(iter(game.exam_marker_sprites))
    game.player.rect.center = marker.rect.center
    return marker


def test_exams_initialize_with_required_fields(game):
    assert game.state.exams
    for exam in game.state.exams:
        assert exam.exam_id
        assert exam.title
        assert exam.skill
        assert exam.room_key
        assert exam.scheduled_day >= 1
        assert exam.recommended_xp > 0
        assert exam.reward_xp == EXAM_REWARD_XP
        assert exam.energy_cost == EXAM_ENERGY_COST
        assert exam.stress_penalty == EXAM_STRESS_PENALTY
        assert exam.attempts == 0
        assert exam.is_pending


def test_exam_summary_returns_next_pending_exam(game):
    assert game.get_exam_summary() == "Exams: Day 5 Academics Midterm"


def test_exam_markers_are_non_blocking(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()

    assert game.school_exam_marker in game.visible_sprites
    assert game.school_exam_marker in game.exam_marker_sprites
    assert game.school_exam_marker not in game.obstacle_sprites


def test_available_exam_in_matching_room_and_day(game):
    move_to_exam_marker(game, ROOM_SCHOOL, day=5)

    available = game.get_available_exams()

    assert len(available) == 1
    assert available[0].exam_id == "academics-midterm"


def test_exam_before_scheduled_day_is_blocked(game):
    move_to_exam_marker(game, ROOM_SCHOOL, day=4)

    press_key(game, pygame.K_e)

    assert game.state.exams[0].attempts == 0
    assert game.current_dialogue == ["No exams are available here right now."]


def test_passing_exam_grants_reward_and_marks_passed(game):
    move_to_exam_marker(game, ROOM_SCHOOL, day=5)
    game.grant_skill_xp(SKILL_ACADEMICS, 30)

    press_key(game, pygame.K_e)

    exam = game.state.exams[0]
    assert exam.status == EXAM_STATUS_PASSED
    assert exam.attempts == 1
    assert game.energy == MAX_ENERGY - EXAM_ENERGY_COST
    assert game.get_skill_xp(SKILL_ACADEMICS) == 30 + EXAM_REWARD_XP
    assert game.current_dialogue == [
        (
            "You passed Academics Midterm and gained "
            f"{EXAM_REWARD_XP} academics XP! Total: {30 + EXAM_REWARD_XP}."
        )
    ]


def test_failing_exam_increases_stress_and_tracks_attempt(game):
    move_to_exam_marker(game, ROOM_SCHOOL, day=5)
    game.grant_skill_xp(SKILL_ACADEMICS, 10)

    press_key(game, pygame.K_e)

    exam = game.state.exams[0]
    assert exam.is_pending
    assert exam.attempts == 1
    assert game.energy == MAX_ENERGY - EXAM_ENERGY_COST
    assert game.stress == EXAM_STRESS_PENALTY
    assert game.current_dialogue == [
        (
            "You failed Academics Midterm. Recommended 30 academics XP; "
            f"you have 10. Stress increased by {EXAM_STRESS_PENALTY}."
        )
    ]


def test_low_energy_blocks_exam_without_attempt(game):
    move_to_exam_marker(game, ROOM_SCHOOL, day=5)
    game.energy = EXAM_ENERGY_COST - 1

    press_key(game, pygame.K_e)

    assert game.state.exams[0].attempts == 0
    assert game.stress > 0
    assert game.current_dialogue[0] == "You're too tired for that. Eat something or sleep first."


def test_completed_exam_does_not_reward_twice(game):
    move_to_exam_marker(game, ROOM_SCHOOL, day=5)
    game.grant_skill_xp(SKILL_ACADEMICS, 30)

    assert game.take_exam() is True
    assert game.take_exam() is False

    assert game.state.exams[0].attempts == 1
    assert game.get_skill_xp(SKILL_ACADEMICS) == 30 + EXAM_REWARD_XP
    assert game.current_dialogue == ["You already passed Academics Midterm."]


def test_mobile_action_takes_exam(game):
    move_to_exam_marker(game, ROOM_PROGRAMMING_LAB, day=6)
    game.grant_skill_xp(SKILL_PROGRAMMING, 35)
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.state.exams[1].status == EXAM_STATUS_PASSED
    assert game.get_skill_xp(SKILL_PROGRAMMING) == 35 + EXAM_REWARD_XP


def test_sleep_preserves_passed_exam_and_unlocks_next_exam(game):
    game.current_day = 5
    game.grant_skill_xp(SKILL_ACADEMICS, 30)
    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.player.rect.center = game.school_exam_marker.rect.center

    assert game.take_exam() is True

    game.sleep_until_next_day()

    assert game.current_day == 6
    assert game.state.exams[0].status == EXAM_STATUS_PASSED
    assert game.get_exam_summary() == "Exams: Day 6 Programming Practical"


def test_exam_hud_does_not_overlap_existing_ui(game):
    game.draw()

    assert game.exam_hud_rect.width > 0
    assert not game.exam_hud_rect.colliderect(game.schedule_hud_rect)
    assert not game.exam_hud_rect.colliderect(game.assignment_hud_rect)
    assert not game.exam_hud_rect.colliderect(game.energy_hud_rect)
    assert not game.exam_hud_rect.colliderect(game.stress_hud_rect)
    assert not game.exam_hud_rect.colliderect(game.inventory.rect)
    assert not game.exam_hud_rect.colliderect(game.mobile_controls.rects["action"])
