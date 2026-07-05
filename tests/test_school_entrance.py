import os

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import pytest
from pathlib import Path

from src.config import (
    ADMIN_OFFICE_CHECKED_IN_DIALOGUE,
    ADMIN_OFFICE_CHECK_IN_DIALOGUE,
    ADMIN_OFFICE_CHECK_IN_XP,
    ADMIN_OFFICE_NO_ID_DIALOGUE,
    ADMIN_OFFICE_TEMP_PASS_ACTIVE_DIALOGUE,
    ITEM_ID,
    ROOM_ADMIN_OFFICE,
    ROOM_INTRAMUROS,
    ROOM_SCHOOL,
    ROOM_SCHOOL_ENTRANCE,
    SCHOOL_GATE_NO_ID_DIALOGUE,
    SCHOOL_GUARD_HAS_ID_DIALOGUE,
    SCHOOL_GUARD_NO_ID_REDIRECT_DIALOGUE,
    SCHOOL_GUARD_TEMP_PASS_DIALOGUE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKILL_ACADEMICS,
)
from src.game import Game
from src.level import Item
from src.npc import NPC


@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()


def test_school_entrance_links_intramuros_and_school(game):
    assert game.rooms[ROOM_INTRAMUROS].right.name == ROOM_SCHOOL_ENTRANCE
    assert game.rooms[ROOM_SCHOOL_ENTRANCE].left.name == ROOM_INTRAMUROS
    assert game.rooms[ROOM_SCHOOL_ENTRANCE].right.name == ROOM_SCHOOL
    assert game.rooms[ROOM_SCHOOL_ENTRANCE].up.name == ROOM_ADMIN_OFFICE
    assert game.rooms[ROOM_ADMIN_OFFICE].down.name == ROOM_SCHOOL_ENTRANCE
    assert game.rooms[ROOM_SCHOOL].left.name == ROOM_SCHOOL_ENTRANCE


def test_bedroom_contains_id_instead_of_notebook(game):
    game.current_room = 'bedroom'
    game.create_map()

    item = next(iter(game.item_sprites))

    assert item.name == "Student ID"
    assert item.item_id == ITEM_ID


def test_school_gate_blocks_player_without_id(game):
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))
    game.player.rect.center = gate.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_room == ROOM_SCHOOL_ENTRANCE
    assert game.current_dialogue == SCHOOL_GATE_NO_ID_DIALOGUE


def test_school_gate_allows_player_with_id(game):
    game.inventory.add_item(Item((0, 0), [], "Student ID", item_id=ITEM_ID))
    game.state.mark_item_picked(ITEM_ID)
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))
    game.player.rect.center = (gate.rect.left - 20, gate.rect.centery)

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_room == ROOM_SCHOOL_ENTRANCE
    assert game.player.rect.left > gate.rect.right


def test_school_gate_allows_player_with_temporary_campus_pass(game):
    game.state.temporary_campus_pass_day = game.current_day
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))
    game.player.rect.center = (gate.rect.left - 20, gate.rect.centery)

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_room == ROOM_SCHOOL_ENTRANCE
    assert game.player.rect.left > gate.rect.right


def test_school_entrance_has_second_section_gate_and_guards(game):
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()

    gate = next(iter(game.gate_sprites))
    section_width = SCREEN_WIDTH // 4

    assert section_width <= gate.rect.centerx < section_width * 2
    assert len(game.guard_sprites) == 2
    assert all(isinstance(guard, NPC) for guard in game.guard_sprites)
    assert all(not guard.can_wander for guard in game.guard_sprites)
    assert all(guard.sprite_asset == 'assets/images/guard.png' for guard in game.guard_sprites)
    assert all(
        guard.sprite_base_assets == ('assets/images/player.png', 'assets/images/mom.png')
        for guard in game.guard_sprites
    )


def test_school_entrance_guards_use_personalized_character_sprites(game):
    assert Path('assets/images/guard.png').exists()

    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    player_image = pygame.image.load('assets/images/player.png').convert_alpha()
    guard_asset = pygame.image.load('assets/images/guard.png').convert_alpha()
    player_pixels = pygame.image.tobytes(player_image, 'RGBA')

    for guard in game.guard_sprites:
        assert guard.image.get_size() == player_image.get_size()
        assert pygame.image.tobytes(guard.image, 'RGBA') != player_pixels
        assert pygame.image.tobytes(guard.image, 'RGBA') == pygame.image.tobytes(guard_asset, 'RGBA')


def test_school_entrance_has_modern_tile_floor(game):
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    floor_tile = next(iter(game.floor_sprites))

    assert floor_tile.image.get_at((1, 1))[:3] != (34, 139, 34)


def test_school_entrance_connects_to_north_room(game):
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))

    office_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == ROOM_ADMIN_OFFICE)
    assert office_door.rect.centerx > gate.rect.centerx

    game.player.rect.topleft = office_door.rect.topleft
    game.update()

    assert game.current_room == ROOM_ADMIN_OFFICE


def test_school_entrance_admin_path_has_clear_doorway(game):
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()

    office_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == ROOM_ADMIN_OFFICE)

    assert not any(sprite.rect.colliderect(office_door.rect) for sprite in game.obstacle_sprites)


def test_school_entrance_has_right_school_entrance_behind_gate(game):
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))

    school_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == ROOM_SCHOOL)

    assert school_door.rect.centerx > gate.rect.centerx


