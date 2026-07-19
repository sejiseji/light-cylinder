import pytest

from light_cylinder.config import (
    OBSERVATION_CYCLE_CLEAR_DURATION,
    OBSERVATION_CYCLE_LIGHT_RAIN_DURATION,
    OBSERVATION_CYCLE_RAIN_DURATION,
    OBSERVATION_CYCLE_SHADOW_DURATION,
)
from light_cylinder.observation_cycle import ObservationCycle, ObservationCyclePhase


def test_observation_cycle_starts_disabled_and_clear() -> None:
    cycle = ObservationCycle()
    sample = cycle.sample()

    assert not cycle.enabled
    assert sample.phase is ObservationCyclePhase.CLEAR
    assert not sample.is_raining
    assert sample.light_multiplier == 1.0


def test_observation_cycle_moves_through_shadow_and_rain() -> None:
    cycle = ObservationCycle(enabled=True)

    cycle.update(OBSERVATION_CYCLE_CLEAR_DURATION + OBSERVATION_CYCLE_SHADOW_DURATION * 0.5)
    shadow_sample = cycle.sample()

    assert shadow_sample.phase is ObservationCyclePhase.SHADOW
    assert not shadow_sample.is_raining
    assert shadow_sample.light_multiplier < 1.0

    cycle.update(OBSERVATION_CYCLE_SHADOW_DURATION * 0.5 + OBSERVATION_CYCLE_LIGHT_RAIN_DURATION)
    rain_sample = cycle.sample()

    assert rain_sample.phase is ObservationCyclePhase.RAIN
    assert rain_sample.rain_multiplier == pytest.approx(1.0)


def test_observation_cycle_wraps_back_to_clear() -> None:
    cycle = ObservationCycle(enabled=True)

    cycle.update(cycle.duration + 1.0)

    assert cycle.sample().phase is ObservationCyclePhase.CLEAR


def test_observation_cycle_rejects_bad_delta_time() -> None:
    cycle = ObservationCycle(enabled=True)

    with pytest.raises(ValueError):
        cycle.update(-0.1)


def test_observation_cycle_can_reach_after_rain_phase() -> None:
    cycle = ObservationCycle(enabled=True)

    cycle.update(
        OBSERVATION_CYCLE_CLEAR_DURATION
        + OBSERVATION_CYCLE_SHADOW_DURATION
        + OBSERVATION_CYCLE_LIGHT_RAIN_DURATION
        + OBSERVATION_CYCLE_RAIN_DURATION
        + 1.0
    )
    sample = cycle.sample()

    assert sample.phase is ObservationCyclePhase.AFTER_RAIN
    assert not sample.is_raining
    assert sample.light_multiplier < 1.0
