from dataclasses import dataclass


TRANSPORT_BUS = "bus"


@dataclass(frozen=True)
class TransportMode:
    key: str
    label: str
    fare: int

    def fare_label(self):
        return str(self.fare)

    def insufficient_funds_dialogue(self):
        return f"I don't have enough money for the {self.label}... (Need {self.fare})"


BUS_TRANSPORT = TransportMode(
    key=TRANSPORT_BUS,
    label="bus",
    fare=20,
)

TRANSPORT_MODES = {
    BUS_TRANSPORT.key: BUS_TRANSPORT,
}


def get_transport_mode(key):
    try:
        return TRANSPORT_MODES[key]
    except KeyError as exc:
        raise ValueError(f"Unknown transport mode: {key}") from exc
