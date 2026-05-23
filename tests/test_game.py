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

def test_game_initialization(game):
    assert game.money == 0
    assert not game.has_talked_to_mom
    assert game.player is not None
    assert game.mom is not None

def test_money_system(game):
    # Simulate first interaction with Mom
    game.player.rect.topleft = (400, 150) # Near Mom
    
    # Start interaction (Mom has 4 lines now)
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    pygame.event.post(event_e)
    game.handle_events()
    assert game.current_dialogue is not None
    assert game.money == 0
    
    # Advance 2 more times (total 3 lines seen)
    for _ in range(2):
        pygame.event.post(event_e)
        game.handle_events()
    assert game.money == 0
        
    # Advance to the 4th line (money should be given now)
    pygame.event.post(event_e)
    game.handle_events()
    assert game.money == 250
    assert game.has_talked_to_mom is True
    assert game.current_dialogue is not None
    assert game.dialogue_index == 3
    
    # Final 'E' to finish dialogue
    pygame.event.post(event_e)
    game.handle_events()
    
    assert game.money == 250
    assert game.current_dialogue is None

def test_no_double_money(game):
    game.money = 250
    game.has_talked_to_mom = True
    
    # Interaction again
    game.player.rect.topleft = (400, 150)
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    
    # Complete dialogue (4 lines + 1 to end)
    for _ in range(5):
        pygame.event.post(event_e)
        game.handle_events()
        
    assert game.money == 250 # Should still be 250

def test_mom_dialogue_changes_after_allowance(game):
    # First interaction
    game.player.rect.topleft = (400, 150)
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    
    # Complete first interaction (5 'E' presses for 4 lines)
    for _ in range(5):
        pygame.event.post(event_e)
        game.handle_events()
    
    assert game.has_talked_to_mom is True
    
    # Start second interaction
    pygame.event.post(event_e)
    game.handle_events()
    
    # Check that the "allowance" line is NOT in the second dialogue
    allowance_line = "Here's your allowance for today."
    assert allowance_line not in game.current_dialogue
    assert "Make sure to study hard!" in game.current_dialogue
