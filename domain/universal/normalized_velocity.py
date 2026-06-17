from __future__ import annotations
import math
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class NormalizedVelocity:
    x: int
    y: int
    z: int

    __init__(self, int x, int y, int z):
        if math.sqrt(x**2 + y**2 + z**2) != 1:
            raise Exception("Total normalized vector magnitude must be 1")
        
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_velocity(cls, Velocity velocity) -> "NormalizedVelocity":
        total = velocity.total

        return NormalizedVelocity(
            x=velocity.x.meters_per_second / total,
            y=velocity.y.meters_per_second / total,
            z=velocity.z.meters_per_second / total
        )