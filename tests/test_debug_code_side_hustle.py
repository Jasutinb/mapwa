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
    DEBUG_CODE_SIDE_HUSTLE_REPEAT_DIALOGUE,
    LOST_CALCULATOR_ITEM_ID,
    ROOM_SCHOOL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKILL_FINANCE,
    SKILL_PROGRAMMING,
)
from src.game import Game
from src.quest_definitions import (
    LOST_CALCULATOR_PICK_UP,
    LOST_CALCULATOR_QUEST_ID,
    LOST_CALCULATOR_RETURN,
)


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    g = Game()
    g.current_room = ROOM_SCHOOL
    g.create_map()
    yield g
    pygame.quit()


def place_player_at_classmate(game):
    classmate = next(iter(game.classmate_sprites))
    game.player.rect.center = classmate.rect.center
    return classmate


def finish_lost_calculator_thread(game):
    game.state.has_talked_to_classmate = True
    game.start_quest(LOST_CALCULATOR_QUEST_ID)
    game.advance_lost_calculator_objective(LOST_CALCULATOR_PICK_UP)
    game.state.inventory_item_ids.append(LOST_CALCULATOR_ITEM_ID)
    game.advance_lost_calculator_objective(LOST_CALCULATOR_RETURN)
    place_player_at_classmate(game)


def debug_code_dialogue(programming_total, finance_total):
    return [
        line.format(
            money=DEBUG_CODE_SIDE_HUSTLE_MONEY,
            programming_xp=DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP,
            programming_total=programming_total,
            finance_xp=DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP,
            finance_total=finance_total,
        )
        for line in DEBUG_CODE_SIDE_HUSTLE_DIALOGUE
    ]


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=key)])


def press_mobile_action(game):
    action_pos = game.mobile_controls.rects["action"].center
    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )


def test_classmate_debug_code_side_hustle_rewards_money_and_skills(game):
    finish_lost_calculator_thread(game)
    starting_energy = game.energy
    starting_stress = game.stress
    starting_day = game.current_day

    assert game.talk_to_classmate() is True

    assert game.money == DEBUG_CODE_SIDE_HUSTLE_MONEY
    assert game.get_skill_xp(SKILL_PROGRAMMING) == DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP
    assert game.get_skill_xp(SKILL_FINANCE) == DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP
    assert game.energy == starting_energy
    assert game.stress == starting_stress
    assert game.current_day == starting_day
    assert game.current_dialogue == debug_code_dialogue(
        DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP,
        DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP,
    )


def test_classmate_debug_code_side_hustle_is_once_per_day(game):
    finish_lost_calculator_thread(game)

    assert game.talk_to_classmate() is True
    game.finish_dialogue()
    assert game.talk_to_classmate() is True

    assert game.money == DEBUG_CODE_SIDE_HUSTLE_MONEY
    assert game.get_skill_xp(SKILL_PROGRAMMING) == DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP
    assert game.get_skill_xp(SKILL_FINANCE) == DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP
    assert game.current_dialogue == list(DEBUG_CODE_SIDE_HUSTLE_REPEAT_DIALOGUE)


def test_classmate_debug_code_side_hustle_resets_next_day(game):
    finish_lost_calculator_thread(game)

    assert game.talk_to_classmate() is True
    game.finish_dialogue()
    game.current_day += 1
    assert game.talk_to_classmate() is True

    assert game.money == DEBUG_CODE_SIDE_HUSTLE_MONEY * 2
    assert game.get_skill_xp(SKILL_PROGRAMMING) == (
        DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP * 2
    )
    assert game.get_skill_xp(SKILL_FINANCE) == DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP * 2
    assert game.current_dialogue == debug_code_dialogue(
        DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP * 2,
        DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP * 2,
    )


def test_mobile_action_can_complete_classmate_debug_code_side_hustle(game):
    finish_lost_calculator_thread(game)

    press_mobile_action(game)

    assert game.money == DEBUG_CODE_SIDE_HUSTLE_MONEY
    assert game.get_skill_xp(SKILL_PROGRAMMING) == DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP
    assert game.get_skill_xp(SKILL_FINANCE) == DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP
    assert game.current_dialogue == debug_code_dialogue(
        DEBUG_CODE_SIDE_HUSTLE_PROGRAMMING_XP,
        DEBUG_CODE_SIDE_HUSTLE_FINANCE_XP,
    )


def test_debug_code_side_hustle_waits_for_classmate_relationship_thread(game):
    place_player_at_classmate(game)

    press_key(game, pygame.K_e)

    assert game.money == 0
    assert game.get_skill_xp(SKILL_PROGRAMMING) == 0
    assert game.get_skill_xp(SKILL_FINANCE) == 0
