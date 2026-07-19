from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, tau
from random import Random

from light_cylinder.config import (
    LIGHT_BEAM_RADIUS,
    RAIN_DEFAULT_INTENSITY,
    RAIN_DROP_COUNT,
    RAIN_INTENSITY_STEP,
    RAIN_MAX_FALL_SPEED,
    RAIN_MAX_LENGTH,
    RAIN_MIN_FALL_SPEED,
    RAIN_MIN_LENGTH,
    RAIN_SEED,
    RAIN_WIND_DRIFT_SCALE,
    RAIN_WIND_TILT_SCALE,
)
from light_cylinder.light import LightBeam
from light_cylinder.math3d import Vec3, clamp
from light_cylinder.world import CylinderWorld


@dataclass(frozen=True, slots=True)
class RainDrop:
    base_position: Vec3
    phase: float
    fall_speed: float
    length: float
    wind_sensitivity: float
    brightness: float

    def segment_at(
        self,
        world: CylinderWorld,
        elapsed_time: float,
        wind: Vec3,
    ) -> tuple[Vec3, Vec3] | None:
        if not isfinite(elapsed_time):
            raise ValueError("elapsed time must be finite")

        travel = (self.phase + elapsed_time * self.fall_speed / world.height) % 1.0
        y = world.top_y - travel * world.height
        if y <= world.bottom_y:
            return None

        horizontal_drift = wind * (travel * RAIN_WIND_DRIFT_SCALE * self.wind_sensitivity)
        tilted_tail = wind * (RAIN_WIND_TILT_SCALE * self.wind_sensitivity)
        head = Vec3(
            self.base_position.x + horizontal_drift.x,
            y,
            self.base_position.z + horizontal_drift.z,
        )
        tail = Vec3(
            head.x - tilted_tail.x,
            max(world.bottom_y, y - self.length),
            head.z - tilted_tail.z,
        )
        if not world.contains_horizontal(head) and not world.contains_horizontal(tail):
            return None
        return head, tail


@dataclass(slots=True)
class RainField:
    drops: tuple[RainDrop, ...]
    elapsed_time: float = 0.0
    intensity: float = RAIN_DEFAULT_INTENSITY

    @classmethod
    def create_default(cls, world: CylinderWorld, beam: LightBeam | None = None) -> RainField:
        rng = Random(RAIN_SEED)
        return cls(drops=_generate_drops(world, rng, beam))

    def update(self, dt: float) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")
        self.elapsed_time = (self.elapsed_time + dt) % 3600.0

    def set_intensity(self, intensity: float) -> None:
        if not isfinite(intensity):
            raise ValueError("rain intensity must be finite")
        self.intensity = clamp(intensity, 0.0, 1.0)

    def adjust_intensity(self, steps: float) -> None:
        self.set_intensity(self.intensity + steps * RAIN_INTENSITY_STEP)

    @property
    def active_drop_count(self) -> int:
        return round(len(self.drops) * self.intensity)

    def active_drops(self) -> tuple[RainDrop, ...]:
        return self.drops[: self.active_drop_count]

    def segments(self, world: CylinderWorld, wind: Vec3) -> tuple[tuple[RainDrop, Vec3, Vec3], ...]:
        segments: list[tuple[RainDrop, Vec3, Vec3]] = []
        for drop in self.active_drops():
            segment = drop.segment_at(world, self.elapsed_time, wind)
            if segment is None:
                continue
            start, end = segment
            segments.append((drop, start, end))
        return tuple(segments)


def _generate_drops(
    world: CylinderWorld,
    rng: Random,
    beam: LightBeam | None,
) -> tuple[RainDrop, ...]:
    drops: list[RainDrop] = []
    for _index in range(RAIN_DROP_COUNT):
        if beam is not None and rng.random() < 0.78:
            base = _sample_light_corridor_point(world, beam, rng)
        else:
            base = world.sample_bottom_point(rng.random() ** 0.55, rng.random())
        angle = rng.random() * tau
        radius_jitter = rng.uniform(0.0, world.radius * 0.08)
        drops.append(
            RainDrop(
                base_position=Vec3(
                    base.x + cos(angle) * radius_jitter,
                    world.top_y,
                    base.z + sin(angle) * radius_jitter,
                ),
                phase=rng.random(),
                fall_speed=rng.uniform(RAIN_MIN_FALL_SPEED, RAIN_MAX_FALL_SPEED),
                length=rng.uniform(RAIN_MIN_LENGTH, RAIN_MAX_LENGTH),
                wind_sensitivity=rng.uniform(0.72, 1.18),
                brightness=rng.uniform(0.72, 1.0),
            )
        )
    return tuple(drops)


def _sample_light_corridor_point(
    world: CylinderWorld,
    beam: LightBeam,
    rng: Random,
) -> Vec3:
    basis_u, basis_v = beam.basis()
    for _attempt in range(16):
        target_y = world.bottom_y + rng.random() * world.height
        if beam.direction.y == 0.0:
            axial_position = rng.random() * beam.length
        else:
            axial_position = (target_y - beam.origin.y) / beam.direction.y
        axis_point = beam.axis_point(clamp(axial_position, 0.0, beam.length))
        radius = LIGHT_BEAM_RADIUS * 0.82 * (rng.random() ** 0.7)
        angle = rng.random() * tau
        offset = basis_u * (cos(angle) * radius) + basis_v * (sin(angle) * radius)
        point = Vec3(axis_point.x + offset.x, world.top_y, axis_point.z + offset.z)
        if world.contains_horizontal(point):
            return point
    return world.sample_bottom_point(rng.random() ** 0.55, rng.random())
