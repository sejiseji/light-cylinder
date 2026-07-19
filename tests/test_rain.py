import pytest

from light_cylinder.config import RAIN_DROP_COUNT
from light_cylinder.math3d import Vec3
from light_cylinder.rain import RainField
from light_cylinder.world import CylinderWorld


def test_rain_field_generates_deterministic_drop_budget() -> None:
    world = CylinderWorld()
    field = RainField.create_default(world)

    assert len(field.drops) == RAIN_DROP_COUNT
    assert field.active_drop_count == round(RAIN_DROP_COUNT * field.intensity)


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


def test_rain_segments_drift_with_wind() -> None:
    world = CylinderWorld()
    field = RainField.create_default(world)

    calm_segments = field.segments(world, Vec3(0.0, 0.0, 0.0))
    windy_segments = field.segments(world, Vec3(1.0, 0.0, 0.25))

    assert calm_segments
    assert windy_segments
    calm_start = calm_segments[0][1]
    windy_start = windy_segments[0][1]
    windy_end = windy_segments[0][2]
    assert windy_start.x != pytest.approx(calm_start.x)
    assert windy_end.x < windy_start.x
