import os

import pygame
import pytest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["SDL_VIDEODRIVER"] = "dummy"

from src.game import Game
from src.quests import QUEST_ACTIVE, QUEST_DONE, Quest, QuestManager, QuestObjective, QuestReward


@pytest.fixture
def game():
    pygame.init()
    game = Game()
    yield game
    pygame.quit()


def test_quest_manager_tracks_active_objective():
    manager = QuestManager()
    quest = Quest(
        "first-day",
        "First Day",
        [QuestObjective("Pick up your ID"), QuestObjective("Reach school")],
    )

    manager.add_quest(quest)
    manager.start_quest("first-day")

    assert quest.status == QUEST_ACTIVE
    assert manager.current_objective == "Pick up your ID"

    assert manager.advance_quest("first-day") is None
    assert manager.current_objective == "Reach school"


def test_quest_completion_returns_reward_once():
    manager = QuestManager()
    reward = QuestReward(money=50, skill_xp={"academics": 5})
    quest = Quest("study", "Study", [QuestObjective("Study", target=2)], reward)

    manager.add_quest(quest)

    assert manager.advance_quest("study") is None
    assert manager.advance_quest("study") == reward
    assert quest.status == QUEST_DONE
    assert manager.advance_quest("study") is None


def test_quest_manager_advances_named_current_objective():
    manager = QuestManager()
    quest = Quest(
        "campus",
        "Campus",
        [
            QuestObjective("Get ID", objective_id="get_id"),
            QuestObjective("Enter campus", objective_id="enter_campus"),
        ],
    )
    manager.add_quest(quest)

    assert manager.advance_objective("campus", "enter_campus") is None
    assert quest.current_objective.description == "Get ID"

    manager.advance_objective("campus", "get_id")
    assert quest.current_objective.description == "Enter campus"


def test_quest_manager_rejects_duplicate_quests():
    manager = QuestManager()
    quest = Quest("dupe", "Duplicate", [QuestObjective("Do it")])
    manager.add_quest(quest)

    with pytest.raises(ValueError):
        manager.add_quest(quest)


def test_game_applies_quest_rewards(game):
    quest = Quest(
        "reward",
        "Reward",
        [QuestObjective("Complete task")],
        QuestReward(money=75, skill_xp={"academics": 4}),
    )

    game.add_quest(quest)
    reward = game.advance_quest("reward")

    assert reward is quest.reward
    assert game.money == 75
    assert game.get_skill_xp("academics") == 4
