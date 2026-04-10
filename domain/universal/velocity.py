from __future__ import annotations
import math
from dataclasses import dataclass
from .meters_per_second import MetersPerSecond

@dataclass(frozen=True, slots=True)
class Velocity:
    x: MetersPerSecond
    y: MetersPerSecond
    z: MetersPerSecond

    @property
    def total(self) -> "MetersPerSecond":
        return MetersPerSecond(
            meters_per_second=math.sqrt(
                self.x.meters_per_second**2
                + self.y.meters_per_second**2
                + self.z.meters_per_second**2
            )
        )

    @classmethod
    def zero(cls) -> "Velocity":
        return cls(
            x=MetersPerSecond(0),
            y=MetersPerSecond(0),
            z=MetersPerSecond(0)
        )
