from domain.missile.components.solid_propellant_type import SolidPropellantType
from domain.missile.factories import MissileFactory
from domain.missile.missile import Missile
from domain.missile.phase.boosting_phase import BoostingMissilePhase
from domain.universal.pressure import PsiaPressure


def main() -> None:
    simulations = [
        (MissileFactory.create_tamir(), PsiaPressure(psia=1000)),
        (MissileFactory.create_trident_ii_d5(), PsiaPressure(psia=1800)),
        (MissileFactory.create_arrow3(), PsiaPressure(psia=1200)),
    ]

    for missile, pressure in simulations:
        run_simulation(missile, pressure)


def run_simulation(missile: Missile, chamber_pressure: PsiaPressure) -> None:
    if missile.propellant.type is SolidPropellantType.NEPE:
        boosting_phase = BoostingMissilePhase.from_nepe(missile, chamber_pressure=chamber_pressure)
    else:
        boosting_phase = BoostingMissilePhase.from_apcp(missile, chamber_pressure=chamber_pressure)

    print("--------------------------------")
    print(f"Launching {missile.name} ({missile.structure.dry_mass:.2f}/{missile.mass:.2f}kg)")
    print(f"Specific Impulse: {boosting_phase.specific_impulse:.2f} s")

    print("\nBurning...")
    boosting_phase.burn()

    print(f"Final Velocity: {missile.velocity.z.meters_per_second:.2f} m/s")


if __name__ == "__main__":
    main()
