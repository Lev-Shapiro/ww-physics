from dataclasses import dataclass

from domain.universal.temperature import Temperature

@dataclass(frozen=True, slots=True)
class ExhaustDto:
    molecular_weight: float  # in g/mol
    flame_temperature: Temperature
    gamma: float  # Ratio of specific heats
    characteristic_velocity: float  # in m/s (c*)