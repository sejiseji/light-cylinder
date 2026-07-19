from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, tau
from random import Random

from light_cylinder.config import (
    LIGHT_BEAM_CORE_RADIUS,
    LIGHT_BEAM_DIRECTION,
    LIGHT_BEAM_END_FADE,
    LIGHT_BEAM_LENGTH,
    LIGHT_BEAM_ORIGIN,
    LIGHT_BEAM_RADIUS,
    LIGHT_CLOUD_SHADOW_AMOUNT,
    LIGHT_CLOUD_SHADOW_FLOOR,
    LIGHT_CLOUD_SHADOW_RATE,
    LIGHT_GROUND_SPARK_COUNT,
    LIGHT_PARTICLE_AXIS_ATTRACTION,
    LIGHT_PARTICLE_COUNT,
    LIGHT_PARTICLE_DRIFT_MAX,
    LIGHT_PARTICLE_DRIFT_MIN,
    LIGHT_PARTICLE_SWAY_AMOUNT,
    LIGHT_PARTICLE_SWAY_RATE,
    LIGHT_PARTICLE_WALK_AMOUNT,
    LIGHT_PARTICLE_WALK_RATE,
    LIGHT_SEED,
)
from light_cylinder.math3d import Vec3, clamp
from light_cylinder.world import CylinderWorld


@dataclass(frozen=True, slots=True)
class LightBeam:
    origin: Vec3
    direction: Vec3
    length: float
    radius: float
    core_radius: float
    end_fade: float

    @classmethod
    def create_default(cls) -> LightBeam:
        return cls(
            origin=Vec3(*LIGHT_BEAM_ORIGIN),
            direction=Vec3(*LIGHT_BEAM_DIRECTION).normalized(),
            length=LIGHT_BEAM_LENGTH,
            radius=LIGHT_BEAM_RADIUS,
            core_radius=LIGHT_BEAM_CORE_RADIUS,
            end_fade=LIGHT_BEAM_END_FADE,
        )

    def __post_init__(self) -> None:
        if not _is_finite_vec3(self.origin):
            raise ValueError("light beam origin must be finite")
        if self.direction.length() == 0 or not _is_finite_vec3(self.direction):
            raise ValueError("light beam direction must be finite and non-zero")
        if self.length <= 0 or self.radius <= 0:
            raise ValueError("light beam length and radius must be positive")
        if not 0 <= self.core_radius < self.radius:
            raise ValueError("light beam core radius must be smaller than radius")
        if self.end_fade <= 0:
            raise ValueError("light beam end fade must be positive")
        object.__setattr__(self, "direction", self.direction.normalized())

    def intensity_at(self, point: Vec3) -> float:
        axial_position = self.axial_position(point)
        if axial_position < 0 or axial_position > self.length:
            return 0.0

        radial_distance = self.radial_distance(point)
        if radial_distance > self.radius:
            return 0.0

        radial = 1.0
        if radial_distance > self.core_radius:
            radial = 1.0 - (radial_distance - self.core_radius) / (self.radius - self.core_radius)

        end = min(axial_position, self.length - axial_position) / self.end_fade
        return clamp(radial, 0.0, 1.0) * clamp(end, 0.0, 1.0)

    def axial_position(self, point: Vec3) -> float:
        return (point - self.origin).dot(self.direction)

    def radial_distance(self, point: Vec3) -> float:
        axis_point = self.axis_point(self.axial_position(point))
        return (point - axis_point).length()

    def axis_point(self, axial_position: float) -> Vec3:
        return self.origin + self.direction * axial_position

    def axis_point_at(self, normalized_position: float) -> Vec3:
        return self.axis_point(clamp(normalized_position, 0.0, 1.0) * self.length)

    def basis(self) -> tuple[Vec3, Vec3]:
        horizontal = Vec3(-self.direction.z, 0.0, self.direction.x).normalized()
        if horizontal.length() == 0:
            horizontal = Vec3(1.0, 0.0, 0.0)
        vertical = self.direction.cross(horizontal).normalized()
        return horizontal, vertical


