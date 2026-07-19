from light_cylinder.config import AFTER_RAIN_CLEAR_WETNESS, AFTER_RAIN_MIN_DURATION
from light_cylinder.environment import EnvironmentPhase, EnvironmentState


def test_environment_starts_clear() -> None:
    state = EnvironmentState()

    assert state.phase is EnvironmentPhase.CLEAR
    assert not state.is_raining
    assert state.light_multiplier == 1.0


def test_environment_enters_rain_and_after_rain() -> None:
    state = EnvironmentState()

    state.set_rain(True, wetness=0.0)
    assert state.phase is EnvironmentPhase.RAIN
    assert state.is_raining
    assert state.light_multiplier < 1.0

    state.set_rain(False, wetness=0.4)
    assert state.phase is EnvironmentPhase.AFTER_RAIN
    assert state.is_after_rain
    assert state.wet_reflection > 0.0


def test_environment_recovers_to_clear_after_drying() -> None:
    state = EnvironmentState()
    state.set_rain(True, wetness=0.0)
    state.set_rain(False, wetness=0.4)

    state.update(AFTER_RAIN_MIN_DURATION + 0.1, AFTER_RAIN_CLEAR_WETNESS)

    assert state.phase is EnvironmentPhase.CLEAR
    assert state.light_multiplier > 0.9


def test_after_rain_dry_rate_changes_with_wetness() -> None:
    state = EnvironmentState(phase=EnvironmentPhase.AFTER_RAIN)

    wet_rate = state.dry_rate_multiplier(0.9)
    dry_rate = state.dry_rate_multiplier(0.1)

    assert wet_rate < dry_rate


def test_after_rain_reflection_outlives_wetness() -> None:
    state = EnvironmentState(phase=EnvironmentPhase.AFTER_RAIN, wet_reflection=0.6)

    assert state.effective_floor_wetness(0.1) > 0.1
