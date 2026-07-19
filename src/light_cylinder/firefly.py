from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, sqrt, tau
from random import Random

from light_cylinder.config import (
    FIREFLY_AFTER_RAIN_SPAWN_MULTIPLIER,
    FIREFLY_BOUNDARY_ACCELERATION,
    FIREFLY_BOUNDARY_MARGIN,
    FIREFLY_CLEAR_SPAWN_MULTIPLIER,
    FIREFLY_GLOW_SPEED_MAX,
    FIREFLY_GLOW_SPEED_MIN,
    FIREFLY_LIFETIME_MAX,
    FIREFLY_LIFETIME_MIN,
    FIREFLY_MAX_COUNT,
    FIREFLY_MAX_SPEED,
    FIREFLY_RAIN_SPAWN_MULTIPLIER,
    FIREFLY_SEED,
    FIREFLY_SPAWN_DELAY_MAX,
    FIREFLY_SPAWN_DELAY_MIN,
    FIREFLY_STRONG_RAIN_THRESHOLD,
    FIREFLY_TARGET_ACCELERATION,
    FIREFLY_TARGET_MAX_HEIGHT_FACTOR,
    FIREFLY_TARGET_MIN_DISTANCE,
    FIREFLY_TARGET_MIN_HEIGHT_FACTOR,
    FIREFLY_TARGET_REACH_RADIUS,
    FIREFLY_VELOCITY_DAMPING,
    FIREFLY_WANDER_ACCELERATION,
    FIREFLY_WIND_INFLUENCE,
)
from light_cylinder.math3d import Vec3, clamp
from light_cylinder.world import CylinderWorld


@dataclass(frozen=True, slots=True)
class Firefly:
    position: Vec3
    velocity: Vec3
    target: Vec3
    age: float
    lifetime: float
    glow_phase: float
    glow_speed: float

    def glow(self) -> float:
        return clamp((sin(self.age * self.glow_speed + self.glow_phase) + 1.0) * 0.5, 0.0, 1.0)


@dataclass(slots=True)
class FireflyField:
    world: CylinderWorld
    fireflies: tuple[Firefly, ...]
    spawn_timer: float
    rng: Random

    @classmethod
    def create_default(cls, world: CylinderWorld) -> FireflyField:
        rng = Random(FIREFLY_SEED)
        return cls(
            world=world,
            fireflies=(),
            spawn_timer=_next_spawn_delay(rng, FIREFLY_CLEAR_SPAWN_MULTIPLIER),
            rng=rng,
        )

    def update(
        self,
        dt: float,
        wind: Vec3,
        environment_state: str,
        rain_intensity: float,
        max_count: int = FIREFLY_MAX_COUNT,
    ) -> None:
        if not isfinite(dt) or dt < 0:
            raise ValueError("dt must be a finite non-negative value")

        active_limit = max(0, min(FIREFLY_MAX_COUNT, max_count))
        self.fireflies = tuple(
            advanced
            for firefly in self.fireflies
            if (advanced := self._advance_firefly(firefly, dt, wind)) is not None
        )[:active_limit]
        self.spawn_timer -= dt
        if self.spawn_timer > 0.0:
            return

        multiplier = spawn_delay_multiplier(environment_state, rain_intensity)
        if multiplier > 0.0 and len(self.fireflies) < active_limit:
            self.fireflies += (self._spawn_firefly(),)
        self.spawn_timer = _next_spawn_delay(self.rng, multiplier)

    def active_fireflies(self) -> tuple[Firefly, ...]:
        return self.fireflies

    def clear(self) -> None:
        self.fireflies = ()
        self.spawn_timer = _next_spawn_delay(self.rng, FIREFLY_CLEAR_SPAWN_MULTIPLIER)

    def _advance_firefly(self, firefly: Firefly, dt: float, wind: Vec3) -> Firefly | None:
        age = firefly.age + dt
        if age >= firefly.lifetime:
            return None

        target = firefly.target
        if (target - firefly.position).length() <= FIREFLY_TARGET_REACH_RADIUS:
            target = _sample_target_away(self.world, self.rng, firefly.position)

        acceleration = (target - firefly.position).normalized() * FIREFLY_TARGET_ACCELERATION
        acceleration += _wander(age, firefly.glow_phase) * FIREFLY_WANDER_ACCELERATION
        acceleration += _boundary_avoidance(self.world, firefly.position)
        acceleration += wind * FIREFLY_WIND_INFLUENCE
        velocity = _clamp_speed(
            firefly.velocity * FIREFLY_VELOCITY_DAMPING + acceleration * dt,
            FIREFLY_MAX_SPEED,
        )
        position = _clamp_inside(self.world, firefly.position + velocity * dt)

        return Firefly(
            position=position,
            velocity=velocity,
            target=target,
            age=age,
            lifetime=firefly.lifetime,
            glow_phase=firefly.glow_phase,
            glow_speed=firefly.glow_speed,
        )

    def _spawn_firefly(self) -> Firefly:
        position = _sample_target(self.world, self.rng)
        target = _sample_target_away(self.world, self.rng, position)
        direction = (target - position).normalized()
        return Firefly(
            position=position,
            velocity=direction * self.rng.uniform(2.0, 6.0),
            target=target,
            age=0.0,
            lifetime=self.rng.uniform(FIREFLY_LIFETIME_MIN, FIREFLY_LIFETIME_MAX),
            glow_phase=self.rng.random() * tau,
            glow_speed=self.rng.uniform(FIREFLY_GLOW_SPEED_MIN, FIREFLY_GLOW_SPEED_MAX),
        )


