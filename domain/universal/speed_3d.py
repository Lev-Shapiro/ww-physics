from __future__ import annotations

import math
from dataclasses import dataclass

from .meters_per_second import MetersPerSecond


@dataclass(frozen=True, slots=True)
class SpeedVector:
    x: MetersPerSecond
    y: MetersPerSecond
    z: MetersPerSecond

    @property
    def total(self) -> MetersPerSecond:
        return MetersPerSecond.from_mps(
            math.sqrt(
                self.x.meters_per_second**2
                + self.y.meters_per_second**2
                + self.z.meters_per_second**2
            )
        )
