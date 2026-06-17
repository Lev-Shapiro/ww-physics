from __future__ import annotations
import math
from dataclasses import dataclass
from domain.universal.velocity import Velocity

@dataclass(frozen=True, slots=True)
class NormalizedVelocity:
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        if math.sqrt(x**2 + y**2 + z**2) != 1:
            raise Exception("Total normalized vector magnitude must be 1")
        
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_velocity(cls, velocity: Velocity) -> "NormalizedVelocity":
        total = velocity.total.meters_per_second

        return NormalizedVelocity(
            x=velocity.x.meters_per_second / total,
            y=velocity.y.meters_per_second / total,
            z=velocity.z.meters_per_second / total
        )