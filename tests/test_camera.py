from math import isfinite

import pytest

from light_cylinder.camera import Camera
from light_cylinder.config import (
    CAMERA_MAX_DISTANCE,
    CAMERA_MAX_PITCH,
    CAMERA_MIN_DISTANCE,
    CAMERA_MIN_PITCH,
    RENDER_HEIGHT,
    RENDER_WIDTH,
)
from light_cylinder.math3d import Vec3


def make_camera() -> Camera:
    return Camera(
        target=Vec3(0.0, 0.0, 0.0),
        yaw=0.0,
        pitch=0.0,
        distance=400.0,
        focal_length=200.0,
        near_clip=5.0,
        screen_center_x=RENDER_WIDTH / 2,
        screen_center_y=RENDER_HEIGHT / 2,
    )


def test_origin_projects_to_screen_center() -> None:
    camera = make_camera()

    projected = camera.project(Vec3(0.0, 0.0, 0.0))

    assert projected is not None
    assert projected.x == pytest.approx(RENDER_WIDTH / 2)
    assert projected.y == pytest.approx(RENDER_HEIGHT / 2)
    assert projected.depth == pytest.approx(400.0)


def test_right_point_projects_right() -> None:
    camera = make_camera()

    center = camera.project(Vec3(0.0, 0.0, 0.0))
    projected = camera.project(Vec3(50.0, 0.0, 0.0))

    assert center is not None
    assert projected is not None
    assert projected.x > center.x


def test_up_point_projects_up() -> None:
    camera = make_camera()

    center = camera.project(Vec3(0.0, 0.0, 0.0))
    projected = camera.project(Vec3(0.0, 50.0, 0.0))

    assert center is not None
    assert projected is not None
    assert projected.y < center.y


def test_near_clip_or_behind_returns_none() -> None:
    camera = make_camera()

    assert camera.project(Vec3(0.0, 0.0, -396.0)) is None
    assert camera.project(Vec3(0.0, 0.0, -410.0)) is None


def test_yaw_changes_projection() -> None:
    camera = make_camera()
    before = camera.project(Vec3(80.0, 0.0, 0.0))

    camera.orbit(0.4, 0.0)
    after = camera.project(Vec3(80.0, 0.0, 0.0))

    assert before is not None
    assert after is not None
    assert after.x != pytest.approx(before.x)


def test_pitch_changes_projection() -> None:
    camera = make_camera()
    before = camera.project(Vec3(0.0, 80.0, 0.0))

    camera.orbit(0.0, 0.4)
    after = camera.project(Vec3(0.0, 80.0, 0.0))

    assert before is not None
    assert after is not None
    assert after.y != pytest.approx(before.y)


def test_pitch_clamp() -> None:
    camera = make_camera()

    camera.orbit(0.0, 100.0)
    assert camera.pitch == pytest.approx(CAMERA_MAX_PITCH)
    camera.orbit(0.0, -200.0)
    assert camera.pitch == pytest.approx(CAMERA_MIN_PITCH)


def test_distance_clamp_and_zoom() -> None:
    camera = make_camera()

    camera.zoom(-1000.0)
    assert camera.distance == pytest.approx(CAMERA_MIN_DISTANCE)
    camera.zoom(2000.0)
    assert camera.distance == pytest.approx(CAMERA_MAX_DISTANCE)


def test_projection_returns_finite_values() -> None:
    camera = make_camera()

    projected = camera.project(Vec3(50.0, 70.0, 90.0))

    assert projected is not None
    assert isfinite(projected.x)
    assert isfinite(projected.y)
    assert isfinite(projected.depth)
