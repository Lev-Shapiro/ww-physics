import math

from domain.universal.temperature import Temperature
from .formula import Formula
from ..universal.constants import GAS_CONSTANT, EARTH_GRAVITY
from ..universal.efficiency_factor import EfficiencyFactor

class ExhaustVelocityThermochemicalFormula(Formula):
    @staticmethod
    def calculate(
        molecular_weight: float,
        flame_temperature: Temperature,
        gamma: float,
        chamber_pressure_ratio: float = 1000.0,
        efficiency: EfficiencyFactor | None = None
    ) -> float:
        """
        Calculate the ideal thermochemical exhaust velocity in m/s,
        optionally adjusted by a real-world efficiency factor.

        v_e = sqrt( (2 * k / (k - 1)) * (R * Tc / M) * [1 - (pe / pc) ** ((k - 1) / k)] )
        where (pe / pc) is the inverse of chamber_pressure_ratio.

        chamber_pressure_ratio: float - the ratio of chamber pressure to exit pressure (pc / pe); default 1000.0
        efficiency: EfficiencyFactor - optional factor representing real-world losses

        Returns: float (exhaust velocity in m/s)
        """

        T = flame_temperature.kelvin
        M = molecular_weight / 1000.0  # convert g/mol to kg/mol

        # Theoretical exhaust velocity (v_e) [m/s]
        term1 = (2 * gamma * GAS_CONSTANT * T) / ((gamma - 1) * M)
        term2 = 1 - (1 / chamber_pressure_ratio) ** ((gamma - 1) / gamma)
        v_e = math.sqrt(term1 * term2)

        # Apply real-world efficiency if provided
        if efficiency is not None:
            v_e *= efficiency.value

        return v_e

