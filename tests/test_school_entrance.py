import os

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import pytest

from src.config import ITEM_ID, ROOM_INTRAMUROS, ROOM_SCHOOL, ROOM_SCHOOL_ENTRANCE
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()


def test_school_entrance_links_intramuros_and_school(game):
    assert game.rooms[ROOM_INTRAMUROS].right.name == ROOM_SCHOOL_ENTRANCE
    assert game.rooms[ROOM_SCHOOL_ENTRANCE].left.name == ROOM_INTRAMUROS
    assert game.rooms[ROOM_SCHOOL_ENTRANCE].right.name == ROOM_SCHOOL
    assert game.rooms[ROOM_SCHOOL].left.name == ROOM_SCHOOL_ENTRANCE


def test_bedroom_contains_id_instead_of_notebook(game):
    game.current_room = 'bedroom'
    game.create_map()

    item = next(iter(game.item_sprites))

    assert item.name == "ID"
    assert item.item_id == ITEM_ID


def test_school_gate_blocks_player_without_id(game):
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))
    game.player.rect.center = gate.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_room == ROOM_SCHOOL_ENTRANCE
    assert game.current_dialogue == ["I need my ID to enter the school."]


def test_school_gate_allows_player_with_id(game):
    game.state.inventory_item_ids.append(ITEM_ID)
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))
    game.player.rect.center = gate.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_room == ROOM_SCHOOL
