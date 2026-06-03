import os

import pygame
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from src.game import Game
from src.transport import BUS_TRANSPORT, TRANSPORT_BUS, get_transport_mode


@pytest.fixture
def game():
    pygame.init()
    g = Game()
    yield g
    pygame.quit()


def test_transport_mode_registry_returns_bus_fare():
    transport = get_transport_mode(TRANSPORT_BUS)

    assert transport is BUS_TRANSPORT
    assert transport.label == "bus"
    assert transport.fare == 20


def test_transport_mode_registry_rejects_unknown_mode():
    with pytest.raises(ValueError, match="Unknown transport mode"):
        get_transport_mode("tricycle")


def test_pay_transport_fare_deducts_registered_fare(game):
    game.money = BUS_TRANSPORT.fare

    assert game.pay_transport_fare(TRANSPORT_BUS) is True
    assert game.money == 0


def test_pay_transport_fare_blocks_when_money_is_short(game):
    game.money = BUS_TRANSPORT.fare - 1

    assert game.pay_transport_fare(TRANSPORT_BUS) is False
    assert game.money == BUS_TRANSPORT.fare - 1
    assert game.current_dialogue == [BUS_TRANSPORT.insufficient_funds_dialogue()]
