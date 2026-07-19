from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sin, tau
from random import Random

from light_cylinder.config import (
    RAIN_DEFAULT_INTENSITY,
    RAIN_DROP_COUNT,
    RAIN_INTENSITY_STEP,
    RAIN_MAX_FALL_SPEED,
    RAIN_MIN_FALL_SPEED,
    RAIN_SEED,
    RAIN_SHORT_LENGTHS,
    RAIN_STATIC_STREAK_COUNT,
    RAIN_STATIC_STREAK_FLASH_RATE,
    RAIN_STATIC_STREAK_FLASH_THRESHOLD,
    RAIN_STATIC_STREAK_MAX_HEIGHT_FACTOR,
    RAIN_STATIC_STREAK_MAX_LENGTH,
    RAIN_STATIC_STREAK_MIN_HEIGHT_FACTOR,
    RAIN_STATIC_STREAK_MIN_LENGTH,
)
from light_cylinder.math3d import Vec3, clamp
from light_cylinder.world import CylinderWorld


@dataclass(frozen=True, slots=True)
class RainImpact:
    position: Vec3
    direction: Vec3
    strength: float
    phase: float


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

        head = Vec3(
            self.base_position.x,
            y,
            self.base_position.z,
        )
        tail = Vec3(
            head.x,
            max(world.bottom_y, y - self.length),
            head.z,
        )
        if not world.contains_horizontal(head) and not world.contains_horizontal(tail):
            return None
        return head, tail

    def ground_impact_between(
        self,
        world: CylinderWorld,
        previous_time: float,
        current_time: float,
        wind: Vec3,
    ) -> RainImpact | None:
        if not isfinite(previous_time) or not isfinite(current_time):
            raise ValueError("impact times must be finite")

        if current_time < previous_time:
            current_time += 3600.0

        previous_travel = self._travel_at(world, previous_time)
        current_travel = self._travel_at(world, current_time)
        if current_travel < previous_travel:
            impact_position = self._position_at_travel(world, 1.0, wind)
            if not world.contains_horizontal(impact_position):
                return None
            return RainImpact(
                position=impact_position,
                direction=self._impact_direction(wind),
                strength=self.brightness,
                phase=self.phase,
            )
        return None

    def _travel_at(self, world: CylinderWorld, elapsed_time: float) -> float:
        return (self.phase + elapsed_time * self.fall_speed / world.height) % 1.0

    def _position_at_travel(self, world: CylinderWorld, travel: float, wind: Vec3) -> Vec3:
        return Vec3(
            self.base_position.x,
            world.bottom_y,
            self.base_position.z,
        )

    def _impact_direction(self, wind: Vec3) -> Vec3:
        return Vec3(0.0, -1.0, 0.0)


@dataclass(frozen=True, slots=True)
class StaticRainStreak:
    head_position: Vec3
    length: float
    phase: float
    brightness: float

    def segment_at(self, world: CylinderWorld, elapsed_time: float) -> tuple[Vec3, Vec3] | None:
        if not isfinite(elapsed_time):
            raise ValueError("elapsed time must be finite")

        pulse = (sin(elapsed_time * RAIN_STATIC_STREAK_FLASH_RATE + self.phase) + 1.0) * 0.5
        if pulse < RAIN_STATIC_STREAK_FLASH_THRESHOLD:
            return None

        tail = Vec3(
            self.head_position.x,
            max(world.bottom_y, self.head_position.y - self.length),
            self.head_position.z,
        )
        if not world.contains_horizontal(self.head_position) and not world.contains_horizontal(
            tail
        ):
            return None
        return self.head_position, tail


@dataclass(slots=True)
class RainField:
    drops: tuple[RainDrop, ...]
    static_streaks: tuple[StaticRainStreak, ...] = ()
    elapsed_time: float = 0.0
    intensity: float = RAIN_DEFAULT_INTENSITY

    @classmethod
    def create_default(cls, world: CylinderWorld, _beam: object | None = None) -> RainField:
        rng = Random(RAIN_SEED)
        return cls(
            drops=_generate_drops(world, rng),
            static_streaks=_generate_static_streaks(world, rng),
        )

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

    def static_segments(
        self,
        world: CylinderWorld,
    ) -> tuple[tuple[StaticRainStreak, Vec3, Vec3], ...]:
        segments: list[tuple[StaticRainStreak, Vec3, Vec3]] = []
        active_count = round(len(self.static_streaks) * self.intensity)
        for streak in self.static_streaks[:active_count]:
            segment = streak.segment_at(world, self.elapsed_time)
            if segment is None:
                continue
            start, end = segment
            segments.append((streak, start, end))
        return tuple(segments)

    def ground_impacts_since(
        self,
        world: CylinderWorld,
        previous_time: float,
        wind: Vec3,
    ) -> tuple[RainImpact, ...]:
        impacts: list[RainImpact] = []
        for drop in self.active_drops():
            impact = drop.ground_impact_between(world, previous_time, self.elapsed_time, wind)
            if impact is not None:
                impacts.append(impact)
        return tuple(impacts)


def _generate_drops(
    world: CylinderWorld,
    rng: Random,
) -> tuple[RainDrop, ...]:
    drops: list[RainDrop] = []
    for _index in range(RAIN_DROP_COUNT):
        base = world.sample_bottom_point(rng.random() ** 0.45, rng.random())
        drops.append(
            RainDrop(
                base_position=Vec3(
                    base.x,
                    world.top_y,
                    base.z,
                ),
                phase=rng.random(),
                fall_speed=rng.uniform(RAIN_MIN_FALL_SPEED, RAIN_MAX_FALL_SPEED),
                length=RAIN_SHORT_LENGTHS[rng.randrange(len(RAIN_SHORT_LENGTHS))],
                wind_sensitivity=rng.uniform(0.72, 1.18),
                brightness=rng.uniform(0.72, 1.0),
            )
        )
    return tuple(drops)


def _generate_static_streaks(
    world: CylinderWorld,
    rng: Random,
) -> tuple[StaticRainStreak, ...]:
    streaks: list[StaticRainStreak] = []
    for _index in range(RAIN_STATIC_STREAK_COUNT):
        base = world.sample_bottom_point(rng.random() ** 0.45, rng.random())
        streaks.append(
            StaticRainStreak(
                head_position=Vec3(
                    base.x,
                    world.bottom_y
                    + world.height
                    * rng.uniform(
                        RAIN_STATIC_STREAK_MIN_HEIGHT_FACTOR,
                        RAIN_STATIC_STREAK_MAX_HEIGHT_FACTOR,
                    ),
                    base.z,
                ),
                length=rng.uniform(RAIN_STATIC_STREAK_MIN_LENGTH, RAIN_STATIC_STREAK_MAX_LENGTH),
                phase=rng.random() * tau,
                brightness=rng.uniform(0.78, 1.0),
            )
        )
    return tuple(streaks)