def spawn_delay_multiplier(environment_state: str, rain_intensity: float) -> float:
    if environment_state == "RAIN":
        if rain_intensity >= FIREFLY_STRONG_RAIN_THRESHOLD:
            return 0.0
        return FIREFLY_RAIN_SPAWN_MULTIPLIER
    if environment_state == "AFTER_RAIN":
        return FIREFLY_AFTER_RAIN_SPAWN_MULTIPLIER
    return FIREFLY_CLEAR_SPAWN_MULTIPLIER


def _next_spawn_delay(rng: Random, multiplier: float) -> float:
    delay = rng.uniform(FIREFLY_SPAWN_DELAY_MIN, FIREFLY_SPAWN_DELAY_MAX)
    if multiplier <= 0.0:
        return delay
    return delay / multiplier


def _sample_target(world: CylinderWorld, rng: Random) -> Vec3:
    base = world.sample_bottom_point(rng.random() ** 0.58, rng.random())
    height_factor = rng.uniform(FIREFLY_TARGET_MIN_HEIGHT_FACTOR, FIREFLY_TARGET_MAX_HEIGHT_FACTOR)
    return Vec3(base.x, world.bottom_y + world.height * height_factor, base.z)


def _sample_target_away(world: CylinderWorld, rng: Random, origin: Vec3) -> Vec3:
    target = _sample_target(world, rng)
    for _attempt in range(12):
        if (target - origin).length() >= FIREFLY_TARGET_MIN_DISTANCE:
            return target
        target = _sample_target(world, rng)
    return target


def _wander(age: float, phase: float) -> Vec3:
    return Vec3(
        sin(age * 0.73 + phase),
        sin(age * 0.49 + phase * 1.31) * 0.35,
        cos(age * 0.67 + phase * 0.83),
    ).normalized()


def _boundary_avoidance(world: CylinderWorld, position: Vec3) -> Vec3:
    radial_x = position.x - world.center_x
    radial_z = position.z - world.center_z
    distance = sqrt(radial_x * radial_x + radial_z * radial_z)
    acceleration = Vec3(0.0, 0.0, 0.0)
    if distance > world.radius - FIREFLY_BOUNDARY_MARGIN and distance > 0.0:
        pressure = (distance - (world.radius - FIREFLY_BOUNDARY_MARGIN)) / FIREFLY_BOUNDARY_MARGIN
        acceleration += Vec3(-radial_x / distance, 0.0, -radial_z / distance) * (
            FIREFLY_BOUNDARY_ACCELERATION * clamp(pressure, 0.0, 1.0)
        )

    min_y = world.bottom_y + world.height * FIREFLY_TARGET_MIN_HEIGHT_FACTOR
    max_y = world.bottom_y + world.height * FIREFLY_TARGET_MAX_HEIGHT_FACTOR
    if position.y < min_y + FIREFLY_BOUNDARY_MARGIN:
        acceleration += Vec3(0.0, FIREFLY_BOUNDARY_ACCELERATION * 0.45, 0.0)
    if position.y > max_y - FIREFLY_BOUNDARY_MARGIN:
        acceleration += Vec3(0.0, -FIREFLY_BOUNDARY_ACCELERATION * 0.45, 0.0)
    return acceleration


def _clamp_speed(velocity: Vec3, max_speed: float) -> Vec3:
    speed = velocity.length()
    if speed <= max_speed or speed == 0.0:
        return velocity
    return velocity * (max_speed / speed)


def _clamp_inside(world: CylinderWorld, position: Vec3) -> Vec3:
    min_y = world.bottom_y + world.height * FIREFLY_TARGET_MIN_HEIGHT_FACTOR
    max_y = world.bottom_y + world.height * FIREFLY_TARGET_MAX_HEIGHT_FACTOR
    y = clamp(position.y, min_y, max_y)
    radial_x = position.x - world.center_x
    radial_z = position.z - world.center_z
    distance = sqrt(radial_x * radial_x + radial_z * radial_z)
    max_radius = world.radius - 1.0
    if distance <= max_radius or distance == 0.0:
        return Vec3(position.x, y, position.z)
    scale = max_radius / distance
    return Vec3(world.center_x + radial_x * scale, y, world.center_z + radial_z * scale)
