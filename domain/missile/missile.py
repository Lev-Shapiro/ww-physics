from __future__ import annotations
import uuid

from domain.missile.components.propellant_mixture import PropellantMixture
from domain.moving_object.moving_object import MovingObject
from domain.universal.constants import EARTH_GRAVITY, GAS_CONSTANT, MOLAR_MASS, SEA_LEVEL_PRESSURE, SEA_LEVEL_STANDARD_TEMPERATURE, TEMPEARATURE_LAPSE_RATE
from domain.universal.coords import Coords
from domain.universal.efficiency_factor import EfficiencyFactor
from domain.universal.pressure import Pressure
from domain.universal.velocity import Velocity
from domain.universal.angle3d import Angle3D
from .missile_structure import MissileStructure
from enum import Enum

class MissileState(str, Enum):
    BOOSTING = "BOOSTING"
    FLYING = "FLYING"
    LANDED = "LANDED"
    EXPLODED = "EXPLODED"
    
class Missile(MovingObject):
    id: str
    name: str 
    propellant: PropellantMixture 
    structure: MissileStructure 
    efficiency_factor: EfficiencyFactor
   
    # Kinematic parameters
    coords: Coords
    velocity: Velocity
    
    start_angle: Angle3D
    
    def __init__(self, name: str, propellant: PropellantMixture, structure: MissileStructure, efficiency: EfficiencyFactor, coords: Coords, velocity: Velocity, start_angle: Angle3D):
        self.id = uuid.uuid4()
        self.name = name
        self.propellant = propellant
        self.structure = structure
        self.efficiency_factor = efficiency
        self.coords = coords
        self.velocity = velocity
        self.start_angle = start_angle
        
    @property
    def mass(self) -> float:
        return self.propellant.mass + self.structure.dry_mass
    
    @property
    def exit_pressure(self) -> Pressure:    
        alt = max(0.0, float(self.coords.y))
        max_alt_m = SEA_LEVEL_STANDARD_TEMPERATURE / TEMPEARATURE_LAPSE_RATE
        effective_alt = min(alt, max_alt_m * 0.999)

        temp_delta = (TEMPEARATURE_LAPSE_RATE * effective_alt) / SEA_LEVEL_STANDARD_TEMPERATURE
        exp = (MOLAR_MASS * EARTH_GRAVITY) / (GAS_CONSTANT * TEMPEARATURE_LAPSE_RATE)
        
        return Pressure.from_pascals(
            (SEA_LEVEL_PRESSURE.pascals)*(1-temp_delta)**exp
        )
        
    @property
    def state(self) -> MissileState:
        return MissileState.BOOSTING if self.propellant.mass > 0 else MissileState.FLYING if self.coords.y > 2 else MissileState.LANDED