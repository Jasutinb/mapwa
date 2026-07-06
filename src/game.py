import pygame
import sys
import asyncio
import os

from src.player import Player
from src.npc import NPC
from src.inventory import Inventory
from src.level import Tile, Chair, ClassMarker, Decoration, Door, Bus, Item, PassGate, RoomNode
from src.mobile_controls import MobileControls
from src.state import StateMachine
from src.states import PlayState, DialogueState, MenuState, SleepConfirmState
from src.game_state import GameState
from src.quest_definitions import (
    FIRST_DAY_ENTER_CAMPUS,
    FIRST_DAY_PICK_UP_ID,
    FIRST_DAY_RIDE_BUS,
    FIRST_DAY_STUDY,
    FIRST_DAY_TALK_TO_MOM,
    HELLO_WORLD_ENTER_LAB,
    HELLO_WORLD_PRACTICE_PROGRAMMING,
    HELLO_WORLD_QUEST_ID,
    FIRST_DAY_QUEST_ID,
    is_first_day_bus_destination,
    is_first_day_item,
)
from src.quests import QuestReward
from src.schedule import classes_for_day, schedule_summary_for_day, weekday_for_day
from src.transport import TRANSPORT_BUS, get_transport_mode
from src.config import (
    ADMIN_OFFICE_CHECKED_IN_DIALOGUE,
    ADMIN_OFFICE_CHECK_IN_DIALOGUE,
    ADMIN_OFFICE_CHECK_IN_XP,
    ADMIN_OFFICE_NO_ID_DIALOGUE,
    ADMIN_OFFICE_TEMP_PASS_ACTIVE_DIALOGUE,
    ALLOWANCE_AMOUNT,
    CAFETERIA_FULL_ENERGY_DIALOGUE,
    CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE,
    CAFETERIA_VENDOR_DIALOGUE,
    CLASS_ALREADY_ATTENDED_DIALOGUE,
    CLASS_ATTENDED_DIALOGUE,
    CLASS_ATTENDANCE_XP,
    CLASS_NO_CLASS_HERE_DIALOGUE,
    CLASS_NO_CLASSES_TODAY_DIALOGUE,
    DAILY_ALLOWANCE_MOM_DIALOGUE,
    ELECTRONICS_LAB_XP,
    FIRST_MOM_DIALOGUE,
    FPS,
    ELECTRONICS_PRACTICE_ENERGY_COST,
    ITEM_ID,
    INSUFFICIENT_ENERGY_DIALOGUE,
    LIBRARY_STUDY_ENERGY_COST,
    LOW_ENERGY_STRESS_DIALOGUE,
    LOW_ENERGY_STRESS_INCREASE,
    MAX_ENERGY,
    MAX_STRESS,
    MEAL_ENERGY,
    MEAL_PRICE,
    MIN_STRESS,
    REPEAT_MOM_DIALOGUE,
    ROOM_ADMIN_OFFICE,
    ROOM_BEDROOM,
    ROOM_CAFETERIA,
    ROOM_ELECTRONICS_LAB,
    ROOM_INTRAMUROS,
    ROOM_LIBRARY,
    ROOM_MAIN,
    ROOM_OUTSIDE,
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL,
    ROOM_SCHOOL_ENTRANCE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCHOOL_GATE_NO_ID_DIALOGUE,
    SCHOOL_GUARD_HAS_ID_DIALOGUE,
    SCHOOL_GUARD_NO_ID_DIALOGUE,
    SCHOOL_GUARD_NO_ID_REDIRECT_DIALOGUE,
    SCHOOL_GUARD_TEMP_PASS_DIALOGUE,
    SCHOOL_STUDY_ENERGY_COST,
    SLEEP_STRESS_RECOVERY,
    SKILL_ACADEMICS,
    SKILL_ELECTRONICS,
    SKILL_PROGRAMMING,
    STATE_DIALOGUE,
    STATE_MENU,
    STATE_PLAY,
    STATE_SLEEP_CONFIRM,
    LIBRARY_STUDY_XP,
    PROGRAMMING_PRACTICE_ENERGY_COST,
    PROGRAMMING_LAB_XP,
    STUDY_DURATION_FRAMES,
    STUDY_XP,
    TILE_SIZE,
)

DEV_LOADOUT_ENV = "MAPWA_DEV_LOADOUT"
DEV_LOADOUT_ITEMS = [
    (ITEM_ID, "Student ID"),
]

