import pytest

from light_cylinder.config import (
    RAIN_DROP_COUNT,
    RAIN_SHORT_LENGTHS,
    RAIN_STATIC_STREAK_COUNT,
    RAIN_STATIC_STREAK_FLASH_RATE,
)
from light_cylinder.math3d import Vec3
from light_cylinder.rain import RainDrop, RainField, StaticRainStreak
from light_cylinder.world import CylinderWorld


def test_rain_field_generates_deterministic_drop_budget() -> None:
    world = CylinderWorld()
    field = RainField.create_default(world)
    streak_heights = [streak.head_position.y for streak in field.static_streaks]

    assert len(field.drops) == RAIN_DROP_COUNT
    assert len(field.static_streaks) == RAIN_STATIC_STREAK_COUNT
    assert field.active_drop_count == round(RAIN_DROP_COUNT * field.intensity)
    assert {drop.length for drop in field.drops} == set(RAIN_SHORT_LENGTHS)
    assert max(streak_heights) - min(streak_heights) > world.height * 0.55


def test_rain_intensity_clamps_and_controls_active_drops() -> None:
    field = RainField.create_default(CylinderWorld())

    field.set_intensity(-1.0)
    assert field.intensity == 0.0
    assert field.active_drops() == ()

    field.set_intensity(2.0)
    assert field.intensity == 1.0
    assert len(field.active_drops()) == RAIN_DROP_COUNT


def test_rain_update_rejects_negative_time() -> None:
    field = RainField.create_default(CylinderWorld())

    with pytest.raises(ValueError):
        field.update(-0.1)


def test_rain_segments_fall_within_cylinder_height() -> None:
    world = CylinderWorld()
    field = RainField.create_default(world)

    segments = field.segments(world, Vec3(0.0, 0.0, 0.0))

    assert segments
    for _drop, start, end in segments:
        assert world.bottom_y <= end.y <= start.y <= world.top_y


def test_rain_segments_ignore_wind_and_fall_vertically() -> None:
    world = CylinderWorld()
    field = RainField.create_default(world)

    calm_segments = field.segments(world, Vec3(0.0, 0.0, 0.0))
    windy_segments = field.segments(world, Vec3(1.0, 0.0, 0.25))

    assert calm_segments
    assert windy_segments
    calm_start = calm_segments[0][1]
    windy_start = windy_segments[0][1]
    windy_end = windy_segments[0][2]
    assert windy_start.x == pytest.approx(calm_start.x)
    assert windy_end.x == pytest.approx(windy_start.x)
    assert windy_end.z == pytest.approx(windy_start.z)


def test_static_rain_streaks_flash_without_changing_length() -> None:
    world = CylinderWorld()
    streak = StaticRainStreak(
        head_position=Vec3(0.0, world.bottom_y + 100.0, 0.0),
        length=64.0,
        phase=0.0,
        brightness=0.8,
    )

    assert streak.segment_at(world, 0.0) is None

    segment = streak.segment_at(world, 1.5707963267948966 / RAIN_STATIC_STREAK_FLASH_RATE)

    assert segment is not None
    start, end = segment
    assert start.x == end.x
    assert start.z == end.z
    assert start.y - end.y == 64.0


def test_rain_field_reports_static_streak_segments_separately() -> None:
    world = CylinderWorld()
    drop = RainDrop(
        base_position=world.top_center,
        phase=0.0,
        fall_speed=120.0,
        length=10.0,
        wind_sensitivity=1.0,
        brightness=0.8,
    )
    streak = StaticRainStreak(
        head_position=Vec3(0.0, world.bottom_y + 80.0, 0.0),
        length=48.0,
        phase=0.0,
        brightness=1.0,
    )
    field = RainField(drops=(drop,), static_streaks=(streak,), intensity=1.0)
    field.elapsed_time = 1.5707963267948966 / RAIN_STATIC_STREAK_FLASH_RATE

    segments = field.static_segments(world)

    assert len(segments) == 1
    assert segments[0][0] is streak


def test_rain_drop_reports_ground_impact_when_cycle_wraps() -> None:
    world = CylinderWorld()
    drop = RainDrop(
        base_position=world.top_center,
        phase=0.99,
        fall_speed=120.0,
        length=10.0,
        wind_sensitivity=1.0,
        brightness=0.8,
    )

    impact = drop.ground_impact_between(
        world,
        previous_time=0.0,
        current_time=1.0 / 30.0,
        wind=Vec3(0.0, 0.0, 0.0),
    )

    assert impact is not None
    assert impact.position.y == world.bottom_y
    assert impact.strength == 0.8


def test_rain_field_reports_active_ground_impacts_since_previous_time() -> None:
    world = CylinderWorld()
    drop = RainDrop(
        base_position=world.top_center,
        phase=0.99,
        fall_speed=120.0,
        length=10.0,
        wind_sensitivity=1.0,
        brightness=1.0,
    )
    field = RainField(drops=(drop,), intensity=1.0)

    previous = field.elapsed_time
    field.update(1.0 / 30.0)

    impacts = field.ground_impacts_since(world, previous, Vec3(0.0, 0.0, 0.0))

    assert len(impacts) == 1
