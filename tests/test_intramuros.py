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
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()

def test_intramuros_transition(game):
    # Setup: Start at Outside with enough money
    game.money = 20
    game.current_room = 'outside'
    game.create_map()
    
    # Move near bus
    game.player.rect.center = game.bus.rect.center
    
    # Press E
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    game.handle_events([event_e])
    
    assert game.current_room == 'intramuros'
    assert game.money == 0
    assert "Intramuros" in game.location_display_text

def test_intramuros_to_school_entrance(game):
    game.current_room = 'intramuros'
    game.create_map()

    entrance_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == 'school_entrance')
    game.player.rect.topleft = entrance_door.rect.topleft
    game.update()
    
    assert game.current_room == 'school_entrance'

def test_intramuros_to_outside(game):
    game.current_room = 'intramuros'
    game.create_map()
    
    # Ensure player is in visible sprites for collision/proximity check
    game.visible_sprites.add(game.player)
    
    # Move to the left side of the bus and ensure proximity
    game.player.rect.center = (game.bus.rect.left + 10, game.bus.rect.centery)
    
    # Press E
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    game.handle_events([event_e])
    
    assert game.current_room == 'outside'

def test_school_to_school_entrance(game):
    game.current_room = 'school'
    game.create_map()
    
    # Move near bus
    game.player.rect.center = game.bus.rect.center
    
    # Press E
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    game.handle_events([event_e])
    
    assert game.current_room == 'school_entrance'
