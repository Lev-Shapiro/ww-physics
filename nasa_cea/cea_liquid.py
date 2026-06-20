from __future__ import annotations

from domain.missile.components.fuel import FuelType
from domain.missile.components.propellant_mixture import PropellantMixture
from domain.missile.components.propellant_type import PropellantType
from nasa_cea.cea_calculator import CEACalculator

from rocketcea.cea_obj import CEA_Obj, add_new_fuel


# ── water-diluted ethanol fuel card ───────────────────────────────────────────
# Cached by (ethanol_wt_pct, water_wt_pct) so we only register each blend once.
_REGISTERED_FUEL_BLENDS: set[str] = set()

# Standard formation enthalpies [cal/mol]:
#   ethanol  C2H5OH(L)  ΔHf = -277.69 kJ/mol = -66,340 cal/mol
#   water    H2O(L)     ΔHf = -285.83 kJ/mol = -68,315 cal/mol
_H_ETHANOL_CAL_MOL = -66_340.0
_H_WATER_CAL_MOL = -68_315.0


def _register_ethanol_water_fuel(ethanol_pct: float, water_pct: float) -> str:
    """
    Register a custom ethanol+water blended fuel card with RocketCEA and return
    its name.  Registrations are idempotent — RocketCEA silently ignores
    duplicate names, so we keep a local set to avoid repeated calls.
    """
    name = f"EtOH{ethanol_pct:.1f}_H2O{water_pct:.1f}".replace(".", "_")
    if name not in _REGISTERED_FUEL_BLENDS:
        card = (
            f"fuel C2H5OH(L)  C 2  H 6  O 1   wt%={ethanol_pct:.2f}"
            f"  h,cal={_H_ETHANOL_CAL_MOL:.1f}   t(k)=298.15\n"
            f"fuel H2O(L)     H 2  O 1          wt%={water_pct:.2f}"
            f"  h,cal={_H_WATER_CAL_MOL:.1f}   t(k)=298.15\n"
        )
        try:
            add_new_fuel(name, card)
        except Exception:
            pass
        _REGISTERED_FUEL_BLENDS.add(name)
    return name


class CEALiquid(CEACalculator):
    """
    Liquid propellant thermodynamic model (RocketCEA).

    Supports pure ethanol/LOX, water-diluted ethanol/LOX (e.g. V-2), and
    liquid methane/LOX (e.g. SpaceX Raptor / Starship).
    When a FuelType.WATER component is present in the mixture the fuel blend
    is registered as a custom RocketCEA card.  The oxidiser-to-fuel mass
    ratio derived from the domain mixture is passed to every CEA call so
    that flame temperature, c*, and γ reflect the actual O/F.
    """

    _mixture: PropellantMixture

    def __init__(self, mixture: PropellantMixture) -> None:
        if mixture.type is not PropellantType.LIQUID:
            raise ValueError("CEALiquid requires PropellantType.LIQUID.")

        self._mixture = mixture

        # O/F mass ratio (oxidiser / fuel total)
        of_ratio = mixture.oxidizer_mass / mixture.fuel_mass if mixture.fuel_mass > 0 else 1.0

        super().__init__(chamber_pressure=mixture.chamber_pressure, mixture_ratio=of_ratio)

    @property
    def mixture(self) -> PropellantMixture:
        return self._mixture

    def _build_cea_obj(self) -> CEA_Obj:
        methane_mass = sum(
            f.mass for f in self._mixture.fuels if f.type is FuelType.METHANE
        )
        if methane_mass > 0:
            # Liquid methane / LOX (e.g. SpaceX Raptor / Starship). RocketCEA
            # ships a built-in "CH4" fuel card; the O/F passed in __init__ drives
            # the flame temperature, c*, and γ used downstream.
            return CEA_Obj(fuelName="CH4", oxName="LOX")

        water_mass = sum(
            f.mass for f in self._mixture.fuels if f.type is FuelType.WATER
        )
        ethanol_mass = sum(
            f.mass for f in self._mixture.fuels if f.type is FuelType.ETHANOL
        )
        total_fuel = ethanol_mass + water_mass

        if water_mass > 0 and total_fuel > 0:
            ethanol_pct = (ethanol_mass / total_fuel) * 100.0
            water_pct = (water_mass / total_fuel) * 100.0
            fuel_name = _register_ethanol_water_fuel(ethanol_pct, water_pct)
            return CEA_Obj(fuelName=fuel_name, oxName="LOX")

        # Pure ethanol — use RocketCEA built-in
        return CEA_Obj(fuelName="Ethanol", oxName="LOX")
