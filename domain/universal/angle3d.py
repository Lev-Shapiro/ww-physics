from dataclasses import dataclass
import math

@dataclass(frozen=True, slots=True)
class Angle3D:
    xy: float
    xz: float

    @classmethod
    def from_radians(cls, xy: float, xz: float) -> "Angle3D":
        return cls(xy=xy, xz=xz)
    
    @classmethod
    def from_degrees(cls, xy: float, xz: float) -> "Angle3D":
        xydeg = xy / 180 * math.pi
        xzdeg = xz / 180 * math.pi
        
        return cls.from_radians(xydeg, xzdeg)