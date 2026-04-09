from domain.missile.components.fuel import Fuel, FuelType
from domain.missile.components.oxidizer import Oxidizer, OxidizerType
from domain.missile.components.solid_propellant import SolidPropellantMixture
from domain.missile.thermodynamics import ThermodynamicsCalculator

def main() -> None:
    total_mass_kg = 100.0
    
    al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, total_mass_kg * 0.15)
    htpb_fuel = Fuel.from_kg(FuelType.HTPB, total_mass_kg * 0.15)
    ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, total_mass_kg * 0.70)

    apcp_mixture = SolidPropellantMixture.mix(
        fuels=(al_fuel, htpb_fuel),
        oxidizers=(ap_ox,)
    )

    print(f"APCP Mixture Total Mass: {apcp_mixture.mass} kg")
    print(f"Fuel/Oxidizer Ratio: {apcp_mixture.ratio:.3f}")

    print("\nCalculating thermodynamic properties using RocketCEA...")
    calculator = ThermodynamicsCalculator()
    properties = calculator.calculate_apcp_properties(
        mixture=apcp_mixture,
        chamber_pressure_psia=1000.0
    )

    print("\n--- Exhaust Gas Properties ---")
    print(f"Average Molecular Weight: {properties.molecular_weight:.3f} g/mol")
    print(f"Flame Temperature:        {properties.flame_temperature:.2f} K")
    print(f"Ratio of Specific Heats:  {properties.gamma:.4f} (gamma)")


if __name__ == "__main__":
    main()
