from __future__ import annotations

from domain.missile.factories import MissileFactory
from domain.missile.missile import Missile
from infrastructure.event_bus.event_bus import EventBus
from reality.reality import Reality
from services.velocity_tracker.velocity_tracker_service import VelocityTrackerService


def main() -> None:
    simulations = [
        MissileFactory.create_tamir(),
        # MissileFactory.create_qassam(),
        # MissileFactory.create_v2(),
    ]

    for missile in simulations:
        run_simulation(missile)


event_bus = EventBus()
tracker = VelocityTrackerService(event_bus=event_bus)

def run_simulation(missile: Missile) -> None:
    update_ms = 5

    tracker.start()
    try:
        Reality(update_ms, True, True, event_bus=event_bus).start([missile])
    finally:
        tracker.stop()


if __name__ == "__main__":
    main()
