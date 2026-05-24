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

def test_transition_from_school_to_intramuros(game):
    # Setup school
    game.current_room = 'school'
    game.create_map()
    
    # Find the door to intramuros
    intramuros_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == 'intramuros')
    
    # Place player on the door
    game.player.rect.topleft = intramuros_door.rect.topleft
    game.update()
    
    assert game.current_room == 'intramuros'
    assert game.player.rect.topleft == intramuros_door.spawn_pos
    # Verify intramuros specific items (bus should be there)
    assert hasattr(game, 'bus')
