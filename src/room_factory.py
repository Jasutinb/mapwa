from src.config import (
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
)
from src.level import RoomNode


class RoomFactory:
    """Own room topology and select the builder for the active room."""

    def __init__(self, game):
        self.game = game

    def create_room_graph(self):
        rooms = {
            ROOM_MAIN: RoomNode(ROOM_MAIN, "Living Room"),
            ROOM_BEDROOM: RoomNode(ROOM_BEDROOM, "Bedroom"),
            ROOM_OUTSIDE: RoomNode(ROOM_OUTSIDE, "Outside"),
            ROOM_INTRAMUROS: RoomNode(ROOM_INTRAMUROS, "Intramuros"),
            ROOM_SCHOOL_ENTRANCE: RoomNode(ROOM_SCHOOL_ENTRANCE, "School Entrance"),
            ROOM_ADMIN_OFFICE: RoomNode(ROOM_ADMIN_OFFICE, "Admin Office"),
            ROOM_SCHOOL: RoomNode(ROOM_SCHOOL, "School"),
            ROOM_PROGRAMMING_LAB: RoomNode(ROOM_PROGRAMMING_LAB, "Programming Lab"),
            ROOM_ELECTRONICS_LAB: RoomNode(ROOM_ELECTRONICS_LAB, "Electronics Lab"),
            ROOM_LIBRARY: RoomNode(ROOM_LIBRARY, "Library"),
            ROOM_CAFETERIA: RoomNode(ROOM_CAFETERIA, "Cafeteria"),
        }
        links = (
            (ROOM_MAIN, "left", ROOM_BEDROOM),
            (ROOM_BEDROOM, "right", ROOM_MAIN),
            (ROOM_MAIN, "right", ROOM_OUTSIDE),
            (ROOM_OUTSIDE, "left", ROOM_MAIN),
            (ROOM_OUTSIDE, "right", ROOM_INTRAMUROS),
            (ROOM_INTRAMUROS, "left", ROOM_OUTSIDE),
            (ROOM_INTRAMUROS, "right", ROOM_SCHOOL_ENTRANCE),
            (ROOM_SCHOOL_ENTRANCE, "left", ROOM_INTRAMUROS),
            (ROOM_SCHOOL_ENTRANCE, "right", ROOM_SCHOOL),
            (ROOM_SCHOOL_ENTRANCE, "up", ROOM_ADMIN_OFFICE),
            (ROOM_ADMIN_OFFICE, "down", ROOM_SCHOOL_ENTRANCE),
            (ROOM_SCHOOL, "left", ROOM_SCHOOL_ENTRANCE),
            (ROOM_SCHOOL, "up", ROOM_PROGRAMMING_LAB),
            (ROOM_PROGRAMMING_LAB, "down", ROOM_SCHOOL),
            (ROOM_SCHOOL, "right", ROOM_ELECTRONICS_LAB),
            (ROOM_ELECTRONICS_LAB, "left", ROOM_SCHOOL),
            (ROOM_SCHOOL, "down", ROOM_LIBRARY),
            (ROOM_LIBRARY, "up", ROOM_SCHOOL),
            (ROOM_CAFETERIA, "up", ROOM_SCHOOL),
        )
        for source, direction, target in links:
            setattr(rooms[source], direction, rooms[target])
        return rooms

    def build_current_room(self):
        game = self.game
        for group in game.room_sprite_groups:
            for sprite in group:
                sprite.kill()

        current_node = game.rooms.get(game.current_room)
        if current_node:
            game.location_display_text = current_node.display_name
        game.location_display_timer = game.location_display_duration

        builders = {
            ROOM_MAIN: game.create_main_room,
            ROOM_BEDROOM: game.create_bedroom,
            ROOM_OUTSIDE: game.create_outside,
            ROOM_INTRAMUROS: game.create_intramuros,
            ROOM_SCHOOL_ENTRANCE: game.create_school_entrance,
            ROOM_ADMIN_OFFICE: game.create_admin_office,
            ROOM_SCHOOL: game.create_school,
            ROOM_PROGRAMMING_LAB: game.create_programming_lab,
            ROOM_ELECTRONICS_LAB: game.create_electronics_lab,
            ROOM_LIBRARY: game.create_library,
            ROOM_CAFETERIA: game.create_cafeteria,
        }
        builder = builders.get(game.current_room)
        if builder:
            builder()
