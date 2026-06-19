from domain.missile.components.fuel import Fuel, FuelType
from domain.missile.components.oxidizer import Oxidizer, OxidizerType
from domain.missile.components.propellant_mixture import PropellantMixture
from domain.missile.components.propellant_type import PropellantType
from domain.universal.pressure import Pressure


class PropellantFactory:
    @staticmethod
    def create_tamir() -> PropellantMixture:
        propellant_mass_kg = 28.0

        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, propellant_mass_kg * 0.16)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, propellant_mass_kg * 0.14)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, propellant_mass_kg * 0.68)

        return PropellantMixture.mix(
            type=PropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,),
            chamber_pressure=Pressure(psia=1000)
        )

    @staticmethod
    def create_qassam() -> PropellantMixture:
        propellant_mass_kg = 20.0

        sugar_fuel = Fuel.from_kg(FuelType.SUGAR, propellant_mass_kg * 0.35)
        kno3_ox = Oxidizer.from_kg(OxidizerType.POTASSIUM_NITRATE, propellant_mass_kg * 0.65)

        return PropellantMixture.mix(
            type=PropellantType.KNSU,
            fuels=(sugar_fuel,),
            oxidizers=(kno3_ox,),
            chamber_pressure=Pressure(psia=350)
        )

    @staticmethod
    def create_v2() -> PropellantMixture:
        fuel_mass_kg = 3_810.0
        ethanol = Fuel.from_kg(FuelType.ETHANOL, fuel_mass_kg * 0.75)  # 2,857.5 kg
        water = Fuel.from_kg(FuelType.WATER, fuel_mass_kg * 0.25)      #   952.5 kg
        lox = Oxidizer.from_kg(OxidizerType.LIQUID_OXYGEN, 4_910.0)

        return PropellantMixture.mix(
            type=PropellantType.LIQUID,
            fuels=(ethanol, water),
            oxidizers=(lox,),
            chamber_pressure=Pressure(psia=217.6),
        )
