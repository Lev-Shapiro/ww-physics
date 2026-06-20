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
        # 24 kg of KNSU (was 20) lifts the propellant mass fraction toward a real
        # Qassam-3, raising the ideal Δv ceiling.
        propellant_mass_kg = 24.0

        sugar_fuel = Fuel.from_kg(FuelType.SUGAR, propellant_mass_kg * 0.35)
        kno3_ox = Oxidizer.from_kg(OxidizerType.POTASSIUM_NITRATE, propellant_mass_kg * 0.65)

        return PropellantMixture.mix(
            type=PropellantType.KNSU,
            fuels=(sugar_fuel,),
            oxidizers=(kno3_ox,),
            # 550 psia (was 350): higher chamber pressure raises mass-flow rate so
            # the motor burns out in ~7 s instead of ~12 s, cutting gravity losses.
            chamber_pressure=Pressure(psia=550)
        )

    @staticmethod
    def create_jerico_iron_man() -> PropellantMixture:
        # Fictional "Jericho" from the Iron Man (2008) film: a large, advanced
        # Stark Industries solid-fuel missile that lofts a cluster of submunitions.
        # Modelled as a high-energy APCP grain (same Al/HTPB/AP chemistry as Tamir)
        # scaled up to a V-2-class motor. ~1500 kg of propellant.
        propellant_mass_kg = 1_500.0

        al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, propellant_mass_kg * 0.18)
        htpb_fuel = Fuel.from_kg(FuelType.HTPB, propellant_mass_kg * 0.12)
        ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, propellant_mass_kg * 0.70)

        return PropellantMixture.mix(
            type=PropellantType.APCP,
            fuels=(al_fuel, htpb_fuel),
            oxidizers=(ap_ox,),
            # High chamber pressure befitting advanced (fictional) Stark engineering.
            chamber_pressure=Pressure(psia=1500)
        )

    @staticmethod
    def create_starship_v3() -> PropellantMixture:
        # SpaceX Starship V3 (Block 3) full stack, modelled as one methalox load:
        # 4,050 t (Super Heavy booster) + 1,600 t (Ship) = 5,650 t of subcooled
        # liquid methane + liquid oxygen burned at Raptor 3 conditions.
        # Raptor 3 runs O/F ≈ 3.6 (≈78% LOX / 22% CH4 by mass).
        total_propellant_kg = 5_650_000.0
        of_ratio = 3.6

        methane_kg = total_propellant_kg / (1.0 + of_ratio)      # ≈ 1,228,261 kg
        lox_kg = total_propellant_kg * of_ratio / (1.0 + of_ratio)  # ≈ 4,421,739 kg

        methane = Fuel.from_kg(FuelType.METHANE, methane_kg)
        lox = Oxidizer.from_kg(OxidizerType.LIQUID_OXYGEN, lox_kg)

        return PropellantMixture.mix(
            type=PropellantType.LIQUID,
            fuels=(methane,),
            oxidizers=(lox,),
            # Raptor 3 chamber pressure ≈ 330 bar ≈ 4785 psia.
            chamber_pressure=Pressure(psia=4785),
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
