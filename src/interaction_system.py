import pygame

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
    SKILL_ACADEMICS,
    SKILL_DISCIPLINE,
    SKILL_MATH,
)


class InteractionSystem:
    """Resolve the shared keyboard/mobile action request in gameplay order."""

    def __init__(self, game):
        self.game = game

    @staticmethod
    def check_proximity(sprite1, sprite2, distance):
        first = pygame.math.Vector2(sprite1.rect.center)
        second = pygame.math.Vector2(sprite2.rect.center)
        return first.distance_to(second) < distance

    def interact(self):
        game = self.game
        near = self.check_proximity

        if (
            game.current_room == ROOM_MAIN
            and hasattr(game, "mom")
            and game.mom in game.visible_sprites
            and near(game.player, game.mom, 64)
        ):
            return game.talk_to_mom()
        if (
            game.current_room in (ROOM_OUTSIDE, ROOM_INTRAMUROS)
            and hasattr(game, "bus")
            and near(game.player, game.bus, 100)
        ):
            return game.ride_bus()
        if game.current_room == ROOM_SCHOOL_ENTRANCE and game.try_enter_school_gate():
            return True
        if game.current_room == ROOM_SCHOOL_ENTRANCE and game.talk_to_guard():
            return True
        if game.current_room == ROOM_ADMIN_OFFICE and game.talk_to_attendant():
            return True
        if game.current_room == ROOM_SCHOOL and game.talk_to_classmate():
            return True
        if (
            game.current_room == ROOM_SCHOOL
            and hasattr(game, "school_desk")
            and near(game.player, game.school_desk, 64)
        ):
            return game.study_at_school()
        if (
            game.current_room == ROOM_PROGRAMMING_LAB
            and hasattr(game, "programming_station")
            and near(game.player, game.programming_station, 64)
        ):
            return game.practice_programming()
        if (
            game.current_room == ROOM_ELECTRONICS_LAB
            and hasattr(game, "electronics_station")
            and near(game.player, game.electronics_station, 64)
        ):
            return game.practice_electronics()
        if game.current_room == ROOM_LIBRARY:
            library_actions = (
                ("library_academics_station", SKILL_ACADEMICS, "academics"),
                ("library_math_station", SKILL_MATH, "math"),
                ("library_discipline_station", SKILL_DISCIPLINE, "discipline"),
            )
            for station_name, skill, label in library_actions:
                station = getattr(game, station_name, None)
                if station and near(game.player, station, 64):
                    return game.study_at_library(skill, label)
        if game.get_exam_marker_near_player():
            return game.take_exam()
        if game.get_class_marker_near_player():
            return game.attend_class()
        if game.get_assignment_marker_near_player():
            return game.complete_assignment()
        if (
            game.current_room == ROOM_CAFETERIA
            and hasattr(game, "food_vendor")
            and near(game.player, game.food_vendor, 64)
        ):
            return game.buy_cafeteria_meal()
        if (
            game.current_room == ROOM_BEDROOM
            and hasattr(game, "bed")
            and near(game.player, game.bed, 64)
        ):
            return game.open_sleep_confirmation()

        for item in pygame.sprite.spritecollide(game.player, game.item_sprites, False):
            if game.pick_up_item(item):
                return True
        return False
