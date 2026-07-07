import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL,
    SKILL_ACADEMICS,
    SKILL_PROGRAMMING,
)
from src.game import Game
from src.schedule import (
    WEEKDAYS,
    WEEKLY_CLASS_SCHEDULE,
    classes_for_day,
    classes_for_weekday,
    schedule_summary_for_day,
    weekday_for_day,
)


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def test_weekly_schedule_entries_have_required_fields():
    assert WEEKLY_CLASS_SCHEDULE

    for entry in WEEKLY_CLASS_SCHEDULE:
        assert entry.course_name
        assert entry.weekday in WEEKDAYS
        assert entry.start_label
        assert entry.end_label
        assert entry.room_label
        assert entry.room_key
        assert entry.skill
        assert entry.time_label == f"{entry.start_label}-{entry.end_label}"


def test_weekday_for_day_starts_on_monday_and_cycles():
    assert weekday_for_day(1) == "Monday"
    assert weekday_for_day(2) == "Tuesday"
    assert weekday_for_day(7) == "Sunday"
    assert weekday_for_day(8) == "Monday"


def test_classes_for_school_day_are_returned_in_display_order():
    monday_classes = classes_for_day(1)

    assert [entry.course_name for entry in monday_classes] == [
        "Academics",
        "Programming",
    ]
    assert monday_classes[0].start_label == "08:00"
    assert monday_classes[0].room_key == ROOM_SCHOOL
    assert monday_classes[0].skill == SKILL_ACADEMICS
    assert monday_classes[1].room_key == ROOM_PROGRAMMING_LAB
    assert monday_classes[1].skill == SKILL_PROGRAMMING


def test_free_days_return_no_classes_and_clear_summary():
    assert classes_for_weekday("Saturday") == []
    assert classes_for_day(6) == []
    assert schedule_summary_for_day(6) == "Saturday: No classes today."


def test_game_schedule_helpers_follow_current_day(game):
    assert game.current_weekday == "Monday"
    assert game.get_today_classes() == classes_for_day(1)
    assert game.get_schedule_summary().startswith("Monday: Next 08:00 Academics")

    game.current_day = 6

    assert game.current_weekday == "Saturday"
    assert game.get_today_classes() == []
    assert game.get_schedule_summary() == "Saturday: No classes today."


def test_sleep_advances_schedule_day(game):
    game.sleep_until_next_day()

    assert game.current_day == 2
    assert game.current_weekday == "Tuesday"
    assert game.get_schedule_summary().startswith("Tuesday: Next 08:00 Math")


def test_schedule_hud_is_not_persistent_in_default_view(game):
    game.draw()

    assert game.schedule_hud_rect.size == (0, 0)
