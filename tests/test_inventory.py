import os
import pytest
import pygame

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from src.game import Game
from src.config import ITEM_ID
from src.inventory import Inventory
from src.level import Item

@pytest.fixture
def game():
    pygame.init()
    # Mock screen to avoid display errors
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()

def test_pick_up_item(game):
    # Transition to bedroom where the item is
    game.current_room = 'bedroom'
    game.create_map()
    
    # Ensure there is an item
    assert len(game.item_sprites) > 0
    item = list(game.item_sprites)[0]
    
    # Move player to item
    game.player.rect.center = item.rect.center
    
    # Simulate 'E' press
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    pygame.event.post(event_e)
    game.handle_events()
    
    # Check if item is in inventory and removed from world
    assert item in game.inventory.slots
    assert item not in game.item_sprites
    assert game.inventory.has_item(ITEM_ID)
    assert game.inventory.has_item("Student ID")
    assert game.current_dialogue is not None
    assert item.name in game.current_dialogue[0]

def test_inventory_full(game):
    game.current_room = 'bedroom'
    game.create_map()
    
    # Fill inventory
    for i in range(game.inventory.slot_count):
        game.inventory.add_item(Item((0, 0), [], f"Item {i}"))
    
    item = list(game.item_sprites)[0]
    game.player.rect.center = item.rect.center
    
    # Try to pick up
    event_e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_e})
    pygame.event.post(event_e)
    game.handle_events()
    
    # Item should still be in world
    assert item in game.item_sprites
    assert item not in game.inventory.slots


def test_unique_item_cannot_be_added_twice(game):
    first_id = Item((0, 0), [], "Student ID", item_id=ITEM_ID)
    duplicate_id = Item((0, 0), [], "Student ID", item_id=ITEM_ID)

    assert game.inventory.add_item(first_id)
    assert not game.inventory.add_item(duplicate_id)
    assert game.inventory.get_items() == [first_id]


def test_inventory_lookup_remove_and_debug_summary():
    pygame.display.set_mode((800, 600))
    inventory = Inventory()
    student_id = Item((0, 0), [], "Student ID", item_id=ITEM_ID)

    assert inventory.add_item(student_id)
    assert inventory.get_item(ITEM_ID) is student_id
    assert inventory.get_item("Student ID") is student_id
    assert inventory.has_item("student id")
    assert "Student ID" in inventory.debug_summary()

    removed = inventory.remove_item("Student ID")

    assert removed is student_id
    assert not inventory.has_item(ITEM_ID)


def test_inventory_use_item_returns_feedback(game):
    student_id = Item((0, 0), [], "Student ID", item_id=ITEM_ID)
    game.inventory.add_item(student_id)

    assert game.use_inventory_item("Student ID")
    assert game.current_dialogue == ["You check your Student ID. Keep it with you."]


def test_player_can_use_item_from_inventory_slot(game):
    student_id = Item((0, 0), [], "Student ID", item_id=ITEM_ID)
    game.inventory.add_item(student_id)

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
    game.handle_events([event])

    assert game.current_dialogue == ["You check your Student ID. Keep it with you."]


def test_consumable_item_is_removed_after_use():
    pygame.display.set_mode((800, 600))
    inventory = Inventory()
    food = Item((0, 0), [], "Food")

    assert inventory.add_item(food)

    message = inventory.use_item("Food")

    assert message == "You eat the food. Energy effects are not implemented yet."
    assert not inventory.has_item("Food")


def test_inventory_persists_between_maps(game):
    game.current_room = "bedroom"
    game.create_map()
    item = next(iter(game.item_sprites))

    assert game.pick_up_item(item)

    game.travel_to_room("main")
    game.travel_to_room("bedroom")

    assert game.inventory.has_item(ITEM_ID)
    assert len(game.item_sprites) == 0
