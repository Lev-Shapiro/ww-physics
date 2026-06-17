from domain.missile.components.propellant_type import PropellantType
from domain.missile.factories import MissileFactory
from domain.missile.missile import Missile
from domain.missile.phase.boosting_phase import BoostingMissilePhase
from reality.reality import Reality


def main() -> None:
    simulations = [
        MissileFactory.create_tamir(),
        MissileFactory.create_qassam(),
        MissileFactory.create_v2(),
    ]
        
    for missile in simulations:
        run_simulation(missile)


def run_simulation(missile: Missile) -> None:
    print("--------------------------------")
    print(f"Launching {missile.name} ({missile.structure.dry_mass:.2f}/{missile.mass:.2f}kg)")

    print("\nBurning...")
    
    print(f"Exit Pressure Start: {missile.exit_pressure.psia:.2f} psia")
    
    update_ms = 40
    
    Reality(update_ms, False, True).start([missile])
    
    print(f"Exit Pressure End: {missile.exit_pressure.psia:.2f} psia")
    
    print(f"Final Velocity: {missile.velocity.y.meters_per_second:.2f} m/s")


if __name__ == "__main__":
    main()
