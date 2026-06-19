from __future__ import annotations
import math
import time
from typing import Optional

from domain.events.missile_events import MissileState, MissileTickEvent
from domain.missile.components.propellant_type import PropellantType
from domain.missile.missile import Missile
from domain.missile.phase.boosting_phase import BoostingMissilePhase
from domain.moving_object.moving_object import MovingObject
from domain.universal.air_resistance import AirResistance
from domain.universal.constants import EARTH_GRAVITY, SEA_LEVEL_AIR_DENSITY
from domain.universal.time import Time
from infrastructure.event_bus.event_bus import EventBus


class Reality:
    def __init__(
        self,
        update_ms: int,
        with_gravity: bool,
        with_air_resistance: bool,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._update_ms = update_ms
        self._event_bus = event_bus
        self.with_gravity = with_gravity
        self.with_air_resistance = with_air_resistance

        self._stop = False
        self._elapsed_ms: float = 0.0
        self._initial_propellant_masses: dict[str, float] = {}
        self._terminal_speeds: dict[str, float] = {}

        self.moving_objects: list[MovingObject] = []
        self.explode_objects: list[MovingObject] = []
        self.boosting_phases: list[BoostingMissilePhase] = []

    def load_missiles_to_simulation(self, missiles: list[Missile]) -> None:
        for missile in missiles:
            self._initial_propellant_masses[missile.name] = missile.propellant.mass

            if missile.propellant.type is PropellantType.NEPE:
                phase = BoostingMissilePhase.from_nepe(missile)
            elif missile.propellant.type is PropellantType.KNSU:
                phase = BoostingMissilePhase.from_knsu(missile)
            elif missile.propellant.type is PropellantType.LIQUID:
                phase = BoostingMissilePhase.from_liquid(missile)
            elif missile.propellant.type is PropellantType.APCP:
                phase = BoostingMissilePhase.from_apcp(missile)
            else:
                raise ValueError(f"Unknown propellant type: {missile.propellant.type}")

            self.boosting_phases.append(phase)

            # Tsiolkovsky ideal Δv estimate (v_e × ln(m₀ / m_dry)) — the terminal
            # speed target the live tracker renders against.
            self._terminal_speeds[missile.name] = phase.exhaust_velocity * math.log(
                missile.mass / missile.structure.dry_mass
            )

            self.moving_objects.append(missile)

    def start(self, missiles: list[Missile]) -> None:
        self.load_missiles_to_simulation(missiles)

        while not self._stop and self.moving_objects:
            self.__update()
            # Real-time sleep during boost for live tracking; fast-forward during coast.
            if self.boosting_phases:
                time.sleep(self._update_ms / 1000)

        self.terminate()

    def terminate(self) -> None:
        self._stop = True

    # ── private ───────────────────────────────────────────────────────────────

    def __update(self) -> None:
        dt = Time.from_seconds(self._update_ms / 1000)
        self._elapsed_ms += self._update_ms

        exhausted = [p for p in self.boosting_phases if p.exhaust(dt) == 0]
        for phase in exhausted:
            self.boosting_phases.remove(phase)

        for obj in self.moving_objects:
            obj.coords.add_velocity(obj.velocity, dt)

            if self.with_gravity:
                obj.velocity.y.add(EARTH_GRAVITY * dt.seconds * -1)

            if self.with_air_resistance and isinstance(obj, Missile):
                AirResistance().apply_drag(obj, dt)

            if self._event_bus and isinstance(obj, Missile):
                initial_propellant = self._initial_propellant_masses.get(obj.name, 0.0)
                fuel_pct = obj.propellant.mass / initial_propellant if initial_propellant > 0 else 0.0

                self._event_bus.publish(
                  MissileTickEvent.build(
                    obj.id,
                    obj.name,
                    obj.velocity,
                    obj.coords,
                    obj.state,
                    self._elapsed_ms,
                    self._terminal_speeds.get(obj.name, 0.0),
                    fuel_pct,
                  )
                )
                
                if obj.state == MissileState.LANDED:
                  self.moving_objects.remove(obj)
                  self.explode_objects.append(obj)