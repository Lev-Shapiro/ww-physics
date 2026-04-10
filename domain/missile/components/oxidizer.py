from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from domain.universal.mass import Mass


class OxidizerType(str, Enum):
    AMMONIUM_PERCHLORATE = "AP"


@dataclass(slots=True)
class Oxidizer:
    type: OxidizerType
    _mass: Mass

    @property
    def mass(self) -> float:
        return self._mass.mass_in_kg

    def use(self, wasted_kg: float) -> None:
        self._mass = self._mass.subtract(wasted_kg)

    @classmethod
    def from_kg(cls, oxidizer_type: OxidizerType, initial_mass_in_kg: float) -> "Oxidizer":
        return cls(type=oxidizer_type, _mass=Mass.from_kg(initial_mass_in_kg))
