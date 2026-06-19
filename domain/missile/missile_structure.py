from __future__ import annotations
from dataclasses import dataclass
from domain.universal.mass import Mass

@dataclass(frozen=True, slots=True)
class MissileStructure:
    burning_surface_area: float
    nozzle_throat_area: float
    casing_mass: Mass
    nozzle_mass: Mass
    electronics_mass: Mass
    payload_mass: Mass
    structural_mass: Mass
    # Aerodynamic drag parameters
    drag_curve: tuple[tuple[float, float], ...] # (Mach, Cd) pairs
    cross_section_area: float # A  — reference area in m² (usually πr²)

    def get_drag_coefficient(self, mach: float) -> float:
        """Linearly interpolate the Cd at the given Mach number."""
        if not self.drag_curve:
            return 0.0
        if mach <= self.drag_curve[0][0]:
            return self.drag_curve[0][1]
        if mach >= self.drag_curve[-1][0]:
            return self.drag_curve[-1][1]
        for i in range(len(self.drag_curve) - 1):
            m0, cd0 = self.drag_curve[i]
            m1, cd1 = self.drag_curve[i + 1]
            if m0 <= mach <= m1:
                t = (mach - m0) / (m1 - m0)
                return cd0 + t * (cd1 - cd0)
        return self.drag_curve[-1][1]

    @property
    def dry_mass(self) -> float:
        return (
            self.casing_mass.mass_in_kg +
            self.nozzle_mass.mass_in_kg +
            self.electronics_mass.mass_in_kg +
            self.payload_mass.mass_in_kg +
            self.structural_mass.mass_in_kg
        )