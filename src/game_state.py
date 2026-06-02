from dataclasses import dataclass, field

from src.config import ROOM_MAIN


@dataclass
class GameState:
    current_room: str = ROOM_MAIN
    money: int = 0
    experience: int = 0
    has_talked_to_mom: bool = False
    current_dialogue: list[str] | None = None
    dialogue_index: int = 0
    picked_item_ids: set[str] = field(default_factory=set)
    inventory_item_ids: list[str] = field(default_factory=list)

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
