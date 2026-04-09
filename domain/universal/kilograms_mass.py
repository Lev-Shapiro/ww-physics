from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KilogramMass:
    mass_in_kg: float

    def subtract(self, wasted_kg: float) -> "KilogramMass":
        return KilogramMass(self.mass_in_kg - wasted_kg)

    @classmethod
    def from_kg(cls, mass_in_kg: float) -> "KilogramMass":
        return cls(mass_in_kg=mass_in_kg)

    @classmethod
    def from_short_ton(cls, mass_in_short_ton: float) -> "KilogramMass":
        return cls(mass_in_kg=mass_in_short_ton * 907.18474)

    @classmethod
    def from_long_ton(cls, mass_in_long_ton: float) -> "KilogramMass":
        return cls(mass_in_kg=mass_in_long_ton * 1016.0469088)
