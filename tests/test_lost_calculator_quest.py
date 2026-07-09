import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from src.config import (
    DEBUG_CODE_SIDE_HUSTLE_DIALOGUE,
    DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP,
    DEBUG_CODE_SIDE_HUSTLE_MONEY,
    DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP,
    LOST_CALCULATOR_ITEM_ID,
    LOST_CALCULATOR_RETURN_DIALOGUE,
    LOST_CALCULATOR_SEARCH_DIALOGUE,
    LOST_CALCULATOR_START_DIALOGUE,
    ROOM_LIBRARY,
    ROOM_SCHOOL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKILL_FINANCE,
    SKILL_PROGRAMMING,
    SKILL_SOCIAL,
)
from src.game import Game
from src.quest_definitions import (
    LOST_CALCULATOR_PICK_UP,
    LOST_CALCULATOR_QUEST_ID,
    LOST_CALCULATOR_RETURN,
    LOST_CALCULATOR_REWARD_XP,
)
from src.quests import QUEST_ACTIVE, QUEST_DONE, QUEST_NOT_STARTED


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    g = Game()
    yield g
    pygame.quit()


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=key)])


def press_mobile_action(game):
    action_pos = game.mobile_controls.rects["action"].center
    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )


def lost_calculator_quest(game):
    return game.quest_manager.get_quest(LOST_CALCULATOR_QUEST_ID)


def place_player_at_classmate(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()
    classmate = next(iter(game.classmate_sprites))
    game.player.rect.center = classmate.rect.center
    return classmate


def start_lost_calculator_quest(game):
    place_player_at_classmate(game)
    game.state.has_talked_to_classmate = True
    assert game.talk_to_classmate() is True
    return lost_calculator_quest(game)


def get_calculator_item(game):
    return next(
        item for item in game.item_sprites if item.item_id == LOST_CALCULATOR_ITEM_ID
    )


def test_lost_calculator_starts_from_classmate_after_social_intro(game):
    quest = lost_calculator_quest(game)
    classmate = place_player_at_classmate(game)

    assert quest.status == QUEST_NOT_STARTED

    press_key(game, pygame.K_e)
    assert quest.status == QUEST_NOT_STARTED

    game.finish_dialogue()
    press_key(game, pygame.K_e)

    assert quest.status == QUEST_ACTIVE
    assert quest.current_objective.objective_id == LOST_CALCULATOR_PICK_UP
    assert game.current_dialogue == list(LOST_CALCULATOR_START_DIALOGUE)
    assert classmate.dialogue == list(LOST_CALCULATOR_START_DIALOGUE)


def test_calculator_spawns_in_library_only_while_pickup_objective_is_active(game):
    game.travel_to_room(ROOM_LIBRARY)
    assert not any(item.item_id == LOST_CALCULATOR_ITEM_ID for item in game.item_sprites)

    quest = start_lost_calculator_quest(game)
    game.finish_dialogue()
    game.travel_to_room(ROOM_LIBRARY)

    calculator = get_calculator_item(game)

    assert quest.current_objective.objective_id == LOST_CALCULATOR_PICK_UP
    assert calculator.name == "Calculator"
    assert calculator in game.visible_sprites
    assert calculator not in game.obstacle_sprites


def test_pc_player_can_pick_up_and_return_lost_calculator(game):
    quest = start_lost_calculator_quest(game)
    game.finish_dialogue()
    game.travel_to_room(ROOM_LIBRARY)
    calculator = get_calculator_item(game)
    game.player.rect.center = calculator.rect.center

    press_key(game, pygame.K_e)

    assert game.has_inventory_item(LOST_CALCULATOR_ITEM_ID)
    assert quest.current_objective.objective_id == LOST_CALCULATOR_RETURN
    assert game.current_dialogue == ["You picked up a Calculator!"]

    game.finish_dialogue()
    place_player_at_classmate(game)
    press_key(game, pygame.K_e)

    assert quest.status == QUEST_DONE
    assert not game.has_inventory_item(LOST_CALCULATOR_ITEM_ID)
    assert game.get_skill_xp(SKILL_SOCIAL) == LOST_CALCULATOR_REWARD_XP
    assert game.current_dialogue == [
        LOST_CALCULATOR_RETURN_DIALOGUE.format(
            xp=LOST_CALCULATOR_REWARD_XP,
            total=LOST_CALCULATOR_REWARD_XP,
        )
    ]


def test_lost_calculator_reward_only_applies_once(game):
    quest = start_lost_calculator_quest(game)
    game.finish_dialogue()
    game.travel_to_room(ROOM_LIBRARY)
    calculator = get_calculator_item(game)

    assert game.pick_up_item(calculator)
    game.finish_dialogue()
    place_player_at_classmate(game)
    assert game.talk_to_classmate() is True

    game.finish_dialogue()
    assert game.talk_to_classmate() is True

    assert quest.status == QUEST_DONE
    assert game.get_skill_xp(SKILL_SOCIAL) == LOST_CALCULATOR_REWARD_XP
    assert game.money == DEBUG_CODE_SIDE_HUSTLE_MONEY
    assert game.get_skill_xp(SKILL_PROGRAMMING) == DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP
    assert game.get_skill_xp(SKILL_FINANCE) == DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP
    assert game.current_dialogue == [
        line.format(
            money=DEBUG_CODE_SIDE_HUSTLE_MONEY,
            programming_xp=DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP,
            programming_total=DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP,
            finance_xp=DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP,
            finance_total=DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP,
        )
        for line in DEBUG_CODE_SIDE_HUSTLE_DIALOGUE
    ]


def test_classmate_reminds_player_to_search_before_calculator_is_found(game):
    start_lost_calculator_quest(game)
    game.finish_dialogue()
    place_player_at_classmate(game)

    assert game.talk_to_classmate() is True

    assert game.current_dialogue == list(LOST_CALCULATOR_SEARCH_DIALOGUE)


def test_mobile_action_can_start_pick_up_and_return_lost_calculator(game):
    quest = lost_calculator_quest(game)
    place_player_at_classmate(game)
    game.state.has_talked_to_classmate = True

    press_mobile_action(game)

    assert quest.status == QUEST_ACTIVE
    assert quest.current_objective.objective_id == LOST_CALCULATOR_PICK_UP

    game.finish_dialogue()
    game.travel_to_room(ROOM_LIBRARY)
    calculator = get_calculator_item(game)
    game.player.rect.center = calculator.rect.center

    press_mobile_action(game)

    assert game.has_inventory_item(LOST_CALCULATOR_ITEM_ID)
    assert quest.current_objective.objective_id == LOST_CALCULATOR_RETURN

    game.finish_dialogue()
    place_player_at_classmate(game)
    press_mobile_action(game)

    assert quest.status == QUEST_DONE
    assert not game.has_inventory_item(LOST_CALCULATOR_ITEM_ID)
    assert game.get_skill_xp(SKILL_SOCIAL) == LOST_CALCULATOR_REWARD_XP
