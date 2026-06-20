from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from domain.universal.mass import Mass


class FuelType(str, Enum):
    ALUMINUM_POWDER = "AL"
    HTPB = "HTPB"
    KEROSENE = "K"
    HYDROGEN = "H"
    HMX = "HMX"
    BTTN = "BTTN"
    SUGAR = "SUGAR"
    ETHANOL = "ETHANOL"
    WATER = "WATER"
    METHANE = "CH4"


@dataclass(slots=True)
class Fuel:
    type: FuelType
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
    def from_kg(cls, fuel_type: FuelType, mass_in_kg: float) -> "Fuel":
        if mass_in_kg < 0:
            raise ValueError("Fuel cannot be negative")
        
        mass = Mass.from_kg(mass_in_kg)
        return cls(type=fuel_type, _mass=mass, _initial_mass=mass)
