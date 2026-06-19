import math

from domain.missile.missile import MissileStructure
from domain.universal.mass import Mass

class StructureFactory:
    @staticmethod
    def create_tamir_structure() -> MissileStructure:
        """
        Tamir interceptor structure. ~62 kg dry mass.
        Total mass (with 28kg fuel) = 90kg.
        Aerodynamics: Mach-dependent Cd curve between 0.2 and 0.75.
        """
        return MissileStructure(
            burning_surface_area=0.15,
            nozzle_throat_area=0.002,
            casing_mass=Mass.from_kg(10.0),
            nozzle_mass=Mass.from_kg(5.0),
            electronics_mass=Mass.from_kg(15.0),
            payload_mass=Mass.from_kg(11.0),
            structural_mass=Mass.from_kg(21.0),
            drag_curve=(
                (0.00, 0.25),
                (0.80, 0.30),
                (1.00, 0.75),   # transonic peak
                (1.20, 0.65),
                (1.50, 0.55),
                (2.00, 0.45),
                (3.00, 0.35),
                (4.50, 0.30),
            ),
            cross_section_area=math.pi * 0.08 ** 2,  # 0.0201 m²
        )

    @staticmethod
    def create_qassam_structure() -> MissileStructure:
        # Dry mass trimmed 70 -> 64 kg (lighter casing/nozzle and a realistic ~10 kg
        # warhead) to raise the propellant mass fraction and ideal Δv.
        return MissileStructure(
            burning_surface_area=0.035,
            nozzle_throat_area=0.00085,  # was 0.00065 — wider throat, faster burn
            casing_mass=Mass.from_kg(13),
            nozzle_mass=Mass.from_kg(8),
            electronics_mass=Mass.from_kg(0),
            payload_mass=Mass.from_kg(10),
            structural_mass=Mass.from_kg(33),
            # Cd curve scaled ~0.55 — the original transonic peak (0.85) was
            # unrealistically high for a finned rocket and bled most of the coast
            # range, especially with the wider 170 mm body.
            drag_curve=(
                (0.00, 0.193),
                (0.80, 0.220),
                (1.00, 0.468),
                (1.20, 0.413),
                (1.50, 0.358),
                (2.00, 0.303),
                (3.00, 0.248),
            ),
            cross_section_area=math.pi * 0.085 ** 2,  # 0.022698 m²
        )

    @staticmethod
    def create_v2_structure() -> MissileStructure:
        return MissileStructure(
            burning_surface_area=1.0,
            nozzle_throat_area=0.147,
            casing_mass=Mass.from_kg(1000),
            nozzle_mass=Mass.from_kg(300),
            electronics_mass=Mass.from_kg(200),
            payload_mass=Mass.from_kg(1000),
            structural_mass=Mass.from_kg(1500),
            drag_curve=(
                (0.00, 0.15),
                (0.80, 0.20),
                (1.00, 0.55),
                (1.20, 0.45),
                (1.50, 0.35),
                (2.00, 0.25),
                (3.00, 0.20),
                (5.00, 0.15),
            ),
            cross_section_area=math.pi * 0.8255 ** 2,  # 2.141 m²
        )
