import os

import pytest

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame

from src.game import Game
from src.state import State, StateMachine


@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()


def test_state_machine_rejects_duplicate_and_unknown_states(game):
    state_machine = StateMachine()
    state_machine.add_state("play", State(game))

    with pytest.raises(ValueError):
        state_machine.add_state("play", State(game))

    with pytest.raises(KeyError):
        state_machine.change_state("missing")


def test_picked_item_does_not_respawn_after_room_rebuild(game):
    game.current_room = "bedroom"
    game.create_map()
    item = next(iter(game.item_sprites))
    game.player.rect.center = item.rect.center

    assert game.pick_up_item(item)

    game.state_machine.change_state("play")
    game.current_room = "bedroom"
    game.create_map()

    assert len(game.item_sprites) == 0
