from abc import ABC
from domain.universal.velocity import Velocity
from domain.universal.coords import Coords
from domain.universal.mass import Mass

class MovingObject(ABC):
  mass: Mass
  coords: Coords
  velocity: Velocity
  is_explosive: bool