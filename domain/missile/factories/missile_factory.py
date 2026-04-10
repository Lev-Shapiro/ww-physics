from domain.missile.factories.propellant_factory import PropellantFactory
from domain.missile.factories.structure_factory import StructureFactory
from domain.missile.missile import Missile
from domain.universal.efficiency_factor import EfficiencyFactor
from domain.universal.coords import Coords
from domain.universal.velocity import Velocity
from domain.universal.meters_per_second import MetersPerSecond

class MissileFactory:
    @staticmethod
    def create_test_missile(name: str) -> Missile:
        return Missile(
            name=name,
            propellant=PropellantFactory.create_apcp(),
            structure=StructureFactory.create_standard_structure(),
            efficiency=EfficiencyFactor.medium_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            )
        )

    @staticmethod
    def create_advanced_interceptor(name: str) -> Missile:
        return Missile(
            name=name,
            propellant=PropellantFactory.create_high_performance_apcp(),
            structure=StructureFactory.create_advanced_structure(),
            efficiency=EfficiencyFactor.extremely_high_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            )
        )

    @staticmethod
    def create_tamir(name: str = "Tamir") -> Missile:
        """Iron Dome Tamir interceptor. ~90 kg total, APCP solid motor."""
        return Missile(
            name=name,
            propellant=PropellantFactory.create_tamir(),
            structure=StructureFactory.create_tamir_structure(),
            efficiency=EfficiencyFactor.high_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            )
        )

    @staticmethod
    def create_trident_ii_d5(name: str = "Trident II D5") -> Missile:
        """Trident II D5 Stage 1 model. ~27,500 kg total, NEPE-75 solid motor."""
        return Missile(
            name=name,
            propellant=PropellantFactory.create_trident_ii_d5_stage1(),
            structure=StructureFactory.create_trident_ii_d5_stage1_structure(),
            efficiency=EfficiencyFactor.extremely_high_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            )
        )

    @staticmethod
    def create_arrow3(name: str = "Arrow 3") -> Missile:
        """Arrow 3 boost stage. ~300 kg total, high-energy APCP solid motor."""
        return Missile(
            name=name,
            propellant=PropellantFactory.create_arrow3(),
            structure=StructureFactory.create_arrow3_structure(),
            efficiency=EfficiencyFactor.extremely_high_quality(),
            coords=Coords.xyz(0, 0, 0),
            velocity=Velocity(
                x=MetersPerSecond(0),
                y=MetersPerSecond(0),
                z=MetersPerSecond(0)
            )
        )
