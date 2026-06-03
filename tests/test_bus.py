import os
import pytest

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from src.game import Game
from src.transport import BUS_TRANSPORT

@pytest.fixture
def game():
    pygame.init()
    g = Game()
    # Mock money and room for testing
    g.money = 100
    return g

def test_bus_interaction_to_intramuros(game):
    game.current_room = 'outside'
    game.create_map()
    
    # Move player near bus
    game.player.rect.center = game.bus.rect.center
    
    # Ride to Intramuros
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])
    assert game.current_room == 'intramuros'
    assert game.money == 100 - BUS_TRANSPORT.fare

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
    assert game.money == 100 - BUS_TRANSPORT.fare

def test_bus_return_trip_no_money(game):
    game.current_room = 'school'
    game.create_map()
    game.money = BUS_TRANSPORT.fare - 1

    # Move player near bus
    game.player.rect.center = game.bus.rect.center

    # Simulate 'E' key press event
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_room == 'school'
    assert game.money == BUS_TRANSPORT.fare - 1
    assert game.current_dialogue is not None
    assert "enough money" in game.current_dialogue[0]
