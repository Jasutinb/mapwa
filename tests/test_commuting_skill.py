import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from src.config import (
    BUS_COMMUTING_XP,
    ROOM_INTRAMUROS,
    ROOM_OUTSIDE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKILL_COMMUTING,
    TRACKED_SKILLS,
)
from src.game import Game
from src.transport import BUS_TRANSPORT


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    g = Game()
    yield g
    pygame.quit()


def place_player_at_bus(game, room=ROOM_OUTSIDE):
    game.current_room = room
    game.create_map()
    game.player.rect.center = game.bus.rect.center


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=key)])


def press_mobile_action(game):
    action_pos = game.mobile_controls.rects["action"].center
    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )


def test_commuting_is_initialized_as_tracked_skill(game):
    assert SKILL_COMMUTING in TRACKED_SKILLS
    assert SKILL_COMMUTING in game.skill_xp_manager.xp_by_skill
    assert game.get_skill_xp(SKILL_COMMUTING) == 0


def test_successful_bus_ride_grants_commuting_xp(game):
    game.money = BUS_TRANSPORT.fare
    place_player_at_bus(game)

    press_key(game, pygame.K_e)

    assert game.current_room == ROOM_INTRAMUROS
    assert game.money == 0
    assert game.get_skill_xp(SKILL_COMMUTING) == BUS_COMMUTING_XP


def test_failed_bus_ride_grants_no_commuting_xp(game):
    game.money = BUS_TRANSPORT.fare - 1
    place_player_at_bus(game)

    press_key(game, pygame.K_e)

    assert game.current_room == ROOM_OUTSIDE
    assert game.money == BUS_TRANSPORT.fare - 1
    assert game.get_skill_xp(SKILL_COMMUTING) == 0


def test_mobile_action_bus_ride_grants_commuting_xp(game):
    game.money = BUS_TRANSPORT.fare
    place_player_at_bus(game)

    press_mobile_action(game)

    assert game.current_room == ROOM_INTRAMUROS
    assert game.money == 0
    assert game.get_skill_xp(SKILL_COMMUTING) == BUS_COMMUTING_XP
