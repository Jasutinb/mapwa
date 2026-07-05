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

def test_location_name_display_on_init(game):
    # On initialization, it should show 'Living Room' (current_room is 'main')
    assert game.location_display_text == 'Living Room'
    assert game.location_display_timer == game.location_display_duration

def test_location_name_updates_on_transition(game):
    # Transition to bedroom
    game.current_room = 'bedroom'
    game.create_map()
    
    assert game.location_display_text == 'Bedroom'
    assert game.location_display_timer == game.location_display_duration

def test_location_timer_decrements(game):
    initial_timer = game.location_display_timer
    game.update()
    assert game.location_display_timer == initial_timer - 1

def test_location_names_mapping(game):
    # Test all mapped names
    rooms = {
        'main': 'Living Room',
        'bedroom': 'Bedroom',
        'outside': 'Outside',
        'intramuros': 'Intramuros',
        'school_entrance': 'School Entrance',
        'admin_office': 'Admin Office',
        'school': 'School',
        'programming_lab': 'Programming Lab',
        'electronics_lab': 'Electronics Lab',
        'library': 'Library',
        'cafeteria': 'Cafeteria'
    }
    
    for room, display_name in rooms.items():
        game.current_room = room
        game.create_map()
        assert game.location_display_text == display_name
