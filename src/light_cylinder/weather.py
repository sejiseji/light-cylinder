from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, pi, sin

from light_cylinder.config import (
    GUST_DURATION,
    GUST_INTERVAL,
    GUST_STRENGTH,
    WIND_BASE_DIRECTION_ANGLE,
    WIND_BASE_SPEED,
    WIND_BLADE_PHASE_SCALE,
    WIND_DIRECTION_SWAY_AMOUNT,
    WIND_DIRECTION_SWAY_RATE,
    WIND_SEED,
    WIND_SLOW_PULSE_AMOUNT,
    WIND_SLOW_PULSE_RATE,
    WIND_SPATIAL_FREQUENCY_X,
    WIND_SPATIAL_FREQUENCY_Z,
    WIND_TIME_WRAP_SECONDS,
)
from light_cylinder.math3d import Vec3


@dataclass(slots=True)
class WindField:
    elapsed_time: float
    base_direction: Vec3
    base_speed: float
    seed: int = WIND_SEED

    @classmethod
    def create_default(cls) -> WindField:
        return cls(
            elapsed_time=0.0,
            base_direction=Vec3(
                cos(WIND_BASE_DIRECTION_ANGLE), 0.0, sin(WIND_BASE_DIRECTION_ANGLE)
            ),
            base_speed=WIND_BASE_SPEED,
            seed=WIND_SEED,
        )

    def update(self, dt: float) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")
        self.elapsed_time = (self.elapsed_time + dt) % WIND_TIME_WRAP_SECONDS

    def sample(self, position: Vec3, phase: float = 0.0) -> Vec3:
        spatial_phase = self.spatial_phase(position)
        pulse = 1.0 + WIND_SLOW_PULSE_AMOUNT * sin(
            self.elapsed_time * WIND_SLOW_PULSE_RATE
            + spatial_phase
            + phase * WIND_BLADE_PHASE_SCALE
        )
        local_angle = WIND_BASE_DIRECTION_ANGLE + WIND_DIRECTION_SWAY_AMOUNT * sin(
            spatial_phase + self.elapsed_time * WIND_DIRECTION_SWAY_RATE
        )
        strength = max(0.0, self.base_speed * pulse + self.current_gust_strength)
        return Vec3(cos(local_angle) * strength, 0.0, sin(local_angle) * strength)

    def spatial_phase(self, position: Vec3) -> float:
        return position.x * WIND_SPATIAL_FREQUENCY_X + position.z * WIND_SPATIAL_FREQUENCY_Z

    @property
    def current_gust_strength(self) -> float:
        cycle_duration = GUST_INTERVAL + GUST_DURATION
        cycle_time = (self.elapsed_time + self._seed_time_offset()) % cycle_duration
        if cycle_time < GUST_INTERVAL:
            return 0.0
        normalized = (cycle_time - GUST_INTERVAL) / GUST_DURATION
        return GUST_STRENGTH * (sin(pi * normalized) ** 2)

    def _seed_time_offset(self) -> float:
        return (self.seed % 997) * 0.001
