import time

from domain.missile.components.propellant_type import PropellantType
from domain.missile.missile import Missile
from domain.missile.phase.boosting_phase import BoostingMissilePhase
from domain.moving_object.moving_object import MovingObject
from domain.universal.constants import EARTH_GRAVITY
from domain.universal.time import Time

class Reality:
  __stop: bool = False
  __update_ms: int
  
  with_gravity: bool
  with_air_resistance: bool
  
  moving_objects: list[MovingObject] = []
  explode_objects: list[MovingObject] = []
  
  boosting_phases: list[BoostingMissilePhase] = []

    
  def __init__(self, update_ms: int, with_gravity: bool, with_air_resistance: bool):
    self.__update_ms = update_ms
    self.with_gravity = with_gravity
    self.with_air_resistance = with_air_resistance
    
  def __update(self):
    r = Time.from_seconds(self.__update_ms / 1000)
    
    for boosting_phase in self.boosting_phases:
      velocity_change = boosting_phase.exhaust(r)
      
      if velocity_change == 0:
        self.boosting_phases.remove(boosting_phase)
      
    for moving_object in self.moving_objects:      
      moving_object.coords.add_velocity(
        moving_object.velocity, 
        r
      )
      
      if moving_object.coords.y >= 0:
        if self.with_gravity:
          moving_object.velocity.y.add(EARTH_GRAVITY * r.seconds * -1)
      else:
        print(f"Speed: {moving_object.velocity.total.meters_per_second:.2f} m/s")
        print(f"Coords: {moving_object.coords.x:.2f}, {moving_object.coords.y:.2f}, {moving_object.coords.z:.2f}")
        
        self.moving_objects.remove(moving_object)
        self.explode_objects.append(moving_object)
      
  def load_missiles_to_simulation(self, missiles: list[Missile]):
    for missile in missiles:
      if missile.propellant.type is PropellantType.NEPE:
        self.boosting_phases.append(BoostingMissilePhase.from_nepe(missile))
      elif missile.propellant.type is PropellantType.KNSU:
        self.boosting_phases.append(BoostingMissilePhase.from_knsu(missile))
      elif missile.propellant.type is PropellantType.LIQUID:
        self.boosting_phases.append(BoostingMissilePhase.from_liquid(missile))
      elif missile.propellant.type is PropellantType.APCP:
        self.boosting_phases.append(BoostingMissilePhase.from_apcp(missile))
      else:
        raise ValueError(f"Unknown propellant type: {missile.propellant.type}")
      
      self.moving_objects.append(missile)
      
  def start(self, missiles: list[Missile]):
    self.load_missiles_to_simulation(missiles)
      
    while not self.__stop and len(self.moving_objects) > 0:
      self.__update()
      
      # time.sleep(self.__update_ms / 1000)
      
    self.terminate()
      
  def terminate(self):
    self.__stop = True