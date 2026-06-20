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
            start_angle=Angle3D.from_degrees(0, 45)
        )

    @staticmethod
    def create_jerico_iron_man(name: str = "Jerico Iron Man") -> Missile:
        # Fictional "Jericho" missile from Iron Man (2008), named "Jerico Iron Man"
        # to avoid confusion with the real Israeli Jericho ballistic missile family.
        # Advanced Stark Industries tech -> high engine efficiency.
        return Missile(
            name=name,
            propellant=PropellantFactory.create_jerico_iron_man(),
            structure=StructureFactory.create_jerico_iron_man_structure(),
            efficiency=EfficiencyFactor.from_value(0.95),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            ),
            start_angle=Angle3D.from_degrees(0, 45)
        )

    @staticmethod
    def create_starship_v3(name: str = "Starship V3") -> Missile:
        # SpaceX Starship V3 (Block 3) full stack, methalox (LCH4/LOX) at Raptor 3
        # conditions. 0.96 efficiency reflects Raptor's full-flow staged-combustion
        # cycle — among the highest-performing engines ever flown.
        return Missile(
            name=name,
            propellant=PropellantFactory.create_starship_v3(),
            structure=StructureFactory.create_starship_v3_structure(),
            efficiency=EfficiencyFactor.from_value(0.96),
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
