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
    # Mock screen to avoid display errors
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()

def test_study_animation_trigger(game):
    # Transition to school where the desk is
    game.current_room = 'school'
    game.create_map()
    
    # Ensure desk exists
    assert hasattr(game, 'school_desk')
    
    # Move player to desk
    game.player.rect.center = game.school_desk.rect.center
    
    # Simulate 'E' press
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    pygame.event.post(event_e)
    game.handle_events()
    
    # Check if study animation started
    assert game.player.studying is True
    assert game.player.study_timer == 60
    assert game.experience == 10

def test_study_animation_duration(game):
    game.player.start_study(2) # Start a very short study for testing
    
    assert game.player.studying is True
    
    game.player.update()
    assert game.player.study_timer == 1
    assert game.player.studying is True
    
    game.player.update()
    assert game.player.study_timer == 0
    assert game.player.studying is False

def test_no_movement_while_studying(game, monkeypatch):
    game.player.start_study(60)
    
    # Mock key press
    def mock_get_pressed():
        keys = {}
        keys[pygame.K_RIGHT] = True
        class MockKeys:
            def __getitem__(self, key):
                return keys.get(key, False)
        return MockKeys()
    
    monkeypatch.setattr(pygame.key, "get_pressed", mock_get_pressed)
    
    old_pos = game.player.rect.copy()
    game.player.update()
    
    # Position might change slightly due to vibration, but direction should be 0
    assert game.player.direction.x == 0
    assert game.player.direction.y == 0
