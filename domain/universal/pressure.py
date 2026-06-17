from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Pressure:
  psia: float
  
  @property
  def pascals(self) -> float:
    return self.psia * 6895
  
  @classmethod
  def from_pascals(self, pascals: float) -> Pressure:
    return Pressure(psia=pascals / 6895)