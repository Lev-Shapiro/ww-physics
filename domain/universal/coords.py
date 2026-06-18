from __future__ import annotations

from dataclasses import dataclass

from domain.universal.time import Time
from domain.universal.velocity import Velocity


@dataclass(frozen=False, slots=True)
class Coords:
    # in meters
    x: float
    y: float
    z: float
    
    def add_velocity(self, velocity: Velocity, time_elapsed: Time):
        self.x = self.x + velocity.x.meters_per_second * time_elapsed.seconds
        self.y = self.y + velocity.y.meters_per_second * time_elapsed.seconds
        self.z = self.z + velocity.z.meters_per_second * time_elapsed.seconds
    
    @classmethod
    def xyz(cls, x: float, y: float, z: float) -> "Coords":
        return cls(x=x, y=y, z=z)

    @classmethod
    def zero(cls) -> "Coords":
        return cls(x=0.0, y=0.0, z=0.0)
