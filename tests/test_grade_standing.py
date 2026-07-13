import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    GRADE_STANDING_ASSIGNMENT_EARLY_BONUS,
    GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE,
    GRADE_STANDING_ASSIGNMENT_SUBMISSION_INCREASE,
    GRADE_STANDING_CLASS_ATTENDANCE_INCREASE,
    GRADE_STANDING_EXAM_FAIL_DECREASE,
    GRADE_STANDING_EXAM_PASS_INCREASE,
    MAX_GRADE_STANDING,
    MIN_GRADE_STANDING,
    ROOM_SCHOOL,
    SKILL_ACADEMICS,
    STARTING_GRADE_STANDING,
)
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def move_to_school_exam_marker(game, day):
    game.current_day = day
    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.visible_sprites.add(game.player)
    game.player.rect.center = game.school_exam_marker.rect.center


def test_grade_standing_initializes_with_default(game):
    assert game.grade_standing == STARTING_GRADE_STANDING
    assert game.state.grade_standing == STARTING_GRADE_STANDING
    assert game.get_grade_summary() == (
        f"Grade Standing: {STARTING_GRADE_STANDING}/{MAX_GRADE_STANDING}"
    )


def test_grade_standing_clamps_to_bounds(game):
    game.grade_standing = MAX_GRADE_STANDING - 2

    assert game.adjust_grade_standing(10) == 2
    assert game.grade_standing == MAX_GRADE_STANDING

    game.grade_standing = MIN_GRADE_STANDING + 2

    assert game.adjust_grade_standing(-10) == -2
    assert game.grade_standing == MIN_GRADE_STANDING


def test_class_reward_reports_actual_clamped_increase(game):
    game.current_day = 1
    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.grade_standing = MAX_GRADE_STANDING

    assert game.attend_class() is True

    assert game.grade_standing == MAX_GRADE_STANDING
    assert game.current_dialogue[0].endswith("Grade Standing increased by 0.")


def test_positive_reward_values_match_approved_balance():
    assert GRADE_STANDING_CLASS_ATTENDANCE_INCREASE == 1
    assert GRADE_STANDING_ASSIGNMENT_SUBMISSION_INCREASE == 3
    assert GRADE_STANDING_ASSIGNMENT_EARLY_BONUS == 1


def test_passing_exam_increases_grade_standing_once(game):
    move_to_school_exam_marker(game, day=5)
    game.grant_skill_xp(SKILL_ACADEMICS, 30)

    assert game.take_exam() is True
    assert game.grade_standing == (
        STARTING_GRADE_STANDING + GRADE_STANDING_EXAM_PASS_INCREASE
    )

    assert game.take_exam() is False
    assert game.grade_standing == (
        STARTING_GRADE_STANDING + GRADE_STANDING_EXAM_PASS_INCREASE
    )


def test_failing_exam_decreases_grade_standing(game):
    move_to_school_exam_marker(game, day=5)
    game.grant_skill_xp(SKILL_ACADEMICS, 10)

    assert game.take_exam() is False
    assert game.grade_standing == (
        STARTING_GRADE_STANDING - GRADE_STANDING_EXAM_FAIL_DECREASE
    )
    assert (
        f"Grade Standing decreased by {GRADE_STANDING_EXAM_FAIL_DECREASE}."
        in game.current_dialogue[0]
    )


def test_missed_assignment_decreases_grade_standing_once(game):
    game.current_day = 2

    game.sleep_until_next_day()

    assert game.grade_standing == (
        STARTING_GRADE_STANDING - GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE
    )
    assert (
        "Grade Standing decreased by "
        f"{GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE}."
        in game.current_dialogue[1]
    )

    game.sleep_until_next_day()

    assert game.grade_standing == (
        STARTING_GRADE_STANDING - GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE
    )


def test_room_changes_and_sleep_preserve_grade_standing(game):
    game.grade_standing = 66

    game.travel_to_room(ROOM_SCHOOL)
    assert game.grade_standing == 66

    game.sleep_until_next_day()
    assert game.grade_standing == 66


def test_grade_hud_is_not_persistent_in_default_view(game):
    game.draw()

    assert game.grade_hud_rect.size == (0, 0)
