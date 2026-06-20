from __future__ import annotations

from domain.missile.factories import MissileFactory
from domain.missile.missile import Missile
from infrastructure.event_bus.event_bus import EventBus
from reality.reality import Reality
from services.velocity_tracker.velocity_tracker_service import VelocityTrackerService

event_bus = EventBus()
tracker = VelocityTrackerService(event_bus=event_bus)

update_ms = 40

def main() -> None:
    try:
        tracker.start()
        
        Reality(update_ms, True, True, event_bus=event_bus).start([
            MissileFactory.create_tamir(),
            MissileFactory.create_qassam(),
            MissileFactory.create_v2(),
        ])
    except Exception as e:
        print(e)
    finally:
        tracker.stop()


if __name__ == "__main__":
    main()
