import os
import pytest
import pygame

# Set dummy drivers BEFORE importing pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.game import Game
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
    game.current_room = "bedroom"
    game.create_map()

    # Ensure there is an item
    assert len(game.item_sprites) > 0
    item = list(game.item_sprites)[0]

    # Move player to item
    game.player.rect.center = item.rect.center

    # Simulate 'E' press
    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})
    pygame.event.post(event_e)
    game.handle_events()

    # Check if item is in inventory and removed from world
    assert item in game.inventory.slots
    assert item not in game.item_sprites
    assert game.current_dialogue is not None
    assert item.name in game.current_dialogue[0]


def test_picked_up_room_item_does_not_respawn(game):
    game.current_room = "bedroom"
    game.create_map()

    item = list(game.item_sprites)[0]
    game.player.rect.center = item.rect.center

    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})
    game.handle_events([event_e])

    game.current_room = "main"
    game.create_map()
    game.current_room = "bedroom"
    game.create_map()

    assert len(game.item_sprites) == 0


def test_inventory_full(game):
    game.current_room = "bedroom"
    game.create_map()

    # Fill inventory
    for i in range(game.inventory.slot_count):
        game.inventory.add_item(Item((0, 0), [], f"Item {i}"))

    item = list(game.item_sprites)[0]
    game.player.rect.center = item.rect.center

    # Try to pick up
    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})
    pygame.event.post(event_e)
    game.handle_events()

    # Item should still be in world
    assert item in game.item_sprites
    assert item not in game.inventory.slots
