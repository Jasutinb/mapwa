import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.states import DialogueState


@pytest.fixture
def font():
    pygame.init()
    pygame.display.set_mode((800, 600))
    try:
        yield pygame.font.SysFont("Arial", 24)
    finally:
        pygame.quit()


def test_dialogue_wraps_lines_to_fit_box_width(font):
    max_width = 260
    lines = DialogueState.wrap_text(
        "This is a very long line of dialogue that should wrap before it leaves the dialogue box.",
        font,
        max_width,
        max_lines=4,
    )

    assert len(lines) > 1
    assert all(font.size(line)[0] <= max_width for line in lines)


def test_dialogue_truncates_to_available_box_lines(font):
    max_width = 180
    lines = DialogueState.wrap_text(
        "This dialogue is intentionally long enough to need more lines than the box can display cleanly.",
        font,
        max_width,
        max_lines=2,
    )

    assert len(lines) == 2
    assert lines[-1].endswith("...")
    assert all(font.size(line)[0] <= max_width for line in lines)
