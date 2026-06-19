from dataclasses import dataclass
import math

from domain.missile.missile import Missile
from domain.universal.constants import SEA_LEVEL_AIR_DENSITY, STRATOSPHERE_SCALE_HEIGHT_M, TROPOPAUSE_ALT_M, TROPOPAUSE_DENSITY_KG_M3, TROPOPAUSE_TEMPERATURE_K
from domain.universal.time import Time

@dataclass(frozen=True, slots=True)
class AirResistance:
  def _air_density(self, altitude_m: float) -> float:
      """ISA air density [kg/m³], valid 0–86 km."""
      h = max(0.0, altitude_m)
      if h < TROPOPAUSE_ALT_M:
          T = 288.15 - 0.0065 * h
          return SEA_LEVEL_AIR_DENSITY * (T / 288.15) ** 4.2561
      return TROPOPAUSE_DENSITY_KG_M3 * math.exp(
          -(h - TROPOPAUSE_ALT_M) / STRATOSPHERE_SCALE_HEIGHT_M
      )
      
  def _speed_of_sound(self, altitude_m: float) -> float:
    """ISA speed of sound [m/s]  (γ = 1.4, dry air)."""
    h = max(0.0, altitude_m)
    T = 288.15 - 0.0065 * h if h < TROPOPAUSE_ALT_M else TROPOPAUSE_TEMPERATURE_K
    return math.sqrt(1.4 * 8.314 / 0.0289644 * T)
  
  def apply_drag(self, missile: Missile, dt_s: Time) -> None:
    """
    Apply aerodynamic drag to missile velocity for one time step.

    F_drag = ½ · ρ(h) · v² · Cd(M) · A   (opposes velocity direction)
    a_drag = F_drag / m

    Cd is the structure's base drag coefficient scaled by a Mach-dependent
    factor that captures the transonic wave-drag rise.
    """
    vx = missile.velocity.x.meters_per_second
    vy = missile.velocity.y.meters_per_second
    vz = missile.velocity.z.meters_per_second
    v_sq = vx * vx + vy * vy + vz * vz

    if v_sq < 1e-6:
        return

    v_mag = math.sqrt(v_sq)
    mach = v_mag / self._speed_of_sound(missile.coords.y)
    cd = missile.structure.get_drag_coefficient(mach)

    rho = self._air_density(missile.coords.y)
    a_drag = 0.5 * rho * v_sq * cd * missile.structure.cross_section_area / missile.mass

    scale = -a_drag * dt_s.seconds / v_mag
    missile.velocity.x.add(vx * scale)
    missile.velocity.y.add(vy * scale)
    missile.velocity.z.add(vz * scale)

