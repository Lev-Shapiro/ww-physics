from __future__ import annotations

from dataclasses import dataclass

from domain.missile.components.propellant_mixture import PropellantMixture
from domain.universal.coords import Coords
from domain.universal.efficiency_factor import EfficiencyFactor
from domain.universal.mass import Mass
from domain.universal.pressure import PsiaPressure
from domain.universal.velocity import Velocity

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

class Missile:
    name: str 
    propellant: PropellantMixture 
    structure: MissileStructure 
    efficiency_factor: EfficiencyFactor
   
    # Kinematic parameters
    coords: Coords
    velocity: Velocity
    
    def __init__(self, name: str, propellant: PropellantMixture, structure: MissileStructure, efficiency: EfficiencyFactor, coords: Coords, velocity: Velocity):
        self.name = name
        self.propellant = propellant
        self.structure = structure
        self.efficiency_factor = efficiency
        self.coords = coords
        self.velocity = velocity
        
    @property
    def mass(self) -> float:
        return self.propellant.mass + self.structure.dry_mass
    
    @property
    def exit_pressure(self):
        # TODO: Shall be dependent on the altitude
        return PsiaPressure(psia=14.7)