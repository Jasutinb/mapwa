import pygame
import pytest

from src.config import (
    ALLOWANCE_AMOUNT,
    GRADE_STANDING_ACADEMIC_RECOGNITION_BONUS,
    STATE_PLANNER,
)
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    instance = Game()
    yield instance
    pygame.quit()


@pytest.mark.parametrize(
    ("score", "label"),
    [
        (100, "Excellent Standing"),
        (90, "Excellent Standing"),
        (89, "Good Standing"),
        (80, "Good Standing"),
        (79, "Stable"),
        (70, "Stable"),
        (69, "At Risk"),
        (60, "At Risk"),
        (59, "Probation"),
        (0, "Probation"),
    ],
)
def test_grade_standing_labels_cover_all_threshold_boundaries(game, score, label):
    assert game.get_grade_standing_label(score) == label


def test_planner_grade_section_uses_live_grade_label(game):
    planner = game.state_machine.states[STATE_PLANNER]

    assert planner.get_sections()["Grade Standing"] == ["75/100 — Stable"]

    game.grade_standing = 90

    assert planner.get_sections()["Grade Standing"] == [
        "90/100 — Excellent Standing"
    ]
    grade_line = planner.get_sections()["Grade Standing"][0]
    grade_rect = planner.section_rects["Grade Standing"]

    assert planner.body_font.render(grade_line, True, "white").get_width() <= (
        grade_rect.width - 28
    )


def test_excellent_standing_adds_one_recognition_bonus_to_daily_allowance(game):
    game.grade_standing = 90

    dialogue = game.get_mom_dialogue()

    assert "Excellent Standing" in dialogue[-2]
    assert f"₱{GRADE_STANDING_ACADEMIC_RECOGNITION_BONUS}" in dialogue[-2]
    assert game.give_daily_allowance() is True
    assert game.money == (
        ALLOWANCE_AMOUNT + GRADE_STANDING_ACADEMIC_RECOGNITION_BONUS
    )
    assert game.give_daily_allowance() is False
    assert game.money == (
        ALLOWANCE_AMOUNT + GRADE_STANDING_ACADEMIC_RECOGNITION_BONUS
    )


def test_nonexcellent_standing_keeps_the_standard_daily_allowance(game):
    game.grade_standing = 89

    assert game.get_academic_recognition_bonus() == 0
    assert game.give_daily_allowance() is True
    assert game.money == ALLOWANCE_AMOUNT


def test_daily_allowance_dialogue_gives_band_specific_feedback(game):
    game.current_day = 2
    game.has_talked_to_mom = True
    game.grade_standing = 60

    assert "At Risk standing needs attention" in game.get_mom_dialogue()[-2]
