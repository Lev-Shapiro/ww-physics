from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MetersPerSecond:
    meters_per_second: float
    
    def add(self, meters_per_second: float):
        self.meters_per_second = self.meters_per_second + meters_per_second

    @classmethod
    def from_kph(cls, kph: float) -> "MetersPerSecond":
        return cls(meters_per_second=kph * 1000 / 3600)
