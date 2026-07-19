import pytest

from light_cylinder.config import (
    FIREFLY_MAX_COUNT,
    FIREFLY_MAX_SPEED,
    FIREFLY_SPAWN_DELAY_MIN,
    FIREFLY_STRONG_RAIN_THRESHOLD,
)
from light_cylinder.firefly import Firefly, FireflyField, spawn_delay_multiplier
from light_cylinder.math3d import Vec3
from light_cylinder.world import CylinderWorld


def test_firefly_field_starts_empty_with_delayed_spawn() -> None:
    field = FireflyField.create_default(CylinderWorld())

    assert field.active_fireflies() == ()
    assert field.spawn_timer >= FIREFLY_SPAWN_DELAY_MIN


def test_firefly_field_spawns_inside_cylinder_after_gap() -> None:
    world = CylinderWorld()
    field = FireflyField.create_default(world)
    field.spawn_timer = 0.0

    field.update(0.0, Vec3(0.0, 0.0, 0.0), "CLEAR", 0.0)

    active = field.active_fireflies()
    assert 1 <= len(active) <= FIREFLY_MAX_COUNT
    assert all(world.contains(firefly.position) for firefly in active)


def test_firefly_spawn_uses_longer_initial_target_distance() -> None:
    world = CylinderWorld()
    field = FireflyField.create_default(world)
    field.spawn_timer = 0.0

    field.update(0.0, Vec3(0.0, 0.0, 0.0), "CLEAR", 0.0)

    firefly = field.active_fireflies()[0]
    assert (firefly.target - firefly.position).length() >= 48.0


def test_firefly_field_respects_adjustable_active_limit() -> None:
    field = FireflyField.create_default(CylinderWorld())

    for _index in range(FIREFLY_MAX_COUNT):
        field.spawn_timer = 0.0
        field.update(0.0, Vec3(0.0, 0.0, 0.0), "CLEAR", 0.0, max_count=FIREFLY_MAX_COUNT)

    assert len(field.active_fireflies()) == FIREFLY_MAX_COUNT

    field.update(0.1, Vec3(0.0, 0.0, 0.0), "CLEAR", 0.0, max_count=3)

    assert len(field.active_fireflies()) == 3


def test_firefly_movement_is_smooth_and_stays_inside() -> None:
    world = CylinderWorld()
    field = FireflyField.create_default(world)
    field.spawn_timer = 0.0
    field.update(0.0, Vec3(0.0, 0.0, 0.0), "CLEAR", 0.0)
    before = field.active_fireflies()[0].position

    field.update(1.0, Vec3(3.0, 0.0, 0.0), "CLEAR", 0.0)

    after = field.active_fireflies()[0].position
    assert world.contains(after)
    assert 0.0 < (after - before).length() <= FIREFLY_MAX_SPEED


def test_firefly_spawn_is_blocked_by_strong_rain() -> None:
    field = FireflyField.create_default(CylinderWorld())
    field.spawn_timer = 0.0

    field.update(
        0.0,
        Vec3(0.0, 0.0, 0.0),
        "RAIN",
        FIREFLY_STRONG_RAIN_THRESHOLD,
    )

    assert field.active_fireflies() == ()
    assert field.spawn_timer >= FIREFLY_SPAWN_DELAY_MIN


def test_firefly_spawn_multipliers_preserve_rare_after_rain_return() -> None:
    assert spawn_delay_multiplier("CLEAR", 0.0) == pytest.approx(1.0)
    assert 0.0 < spawn_delay_multiplier("AFTER_RAIN", 0.0) < 1.0
    assert 0.0 < spawn_delay_multiplier("RAIN", 0.2) < spawn_delay_multiplier("AFTER_RAIN", 0.0)
    assert spawn_delay_multiplier("RAIN", FIREFLY_STRONG_RAIN_THRESHOLD) == 0.0


def test_firefly_glow_stays_normalized() -> None:
    firefly = Firefly(
        position=Vec3(0.0, 40.0, 0.0),
        velocity=Vec3(0.0, 0.0, 0.0),
        target=Vec3(1.0, 42.0, 1.0),
        age=3.0,
        lifetime=10.0,
        glow_phase=1.0,
        glow_speed=0.9,
    )

    assert 0.0 <= firefly.glow() <= 1.0


def test_firefly_field_clear_removes_active_visitors() -> None:
    field = FireflyField.create_default(CylinderWorld())
    field.spawn_timer = 0.0
    field.update(0.0, Vec3(0.0, 0.0, 0.0), "CLEAR", 0.0)

    field.clear()

    assert field.active_fireflies() == ()
