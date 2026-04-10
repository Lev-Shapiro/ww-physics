from domain.missile.missile import MissileStructure
from domain.universal.mass import Mass

class StructureFactory:
    @staticmethod
    def create_standard_structure(
        burning_surface_area: float = 0.05,
        nozzle_throat_area: float = 0.0005,
        casing_mass_kg: float = 2.0,
        nozzle_mass_kg: float = 0.5,
        electronics_mass_kg: float = 0.5,
        payload_mass_kg: float = 1.0,
        structural_mass_kg: float = 1.0
    ) -> MissileStructure:
        """
        Creates a standard missile structure with default or specific values.
        """
        return MissileStructure(
            burning_surface_area=burning_surface_area,
            nozzle_throat_area=nozzle_throat_area,
            casing_mass=Mass.from_kg(casing_mass_kg),
            nozzle_mass=Mass.from_kg(nozzle_mass_kg),
            electronics_mass=Mass.from_kg(electronics_mass_kg),
            payload_mass=Mass.from_kg(payload_mass_kg),
            structural_mass=Mass.from_kg(structural_mass_kg)
        )

    @staticmethod
    def create_advanced_structure(
        burning_surface_area: float = 0.1,
        nozzle_throat_area: float = 0.001,
        casing_mass_kg: float = 3.0,
        nozzle_mass_kg: float = 1.5,
        electronics_mass_kg: float = 2.0,
        payload_mass_kg: float = 2.0,
        structural_mass_kg: float = 1.5
    ) -> MissileStructure:
        """
        Creates an advanced, high-performance missile structure.
        Total dry mass: 10kg. For 20kg propellant, this is a 66% mass fraction,
        which is high-end for a tactical interceptor.
        """
        return MissileStructure(
            burning_surface_area=burning_surface_area,
            nozzle_throat_area=nozzle_throat_area,
            casing_mass=Mass.from_kg(casing_mass_kg),
            nozzle_mass=Mass.from_kg(nozzle_mass_kg),
            electronics_mass=Mass.from_kg(electronics_mass_kg),
            payload_mass=Mass.from_kg(payload_mass_kg),
            structural_mass=Mass.from_kg(structural_mass_kg)
        )
