import os
import pytest
import pygame

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from src.game import Game
from src.game import SCREEN_WIDTH, SCREEN_HEIGHT

@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()

def test_transition_to_bedroom(game):
    assert game.current_room == 'main'
    
    # Find the door to bedroom
    bedroom_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == 'bedroom')
    
    # Place player on the door
    game.player.rect.topleft = bedroom_door.rect.topleft
    game.update()
    
    assert game.current_room == 'bedroom'
    assert game.player.rect.topleft == bedroom_door.spawn_pos
    # Verify bedroom specific items
    decoration_names = [s.__class__.__name__ for s in game.visible_sprites]
    assert 'Decoration' in decoration_names

def test_transition_to_outside(game):
    assert game.current_room == 'main'
    
    # Find the door to outside
    outside_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == 'outside')
    
    # Place player on the door
    game.player.rect.topleft = outside_door.rect.topleft
    game.update()
    
    assert game.current_room == 'outside'
    assert game.player.rect.topleft == outside_door.spawn_pos

def test_transition_back_to_main_from_bedroom(game):
    # Setup bedroom
    game.current_room = 'bedroom'
    game.create_map()
    
    # Find the door to main
    main_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == 'main')
    
    # Place player on the door
    game.player.rect.topleft = main_door.rect.topleft
    game.update()
    
    assert game.current_room == 'main'
    assert game.player.rect.topleft == main_door.spawn_pos
    assert game.mom in game.visible_sprites

def test_transition_back_to_main_from_outside(game):
    # Setup outside
    game.current_room = 'outside'
    game.create_map()
    
    # Find the door to main
    main_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == 'main')
    
    # Place player on the door
    game.player.rect.topleft = main_door.rect.topleft
    game.update()
    
    assert game.current_room == 'main'
    assert game.player.rect.topleft == main_door.spawn_pos
    assert game.mom in game.visible_sprites

def test_no_transition_without_door(game):
    assert game.current_room == 'main'
    
    # Move player off the left edge where there is no door (top-left)
    game.player.rect.left = -10
    game.player.rect.top = 0
    game.update()
    
    # Should NOT transition because it's not colliding with a door
    assert game.current_room == 'main'
