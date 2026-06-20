from __future__ import annotations

from dataclasses import dataclass

from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from domain.events.missile_events import MissileTickEvent
from domain.missile.missile import MissileState
from infrastructure.event_bus.event_bus import EventBus

_LABEL_W = 8
_BAR_W = 20
_VALUE_W = 11

def _bar(ratio: float, filled: str = "█", empty: str = "░", w: int = _BAR_W) -> str:
    ratio = max(0.0, min(1.0, ratio))
    n = round(ratio * w)
    return filled * n + empty * (w - n)

def _speed_row(
    label: str,
    val: float,
    max_v: float,
    bar_char: str,
    bar_style: str,
    value_style: str,
) -> Text:
    ratio = min(1.0, val / max_v) if max_v > 0 else 0.0
    t = Text()
    t.append(f"  {label:<{_LABEL_W}}  ", style="dim")
    t.append(_bar(ratio, filled=bar_char), style=bar_style)
    t.append(f"  {val:>{_VALUE_W},.1f} m/s", style=value_style)
    return t

@dataclass
class _MissileTrack:
    peak_speed: float = 0.0
    prev_speed: float | None = None
    prev_elapsed_ms: float | None = None
    panel: Panel | None = None

class VelocityTrackerService:
    def __init__(self, event_bus: EventBus) -> None:
        # Keyed by missile_id so several missiles can be tracked concurrently
        # without sharing peak / acceleration baselines.
        self._tracks: dict[str, _MissileTrack] = {}

        self._live = Live(
            self._idle_panel(),
            refresh_per_second=12,
            screen=False,
            transient=False,
        )
        event_bus.subscribe(MissileTickEvent, self._on_tick)

    # ── lifecycle ─────────────────────────────────────────────────────────────

    def start(self) -> None:
        # Reset per-flight derived state so a reused tracker doesn't carry a
        # previous run's peak speed / acceleration baselines into the next run.
        self._tracks.clear()
        self._live.update(self._idle_panel())
        self._live.start(refresh=True)

    def stop(self) -> None:
        self._live.stop()

    # ── event handling ──────────────────────────────────────────────────────────

    def _on_tick(self, event: MissileTickEvent) -> None:
        track = self._tracks.setdefault(event.missile_id, _MissileTrack())

        speed = event.velocity_vector.total.meters_per_second
        track.peak_speed = max(track.peak_speed, speed)

        if track.prev_speed is None or track.prev_elapsed_ms is None:
            accel = 0.0
        else:
            dt = (event.elapsed_ms - track.prev_elapsed_ms) / 1000.0
            accel = (speed - track.prev_speed) / dt if dt > 0 else 0.0

        track.prev_speed = speed
        track.prev_elapsed_ms = event.elapsed_ms

        track.panel = self._render(event, track, speed, accel)

        self._live.update(self._compose())

    def _compose(self):
        """Lay every tracked missile's panel side by side in one renderable."""
        panels = [t.panel for t in self._tracks.values() if t.panel is not None]
        if not panels:
            return self._idle_panel()
        return Columns(panels, equal=True, expand=False)

    # ── rendering ─────────────────────────────────────────────────────────────

    def _idle_panel(self) -> Panel:
        return Panel(
            Align.center(Text("🚀  awaiting launch…", style="dim")),
            box=box.ROUNDED,
            border_style="dim",
            padding=(1, 1),
            width=58,
        )

    def _render(self, event: MissileTickEvent, track: _MissileTrack, speed: float, accel: float) -> Panel:
        vx = event.velocity_vector.x.meters_per_second
        vy = event.velocity_vector.y.meters_per_second
        vz = event.velocity_vector.z.meters_per_second
        altitude = event.coords.y
        is_boosting = event.state == MissileState.BOOSTING

        max_v = max(event.terminal_speed, track.peak_speed, speed, 100.0)

        # ── header ────────────────────────────────────────────────────────────
        phase_style = "bold green" if is_boosting else "bold yellow"
        phase_label = "● BOOSTING" if is_boosting else "● COASTING"

        header = Text(justify="center")
        header.append("🚀  ")
        header.append(event.missile_name, style="bold white")
        header.append("  ·  ")
        header.append(phase_label, style=phase_style)

        # ── speed bars ────────────────────────────────────────────────────────
        speed_row = _speed_row("SPEED", speed, max_v, "█", "bold cyan", "bold white")
        term_row = _speed_row("TERMINAL", event.terminal_speed, max_v, "▬", "dim white", "dim")
        peak_row = _speed_row("PEAK", track.peak_speed, max_v, "▓", "blue", "blue")

        # ── velocity components ───────────────────────────────────────────────
        comp = Text()
        comp.append("  ")
        comp.append(f"Vx {vx:>8.1f}", style="cyan")
        comp.append("  │  ", style="dim")
        comp.append(f"Vy {vy:>8.1f}", style="cyan")
        comp.append("  │  ", style="dim")
        comp.append(f"Vz {vz:>6.1f}", style="cyan")
        comp.append("  m/s", style="dim")
        
        # --- coords ---
        coords_line = Text()
        coords_line.append(f"{event.coords.x:>10,.0f} m", style="white")
        coords_line.append(f"  │  ", style="dim")
        coords_line.append(f"{event.coords.y:>10,.0f} m", style="white")
        coords_line.append(f"  │  ", style="dim")
        coords_line.append(f"{event.coords.z:>10,.0f} m", style="white")
        coords_line.append("  m", style="dim")

        # ── acceleration ──────────────────────────────────────────────────────
        # `accel` = d|v|/dt — rate of change of speed magnitude.
        # The label distinguishes thrust-driven acceleration from gravitational
        # speed gain during descent (both show positive d|v|/dt but for
        # completely different physical reasons).
        a = accel
        if is_boosting:
            if a > 100:
                sym, ac_st, ac_label = "↑↑↑", "bold green", "THRUSTING"
            elif a > 10:
                sym, ac_st, ac_label = "↑↑ ", "green", "THRUSTING"
            else:
                sym, ac_st, ac_label = "↑  ", "green", "THRUSTING"
        else:
            # Coast phase: positive = falling (gravity adds to speed),
            # negative = ascending (gravity removes from speed).
            if a > 5:
                sym, ac_st, ac_label = "↘  ", "yellow", "FALLING"
            elif a < -5:
                sym, ac_st, ac_label = "↗  ", "cyan", "ASCENDING"
            else:
                sym, ac_st, ac_label = "→  ", "dim", "COASTING"

        sign = "+" if a >= 0 else ""
        accel_line = Text()
        accel_line.append(f"  {'ACCEL':<{_LABEL_W}}  ", style="dim")
        accel_line.append(f"{sym}  {sign}{a:.1f} m/s²", style=ac_st)
        accel_line.append(f"   [{ac_label}]", style="dim")

        # ── fuel & altitude ───────────────────────────────────────────────────
        fuel_pct = max(0.0, event.fuel_pct)
        fc = "cyan" if fuel_pct > 0.5 else ("yellow" if fuel_pct > 0.2 else "red")

        fuel_line = Text()
        fuel_line.append(f"  {'FUEL':<{_LABEL_W}}  ", style="dim")
        fuel_line.append(_bar(fuel_pct), style=fc)
        fuel_line.append(f"  {fuel_pct * 100:>{_VALUE_W}.1f}%", style=fc)

        alt_line = Text()
        alt_line.append(f"  {'ALT':<{_LABEL_W}}  ", style="dim")
        alt_line.append(f"{altitude:>10,.0f} m", style="white")
        alt_line.append(f"   T+{event.elapsed_ms / 1000:.1f}s", style="dim")

        # ── compose ───────────────────────────────────────────────────────────
        border_style = "cyan" if is_boosting else "yellow"
        sep = Rule(style="dim")

        return Panel(
            Group(
                Text(""),
                Align.center(header),
                Text(""),
                speed_row,
                term_row,
                peak_row,
                Text(""),
                sep,
                comp,
                sep,
                coords_line,
                sep,
                accel_line,
                sep,
                fuel_line,
                alt_line,
                Text(""),
            ),
            box=box.ROUNDED,
            border_style=border_style,
            padding=(0, 1),
            width=58,
        )
