from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Time:
    seconds: float

    @classmethod
    def from_seconds(cls, seconds: float) -> "Time":
        return cls(seconds=seconds)

    @classmethod
    def from_minutes(cls, minutes: float) -> "Time":
        return cls(seconds=minutes * 60)

    @classmethod
    def from_hours(cls, hours: float) -> "Time":
        return cls(seconds=hours * 3600)
