from dataclasses import dataclass

from domain.universal.temperature_kelvin import TemperatureKelvin

@dataclass(frozen=True, slots=True)
class ExhaustDto:
    molecular_weight: float  # in g/mol
    flame_temperature: TemperatureKelvin
    gamma: float  # Ratio of specific heats
