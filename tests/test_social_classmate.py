import os
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from src.config import (
    CLASSMATE_INTRO_DIALOGUE,
    CLASSMATE_SOCIAL_XP,
    LOST_CALCULATOR_START_DIALOGUE,
    ROOM_SCHOOL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKILL_ACADEMICS,
    SKILL_SOCIAL,
    STUDY_XP,
    TILE_SIZE,
)
from src.game import Game
from src.npc import NPC


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    g = Game()
    g.current_room = ROOM_SCHOOL
    g.create_map()
    yield g
    pygame.quit()


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=key)])


def classmate_intro_dialogue(total=CLASSMATE_SOCIAL_XP):
    return [
        line.format(xp=CLASSMATE_SOCIAL_XP, total=total)
        for line in CLASSMATE_INTRO_DIALOGUE
    ]


def test_school_has_one_classmate_npc(game):
    classmate = next(iter(game.classmate_sprites))

    assert len(game.classmate_sprites) == 1
    assert isinstance(classmate, NPC)
    assert classmate.name == "Classmate"
    assert classmate in game.visible_sprites
    assert classmate in game.obstacle_sprites
    assert classmate.sprite_asset == "assets/images/classmate.png"
    assert classmate.sprite_base_assets == (
        "assets/images/player.png",
        "assets/images/mom.png",
    )


def test_classmate_sprite_uses_personalized_character_art(game):
    assert Path("assets/images/classmate.png").exists()

    player_image = pygame.image.load("assets/images/player.png").convert_alpha()
    classmate_image = pygame.image.load("assets/images/classmate.png").convert_alpha()

    assert classmate_image.get_size() == player_image.get_size()
    assert pygame.image.tobytes(classmate_image, "RGBA") != pygame.image.tobytes(
        player_image, "RGBA"
    )


def test_classmate_does_not_block_core_school_interactions(game):
    classmate = next(iter(game.classmate_sprites))
    blocked_objects = [
        *game.door_sprites,
        game.school_desk,
        game.school_class_marker,
        game.school_exam_marker,
    ]
    transition_paths = [
        pygame.Rect(0, SCREEN_HEIGHT // 2 - TILE_SIZE, TILE_SIZE * 4, TILE_SIZE * 3),
        pygame.Rect(
            SCREEN_WIDTH - TILE_SIZE * 4,
            SCREEN_HEIGHT // 2 - TILE_SIZE,
            TILE_SIZE * 4,
            TILE_SIZE * 3,
        ),
        pygame.Rect(
            SCREEN_WIDTH // 2 - TILE_SIZE * 2,
            0,
            TILE_SIZE * 4,
            TILE_SIZE * 4,
        ),
        pygame.Rect(
            SCREEN_WIDTH - TILE_SIZE * 7,
            SCREEN_HEIGHT - TILE_SIZE * 4,
            TILE_SIZE * 3,
            TILE_SIZE * 4,
        ),
        pygame.Rect(
            TILE_SIZE * 4,
            SCREEN_HEIGHT - TILE_SIZE * 4,
            TILE_SIZE * 3,
            TILE_SIZE * 4,
        ),
    ]

    assert not any(classmate.rect.colliderect(sprite.rect) for sprite in blocked_objects)
    assert not any(classmate.rect.colliderect(path) for path in transition_paths)


def test_pc_interaction_with_classmate_unlocks_social_skill_once(game):
    classmate = next(iter(game.classmate_sprites))
    game.player.rect.center = classmate.rect.center

    press_key(game, pygame.K_e)

    assert game.state.has_talked_to_classmate is True
    assert game.get_skill_xp(SKILL_SOCIAL) == CLASSMATE_SOCIAL_XP
    assert game.current_dialogue == classmate_intro_dialogue()


def test_follow_up_classmate_interaction_does_not_grant_extra_social_xp(game):
    classmate = next(iter(game.classmate_sprites))
    game.player.rect.center = classmate.rect.center

    assert game.talk_to_classmate() is True
    game.finish_dialogue()
    assert game.talk_to_classmate() is True

    assert game.get_skill_xp(SKILL_SOCIAL) == CLASSMATE_SOCIAL_XP
    assert game.current_dialogue == list(LOST_CALCULATOR_START_DIALOGUE)


def test_mobile_action_button_talks_to_classmate(game):
    classmate = next(iter(game.classmate_sprites))
    game.player.rect.center = classmate.rect.center
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.state.has_talked_to_classmate is True
    assert game.get_skill_xp(SKILL_SOCIAL) == CLASSMATE_SOCIAL_XP
    assert game.current_dialogue == classmate_intro_dialogue()


def test_school_desk_study_interaction_still_works(game):
    game.player.rect.center = game.school_desk.rect.center

    press_key(game, pygame.K_e)

    assert game.get_skill_xp(SKILL_ACADEMICS) == STUDY_XP
    assert game.get_skill_xp(SKILL_SOCIAL) == 0
