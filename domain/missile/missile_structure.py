from __future__ import annotations
from dataclasses import dataclass
from domain.universal.mass import Mass

@dataclass(frozen=True, slots=True)
class MissileStructure:
    burning_surface_area: float
    nozzle_throat_area: float
    casing_mass: Mass
    nozzle_mass: Mass
    electronics_mass: Mass
    payload_mass: Mass
    structural_mass: Mass
    
    @property
    def dry_mass(self) -> float:
        return (
            self.casing_mass.mass_in_kg +
            self.nozzle_mass.mass_in_kg +
            self.electronics_mass.mass_in_kg +
            self.payload_mass.mass_in_kg +
            self.structural_mass.mass_in_kg
        )