from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from ..universal.coords import Coords
from ..universal.kilograms_mass import KilogramMass
from ..universal.speed_3d import SpeedVector


@dataclass(frozen=True, slots=True)
class Missile(ABC):
    name: str
    mass: KilogramMass
    coords: Coords
    speed: SpeedVector
