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
    player = Player((0, 0), [])
    player.direction.x = 1
    player.move(player.speed)
    assert player.rect.x == player.speed
    assert player.rect.y == 0

    player.direction.x = 0
    player.direction.y = 1
    player.move(player.speed)
    assert player.rect.y == player.speed
