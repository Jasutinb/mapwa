import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()


def test_intramuros_has_commute_landmarks(game):
    game.current_room = "intramuros"
    game.create_map()

    assert set(game.intramuros_landmarks) >= {
        "Mapua University Entrance",
        "Guard Booth",
        "Snack Vendor",
        "Transit Waiting Area",
        "Old Stone Wall",
        "Intramuros Gate",
    }
    assert hasattr(game, "intramuros_guard")
    assert hasattr(game, "intramuros_classmate")
    assert any(item.name == "Student Flyer" for item in game.item_sprites)
    assert any(
        getattr(door, "target_room", None) == "school" for door in game.door_sprites
    )
    assert not any(
        getattr(door, "target_room", None) == "outside" for door in game.door_sprites
    )


def test_intramuros_destinations_are_not_collision_blockers(game):
    game.current_room = "intramuros"
    game.create_map()

    open_destination_names = {
        "Guard Booth",
        "Snack Vendor",
        "Transit Waiting Area",
    }
    obstacle_names = {
        getattr(sprite, "name", None)
        for sprite in game.obstacle_sprites
        if getattr(sprite, "name", None)
    }

    assert open_destination_names.isdisjoint(obstacle_names)


def test_intramuros_classmate_dialogue(game):
    game.current_room = "intramuros"
    game.create_map()
    game.player.rect.center = game.intramuros_classmate.rect.center

    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})
    game.handle_events([event_e])

    assert game.current_dialogue == game.intramuros_classmate.dialogue
    assert game.current_dialogue_source == "intramuros"


def test_intramuros_school_gate_door(game):
    game.current_room = "intramuros"
    game.create_map()
    school_door = next(
        door
        for door in game.door_sprites
        if getattr(door, "target_room", None) == "school"
    )

    game.player.rect.topleft = school_door.rect.topleft
    game.update()

    assert game.current_room == "school"
    assert game.player.rect.topleft == school_door.spawn_pos


def test_intramuros_outside_transition_is_bus_only(game):
    game.current_room = "intramuros"
    game.create_map()

    outside_doors = [
        door
        for door in game.door_sprites
        if getattr(door, "target_room", None) == "outside"
    ]
    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})

    assert outside_doors == []

    game.visible_sprites.add(game.player)
    game.player.rect.center = (game.bus.rect.left + 10, game.bus.rect.centery)
    game.handle_events([event_e])

    assert game.current_room == "outside"


def test_intramuros_student_flyer_can_be_picked_up(game):
    game.current_room = "intramuros"
    game.create_map()
    flyer = next(item for item in game.item_sprites if item.name == "Student Flyer")
    game.player.rect.center = flyer.rect.center

    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})
    game.handle_events([event_e])

    assert flyer in game.inventory.slots
    assert flyer not in game.item_sprites
    assert "Student Flyer" in game.current_dialogue[0]
