from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TemperatureKelvin:
    kelvin: float

    @classmethod
    def from_kelvin(cls, kelvin: float) -> "TemperatureKelvin":
        return cls(kelvin=kelvin)

    @classmethod
    def from_celsius(cls, celsius: float) -> "TemperatureKelvin":
        return cls(kelvin=celsius + 273.15)
