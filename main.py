from domain.missile.components.solid_propellant_type import SolidPropellantType
from domain.missile.factories import MissileFactory
from domain.missile.missile import Missile
from domain.missile.phase.boosting_phase import BoostingMissilePhase
from domain.universal.pressure import PsiaPressure


def main() -> None:
    missiles = [
        MissileFactory.create_test_missile(name="Standard Missile"),
        MissileFactory.create_advanced_interceptor(name="Advanced Interceptor"),
        MissileFactory.create_tamir(),
        MissileFactory.create_trident_ii_d5(),
        MissileFactory.create_arrow3(),
    ]

    for missile in missiles:
        run_simulation(missile)


def run_simulation(missile: Missile) -> None:
    if missile.propellant.type is SolidPropellantType.NEPE:
        boosting_phase = BoostingMissilePhase.from_nepe(missile, chamber_pressure=PsiaPressure(psia=1000))
    else:
        boosting_phase = BoostingMissilePhase.from_apcp(missile, chamber_pressure=PsiaPressure(psia=1000))

    print("--------------------------------")
    print(f"Launching {missile.name} ({missile.structure.dry_mass:.2f}/{missile.mass:.2f}kg)")
    print(f"Specific Impulse: {boosting_phase.specific_impulse:.2f} s")

    print("\nBurning...")
    boosting_phase.burn()

    print(f"Final Velocity: {missile.velocity.z.meters_per_second:.2f} m/s")


if __name__ == "__main__":
    main()
