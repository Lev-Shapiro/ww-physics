from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class EfficiencyFactor:
    """
    Represents the real-world efficiency factor (often denoted as a performance coefficient) 
    applied to ideal thermodynamic calculations. 
    
    Theoretical thermodynamic calculations (like those from RocketCEA) assume perfect, 
    instantaneous combustion, infinite reaction rates, complete mixing, and an ideal 
    isentropic expansion through the nozzle. However, real rocket motors suffer from 
    several unavoidable losses:
    
    - Combustion Inefficiency: Unburned or partially burned propellant, or poor mixing.
    - Two-Phase Flow Losses: Condensed particles (like liquid/solid Al2O3 from Aluminum fuel) 
      cannot expand like a gas, causing thermal and velocity lags.
    - Divergence Losses: Thrust is lost because the nozzle exhaust expands at an angle 
      rather than perfectly straight backwards.
    - Boundary Layer & Heat Transfer: Friction and heat loss to the nozzle and chamber walls.
    
    This factor is applied directly to the ideal Specific Impulse (Isp) or ideal thrust 
    to yield a much more realistic estimate of the actual delivered performance.
    """
    value: float

    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"Efficiency factor must be between 0.0 and 1.0, got {self.value}")

    @classmethod
    def from_value(cls, value: float) -> EfficiencyFactor:
        """Create a custom efficiency factor."""
        return cls(value=value)

    @classmethod
    def low_quality(cls) -> EfficiencyFactor:
        """
        Amateur or poorly optimized motors.
        Significant two-phase flow losses, poor mixing, or simple low-expansion conical nozzles.
        Typically ~85% efficiency.
        """
        return cls(value=0.85)

    @classmethod
    def medium_quality(cls) -> EfficiencyFactor:
        """
        Standard hobby or basic commercial motors.
        Decent combustion, moderate aluminum content, standard nozzle geometry.
        Typically ~90% efficiency.
        """
        return cls(value=0.90)

    @classmethod
    def high_quality(cls) -> EfficiencyFactor:
        """
        Professional or well-optimized aerospace motors.
        Optimized bell nozzle contours, high combustion efficiency, minimized boundary layer losses.
        Typically ~95% efficiency.
        """
        return cls(value=0.95)

    @classmethod
    def extremely_high_quality(cls) -> EfficiencyFactor:
        """
        State-of-the-art aerospace solid rocket motors (e.g., Space Shuttle SRB, Ariane 5 boosters).
        Highly optimized 3D nozzle contours, near-perfect mixing, finely-tuned propellant grains.
        Typically ~98% efficiency.
        """
        return cls(value=0.98)
