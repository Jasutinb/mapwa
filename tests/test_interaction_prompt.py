import os
from unittest.mock import Mock

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

from src.config import STATE_PLAY
from src.game import Game


class FakeFont:
    def __init__(self):
        self.rendered_text = []

    def render(self, text, antialias, color):
        self.rendered_text.append(text)
        return FakeSurface()


class FakeSurface:
    def get_rect(self, **kwargs):
        rect = pygame.Rect(0, 0, 120, 20)
        for attr, value in kwargs.items():
            setattr(rect, attr, value)
        return rect


def test_interaction_prompt_appears_near_interactable():
    pygame.init()
    game = Game()
    game.font = FakeFont()
    game.player.rect.center = game.mom.rect.center
    screen = Mock()

    game.state_machine.states[STATE_PLAY].draw(screen)

    assert "Press E to talk" in game.font.rendered_text
    assert screen.blit.called
    pygame.quit()


def test_interaction_prompt_is_hidden_when_player_is_far():
    pygame.init()
    game = Game()
    game.font = FakeFont()
    game.player.rect.center = (700, 500)
    screen = Mock()

    game.state_machine.states[STATE_PLAY].draw(screen)

    assert game.font.rendered_text == []
    screen.blit.assert_not_called()
    pygame.quit()
