import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.game import Game
from src.mobile_controls import MobileControls
from src.player import Player


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


def test_mobile_joystick_mouse_controls_direction():
    controls = MobileControls()
    right_pos = (
        controls.joystick_center.x + controls.joystick_radius,
        controls.joystick_center.y,
    )

    controls.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": right_pos})]
    )

    assert controls.direction.x == 1
    assert controls.direction.y == 0

    controls.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": right_pos})]
    )

    assert controls.direction.length_squared() == 0


def test_mobile_joystick_clears_bottom_hud():
    controls = MobileControls()
    joystick_bottom = controls.joystick_center.y + controls.joystick_radius
    touch_area_bottom = joystick_bottom + controls.knob_radius

    assert joystick_bottom <= SCREEN_HEIGHT - controls.bottom_hud_clearance
    assert touch_area_bottom < SCREEN_HEIGHT - 45


def test_mobile_action_button_does_not_cover_bottom_hud():
    controls = MobileControls()
    money_hud = pygame.Rect(15, SCREEN_HEIGHT - 45, 240, 35)

    assert not controls.rects["action"].colliderect(money_hud)


def test_mobile_action_button_does_not_cover_dialogue_box():
    controls = MobileControls()
    dialogue_box = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)

    assert not controls.rects["action"].colliderect(dialogue_box)


def test_mobile_joystick_drag_clamps_direction():
    controls = MobileControls()
    start_pos = controls.joystick_center
    far_up_right = (
        controls.joystick_center.x + controls.joystick_radius * 4,
        controls.joystick_center.y - controls.joystick_radius * 4,
    )

    controls.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": start_pos})]
    )
    controls.handle_events(
        [
            pygame.event.Event(
                pygame.MOUSEMOTION,
                {"buttons": (1, 0, 0), "pos": far_up_right},
            )
        ]
    )

    assert controls.direction.length() == pytest.approx(1)
    assert controls.direction.x > 0
    assert controls.direction.y < 0


def test_mobile_joystick_dead_zone():
    controls = MobileControls()
    small_offset = (
        controls.joystick_center.x + controls.joystick_radius * 0.1,
        controls.joystick_center.y,
    )

    controls.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": small_offset})]
    )

    assert controls.direction.length_squared() == 0


def test_mobile_touch_controls_direction():
    controls = MobileControls()
    up_pos = (
        controls.joystick_center.x,
        controls.joystick_center.y - controls.joystick_radius,
    )

    controls.handle_events(
        [
            pygame.event.Event(
                pygame.FINGERDOWN,
                {
                    "finger_id": 1,
                    "x": up_pos[0] / SCREEN_WIDTH,
                    "y": up_pos[1] / SCREEN_HEIGHT,
                },
            )
        ]
    )

    assert controls.direction.y == pytest.approx(-1, abs=0.02)

    controls.handle_events([pygame.event.Event(pygame.FINGERUP, {"finger_id": 1})])

    assert controls.direction.length_squared() == 0


def test_mobile_action_press_is_consumed_once():
    controls = MobileControls()
    action_pos = controls.rects["action"].center

    controls.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert controls.consume_action_press() is True
    assert controls.consume_action_press() is False


def test_player_uses_mobile_direction():
    player = Player((0, 0), [])
    player.mobile_direction.xy = (1, 0)

    player.update()

    assert player.rect.x == player.speed


def test_mobile_action_button_triggers_interaction():
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game()
    game.player.rect.center = game.mom.rect.center
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": action_pos})]
    )

    assert game.current_dialogue == game.mom.dialogue
