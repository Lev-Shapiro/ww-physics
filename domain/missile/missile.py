from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from domain.missile.components.solid_propellant import SolidPropellantMixture

@dataclass(frozen=True, slots=True)
class Missile(ABC):
    name: str
    propellant: SolidPropellantMixture
    