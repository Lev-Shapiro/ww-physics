from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Coords:
    x: float
    y: float
    z: float

    @classmethod
    def xyz(cls, x: float, y: float, z: float) -> "Coords":
        return cls(x=x, y=y, z=z)

    @classmethod
    def zero(cls) -> "Coords":
        return cls(x=0.0, y=0.0, z=0.0)
