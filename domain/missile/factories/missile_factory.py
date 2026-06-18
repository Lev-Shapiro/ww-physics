from domain.missile.factories.propellant_factory import PropellantFactory
from domain.missile.factories.structure_factory import StructureFactory
from domain.missile.missile import Missile
from domain.universal.angle3d import Angle3D
from domain.universal.efficiency_factor import EfficiencyFactor
from domain.universal.coords import Coords
from domain.universal.velocity import Velocity
from domain.universal.meters_per_second import MetersPerSecond

class MissileFactory:
    @staticmethod
    def create_tamir(name: str = "Tamir") -> Missile:
        return Missile(
            name=name,
            propellant=PropellantFactory.create_tamir(),
            structure=StructureFactory.create_tamir_structure(),
            efficiency=EfficiencyFactor.extremely_high_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            ),
            start_angle=Angle3D.from_degrees(0, 45)
        )

    @staticmethod
    def create_qassam(name: str = "Qassam") -> Missile:
        """short-range unguided rocket model."""
        return Missile(
            name=name,
            propellant=PropellantFactory.create_qassam(),
            structure=StructureFactory.create_qassam_structure(),
            efficiency=EfficiencyFactor.low_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            ),
            start_angle=Angle3D.from_degrees(0, 90)
        )

    @staticmethod
    def create_v2(name: str = "V-2") -> Missile:
        return Missile(
            name=name,
            propellant=PropellantFactory.create_v2(),
            structure=StructureFactory.create_v2_structure(),
            efficiency=EfficiencyFactor.high_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            ),
            start_angle=Angle3D.from_degrees(0, 90)
        )
