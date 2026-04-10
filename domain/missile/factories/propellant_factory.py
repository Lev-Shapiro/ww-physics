from domain.missile.components.fuel import Fuel, FuelType
from domain.missile.components.oxidizer import Oxidizer, OxidizerType
from domain.missile.components.solid_propellant_mixture import SolidPropellantMixture
from domain.missile.components.solid_propellant_type import SolidPropellantType

class PropellantFactory:
    @staticmethod
    def create_apcp(total_mass_kg: float) -> SolidPropellantMixture:
        """
        Creates a standard APCP propellant mixture.
        Ratio: 16% Al, 12.5% HTPB, 71.5% AP
        """
        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, total_mass_kg * 0.16)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, total_mass_kg * 0.125)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, total_mass_kg * 0.715)

        return SolidPropellantMixture.mix(
            type=SolidPropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,)
        )

    @staticmethod
    def create_high_performance_apcp(total_mass_kg: float) -> SolidPropellantMixture:
        """
        Creates a high-performance APCP propellant mixture.
        Uses a slightly different ratio for higher isp potential (hypothetically).
        Ratio: 20% Al, 10% HTPB, 70% AP
        """
        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, total_mass_kg * 0.20)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, total_mass_kg * 0.10)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, total_mass_kg * 0.70)

        return SolidPropellantMixture.mix(
            type=SolidPropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,)
        )
