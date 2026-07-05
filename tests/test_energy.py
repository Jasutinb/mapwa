import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import (
    CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE,
    ELECTRONICS_PRACTICE_ENERGY_COST,
    ELECTRONICS_LAB_XP,
    INSUFFICIENT_ENERGY_DIALOGUE,
    LIBRARY_STUDY_ENERGY_COST,
    LIBRARY_STUDY_XP,
    LOW_ENERGY_STRESS_DIALOGUE,
    LOW_ENERGY_STRESS_INCREASE,
    MAX_ENERGY,
    MEAL_ENERGY,
    MEAL_PRICE,
    PROGRAMMING_LAB_XP,
    PROGRAMMING_PRACTICE_ENERGY_COST,
    ROOM_CAFETERIA,
    ROOM_ELECTRONICS_LAB,
    ROOM_LIBRARY,
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL,
    SCHOOL_STUDY_ENERGY_COST,
    SKILL_ACADEMICS,
    SKILL_ELECTRONICS,
    SKILL_MATH,
    SKILL_PROGRAMMING,
    STUDY_XP,
)
from src.game import Game
from src.quest_definitions import (
    HELLO_WORLD_PRACTICE_PROGRAMMING,
    HELLO_WORLD_QUEST_ID,
    HELLO_WORLD_REWARD_XP,
)
from src.quests import QUEST_DONE


LOW_ENERGY_DIALOGUE = INSUFFICIENT_ENERGY_DIALOGUE + [
    LOW_ENERGY_STRESS_DIALOGUE.format(amount=LOW_ENERGY_STRESS_INCREASE)
]


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def test_sleep_restores_energy_to_max(game):
    game.energy = 7

    game.sleep_until_next_day()

    assert game.current_day == 2
    assert game.energy == MAX_ENERGY


def test_school_study_spends_energy_when_started(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.player.rect.center = game.school_desk.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.energy == MAX_ENERGY - SCHOOL_STUDY_ENERGY_COST
    assert game.get_skill_xp(SKILL_ACADEMICS) == STUDY_XP
    assert game.player.studying is True


def test_school_study_blocks_when_energy_is_low(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.energy = SCHOOL_STUDY_ENERGY_COST - 1
    game.player.rect.center = game.school_desk.rect.center

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    assert game.energy == SCHOOL_STUDY_ENERGY_COST - 1
    assert game.get_skill_xp(SKILL_ACADEMICS) == 0
    assert game.player.studying is False
    assert game.current_dialogue == LOW_ENERGY_DIALOGUE


def test_programming_practice_spends_energy_and_completes_quest(game):
    game.travel_to_room(ROOM_PROGRAMMING_LAB)
    game.player.rect.center = game.programming_station.rect.center

    game.practice_programming()

    assert game.energy == MAX_ENERGY - PROGRAMMING_PRACTICE_ENERGY_COST
    assert game.quest_manager.get_quest(HELLO_WORLD_QUEST_ID).status == QUEST_DONE
    assert game.get_skill_xp(SKILL_PROGRAMMING) == PROGRAMMING_LAB_XP + HELLO_WORLD_REWARD_XP


def test_programming_practice_blocks_without_quest_progress_when_energy_is_low(game):
    game.travel_to_room(ROOM_PROGRAMMING_LAB)
    quest = game.quest_manager.get_quest(HELLO_WORLD_QUEST_ID)
    assert quest.current_objective.objective_id == HELLO_WORLD_PRACTICE_PROGRAMMING
    game.energy = PROGRAMMING_PRACTICE_ENERGY_COST - 1

    game.practice_programming()

    assert game.energy == PROGRAMMING_PRACTICE_ENERGY_COST - 1
    assert quest.current_objective.objective_id == HELLO_WORLD_PRACTICE_PROGRAMMING
    assert game.get_skill_xp(SKILL_PROGRAMMING) == 0
    assert game.current_dialogue == LOW_ENERGY_DIALOGUE


def test_electronics_practice_spends_energy(game):
    game.current_room = ROOM_ELECTRONICS_LAB
    game.create_map()

    game.practice_electronics()

    assert game.energy == MAX_ENERGY - ELECTRONICS_PRACTICE_ENERGY_COST
    assert game.get_skill_xp(SKILL_ELECTRONICS) == ELECTRONICS_LAB_XP


def test_electronics_practice_blocks_when_energy_is_low(game):
    game.current_room = ROOM_ELECTRONICS_LAB
    game.create_map()
    game.energy = ELECTRONICS_PRACTICE_ENERGY_COST - 1

    game.practice_electronics()

    assert game.energy == ELECTRONICS_PRACTICE_ENERGY_COST - 1
    assert game.get_skill_xp(SKILL_ELECTRONICS) == 0
    assert game.current_dialogue == LOW_ENERGY_DIALOGUE


def test_library_study_spends_energy(game):
    game.current_room = ROOM_LIBRARY
    game.create_map()

    game.study_at_library(SKILL_MATH, "math")

    assert game.energy == MAX_ENERGY - LIBRARY_STUDY_ENERGY_COST
    assert game.get_skill_xp(SKILL_MATH) == LIBRARY_STUDY_XP


def test_mobile_library_study_blocks_when_energy_is_low(game):
    game.current_room = ROOM_LIBRARY
    game.create_map()
    game.energy = LIBRARY_STUDY_ENERGY_COST - 1
    game.player.rect.center = game.library_math_station.rect.center
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.energy == LIBRARY_STUDY_ENERGY_COST - 1
    assert game.get_skill_xp(SKILL_MATH) == 0
    assert game.current_dialogue == LOW_ENERGY_DIALOGUE


def test_food_still_restores_spent_energy_after_activity_costs(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE
    game.energy = MAX_ENERGY - MEAL_ENERGY

    game.buy_cafeteria_meal()

    assert game.money == 0
    assert game.energy == MAX_ENERGY


def test_food_purchase_still_blocks_without_money(game):
    game.current_room = ROOM_CAFETERIA
    game.create_map()
    game.money = MEAL_PRICE - 1
    game.energy = MAX_ENERGY - MEAL_ENERGY

    game.buy_cafeteria_meal()

    assert game.money == MEAL_PRICE - 1
    assert game.energy == MAX_ENERGY - MEAL_ENERGY
    assert game.current_dialogue == CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE
