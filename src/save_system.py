import json
import sys
from pathlib import Path

from src.assignments import (
    ASSIGNMENT_STATUS_ACTIVE,
    ASSIGNMENT_STATUS_COMPLETED,
    ASSIGNMENT_STATUS_MISSED,
)
from src.config import (
    MAX_ENERGY,
    MAX_GRADE_STANDING,
    MAX_STRESS,
    MIN_GRADE_STANDING,
    MIN_STRESS,
)
from src.exams import EXAM_STATUS_PASSED, EXAM_STATUS_PENDING
from src.game_state import GameState
from src.quests import QUEST_ACTIVE, QUEST_DONE, QUEST_NOT_STARTED


SAVE_VERSION = 1
DEFAULT_SAVE_PATH = "mapwa-save.json"
DEFAULT_BROWSER_KEY = "mapwa.game_state"


class SaveError(Exception):
    """Base error for save data that cannot be read or written safely."""


class SaveNotFoundError(SaveError):
    """Raised when the selected persistence backend has no save."""


class IncompatibleSaveError(SaveError):
    """Raised when save data is from an unsupported format version."""


class DesktopSaveStorage:
    def __init__(self, path=DEFAULT_SAVE_PATH):
        self.path = Path(path)

    def read(self):
        if not self.path.exists():
            return None
        return self.path.read_text(encoding="utf-8")

    def write(self, content):
        self.path.write_text(content, encoding="utf-8")


class BrowserSaveStorage:
    def __init__(self, key=DEFAULT_BROWSER_KEY, window=None):
        self.key = key
        self.window = window

    def _local_storage(self):
        window = self.window
        if window is None:
            import platform

            window = getattr(platform, "window", None)
        if window is None or not hasattr(window, "localStorage"):
            raise SaveError("Browser storage is unavailable.")
        return window.localStorage

    def read(self):
        return self._local_storage().getItem(self.key)

    def write(self, content):
        self._local_storage().setItem(self.key, content)


def create_default_storage():
    if sys.platform == "emscripten":
        return BrowserSaveStorage()
    return DesktopSaveStorage()


