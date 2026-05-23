import os
import pytest
import pygame

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from src.game import Game

@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()

def test_transition_from_school_to_outside(game):
    # Setup school
    game.current_room = 'school'
    game.create_map()
    
    # Find the door to outside
    outside_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == 'outside')
    
    # Place player on the door
    game.player.rect.topleft = outside_door.rect.topleft
    game.update()
    
    assert game.current_room == 'outside'
    assert game.player.rect.topleft == outside_door.spawn_pos
    # Verify outside specific items (bus should be there)
    assert hasattr(game, 'bus')
