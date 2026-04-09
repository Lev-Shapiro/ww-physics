from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetersPerSecond:
    meters_per_second: float

    @classmethod
    def from_mps(cls, mps: float) -> "MetersPerSecond":
        return cls(meters_per_second=mps)

    @classmethod
    def from_kph(cls, kph: float) -> "MetersPerSecond":
        return cls(meters_per_second=kph * 1000 / 3600)
