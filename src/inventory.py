from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class ItemDefinition:
    id: str
    name: str
    type: str
    description: str
    unique: bool = True
    usable: bool = False
    use_message: str | None = None


ITEM_DEFINITIONS = {
    "student_id": ItemDefinition(
        id="student_id",
        name="Student ID",
        type="key_item",
        description="Required to enter Mapua.",
        use_message="You check your Student ID. Keep it with you.",
    ),
    "wallet": ItemDefinition(
        id="wallet",
        name="Wallet",
        type="key_item",
        description="Stores your allowance and commute money.",
    ),
    "notebook": ItemDefinition(
        id="notebook",
        name="Notebook",
        type="school_supply",
        description="Useful for reviewing lecture notes.",
    ),
    "laptop": ItemDefinition(
        id="laptop",
        name="Laptop",
        type="equipment",
        description="Needed for programming activities.",
    ),
    "calculator": ItemDefinition(
        id="calculator",
        name="Calculator",
        type="school_supply",
        description="Useful for engineering math.",
    ),
    "charger": ItemDefinition(
        id="charger",
        name="Charger",
        type="equipment",
        description="Keeps your devices ready for class.",
    ),
    "food_placeholder": ItemDefinition(
        id="food_placeholder",
        name="Food",
        type="consumable",
        description="A placeholder food item for future energy restoration.",
        unique=False,
        usable=True,
        use_message="You eat the food. Energy effects are not implemented yet.",
    ),
}


class Inventory:
    def __init__(self, slot_count=5, slot_size=64, padding=10, item_definitions=None):
        self.slot_count = slot_count
        self.slot_size = slot_size
        self.padding = padding
        self.item_definitions = item_definitions or ITEM_DEFINITIONS

        # Calculate bar dimensions
        self.width = (self.slot_size * self.slot_count) + (self.padding * (self.slot_count + 1))
        self.height = self.slot_size + (self.padding * 2)

        # Position at bottom center
        display_surface = pygame.display.get_surface()
        screen_width = display_surface.get_width() if display_surface else 800
        screen_height = display_surface.get_height() if display_surface else 600
        self.rect = pygame.Rect(
            (screen_width - self.width) // 2,
            screen_height - self.height - 20, # 20px margin from bottom
            self.width,
            self.height
        )

        self.slots = [None] * self.slot_count # Empty slots

    def add_item(self, item):
        item_id = self._item_id(item)
        definition = self.get_definition(item_id)
        if definition and definition.unique and self.has_item(item_id):
            return False

        for i in range(self.slot_count):
            if self.slots[i] is None:
                self.slots[i] = item
                self._apply_definition(item, definition)
                return True
        return False

    def remove_item(self, item_id_or_name):
        for index, item in enumerate(self.slots):
            if item and self._matches(item, item_id_or_name):
                self.slots[index] = None
                return item
        return None

    def has_item(self, item_id_or_name):
        return self.get_item(item_id_or_name) is not None

    def get_item(self, item_id_or_name):
        query = self._normalize(item_id_or_name)
        for item in self.slots:
            if item and self._matches(item, query):
                return item
        return None

    def get_items(self):
        return [item for item in self.slots if item is not None]

    def use_item(self, item_id_or_name):
        item = self.get_item(item_id_or_name)
        if item is None:
            return None

        definition = self.get_definition(self._item_id(item))
        if definition and definition.use_message:
            if definition.usable and definition.type == "consumable":
                self.remove_item(definition.id)
            return definition.use_message
        return f"You inspect the {self._item_name(item)}."

    def debug_summary(self):
        item_names = [self._item_name(item) for item in self.get_items()]
        return "Inventory: " + (", ".join(item_names) if item_names else "empty")

    def debug_print(self):
        summary = self.debug_summary()
        print(summary)
        return summary

    def get_slot_rect(self, index):
        if index < 0 or index >= self.slot_count:
            raise IndexError("Inventory slot index out of range")
        slot_x = self.rect.x + self.padding + (index * (self.slot_size + self.padding))
        slot_y = self.rect.y + self.padding
        return pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)

    def get_slot_rects(self):
        return [self.get_slot_rect(index) for index in range(self.slot_count)]

    def get_definition(self, item_id_or_name):
        query = self._normalize(item_id_or_name)
        for item_definition in self.item_definitions.values():
            if query in (self._normalize(item_definition.id), self._normalize(item_definition.name)):
                return item_definition
        return None

    def _apply_definition(self, item, definition):
        if definition is None:
            return
        item.item_id = definition.id
        item.name = definition.name
        item.item_type = definition.type
        item.description = definition.description
        item.unique = definition.unique
        item.usable = definition.usable

    def _matches(self, item, item_id_or_name):
        query = self._normalize(item_id_or_name)
        return query in (
            self._normalize(self._item_id(item)),
            self._normalize(self._item_name(item)),
        )

    def _item_id(self, item):
        return getattr(item, "item_id", None) or self._normalize(getattr(item, "name", ""))

    def _item_name(self, item):
        return getattr(item, "name", self._item_id(item))

    def _normalize(self, value):
        return str(value).strip().lower().replace(" ", "_")

    def draw(self, surface):
        # Draw background bar
        pygame.draw.rect(surface, (40, 40, 40), self.rect, border_radius=10)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2, border_radius=10)
        
        # Draw slots
        for i in range(self.slot_count):
            slot_rect = self.get_slot_rect(i)
            
            # Draw slot background
            pygame.draw.rect(surface, (60, 60, 60), slot_rect, border_radius=5)
            # Draw slot border
            pygame.draw.rect(surface, (100, 100, 100), slot_rect, 2, border_radius=5)
            
            # Draw item if slot is not empty
            if self.slots[i]:
                # Resize image to fit slot if needed
                item_image = self.slots[i].image
                if item_image.get_width() > self.slot_size - 10 or item_image.get_height() > self.slot_size - 10:
                    item_image = pygame.transform.scale(item_image, (self.slot_size - 10, self.slot_size - 10))
                
                item_rect = item_image.get_rect(center=slot_rect.center)
                surface.blit(item_image, item_rect)
