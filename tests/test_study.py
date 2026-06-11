import os
import pytest
import pygame

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from src.game import Game
from src.config import SKILL_ACADEMICS

@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()

def test_study_at_school(game):
    # Transition to school
    game.current_room = 'school'
    game.create_map()
    
    initial_xp = game.experience
    
    # Move player near the school desk
    game.visible_sprites.add(game.player)
    game.player.rect.center = game.school_desk.rect.center
    
    # Simulate 'E' key press event
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    pygame.event.post(event)
    game.handle_events()
    
    assert game.experience == initial_xp + 10
    assert game.get_skill_xp(SKILL_ACADEMICS) == 10
    
    # Fast forward study
    for _ in range(61):
        game.update()
    
    assert game.current_dialogue is not None
    assert "studied hard" in game.current_dialogue[0]
