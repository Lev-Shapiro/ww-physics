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
    def create_jerico_iron_man_structure() -> MissileStructure:
        """
        Fictional Iron Man "Jericho" structure. Large tactical solid-fuel missile
        (~0.5 m body) carrying a heavy ~600 kg cluster-submunition payload.
        Dry mass = 350 + 120 + 90 + 600 + 240 = 1400 kg.
        Total mass (with 1500 kg propellant) = 2900 kg.
        """
        return MissileStructure(
            burning_surface_area=2.5,
            nozzle_throat_area=0.02,
            casing_mass=Mass.from_kg(350),
            nozzle_mass=Mass.from_kg(120),
            electronics_mass=Mass.from_kg(90),   # guidance for cluster dispersal
            payload_mass=Mass.from_kg(600),      # cluster of submunitions
            structural_mass=Mass.from_kg(240),
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
            cross_section_area=math.pi * 0.25 ** 2,  # 0.196 m²
        )

    @staticmethod
    def create_starship_v3_structure() -> MissileStructure:
        """
        SpaceX Starship V3 (Block 3) full stack, 9 m diameter, ~124 m tall.

        Single-stage limitation: this model can't stage, so the throat area
        represents the 33 Super Heavy Raptor 3 engines firing at liftoff
        (≈1.30 m² total, ≈0.224 m per engine), sized to ~80 MN / ~23,600 kg/s.

        Mass budget (dry ≈ 320 t + 100 t payload = 420 t inert):
          casing/tanks 140 t, engines 42×1525 kg ≈ 64 t, avionics 5 t,
          payload 100 t, remaining structure 111 t.
        Total liftoff mass = 420 t inert + 5,650 t propellant ≈ 6,070 t.
        """
        return MissileStructure(
            burning_surface_area=1.0,        # unused for liquid propellant
            nozzle_throat_area=1.30,         # 33 booster Raptor 3 throats at liftoff
            casing_mass=Mass.from_kg(140_000),
            nozzle_mass=Mass.from_kg(64_050),   # 42 Raptor 3 @ 1,525 kg
            electronics_mass=Mass.from_kg(5_000),
            payload_mass=Mass.from_kg(100_000),  # 100 t to LEO
            structural_mass=Mass.from_kg(111_000),
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
            cross_section_area=math.pi * 4.5 ** 2,  # 63.617 m² (9 m diameter)
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
