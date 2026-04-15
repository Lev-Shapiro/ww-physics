from __future__ import annotations

from domain.missile.missile import Missile
from domain.universal.normalized_velocity import NormalizedVelocity

class BallisticMissilePhase:
    """Coast / ballistic flight after thrust ends; holds the missile under simulation."""

    def __init__(self, missile: Missile, trajectory: NormalizedVelocity) -> None:
        self._missile = missile

    
