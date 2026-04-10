from __future__ import annotations

from domain.missile.components.fuel import FuelType
from domain.missile.components.oxidizer import OxidizerType
from domain.missile.components.solid_propellant_mixture import SolidPropellantMixture
from domain.missile.components.solid_propellant_type import SolidPropellantType
from domain.universal.pressure import PsiaPressure
from nasa_cea.cea_calculator import CEACalculator

from rocketcea.cea_obj import CEA_Obj, add_new_propellant


def _apcp_component_mass_fractions(mixture: SolidPropellantMixture) -> tuple[float, float, float]:
    """Return mass fractions (0–100) for Al, AP, and HTPB for a validated APCP mixture."""
    if mixture.type is not SolidPropellantType.APCP:
        raise ValueError("CEA APCP calculator requires SolidPropellantType.APCP.")

    total = mixture.mass
    if total <= 0:
        raise ValueError("Solid propellant mixture must have positive total mass.")

    if not mixture.oxidizers:
        raise ValueError("APCP mixture must include at least one oxidizer (ammonium perchlorate).")

    unsupported_ox = [o for o in mixture.oxidizers if o.type is not OxidizerType.AMMONIUM_PERCHLORATE]
    if unsupported_ox:
        raise ValueError("APCP RocketCEA model only supports ammonium perchlorate as oxidizer.")

    if not mixture.fuels:
        raise ValueError("APCP mixture must include fuels (aluminum and HTPB).")

    allowed_fuels = frozenset({FuelType.ALUMINUM_POWDER, FuelType.HTPB})
    bad_fuels = [f for f in mixture.fuels if f.type not in allowed_fuels]
    if bad_fuels:
        raise ValueError(
            "APCP RocketCEA model only supports aluminum powder and HTPB fuels; "
            f"got: {sorted({f.type.value for f in bad_fuels})}"
        )

    al_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.ALUMINUM_POWDER)
    htpb_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.HTPB)
    ap_mass = sum(o.mass for o in mixture.oxidizers)

    if al_mass <= 0 or htpb_mass <= 0 or ap_mass <= 0:
        raise ValueError(
            "APCP mixture must have positive mass for aluminum, HTPB, and ammonium perchlorate."
        )

    al_pct = (al_mass / total) * 100.0
    ap_pct = (ap_mass / total) * 100.0
    htpb_pct = (htpb_mass / total) * 100.0
    return al_pct, ap_pct, htpb_pct


class CEAAPCP(CEACalculator):
    """APCP thermodynamic model from RocketCEA, driven by a domain SolidPropellantMixture."""

    _mixture: SolidPropellantMixture

    def __init__(self, mixture: SolidPropellantMixture, chamber_pressure: PsiaPressure) -> None:
        self._mixture = mixture
        super().__init__(chamber_pressure=chamber_pressure)

    @property
    def mixture(self) -> SolidPropellantMixture:
        return self._mixture

    def _build_cea_obj(self) -> CEA_Obj:
        al_pct, ap_pct, htpb_pct = _apcp_component_mass_fractions(self._mixture)

        propellant_name = f"APCP_{al_pct:.4f}_{ap_pct:.4f}_{htpb_pct:.4f}".replace(".", "_")
        card = f"""
oxidizer NH4CLO4(I)   wt%={ap_pct}
h,cal=-70690.0 t(k)=298.15 rho=1.95
fuel R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%={htpb_pct}
h,cal= 1200.0 t(k)=298.15 rho=0.9220
fuel Aluminum  AL 1       wt%={al_pct}
h,cal=0.0     t(k)=298.15
"""
        try:
            add_new_propellant(propellant_name, card)
        except Exception:
            # RocketCEA keeps propellant definitions globally; ignore duplicate registrations.
            pass

        return CEA_Obj(propName=propellant_name)
