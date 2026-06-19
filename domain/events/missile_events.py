from __future__ import annotations
from dataclasses import dataclass

from domain.missile.missile import MissileState
from domain.universal.coords import Coords
from domain.universal.velocity import Velocity

@dataclass(frozen=True, slots=True)
class MissileTickEvent:
    """Emitted by the simulation engine on every physics tick for a missile in flight."""

    missile_id: str
    missile_name: str
    velocity_vector: Velocity
    coords: Coords
    elapsed_ms: float
    state: MissileState
    terminal_speed: float
    fuel_pct: float

    @classmethod
    def build(cls, id: str, name: str, velocity: Velocity, coords: Coords, state: MissileState, elapsed_ms: float, terminal_speed: float, fuel_pct: float) -> MissileTickEvent:
        return cls(
            missile_id=id,
            missile_name=name,
            velocity_vector=velocity,
            coords=coords,
            elapsed_ms=elapsed_ms,
            state=state,
            terminal_speed=terminal_speed,
            fuel_pct=fuel_pct,
        )