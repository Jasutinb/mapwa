import pygame
import pytest

from src.config import STATE_DIALOGUE, STATE_PLANNER, STATE_PLAY
from src.game import Game


@pytest.fixture
def game():
    pygame.init()
    pygame.display.set_mode((800, 600))
    instance = Game()
    yield instance
    pygame.quit()


def press_key(game, key):
    game.handle_events([pygame.event.Event(pygame.KEYDOWN, {"key": key})])


def test_desktop_planner_opens_and_closes_with_p_or_escape(game):
    press_key(game, pygame.K_p)

    assert game.state_machine.current_state_name == STATE_PLANNER

    press_key(game, pygame.K_p)

    assert game.state_machine.current_state_name == STATE_PLAY

    press_key(game, pygame.K_p)
    press_key(game, pygame.K_ESCAPE)

    assert game.state_machine.current_state_name == STATE_PLAY


def test_planner_does_not_interrupt_dialogue(game):
    game.show_dialogue(["Stay focused."])

    press_key(game, pygame.K_p)

    assert game.state_machine.current_state_name == STATE_DIALOGUE
    assert game.current_dialogue == ["Stay focused."]


def test_mobile_planner_button_opens_and_closes_same_state(game):
    planner_pos = game.mobile_controls.rects["planner"].center

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": planner_pos})]
    )

    assert game.state_machine.current_state_name == STATE_PLANNER

    game.handle_events(
        [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": planner_pos})]
    )

    assert game.state_machine.current_state_name == STATE_PLAY


def test_planner_sections_use_live_academic_and_objective_state(game):
    planner = game.state_machine.states[STATE_PLANNER]

    sections = planner.get_sections()

    assert sections["Today's Schedule"] == [
        "08:00 Academics (School)",
        "10:00 Programming (Programming Lab)",
    ]
    assert sections["Assignments"] == ["Academics Reflection due Day 2"]
    assert sections["Upcoming Exams"] == [
        "Day 5 Academics Midterm",
        "Day 6 Programming Practical",
    ]
    assert sections["Grade Standing"] == ["75/100"]
    assert sections["Current Objective"] == ["Pick up your Student ID."]


def test_planner_sections_have_clean_empty_states(game):
    game.current_day = 6
    game.state.assignments.clear()
    game.state.exams.clear()
    game.quest_manager.quests.clear()
    planner = game.state_machine.states[STATE_PLANNER]

    sections = planner.get_sections()

    assert sections["Today's Schedule"] == ["No classes scheduled today."]
    assert sections["Assignments"] == ["No active assignments."]
    assert sections["Upcoming Exams"] == ["No upcoming exams."]
    assert sections["Current Objective"] == ["No active objective."]


def test_planner_layout_stays_in_bounds_and_suppresses_play_hud(game, monkeypatch):
    inventory_draws = []
    monkeypatch.setattr(
        game.inventory,
        "draw",
        lambda screen: inventory_draws.append(screen),
    )
    press_key(game, pygame.K_p)
    game.draw()
    planner = game.state_machine.states[STATE_PLANNER]

    assert pygame.Rect(0, 0, 800, 600).contains(planner.panel_rect)
    assert all(
        planner.panel_rect.contains(rect) for rect in planner.section_rects.values()
    )
    section_rects = list(planner.section_rects.values())
    assert all(
        not first.colliderect(second)
        for index, first in enumerate(section_rects)
        for second in section_rects[index + 1 :]
    )
    assert all(
        not game.mobile_controls.rects["planner"].colliderect(rect)
        for rect in section_rects
    )
    assert inventory_draws == []
    assert game.money_hud_rect.size == (0, 0)
    assert game.objective_hud_rect.size == (0, 0)
    assert game.energy_hud_rect.size == (0, 0)
    assert game.stress_hud_rect.size == (0, 0)
