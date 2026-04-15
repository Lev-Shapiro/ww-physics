from __future__ import annotations

from domain.missile.components.fuel import FuelType
from domain.missile.components.oxidizer import OxidizerType
from domain.missile.components.propellant_mixture import PropellantMixture
from domain.missile.components.propellant_type import PropellantType
from nasa_cea.cea_calculator import CEACalculator

from rocketcea.cea_obj import CEA_Obj, add_new_propellant


def _knsu_component_mass_fractions(mixture: PropellantMixture) -> tuple[float, float]:
    """Return mass fractions (0–100) for Sugar and Potassium Nitrate for a KNSU mixture."""
    if mixture.type is not PropellantType.KNSU:
        raise ValueError("CEA KNSU calculator requires PropellantType.KNSU.")

    total = mixture.mass
    if total <= 0:
        raise ValueError("Propellant mixture must have positive total mass.")

    if not mixture.oxidizers:
        raise ValueError("KNSU mixture must include at least one oxidizer (potassium nitrate).")

    unsupported_ox = [o for o in mixture.oxidizers if o.type is not OxidizerType.POTASSIUM_NITRATE]
    if unsupported_ox:
        raise ValueError("KNSU RocketCEA model only supports potassium nitrate as oxidizer.")

    if not mixture.fuels:
        raise ValueError("KNSU mixture must include fuel (sugar).")

    allowed_fuels = frozenset({FuelType.SUGAR})
    bad_fuels = [f for f in mixture.fuels if f.type not in allowed_fuels]
    if bad_fuels:
        raise ValueError(
            "KNSU RocketCEA model only supports sugar fuel; "
            f"got: {sorted({f.type.value for f in bad_fuels})}"
        )

    sugar_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.SUGAR)
    kno3_mass = sum(o.mass for o in mixture.oxidizers)

    if sugar_mass <= 0 or kno3_mass <= 0:
        raise ValueError(
            "KNSU mixture must have positive mass for sugar and potassium nitrate."
        )

    sugar_pct = (sugar_mass / total) * 100.0
    kno3_pct = (kno3_mass / total) * 100.0
    return sugar_pct, kno3_pct


class CEAKNSU(CEACalculator):
    """KNSU (Sugar/KNO3) thermodynamic model from RocketCEA."""

    _mixture: PropellantMixture

    def __init__(self, mixture: PropellantMixture) -> None:
        self._mixture = mixture
        super().__init__(chamber_pressure=mixture.chamber_pressure)

    @property
    def mixture(self) -> PropellantMixture:
        return self._mixture

    def _build_cea_obj(self) -> CEA_Obj:
        sugar_pct, kno3_pct = _knsu_component_mass_fractions(self._mixture)

        propellant_name = f"KNSU_{sugar_pct:.4f}_{kno3_pct:.4f}".replace(".", "_")
        
        # Sucrose C12H22O11
        # KNO3
        card = f"""
oxidizer KNO3(L)  K 1 N 1 O 3     wt%={kno3_pct}
h,cal=-117700.0 t(k)=298.15 rho=2.109
fuel Sucrose      C 12 H 22 O 11  wt%={sugar_pct}
h,cal=-531000.0 t(k)=298.15 rho=1.587
"""
        try:
            add_new_propellant(propellant_name, card)
        except Exception:
            pass

        return CEA_Obj(propName=propellant_name)
