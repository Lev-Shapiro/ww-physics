from domain.missile.components.fuel import Fuel, FuelType
from domain.missile.components.oxidizer import Oxidizer, OxidizerType
from domain.missile.components.solid_propellant import SolidPropellantMixture
from domain.missile.thermodynamics import ThermodynamicsCalculator
from domain.formulas.specific_impulse import SpecificImpulseThermochemicalFormula
from domain.universal.pressure import PsiaPressure
from domain.universal.efficiency_factor import EfficiencyFactor

def main() -> None:
    total_mass_kg = 100.0
    
    al_fuel = Fuel.from_kg(FuelType.ALUMINUM_POWDER, total_mass_kg * 0.16)
    htpb_fuel = Fuel.from_kg(FuelType.HTPB, total_mass_kg * 0.125)
    ap_ox = Oxidizer.from_kg(OxidizerType.AMMONIUM_PERCHLORATE, total_mass_kg * 0.715)

    apcp_mixture = SolidPropellantMixture.mix(
        fuels=(al_fuel, htpb_fuel),
        oxidizers=(ap_ox,)
    )

    print(f"APCP Mixture Total Mass: {apcp_mixture.mass} kg")
    print(f"Fuel/Oxidizer Ratio: {apcp_mixture.ratio:.3f}")

    print("\nCalculating thermodynamic properties using RocketCEA...")
    
    chamber_pressure = PsiaPressure.from_psia(1000)
    external_pressure = PsiaPressure.from_psia(14.7)
    
    chamber_pressure_ratio = chamber_pressure.psia / external_pressure.psia
    
    calculator = ThermodynamicsCalculator()
    properties = calculator.calculate_apcp_properties(
        mixture=apcp_mixture,
        chamber_pressure=chamber_pressure,
    )

    print("\n--- Exhaust Gas Properties ---")
    print(f"Average Molecular Weight: {properties.molecular_weight:.3f} g/mol")
    print(f"Flame Temperature:        {properties.flame_temperature.kelvin:.2f} K")
    print(f"Ratio of Specific Heats:  {properties.gamma:.4f} (gamma)")
    
    efficiency = EfficiencyFactor.medium_quality()
    
    real_isp = SpecificImpulseThermochemicalFormula.calculate(
        exhaust=properties, 
        chamber_pressure_ratio=chamber_pressure_ratio,
        efficiency=efficiency
    )
    
    print(f"Real-World Specific Impulse ({efficiency.value*100}% eff): {real_isp:.2f} s")


if __name__ == "__main__":
    main()
