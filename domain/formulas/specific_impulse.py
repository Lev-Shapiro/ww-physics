import math
from .formula import Formula
from ..dto.exhaust_dto import ExhaustDto
from ..universal.constants import GAS_CONSTANT, EARTH_GRAVITY
from ..universal.efficiency_factor import EfficiencyFactor

class SpecificImpulseThermochemicalFormula(Formula):
    @staticmethod
    def calculate(
        exhaust: ExhaustDto, 
        chamber_pressure_ratio: float = 1000.0,
        efficiency: EfficiencyFactor | None = None
    ) -> float:
        """
        Calculate the ideal thermochemical specific impulse (Isp) in seconds,
        optionally adjusted by a real-world efficiency factor.

        Isp = (1 / g0) * sqrt( (2 * k / (k - 1)) * (R * Tc / M) * [1 - (pe / pc) ** ((k - 1) / k)] )
        where (pe / pc) is the inverse of chamber_pressure_ratio.

        exhaust: ExhaustDto - properties of exhaust gases
        chamber_pressure_ratio: float - the ratio of chamber pressure to exit pressure (pc / pe); default 1000.0
        efficiency: EfficiencyFactor - optional factor representing real-world losses

        Returns: float (Isp in seconds)
        """

        gamma = exhaust.gamma
        T = exhaust.flame_temperature.kelvin
        M = exhaust.molecular_weight / 1000.0  # convert g/mol to kg/mol

        # Theoretical exhaust velocity (v_e) [m/s]
        term1 = (2 * gamma * GAS_CONSTANT * T) / ((gamma - 1) * M)
        term2 = 1 - (1 / chamber_pressure_ratio) ** ((gamma - 1) / gamma)
        v_e = math.sqrt(term1 * term2)

        # Ideal specific impulse [s]
        Isp = v_e / EARTH_GRAVITY

        # Apply real-world efficiency if provided
        if efficiency is not None:
            Isp *= efficiency.value

        return Isp