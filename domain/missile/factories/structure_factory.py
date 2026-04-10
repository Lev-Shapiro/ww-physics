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
    def create_tamir_structure() -> MissileStructure:
        """Tamir interceptor structure. ~28 kg dry mass (casing, nozzle, electronics, warhead)."""
        return MissileStructure(
            burning_surface_area=0.15,
            nozzle_throat_area=0.002,
            casing_mass=Mass.from_kg(5.0),
            nozzle_mass=Mass.from_kg(2.0),
            electronics_mass=Mass.from_kg(5.0),
            payload_mass=Mass.from_kg(11.0),
            structural_mass=Mass.from_kg(5.0),
        )

    @staticmethod
    def create_trident_ii_d5_stage1_structure() -> MissileStructure:
        """Trident II D5 Stage 1 structure. ~2,500 kg dry mass."""
        return MissileStructure(
            burning_surface_area=8.0,
            nozzle_throat_area=0.35,
            casing_mass=Mass.from_kg(1_000.0),
            nozzle_mass=Mass.from_kg(500.0),
            electronics_mass=Mass.from_kg(200.0),
            payload_mass=Mass.from_kg(200.0),
            structural_mass=Mass.from_kg(600.0),
        )

    @staticmethod
    def create_arrow3_structure() -> MissileStructure:
        """Arrow 3 boost-stage structure. ~120 kg dry mass."""
        return MissileStructure(
            burning_surface_area=0.3,
            nozzle_throat_area=0.005,
            casing_mass=Mass.from_kg(40.0),
            nozzle_mass=Mass.from_kg(20.0),
            electronics_mass=Mass.from_kg(30.0),
            payload_mass=Mass.from_kg(15.0),
            structural_mass=Mass.from_kg(15.0),
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