class Game:
    def __init__(self):
        # pygame.init() moved to main.py for better WASM compatibility
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Student RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState()

        # Sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.floor_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.bed_sprites = pygame.sprite.Group()
        self.gate_sprites = pygame.sprite.Group()
        self.guard_sprites = pygame.sprite.Group()
        self.chair_sprites = pygame.sprite.Group()
        self.attendant_sprites = pygame.sprite.Group()
        self.class_marker_sprites = pygame.sprite.Group()

        self.location_display_text = ""
        self.location_display_timer = 0
        self.location_display_duration = 120 # 2 seconds at 60 FPS
        self.schedule_hud_rect = pygame.Rect(0, 0, 0, 0)
        self.energy_hud_rect = pygame.Rect(0, 0, 0, 0)
        self.stress_hud_rect = pygame.Rect(0, 0, 0, 0)
        self.mobile_controls = MobileControls((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Level setup
        self.setup_rooms()
        self.current_room = ROOM_MAIN
        self.create_map()

        # Player setup
        self.player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), [self.visible_sprites], self.obstacle_sprites)

        # NPC setup
        self.mom = NPC((SCREEN_WIDTH // 2, 100), [self.visible_sprites], 'assets/images/mom.png', name="Mom")
        self.mom.dialogue = list(FIRST_MOM_DIALOGUE)

        try:
            self.font = pygame.font.SysFont('Arial', 24)
        except pygame.error:
            self.font = pygame.font.Font(None, 24)

        # Inventory setup
        self.inventory = Inventory()
        self.mobile_controls.set_inventory_slot_rects(self.inventory.get_slot_rects())
        if os.environ.get(DEV_LOADOUT_ENV) == "1":
            self.apply_dev_loadout()

        # UI Assets
        self.money_icon = self.create_money_icon()

        # State Machine setup
        self.state_machine = StateMachine()
        self.previous_state_before_menu = STATE_PLAY
        self.state_machine.add_state(STATE_PLAY, PlayState(self))
        self.state_machine.add_state(STATE_DIALOGUE, DialogueState(self))
        self.state_machine.add_state(STATE_MENU, MenuState(self))
        self.state_machine.add_state(STATE_SLEEP_CONFIRM, SleepConfirmState(self))
        self.state_machine.change_state(STATE_PLAY)

    @property
    def current_room(self):
        return self.state.current_room

    @current_room.setter
    def current_room(self, value):
        self.state.current_room = value

    @property
    def current_dialogue(self):
        return self.state.current_dialogue

    @current_dialogue.setter
    def current_dialogue(self, value):
        self.state.current_dialogue = value

    @property
    def dialogue_index(self):
        return self.state.dialogue_index

    @dialogue_index.setter
    def dialogue_index(self, value):
        self.state.dialogue_index = value

    @property
    def money(self):
        return self.state.money

    @money.setter
    def money(self, value):
        self.state.money = value

    @property
    def energy(self):
        return self.state.energy

    @energy.setter
    def energy(self, value):
        self.state.energy = max(0, min(MAX_ENERGY, value))

    @property
    def stress(self):
        return self.state.stress

    @stress.setter
    def stress(self, value):
        self.state.stress = max(MIN_STRESS, min(MAX_STRESS, value))

    @property
    def experience(self):
        return self.state.experience

    @property
    def skill_xp_manager(self):
        return self.state.skill_xp_manager

    @property
    def quest_manager(self):
        return self.state.quest_manager

    @property
    def current_day(self):
        return self.state.current_day

    @current_day.setter
    def current_day(self, value):
        self.state.current_day = value

    @property
    def current_weekday(self):
        return weekday_for_day(self.current_day)

    def get_today_classes(self):
        return classes_for_day(self.current_day)

    def get_schedule_summary(self):
        return schedule_summary_for_day(self.current_day)

    def get_schedule_hud_lines(self):
        return [
            f"Day {self.current_day} - {self.current_weekday}",
            self.get_schedule_summary(),
        ]

    def get_attended_class_ids(self):
        if self.state.attended_class_day != self.current_day:
            self.state.attended_class_day = self.current_day
            self.state.attended_class_ids.clear()
        return self.state.attended_class_ids

    def get_today_classes_for_room(self, room_name=None):
        target_room = room_name or self.current_room
        return [entry for entry in self.get_today_classes() if entry.room_key == target_room]

    def get_class_marker_near_player(self):
        return next(
            (
                marker
                for marker in self.class_marker_sprites
                if self.check_proximity(self.player, marker, 64)
            ),
            None,
        )

    def attend_class(self):
        classes_today = self.get_today_classes()
        if not classes_today:
            self.show_dialogue([CLASS_NO_CLASSES_TODAY_DIALOGUE])
            return False

        room_classes = self.get_today_classes_for_room()
        if not room_classes:
            self.show_dialogue([CLASS_NO_CLASS_HERE_DIALOGUE])
            return False

        attended_ids = self.get_attended_class_ids()
        class_entry = next(
            (entry for entry in room_classes if entry.identifier not in attended_ids),
            room_classes[0],
        )
        if class_entry.identifier in attended_ids:
            self.show_dialogue(
                [
                    CLASS_ALREADY_ATTENDED_DIALOGUE.format(
                        course_name=class_entry.course_name
                    )
                ]
            )
            return False

        attended_ids.add(class_entry.identifier)
        skill_xp = self.grant_skill_xp(class_entry.skill, CLASS_ATTENDANCE_XP)
        self.show_dialogue(
            [
                CLASS_ATTENDED_DIALOGUE.format(
                    course_name=class_entry.course_name,
                    xp=CLASS_ATTENDANCE_XP,
                    skill=class_entry.skill,
                    total=skill_xp,
                )
            ]
        )
        return True


    @property
    def last_allowance_day(self):
        return self.state.last_allowance_day

    @last_allowance_day.setter
    def last_allowance_day(self, value):
        self.state.last_allowance_day = value

    @property
    def has_talked_to_mom(self):
        return self.state.has_talked_to_mom

    @has_talked_to_mom.setter
    def has_talked_to_mom(self, value):
        self.state.has_talked_to_mom = value

    def setup_rooms(self):
        # Create room nodes
        self.rooms = {
            ROOM_MAIN: RoomNode(ROOM_MAIN, 'Living Room'),
            ROOM_BEDROOM: RoomNode(ROOM_BEDROOM, 'Bedroom'),
            ROOM_OUTSIDE: RoomNode(ROOM_OUTSIDE, 'Outside'),
            ROOM_INTRAMUROS: RoomNode(ROOM_INTRAMUROS, 'Intramuros'),
            ROOM_SCHOOL_ENTRANCE: RoomNode(ROOM_SCHOOL_ENTRANCE, 'School Entrance'),
            ROOM_ADMIN_OFFICE: RoomNode(ROOM_ADMIN_OFFICE, 'Admin Office'),
            ROOM_SCHOOL: RoomNode(ROOM_SCHOOL, 'School'),
            ROOM_PROGRAMMING_LAB: RoomNode(ROOM_PROGRAMMING_LAB, 'Programming Lab'),
            ROOM_ELECTRONICS_LAB: RoomNode(ROOM_ELECTRONICS_LAB, 'Electronics Lab'),
            ROOM_LIBRARY: RoomNode(ROOM_LIBRARY, 'Library'),
            ROOM_CAFETERIA: RoomNode(ROOM_CAFETERIA, 'Cafeteria')
        }

        # Link rooms
        # Main is center-ish
        # Bedroom is to the left of Main
        self.rooms[ROOM_MAIN].left = self.rooms[ROOM_BEDROOM]
        self.rooms[ROOM_BEDROOM].right = self.rooms[ROOM_MAIN]

        # Outside is to the right of Main
        self.rooms[ROOM_MAIN].right = self.rooms[ROOM_OUTSIDE]
        self.rooms[ROOM_OUTSIDE].left = self.rooms[ROOM_MAIN]

        # Intramuros is linked via Bus from Outside, but geographically let's say it's to the right of Outside
        self.rooms[ROOM_OUTSIDE].right = self.rooms[ROOM_INTRAMUROS]
        self.rooms[ROOM_INTRAMUROS].left = self.rooms[ROOM_OUTSIDE]

        # School Entrance sits between Intramuros and School
        self.rooms[ROOM_INTRAMUROS].right = self.rooms[ROOM_SCHOOL_ENTRANCE]
        self.rooms[ROOM_SCHOOL_ENTRANCE].left = self.rooms[ROOM_INTRAMUROS]
        self.rooms[ROOM_SCHOOL_ENTRANCE].right = self.rooms[ROOM_SCHOOL]
        self.rooms[ROOM_SCHOOL_ENTRANCE].up = self.rooms[ROOM_ADMIN_OFFICE]
        self.rooms[ROOM_ADMIN_OFFICE].down = self.rooms[ROOM_SCHOOL_ENTRANCE]
        self.rooms[ROOM_SCHOOL].left = self.rooms[ROOM_SCHOOL_ENTRANCE]
        self.rooms[ROOM_SCHOOL].up = self.rooms[ROOM_PROGRAMMING_LAB]
        self.rooms[ROOM_SCHOOL].right = self.rooms[ROOM_ELECTRONICS_LAB]
        self.rooms[ROOM_SCHOOL].down = self.rooms[ROOM_LIBRARY]
        self.rooms[ROOM_PROGRAMMING_LAB].down = self.rooms[ROOM_SCHOOL]
        self.rooms[ROOM_ELECTRONICS_LAB].left = self.rooms[ROOM_SCHOOL]
        self.rooms[ROOM_LIBRARY].up = self.rooms[ROOM_SCHOOL]
        self.rooms[ROOM_CAFETERIA].up = self.rooms[ROOM_SCHOOL]

    def create_money_icon(self):
        icon = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(icon, (255, 215, 0), (12, 12), 11) # Gold circle
        pygame.draw.circle(icon, (184, 134, 11), (12, 12), 11, 2) # Darker border
        # Draw a small 'P' for Peso
        try:
            font = pygame.font.SysFont('Arial', 20, bold=True)
        except pygame.error:
            font = pygame.font.Font(None, 20)
        p_surf = font.render("P", True, (139, 69, 19))
        p_rect = p_surf.get_rect(center=(12, 12))
        icon.blit(p_surf, p_rect)
        return icon

    def show_dialogue(self, lines):
        self.state.start_dialogue(lines)
        self.state_machine.change_state(STATE_DIALOGUE)

    def open_menu(self):
        if self.state_machine.current_state_name == STATE_MENU:
            return
        self.previous_state_before_menu = self.state_machine.current_state_name or STATE_PLAY
        self.state_machine.change_state(STATE_MENU)

    def close_menu(self):
        target_state = self.previous_state_before_menu or STATE_PLAY
        self.state_machine.change_state(target_state)

    def open_sleep_confirmation(self):
        self.state_machine.change_state(STATE_SLEEP_CONFIRM)

    def cancel_sleep_confirmation(self):
        self.state_machine.change_state(STATE_PLAY)

    def sleep_until_next_day(self):
        self.current_day += 1
        self.energy = MAX_ENERGY
        self.reduce_stress(SLEEP_STRESS_RECOVERY)
        self.state.attended_class_day = self.current_day
        self.state.attended_class_ids.clear()
        self.state.temporary_campus_pass_day = None
        self.show_dialogue([f"You slept through the night. Day {self.current_day} begins."])

    def finish_dialogue(self):
        self.state.clear_dialogue()
        if not self.can_receive_allowance_today():
            self.mom.dialogue = list(REPEAT_MOM_DIALOGUE)
        self.state_machine.change_state(STATE_PLAY)

    def can_receive_allowance_today(self):
        return self.last_allowance_day < self.current_day

    def give_daily_allowance(self):
        if not self.can_receive_allowance_today():
            return False

        self.money += ALLOWANCE_AMOUNT
        self.last_allowance_day = self.current_day
        self.has_talked_to_mom = True
        self.advance_first_day_objective(FIRST_DAY_TALK_TO_MOM)
        return True

    def get_mom_dialogue(self):
        if not self.can_receive_allowance_today():
            return list(REPEAT_MOM_DIALOGUE)
        if self.has_talked_to_mom:
            return list(DAILY_ALLOWANCE_MOM_DIALOGUE)
        return list(FIRST_MOM_DIALOGUE)

    def advance_dialogue(self):
        if not self.current_dialogue:
            return

        finished = self.state.advance_dialogue()
        if finished:
            self.finish_dialogue()
            return

        if self.dialogue_index == len(self.current_dialogue) - 1:
            self.give_daily_allowance()

    def talk_to_mom(self):
        self.mom.dialogue = self.get_mom_dialogue()
        self.show_dialogue(self.mom.interact())

    def talk_to_guard(self):
        guard = next((sprite for sprite in self.guard_sprites if self.check_proximity(self.player, sprite, 64)), None)
        if guard is None:
            return False
        if not self.has_inventory_item(ITEM_ID) and not self.has_temporary_campus_pass():
            self.travel_to_room(ROOM_ADMIN_OFFICE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 96))
            self.show_dialogue(list(SCHOOL_GUARD_NO_ID_REDIRECT_DIALOGUE))
            return True
        guard.dialogue = self.get_school_guard_dialogue()
        self.show_dialogue(guard.interact())
        return True

    def get_school_guard_dialogue(self):
        if self.has_inventory_item(ITEM_ID):
            return list(SCHOOL_GUARD_HAS_ID_DIALOGUE)
        if self.has_temporary_campus_pass():
            return list(SCHOOL_GUARD_TEMP_PASS_DIALOGUE)
        return list(SCHOOL_GUARD_NO_ID_DIALOGUE)

    def talk_to_attendant(self):
        attendant = next((sprite for sprite in self.attendant_sprites if self.check_proximity(self.player, sprite, 64)), None)
        if attendant is None:
            return False
        attendant.dialogue = self.get_admin_attendant_dialogue()
        self.complete_admin_office_check_in()
        self.show_dialogue(attendant.interact())
        return True

    def get_admin_attendant_dialogue(self):
        if not self.has_inventory_item(ITEM_ID):
            if self.has_temporary_campus_pass():
                return list(ADMIN_OFFICE_TEMP_PASS_ACTIVE_DIALOGUE)
            return list(ADMIN_OFFICE_NO_ID_DIALOGUE)
        if self.state.admin_office_checked_in:
            return list(ADMIN_OFFICE_CHECKED_IN_DIALOGUE)
        return list(ADMIN_OFFICE_CHECK_IN_DIALOGUE)

    def complete_admin_office_check_in(self):
        if not self.has_inventory_item(ITEM_ID):
            if self.has_temporary_campus_pass():
                return False
            self.grant_temporary_campus_pass()
            return True

        if self.state.admin_office_checked_in:
            return False
        self.state.admin_office_checked_in = True
        self.grant_skill_xp(SKILL_ACADEMICS, ADMIN_OFFICE_CHECK_IN_XP)
        return True

    def grant_temporary_campus_pass(self):
        self.state.temporary_campus_pass_day = self.current_day

    def has_temporary_campus_pass(self):
        return self.state.temporary_campus_pass_day == self.current_day

    def has_school_gate_access(self, required_item_id):
        return self.has_inventory_item(required_item_id) or self.has_temporary_campus_pass()

    def travel_to_room(self, room_name, spawn_pos=None, use_topleft=False):
        self.current_room = room_name
        self.create_map()
        if spawn_pos and use_topleft:
            self.player.rect.topleft = spawn_pos
        else:
            self.player.rect.center = spawn_pos or (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.visible_sprites.add(self.player)
        if room_name == ROOM_PROGRAMMING_LAB:
            self.advance_hello_world_objective(HELLO_WORLD_ENTER_LAB)

    def pay_transport_fare(self, transport_key):
        transport = get_transport_mode(transport_key)
        if self.money < transport.fare:
            self.show_dialogue([transport.insufficient_funds_dialogue()])
            return False

        self.money -= transport.fare
        return True

    def ride_bus(self):
        current_node = self.rooms.get(self.current_room)
        if not self.pay_transport_fare(TRANSPORT_BUS):
            return False

        if self.current_room == ROOM_OUTSIDE:
            destination = current_node.right.name if current_node and current_node.right else ROOM_INTRAMUROS
        elif self.current_room == ROOM_INTRAMUROS:
            destination = current_node.left.name if current_node and current_node.left else ROOM_OUTSIDE
        else:
            destination = current_node.left.name if current_node and current_node.left else ROOM_INTRAMUROS

        self.travel_to_room(destination)
        if is_first_day_bus_destination(destination):
            self.advance_first_day_objective(FIRST_DAY_RIDE_BUS)
        return True

    def study_at_school(self):
        if not self.spend_energy(SCHOOL_STUDY_ENERGY_COST):
            return False
        self.grant_skill_xp(SKILL_ACADEMICS, STUDY_XP)
        self.player.start_study(STUDY_DURATION_FRAMES)
        self.advance_first_day_objective(FIRST_DAY_STUDY)
        return True

    def practice_programming(self):
        if not self.spend_energy(PROGRAMMING_PRACTICE_ENERGY_COST):
            return False
        skill_xp = self.grant_skill_xp(SKILL_PROGRAMMING, PROGRAMMING_LAB_XP)
        self.advance_hello_world_objective(HELLO_WORLD_PRACTICE_PROGRAMMING)
        skill_xp = self.get_skill_xp(SKILL_PROGRAMMING)
        self.show_dialogue([f"You practiced coding and gained {PROGRAMMING_LAB_XP} programming XP! Total: {skill_xp}."])
        return True

    def practice_electronics(self):
        if not self.spend_energy(ELECTRONICS_PRACTICE_ENERGY_COST):
            return False
        skill_xp = self.grant_skill_xp(SKILL_ELECTRONICS, ELECTRONICS_LAB_XP)
        self.show_dialogue([f"You practiced circuits and gained {ELECTRONICS_LAB_XP} electronics XP! Total: {skill_xp}."])
        return True

    def study_at_library(self, skill, label):
        if not self.spend_energy(LIBRARY_STUDY_ENERGY_COST):
            return False
        skill_xp = self.grant_skill_xp(skill, LIBRARY_STUDY_XP)
        self.show_dialogue([f"You studied {label} and gained {LIBRARY_STUDY_XP} {label} XP! Total: {skill_xp}."])
        return True

    def spend_energy(self, amount):
        if self.energy < amount:
            stress_increased = self.increase_stress(LOW_ENERGY_STRESS_INCREASE)
            dialogue = list(INSUFFICIENT_ENERGY_DIALOGUE)
            if stress_increased:
                dialogue.append(LOW_ENERGY_STRESS_DIALOGUE.format(amount=stress_increased))
            self.show_dialogue(dialogue)
            return False
        self.energy -= amount
        return True

    def restore_energy(self, amount):
        before = self.energy
        self.energy = self.energy + amount
        return self.energy - before

    def increase_stress(self, amount):
        before = self.stress
        self.stress = self.stress + amount
        return self.stress - before

    def reduce_stress(self, amount):
        before = self.stress
        self.stress = self.stress - amount
        return before - self.stress

    def buy_cafeteria_meal(self):
        if self.energy >= MAX_ENERGY:
            self.show_dialogue(list(CAFETERIA_FULL_ENERGY_DIALOGUE))
            return False
        if self.money < MEAL_PRICE:
            self.show_dialogue(list(CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE))
            return False

        self.money -= MEAL_PRICE
        restored = self.restore_energy(MEAL_ENERGY)
        self.show_dialogue(
            [
                f"You bought a meal for {MEAL_PRICE} and restored {restored} energy. "
                f"Energy: {self.energy}/{MAX_ENERGY}."
            ]
        )
        return True

    def grant_skill_xp(self, skill, amount):
        return self.skill_xp_manager.grant_xp(skill, amount)

    def get_skill_xp(self, skill):
        return self.skill_xp_manager.get_xp(skill)

    def add_quest(self, quest):
        return self.quest_manager.add_quest(quest)

    def start_quest(self, quest_id):
        return self.quest_manager.start_quest(quest_id)

    def advance_quest(self, quest_id, amount=1, objective_index=None):
        reward = self.quest_manager.advance_quest(quest_id, amount, objective_index)
        self.apply_quest_reward(reward)
        return reward

    def advance_quest_objective(self, quest_id, objective_id, amount=1):
        reward = self.quest_manager.advance_objective(quest_id, objective_id, amount)
        self.apply_quest_reward(reward)
        return reward

    def advance_first_day_objective(self, objective_id):
        return self.advance_quest_objective(FIRST_DAY_QUEST_ID, objective_id)

    def advance_hello_world_objective(self, objective_id):
        return self.advance_quest_objective(HELLO_WORLD_QUEST_ID, objective_id)

    def apply_quest_reward(self, reward):
        if reward is None:
            return
        if not isinstance(reward, QuestReward):
            raise TypeError("Quest reward must be a QuestReward")
        self.money += reward.money
        for skill, amount in reward.skill_xp.items():
            self.grant_skill_xp(skill, amount)

    def apply_dev_loadout(self):
        self.money = 999
        for item_id, item_name in DEV_LOADOUT_ITEMS:
            if not self.inventory.has_item(item_id):
                self.inventory.add_item(Item((0, 0), [], item_name, item_id=item_id))
            self.state.mark_item_picked(item_id)

    def pick_up_item(self, item):
        if not self.inventory.add_item(item):
            return False

        self.state.mark_item_picked(item.item_id)
        if is_first_day_item(item.item_id):
            self.advance_first_day_objective(FIRST_DAY_PICK_UP_ID)
        item.kill()
        self.show_dialogue([f"You picked up a {item.name}!"])
        return True

    def has_inventory_item(self, item_id_or_name):
        return (
            self.inventory.has_item(item_id_or_name)
            or item_id_or_name in self.state.inventory_item_ids
        )

    def remove_inventory_item(self, item_id_or_name):
        item = self.inventory.remove_item(item_id_or_name)
        if item:
            self.state.remove_inventory_item(item.item_id)
        return item

    def use_inventory_item(self, item_id_or_name):
        message = self.inventory.use_item(item_id_or_name)
        if message is None:
            self.show_dialogue(["You do not have that item."])
            return False
        self.show_dialogue([message])
        return True

    def use_inventory_slot(self, slot_index):
        if slot_index < 0 or slot_index >= self.inventory.slot_count:
            return False
        item = self.inventory.slots[slot_index]
        if item is None:
            self.show_dialogue(["That inventory slot is empty."])
            return False
        return self.use_inventory_item(item.item_id)

    def try_enter_school_gate(self):
        gate = next((sprite for sprite in self.gate_sprites if self.check_proximity(self.player, sprite, 80)), None)
        if gate is None:
            return False

        if not self.has_school_gate_access(gate.required_item_id):
            self.show_dialogue(list(SCHOOL_GATE_NO_ID_DIALOGUE))
            return True

        if gate.target_room == self.current_room:
            spawn_pos = gate.right_spawn_pos if self.player.rect.centerx < gate.rect.centerx else gate.left_spawn_pos
            self.travel_to_room(gate.target_room, spawn_pos, use_topleft=True)
        else:
            self.travel_to_room(gate.target_room, gate.spawn_pos, use_topleft=True)
        self.advance_first_day_objective(FIRST_DAY_ENTER_CAMPUS)
        return True

    def create_guard_npc(self, pos, dialogue):
        guard = NPC(pos, [self.visible_sprites, self.obstacle_sprites, self.guard_sprites], 'assets/images/guard.png', name="Guard", can_wander=False)
        guard.dialogue = dialogue
        guard.sprite_asset = 'assets/images/guard.png'
        guard.sprite_base_assets = ('assets/images/player.png', 'assets/images/mom.png')
        return guard

    def create_attendant_npc(self, pos):
        attendant = NPC(pos, [self.visible_sprites, self.obstacle_sprites, self.attendant_sprites], 'assets/images/mom.png', name="Attendant", can_wander=False)
        attendant.dialogue = list(ADMIN_OFFICE_NO_ID_DIALOGUE)
        attendant.sprite_asset = 'assets/images/mom.png'
        attendant.sprite_base_assets = ('assets/images/player.png', 'assets/images/mom.png')
        return attendant

    def create_map(self):
        # Clear existing sprites
        for sprite in self.visible_sprites:
            sprite.kill()
        for sprite in self.obstacle_sprites:
            sprite.kill()
        for sprite in self.floor_sprites:
            sprite.kill()
        for sprite in self.door_sprites:
            sprite.kill()
        for sprite in self.item_sprites:
            sprite.kill()
        for sprite in self.bed_sprites:
            sprite.kill()
        for sprite in self.gate_sprites:
            sprite.kill()
        for sprite in self.guard_sprites:
            sprite.kill()
        for sprite in self.chair_sprites:
            sprite.kill()
        for sprite in self.attendant_sprites:
            sprite.kill()
        for sprite in self.class_marker_sprites:
            sprite.kill()

        # Set location display
        current_node = self.rooms.get(self.current_room)
        if current_node:
            self.location_display_text = current_node.display_name
        
        self.location_display_timer = self.location_display_duration

        if self.current_room == ROOM_MAIN:
            self.create_main_room()
        elif self.current_room == ROOM_BEDROOM:
            self.create_bedroom()
        elif self.current_room == ROOM_OUTSIDE:
            self.create_outside()
        elif self.current_room == ROOM_INTRAMUROS:
            self.create_intramuros()
        elif self.current_room == ROOM_SCHOOL_ENTRANCE:
            self.create_school_entrance()
        elif self.current_room == ROOM_ADMIN_OFFICE:
            self.create_admin_office()
        elif self.current_room == ROOM_SCHOOL:
            self.create_school()
        elif self.current_room == ROOM_PROGRAMMING_LAB:
            self.create_programming_lab()
        elif self.current_room == ROOM_ELECTRONICS_LAB:
            self.create_electronics_lab()
        elif self.current_room == ROOM_LIBRARY:
            self.create_library()
        elif self.current_room == ROOM_CAFETERIA:
            self.create_cafeteria()

    def create_main_room(self):
        try:
            floor_surf = pygame.image.load('assets/images/floor.png').convert()
            wall_surf = pygame.image.load('assets/images/wall.png').convert()
        except (pygame.error, FileNotFoundError):
            floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            floor_surf.fill((100, 50, 0))
            wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            wall_surf.fill((200, 200, 200))

        # Fill screen with floor tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)
        
        # Add walls at the top
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((col, TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        # Add a table
        Decoration((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        
        # Add doors
        # To Bedroom (left)
        Door((0, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_MAIN].left.name, (SCREEN_WIDTH - 64, SCREEN_HEIGHT // 2))
        # To Outside (right)
        Door((SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_MAIN].right.name, (64, SCREEN_HEIGHT // 2))

        # Add Mom back if in main room
        if hasattr(self, 'mom'):
            self.visible_sprites.add(self.mom)

    def create_bedroom(self):
        try:
            floor_surf = pygame.image.load('assets/images/floor.png').convert()
            wall_surf = pygame.image.load('assets/images/wall.png').convert()
        except (pygame.error, FileNotFoundError):
            floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            floor_surf.fill((100, 50, 0))
            wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            wall_surf.fill((200, 200, 200))

        # Fill screen with floor tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)
        
        # Add walls at the top
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((col, TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        # Add bedroom decorations
        self.bed = Decoration((100, 100), [self.visible_sprites, self.obstacle_sprites, self.bed_sprites], 'assets/images/bed.png')
        Decoration((200, 300), [self.visible_sprites], 'assets/images/rug.png')

        # Add items
        if ITEM_ID not in self.state.picked_item_ids:
            Item((300, 150), [self.visible_sprites, self.item_sprites], "Student ID", item_id=ITEM_ID)

        # Add door back to Main
        Door((SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_BEDROOM].right.name, (64, SCREEN_HEIGHT // 2))

    def create_outside(self):
        try:
            grass_surf = pygame.image.load('assets/images/grass.png').convert()
        except (pygame.error, FileNotFoundError):
            grass_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            grass_surf.fill((34, 139, 34))

        # Fill screen with grass tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], grass_surf)

        # Add bus
        self.bus = Bus((SCREEN_WIDTH // 2 - 64, SCREEN_HEIGHT // 2 - 100), [self.visible_sprites])

        # Add door back to Main
        Door((0, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_OUTSIDE].left.name, (SCREEN_WIDTH - 64, SCREEN_HEIGHT // 2))

    def create_intramuros(self):
        try:
            # Cobblestone/Stone look for Intramuros
            stone_surf = pygame.image.load('assets/images/floor.png').convert()
        except (pygame.error, FileNotFoundError):
            stone_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            stone_surf.fill((128, 128, 128)) # Gray for stone

        try:
            wall_surf = pygame.image.load('assets/images/wall.png').convert()
        except (pygame.error, FileNotFoundError):
            wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            wall_surf.fill((100, 100, 100))

        # Fill screen with stone floor tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], stone_surf)

        # Top and Bottom walls
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((col, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        # Add a landmark - Manila Cathedral placeholder
        # We can use a table as placeholder or something else, but let's just use Decoration
        Decoration((SCREEN_WIDTH // 2, 50), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')

        # Add bus
        # Position it near the center
        self.bus = Bus((SCREEN_WIDTH // 2 - 64, SCREEN_HEIGHT // 2 + 50), [self.visible_sprites])

        Door((SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_INTRAMUROS].right.name, (64, SCREEN_HEIGHT // 2))

    def create_school_entrance(self):
        tile_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile_surf.fill((188, 194, 198))
        pygame.draw.line(tile_surf, (226, 230, 232), (0, 0), (TILE_SIZE, 0), 2)
        pygame.draw.line(tile_surf, (130, 138, 144), (0, TILE_SIZE - 1), (TILE_SIZE, TILE_SIZE - 1), 1)
        pygame.draw.line(tile_surf, (226, 230, 232), (0, 0), (0, TILE_SIZE), 2)
        pygame.draw.line(tile_surf, (130, 138, 144), (TILE_SIZE - 1, 0), (TILE_SIZE - 1, TILE_SIZE), 1)

        wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wall_surf.fill((82, 92, 102))
        fence_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        fence_surf.fill((0, 0, 0, 0))
        for x in (6, 15, 24):
            pygame.draw.rect(fence_surf, (112, 120, 126), (x, 2, 3, TILE_SIZE - 4))
        pygame.draw.rect(fence_surf, (172, 178, 184), (3, 8, TILE_SIZE - 6, 3))
        pygame.draw.rect(fence_surf, (172, 178, 184), (3, 22, TILE_SIZE - 6, 3))

        section_width = SCREEN_WIDTH // 4
        admin_door_x = SCREEN_WIDTH // 2 + section_width
        gate_x = section_width + section_width // 2 - TILE_SIZE // 2
        gate_y = SCREEN_HEIGHT // 2 - TILE_SIZE

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], tile_surf)

        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            if not (admin_door_x - TILE_SIZE <= col <= admin_door_x + TILE_SIZE):
                Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((col, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        Door((0, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_SCHOOL_ENTRANCE].left.name, (SCREEN_WIDTH - 64, SCREEN_HEIGHT // 2))

        for row in range(TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE):
            if not (gate_y - TILE_SIZE <= row <= gate_y + TILE_SIZE * 2):
                Tile((gate_x, row), [self.visible_sprites, self.obstacle_sprites], fence_surf)

        gate = PassGate(
            (gate_x, gate_y),
            [self.visible_sprites, self.obstacle_sprites, self.gate_sprites],
            ROOM_SCHOOL_ENTRANCE,
            (gate_x + 96, SCREEN_HEIGHT // 2),
            ITEM_ID,
        )
        gate.left_spawn_pos = (gate_x - 64, SCREEN_HEIGHT // 2)
        gate.right_spawn_pos = (gate_x + 96, SCREEN_HEIGHT // 2)

        self.guard_1 = self.create_guard_npc(
            (gate_x - 48, gate_y + 112),
            SCHOOL_GUARD_NO_ID_DIALOGUE,
        )
        self.guard_2 = self.create_guard_npc(
            (gate_x + 48, gate_y + 112),
            SCHOOL_GUARD_NO_ID_DIALOGUE,
        )

        Door((admin_door_x, 0), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_SCHOOL_ENTRANCE].up.name, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 96))
        Door((SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_SCHOOL_ENTRANCE].right.name, (64, SCREEN_HEIGHT // 2))

    def create_admin_office(self):
        floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        floor_surf.fill((205, 208, 210))
        pygame.draw.line(floor_surf, (235, 238, 240), (0, 0), (TILE_SIZE, 0), 2)
        pygame.draw.line(floor_surf, (150, 155, 160), (0, TILE_SIZE - 1), (TILE_SIZE, TILE_SIZE - 1), 1)

        wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wall_surf.fill((95, 105, 115))

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)

        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            if not (SCREEN_WIDTH // 2 - TILE_SIZE <= col <= SCREEN_WIDTH // 2 + TILE_SIZE):
                Tile((col, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            Tile((0, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((SCREEN_WIDTH - TILE_SIZE, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        Decoration((SCREEN_WIDTH // 2 - 80, 120), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        self.attendant = self.create_attendant_npc((SCREEN_WIDTH // 2 - 8, 150))

        chair_rows = 4
        chair_gap_x = 48
        chair_gap_y = 40
        chair_start_y = 240
        waiting_sections = (
            (176, 3),
            (504, 3),
        )
        for section_start_x, chair_cols in waiting_sections:
            for row in range(chair_rows):
                for col in range(chair_cols):
                    Chair(
                        (section_start_x + col * chair_gap_x, chair_start_y + row * chair_gap_y),
                        [self.visible_sprites, self.obstacle_sprites, self.chair_sprites],
                    )

        Door((SCREEN_WIDTH // 2 - TILE_SIZE // 2, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_ADMIN_OFFICE].down.name, (SCREEN_WIDTH // 2, 96))

    def create_school(self):
        try:
            floor_surf = pygame.image.load('assets/images/floor.png').convert()
            wall_surf = pygame.image.load('assets/images/wall.png').convert()
        except (pygame.error, FileNotFoundError):
            floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            floor_surf.fill((150, 150, 150))
            wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            wall_surf.fill((100, 100, 100))

        # Fill screen with floor tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)
        
        lab_door_x = SCREEN_WIDTH // 2 - TILE_SIZE // 2

        # Add walls at the top
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            if not (lab_door_x - TILE_SIZE <= col <= lab_door_x + TILE_SIZE):
                Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
                Tile((col, TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        # Add text to indicate it's the school
        # Note: we don't have a specific way to draw static text on map yet, 
        # but we can add a sign or something.
        self.school_desk = Decoration((SCREEN_WIDTH // 2, 100), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png') # Placeholder for school desk
        self.school_class_marker = ClassMarker((SCREEN_WIDTH // 2 + 144, 160), [self.visible_sprites, self.class_marker_sprites])

        # Add door to exit school
        Door((0, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_SCHOOL].left.name, (SCREEN_WIDTH - 64, SCREEN_HEIGHT // 2))
        Door((lab_door_x, 0), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_SCHOOL].up.name, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 96))
        Door((SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_SCHOOL].right.name, (96, SCREEN_HEIGHT // 2))
        Door((SCREEN_WIDTH - 6 * TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_SCHOOL].down.name, (SCREEN_WIDTH - 6 * TILE_SIZE, 96))
        Door((5 * TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.door_sprites], ROOM_CAFETERIA, (5 * TILE_SIZE, 96))

    def create_programming_lab(self):
        floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        floor_surf.fill((74, 82, 92))
        pygame.draw.line(floor_surf, (105, 116, 128), (0, 0), (TILE_SIZE, 0), 1)
        pygame.draw.line(floor_surf, (44, 50, 58), (0, TILE_SIZE - 1), (TILE_SIZE, TILE_SIZE - 1), 1)

        wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wall_surf.fill((42, 48, 56))

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)

        exit_door_x = SCREEN_WIDTH // 2 - TILE_SIZE // 2
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            if not (exit_door_x - TILE_SIZE <= col <= exit_door_x + TILE_SIZE):
                Tile((col, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            Tile((0, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((SCREEN_WIDTH - TILE_SIZE, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        self.programming_station = Decoration((SCREEN_WIDTH // 2 - 64, 120), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        self.programming_class_marker = ClassMarker((SCREEN_WIDTH // 2 + 160, 184), [self.visible_sprites, self.class_marker_sprites])
        Decoration((SCREEN_WIDTH // 2 + 64, 120), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        Decoration((SCREEN_WIDTH // 2 - 64, 260), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        Decoration((SCREEN_WIDTH // 2 + 64, 260), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')

        Door((exit_door_x, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_PROGRAMMING_LAB].down.name, (SCREEN_WIDTH // 2 - 96, 96))

    def create_electronics_lab(self):
        floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        floor_surf.fill((69, 84, 76))
        pygame.draw.line(floor_surf, (102, 124, 112), (0, 0), (TILE_SIZE, 0), 1)
        pygame.draw.line(floor_surf, (38, 52, 45), (0, TILE_SIZE - 1), (TILE_SIZE, TILE_SIZE - 1), 1)

        wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wall_surf.fill((35, 54, 48))

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)

        entry_door_y = SCREEN_HEIGHT // 2
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((col, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            if not (entry_door_y - TILE_SIZE <= row <= entry_door_y + TILE_SIZE):
                Tile((0, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((SCREEN_WIDTH - TILE_SIZE, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        self.electronics_station = Decoration((SCREEN_WIDTH // 2 - 64, 120), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        self.electronics_class_marker = ClassMarker((SCREEN_WIDTH // 2 + 160, 184), [self.visible_sprites, self.class_marker_sprites])
        Decoration((SCREEN_WIDTH // 2 + 64, 120), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        Decoration((SCREEN_WIDTH // 2 - 64, 280), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        Decoration((SCREEN_WIDTH // 2 + 64, 280), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')

        Door((TILE_SIZE, entry_door_y), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_ELECTRONICS_LAB].left.name, (SCREEN_WIDTH - 96, SCREEN_HEIGHT // 2))

    def create_library(self):
        floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        floor_surf.fill((96, 82, 66))
        pygame.draw.line(floor_surf, (122, 106, 86), (0, 0), (TILE_SIZE, 0), 1)
        pygame.draw.line(floor_surf, (65, 54, 44), (0, TILE_SIZE - 1), (TILE_SIZE, TILE_SIZE - 1), 1)

        wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wall_surf.fill((54, 44, 36))

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)

        exit_door_x = SCREEN_WIDTH - 6 * TILE_SIZE
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            if not (exit_door_x - TILE_SIZE <= col <= exit_door_x + TILE_SIZE):
                Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((col, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            Tile((0, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((SCREEN_WIDTH - TILE_SIZE, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        self.library_academics_station = Decoration((144, 220), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        self.library_math_station = Decoration((368, 220), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        self.library_discipline_station = Decoration((592, 220), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
        self.library_class_marker = ClassMarker((SCREEN_WIDTH // 2 - 16, 360), [self.visible_sprites, self.class_marker_sprites])

        for shelf_x in (128, 256, 480, 640):
            Decoration((shelf_x, 96), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')

        Door((exit_door_x, 0), [self.visible_sprites, self.door_sprites], self.rooms[ROOM_LIBRARY].up.name, (SCREEN_WIDTH - 6 * TILE_SIZE, SCREEN_HEIGHT - 96))

    def create_cafeteria(self):
        floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        floor_surf.fill((112, 88, 70))
        pygame.draw.line(floor_surf, (142, 112, 90), (0, 0), (TILE_SIZE, 0), 1)
        pygame.draw.line(floor_surf, (75, 57, 46), (0, TILE_SIZE - 1), (TILE_SIZE, TILE_SIZE - 1), 1)

        wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wall_surf.fill((72, 54, 42))

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)

        exit_door_x = 5 * TILE_SIZE
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            if not (exit_door_x - TILE_SIZE <= col <= exit_door_x + TILE_SIZE):
                Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((col, SCREEN_HEIGHT - TILE_SIZE), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            Tile((0, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile((SCREEN_WIDTH - TILE_SIZE, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)

        self.food_vendor = NPC((SCREEN_WIDTH // 2 - 32, 128), [self.visible_sprites, self.obstacle_sprites], 'assets/images/mom.png', name="Food Vendor", can_wander=False)
        self.food_vendor.dialogue = list(CAFETERIA_VENDOR_DIALOGUE)
        self.food_vendor.sprite_asset = 'assets/images/mom.png'
        self.food_vendor.sprite_base_assets = ('assets/images/player.png', 'assets/images/mom.png')

        for table_x in (160, 320, 480, 640):
            Decoration((table_x, 320), [self.visible_sprites, self.obstacle_sprites], 'assets/images/table.png')
            Chair((table_x, 280), [self.visible_sprites, self.obstacle_sprites])
            Chair((table_x, 368), [self.visible_sprites, self.obstacle_sprites])

        Door((exit_door_x, 0), [self.visible_sprites, self.door_sprites], ROOM_SCHOOL, (5 * TILE_SIZE, SCREEN_HEIGHT - 96))

    async def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.handle_events(events)
            self.update()
            self.draw()
            # Ensure high compatibility with browser loop
            self.clock.tick(FPS)
            await asyncio.sleep(0)
        pygame.quit()
        sys.exit()

    def handle_events(self, events=None):
        if events is None:
            events = pygame.event.get()
        self.mobile_controls.handle_events(events)
        if self.mobile_controls.consume_action_press():
            events = list(events)
            events.append(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e))
        inventory_slot_index = self.mobile_controls.consume_inventory_slot_press()
        if inventory_slot_index is not None:
            events = list(events)
            events.append(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1 + inventory_slot_index))
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.state_machine.current_state_name == STATE_MENU:
                    self.close_menu()
                else:
                    self.open_menu()
                break
        self.state_machine.handle_events(events)

    def check_proximity(self, sprite1, sprite2, distance):
        p1 = pygame.math.Vector2(sprite1.rect.center)
        p2 = pygame.math.Vector2(sprite2.rect.center)
        return p1.distance_to(p2) < distance

    def update(self):
        if self.location_display_timer > 0:
            self.location_display_timer -= 1

        self.player.mobile_direction = self.mobile_controls.direction
        self.state_machine.update()

    def check_transitions(self):
        hits = pygame.sprite.spritecollide(self.player, self.door_sprites, False)
        for door in hits:
            self.travel_to_room(door.target_room, door.spawn_pos, use_topleft=True)
            break

    def draw(self):
        self.screen.fill((50, 50, 50))  # Dark gray background
        self.floor_sprites.draw(self.screen)
        self.visible_sprites.draw(self.screen)
        
        self.state_machine.draw(self.screen)

        # Draw money counter
        money_text = str(self.money)
        money_surf = self.font.render(money_text, True, 'white')
        money_rect = money_surf.get_rect(bottomleft=(60, SCREEN_HEIGHT - 20))
        
        # Draw money icon
        icon_rect = self.money_icon.get_rect(midleft=(25, money_rect.centery))
        
        # Draw a small background for money for better visibility
        bg_rect = pygame.Rect(15, SCREEN_HEIGHT - 45, money_surf.get_width() + 55, 30)
        pygame.draw.rect(self.screen, (30, 30, 30), bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect, 1, border_radius=5)
        
        self.screen.blit(self.money_icon, icon_rect)
        self.screen.blit(money_surf, money_rect)

        # Draw XP counter
        xp_text = f"XP: {self.experience}"
        xp_surf = self.font.render(xp_text, True, 'white')
        xp_rect = xp_surf.get_rect(bottomleft=(bg_rect.right + 10, SCREEN_HEIGHT - 20))
        
        xp_bg_rect = xp_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (30, 30, 30), xp_bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), xp_bg_rect, 1, border_radius=5)
        self.screen.blit(xp_surf, xp_rect)

        # Draw energy counter away from bottom inventory and mobile controls
        energy_text = f"Energy: {self.energy}/{MAX_ENERGY}"
        energy_surf = self.font.render(energy_text, True, 'white')
        energy_rect = energy_surf.get_rect(topright=(SCREEN_WIDTH - 25, 20))
        self.energy_hud_rect = energy_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (30, 30, 30), self.energy_hud_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), self.energy_hud_rect, 1, border_radius=5)
        self.screen.blit(energy_surf, energy_rect)

        stress_text = f"Stress: {self.stress}/{MAX_STRESS}"
        stress_surf = self.font.render(stress_text, True, 'white')
        stress_rect = stress_surf.get_rect(topright=(SCREEN_WIDTH - 25, self.energy_hud_rect.bottom + 10))
        self.stress_hud_rect = stress_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (30, 30, 30), self.stress_hud_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), self.stress_hud_rect, 1, border_radius=5)
        self.screen.blit(stress_surf, stress_rect)

        schedule_lines = self.get_schedule_hud_lines()
        schedule_surfs = [self.font.render(line, True, 'white') for line in schedule_lines]
        schedule_width = max(surf.get_width() for surf in schedule_surfs) + 20
        schedule_height = self.font.get_linesize() * len(schedule_surfs) + 12
        self.schedule_hud_rect = pygame.Rect(15, 20, schedule_width, schedule_height)
        pygame.draw.rect(self.screen, (30, 30, 30), self.schedule_hud_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), self.schedule_hud_rect, 1, border_radius=5)
        for line_index, schedule_surf in enumerate(schedule_surfs):
            self.screen.blit(
                schedule_surf,
                (
                    self.schedule_hud_rect.x + 10,
                    self.schedule_hud_rect.y + 6 + line_index * self.font.get_linesize(),
                ),
            )

        # Draw location name
        if self.location_display_timer > 0:
            # Fade out effect
            alpha = min(255, self.location_display_timer * 5)
            # Create a larger font for location
            try:
                loc_font = pygame.font.SysFont('Arial', 48, bold=True)
            except pygame.error:
                loc_font = pygame.font.Font(None, 48)
            loc_surf = loc_font.render(self.location_display_text, True, 'white')
            loc_surf.set_alpha(alpha)
            loc_rect = loc_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
            
            # Draw shadow for better readability
            shadow_surf = loc_font.render(self.location_display_text, True, 'black')
            shadow_surf.set_alpha(alpha)
            shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 2, 100 + 2))
            
            self.screen.blit(shadow_surf, shadow_rect)
            self.screen.blit(loc_surf, loc_rect)

        self.inventory.draw(self.screen)
        self.mobile_controls.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
