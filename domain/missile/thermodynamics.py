from __future__ import annotations

from dataclasses import dataclass

from .components.fuel import FuelType
from .components.oxidizer import OxidizerType
from .components.solid_propellant import SolidPropellantMixture

from rocketcea.cea_obj import CEA_Obj, add_new_propellant

@dataclass(frozen=True, slots=True)
class ExhaustProperties:
    molecular_weight: float  # in g/mol
    flame_temperature: float  # in Kelvin
    gamma: float  # Ratio of specific heats


class ThermodynamicsCalculator:
    """
    Domain service to compute thermodynamic properties using RocketCEA.
    """

    @staticmethod
    def calculate_apcp_properties(
        mixture: SolidPropellantMixture, chamber_pressure_psia: float = 1000.0
    ) -> ExhaustProperties:
        """
        Calculates the thermodynamic properties of an APCP mixture.
        Assumes the mixture contains Aluminum, HTPB as fuels and AP as oxidizer.
        """
        if mixture.mass <= 0:
            raise ValueError("Mixture must have positive mass.")

        al_mass = sum(f.mass for f in mixture.fuels if f.type == FuelType.ALUMINUM_POWDER)
        htpb_mass = sum(f.mass for f in mixture.fuels if f.type == FuelType.HTPB)
        ap_mass = sum(o.mass for o in mixture.oxidizers if o.type == OxidizerType.AMMONIUM_PERCHLORATE)

        total_mass = al_mass + htpb_mass + ap_mass
        if total_mass == 0:
            raise ValueError("Mixture does not contain valid APCP components (AL, HTPB, AP).")

        al_pct = (al_mass / total_mass) * 100.0
        htpb_pct = (htpb_mass / total_mass) * 100.0
        ap_pct = (ap_mass / total_mass) * 100.0

        propellant_name = f"APCP_{al_pct:.2f}_{ap_pct:.2f}_{htpb_pct:.2f}".replace(".", "_")
        
        add_new_propellant(propellant_name, f"""
fuel NH4CLO4(I)       wt%={ap_pct}
fuel R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%={htpb_pct}
h,cal= 1200.0 t(k)=298.15 rho=0.9220
fuel Aluminum  AL 1       wt%={al_pct}
h,cal=0.0     t(k)=298.15
""")

        cea = CEA_Obj(propName=propellant_name)

        mw, gamma = cea.get_Chamber_MolWt_gamma(Pc=chamber_pressure_psia, MR=1.0, eps=10.0)
        t_comb_rankine = cea.get_Tcomb(Pc=chamber_pressure_psia, MR=1.0)
        t_comb_kelvin = t_comb_rankine * 5.0 / 9.0

        return ExhaustProperties(
            molecular_weight=float(mw),
            flame_temperature=float(t_comb_kelvin),
            gamma=float(gamma),
        )
