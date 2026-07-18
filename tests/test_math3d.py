from math import pi

import pytest

from light_cylinder.math3d import Vec2, Vec3, clamp, lerp, lerp_vec3, rotate_x, rotate_y


def assert_vec3_close(actual: Vec3, expected: Vec3) -> None:
    assert actual.x == pytest.approx(expected.x)
    assert actual.y == pytest.approx(expected.y)
    assert actual.z == pytest.approx(expected.z)


def test_vec2_operations() -> None:
    first = Vec2(3.0, 4.0)
    second = Vec2(1.0, 2.0)

    assert first + second == Vec2(4.0, 6.0)
    assert first - second == Vec2(2.0, 2.0)
    assert first * 2 == Vec2(6.0, 8.0)
    assert first / 2 == Vec2(1.5, 2.0)
    assert first.length() == pytest.approx(5.0)
    assert first.length_squared() == pytest.approx(25.0)
    assert first.normalized().length() == pytest.approx(1.0)
    assert first.dot(second) == pytest.approx(11.0)


def test_vec3_operations() -> None:
    first = Vec3(1.0, 2.0, 3.0)
    second = Vec3(4.0, 5.0, 6.0)

    assert first + second == Vec3(5.0, 7.0, 9.0)
    assert second - first == Vec3(3.0, 3.0, 3.0)
    assert -first == Vec3(-1.0, -2.0, -3.0)
    assert first * 2 == Vec3(2.0, 4.0, 6.0)
    assert 2 * first == Vec3(2.0, 4.0, 6.0)
    assert second / 2 == Vec3(2.0, 2.5, 3.0)
    assert first.dot(second) == pytest.approx(32.0)
    assert Vec3(1.0, 0.0, 0.0).cross(Vec3(0.0, 1.0, 0.0)) == Vec3(0.0, 0.0, 1.0)


def test_vec3_length_and_normalization() -> None:
    vector = Vec3(2.0, 3.0, 6.0)

    assert vector.length_squared() == pytest.approx(49.0)
    assert vector.length() == pytest.approx(7.0)
    assert vector.normalized().length() == pytest.approx(1.0)


def test_zero_normalization_returns_zero() -> None:
    assert Vec2(0.0, 0.0).normalized() == Vec2(0.0, 0.0)
    assert Vec3(0.0, 0.0, 0.0).normalized() == Vec3(0.0, 0.0, 0.0)


def test_division_by_zero_is_explicit() -> None:
    with pytest.raises(ZeroDivisionError):
        Vec2(1.0, 0.0) / 0
    with pytest.raises(ZeroDivisionError):
        Vec3(1.0, 0.0, 0.0) / 0


def test_clamp_and_lerp() -> None:
    assert clamp(5.0, 0.0, 10.0) == pytest.approx(5.0)
    assert clamp(-5.0, 0.0, 10.0) == pytest.approx(0.0)
    assert clamp(15.0, 0.0, 10.0) == pytest.approx(10.0)
    assert lerp(10.0, 20.0, 0.25) == pytest.approx(12.5)
    assert lerp_vec3(Vec3(0.0, 0.0, 0.0), Vec3(10.0, 20.0, 30.0), 0.5) == Vec3(
        5.0,
        10.0,
        15.0,
    )


def test_rotate_x() -> None:
    assert_vec3_close(rotate_x(Vec3(0.0, 1.0, 0.0), pi / 2), Vec3(0.0, 0.0, 1.0))


def test_rotate_y() -> None:
    assert_vec3_close(rotate_y(Vec3(0.0, 0.0, 1.0), pi / 2), Vec3(1.0, 0.0, 0.0))
