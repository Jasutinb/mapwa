import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    LIBRARY_STUDY_XP,
    ROOM_LIBRARY,
    ROOM_SCHOOL,
    SKILL_ACADEMICS,
    SKILL_DISCIPLINE,
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


def test_library_room_links_from_school(game):
    assert game.rooms[ROOM_SCHOOL].down.name == ROOM_LIBRARY
    assert game.rooms[ROOM_LIBRARY].up.name == ROOM_SCHOOL


def test_school_has_clear_door_to_library(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()

    library_door = next(s for s in game.door_sprites if s.target_room == ROOM_LIBRARY)
    game.player.rect.topleft = library_door.rect.topleft

    game.update()

    assert game.current_room == ROOM_LIBRARY
    assert game.player.rect.topleft == library_door.spawn_pos
    assert hasattr(game, "library_academics_station")
    assert hasattr(game, "library_math_station")
    assert hasattr(game, "library_discipline_station")
    assert not pygame.sprite.spritecollide(game.player, game.obstacle_sprites, False)


def test_library_exit_returns_to_clear_school_path(game):
    game.current_room = ROOM_LIBRARY
    game.create_map()

    school_door = next(s for s in game.door_sprites if s.target_room == ROOM_SCHOOL)
    game.player.rect.topleft = school_door.rect.topleft

    game.update()

    assert game.current_room == ROOM_SCHOOL
    assert game.player.rect.topleft == school_door.spawn_pos
    assert hasattr(game, "school_desk")
    assert not pygame.sprite.spritecollide(game.player, game.obstacle_sprites, False)


@pytest.mark.parametrize(
    ("station_name", "skill", "label"),
    [
        ("library_academics_station", SKILL_ACADEMICS, "academics"),
        ("library_math_station", SKILL_MATH, "math"),
        ("library_discipline_station", SKILL_DISCIPLINE, "discipline"),
    ],
)
def test_library_station_interactions_grant_matching_skill_xp(game, station_name, skill, label):
    game.current_room = ROOM_LIBRARY
    game.create_map()
    station = getattr(game, station_name)
    game.player.rect.center = station.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.get_skill_xp(skill) == LIBRARY_STUDY_XP
    assert game.current_dialogue == [
        f"You studied {label} and gained {LIBRARY_STUDY_XP} {label} XP! Total: {LIBRARY_STUDY_XP}."
    ]


@pytest.mark.parametrize(
    ("station_name", "skill"),
    [
        ("library_academics_station", SKILL_ACADEMICS),
        ("library_math_station", SKILL_MATH),
        ("library_discipline_station", SKILL_DISCIPLINE),
    ],
)
def test_mobile_action_button_triggers_library_station_interactions(game, station_name, skill):
    game.current_room = ROOM_LIBRARY
    game.create_map()
    station = getattr(game, station_name)
    game.player.rect.center = station.rect.center
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.get_skill_xp(skill) == LIBRARY_STUDY_XP
