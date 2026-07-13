import json
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from src.assignments import ASSIGNMENT_STATUS_COMPLETED
from src.config import ITEM_ID, ROOM_LIBRARY, ROOM_PROGRAMMING_LAB, SKILL_ACADEMICS
from src.exams import EXAM_STATUS_PASSED
from src.game import Game
from src.game_state import GameState
from src.level import Item
from src.quest_definitions import HELLO_WORLD_ENTER_LAB, HELLO_WORLD_QUEST_ID
from src.quests import QUEST_ACTIVE
from src.save_system import (
    BrowserSaveStorage,
    DesktopSaveStorage,
    IncompatibleSaveError,
    SaveError,
    SaveNotFoundError,
    SaveSystem,
)


class MemoryStorage:
    def __init__(self, content=None):
        self.content = content

    def read(self):
        return self.content

    def write(self, content):
        self.content = content


class FakeLocalStorage:
    def __init__(self):
        self.values = {}

    def getItem(self, key):
        return self.values.get(key)

    def setItem(self, key, value):
        self.values[key] = value


class FakeWindow:
    def __init__(self):
        self.localStorage = FakeLocalStorage()


@pytest.fixture
def game():
    pygame.init()
    instance = Game()
    instance.save_system = SaveSystem(MemoryStorage())
    yield instance
    pygame.quit()


def create_progressed_state():
    state = GameState()
    state.current_room = ROOM_LIBRARY
    state.current_day = 4
    state.money = 375
    state.energy = 42
    state.stress = 37
    state.grade_standing = 81
    state.has_talked_to_mom = True
    state.has_talked_to_classmate = True
    state.last_allowance_day = 4
    state.last_debug_code_side_hustle_day = 3
    state.admin_office_checked_in = True
    state.temporary_campus_pass_day = 4
    state.attended_class_day = 4
    state.attended_class_ids.add("day-4-academics")
    state.mark_item_picked(ITEM_ID)
    state.skill_xp_manager.xp_by_skill[SKILL_ACADEMICS] = 30

    quest = next(iter(state.quest_manager.quests.values()))
    quest.status = QUEST_ACTIVE
    quest.objectives[0].progress = min(1, quest.objectives[0].target)
    state.assignments[0].status = ASSIGNMENT_STATUS_COMPLETED
    state.assignments[0].missed_stress_applied = True
    state.exams[0].status = EXAM_STATUS_PASSED
    state.exams[0].attempts = 2
    return state


def test_game_state_round_trip_restores_major_progress():
    storage = MemoryStorage()
    save_system = SaveSystem(storage)
    original = create_progressed_state()

    save_system.save(original)
    restored = save_system.load()

    assert restored.current_room == ROOM_LIBRARY
    assert restored.current_day == 4
    assert restored.money == 375
    assert restored.energy == 42
    assert restored.stress == 37
    assert restored.grade_standing == 81
    assert restored.has_talked_to_mom is True
    assert restored.has_talked_to_classmate is True
    assert restored.last_allowance_day == 4
    assert restored.last_debug_code_side_hustle_day == 3
    assert restored.admin_office_checked_in is True
    assert restored.temporary_campus_pass_day == 4
    assert restored.attended_class_ids == {"day-4-academics"}
    assert restored.inventory_item_ids == [ITEM_ID]
    assert restored.picked_item_ids == {ITEM_ID}
    assert restored.skill_xp_manager.get_xp(SKILL_ACADEMICS) == 30

    original_quest = next(iter(original.quest_manager.quests.values()))
    restored_quest = restored.quest_manager.get_quest(original_quest.quest_id)
    assert restored_quest.status == QUEST_ACTIVE
    assert restored_quest.objectives[0].progress == original_quest.objectives[0].progress
    assert restored.assignments[0].status == ASSIGNMENT_STATUS_COMPLETED
    assert restored.assignments[0].missed_stress_applied is True
    assert restored.exams[0].status == EXAM_STATUS_PASSED
    assert restored.exams[0].attempts == 2


def test_missing_corrupt_and_incompatible_saves_fail_safely():
    with pytest.raises(SaveNotFoundError):
        SaveSystem(MemoryStorage()).load()

    with pytest.raises(SaveError, match="corrupt"):
        SaveSystem(MemoryStorage("not-json")).load()

    old_payload = SaveSystem.serialize(GameState())
    old_payload["version"] = 0
    with pytest.raises(IncompatibleSaveError):
        SaveSystem(MemoryStorage(json.dumps(old_payload))).load()


def test_deserializer_rejects_invalid_state_without_partial_restore():
    payload = SaveSystem.serialize(GameState())
    payload["state"]["energy"] = "full"

    with pytest.raises(SaveError, match="energy"):
        SaveSystem.deserialize(payload)


def test_desktop_storage_round_trip_uses_utf8_file(tmp_path):
    path = tmp_path / "save.json"
    save_system = SaveSystem(DesktopSaveStorage(path))
    state = create_progressed_state()

    save_system.save(state)

    assert path.exists()
    assert save_system.load().money == state.money


def test_browser_storage_round_trip_uses_local_storage():
    window = FakeWindow()
    save_system = SaveSystem(BrowserSaveStorage("mapwa-test", window=window))

    save_system.save(create_progressed_state())

    assert "mapwa-test" in window.localStorage.values
    assert save_system.load().current_room == ROOM_LIBRARY


def test_game_save_and_load_restores_room_inventory_and_state(game):
    game.current_room = ROOM_LIBRARY
    game.current_day = 4
    game.money = 375
    game.energy = 42
    game.inventory.add_item(Item((0, 0), [], "Student ID", item_id=ITEM_ID))
    game.state.mark_item_picked(ITEM_ID)

    assert game.save_game()

    game.current_room = "main"
    game.current_day = 1
    game.money = 0
    game.energy = 100
    game.inventory = game.inventory.__class__()

    assert game.load_game()
    assert game.current_room == ROOM_LIBRARY
    assert game.current_day == 4
    assert game.money == 375
    assert game.energy == 42
    assert game.inventory.has_item(ITEM_ID)
    assert game.player in game.visible_sprites
    assert game.current_dialogue == ["Game loaded."]


def test_loading_room_does_not_replay_room_entry_quest_progress(game):
    game.current_room = ROOM_PROGRAMMING_LAB
    quest = game.quest_manager.get_quest(HELLO_WORLD_QUEST_ID)
    objective = next(
        item for item in quest.objectives if item.objective_id == HELLO_WORLD_ENTER_LAB
    )
    assert objective.progress == 0
    game.save_system.save(game.state)

    assert game.load_game()

    loaded_quest = game.quest_manager.get_quest(HELLO_WORLD_QUEST_ID)
    loaded_objective = next(
        item
        for item in loaded_quest.objectives
        if item.objective_id == HELLO_WORLD_ENTER_LAB
    )
    assert loaded_objective.progress == 0


def test_failed_game_load_keeps_live_progress(game):
    game.money = 99

    assert not game.load_game()
    assert game.money == 99
    assert game.current_dialogue == ["No save game was found."]
