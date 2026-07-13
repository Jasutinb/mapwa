import os

import pytest

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame

from src.game import Game
from src.state import State, StateMachine


class TrackingState(State):
    def __init__(self, game):
        super().__init__(game)
        self.calls = []

    def handle_events(self, events):
        self.calls.append(("handle_events", events))

    def update(self):
        self.calls.append(("update", None))

    def draw(self, screen):
        self.calls.append(("draw", screen))

    def enter(self):
        self.calls.append(("enter", None))

    def exit(self):
        self.calls.append(("exit", None))


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


def test_state_machine_runs_lifecycle_and_delegates_to_current_state(game):
    state_machine = StateMachine()
    play = TrackingState(game)
    menu = TrackingState(game)
    events = [object()]
    screen = object()
    state_machine.add_state("play", play)
    state_machine.add_state("menu", menu)

    assert state_machine.change_state("play")
    state_machine.handle_events(events)
    state_machine.update()
    state_machine.draw(screen)
    assert not state_machine.change_state("play")
    assert state_machine.change_state("menu")

    assert play.calls == [
        ("enter", None),
        ("handle_events", events),
        ("update", None),
        ("draw", screen),
        ("exit", None),
    ]
    assert menu.calls == [("enter", None)]
    assert state_machine.current_state is menu
    assert state_machine.current_state_name == "menu"


def test_state_machine_safely_ignores_delegation_without_current_state():
    state_machine = StateMachine()

    state_machine.handle_events([object()])
    state_machine.update()
    state_machine.draw(object())

    assert state_machine.current_state is None
    assert state_machine.current_state_name is None


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
