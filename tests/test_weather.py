from itertools import pairwise
from math import isfinite

import pytest

from light_cylinder.config import (
    GUST_STRENGTH,
    MICRO_WIND_AMOUNT,
    WIND_BASE_SPEED,
    WIND_SLOW_PULSE_AMOUNT,
    WIND_TIME_WRAP_SECONDS,
)
from light_cylinder.math3d import Vec3
from light_cylinder.weather import WindField


def test_initial_state() -> None:
    wind = WindField.create_default()

    assert wind.elapsed_time == 0.0
    assert wind.base_direction.y == 0.0
    assert wind.base_direction.length() == pytest.approx(1.0)
    assert wind.base_speed == pytest.approx(WIND_BASE_SPEED)


def test_update_advances_time_and_rejects_bad_dt() -> None:
    wind = WindField.create_default()

    wind.update(0.5)

    assert wind.elapsed_time == pytest.approx(0.5)
    with pytest.raises(ValueError):
        wind.update(-0.1)
    with pytest.raises(ValueError):
        wind.update(float("inf"))


def test_time_wrap_stays_finite() -> None:
    wind = WindField.create_default()

    wind.update(WIND_TIME_WRAP_SECONDS + 12.0)

    assert wind.elapsed_time == pytest.approx(12.0)
    assert isfinite(wind.sample(Vec3(0.0, 0.0, 0.0)).length())


def test_same_seed_and_time_are_deterministic() -> None:
    first = WindField.create_default()
    second = WindField.create_default()
    first.update(3.5)
    second.update(3.5)
    position = Vec3(12.0, 0.0, -7.0)

    assert first.sample(position, phase=0.25) == second.sample(position, phase=0.25)


def test_sample_is_stable_for_same_position_and_time() -> None:
    wind = WindField.create_default()
    wind.update(2.0)
    position = Vec3(4.0, 0.0, 6.0)

    assert wind.sample(position, phase=1.0) == wind.sample(position, phase=1.0)


def test_spatial_phase_changes_sample() -> None:
    wind = WindField.create_default()
    wind.update(2.0)

    assert wind.sample(Vec3(0.0, 0.0, 0.0)) != wind.sample(Vec3(100.0, 0.0, 50.0))


def test_sample_is_finite_and_horizontal() -> None:
    wind = WindField.create_default()
    wind.update(8.0)

    sample = wind.sample(Vec3(30.0, 0.0, -15.0), phase=2.0)

    assert isfinite(sample.x)
    assert isfinite(sample.y)
    assert isfinite(sample.z)
    assert sample.y == 0.0


def test_amplified_sample_keeps_steady_anchor_and_expands_motion() -> None:
    wind = WindField.create_default()
    wind.update(2.0)
    position = Vec3(30.0, 0.0, -15.0)
    steady = wind.steady_sample()
    stage_one_motion = wind.sample(position, phase=2.0) - steady
    stage_three_motion = wind.amplified_sample(position, phase=2.0, motion_multiplier=2.7) - steady

    assert wind.amplified_sample(position, phase=2.0, motion_multiplier=1.0) == wind.sample(
        position,
        phase=2.0,
    )
    assert stage_three_motion.length() == pytest.approx(stage_one_motion.length() * 2.7)


def test_sample_at_can_use_a_faster_motion_time() -> None:
    wind = WindField.create_default()
    position = Vec3(30.0, 0.0, -15.0)

    early = wind.sample_at(1.0, position, phase=2.0)
    faster = wind.sample_at(2.0, position, phase=2.0)

    assert early != faster


def test_gust_strength_range_and_continuity() -> None:
    wind = WindField.create_default()
    values = []
    for _ in range(90):
        wind.update(0.1)
        values.append(wind.current_gust_strength)

    assert min(values) >= 0.0
    assert max(values) <= GUST_STRENGTH
    assert max(abs(a - b) for a, b in pairwise(values)) < GUST_STRENGTH


def test_long_running_sample_remains_finite() -> None:
    wind = WindField.create_default()

    for _ in range(600):
        wind.update(1.0)
    sample = wind.sample(Vec3(20.0, 0.0, 30.0), phase=4.0)

    assert isfinite(sample.length())


def test_wind_magnitude_has_reasonable_bound() -> None:
    wind = WindField.create_default()
    max_seen = 0.0
    for _ in range(240):
        wind.update(0.25)
        max_seen = max(max_seen, wind.sample(Vec3(96.0, 0.0, -96.0), phase=3.0).length())

    assert max_seen <= WIND_BASE_SPEED * (1.0 + WIND_SLOW_PULSE_AMOUNT + MICRO_WIND_AMOUNT) + (
        GUST_STRENGTH
    )
