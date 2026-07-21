from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, tau
from random import Random

from light_cylinder.config import (
    FOXTAIL_COUNT,
    FOXTAIL_HEAD_LAG_FACTOR,
    FOXTAIL_HEAD_LENGTH_MAX,
    FOXTAIL_HEAD_LENGTH_MIN,
    FOXTAIL_HEAD_SEGMENTS_MAX,
    FOXTAIL_HEAD_SEGMENTS_MIN,
    FOXTAIL_HEIGHT_MAX_FACTOR,
    FOXTAIL_HEIGHT_MIN_FACTOR,
    FOXTAIL_NATURAL_BEND_MAX,
    FOXTAIL_NATURAL_BEND_MIN,
    FOXTAIL_RAIN_DROOP_SCALE,
    FOXTAIL_SEED,
    FOXTAIL_STEM_SEGMENTS,
    FOXTAIL_WIND_RESPONSE_SCALE,
    GRASS_MAX_HEIGHT,
)
from light_cylinder.math3d import Vec3, clamp
from light_cylinder.world import CylinderWorld


@dataclass(frozen=True, slots=True)
class Foxtail:
    base: Vec3
    height: float
    natural_bend: Vec3
    stiffness: float
    phase: float
    head_length: float
    head_segments: int


@dataclass(frozen=True, slots=True)
class FoxtailShape:
    stem_points: tuple[Vec3, ...]
    head_points: tuple[Vec3, ...]
    droplet_points: tuple[Vec3, ...]


@dataclass(frozen=True, slots=True)
class FoxtailField:
    foxtails: tuple[Foxtail, ...]
    seed: int

    @classmethod
    def generate(
        cls,
        world: CylinderWorld,
        seed: int = FOXTAIL_SEED,
        count: int = FOXTAIL_COUNT,
    ) -> FoxtailField:
        if count < 0:
            raise ValueError("foxtail count must be non-negative")
        rng = Random(seed)
        foxtails: list[Foxtail] = []
        for index in range(count):
            base = _sample_foxtail_base(world, rng, index, count)
            height = GRASS_MAX_HEIGHT * rng.uniform(
                FOXTAIL_HEIGHT_MIN_FACTOR,
                FOXTAIL_HEIGHT_MAX_FACTOR,
            )
            foxtails.append(
                Foxtail(
                    base=base,
                    height=height,
                    natural_bend=_natural_bend(rng),
                    stiffness=rng.uniform(0.72, 1.08),
                    phase=rng.random() * tau,
                    head_length=rng.uniform(FOXTAIL_HEAD_LENGTH_MIN, FOXTAIL_HEAD_LENGTH_MAX),
                    head_segments=rng.randrange(
                        FOXTAIL_HEAD_SEGMENTS_MIN,
                        FOXTAIL_HEAD_SEGMENTS_MAX + 1,
                    ),
                )
            )
        return cls(foxtails=tuple(foxtails), seed=seed)


def sample_foxtail_shape(
    foxtail: Foxtail,
    wind: Vec3,
    rain_weight: float = 0.0,
    after_rain_weight: float = 0.0,
) -> FoxtailShape:
    if not isfinite(rain_weight) or not isfinite(after_rain_weight):
        raise ValueError("rain weights must be finite")

    rain = clamp(rain_weight, 0.0, 1.0)
    after_rain = clamp(after_rain_weight, 0.0, 1.0)
    stem_bend = foxtail.natural_bend + _wind_bend(foxtail, wind, 1.0)
    head_bend = foxtail.natural_bend + _wind_bend(foxtail, wind, FOXTAIL_HEAD_LAG_FACTOR)
    droop = Vec3(0.0, -foxtail.height * FOXTAIL_RAIN_DROOP_SCALE * rain, 0.0)

    stem_points = tuple(
        foxtail.base + Vec3(0.0, foxtail.height * t, 0.0) + stem_bend * (t * t) + droop * (t**2.4)
        for t in (index / FOXTAIL_STEM_SEGMENTS for index in range(FOXTAIL_STEM_SEGMENTS + 1))
    )
    tip = stem_points[-1]
    head_axis = Vec3(0.0, 1.0, 0.0) + head_bend.normalized() * 0.38 + droop.normalized() * 0.22
    if head_axis.length() == 0.0:
        head_axis = Vec3(0.0, 1.0, 0.0)
    head_direction = head_axis.normalized()
    head_points = tuple(
        tip + head_direction * (foxtail.head_length * index / foxtail.head_segments)
        for index in range(foxtail.head_segments + 1)
    )
    droplet_points = _droplet_points(head_points, after_rain)
    if not all(_is_finite_vec3(point) for point in stem_points + head_points + droplet_points):
        raise ValueError("foxtail points must be finite")
    return FoxtailShape(
        stem_points=stem_points, head_points=head_points, droplet_points=droplet_points
    )


def _sample_foxtail_base(
    world: CylinderWorld,
    rng: Random,
    index: int,
    count: int,
) -> Vec3:
    angle = (index + 0.34 + rng.random() * 0.18) / max(1, count)
    radius = rng.uniform(0.34, 0.78)
    return world.sample_bottom_point(radius, angle)


def _natural_bend(rng: Random) -> Vec3:
    angle = rng.random() * tau
    amount = rng.uniform(FOXTAIL_NATURAL_BEND_MIN, FOXTAIL_NATURAL_BEND_MAX)
    return Vec3(cos(angle) * amount, 0.0, sin(angle) * amount)


def _wind_bend(foxtail: Foxtail, wind: Vec3, lag_factor: float) -> Vec3:
    horizontal = Vec3(wind.x, 0.0, wind.z)
    bend = horizontal * (FOXTAIL_WIND_RESPONSE_SCALE * lag_factor / max(0.35, foxtail.stiffness))
    max_bend = foxtail.height * 0.42
    if bend.length() <= max_bend:
        return bend
    return bend.normalized() * max_bend


def _droplet_points(head_points: tuple[Vec3, ...], after_rain_weight: float) -> tuple[Vec3, ...]:
    if after_rain_weight <= 0.0 or len(head_points) < 4:
        return ()
    last = len(head_points) - 1
    return tuple(
        head_points[index] + Vec3(0.0, -1.0 - after_rain_weight * 2.0, 0.0)
        for index in (last // 2, max(1, last - 1))
    )


def _is_finite_vec3(point: Vec3) -> bool:
    return isfinite(point.x) and isfinite(point.y) and isfinite(point.z)