@dataclass(frozen=True, slots=True)
class LightParticle:
    axial_position: float
    radial_distance: float
    angle: float
    phase: float
    drift_speed: float
    brightness: float

    def position_at(self, beam: LightBeam, elapsed_time: float) -> Vec3:
        axial_position = (self.axial_position + self.drift_speed * elapsed_time) % beam.length
        angle = self.angle + sin(elapsed_time * LIGHT_PARTICLE_SWAY_RATE + self.phase) * (
            LIGHT_PARTICLE_SWAY_AMOUNT
        )
        walk = sin(elapsed_time * LIGHT_PARTICLE_WALK_RATE + self.phase * 1.37) * (
            LIGHT_PARTICLE_WALK_AMOUNT
        )
        radial_distance = max(
            0.0,
            self.radial_distance * (1.0 - LIGHT_PARTICLE_AXIS_ATTRACTION) + walk,
        )
        basis_u, basis_v = beam.basis()
        offset = basis_u * (cos(angle) * radial_distance)
        offset += basis_v * (sin(angle) * radial_distance)
        return beam.axis_point(axial_position) + offset


@dataclass(frozen=True, slots=True)
class LightGroundSpark:
    position: Vec3
    brightness: float


@dataclass(slots=True)
class LightField:
    beam: LightBeam
    particles: tuple[LightParticle, ...]
    ground_sparks: tuple[LightGroundSpark, ...]
    elapsed_time: float = 0.0

    @classmethod
    def create_default(
        cls,
        world: CylinderWorld,
        particle_count: int = LIGHT_PARTICLE_COUNT,
    ) -> LightField:
        beam = LightBeam.create_default()
        rng = Random(LIGHT_SEED)
        return cls(
            beam=beam,
            particles=_generate_particles(beam, rng, particle_count),
            ground_sparks=_generate_ground_sparks(world, beam, rng),
        )

    def update(self, dt: float) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")
        self.elapsed_time = (self.elapsed_time + dt) % 3600.0

    def particle_positions(self) -> tuple[tuple[LightParticle, Vec3], ...]:
        return tuple(
            (particle, particle.position_at(self.beam, self.elapsed_time))
            for particle in self.particles
        )

    @property
    def intensity_multiplier(self) -> float:
        cloud = (1.0 + sin(self.elapsed_time * LIGHT_CLOUD_SHADOW_RATE)) * 0.5
        multiplier = 1.0 - LIGHT_CLOUD_SHADOW_AMOUNT * cloud
        return max(LIGHT_CLOUD_SHADOW_FLOOR, multiplier)


def _generate_particles(
    beam: LightBeam,
    rng: Random,
    particle_count: int,
) -> tuple[LightParticle, ...]:
    if particle_count < 0:
        raise ValueError("particle count must be non-negative")
    particles: list[LightParticle] = []
    for _index in range(particle_count):
        normalized_radius = rng.random() ** 0.72
        particles.append(
            LightParticle(
                axial_position=rng.random() * beam.length,
                radial_distance=normalized_radius * beam.radius * 0.92,
                angle=rng.random() * tau,
                phase=rng.random() * tau,
                drift_speed=rng.uniform(LIGHT_PARTICLE_DRIFT_MIN, LIGHT_PARTICLE_DRIFT_MAX),
                brightness=rng.uniform(0.58, 1.0),
            )
        )
    return tuple(particles)


def _generate_ground_sparks(
    world: CylinderWorld,
    beam: LightBeam,
    rng: Random,
) -> tuple[LightGroundSpark, ...]:
    sparks: list[LightGroundSpark] = []
    floor_center = _beam_floor_center(world, beam)
    attempts = 0
    max_attempts = max(1, LIGHT_GROUND_SPARK_COUNT * 20)

    while len(sparks) < LIGHT_GROUND_SPARK_COUNT and attempts < max_attempts:
        attempts += 1
        radius = beam.radius * (rng.random() ** 0.58)
        angle = rng.random() * tau
        point = Vec3(
            floor_center.x + cos(angle) * radius,
            world.bottom_y,
            floor_center.z + sin(angle) * radius,
        )
        intensity = beam.intensity_at(point)
        if world.contains_horizontal(point) and intensity > 0.18:
            sparks.append(LightGroundSpark(position=point, brightness=rng.uniform(0.55, 1.0)))

    return tuple(sparks)


def _beam_floor_center(world: CylinderWorld, beam: LightBeam) -> Vec3:
    if beam.direction.y == 0:
        return world.bottom_center
    axial_position = (world.bottom_y - beam.origin.y) / beam.direction.y
    axis_point = beam.axis_point(clamp(axial_position, 0.0, beam.length))
    return Vec3(axis_point.x, world.bottom_y, axis_point.z)


def _is_finite_vec3(point: Vec3) -> bool:
    return isfinite(point.x) and isfinite(point.y) and isfinite(point.z)
