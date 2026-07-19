from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, tau

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

    def update(self, dt: float, impacts: tuple[RainImpact, ...] = ()) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")

        next_splashes = [splash for splash in self.splashes if splash.update(dt)]
        for impact in impacts:
            next_splashes.extend(_create_splashes(impact))

        self.splashes = tuple(next_splashes)
        self.wetness = clamp(
            self.wetness + len(impacts) * RAIN_GROUND_WETNESS_GAIN - dt * RAIN_GROUND_DRY_RATE,
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
