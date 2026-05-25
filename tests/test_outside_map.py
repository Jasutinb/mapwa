import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import SCREEN_HEIGHT, TILE_SIZE
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()


def test_outside_has_neighborhood_landmarks(game):
    game.current_room = "outside"
    game.create_map()

    assert set(game.outside_landmarks) >= {
        "House Front",
        "Sari-sari Store",
        "Bus Stop",
        "Bus Shelter",
    }
    assert game.bus.rect.top == SCREEN_HEIGHT - TILE_SIZE * 5
    assert any(item.name == "Coin" for item in game.item_sprites)
    assert any(
        getattr(door, "target_room", None) == "main" for door in game.door_sprites
    )


def test_outside_destinations_are_not_collision_blockers(game):
    game.current_room = "outside"
    game.create_map()

    open_destination_names = {"Sari-sari Store", "Bus Stop", "Bus Shelter"}
    obstacle_names = {
        getattr(sprite, "name", None)
        for sprite in game.obstacle_sprites
        if getattr(sprite, "name", None)
    }

    assert open_destination_names.isdisjoint(obstacle_names)


def test_outside_neighbor_dialogue_does_not_grant_mom_allowance(game):
    game.current_room = "outside"
    game.create_map()
    game.money = 0
    game.has_talked_to_mom = False
    game.player.rect.center = game.outside_neighbor.rect.center

    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})
    game.handle_events([event_e])

    assert game.current_dialogue == game.outside_neighbor.dialogue
    assert game.current_dialogue_source == "outside"

    for _ in game.outside_neighbor.dialogue:
        game.handle_events([event_e])

    assert game.money == 0
    assert game.has_talked_to_mom is False
    assert game.current_dialogue is None


def test_outside_coin_can_be_picked_up(game):
    game.current_room = "outside"
    game.create_map()
    coin = next(item for item in game.item_sprites if item.name == "Coin")
    game.player.rect.center = coin.rect.center

    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})
    game.handle_events([event_e])

    assert coin in game.inventory.slots
    assert coin not in game.item_sprites
    assert "Coin" in game.current_dialogue[0]
