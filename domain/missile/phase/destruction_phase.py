from __future__ import annotations

from domain.missile.missile import Missile


class DestructionMissilePhase:
    """Terminal / breakup phase; references the missile being destroyed or fragmented."""

    def __init__(self, missile: Missile) -> None:
        self._missile = missile
