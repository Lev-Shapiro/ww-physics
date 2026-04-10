from __future__ import annotations

from domain.missile.components.fuel import FuelType
from domain.missile.components.oxidizer import OxidizerType
from domain.missile.components.solid_propellant_mixture import SolidPropellantMixture
from domain.missile.components.solid_propellant_type import SolidPropellantType
from domain.universal.pressure import PsiaPressure
from nasa_cea.cea_calculator import CEACalculator

from rocketcea.cea_obj import CEA_Obj, add_new_propellant


def _nepe_component_mass_fractions(mixture: SolidPropellantMixture) -> tuple[float, float, float, float]:
    """Return mass fractions (0–100) for Al, AP, HMX, and HTPB for a validated NEPE mixture."""
    if mixture.type is not SolidPropellantType.NEPE:
        raise ValueError("CEA NEPE calculator requires SolidPropellantType.NEPE.")

    total = mixture.mass
    if total <= 0:
        raise ValueError("Solid propellant mixture must have positive total mass.")

    if not mixture.oxidizers:
        raise ValueError("NEPE mixture must include ammonium perchlorate as oxidizer.")

    unsupported_ox = [o for o in mixture.oxidizers if o.type is not OxidizerType.AMMONIUM_PERCHLORATE]
    if unsupported_ox:
        raise ValueError("NEPE RocketCEA model only supports ammonium perchlorate as oxidizer.")

    if not mixture.fuels:
        raise ValueError("NEPE mixture must include fuels (aluminum, HTPB, and HMX).")

    allowed_fuels = frozenset({FuelType.ALUMINUM_POWDER, FuelType.HTPB, FuelType.HMX})
    bad_fuels = [f for f in mixture.fuels if f.type not in allowed_fuels]
    if bad_fuels:
        raise ValueError(
            "NEPE RocketCEA model only supports aluminum powder, HTPB, and HMX fuels; "
            f"got: {sorted({f.type.value for f in bad_fuels})}"
        )

    al_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.ALUMINUM_POWDER)
    htpb_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.HTPB)
    hmx_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.HMX)
    ap_mass = sum(o.mass for o in mixture.oxidizers)

    if al_mass <= 0 or htpb_mass <= 0 or hmx_mass <= 0 or ap_mass <= 0:
        raise ValueError(
            "NEPE mixture must have positive mass for aluminum, HTPB, HMX, and ammonium perchlorate."
        )

    al_pct = (al_mass / total) * 100.0
    ap_pct = (ap_mass / total) * 100.0
    htpb_pct = (htpb_mass / total) * 100.0
    hmx_pct = (hmx_mass / total) * 100.0
    return al_pct, ap_pct, hmx_pct, htpb_pct


class CEANEPE(CEACalculator):
    """NEPE thermodynamic model from RocketCEA, for HMX/AP/Al/HTPB propellants (e.g. Trident II D5).

    NEPE (Nitrate Ester Plasticized Polyether) is a high-energy solid propellant used in advanced
    ballistic missiles. HMX provides additional energy density over standard APCP. The BTTN
    nitrate ester plasticizer (typically ~5%) is absorbed into the HTPB binder fraction for
    this model.
    """

    _mixture: SolidPropellantMixture

    def __init__(self, mixture: SolidPropellantMixture, chamber_pressure: PsiaPressure) -> None:
        self._mixture = mixture
        super().__init__(chamber_pressure=chamber_pressure)

    @property
    def mixture(self) -> SolidPropellantMixture:
        return self._mixture

    def _build_cea_obj(self) -> CEA_Obj:
        al_pct, ap_pct, hmx_pct, htpb_pct = _nepe_component_mass_fractions(self._mixture)

        propellant_name = (
            f"NEPE_{al_pct:.4f}_{ap_pct:.4f}_{hmx_pct:.4f}_{htpb_pct:.4f}".replace(".", "_")
        )
        card = f"""
oxidizer NH4CLO4(I)   wt%={ap_pct}
h,cal=-70690.0 t(k)=298.15 rho=1.95
fuel R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%={htpb_pct}
h,cal= 1200.0 t(k)=298.15 rho=0.9220
fuel Aluminum  AL 1       wt%={al_pct}
h,cal=0.0     t(k)=298.15
fuel HMX  C 4 H 8 N 8 O 8    wt%={hmx_pct}
h,cal=17200.0 t(k)=298.15 rho=1.91
"""
        try:
            add_new_propellant(propellant_name, card)
        except Exception:
            # RocketCEA keeps propellant definitions globally; ignore duplicate registrations.
            pass

        return CEA_Obj(propName=propellant_name)
