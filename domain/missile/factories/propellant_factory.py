from domain.missile.components.fuel import Fuel, FuelType
from domain.missile.components.oxidizer import Oxidizer, OxidizerType
from domain.missile.components.solid_propellant_mixture import SolidPropellantMixture
from domain.missile.components.solid_propellant_type import SolidPropellantType


class PropellantFactory:
    @staticmethod
    def create_apcp() -> SolidPropellantMixture:
        propellant_mass_kg = 10

        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, propellant_mass_kg * 0.16)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, propellant_mass_kg * 0.125)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, propellant_mass_kg * 0.715)

        return SolidPropellantMixture.mix(
            type=SolidPropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,)
        )

    @staticmethod
    def create_high_performance_apcp() -> SolidPropellantMixture:
        propellant_mass_kg = 100

        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, propellant_mass_kg * 0.20)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, propellant_mass_kg * 0.10)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, propellant_mass_kg * 0.70)

        return SolidPropellantMixture.mix(
            type=SolidPropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,)
        )

    @staticmethod
    def create_tamir() -> SolidPropellantMixture:
        """Tamir interceptor (Iron Dome) solid propellant — AP/Al/HTPB, ~90 kg missile total.

        Composition based on open-source literature for Rafael tactical interceptor motors:
        68% AP, 18% Al, 14% HTPB.
        """
        propellant_mass_kg = 60.0

        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, propellant_mass_kg * 0.18)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, propellant_mass_kg * 0.14)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, propellant_mass_kg * 0.68)

        return SolidPropellantMixture.mix(
            type=SolidPropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,)
        )

    @staticmethod
    def create_trident_ii_d5_stage1() -> SolidPropellantMixture:
        """Trident II D5 Stage 1 NEPE-75 propellant — HMX/AP/Al/HTPB.

        Composition from public-domain sources (FAS, Jane's) for Thiokol/ATK NEPE-75:
        44% AP, 20% Al, 19% HMX, 17% HTPB (BTTN plasticizer absorbed into binder fraction).
        Stage 1 propellant load: ~25,000 kg.
        """
        propellant_mass_kg = 25_000.0

        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, propellant_mass_kg * 0.20)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, propellant_mass_kg * 0.17)
        hmx_fuel = Fuel.from_kg(FuelType.HMX, propellant_mass_kg * 0.19)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, propellant_mass_kg * 0.44)

        return SolidPropellantMixture.mix(
            type=SolidPropellantType.NEPE,
            fuels=(al_fuel, htpb_fuel, hmx_fuel),
            oxidizers=(ap_ox,)
        )

    @staticmethod
    def create_arrow3() -> SolidPropellantMixture:
        """Arrow 3 boost-stage solid propellant — high-energy AP/Al/HTPB.

        Arrow 3 uses a high-energy solid propellant for exoatmospheric intercept.
        Estimated composition based on high-performance interceptor motors: 70% AP, 20% Al, 10% HTPB.
        Boost stage propellant load: ~180 kg.
        """
        propellant_mass_kg = 180.0

        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, propellant_mass_kg * 0.20)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, propellant_mass_kg * 0.10)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, propellant_mass_kg * 0.70)

        return SolidPropellantMixture.mix(
            type=SolidPropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,)
        )
