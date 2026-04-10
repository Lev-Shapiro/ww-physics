from domain.missile.factories import PropellantFactory, StructureFactory, MissileFactory
from domain.missile.phase.boosting_phase import BoostingMissilePhase
from domain.universal.pressure import PsiaPressure

def main() -> None:
    # --- Standard Missile ---
    print("=== Standard Missile Simulation ===")
    total_mass_kg = 10.0
    apcp_mixture = PropellantFactory.create_apcp(total_mass_kg)
    structure = StructureFactory.create_standard_structure()
    missile = MissileFactory.create_test_missile(
        name="Standard Missile",
        propellant=apcp_mixture,
        structure=structure
    )
    run_simulation(missile)

    # --- Advanced Missile ---
    print("\n=== Advanced Missile Simulation ===")
    adv_total_mass_kg = 20.0
    adv_apcp_mixture = PropellantFactory.create_high_performance_apcp(adv_total_mass_kg)
    adv_structure = StructureFactory.create_advanced_structure()
    adv_missile = MissileFactory.create_advanced_interceptor(
        name="Advanced Interceptor",
        propellant=adv_apcp_mixture,
        structure=adv_structure
    )
    run_simulation(adv_missile)

def run_simulation(missile) -> None:
    print(f"Initializing {missile.name}...")
    print(f"Propellant Mixture: {missile.propellant.type.value}")
    print(f"Total Propellant Mass: {missile.propellant.mass:.2f} kg")
    print(f"Fuel/Oxidizer Ratio: {missile.propellant.ratio:.3f}")
    print(f"Missile Total Mass: {missile.mass:.2f} kg")

    print(f"\nStarting Boosting Phase for {missile.name}...")
    boosting_phase = BoostingMissilePhase.from_apcp(missile, chamber_pressure=PsiaPressure(psia=1200))
    
    print(f"Chamber Pressure: {boosting_phase.chamber_pressure.psia:.2f} psia")
    print(f"Exhaust Velocity: {boosting_phase.exhaust_velocity:.2f} m/s")
    print(f"Specific Impulse: {boosting_phase.specific_impulse:.2f} s")
    print(f"Mass Flow Rate:   {boosting_phase.mass_flow_rate:.4f} kg/s")
    
    print("\nBurning...")
    boosting_phase.burn()
    
    print(f"\n--- Final State: {missile.name} ---")
    print(f"Final Missile Mass: {missile.mass:.2f} kg")
    print(f"Final Propellant Mass: {missile.propellant.mass:.2f} kg")
    print(f"Final Velocity (Z): {missile.velocity.z.meters_per_second:.2f} m/s")

if __name__ == "__main__":
    main()
