from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, tau
from random import Random

from light_cylinder.config import (
    GRASS_COUNT,
    GRASS_MAX_BEND,
    GRASS_MAX_HEIGHT,
    GRASS_MAX_STIFFNESS,
    GRASS_MIN_BEND,
    GRASS_MIN_HEIGHT,
    GRASS_MIN_STIFFNESS,
    GRASS_SEED,
)
from light_cylinder.math3d import Vec3
from light_cylinder.world import CylinderWorld


@dataclass(frozen=True, slots=True)
class GrassBlade:
    base: Vec3
    height: float
    natural_bend: Vec3
    stiffness: float
    phase: float
    width_class: int
    color_variant: int


@dataclass(frozen=True, slots=True)
class GrassField:
    blades: tuple[GrassBlade, ...]
    seed: int

    @classmethod
    def generate(
        cls,
        world: CylinderWorld,
        seed: int = GRASS_SEED,
        grass_count: int = GRASS_COUNT,
        max_attempts: int | None = None,
    ) -> GrassField:
        if grass_count < 0:
            raise ValueError("grass_count must be non-negative")

        rng = Random(seed)
        attempts_limit = max_attempts if max_attempts is not None else max(1, grass_count * 20)
        blades: list[GrassBlade] = []
        attempts = 0

        while len(blades) < grass_count and attempts < attempts_limit:
            attempts += 1
            base = world.sample_bottom_point(rng.random(), rng.random())
            if rng.random() > density_weight(world.normalized_radius(base)):
                continue

            blades.append(
                GrassBlade(
                    base=base,
                    height=rng.uniform(GRASS_MIN_HEIGHT, GRASS_MAX_HEIGHT),
                    natural_bend=_natural_bend(rng),
                    stiffness=rng.uniform(GRASS_MIN_STIFFNESS, GRASS_MAX_STIFFNESS),
                    phase=rng.random() * tau,
                    width_class=rng.randrange(3),
                    color_variant=rng.randrange(3),
                )
            )

        if len(blades) != grass_count:
            raise ValueError("could not generate the requested grass count within max_attempts")

        return cls(blades=tuple(blades), seed=seed)

    def __len__(self) -> int:
        return len(self.blades)


def density_weight(normalized_radius: float) -> float:
    return max(0.0, min(1.0, 1.0 - 0.35 * abs(normalized_radius - 0.65)))


def sample_blade_points(
    blade: GrassBlade,
    segment_count: int,
    additional_bend: Vec3 | None = None,
) -> tuple[Vec3, ...]:
    if segment_count < 1:
        raise ValueError("segment_count must be positive")

    bend = blade.natural_bend + (additional_bend or Vec3(0.0, 0.0, 0.0))
    points = tuple(
        blade.base + Vec3(0.0, blade.height * t, 0.0) + bend * (t * t)
        for t in (index / segment_count for index in range(segment_count + 1))
    )
    if not all(_is_finite_vec3(point) for point in points):
        raise ValueError("blade points must be finite")
    return points


def _natural_bend(rng: Random) -> Vec3:
    bend_angle = rng.random() * tau
    bend_amount = rng.uniform(GRASS_MIN_BEND, GRASS_MAX_BEND)
    return Vec3(cos(bend_angle) * bend_amount, 0.0, sin(bend_angle) * bend_amount)


def _is_finite_vec3(point: Vec3) -> bool:
    return isfinite(point.x) and isfinite(point.y) and isfinite(point.z)
