from __future__ import annotations
import math

from domain.formulas.exhaust_velocity import ExhaustVelocityThermochemicalFormula
from domain.missile.missile import Missile
from domain.universal.constants import EARTH_GRAVITY
from domain.universal.pressure import PsiaPressure
from domain.universal.time import Time
from nasa_cea.cea_apcp import CEAAPCP
from nasa_cea.cea_calculator import CEACalculator
from nasa_cea.cea_nepe import CEANEPE

class BoostingMissilePhase:
    """Powered ascent; transitions from or into ballistic behavior via the ballistic phase context."""

    missile: Missile
    calculator: CEACalculator
    
    def __init__(self, missile: Missile, cea_calculator: CEACalculator):
        self.missile = missile
        self.calculator = cea_calculator
    
    @property
    def chamber_density(self):
      return self.calculator.chamber_density
    
    @property
    def chamber_pressure(self):
      return self.calculator.chamber_pressure
         
    @property
    def burn_phase_ratio(self):
      return self.missile.structure.burning_surface_area / self.missile.structure.nozzle_throat_area
    
    @property
    def inout_pressure_ratio(self):
      return self.chamber_pressure.psia / self.missile.exit_pressure.psia
    
    @property
    def burn_rate_coefficient(self):
      return 0.01
    
    @property
    def pressure_exponent(self):
      return 0.5
    
    @property
    def burn_rate(self):
      return self.burn_rate_coefficient * (self.chamber_pressure.psia ** self.pressure_exponent)
    
    @property
    def mass_flow_rate(self):
      return self.chamber_density * self.missile.structure.burning_surface_area * self.burn_rate
    
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
        
    def __burn(self, time_elapsed: Time) -> bool:
      if self.missile.propellant.mass <= 0:
          return True

      relative_mass_flow_rate = self.mass_flow_rate * time_elapsed.seconds
      
      if relative_mass_flow_rate >= self.missile.propellant.mass:
          relative_mass_flow_rate = self.missile.propellant.mass
      
      initial_mass = self.missile.mass
      self.missile.propellant.burn(relative_mass_flow_rate)
      final_mass = self.missile.mass
            
      if initial_mass > final_mass:
          velocity_change = self.exhaust_velocity * math.log(
            initial_mass / final_mass
          )
          self.missile.velocity.z.add(velocity_change)
      else:
        return True
          
      return False
            
    def burn(self):
      time_step = Time.from_seconds(0.1) # 100ms
      while not self.__burn(time_step):
          pass

    @staticmethod
    def from_apcp(missile: Missile, chamber_pressure: PsiaPressure = PsiaPressure(psia=1000)) -> BoostingMissilePhase:
        cea_calculator = CEAAPCP(missile.propellant, chamber_pressure)
        return BoostingMissilePhase(missile=missile, cea_calculator=cea_calculator)

    @staticmethod
    def from_nepe(missile: Missile, chamber_pressure: PsiaPressure = PsiaPressure(psia=1000)) -> BoostingMissilePhase:
        cea_calculator = CEANEPE(missile.propellant, chamber_pressure)
        return BoostingMissilePhase(missile=missile, cea_calculator=cea_calculator)
