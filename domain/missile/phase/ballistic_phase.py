from __future__ import annotations

from domain.missile.missile import Missile

class BallisticMissilePhase:
    """Coast / ballistic flight after thrust ends; holds the missile under simulation."""

    def __init__(self, missile: Missile) -> None:
        self._missile = missile
