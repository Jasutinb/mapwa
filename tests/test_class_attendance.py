import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    CLASS_ALREADY_ATTENDED_DIALOGUE,
    CLASS_ATTENDANCE_XP,
    CLASS_NO_CLASS_HERE_DIALOGUE,
    CLASS_NO_CLASSES_TODAY_DIALOGUE,
    GRADE_STANDING_CLASS_ATTENDANCE_INCREASE,
    MAX_ENERGY,
    ROOM_LIBRARY,
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL,
    SCHOOL_STUDY_ENERGY_COST,
    SKILL_ACADEMICS,
    SKILL_MATH,
    SKILL_PROGRAMMING,
    STUDY_XP,
    STARTING_GRADE_STANDING,
)
from src.game import Game
from src.schedule import classes_for_day


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, {"key": key})])


def move_to_room_class_marker(game, room, day=1):
    game.current_day = day
    game.current_room = room
    game.create_map()
    marker = next(iter(game.class_marker_sprites))
    game.player.rect.center = marker.rect.center
    return marker


def test_attend_scheduled_class_in_matching_room_with_keyboard(game):
    move_to_room_class_marker(game, ROOM_SCHOOL, day=1)
    class_entry = classes_for_day(1)[0]

    press_key(game, pygame.K_e)

    assert game.get_skill_xp(SKILL_ACADEMICS) == CLASS_ATTENDANCE_XP
    assert class_entry.identifier in game.get_attended_class_ids()
    assert game.grade_standing == (
        STARTING_GRADE_STANDING + GRADE_STANDING_CLASS_ATTENDANCE_INCREASE
    )
    assert game.current_dialogue == [
        (
            "You attended Academics and gained "
            f"{CLASS_ATTENDANCE_XP} academics XP! Total: {CLASS_ATTENDANCE_XP}. "
            "Grade Standing increased by 1."
        )
    ]


def test_attend_scheduled_class_with_mobile_action(game):
    move_to_room_class_marker(game, ROOM_PROGRAMMING_LAB, day=1)
    action_pos = game.mobile_controls.rects["action"].center
    programming_class = classes_for_day(1)[1]

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.get_skill_xp(SKILL_PROGRAMMING) == CLASS_ATTENDANCE_XP
    assert programming_class.identifier in game.get_attended_class_ids()
    assert game.grade_standing == (
        STARTING_GRADE_STANDING + GRADE_STANDING_CLASS_ATTENDANCE_INCREASE
    )


def test_duplicate_class_attendance_is_blocked(game):
    move_to_room_class_marker(game, ROOM_SCHOOL, day=1)

    assert game.attend_class() is True
    assert game.attend_class() is False

    assert game.get_skill_xp(SKILL_ACADEMICS) == CLASS_ATTENDANCE_XP
    assert game.grade_standing == (
        STARTING_GRADE_STANDING + GRADE_STANDING_CLASS_ATTENDANCE_INCREASE
    )
    assert game.current_dialogue == [
        CLASS_ALREADY_ATTENDED_DIALOGUE.format(course_name="Academics")
    ]
    assert len(game.get_attended_class_ids()) == 1


def test_wrong_room_attendance_is_blocked(game):
    move_to_room_class_marker(game, ROOM_LIBRARY, day=1)

    press_key(game, pygame.K_e)

    assert game.get_skill_xp(SKILL_MATH) == 0
    assert game.get_attended_class_ids() == set()
    assert game.current_dialogue == [CLASS_NO_CLASS_HERE_DIALOGUE]


def test_free_day_attendance_is_blocked(game):
    move_to_room_class_marker(game, ROOM_SCHOOL, day=6)

    press_key(game, pygame.K_e)

    assert game.get_skill_xp(SKILL_ACADEMICS) == 0
    assert game.get_attended_class_ids() == set()
    assert game.current_dialogue == [CLASS_NO_CLASSES_TODAY_DIALOGUE]


def test_sleep_resets_attended_classes_for_next_day(game):
    move_to_room_class_marker(game, ROOM_SCHOOL, day=1)
    assert game.attend_class() is True
    assert game.get_attended_class_ids()

    game.sleep_until_next_day()
    move_to_room_class_marker(game, ROOM_LIBRARY, day=2)

    assert game.get_attended_class_ids() == set()
    assert game.attend_class() is True
    assert game.get_skill_xp(SKILL_MATH) == CLASS_ATTENDANCE_XP


def test_existing_school_study_station_still_studies(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.player.rect.center = game.school_desk.rect.center

    press_key(game, pygame.K_e)

    assert game.get_skill_xp(SKILL_ACADEMICS) == STUDY_XP
    assert game.energy == MAX_ENERGY - SCHOOL_STUDY_ENERGY_COST
    assert game.player.studying is True
    assert game.get_attended_class_ids() == set()
