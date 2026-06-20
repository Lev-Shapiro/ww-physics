from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from domain.universal.mass import Mass


class OxidizerType(str, Enum):
    AMMONIUM_PERCHLORATE = "AP"
    POTASSIUM_NITRATE = "KNO3"
    LIQUID_OXYGEN = "LOX"


@dataclass(slots=True)
class Oxidizer:
    type: OxidizerType
    _mass: Mass
    _initial_mass: Mass

    @property
    def mass(self) -> float:
        return self._mass.mass_in_kg

    @property
    def initial_mass(self) -> float:
        return self._initial_mass.mass_in_kg
    
    def use(self, wasted_kg: float) -> None:
        self._mass = self._mass.subtract(wasted_kg)

    @classmethod
    def from_kg(cls, oxidizer_type: OxidizerType, mass_in_kg: float) -> "Oxidizer":
        if mass_in_kg < 0:
            raise ValueError("Oxidizer cannot be negative")
        
        mass = Mass.from_kg(mass_in_kg)
        return cls(type=oxidizer_type, _mass=mass, _initial_mass=mass)
