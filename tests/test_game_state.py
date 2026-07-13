from src.game_state import GameState


def test_mutable_defaults_are_isolated_between_game_states():
    first = GameState()
    second = GameState()

    first.skill_xp_manager.grant_xp("academics", 5)
    first.quest_manager.quests.clear()
    first.assignments.clear()
    first.exams.clear()
    first.mark_item_picked("student_id")

    assert second.skill_xp_manager.get_xp("academics") == 0
    assert second.quest_manager.quests
    assert second.assignments
    assert second.exams
    assert second.picked_item_ids == set()
    assert second.inventory_item_ids == []


def test_dialogue_helpers_track_progress_and_reset_state():
    state = GameState()

    state.start_dialogue(["First", "Second"])

    assert state.current_dialogue == ["First", "Second"]
    assert state.dialogue_index == 0
    assert not state.advance_dialogue()
    assert state.dialogue_index == 1
    assert state.advance_dialogue()

    state.clear_dialogue()

    assert state.current_dialogue is None
    assert state.dialogue_index == 0
    assert state.advance_dialogue()


def test_experience_aggregates_all_skill_xp():
    state = GameState()

    state.skill_xp_manager.grant_xp("academics", 7)
    state.skill_xp_manager.grant_xp("programming", 3)

    assert state.experience == 10


def test_item_bookkeeping_is_idempotent_and_removal_preserves_pickup_history():
    state = GameState()

    state.mark_item_picked("student_id")
    state.mark_item_picked("student_id")

    assert state.picked_item_ids == {"student_id"}
    assert state.inventory_item_ids == ["student_id"]

    state.remove_inventory_item("student_id")
    state.remove_inventory_item("student_id")

    assert state.picked_item_ids == {"student_id"}
    assert state.inventory_item_ids == []
