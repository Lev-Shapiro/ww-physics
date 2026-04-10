from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Temperature:
    kelvin: float

    @classmethod
    def from_kelvin(cls, kelvin: float) -> "Temperature":
        return cls(kelvin=kelvin)

    @classmethod
    def from_celsius(cls, celsius: float) -> "Temperature":
        return cls(kelvin=celsius + 273.15)
