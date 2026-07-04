import os

import pygame
import pytest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["SDL_VIDEODRIVER"] = "dummy"

from src.config import ITEM_ID, ROOM_OUTSIDE, ROOM_SCHOOL, ROOM_SCHOOL_ENTRANCE
from src.game import Game
from src.level import Item
from src.quest_definitions import (
    FIRST_DAY_QUEST_ID,
    FIRST_DAY_RIDE_BUS,
    FIRST_DAY_TALK_TO_MOM,
)
from src.quests import QUEST_ACTIVE, QUEST_DONE
from src.transport import BUS_TRANSPORT


@pytest.fixture
def game():
    pygame.init()
    game = Game()
    yield game
    pygame.quit()


def first_day_quest(game):
    return game.quest_manager.get_quest(FIRST_DAY_QUEST_ID)


def test_game_starts_first_day_quest(game):
    quest = first_day_quest(game)

    assert quest.status == QUEST_ACTIVE
    assert quest.current_objective.description == "Pick up your Student ID."
    assert game.quest_manager.current_objective == "Pick up your Student ID."


def test_first_day_quest_rejects_out_of_order_objectives(game):
    quest = first_day_quest(game)

    assert game.advance_first_day_objective(FIRST_DAY_TALK_TO_MOM) is None
    assert quest.current_objective.objective_id != FIRST_DAY_RIDE_BUS


def test_first_day_quest_tracks_current_game_loop(game):
    game.pick_up_item(Item((0, 0), [], "Student ID", item_id=ITEM_ID))
    assert first_day_quest(game).current_objective.description == "Talk to Mom for your allowance."

    game.give_daily_allowance()
    assert first_day_quest(game).current_objective.description == "Ride the bus to Intramuros."

    game.current_room = ROOM_OUTSIDE
    game.create_map()
    game.money = BUS_TRANSPORT.fare
    game.ride_bus()
    assert first_day_quest(game).current_objective.description == "Use your Student ID to enter campus."

    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))
    game.player.rect.center = (gate.rect.left - 20, gate.rect.centery)
    game.try_enter_school_gate()
    assert first_day_quest(game).current_objective.description == "Study at the school desk."

    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.study_at_school()

    assert first_day_quest(game).status == QUEST_DONE
    assert game.get_skill_xp("academics") == 15
