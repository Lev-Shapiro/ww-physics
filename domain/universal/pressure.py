from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PsiaPressure:
  psia: float
  
  @classmethod
  def from_psia(cls, psia: float) -> "PsiaPressure":
    return cls(psia=psia)