from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, tau
from random import Random

from light_cylinder.config import (
    RAIN_GRASS_IMPACT_DECAY_RATE,
    RAIN_GRASS_IMPACT_RADIUS,
    RAIN_GRASS_REACTION_BEND_SCALE,
    RAIN_GROUND_DRY_RATE,
    RAIN_GROUND_WETNESS_GAIN,
    RAIN_SPLASH_GRAVITY,
    RAIN_SPLASH_LIFETIME,
    RAIN_SPLASH_SPEED,
    RAIN_SPLASHES_PER_IMPACT,
    TIP_DROPLET_FALL_SPEED,
    TIP_DROPLET_HOLD_MAX,
    TIP_DROPLET_HOLD_MIN,
    TIP_DROPLET_MAX_COUNT,
    TIP_DROPLET_SEED,
)
from light_cylinder.grass import GrassBlade
from light_cylinder.math3d import Vec3, clamp
from light_cylinder.rain import RainImpact


@dataclass(slots=True)
class SplashParticle:
    position: Vec3
    velocity: Vec3
    age: float = 0.0
    lifetime: float = RAIN_SPLASH_LIFETIME
    brightness: float = 1.0

    def update(self, dt: float) -> bool:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")
        self.age += dt
        self.position = self.position + self.velocity * dt
        self.velocity = Vec3(
            self.velocity.x,
            self.velocity.y - RAIN_SPLASH_GRAVITY * dt,
            self.velocity.z,
        )
        return self.age < self.lifetime and self.position.y >= 0.0

    @property
    def normalized_age(self) -> float:
        return clamp(self.age / self.lifetime, 0.0, 1.0)


@dataclass(slots=True)
class GroundReactionField:
    wetness: float = 0.0
    splashes: tuple[SplashParticle, ...] = ()

    def update(
        self,
        dt: float,
        impacts: tuple[RainImpact, ...] = (),
        dry_rate_multiplier: float = 1.0,
    ) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")
        if not isfinite(dry_rate_multiplier) or dry_rate_multiplier < 0:
            raise ValueError("dry rate multiplier must be a finite non-negative value")

        next_splashes = [splash for splash in self.splashes if splash.update(dt)]
        for impact in impacts:
            next_splashes.extend(_create_splashes(impact))

        self.splashes = tuple(next_splashes)
        self.wetness = clamp(
            self.wetness
            + len(impacts) * RAIN_GROUND_WETNESS_GAIN
            - dt * RAIN_GROUND_DRY_RATE * dry_rate_multiplier,
            0.0,
            1.0,
        )


@dataclass(slots=True)
class GrassReaction:
    impact: float = 0.0
    direction: Vec3 = Vec3(0.0, -1.0, 0.0)


@dataclass(slots=True)
class GrassReactionField:
    reactions: list[GrassReaction]

    @classmethod
    def create(cls, blade_count: int) -> GrassReactionField:
        if blade_count < 0:
            raise ValueError("blade count must be non-negative")
        return cls(reactions=[GrassReaction() for _index in range(blade_count)])

    def update(self, dt: float) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")
        for reaction in self.reactions:
            reaction.impact = max(0.0, reaction.impact - dt * RAIN_GRASS_IMPACT_DECAY_RATE)

    def apply_impacts(
        self,
        blades: tuple[GrassBlade, ...],
        impacts: tuple[RainImpact, ...],
    ) -> None:
        if len(blades) != len(self.reactions):
            raise ValueError("blade and reaction counts must match")

        radius_sq = RAIN_GRASS_IMPACT_RADIUS * RAIN_GRASS_IMPACT_RADIUS
        for impact in impacts:
            nearest_index = self._nearest_blade_index(blades, impact.position, radius_sq)
            if nearest_index is None:
                continue
            blade = blades[nearest_index]
            distance = _horizontal_distance(blade.base, impact.position)
            falloff = 1.0 - clamp(distance / RAIN_GRASS_IMPACT_RADIUS, 0.0, 1.0)
            reaction = self.reactions[nearest_index]
            reaction.impact = max(reaction.impact, impact.strength * falloff)
            reaction.direction = impact.direction

    def bend_for(self, blade_index: int) -> Vec3:
        reaction = self.reactions[blade_index]
        return reaction.direction * (reaction.impact * RAIN_GRASS_REACTION_BEND_SCALE)

    @property
    def active_count(self) -> int:
        return sum(1 for reaction in self.reactions if reaction.impact > 0.0)

    def _nearest_blade_index(
        self,
        blades: tuple[GrassBlade, ...],
        position: Vec3,
        radius_sq: float,
    ) -> int | None:
        nearest_index: int | None = None
        nearest_distance_sq = radius_sq
        for index, blade in enumerate(blades):
            dx = blade.base.x - position.x
            dz = blade.base.z - position.z
            distance_sq = dx * dx + dz * dz
            if distance_sq <= nearest_distance_sq:
                nearest_distance_sq = distance_sq
                nearest_index = index
        return nearest_index


