from __future__ import annotations

from dataclasses import dataclass

from domain.universal.pressure import PsiaPressure

from .fuel import Fuel
from .oxidizer import Oxidizer
from .propellant_type import PropellantType


@dataclass(frozen=True, slots=True)
class PropellantMixture:
    type: PropellantType
    fuels: tuple[Fuel, ...]
    oxidizers: tuple[Oxidizer, ...]
    chamber_pressure: PsiaPressure
    
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

    def burn(self, relative_mass_flow_rate: float):        
        relative_mass_ratio = relative_mass_flow_rate / self.mass
        
        for fuel in self.fuels:
            fuel.use(fuel.mass * relative_mass_ratio)
        
        for oxidizer in self.oxidizers:
            oxidizer.use(oxidizer.mass * relative_mass_ratio)

    @classmethod
    def mix(cls, type: PropellantType, fuels: tuple[Fuel, ...], oxidizers: tuple[Oxidizer, ...], chamber_pressure: PsiaPressure) -> "PropellantMixture":
        return cls(type=type, fuels=fuels, oxidizers=oxidizers, chamber_pressure=chamber_pressure)