class SaveSystem:
    def __init__(self, storage=None):
        self.storage = storage or create_default_storage()

    def save(self, state):
        content = json.dumps(self.serialize(state), sort_keys=True, separators=(",", ":"))
        try:
            self.storage.write(content)
        except SaveError:
            raise
        except Exception as exc:
            raise SaveError("The game could not write the save.") from exc

    def load(self):
        try:
            content = self.storage.read()
        except SaveError:
            raise
        except Exception as exc:
            raise SaveError("The game could not read the save.") from exc

        if content is None:
            raise SaveNotFoundError("No save game was found.")

        try:
            payload = json.loads(str(content))
        except (TypeError, ValueError) as exc:
            raise SaveError("The save game is corrupt.") from exc
        return self.deserialize(payload)

    @staticmethod
    def serialize(state):
        return {
            "version": SAVE_VERSION,
            "state": {
                "current_room": state.current_room,
                "current_day": state.current_day,
                "money": state.money,
                "energy": state.energy,
                "stress": state.stress,
                "grade_standing": state.grade_standing,
                "has_talked_to_mom": state.has_talked_to_mom,
                "has_talked_to_classmate": state.has_talked_to_classmate,
                "last_allowance_day": state.last_allowance_day,
                "last_debug_code_side_hustle_day": state.last_debug_code_side_hustle_day,
                "admin_office_checked_in": state.admin_office_checked_in,
                "temporary_campus_pass_day": state.temporary_campus_pass_day,
                "attended_class_day": state.attended_class_day,
                "attended_class_ids": sorted(state.attended_class_ids),
                "picked_item_ids": sorted(state.picked_item_ids),
                "inventory_item_ids": list(state.inventory_item_ids),
                "skill_xp": dict(state.skill_xp_manager.xp_by_skill),
                "quests": {
                    quest_id: {
                        "status": quest.status,
                        "objectives": [
                            {
                                "objective_id": objective.objective_id,
                                "progress": objective.progress,
                            }
                            for objective in quest.objectives
                        ],
                    }
                    for quest_id, quest in state.quest_manager.quests.items()
                },
                "assignments": {
                    assignment.assignment_id: {
                        "status": assignment.status,
                        "missed_stress_applied": assignment.missed_stress_applied,
                    }
                    for assignment in state.assignments
                },
                "exams": {
                    exam.exam_id: {
                        "status": exam.status,
                        "attempts": exam.attempts,
                    }
                    for exam in state.exams
                },
            },
        }

    @classmethod
    def deserialize(cls, payload):
        payload = cls._mapping(payload, "save payload")
        version = payload.get("version")
        if version != SAVE_VERSION:
            raise IncompatibleSaveError(
                f"Save version {version!r} is not supported by version {SAVE_VERSION}."
            )

        saved = cls._mapping(payload.get("state"), "saved state")
        state = GameState()
        state.current_room = cls._string(saved, "current_room")
        state.current_day = cls._integer(saved, "current_day", minimum=1)
        state.money = cls._integer(saved, "money", minimum=0)
        state.energy = cls._integer(saved, "energy", minimum=0, maximum=MAX_ENERGY)
        state.stress = cls._integer(
            saved, "stress", minimum=MIN_STRESS, maximum=MAX_STRESS
        )
        state.grade_standing = cls._integer(
            saved,
            "grade_standing",
            minimum=MIN_GRADE_STANDING,
            maximum=MAX_GRADE_STANDING,
        )
        state.has_talked_to_mom = cls._boolean(saved, "has_talked_to_mom")
        state.has_talked_to_classmate = cls._boolean(
            saved, "has_talked_to_classmate"
        )
        state.last_allowance_day = cls._integer(
            saved, "last_allowance_day", minimum=0
        )
        state.last_debug_code_side_hustle_day = cls._integer(
            saved, "last_debug_code_side_hustle_day", minimum=0
        )
        state.admin_office_checked_in = cls._boolean(
            saved, "admin_office_checked_in"
        )
        pass_day = saved.get("temporary_campus_pass_day")
        if pass_day is not None and (type(pass_day) is not int or pass_day < 1):
            raise SaveError("temporary_campus_pass_day must be a positive day or null.")
        state.temporary_campus_pass_day = pass_day
        state.attended_class_day = cls._integer(
            saved, "attended_class_day", minimum=1
        )
        state.attended_class_ids = set(cls._string_list(saved, "attended_class_ids"))
        state.picked_item_ids = set(cls._string_list(saved, "picked_item_ids"))
        state.inventory_item_ids = cls._string_list(saved, "inventory_item_ids")

        skill_xp = cls._mapping(saved.get("skill_xp"), "skill XP")
        for skill, amount in skill_xp.items():
            if not isinstance(skill, str) or not skill:
                raise SaveError("Skill names must be non-empty strings.")
            if type(amount) is not int or amount < 0:
                raise SaveError("Skill XP must be a non-negative integer.")
        state.skill_xp_manager.xp_by_skill.update(skill_xp)

        cls._restore_quests(state, saved.get("quests"))
        cls._restore_assignments(state, saved.get("assignments"))
        cls._restore_exams(state, saved.get("exams"))
        return state

    @classmethod
    def _restore_quests(cls, state, saved_quests):
        saved_quests = cls._mapping(saved_quests, "quests")
        valid_statuses = {QUEST_NOT_STARTED, QUEST_ACTIVE, QUEST_DONE}
        for quest_id, quest_data in saved_quests.items():
            if quest_id not in state.quest_manager.quests:
                continue
            quest_data = cls._mapping(quest_data, f"quest {quest_id}")
            status = quest_data.get("status")
            if status not in valid_statuses:
                raise SaveError(f"Quest {quest_id} has an invalid status.")
            objectives = quest_data.get("objectives")
            if not isinstance(objectives, list):
                raise SaveError(f"Quest {quest_id} objectives must be a list.")

            quest = state.quest_manager.quests[quest_id]
            saved_by_id = {
                item.get("objective_id"): item
                for item in objectives
                if isinstance(item, dict) and item.get("objective_id") is not None
            }
            for index, objective in enumerate(quest.objectives):
                objective_data = saved_by_id.get(objective.objective_id)
                if objective_data is None and index < len(objectives):
                    objective_data = objectives[index]
                objective_data = cls._mapping(
                    objective_data, f"quest {quest_id} objective {index}"
                )
                progress = objective_data.get("progress")
                if type(progress) is not int or not 0 <= progress <= objective.target:
                    raise SaveError(f"Quest {quest_id} has invalid objective progress.")
                objective.progress = progress
            quest.status = status

    @classmethod
    def _restore_assignments(cls, state, saved_assignments):
        saved_assignments = cls._mapping(saved_assignments, "assignments")
        valid_statuses = {
            ASSIGNMENT_STATUS_ACTIVE,
            ASSIGNMENT_STATUS_COMPLETED,
            ASSIGNMENT_STATUS_MISSED,
        }
        assignments = {item.assignment_id: item for item in state.assignments}
        for assignment_id, assignment_data in saved_assignments.items():
            if assignment_id not in assignments:
                continue
            assignment_data = cls._mapping(
                assignment_data, f"assignment {assignment_id}"
            )
            status = assignment_data.get("status")
            if status not in valid_statuses:
                raise SaveError(f"Assignment {assignment_id} has an invalid status.")
            missed_applied = assignment_data.get("missed_stress_applied")
            if type(missed_applied) is not bool:
                raise SaveError(
                    f"Assignment {assignment_id} has an invalid penalty flag."
                )
            assignments[assignment_id].status = status
            assignments[assignment_id].missed_stress_applied = missed_applied

    @classmethod
    def _restore_exams(cls, state, saved_exams):
        saved_exams = cls._mapping(saved_exams, "exams")
        exams = {item.exam_id: item for item in state.exams}
        for exam_id, exam_data in saved_exams.items():
            if exam_id not in exams:
                continue
            exam_data = cls._mapping(exam_data, f"exam {exam_id}")
            status = exam_data.get("status")
            if status not in {EXAM_STATUS_PENDING, EXAM_STATUS_PASSED}:
                raise SaveError(f"Exam {exam_id} has an invalid status.")
            attempts = exam_data.get("attempts")
            if type(attempts) is not int or attempts < 0:
                raise SaveError(f"Exam {exam_id} has invalid attempts.")
            exams[exam_id].status = status
            exams[exam_id].attempts = attempts

    @staticmethod
    def _mapping(value, label):
        if not isinstance(value, dict):
            raise SaveError(f"{label} must be an object.")
        return value

    @staticmethod
    def _string(mapping, key):
        value = mapping.get(key)
        if not isinstance(value, str) or not value:
            raise SaveError(f"{key} must be a non-empty string.")
        return value

    @staticmethod
    def _boolean(mapping, key):
        value = mapping.get(key)
        if type(value) is not bool:
            raise SaveError(f"{key} must be true or false.")
        return value

    @staticmethod
    def _integer(mapping, key, minimum=None, maximum=None):
        value = mapping.get(key)
        if type(value) is not int:
            raise SaveError(f"{key} must be an integer.")
        if minimum is not None and value < minimum:
            raise SaveError(f"{key} is below its minimum value.")
        if maximum is not None and value > maximum:
            raise SaveError(f"{key} is above its maximum value.")
        return value

    @staticmethod
    def _string_list(mapping, key):
        value = mapping.get(key)
        if not isinstance(value, list) or any(
            not isinstance(item, str) or not item for item in value
        ):
            raise SaveError(f"{key} must be a list of non-empty strings.")
        return list(dict.fromkeys(value))
