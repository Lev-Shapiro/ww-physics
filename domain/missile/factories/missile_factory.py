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
            efficiency=EfficiencyFactor.from_value(0.85),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            ),
            start_angle=Angle3D.from_degrees(0, 90)
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
            start_angle=Angle3D.from_degrees(0, 45)
        )

    @staticmethod
    def create_v2(name: str = "V-2") -> Missile:
        # 0.88 reflects 1940s combustion instability, turbopump losses, and
        # mixture-ratio drift — well below a modern optimised engine (0.95+).
        return Missile(
            name=name,
            propellant=PropellantFactory.create_v2(),
            structure=StructureFactory.create_v2_structure(),
            efficiency=EfficiencyFactor.from_value(0.88),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            ),
            start_angle=Angle3D.from_degrees(0, 45)
        )
