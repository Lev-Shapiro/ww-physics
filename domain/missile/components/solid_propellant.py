from __future__ import annotations

from dataclasses import dataclass

from .fuel import Fuel
from .oxidizer import Oxidizer


@dataclass(frozen=True, slots=True)
class SolidPropellantMixture:
    fuels: tuple[Fuel, ...]
    oxidizers: tuple[Oxidizer, ...]

    @property
    def mass(self) -> float:
        return sum(f.mass for f in self.fuels) + sum(o.mass for o in self.oxidizers)

    @property
    def fuel_mass(self) -> float:
        return sum(f.mass for f in self.fuels)

    @property
    def oxidizer_mass(self) -> float:
        return sum(o.mass for o in self.oxidizers)

    @property
    def ratio(self) -> float:
        ox_mass = self.oxidizer_mass
        return self.fuel_mass / ox_mass if ox_mass > 0 else float('inf')
    
    def use(self, relative_mass_flow_rate):
        missile_mass = self.mass
        
        for fuel in self.fuels:
            fuel.use(fuel.mass / missile_mass * relative_mass_flow_rate)
        
        for oxidizer in self.oxidizers:
            oxidizer.use(oxidizer.mass / missile_mass * relative_mass_flow_rate)

    @classmethod
    def mix(cls, fuels: tuple[Fuel, ...], oxidizers: tuple[Oxidizer, ...]) -> "SolidPropellantMixture":
        return cls(fuels=fuels, oxidizers=oxidizers)
