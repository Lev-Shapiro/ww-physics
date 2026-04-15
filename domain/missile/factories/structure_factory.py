from domain.missile.missile import MissileStructure
from domain.universal.mass import Mass

class StructureFactory:
    @staticmethod
    def create_tamir_structure() -> MissileStructure:
        """Tamir interceptor structure. ~28 kg dry mass (casing, nozzle, electronics, warhead)."""
        return MissileStructure(
            burning_surface_area=0.15,
            nozzle_throat_area=0.002,
            casing_mass=Mass.from_kg(5.0),
            nozzle_mass=Mass.from_kg(4.0),
            electronics_mass=Mass.from_kg(10.0),
            payload_mass=Mass.from_kg(11.0),
            structural_mass=Mass.from_kg(10.0),
            # Fuel: 50kg, rest: 40kg
            # Total: 90kg
        )

    @staticmethod
    def create_qassam_structure() -> MissileStructure:
        """Qassam-class rocket structure. Lightweight steel tube with minimal guidance."""
        return MissileStructure(
            burning_surface_area=0.035,
            nozzle_throat_area=0.00065,
            casing_mass=Mass.from_kg(15),
            nozzle_mass=Mass.from_kg(10),
            electronics_mass=Mass.from_kg(0),
            payload_mass=Mass.from_kg(15),
            structural_mass=Mass.from_kg(30),
            # Fuel: 20kg, rest: 70kg
            # Total: 30kg
        )

    @staticmethod
    def create_v2_structure() -> MissileStructure:
        """V-2 rocket structure. Large liquid propellant rocket."""
        return MissileStructure(
            burning_surface_area=1.0,  # Approximate
            nozzle_throat_area=0.05,  # Approximate
            casing_mass=Mass.from_kg(1000),
            nozzle_mass=Mass.from_kg(300),
            electronics_mass=Mass.from_kg(200),
            payload_mass=Mass.from_kg(1000),  # Warhead
            structural_mass=Mass.from_kg(1500),
            # Fuel: 8700kg, warhead: 1000kg, rest: 3000kg
            # Total: 12800kg
        )
