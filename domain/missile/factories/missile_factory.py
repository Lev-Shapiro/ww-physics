from domain.missile.missile import Missile, MissileStructure
from domain.missile.components.solid_propellant_mixture import SolidPropellantMixture
from domain.universal.efficiency_factor import EfficiencyFactor
from domain.universal.coords import Coords
from domain.universal.velocity import Velocity
from domain.universal.meters_per_second import MetersPerSecond

class MissileFactory:
    @staticmethod
    def create_test_missile(
        name: str,
        propellant: SolidPropellantMixture,
        structure: MissileStructure
    ) -> Missile:
        """
        Creates a test missile with standard test parameters.
        """
        return Missile(
            name=name,
            propellant=propellant,
            structure=structure,
            efficiency=EfficiencyFactor.medium_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            )
        )

    @staticmethod
    def create_advanced_interceptor(
        name: str,
        propellant: SolidPropellantMixture,
        structure: MissileStructure
    ) -> Missile:
        """
        Creates a high-performance advanced interceptor missile.
        """
        return Missile(
            name=name,
            propellant=propellant,
            structure=structure,
            efficiency=EfficiencyFactor.high_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            )
        )
