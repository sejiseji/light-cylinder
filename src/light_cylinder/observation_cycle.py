from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite

from light_cylinder.config import (
    OBSERVATION_CYCLE_AFTER_RAIN_DURATION,
    OBSERVATION_CYCLE_CLEAR_DURATION,
    OBSERVATION_CYCLE_CLOUD_SHADOW_AMOUNT,
    OBSERVATION_CYCLE_LIGHT_RAIN_DURATION,
    OBSERVATION_CYCLE_LIGHT_RAIN_MULTIPLIER,
    OBSERVATION_CYCLE_RAIN_DURATION,
    OBSERVATION_CYCLE_SHADOW_DURATION,
)
from light_cylinder.math3d import clamp


class ObservationCyclePhase(Enum):
    CLEAR = "CLEAR"
    SHADOW = "SHADOW"
    LIGHT_RAIN = "LIGHT_RAIN"
    RAIN = "RAIN"
    AFTER_RAIN = "AFTER_RAIN"


@dataclass(frozen=True, slots=True)
class ObservationCycleSample:
    phase: ObservationCyclePhase
    phase_progress: float
    rain_multiplier: float
    light_multiplier: float

    @property
    def is_raining(self) -> bool:
        return self.rain_multiplier > 0.0


@dataclass(slots=True)
class ObservationCycle:
    enabled: bool = False
    elapsed_time: float = 0.0

    def set_enabled(self, enabled: bool) -> None:
        if enabled and not self.enabled:
            self.elapsed_time = 0.0
        self.enabled = enabled

    def toggle(self) -> None:
        self.set_enabled(not self.enabled)

    def update(self, dt: float) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")
        if not self.enabled:
            return
        self.elapsed_time = (self.elapsed_time + dt) % self.duration

    @property
    def duration(self) -> float:
        return sum(_PHASE_DURATIONS)

    def sample(self) -> ObservationCycleSample:
        if not self.enabled:
            return ObservationCycleSample(
                phase=ObservationCyclePhase.CLEAR,
                phase_progress=0.0,
                rain_multiplier=0.0,
                light_multiplier=1.0,
            )

        phase, progress = _phase_at(self.elapsed_time)
        cloud_shadow = _cloud_shadow_for(phase, progress)
        return ObservationCycleSample(
            phase=phase,
            phase_progress=progress,
            rain_multiplier=_rain_multiplier_for(phase, progress),
            light_multiplier=1.0 - OBSERVATION_CYCLE_CLOUD_SHADOW_AMOUNT * cloud_shadow,
        )


_PHASE_DURATIONS = (
    OBSERVATION_CYCLE_CLEAR_DURATION,
    OBSERVATION_CYCLE_SHADOW_DURATION,
    OBSERVATION_CYCLE_LIGHT_RAIN_DURATION,
    OBSERVATION_CYCLE_RAIN_DURATION,
    OBSERVATION_CYCLE_AFTER_RAIN_DURATION,
)
_PHASES = (
    ObservationCyclePhase.CLEAR,
    ObservationCyclePhase.SHADOW,
    ObservationCyclePhase.LIGHT_RAIN,
    ObservationCyclePhase.RAIN,
    ObservationCyclePhase.AFTER_RAIN,
)


def _phase_at(elapsed_time: float) -> tuple[ObservationCyclePhase, float]:
    remaining = elapsed_time
    for phase, duration in zip(_PHASES, _PHASE_DURATIONS, strict=True):
        if remaining < duration:
            return phase, clamp(remaining / duration, 0.0, 1.0)
        remaining -= duration
    return ObservationCyclePhase.AFTER_RAIN, 1.0


def _cloud_shadow_for(phase: ObservationCyclePhase, progress: float) -> float:
    if phase is ObservationCyclePhase.CLEAR:
        return 0.0
    if phase is ObservationCyclePhase.SHADOW:
        return _smoothstep(progress)
    if phase is ObservationCyclePhase.AFTER_RAIN:
        return 1.0 - _smoothstep(progress)
    return 1.0


def _rain_multiplier_for(phase: ObservationCyclePhase, progress: float) -> float:
    if phase is ObservationCyclePhase.LIGHT_RAIN:
        return OBSERVATION_CYCLE_LIGHT_RAIN_MULTIPLIER * _smoothstep(progress)
    if phase is ObservationCyclePhase.RAIN:
        return 1.0
    return 0.0


def _smoothstep(value: float) -> float:
    t = clamp(value, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)
