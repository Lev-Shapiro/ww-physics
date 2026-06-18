from __future__ import annotations
import math
from dataclasses import dataclass

from domain.universal.angle3d import Angle3D
from .meters_per_second import MetersPerSecond

@dataclass(frozen=False, slots=True)
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
                
    def add_tangential_velocity(self, delta_v: MetersPerSecond, thrust_angle: Angle3D):
        """Add a delta-v increment along the fixed thrust axis defined by thrust_angle."""
        dv = delta_v.meters_per_second
        self.x.add(dv * math.sin(thrust_angle.xy) * math.cos(thrust_angle.xz))
        self.y.add(dv * math.sin(thrust_angle.xz))
        self.z.add(dv * math.cos(thrust_angle.xy) * math.cos(thrust_angle.xz))

    @classmethod
    def zero(cls) -> "Velocity":
        return cls(
            x=MetersPerSecond(0),
            y=MetersPerSecond(0),
            z=MetersPerSecond(0)
        )
