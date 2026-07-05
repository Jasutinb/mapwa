import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    ELECTRONICS_LAB_XP,
    ROOM_ELECTRONICS_LAB,
    ROOM_SCHOOL,
    TILE_SIZE,
    SKILL_ELECTRONICS,
)
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def test_electronics_lab_room_links_from_school(game):
    assert game.rooms[ROOM_SCHOOL].right.name == ROOM_ELECTRONICS_LAB
    assert game.rooms[ROOM_ELECTRONICS_LAB].left.name == ROOM_SCHOOL


def test_school_has_clear_door_to_electronics_lab(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()

    lab_door = next(s for s in game.door_sprites if s.target_room == ROOM_ELECTRONICS_LAB)
    game.player.rect.topleft = lab_door.rect.topleft

    game.update()

    assert game.current_room == ROOM_ELECTRONICS_LAB
    assert game.player.rect.topleft == lab_door.spawn_pos
    assert hasattr(game, "electronics_station")
    assert not pygame.sprite.spritecollide(game.player, game.obstacle_sprites, False)


def test_electronics_lab_exit_returns_to_clear_school_path(game):
    game.current_room = ROOM_ELECTRONICS_LAB
    game.create_map()

    school_door = next(s for s in game.door_sprites if s.target_room == ROOM_SCHOOL)
    game.player.rect.topleft = school_door.rect.topleft

    game.update()

    assert game.current_room == ROOM_SCHOOL
    assert game.player.rect.topleft == school_door.spawn_pos
    assert hasattr(game, "school_desk")
    assert not pygame.sprite.spritecollide(game.player, game.obstacle_sprites, False)


def test_electronics_lab_exit_trigger_is_reachable_from_inside_room(game):
    game.current_room = ROOM_ELECTRONICS_LAB
    game.create_map()

    school_door = next(s for s in game.door_sprites if s.target_room == ROOM_SCHOOL)

    assert school_door.rect.left >= TILE_SIZE


def test_electronics_station_interaction_grants_electronics_xp(game):
    game.current_room = ROOM_ELECTRONICS_LAB
    game.create_map()
    game.player.rect.center = game.electronics_station.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.get_skill_xp(SKILL_ELECTRONICS) == ELECTRONICS_LAB_XP
    assert game.current_dialogue == [
        f"You practiced circuits and gained {ELECTRONICS_LAB_XP} electronics XP! Total: {ELECTRONICS_LAB_XP}."
    ]


def test_mobile_action_button_triggers_electronics_practice(game):
    game.current_room = ROOM_ELECTRONICS_LAB
    game.create_map()
    game.player.rect.center = game.electronics_station.rect.center
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.get_skill_xp(SKILL_ELECTRONICS) == ELECTRONICS_LAB_XP