def test_school_entrance_guard_is_interactable(game):
    game.state.temporary_campus_pass_day = game.current_day
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    guard = next(iter(game.guard_sprites))
    game.player.rect.center = guard.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_dialogue == guard.dialogue


def test_admin_office_has_compact_waiting_area_with_clear_exit_path(game):
    game.current_room = ROOM_ADMIN_OFFICE
    game.create_map()

    exit_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == ROOM_SCHOOL_ENTRANCE)
    spawn_path = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 96, game.player.rect.width, 96)

    assert len(game.chair_sprites) == 24
    assert len({chair.rect.x for chair in game.chair_sprites}) == 6
    assert len({chair.rect.y for chair in game.chair_sprites}) == 4
    assert not any(chair.rect.colliderect(spawn_path) for chair in game.chair_sprites)
    assert not any(chair.rect.colliderect(exit_door.rect) for chair in game.chair_sprites)


def test_admin_office_exit_returns_to_school_entrance(game):
    game.current_room = ROOM_ADMIN_OFFICE
    game.create_map()

    exit_door = next(s for s in game.door_sprites if getattr(s, 'target_room', None) == ROOM_SCHOOL_ENTRANCE)
    game.player.rect.topleft = exit_door.rect.topleft
    game.update()

    assert game.current_room == ROOM_SCHOOL_ENTRANCE
    assert game.player.rect.topleft == exit_door.spawn_pos


def test_admin_office_has_interactable_attendant(game):
    game.current_room = ROOM_ADMIN_OFFICE
    game.create_map()
    attendant = next(iter(game.attendant_sprites))
    game.player.rect.center = attendant.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert attendant.name == "Attendant"
    assert attendant.sprite_base_assets == ('assets/images/player.png', 'assets/images/mom.png')
    assert game.current_dialogue == attendant.dialogue


def test_admin_office_attendant_grants_temporary_campus_pass_without_id(game):
    game.current_room = ROOM_ADMIN_OFFICE
    game.create_map()
    attendant = next(iter(game.attendant_sprites))
    game.player.rect.center = attendant.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_dialogue == ADMIN_OFFICE_NO_ID_DIALOGUE
    assert game.state.temporary_campus_pass_day == game.current_day
    assert game.state.admin_office_checked_in is False
    assert game.get_skill_xp(SKILL_ACADEMICS) == 0


def test_admin_office_attendant_repeats_active_temporary_pass(game):
    game.state.temporary_campus_pass_day = game.current_day
    game.current_room = ROOM_ADMIN_OFFICE
    game.create_map()
    attendant = next(iter(game.attendant_sprites))
    game.player.rect.center = attendant.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_dialogue == ADMIN_OFFICE_TEMP_PASS_ACTIVE_DIALOGUE
    assert game.state.temporary_campus_pass_day == game.current_day
    assert game.state.admin_office_checked_in is False
    assert game.get_skill_xp(SKILL_ACADEMICS) == 0


def test_admin_office_attendant_checks_in_student_with_id(game):
    game.inventory.add_item(Item((0, 0), [], "Student ID", item_id=ITEM_ID))
    game.state.mark_item_picked(ITEM_ID)
    game.current_room = ROOM_ADMIN_OFFICE
    game.create_map()
    attendant = next(iter(game.attendant_sprites))
    game.player.rect.center = attendant.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_dialogue == ADMIN_OFFICE_CHECK_IN_DIALOGUE
    assert game.state.admin_office_checked_in is True
    assert game.get_skill_xp(SKILL_ACADEMICS) == ADMIN_OFFICE_CHECK_IN_XP


def test_admin_office_check_in_reward_only_happens_once(game):
    game.inventory.add_item(Item((0, 0), [], "Student ID", item_id=ITEM_ID))
    game.state.mark_item_picked(ITEM_ID)
    game.current_room = ROOM_ADMIN_OFFICE
    game.create_map()
    attendant = next(iter(game.attendant_sprites))
    game.player.rect.center = attendant.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])
    game.finish_dialogue()
    game.handle_events([event])

    assert game.current_dialogue == ADMIN_OFFICE_CHECKED_IN_DIALOGUE
    assert game.get_skill_xp(SKILL_ACADEMICS) == ADMIN_OFFICE_CHECK_IN_XP


def test_school_guard_sends_no_id_student_to_admin_office(game):
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    guard = next(iter(game.guard_sprites))
    game.player.rect.center = guard.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_room == ROOM_ADMIN_OFFICE
    assert game.current_dialogue == SCHOOL_GUARD_NO_ID_REDIRECT_DIALOGUE
    assert game.state.temporary_campus_pass_day is None


def test_school_guard_recognizes_temporary_campus_pass(game):
    game.state.temporary_campus_pass_day = game.current_day
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    guard = next(iter(game.guard_sprites))
    game.player.rect.center = guard.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_room == ROOM_SCHOOL_ENTRANCE
    assert game.current_dialogue == SCHOOL_GUARD_TEMP_PASS_DIALOGUE


def test_school_guard_verifies_student_with_id(game):
    game.inventory.add_item(Item((0, 0), [], "Student ID", item_id=ITEM_ID))
    game.state.mark_item_picked(ITEM_ID)
    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    guard = next(iter(game.guard_sprites))
    game.player.rect.center = guard.rect.center

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    game.handle_events([event])

    assert game.current_dialogue == SCHOOL_GUARD_HAS_ID_DIALOGUE
