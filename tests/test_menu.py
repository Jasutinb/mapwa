import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from src.config import STATE_MENU, STATE_PLAY
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()


def test_escape_opens_and_closes_menu(game):

    assert game.state_machine.current_state_name == STATE_PLAY

    escape_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})

    game.handle_events([escape_event])

    assert game.state_machine.current_state_name == STATE_MENU
    assert game.previous_state_before_menu == STATE_PLAY

    game.handle_events([escape_event])

    assert game.state_machine.current_state_name == STATE_PLAY
