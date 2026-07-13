import os

import pygame
import pytest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["SDL_VIDEODRIVER"] = "dummy"

from src.config import (
    FIRST_DAY_ENERGY_STRESS_TUTORIAL_DIALOGUE,
    FIRST_DAY_GRADE_STANDING_TUTORIAL_DIALOGUE,
    FIRST_DAY_PLANNER_TUTORIAL_DIALOGUE,
    ITEM_ID,
    MAX_ENERGY,
    ROOM_OUTSIDE,
    ROOM_SCHOOL,
    ROOM_SCHOOL_ENTRANCE,
    SCHOOL_STUDY_ENERGY_COST,
)
from src.game import Game
from src.level import Item
from src.quest_definitions import (
    FIRST_DAY_ENTER_CAMPUS,
    FIRST_DAY_PICK_UP_ID,
    FIRST_DAY_QUEST_ID,
    FIRST_DAY_RIDE_BUS,
    FIRST_DAY_STUDY,
    FIRST_DAY_TALK_TO_MOM,
)
from src.quests import QUEST_ACTIVE, QUEST_DONE
from src.save_system import SaveSystem
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
    assert game.current_dialogue == FIRST_DAY_PLANNER_TUTORIAL_DIALOGUE

    game.current_room = ROOM_SCHOOL_ENTRANCE
    game.create_map()
    gate = next(iter(game.gate_sprites))
    game.player.rect.center = (gate.rect.left - 20, gate.rect.centery)
    game.try_enter_school_gate()
    assert first_day_quest(game).current_objective.description == "Study at the school desk."
    assert game.current_dialogue == FIRST_DAY_GRADE_STANDING_TUTORIAL_DIALOGUE

    game.current_room = ROOM_SCHOOL
    game.create_map()
    game.study_at_school()

    assert first_day_quest(game).status == QUEST_DONE
    assert game.get_skill_xp("academics") == 15
    assert game.current_dialogue == FIRST_DAY_ENERGY_STRESS_TUTORIAL_DIALOGUE


def test_planner_tutorial_names_deadlines_and_desktop_mobile_controls(game):
    game.advance_first_day_objective(FIRST_DAY_PICK_UP_ID)
    game.advance_first_day_objective(FIRST_DAY_TALK_TO_MOM)
    game.current_room = ROOM_OUTSIDE
    game.create_map()
    game.money = BUS_TRANSPORT.fare

    assert game.ride_bus() is True

    assert game.current_dialogue == FIRST_DAY_PLANNER_TUTORIAL_DIALOGUE
    copy = " ".join(game.current_dialogue).lower()
    assert "assignments" in copy
    assert "exams" in copy
    assert "deadlines" in copy
    assert "press p" in copy
    assert "planner button" in copy


def test_first_day_tutorial_beats_do_not_repeat_after_objective_advances(game):
    game.advance_first_day_objective(FIRST_DAY_PICK_UP_ID)
    game.advance_first_day_objective(FIRST_DAY_TALK_TO_MOM)
    game.current_room = ROOM_OUTSIDE
    game.create_map()
    game.money = BUS_TRANSPORT.fare * 2

    assert game.ride_bus() is True
    game.finish_dialogue()
    assert game.ride_bus() is True

    assert game.current_dialogue is None
    assert game.is_current_first_day_objective(FIRST_DAY_RIDE_BUS) is False


def test_study_tutorial_explains_energy_and_stress_without_changing_rewards(game):
    for objective_id in (
        FIRST_DAY_PICK_UP_ID,
        FIRST_DAY_TALK_TO_MOM,
        FIRST_DAY_RIDE_BUS,
        FIRST_DAY_ENTER_CAMPUS,
    ):
        game.advance_first_day_objective(objective_id)
    game.current_room = ROOM_SCHOOL
    game.create_map()

    assert game.study_at_school() is True

    assert game.energy == MAX_ENERGY - SCHOOL_STUDY_ENERGY_COST
    assert game.current_dialogue == FIRST_DAY_ENERGY_STRESS_TUTORIAL_DIALOGUE
    assert first_day_quest(game).status == QUEST_DONE
    assert game.get_skill_xp("academics") == 15
    assert game.is_current_first_day_objective(FIRST_DAY_STUDY) is False


def test_saved_quest_progress_preserves_tutorial_one_time_guards(game):
    game.advance_first_day_objective(FIRST_DAY_PICK_UP_ID)
    game.advance_first_day_objective(FIRST_DAY_TALK_TO_MOM)
    game.advance_first_day_objective(FIRST_DAY_RIDE_BUS)

    restored = SaveSystem.deserialize(SaveSystem.serialize(game.state))
    game.state = restored

    assert game.is_current_first_day_objective(FIRST_DAY_RIDE_BUS) is False
