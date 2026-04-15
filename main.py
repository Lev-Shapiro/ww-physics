from domain.missile.components.propellant_type import PropellantType
from domain.missile.factories import MissileFactory
from domain.missile.missile import Missile
from domain.missile.phase.boosting_phase import BoostingMissilePhase


def main() -> None:
    simulations = [
        MissileFactory.create_tamir(),
        MissileFactory.create_qassam(),
        MissileFactory.create_v2(),
    ]
    for missile in simulations:
        run_simulation(missile)


def run_simulation(missile: Missile) -> None:
    if missile.propellant.type is PropellantType.NEPE:
        boosting_phase = BoostingMissilePhase.from_nepe(missile)
    elif missile.propellant.type is PropellantType.KNSU:
        boosting_phase = BoostingMissilePhase.from_knsu(missile)
    elif missile.propellant.type is PropellantType.LIQUID:
        boosting_phase = BoostingMissilePhase.from_liquid(missile)
    else:
        boosting_phase = BoostingMissilePhase.from_apcp(missile)

    print("--------------------------------")
    print(f"Launching {missile.name} ({missile.structure.dry_mass:.2f}/{missile.mass:.2f}kg)")
    print(f"Specific Impulse: {boosting_phase.specific_impulse:.2f} s")

    print("\nBurning...")
    boosting_phase.burn()

    print(f"Final Velocity: {missile.velocity.z.meters_per_second:.2f} m/s")


if __name__ == "__main__":
    main()
