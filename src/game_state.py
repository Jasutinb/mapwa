from dataclasses import dataclass, field

from src.config import MAX_ENERGY, ROOM_MAIN
from src.quest_definitions import create_initial_quest_manager
from src.quests import QuestManager
from src.skill_xp import SkillXPManager


@dataclass
class GameState:
    current_room: str = ROOM_MAIN
    current_day: int = 1
    money: int = 0
    energy: int = MAX_ENERGY
    skill_xp_manager: SkillXPManager = field(default_factory=SkillXPManager)
    quest_manager: QuestManager = field(default_factory=create_initial_quest_manager)
    has_talked_to_mom: bool = False
    last_allowance_day: int = 0
    admin_office_checked_in: bool = False
    temporary_campus_pass_day: int | None = None
    current_dialogue: list[str] | None = None
    dialogue_index: int = 0
    picked_item_ids: set[str] = field(default_factory=set)
    inventory_item_ids: list[str] = field(default_factory=list)

    @property
    def experience(self) -> int:
        return self.skill_xp_manager.total_xp

    def start_dialogue(self, lines: list[str]) -> None:
        self.current_dialogue = list(lines)
        self.dialogue_index = 0

    def clear_dialogue(self) -> None:
        self.current_dialogue = None
        self.dialogue_index = 0

    def advance_dialogue(self) -> bool:
        if not self.current_dialogue:
            return True

        self.dialogue_index += 1
        return self.dialogue_index >= len(self.current_dialogue)

    def mark_item_picked(self, item_id: str) -> None:
        self.picked_item_ids.add(item_id)
        if item_id not in self.inventory_item_ids:
            self.inventory_item_ids.append(item_id)

    def remove_inventory_item(self, item_id: str) -> None:
        if item_id in self.inventory_item_ids:
            self.inventory_item_ids.remove(item_id)
