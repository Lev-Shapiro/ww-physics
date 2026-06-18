from __future__ import annotations
import math

from domain.formulas.exhaust_velocity import ExhaustVelocityThermochemicalFormula
from domain.missile.missile import Missile
from domain.universal.constants import EARTH_GRAVITY
from domain.universal.meters_per_second import MetersPerSecond
from domain.universal.time import Time
from nasa_cea.cea_apcp import CEAAPCP
from nasa_cea.cea_calculator import CEACalculator
from nasa_cea.cea_knsu import CEAKNSU
from nasa_cea.cea_liquid import CEALiquid
from nasa_cea.cea_nepe import CEANEPE

class BoostingMissilePhase:
    """Powered ascent; transitions from or into ballistic behavior via the ballistic phase context."""

    missile: Missile
    calculator: CEACalculator
    
    def __init__(self, missile: Missile, cea_calculator: CEACalculator):
        self.missile = missile
        self.calculator = cea_calculator
        
    @property
    def chamber_pressure(self):
      return self.calculator.chamber_pressure
         
    @property
    def inout_pressure_ratio(self):
      return self.chamber_pressure.psia / self.missile.exit_pressure.psia
    
    @property
    def mass_flow_rate(self):
      return (self.chamber_pressure.pascals * self.missile.structure.nozzle_throat_area) / self.calculator.characteristic_velocity
    
    @property
    def exhaust_velocity(self):
      return ExhaustVelocityThermochemicalFormula.calculate(
            molecular_weight=self.calculator.molecular_weight,
            flame_temperature=self.calculator.flame_temperature,
            gamma=self.calculator.gamma,
            chamber_pressure_ratio=self.inout_pressure_ratio,
            efficiency=self.missile.efficiency_factor
        )
    
    @property
    def specific_impulse(self):
        return self.exhaust_velocity / EARTH_GRAVITY
        
    # Output: Velocity change in meters per second
    def exhaust(self, time: Time) -> float:
      if self.missile.propellant.mass <= 0:
          return 0
        
      relative_mass_flow_rate = self.mass_flow_rate * time.seconds
      
      if relative_mass_flow_rate >= self.missile.propellant.mass:
          relative_mass_flow_rate = self.missile.propellant.mass
      
      initial_mass = self.missile.mass
      self.missile.propellant.burn(relative_mass_flow_rate)
      final_mass = self.missile.mass
            
      if initial_mass > final_mass:
          velocity_change = MetersPerSecond.from_meters_per_second(
            self.exhaust_velocity * math.log(
              initial_mass / final_mass
            )
          )
          
          self.missile.velocity.add_tangential_velocity(velocity_change, self.missile.start_angle)
          
      return velocity_change

    @staticmethod
    def from_apcp(missile: Missile) -> BoostingMissilePhase:
        cea_calculator = CEAAPCP(missile.propellant)
        return BoostingMissilePhase(missile=missile, cea_calculator=cea_calculator)

    @staticmethod
    def from_nepe(missile: Missile) -> BoostingMissilePhase:
        cea_calculator = CEANEPE(missile.propellant)
        return BoostingMissilePhase(missile=missile, cea_calculator=cea_calculator)

    @staticmethod
    def from_knsu(missile: Missile) -> BoostingMissilePhase:
        cea_calculator = CEAKNSU(missile.propellant)
        return BoostingMissilePhase(missile=missile, cea_calculator=cea_calculator)

    @staticmethod
    def from_liquid(missile: Missile) -> BoostingMissilePhase:
        cea_calculator = CEALiquid(missile.propellant)
        return BoostingMissilePhase(missile=missile, cea_calculator=cea_calculator)
