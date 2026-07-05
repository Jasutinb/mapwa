import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import PROGRAMMING_LAB_XP, ROOM_PROGRAMMING_LAB, ROOM_SCHOOL, SKILL_PROGRAMMING
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def test_programming_lab_room_links_from_school(game):
    assert game.rooms[ROOM_SCHOOL].up.name == ROOM_PROGRAMMING_LAB
    assert game.rooms[ROOM_PROGRAMMING_LAB].down.name == ROOM_SCHOOL


def test_school_has_door_to_programming_lab(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()

    lab_door = next(s for s in game.door_sprites if s.target_room == ROOM_PROGRAMMING_LAB)
    game.player.rect.topleft = lab_door.rect.topleft

    game.update()

    assert game.current_room == ROOM_PROGRAMMING_LAB
    assert game.player.rect.topleft == lab_door.spawn_pos
    assert hasattr(game, "programming_station")


def test_programming_lab_exit_returns_to_school(game):
    game.current_room = ROOM_PROGRAMMING_LAB
    game.create_map()

    school_door = next(s for s in game.door_sprites if s.target_room == ROOM_SCHOOL)
    game.player.rect.topleft = school_door.rect.topleft

    game.update()

    assert game.current_room == ROOM_SCHOOL
    assert game.player.rect.topleft == school_door.spawn_pos
    assert hasattr(game, "school_desk")
    assert not pygame.sprite.spritecollide(game.player, game.obstacle_sprites, False)


def test_programming_station_interaction_grants_programming_xp(game):
    game.current_room = ROOM_PROGRAMMING_LAB
    game.create_map()
    game.player.rect.center = game.programming_station.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.get_skill_xp(SKILL_PROGRAMMING) == PROGRAMMING_LAB_XP
    assert game.current_dialogue == [
        f"You practiced coding and gained {PROGRAMMING_LAB_XP} programming XP! Total: {PROGRAMMING_LAB_XP}."
    ]


def test_mobile_action_button_triggers_programming_practice(game):
    game.current_room = ROOM_PROGRAMMING_LAB
    game.create_map()
    game.player.rect.center = game.programming_station.rect.center
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.get_skill_xp(SKILL_PROGRAMMING) == PROGRAMMING_LAB_XP
