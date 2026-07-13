import pygame
import pytest

from src.academic_system import AcademicSystem
from src.game import Game
from src.hud_renderer import HUDRenderer
from src.interaction_system import InteractionSystem
from src.room_factory import RoomFactory
from src.save_system import SaveSystem


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    instance = Game()
    yield instance
    pygame.quit()


def test_game_composes_focused_system_boundaries(game):
    assert isinstance(game.academic_system, AcademicSystem)
    assert isinstance(game.hud_renderer, HUDRenderer)
    assert isinstance(game.interaction_system, InteractionSystem)
    assert isinstance(game.room_factory, RoomFactory)
    assert isinstance(game.save_system, SaveSystem)


def test_game_academic_api_delegates_to_academic_system(game, monkeypatch):
    monkeypatch.setattr(
        game.academic_system,
        "get_assignment_summary",
        lambda: "delegated assignment summary",
    )

    assert game.get_assignment_summary() == "delegated assignment summary"


def test_game_hud_api_delegates_to_hud_renderer(game, monkeypatch):
    monkeypatch.setattr(
        game.hud_renderer,
        "fit_text",
        lambda text, max_width: f"{text}:{max_width}",
    )

    assert game.fit_hud_text("Objective", 120) == "Objective:120"


def test_keyboard_and_mobile_actions_share_interaction_system(
    game,
    monkeypatch,
):
    calls = []
    monkeypatch.setattr(
        game.interaction_system,
        "interact",
        lambda: calls.append("interact") or True,
    )

    game.handle_events([pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})])
    action_pos = game.mobile_controls.rects["action"].center
    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert calls == ["interact", "interact"]


def test_game_room_api_delegates_to_room_factory(game, monkeypatch):
    calls = []
    monkeypatch.setattr(
        game.room_factory,
        "build_current_room",
        lambda: calls.append(game.current_room),
    )

    game.create_map()

    assert calls == [game.current_room]