def _create_splashes(impact: RainImpact) -> tuple[SplashParticle, ...]:
    splashes: list[SplashParticle] = []
    for index in range(RAIN_SPLASHES_PER_IMPACT):
        angle = impact.phase + tau * index / max(1, RAIN_SPLASHES_PER_IMPACT)
        speed = RAIN_SPLASH_SPEED * impact.strength
        splashes.append(
            SplashParticle(
                position=impact.position,
                velocity=Vec3(cos(angle) * speed, speed * 0.34, sin(angle) * speed),
                brightness=impact.strength,
            )
        )
    return tuple(splashes)


def _horizontal_distance(start: Vec3, end: Vec3) -> float:
    dx = start.x - end.x
    dz = start.z - end.z
    return (dx * dx + dz * dz) ** 0.5


@dataclass(slots=True)
class TipDroplet:
    blade_index: int
    hold_time: float
    fall_distance: float = 0.0
    age: float = 0.0
    active: bool = True
    falling: bool = False

    def update(self, dt: float) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")
        if not self.active:
            return
        self.age += dt
        if self.age >= self.hold_time:
            self.falling = True
            self.fall_distance += TIP_DROPLET_FALL_SPEED * dt

    def position_from_tip(self, tip: Vec3, blade_height: float) -> Vec3:
        return Vec3(tip.x, max(0.0, tip.y - self.fall_distance), tip.z)

    def should_remove(self, blade_height: float) -> bool:
        return self.fall_distance > blade_height * 0.72


@dataclass(slots=True)
class TipDropletField:
    candidate_indices: tuple[int, ...]
    droplets: list[TipDroplet]

    @classmethod
    def create(cls, blades: tuple[GrassBlade, ...]) -> TipDropletField:
        rng = Random(TIP_DROPLET_SEED)
        ranked = sorted(
            range(len(blades)),
            key=lambda index: (
                abs(blades[index].base.x) * 0.8 + abs(blades[index].base.z),
                rng.random(),
            ),
        )
        return cls(candidate_indices=tuple(ranked[:TIP_DROPLET_MAX_COUNT]), droplets=[])

    def seed_after_rain(self, wetness: float) -> None:
        if self.droplets or wetness <= 0.0:
            return
        count = min(
            len(self.candidate_indices),
            max(1, round(len(self.candidate_indices) * clamp(wetness, 0.0, 1.0))),
        )
        rng = Random(TIP_DROPLET_SEED + count)
        for blade_index in self.candidate_indices[:count]:
            hold = rng.uniform(TIP_DROPLET_HOLD_MIN, TIP_DROPLET_HOLD_MAX)
            self.droplets.append(TipDroplet(blade_index=blade_index, hold_time=hold))

    def update(self, dt: float, blades: tuple[GrassBlade, ...]) -> None:
        for droplet in self.droplets:
            droplet.update(dt)
            if droplet.should_remove(blades[droplet.blade_index].height):
                droplet.active = False
        self.droplets = [droplet for droplet in self.droplets if droplet.active]

    @property
    def active_count(self) -> int:
        return len(self.droplets)
