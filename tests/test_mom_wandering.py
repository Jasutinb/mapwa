import os
import pytest
import pygame
import random

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from src.game import Game
from src.npc import NPC

@pytest.fixture
def game():
    pygame.init()
    # Mock screen to avoid display errors if any
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()

def test_mom_starts_at_initial_position(game):
    initial_pos = (800 // 2, 100)
    # Note: Game class might set it slightly differently or NPC might use topleft vs center
    # In src/game.py: self.mom = NPC((SCREEN_WIDTH // 2, 100), [self.visible_sprites], 'assets/images/mom.png', name="Mom")
    assert game.mom.rect.topleft == initial_pos

def test_mom_wanders(game):
    # Set a seed for reproducibility if random is used, 
    # but here we just want to see if it moves at all after some updates.
    random.seed(42)
    
    initial_pos = game.mom.rect.topleft
    
    # Update many times to allow for wandering
    # We need to be in 'main' room for mom to be updated if logic is added there
    game.current_room = 'main'
    
    # Mocking time/random might be better but let's see if we can just run it
    for _ in range(100):
        game.update()
    
    # If mom is wandering, her position should eventually change
    # Note: In current implementation she won't move yet.
    assert game.mom.rect.topleft != initial_pos
