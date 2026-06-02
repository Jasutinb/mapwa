import os
import pytest
import pygame

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from src.game import Game
from src.game import DEV_LOADOUT_ENV
from src.config import ITEM_ID

ALLOWANCE_LINE = "Here's your allowance for today."

@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()

def press_interact(game):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e}))
    game.handle_events()

def complete_current_dialogue(game):
    while game.current_dialogue is not None:
        press_interact(game)

def test_game_initialization(game):
    assert game.current_day == 1
    assert game.last_allowance_day == 0
    assert game.money == 0
    assert not game.has_talked_to_mom
    assert game.player is not None
    assert game.mom is not None

def test_dev_loadout_starts_with_money_and_items(monkeypatch):
    monkeypatch.setenv(DEV_LOADOUT_ENV, "1")
    pygame.init()
    g = Game()
    try:
        assert g.money == 999
        assert ITEM_ID in g.state.inventory_item_ids
        assert ITEM_ID in g.state.picked_item_ids
        assert any(getattr(item, 'item_id', None) == ITEM_ID for item in g.inventory.slots)
    finally:
        pygame.quit()

def test_money_system(game):
    # Simulate first interaction with Mom
    game.player.rect.topleft = (400, 150) # Near Mom
    
    # Start interaction (Mom has 4 lines now)
    press_interact(game)
    assert game.current_dialogue is not None
    assert game.money == 0
    
    # Advance 2 more times (total 3 lines seen)
    for _ in range(2):
        press_interact(game)
    assert game.money == 0
        
    # Advance to the 4th line (money should be given now)
    press_interact(game)
    assert game.money == 250
    assert game.has_talked_to_mom is True
    assert game.last_allowance_day == 1
    assert game.current_dialogue is not None
    assert game.dialogue_index == 3
    
    # Final 'E' to finish dialogue
    press_interact(game)
    
    assert game.money == 250
    assert game.current_dialogue is None

def test_no_double_money_on_same_day(game):
    game.money = 250
    game.has_talked_to_mom = True
    game.last_allowance_day = game.current_day
    
    # Interaction again
    game.player.rect.topleft = (400, 150)
    press_interact(game)
    complete_current_dialogue(game)
        
    assert game.money == 250 # Should still be 250

def test_mom_gives_allowance_again_on_new_day(game):
    game.player.rect.topleft = (400, 150)

    press_interact(game)
    complete_current_dialogue(game)

    assert game.money == 250
    assert game.last_allowance_day == 1

    game.current_day = 2
    press_interact(game)

    assert game.current_dialogue is not None
    assert ALLOWANCE_LINE in game.current_dialogue

    while game.dialogue_index < len(game.current_dialogue) - 1:
        press_interact(game)

    assert game.money == 500
    assert game.last_allowance_day == 2

def test_mom_dialogue_changes_after_allowance(game):
    # First interaction
    game.player.rect.topleft = (400, 150)
    
    # Complete first interaction (5 'E' presses for 4 lines)
    press_interact(game)
    complete_current_dialogue(game)
    
    assert game.has_talked_to_mom is True
    
    # Start second interaction
    press_interact(game)
    
    # Check that the "allowance" line is NOT in the second dialogue
    assert ALLOWANCE_LINE not in game.current_dialogue
    assert "Make sure to study hard!" in game.current_dialogue
