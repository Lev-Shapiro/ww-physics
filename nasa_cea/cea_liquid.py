from __future__ import annotations

from domain.missile.components.propellant_mixture import PropellantMixture
from domain.missile.components.propellant_type import PropellantType
from domain.universal.pressure import PsiaPressure
from nasa_cea.cea_calculator import CEACalculator

from rocketcea.cea_obj import CEA_Obj


def _liquid_component_mass_fractions(mixture: PropellantMixture) -> tuple[float, float]:
    """Return mass fractions (0–100) for Ethanol and LOX for a validated liquid mixture."""
    if mixture.type is not PropellantType.LIQUID:
        raise ValueError("CEA Liquid calculator requires PropellantType.LIQUID.")

    total = mixture.mass
    if total <= 0:
        raise ValueError("Propellant mixture must have positive total mass.")

    if not mixture.fuels or not mixture.oxidizers:
        raise ValueError("Liquid mixture must include at least one fuel and one oxidizer.")

    # Assume first fuel is ethanol, first oxidizer is LOX
    ethanol_mass = mixture.fuels[0].mass
    lox_mass = mixture.oxidizers[0].mass

    ethanol_pct = (ethanol_mass / total) * 100
    lox_pct = (lox_mass / total) * 100

    return ethanol_pct, lox_pct


class CEALiquid(CEACalculator):
    """Liquid propellant thermodynamic model from RocketCEA, driven by a domain PropellantMixture."""

    _mixture: PropellantMixture

    def __init__(self, mixture: PropellantMixture) -> None:
        self._mixture = mixture
        super().__init__(mixture.chamber_pressure)

    def _build_cea_obj(self) -> CEA_Obj:
        return CEA_Obj(propName='Ethanol', oxName='LOX')

    @property
    def mixture(self) -> PropellantMixture:
        return self._mixture