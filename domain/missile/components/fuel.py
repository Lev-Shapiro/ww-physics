from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ...universal.kilograms_mass import KilogramMass


class FuelType(str, Enum):
    ALUMINUM_POWDER = "AL"
    HTPB = "HTPB"
    KEROSENE = "K"
    HYDROGEN = "H"


@dataclass(slots=True)
class Fuel:
    type: FuelType
    _mass: KilogramMass

    @property
    def mass(self) -> float:
        return self._mass.mass_in_kg

    def use(self, wasted_kg: float) -> None:
        self._mass = self._mass.subtract(wasted_kg)

    @classmethod
    def from_kg(cls, fuel_type: FuelType, initial_mass_in_kg: float) -> "Fuel":
        return cls(type=fuel_type, _mass=KilogramMass.from_kg(initial_mass_in_kg))
