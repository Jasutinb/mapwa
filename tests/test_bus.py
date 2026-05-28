import os
import pytest

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from src.game import Game

@pytest.fixture
def game():
    pygame.init()
    g = Game()
    # Mock money and room for testing
    g.money = 100
    return g

def test_bus_interaction_to_school_entrance(game):
    game.current_room = 'outside'
    game.create_map()
    
    # Move player near bus
    game.player.rect.center = game.bus.rect.center
    
    # Ride to Intramuros
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])
    assert game.current_room == 'intramuros'
    assert game.money == 80

    # Ensure player is visible for next check
    game.visible_sprites.add(game.player)
    # Move to right side of Intramuros bus to go to the school entrance
    game.player.rect.center = (game.bus.rect.right - 10, game.bus.rect.centery)
    game.handle_events([event])
    
    assert game.current_room == 'school_entrance'
    assert game.money == 80

def test_bus_interaction_no_money(game):
    game.current_room = 'outside'
    game.create_map()
    game.money = 10 # Not enough
    
    # Move player near bus
    game.player.rect.center = game.bus.rect.center
    
    # Simulate 'E' key press event
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    pygame.event.post(event)
    game.handle_events()
    
    assert game.current_room == 'outside'
    assert game.money == 10
    assert game.current_dialogue is not None
    assert "enough money" in game.current_dialogue[0]

def test_bus_interaction_from_school_to_entrance(game):
    game.current_room = 'school'
    game.create_map()
    
    # Move player near bus
    game.player.rect.center = game.bus.rect.center
    
    # Ride back to the school entrance
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])
    assert game.current_room == 'school_entrance'
    assert game.money == 100 # No cost to go home
