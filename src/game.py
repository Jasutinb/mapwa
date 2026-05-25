import pygame
import sys
import asyncio

from src.config import (
    FPS,
    LOCATION_DISPLAY_DURATION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
)
from src.player import Player
from src.npc import NPC
from src.inventory import Inventory
from src.level import Tile, Decoration, Door, Bus, Item, MapProp, RoomNode
from src.mobile_controls import MobileControls
from src.state import StateMachine
from src.states import PlayState, DialogueState


class Game:
    def __init__(self):
        # pygame.init() moved to main.py for better WASM compatibility
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Student RPG")
        self.clock = pygame.time.Clock()
        self.running = True

        # Sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.floor_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()

        self.location_display_text = ""
        self.location_display_timer = 0
        self.location_display_duration = LOCATION_DISPLAY_DURATION
        self.collected_item_ids = set()
        self.mobile_controls = MobileControls()

        # Level setup
        self.setup_rooms()
        self.current_room = "main"
        self.create_map()

        # Player setup
        self.player = Player(
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            [self.visible_sprites],
            self.obstacle_sprites,
        )

        # NPC setup
        self.mom = NPC(
            (SCREEN_WIDTH // 2, 100),
            [self.visible_sprites],
            "assets/images/mom.png",
            name="Mom",
        )
        self.mom.dialogue = [
            "Hi sweetie!",
            "Are you ready for your first day at school?",
            "Don't forget your backpack!",
            "Here's your allowance for today.",
        ]

        # Interaction setup
        self.current_dialogue = None
        self.current_dialogue_source = None
        self.dialogue_index = 0
        try:
            self.font = pygame.font.SysFont("Arial", 24)
        except pygame.error:
            self.font = pygame.font.Font(None, 24)

        # Inventory setup
        self.inventory = Inventory()

        # Money setup
        self.money = 0
        self.has_talked_to_mom = False

        # Experience setup
        self.experience = 0

        # UI Assets
        self.money_icon = self.create_money_icon()

        # State Machine setup
        self.state_machine = StateMachine()
        self.state_machine.add_state("play", PlayState(self))
        self.state_machine.add_state("dialogue", DialogueState(self))
        self.state_machine.change_state("play")

    def setup_rooms(self):
        # Create room nodes
        self.rooms = {
            "main": RoomNode("main", "Living Room"),
            "bedroom": RoomNode("bedroom", "Bedroom"),
            "outside": RoomNode("outside", "Outside"),
            "intramuros": RoomNode("intramuros", "Intramuros"),
            "school": RoomNode("school", "School"),
        }

        # Link rooms
        # Main is center-ish
        # Bedroom is to the left of Main
        self.rooms["main"].left = self.rooms["bedroom"]
        self.rooms["bedroom"].right = self.rooms["main"]

        # Outside is to the right of Main
        self.rooms["main"].right = self.rooms["outside"]
        self.rooms["outside"].left = self.rooms["main"]

        # Intramuros is linked via Bus from Outside, but geographically let's say it's to the right of Outside
        self.rooms["outside"].right = self.rooms["intramuros"]
        self.rooms["intramuros"].left = self.rooms["outside"]

        # School is linked via Bus from Intramuros, let's say it's to the right of Intramuros
        self.rooms["intramuros"].right = self.rooms["school"]
        self.rooms["school"].left = self.rooms["intramuros"]

    def create_money_icon(self):
        icon = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(icon, (255, 215, 0), (12, 12), 11)  # Gold circle
        pygame.draw.circle(icon, (184, 134, 11), (12, 12), 11, 2)  # Darker border
        # Draw a small 'P' for Peso
        try:
            font = pygame.font.SysFont("Arial", 20, bold=True)
        except pygame.error:
            font = pygame.font.Font(None, 20)
        p_surf = font.render("P", True, (139, 69, 19))
        p_rect = p_surf.get_rect(center=(12, 12))
        icon.blit(p_surf, p_rect)
        return icon

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
        for sprite in self.interactable_sprites:
            sprite.kill()

        # Set location display
        current_node = self.rooms.get(self.current_room)
        if current_node:
            self.location_display_text = current_node.display_name

        self.location_display_timer = self.location_display_duration

        if self.current_room == "main":
            self.create_main_room()
        elif self.current_room == "bedroom":
            self.create_bedroom()
        elif self.current_room == "outside":
            self.create_outside()
        elif self.current_room == "intramuros":
            self.create_intramuros()
        elif self.current_room == "school":
            self.create_school()

    def create_main_room(self):
        try:
            floor_surf = pygame.image.load("assets/images/floor.png").convert()
            wall_surf = pygame.image.load("assets/images/wall.png").convert()
        except pygame.error, FileNotFoundError:
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
            Tile(
                (col, TILE_SIZE),
                [self.visible_sprites, self.obstacle_sprites],
                wall_surf,
            )

        # Add a table
        Decoration(
            (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2),
            [self.visible_sprites, self.obstacle_sprites],
            "assets/images/table.png",
        )

        # Add doors
        # To Bedroom (left)
        Door(
            (0, SCREEN_HEIGHT // 2),
            [self.visible_sprites, self.door_sprites],
            self.rooms["main"].left.name,
            (SCREEN_WIDTH - 64, SCREEN_HEIGHT // 2),
        )
        # To Outside (right)
        Door(
            (SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2),
            [self.visible_sprites, self.door_sprites],
            self.rooms["main"].right.name,
            (64, SCREEN_HEIGHT // 2),
        )

        # Add Mom back if in main room
        if hasattr(self, "mom"):
            self.visible_sprites.add(self.mom)

    def create_bedroom(self):
        try:
            floor_surf = pygame.image.load("assets/images/floor.png").convert()
            wall_surf = pygame.image.load("assets/images/wall.png").convert()
        except pygame.error, FileNotFoundError:
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
            Tile(
                (col, TILE_SIZE),
                [self.visible_sprites, self.obstacle_sprites],
                wall_surf,
            )

        # Add bedroom decorations
        Decoration(
            (100, 100),
            [self.visible_sprites, self.obstacle_sprites],
            "assets/images/bed.png",
        )
        Decoration((200, 300), [self.visible_sprites], "assets/images/rug.png")

        # Add items
        self.add_room_item("bedroom:notebook", (300, 150), "Notebook")

        # Add door back to Main
        Door(
            (SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2),
            [self.visible_sprites, self.door_sprites],
            self.rooms["bedroom"].right.name,
            (64, SCREEN_HEIGHT // 2),
        )

    def create_outside(self):
        try:
            grass_surf = pygame.image.load("assets/images/grass.png").convert()
        except pygame.error, FileNotFoundError:
            grass_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            grass_surf.fill((34, 139, 34))

        road_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        road_surf.fill((68, 70, 74))
        sidewalk_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sidewalk_surf.fill((176, 176, 164))
        path_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        path_surf.fill((158, 132, 88))

        # Fill screen with grass tiles, then layer walkable paths over it.
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], grass_surf)

        for row in range(SCREEN_HEIGHT - TILE_SIZE * 5, SCREEN_HEIGHT - TILE_SIZE * 2, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], road_surf)

        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, SCREEN_HEIGHT - TILE_SIZE * 6), [self.floor_sprites], sidewalk_surf)

        for row in range(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - TILE_SIZE * 5, TILE_SIZE):
            for col in range(TILE_SIZE, TILE_SIZE * 5, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], path_surf)

        self.outside_landmarks = {}

        house = MapProp(
            (0, SCREEN_HEIGHT // 2 - 96),
            (TILE_SIZE * 4, TILE_SIZE * 5),
            [self.visible_sprites],
            (138, 84, 58),
            "House Front",
            kind="house",
            border_color=(84, 50, 34),
        )
        self.outside_landmarks[house.name] = house.rect.copy()

        shop = MapProp(
            (SCREEN_WIDTH - 224, SCREEN_HEIGHT // 2 - 144),
            (176, 96),
            [self.visible_sprites, self.interactable_sprites],
            (54, 132, 150),
            "Sari-sari Store",
            kind="shop",
            border_color=(28, 70, 82),
            dialogue=[
                "The store is open early.",
                "Snacks and school supplies will be sold here soon.",
            ],
        )
        self.outside_landmarks[shop.name] = shop.rect.copy()

        bus_stop = MapProp(
            (SCREEN_WIDTH // 2 - 48, SCREEN_HEIGHT - TILE_SIZE * 7),
            (32, 80),
            [self.visible_sprites, self.interactable_sprites],
            (238, 214, 94),
            "Bus Stop",
            kind="bus_stop",
            border_color=(76, 76, 62),
            dialogue=["Buses here go to Intramuros."],
        )
        self.outside_landmarks[bus_stop.name] = bus_stop.rect.copy()

        shelter = MapProp(
            (SCREEN_WIDTH // 2 - 16, SCREEN_HEIGHT - TILE_SIZE * 7),
            (112, 56),
            [self.visible_sprites],
            (112, 128, 140, 210),
            "Bus Shelter",
            kind="shelter",
            border_color=(54, 68, 76),
        )
        self.outside_landmarks[shelter.name] = shelter.rect.copy()

        for tree_pos in [(216, 128), (328, 176), (704, 96)]:
            tree = MapProp(
                tree_pos,
                (40, 56),
                [self.visible_sprites, self.obstacle_sprites],
                (42, 126, 62),
                "Tree",
                kind="tree",
                border_color=(24, 76, 38),
            )
            self.outside_landmarks[f"Tree {tree_pos[0]}"] = tree.rect.copy()

        for fence_pos in [(168, 288), (200, 288), (232, 288)]:
            fence = MapProp(
                fence_pos,
                (28, 16),
                [self.visible_sprites, self.obstacle_sprites],
                (180, 132, 74),
                "Fence",
                kind="fence",
                border_color=(116, 78, 42),
            )
            self.outside_landmarks[f"Fence {fence_pos[0]}"] = fence.rect.copy()

        self.outside_neighbor = NPC(
            (272, SCREEN_HEIGHT // 2 - 24),
            [self.visible_sprites, self.interactable_sprites],
            "assets/images/mom.png",
            name="Neighbor",
        )
        self.outside_neighbor.speed = 0
        self.outside_neighbor.dialogue = [
            "Morning! The bus stop is just ahead.",
            "Intramuros is a good place to explore before school.",
        ]

        # Add bus
        self.bus = Bus(
            (SCREEN_WIDTH // 2 + 112, SCREEN_HEIGHT - TILE_SIZE * 5),
            [self.visible_sprites],
        )

        # Add door back to Main
        Door(
            (0, SCREEN_HEIGHT // 2),
            [self.visible_sprites, self.door_sprites],
            self.rooms["outside"].left.name,
            (SCREEN_WIDTH - 64, SCREEN_HEIGHT // 2),
        )

        self.add_room_item("outside:coin", (192, SCREEN_HEIGHT // 2 + 48), "Coin")

    def create_intramuros(self):
        def patterned_tile(base_color, line_color=None):
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surface.fill(base_color)
            if line_color:
                pygame.draw.line(surface, line_color, (0, 0), (TILE_SIZE, 0))
                pygame.draw.line(surface, line_color, (0, 0), (0, TILE_SIZE))
            return surface

        stone_surf = patterned_tile((142, 137, 126), (116, 111, 102))
        plaza_surf = patterned_tile((166, 157, 138), (132, 122, 106))
        road_surf = patterned_tile((66, 68, 72), (52, 54, 58))
        sidewalk_surf = patterned_tile((186, 178, 160), (150, 142, 126))
        crosswalk_surf = patterned_tile((228, 226, 216), (196, 194, 184))
        wall_surf = patterned_tile((92, 88, 80), (68, 64, 58))

        road_top = SCREEN_HEIGHT - TILE_SIZE * 8
        road_bottom = SCREEN_HEIGHT - TILE_SIZE * 5
        upper_sidewalk = road_top - TILE_SIZE
        lower_sidewalk = road_bottom
        school_path_left = SCREEN_WIDTH - TILE_SIZE * 7
        school_path_right = SCREEN_WIDTH - TILE_SIZE * 2

        # Fill screen with stone, then layer the commute route over it.
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], stone_surf)

        for row in range(road_top, road_bottom, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], road_surf)

        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, upper_sidewalk), [self.floor_sprites], sidewalk_surf)
            Tile((col, lower_sidewalk), [self.floor_sprites], sidewalk_surf)

        for row in range(TILE_SIZE * 4, upper_sidewalk + TILE_SIZE, TILE_SIZE):
            for col in range(school_path_left, school_path_right, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], plaza_surf)

        for row in range(road_top, road_bottom, TILE_SIZE):
            Tile((TILE_SIZE * 18, row), [self.floor_sprites], crosswalk_surf)

        # Physical boundaries for the walled city edge.
        gate_gap_top = road_top - TILE_SIZE
        gate_gap_bottom = road_bottom + TILE_SIZE
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            if not gate_gap_top <= row <= gate_gap_bottom:
                Tile((0, row), [self.visible_sprites, self.obstacle_sprites], wall_surf)
                Tile(
                    (SCREEN_WIDTH - TILE_SIZE, row),
                    [self.visible_sprites, self.obstacle_sprites],
                    wall_surf,
                )

        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile(
                (col, SCREEN_HEIGHT - TILE_SIZE),
                [self.visible_sprites, self.obstacle_sprites],
                wall_surf,
            )

        self.intramuros_landmarks = {}

        gate = MapProp(
            (SCREEN_WIDTH - TILE_SIZE * 8, TILE_SIZE * 2),
            (TILE_SIZE * 7, TILE_SIZE * 3),
            [self.visible_sprites, self.obstacle_sprites],
            (126, 42, 48),
            "Mapua University Entrance",
            kind="school_gate",
            border_color=(72, 26, 30),
            label="MAPUA UNIVERSITY",
            dialogue=["The Mapua gate is busy with students heading to class."],
        )
        self.intramuros_landmarks[gate.name] = gate.rect.copy()

        guard_booth = MapProp(
            (SCREEN_WIDTH - TILE_SIZE * 9, TILE_SIZE * 6),
            (TILE_SIZE * 2, TILE_SIZE * 2),
            [self.visible_sprites, self.interactable_sprites],
            (94, 112, 124),
            "Guard Booth",
            kind="guard_booth",
            border_color=(48, 60, 68),
            dialogue=[
                "The guard nods as students pass through.",
                "Classes are inside. Use the gate when you're ready.",
            ],
        )
        self.intramuros_landmarks[guard_booth.name] = guard_booth.rect.copy()

        vendor = MapProp(
            (TILE_SIZE * 7, upper_sidewalk - TILE_SIZE),
            (TILE_SIZE * 3, TILE_SIZE * 2),
            [self.visible_sprites, self.interactable_sprites],
            (222, 166, 54),
            "Snack Vendor",
            kind="vendor",
            border_color=(126, 82, 24),
            label="SNACKS",
            dialogue=[
                "Fresh bread and cold drinks for students.",
                "A quick snack before class might help later.",
            ],
        )
        self.intramuros_landmarks[vendor.name] = vendor.rect.copy()

        waiting_area = MapProp(
            (TILE_SIZE * 10, lower_sidewalk),
            (TILE_SIZE * 4, TILE_SIZE),
            [self.visible_sprites, self.interactable_sprites],
            (232, 218, 116),
            "Transit Waiting Area",
            kind="bus_stop",
            border_color=(112, 104, 54),
            dialogue=[
                "Students wait here for rides home.",
                "Stand left of the bus to go back Outside, or right to go to School.",
            ],
        )
        self.intramuros_landmarks[waiting_area.name] = waiting_area.rect.copy()

        old_wall_marker = MapProp(
            (TILE_SIZE * 2, TILE_SIZE * 4),
            (TILE_SIZE * 5, TILE_SIZE * 2),
            [self.visible_sprites],
            (104, 100, 90),
            "Old Stone Wall",
            kind="wall_marker",
            border_color=(72, 68, 62),
            label="WALLED CITY",
        )
        self.intramuros_landmarks[old_wall_marker.name] = old_wall_marker.rect.copy()

        left_gate = MapProp(
            (TILE_SIZE, upper_sidewalk),
            (TILE_SIZE * 3, TILE_SIZE),
            [self.visible_sprites],
            (116, 104, 88),
            "Intramuros Gate",
            kind="gate",
            border_color=(76, 68, 56),
        )
        self.intramuros_landmarks[left_gate.name] = left_gate.rect.copy()

        for lamp_pos in [
            (TILE_SIZE * 5, upper_sidewalk - TILE_SIZE),
            (TILE_SIZE * 14, upper_sidewalk - TILE_SIZE),
            (TILE_SIZE * 20, lower_sidewalk + TILE_SIZE),
        ]:
            lamp = MapProp(
                lamp_pos,
                (12, 36),
                [self.visible_sprites, self.obstacle_sprites],
                (54, 58, 62),
                "Lamp Post",
                kind="lamp",
                border_color=(30, 32, 34),
            )
            self.intramuros_landmarks[f"Lamp Post {lamp_pos[0]}"] = lamp.rect.copy()

        for planter_pos in [
            (TILE_SIZE * 12, TILE_SIZE * 5),
            (TILE_SIZE * 15, TILE_SIZE * 7),
            (TILE_SIZE * 22, TILE_SIZE * 9),
        ]:
            planter = MapProp(
                planter_pos,
                (TILE_SIZE, TILE_SIZE),
                [self.visible_sprites, self.obstacle_sprites],
                (50, 128, 74),
                "Planter",
                kind="planter",
                border_color=(36, 80, 48),
            )
            self.intramuros_landmarks[f"Planter {planter_pos[0]}"] = planter.rect.copy()

        self.intramuros_guard = NPC(
            (SCREEN_WIDTH - TILE_SIZE * 6, TILE_SIZE * 7),
            [self.visible_sprites, self.interactable_sprites],
            "assets/images/mom.png",
            name="Guard",
        )
        self.intramuros_guard.speed = 0
        self.intramuros_guard.dialogue = [
            "Good morning. Mapua students may enter through the gate.",
            "Keep your ID ready once we add the school ID system.",
        ]

        self.intramuros_classmate = NPC(
            (SCREEN_WIDTH - TILE_SIZE * 4, TILE_SIZE * 8),
            [self.visible_sprites, self.interactable_sprites],
            "assets/images/mom.png",
            name="Classmate",
        )
        self.intramuros_classmate.speed = 0
        self.intramuros_classmate.dialogue = [
            "I usually take this Intramuros route too.",
            "Let's head inside before class starts.",
        ]

        self.bus = Bus(
            (SCREEN_WIDTH // 2 - 64, road_top + TILE_SIZE),
            [self.visible_sprites],
        )

        Door(
            (SCREEN_WIDTH - TILE_SIZE * 5, TILE_SIZE * 5),
            [self.visible_sprites, self.door_sprites],
            self.rooms["intramuros"].right.name,
            (96, SCREEN_HEIGHT // 2),
        )

        self.add_room_item(
            "intramuros:student_flyer",
            (TILE_SIZE * 16, lower_sidewalk + TILE_SIZE),
            "Student Flyer",
        )

    def create_school(self):
        try:
            floor_surf = pygame.image.load("assets/images/floor.png").convert()
            wall_surf = pygame.image.load("assets/images/wall.png").convert()
        except pygame.error, FileNotFoundError:
            floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            floor_surf.fill((150, 150, 150))
            wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            wall_surf.fill((100, 100, 100))

        # Fill screen with floor tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)

        # Add walls at the top
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites, self.obstacle_sprites], wall_surf)
            Tile(
                (col, TILE_SIZE),
                [self.visible_sprites, self.obstacle_sprites],
                wall_surf,
            )

        # Add text to indicate it's the school
        # Note: we don't have a specific way to draw static text on map yet,
        # but we can add a sign or something.
        self.school_desk = Decoration(
            (SCREEN_WIDTH // 2, 100),
            [self.visible_sprites, self.obstacle_sprites],
            "assets/images/table.png",
        )  # Placeholder for school desk

        # Add bus to go back
        self.bus = Bus(
            (SCREEN_WIDTH // 2 - 64, SCREEN_HEIGHT - 100), [self.visible_sprites]
        )

        # Add door to exit school
        Door(
            (0, SCREEN_HEIGHT // 2),
            [self.visible_sprites, self.door_sprites],
            self.rooms["school"].left.name,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),
        )

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
        self.state_machine.handle_events(events)

    def add_room_item(self, item_id, pos, name, image_path=None):
        if item_id not in self.collected_item_ids:
            Item(
                pos,
                [self.visible_sprites, self.item_sprites],
                name,
                image_path,
                item_id,
            )

    def mark_item_collected(self, item):
        item_id = getattr(item, "item_id", None)
        if item_id:
            self.collected_item_ids.add(item_id)

    def check_proximity(self, sprite1, sprite2, distance):
        p1 = pygame.math.Vector2(sprite1.rect.center)
        p2 = pygame.math.Vector2(sprite2.rect.center)
        return p1.distance_to(p2) < distance

    def update(self):
        if self.location_display_timer > 0:
            self.location_display_timer -= 1

        if hasattr(self, "player"):
            self.player.mobile_direction = self.mobile_controls.direction

        self.state_machine.update()

    def check_transitions(self):
        hits = pygame.sprite.spritecollide(self.player, self.door_sprites, False)
        for door in hits:
            self.current_room = door.target_room
            self.create_map()
            self.player.rect.topleft = door.spawn_pos
            self.visible_sprites.add(self.player)
            break

    def draw(self):
        self.screen.fill((50, 50, 50))  # Dark gray background
        self.floor_sprites.draw(self.screen)
        self.visible_sprites.draw(self.screen)

        self.state_machine.draw(self.screen)

        # Draw money counter
        money_text = str(self.money)
        money_surf = self.font.render(money_text, True, "white")
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
        xp_surf = self.font.render(xp_text, True, "white")
        xp_rect = xp_surf.get_rect(bottomleft=(bg_rect.right + 10, SCREEN_HEIGHT - 20))

        xp_bg_rect = xp_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (30, 30, 30), xp_bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), xp_bg_rect, 1, border_radius=5)
        self.screen.blit(xp_surf, xp_rect)

        # Draw location name
        if self.location_display_timer > 0:
            # Fade out effect
            alpha = min(255, self.location_display_timer * 5)
            # Create a larger font for location
            try:
                loc_font = pygame.font.SysFont("Arial", 48, bold=True)
            except pygame.error:
                loc_font = pygame.font.Font(None, 48)
            loc_surf = loc_font.render(self.location_display_text, True, "white")
            loc_surf.set_alpha(alpha)
            loc_rect = loc_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))

            # Draw shadow for better readability
            shadow_surf = loc_font.render(self.location_display_text, True, "black")
            shadow_surf.set_alpha(alpha)
            shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 2, 100 + 2))

            self.screen.blit(shadow_surf, shadow_rect)
            self.screen.blit(loc_surf, loc_rect)

        self.inventory.draw(self.screen)
        self.mobile_controls.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    asyncio.run(game.run())
