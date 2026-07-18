from math import sqrt

import pytest

from light_cylinder.config import CYLINDER_HEIGHT, CYLINDER_RADIUS
from light_cylinder.math3d import Vec3
from light_cylinder.world import CylinderWorld


def assert_vec3_close(actual: Vec3, expected: Vec3) -> None:
    assert actual.x == pytest.approx(expected.x)
    assert actual.y == pytest.approx(expected.y)
    assert actual.z == pytest.approx(expected.z)


def test_default_values_and_top_y() -> None:
    world = CylinderWorld()

    assert world.center_x == 0.0
    assert world.center_z == 0.0
    assert world.bottom_y == 0.0
    assert world.radius == CYLINDER_RADIUS
    assert world.height == CYLINDER_HEIGHT
    assert world.top_y == pytest.approx(CYLINDER_HEIGHT)


def test_contains_center_and_boundaries() -> None:
    world = CylinderWorld()

    assert world.contains(Vec3(0.0, CYLINDER_HEIGHT * 0.5, 0.0))
    assert world.contains(world.bottom_center)
    assert world.contains(world.top_center)
    assert world.contains(Vec3(CYLINDER_RADIUS, 10.0, 0.0))


def test_contains_rejects_outside_radius_and_height() -> None:
    world = CylinderWorld()

    assert not world.contains(Vec3(CYLINDER_RADIUS + 0.1, 10.0, 0.0))
    assert not world.contains(Vec3(0.0, -0.1, 0.0))
    assert not world.contains(Vec3(0.0, CYLINDER_HEIGHT + 0.1, 0.0))


def test_center_offset() -> None:
    world = CylinderWorld(center_x=10.0, center_z=-20.0, bottom_y=5.0, radius=3.0, height=9.0)

    assert world.top_y == pytest.approx(14.0)
    assert world.contains(Vec3(13.0, 5.0, -20.0))
    assert not world.contains(Vec3(13.1, 5.0, -20.0))


def test_radial_distance_and_normalized_radius() -> None:
    world = CylinderWorld(radius=10.0)
    point = Vec3(6.0, 0.0, 8.0)

    assert world.radial_distance_squared(point) == pytest.approx(100.0)
    assert world.radial_distance(point) == pytest.approx(10.0)
    assert world.normalized_radius(point) == pytest.approx(1.0)


def test_ring_point_counts_and_theta_zero() -> None:
    world = CylinderWorld(radius=10.0)

    bottom = world.bottom_ring_points(8)
    top = world.top_ring_points(8)

    assert len(bottom) == 8
    assert len(top) == 8
    assert_vec3_close(bottom[0], Vec3(10.0, 0.0, 0.0))
    assert_vec3_close(top[0], Vec3(10.0, CYLINDER_HEIGHT, 0.0))


def test_ring_points_stay_on_radius_and_y_planes() -> None:
    world = CylinderWorld(radius=10.0, bottom_y=2.0, height=8.0)

    bottom = world.bottom_ring_points(16)
    top = world.top_ring_points(16)

    assert all(point.y == pytest.approx(2.0) for point in bottom)
    assert all(point.y == pytest.approx(10.0) for point in top)
    assert all(world.radial_distance(point) == pytest.approx(10.0) for point in bottom)
    assert all(world.radial_distance(point) == pytest.approx(10.0) for point in top)


def test_segment_count_rejects_too_small_values() -> None:
    world = CylinderWorld()

    with pytest.raises(ValueError):
        world.bottom_ring_points(2)
    with pytest.raises(ValueError):
        world.top_ring_points(2)
    with pytest.raises(ValueError):
        world.ring_points_at(2, 0.0)


def test_vertical_guide_segments() -> None:
    world = CylinderWorld()

    guides = world.vertical_guide_segments(8)

    assert len(guides) == 8
    assert all(start.y == pytest.approx(world.bottom_y) for start, _end in guides)
    assert all(end.y == pytest.approx(world.top_y) for _start, end in guides)


def test_vertical_guide_count_rejects_zero() -> None:
    with pytest.raises(ValueError):
        CylinderWorld().vertical_guide_segments(0)


def test_sample_bottom_point_center_and_outer_edge() -> None:
    world = CylinderWorld(radius=10.0)

    center = world.sample_bottom_point(0.0, 0.75)
    outer = world.sample_bottom_point(1.0, 0.25)

    assert_vec3_close(center, Vec3(0.0, 0.0, 0.0))
    assert_vec3_close(outer, Vec3(0.0, 0.0, 10.0))
    assert world.contains(outer)


def test_sample_bottom_point_uses_area_uniform_radius() -> None:
    world = CylinderWorld(radius=10.0)

    point = world.sample_bottom_point(0.25, 0.0)

    assert_vec3_close(point, Vec3(5.0, 0.0, 0.0))
    assert world.radial_distance(point) == pytest.approx(10.0 * sqrt(0.25))


def test_sample_bottom_point_is_deterministic_and_clamps_inputs() -> None:
    world = CylinderWorld(radius=10.0)

    first = world.sample_bottom_point(1.25, -0.5)
    second = world.sample_bottom_point(1.25, -0.5)

    assert first == second
    assert_vec3_close(first, Vec3(10.0, 0.0, 0.0))
    assert world.contains(first)
