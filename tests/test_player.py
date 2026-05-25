import os
import pytest

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from src.player import Player

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_player_initialization():
    player = Player((100, 100), [])
    assert player.rect.topleft == (100, 100)
    assert player.speed == 4
    assert player.direction.magnitude() == 0

def test_player_movement():
    player = Player((0, 0), [], pygame.sprite.Group())
    player.direction.x = 1
    player.move(player.speed)
    assert player.rect.x == player.speed

def test_player_wall_collision():
    obstacles = pygame.sprite.Group()
    wall = pygame.sprite.Sprite(obstacles)
    wall.rect = pygame.Rect(64, 0, 64, 64)
    
    player = Player((0, 0), [], obstacles)
    player.rect.topleft = (32, 0)
    
    # Try to move into the wall
    player.direction.x = 1
    player.move(4)
    
    # Should be blocked by the wall's left edge
    assert player.rect.right <= wall.rect.left

def test_player_screen_boundaries():
    player = Player((0, 0), [], pygame.sprite.Group())
    
    # Try to move past left edge
    player.rect.left = 0
    player.direction.x = -1
    player.move(4)
    assert player.rect.left == 0
    
    # Try to move past top edge
    player.rect.top = 0
    player.direction.y = -1
    player.move(4)
    assert player.rect.top == 0
    assert player.rect.y == 0

    player.direction.x = 0
    player.direction.y = 1
    player.move(player.speed)
    assert player.rect.y == player.speed

def test_player_wasd_input(monkeypatch):
    player = Player((0, 0), [])
    
    # Mock pygame.key.get_pressed to simulate 'W' and 'D' keys being pressed
    def mock_get_pressed():
        keys = {} # Use a dictionary to avoid IndexError
        keys[pygame.K_w] = True
        keys[pygame.K_d] = True
        # Return a object that mimics ScancodeWrapper behaviors
        class MockKeys:
            def __getitem__(self, key):
                return keys.get(key, False)
        return MockKeys()

    monkeypatch.setattr(pygame.key, "get_pressed", mock_get_pressed)
    
    player.input()
    assert player.direction.y == -1
    assert player.direction.x == 1
