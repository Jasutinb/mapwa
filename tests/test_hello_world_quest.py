import os

import pygame
import pytest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["SDL_VIDEODRIVER"] = "dummy"

from src.config import (
    PROGRAMMING_LAB_XP,
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL,
    SKILL_PROGRAMMING,
)
from src.game import Game
from src.quest_definitions import (
    HELLO_WORLD_ENTER_LAB,
    HELLO_WORLD_PRACTICE_PROGRAMMING,
    HELLO_WORLD_QUEST_ID,
    HELLO_WORLD_REWARD_XP,
)
from src.quests import QUEST_ACTIVE, QUEST_DONE


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def hello_world_quest(game):
    return game.quest_manager.get_quest(HELLO_WORLD_QUEST_ID)


def test_game_starts_hello_world_quest_behind_first_day(game):
    quest = hello_world_quest(game)

    assert quest.status == QUEST_ACTIVE
    assert quest.current_objective.description == "Find the Programming Lab."
    assert game.quest_manager.current_objective == "Pick up your Student ID."


def test_hello_world_rejects_out_of_order_programming_practice(game):
    quest = hello_world_quest(game)

    assert game.advance_hello_world_objective(HELLO_WORLD_PRACTICE_PROGRAMMING) is None
    assert quest.current_objective.objective_id == HELLO_WORLD_ENTER_LAB


def test_entering_programming_lab_advances_hello_world_quest(game):
    game.current_room = ROOM_SCHOOL
    game.create_map()
    lab_door = next(s for s in game.door_sprites if s.target_room == ROOM_PROGRAMMING_LAB)

    game.player.rect.topleft = lab_door.rect.topleft
    game.update()

    quest = hello_world_quest(game)
    assert game.current_room == ROOM_PROGRAMMING_LAB
    assert quest.current_objective.objective_id == HELLO_WORLD_PRACTICE_PROGRAMMING


def test_programming_practice_completes_hello_world_and_applies_reward(game):
    game.travel_to_room(ROOM_PROGRAMMING_LAB)
    game.player.rect.center = game.programming_station.rect.center

    game.practice_programming()

    assert hello_world_quest(game).status == QUEST_DONE
    assert game.get_skill_xp(SKILL_PROGRAMMING) == PROGRAMMING_LAB_XP + HELLO_WORLD_REWARD_XP
    assert game.current_dialogue == [
        "You practiced coding and gained 10 programming XP! Total: 15."
    ]


def test_hello_world_reward_only_applies_once(game):
    game.travel_to_room(ROOM_PROGRAMMING_LAB)

    game.practice_programming()
    game.practice_programming()

    assert hello_world_quest(game).status == QUEST_DONE
    assert game.get_skill_xp(SKILL_PROGRAMMING) == PROGRAMMING_LAB_XP * 2 + HELLO_WORLD_REWARD_XP
