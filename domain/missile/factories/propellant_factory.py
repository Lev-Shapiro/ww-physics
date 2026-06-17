from domain.missile.components.fuel import Fuel, FuelType
from domain.missile.components.oxidizer import Oxidizer, OxidizerType
from domain.missile.components.propellant_mixture import PropellantMixture
from domain.missile.components.propellant_type import PropellantType
from domain.universal.pressure import PsiaPressure


class PropellantFactory:
    @staticmethod
    def create_tamir() -> PropellantMixture:
        """Tamir interceptor (Iron Dome) solid propellant — AP/Al/HTPB, ~90 kg missile total.

        Composition based on open-source literature for Rafael tactical interceptor motors:
        68% AP, 18% Al, 14% HTPB.
        """
        propellant_mass_kg = 50.0

        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, propellant_mass_kg * 0.16)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, propellant_mass_kg * 0.14)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, propellant_mass_kg * 0.68)

        return PropellantMixture.mix(
            type=PropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,),
            chamber_pressure=PsiaPressure(psia=2000)
        )

    @staticmethod
    def create_qassam() -> PropellantMixture:
        """Qassam-class unguided rocket propellant modeled as KNSU (sugar propellant)."""
        propellant_mass_kg = 20.0

        sugar_fuel = Fuel.from_kg(FuelType.SUGAR, propellant_mass_kg * 0.35)
        kno3_ox = Oxidizer.from_kg(OxidizerType.POTASSIUM_NITRATE, propellant_mass_kg * 0.65)

        return PropellantMixture.mix(
            type=PropellantType.KNSU,
            fuels=(sugar_fuel,),
            oxidizers=(kno3_ox,),
            chamber_pressure=PsiaPressure(psia=350)
        )

    @staticmethod
    def create_v2() -> PropellantMixture:
        """V-2 rocket liquid propellant — Ethanol and Liquid Oxygen."""
        ethanol_fuel = Fuel.from_kg(FuelType.ETHANOL, 4900)
        lox_ox = Oxidizer.from_kg(OxidizerType.LIQUID_OXYGEN, 3800)

        return PropellantMixture.mix(
            type=PropellantType.LIQUID,
            fuels=(ethanol_fuel,),
            oxidizers=(lox_ox,),
            chamber_pressure=PsiaPressure(psia=1500)  # Approximate chamber pressure
        )
