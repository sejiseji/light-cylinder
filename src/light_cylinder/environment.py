from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite

from light_cylinder.config import (
    AFTER_RAIN_CLEAR_WETNESS,
    AFTER_RAIN_CLOUD_RECOVERY_RATE,
    AFTER_RAIN_DRY_RATE_MAX,
    AFTER_RAIN_DRY_RATE_MIN,
    AFTER_RAIN_LIGHT_SHADOW_AMOUNT,
    AFTER_RAIN_MIN_DURATION,
    AFTER_RAIN_MIN_WETNESS,
    AFTER_RAIN_REFLECTION_DECAY_RATE,
)
from light_cylinder.math3d import clamp


class EnvironmentPhase(Enum):
    CLEAR = "CLEAR"
    RAIN = "RAIN"
    AFTER_RAIN = "AFTER_RAIN"


@dataclass(slots=True)
class EnvironmentState:
    phase: EnvironmentPhase = EnvironmentPhase.CLEAR
    phase_time: float = 0.0
    cloud_shadow: float = 0.0
    wet_reflection: float = 0.0

    def set_rain(self, enabled: bool, wetness: float) -> None:
        if enabled:
            if self.phase is not EnvironmentPhase.RAIN:
                self.phase = EnvironmentPhase.RAIN
                self.phase_time = 0.0
            self.cloud_shadow = 1.0
            return

        if self.phase is EnvironmentPhase.RAIN and wetness >= AFTER_RAIN_MIN_WETNESS:
            self.phase = EnvironmentPhase.AFTER_RAIN
            self.phase_time = 0.0
            self.wet_reflection = max(self.wet_reflection, wetness)
            return

        if wetness < AFTER_RAIN_MIN_WETNESS:
            self.phase = EnvironmentPhase.CLEAR
            self.phase_time = 0.0

    def update(self, dt: float, wetness: float) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")

        self.phase_time += dt
        if self.phase is EnvironmentPhase.RAIN:
            self.cloud_shadow = 1.0
            self.wet_reflection = max(self.wet_reflection, wetness)
            return

        self.cloud_shadow = max(0.0, self.cloud_shadow - dt * AFTER_RAIN_CLOUD_RECOVERY_RATE)
        self.wet_reflection = max(0.0, self.wet_reflection - dt * AFTER_RAIN_REFLECTION_DECAY_RATE)

        if self.phase is EnvironmentPhase.AFTER_RAIN and self._can_return_to_clear(wetness):
            self.phase = EnvironmentPhase.CLEAR
            self.phase_time = 0.0

    @property
    def is_raining(self) -> bool:
        return self.phase is EnvironmentPhase.RAIN

    @property
    def is_after_rain(self) -> bool:
        return self.phase is EnvironmentPhase.AFTER_RAIN

    @property
    def light_multiplier(self) -> float:
        return 1.0 - AFTER_RAIN_LIGHT_SHADOW_AMOUNT * self.cloud_shadow

    def dry_rate_multiplier(self, wetness: float) -> float:
        if self.phase is EnvironmentPhase.RAIN:
            return 0.18
        if self.phase is EnvironmentPhase.AFTER_RAIN:
            dry_progress = 1.0 - clamp(wetness, 0.0, 1.0)
            return (
                AFTER_RAIN_DRY_RATE_MIN
                + (AFTER_RAIN_DRY_RATE_MAX - AFTER_RAIN_DRY_RATE_MIN) * dry_progress
            )
        return 1.0

    def effective_floor_wetness(self, wetness: float) -> float:
        return clamp(max(wetness, self.wet_reflection * 0.65), 0.0, 1.0)

    def _can_return_to_clear(self, wetness: float) -> bool:
        return self.phase_time >= AFTER_RAIN_MIN_DURATION and wetness <= AFTER_RAIN_CLEAR_WETNESS
