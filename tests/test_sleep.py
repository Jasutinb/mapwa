import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.config import STATE_DIALOGUE, STATE_PLAY, STATE_SLEEP_CONFIRM
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    g = Game()
    yield g
    pygame.quit()


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, {"key": key})])


def complete_current_dialogue(game):
    while game.current_dialogue is not None:
        press_key(game, pygame.K_e)


def move_to_bedroom_bed(game):
    game.current_room = "bedroom"
    game.create_map()
    game.visible_sprites.add(game.player)
    game.player.rect.center = game.bed.rect.center


def receive_mom_allowance(game):
    game.current_room = "main"
    game.create_map()
    game.visible_sprites.add(game.player)
    game.player.rect.center = game.mom.rect.center
    press_key(game, pygame.K_e)
    complete_current_dialogue(game)


def test_bed_interaction_opens_sleep_confirmation(game):
    move_to_bedroom_bed(game)

    press_key(game, pygame.K_e)

    assert game.current_day == 1
    assert game.current_dialogue is None
    assert game.state_machine.current_state_name == STATE_SLEEP_CONFIRM


def test_confirming_sleep_advances_to_next_day(game):
    move_to_bedroom_bed(game)
    press_key(game, pygame.K_e)

    press_key(game, pygame.K_RETURN)

    assert game.current_day == 2
    assert game.state_machine.current_state_name == STATE_DIALOGUE
    assert game.current_dialogue == ["You slept through the night. Day 2 begins."]


def test_cancel_sleep_keeps_current_day(game):
    move_to_bedroom_bed(game)
    press_key(game, pygame.K_e)

    press_key(game, pygame.K_RIGHT)
    press_key(game, pygame.K_e)

    assert game.current_day == 1
    assert game.current_dialogue is None
    assert game.state_machine.current_state_name == STATE_PLAY


def test_sleeping_allows_next_day_allowance(game):
    receive_mom_allowance(game)
    assert game.money == 250
    assert game.last_allowance_day == 1

    move_to_bedroom_bed(game)
    press_key(game, pygame.K_e)
    press_key(game, pygame.K_e)
    complete_current_dialogue(game)

    receive_mom_allowance(game)

    assert game.current_day == 2
    assert game.money == 500
    assert game.last_allowance_day == 2


def test_bedroom_interact_away_from_bed_does_not_open_sleep_prompt(game):
    game.current_room = "bedroom"
    game.create_map()
    game.visible_sprites.add(game.player)
    game.player.rect.center = (700, 500)

    press_key(game, pygame.K_e)

    assert game.state_machine.current_state_name == STATE_PLAY
    assert game.current_day == 1


def test_mobile_action_opens_sleep_confirmation(game):
    move_to_bedroom_bed(game)
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.FINGERDOWN, {"finger_id": 1, "x": action_pos[0] / 800, "y": action_pos[1] / 600})]
    )

    assert game.current_day == 1
    assert game.state_machine.current_state_name == STATE_SLEEP_CONFIRM


def test_mobile_action_confirms_default_sleep(game):
    move_to_bedroom_bed(game)
    action_pos = game.mobile_controls.rects["action"].center

    game.handle_events(
        [pygame.event.Event(pygame.FINGERDOWN, {"finger_id": 1, "x": action_pos[0] / 800, "y": action_pos[1] / 600})]
    )
    game.handle_events(
        [pygame.event.Event(pygame.FINGERDOWN, {"finger_id": 2, "x": action_pos[0] / 800, "y": action_pos[1] / 600})]
    )

    assert game.current_day == 2
    assert game.state_machine.current_state_name == STATE_DIALOGUE


def test_mobile_joystick_can_select_cancel_sleep(game):
    move_to_bedroom_bed(game)
    action_pos = game.mobile_controls.rects["action"].center
    joystick_right = (
        game.mobile_controls.joystick_center.x + game.mobile_controls.joystick_radius,
        game.mobile_controls.joystick_center.y,
    )

    game.handle_events(
        [pygame.event.Event(pygame.FINGERDOWN, {"finger_id": 1, "x": action_pos[0] / 800, "y": action_pos[1] / 600})]
    )
    game.handle_events(
        [pygame.event.Event(pygame.FINGERDOWN, {"finger_id": 2, "x": joystick_right[0] / 800, "y": joystick_right[1] / 600})]
    )
    game.update()
    game.handle_events(
        [pygame.event.Event(pygame.FINGERDOWN, {"finger_id": 3, "x": action_pos[0] / 800, "y": action_pos[1] / 600})]
    )

    assert game.current_day == 1
    assert game.current_dialogue is None
    assert game.state_machine.current_state_name == STATE_PLAY
