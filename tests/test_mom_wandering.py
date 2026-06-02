import os
import pytest
import pygame
import random

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from src.game import Game

@pytest.fixture
def game():
    pygame.init()
    # Mock screen to avoid display errors if any
    pygame.display.set_mode((800, 600))
    random.seed(42)
    g = Game()
    yield g
    pygame.quit()

def test_mom_starts_at_initial_position(game):
    initial_pos = (800 // 2, 100)
    # Note: Game class might set it slightly differently or NPC might use topleft vs center
    # In src/game.py: self.mom = NPC((SCREEN_WIDTH // 2, 100), [self.visible_sprites], 'assets/images/mom.png', name="Mom")
    assert game.mom.rect.topleft == initial_pos

def test_mom_wanders(game):
    initial_pos = game.mom.rect.topleft
    game.current_room = 'main'

    for _ in range(10):
        game.update()

    assert game.mom.rect.topleft != initial_pos
