from __future__ import annotations

from domain.missile.components.propellant_mixture import PropellantMixture
from domain.moving_object.moving_object import MovingObject
from domain.universal.constants import EARTH_GRAVITY, GAS_CONSTANT, SEA_LEVEL_PRESSURE
from domain.universal.coords import Coords
from domain.universal.efficiency_factor import EfficiencyFactor
from domain.universal.pressure import Pressure
from domain.universal.velocity import Velocity
from .missile_structure import MissileStructure

class Missile(MovingObject):
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
    def exit_pressure(self) -> Pressure:
        TEMPEARATURE_LAPSE_RATE = 0.0065 # [K/m]
        SEA_LEVEL_STANDARD_TEMPERATURE=288.15 # [K]
        MOLAR_MASS = 0.0289644 # [kg/mol]
    
        alt = max(0.0, float(self.coords.y))
        max_alt_m = SEA_LEVEL_STANDARD_TEMPERATURE / TEMPEARATURE_LAPSE_RATE
        effective_alt = min(alt, max_alt_m * 0.999)

        temp_delta = (TEMPEARATURE_LAPSE_RATE * effective_alt) / SEA_LEVEL_STANDARD_TEMPERATURE
        exp = (MOLAR_MASS * EARTH_GRAVITY) / (GAS_CONSTANT * TEMPEARATURE_LAPSE_RATE)
        
        # TODO: Shall be dependent on the altitude
        return Pressure.from_pascals(
            (SEA_LEVEL_PRESSURE.pascals)*(1-temp_delta)**exp
        )
    
        # Sea-level (easiest way)
        # return Pressure(psia=14.7)