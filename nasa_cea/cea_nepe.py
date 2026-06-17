from __future__ import annotations

from domain.missile.components.fuel import FuelType
from domain.missile.components.oxidizer import OxidizerType
from domain.missile.components.propellant_mixture import PropellantMixture
from domain.missile.components.propellant_type import PropellantType
from domain.universal.pressure import PsiaPressure
from nasa_cea.cea_calculator import CEACalculator

from rocketcea.cea_obj import CEA_Obj, add_new_propellant


def _nepe_component_mass_fractions(
    mixture: PropellantMixture,
) -> tuple[float, float, float, float, float]:
    """Return mass fractions (0–100) for Al, AP, HMX, HTPB, and BTTN for a validated NEPE mixture."""
    if mixture.type is not PropellantType.NEPE:
        raise ValueError("CEA NEPE calculator requires PropellantType.NEPE.")

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

    allowed_fuels = frozenset({FuelType.ALUMINUM_POWDER, FuelType.HTPB, FuelType.HMX, FuelType.BTTN})
    bad_fuels = [f for f in mixture.fuels if f.type not in allowed_fuels]
    if bad_fuels:
        raise ValueError(
            "NEPE RocketCEA model only supports aluminum powder, HTPB, HMX, and BTTN fuels; "
            f"got: {sorted({f.type.value for f in bad_fuels})}"
        )

    al_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.ALUMINUM_POWDER)
    htpb_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.HTPB)
    hmx_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.HMX)
    bttn_mass = sum(f.mass for f in mixture.fuels if f.type is FuelType.BTTN)
    ap_mass = sum(o.mass for o in mixture.oxidizers)

    if al_mass <= 0 or htpb_mass <= 0 or hmx_mass <= 0 or ap_mass <= 0:
        raise ValueError(
            "NEPE mixture must have positive mass for aluminum, HTPB, HMX, and ammonium perchlorate."
        )

    al_pct = (al_mass / total) * 100.0
    ap_pct = (ap_mass / total) * 100.0
    htpb_pct = (htpb_mass / total) * 100.0
    hmx_pct = (hmx_mass / total) * 100.0
    bttn_pct = (bttn_mass / total) * 100.0
    return al_pct, ap_pct, hmx_pct, htpb_pct, bttn_pct


class CEANEPE(CEACalculator):
    """NEPE thermodynamic model from RocketCEA, for HMX/AP/Al/HTPB/BTTN propellants (e.g. Trident II D5).

    NEPE (Nitrate Ester Plasticized Polyether) derives its advantage over APCP from two sources:
    - HMX provides additional combustion energy as an energetic filler.
    - BTTN (butanetriol trinitrate, C4H7N3O9) is the nitrate ester plasticizer; it is oxygen-rich
      and substantially improves the overall O/F balance relative to APCP at equivalent AP loading.
    """

    _mixture: PropellantMixture

    def __init__(self, mixture: PropellantMixture) -> None:
        self._mixture = mixture
        super().__init__(chamber_pressure=mixture.chamber_pressure)

    @property
    def mixture(self) -> PropellantMixture:
        return self._mixture

    def _build_cea_obj(self) -> CEA_Obj:
        al_pct, ap_pct, hmx_pct, htpb_pct, bttn_pct = _nepe_component_mass_fractions(self._mixture)

        propellant_name = (
            f"NEPE_{al_pct:.3f}_{ap_pct:.3f}_{hmx_pct:.3f}_{htpb_pct:.3f}_{bttn_pct:.3f}"
            .replace(".", "_")
        )

        bttn_line = ""
        if bttn_pct > 0:
            # BTTN: C4H7N3O9, ΔHf ≈ -145 kcal/mol, ρ = 1.52 g/cm³
            bttn_line = f"""fuel BTTN  C 4 H 7 N 3 O 9    wt%={bttn_pct}
h,cal=-145000.0 t(k)=298.15 rho=1.52
"""

        card = f"""
oxidizer NH4CLO4(I)   wt%={ap_pct}
h,cal=-70690.0 t(k)=298.15 rho=1.95
fuel R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%={htpb_pct}
h,cal= 1200.0 t(k)=298.15 rho=0.9220
fuel Aluminum  AL 1       wt%={al_pct}
h,cal=0.0     t(k)=298.15
fuel HMX  C 4 H 8 N 8 O 8    wt%={hmx_pct}
h,cal=17200.0 t(k)=298.15 rho=1.91
{bttn_line}"""
        try:
            add_new_propellant(propellant_name, card)
        except Exception:
            # RocketCEA keeps propellant definitions globally; ignore duplicate registrations.
            pass

        return CEA_Obj(propName=propellant_name)
