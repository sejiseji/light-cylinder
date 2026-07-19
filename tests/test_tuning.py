import pytest

from light_cylinder.config import (
    GRASS_COUNT,
    LIGHT_PARTICLE_COUNT,
    MENU_RAIN_INTENSITIES,
    MENU_STAGE_MAX,
    MENU_STAGE_MIN,
    MENU_WIND_MULTIPLIERS,
    MENU_WIND_SPEED_MULTIPLIERS,
    RAIN_DEFAULT_INTENSITY,
)
from light_cylinder.tuning import ObservationTuning


def test_observation_tuning_starts_at_current_stage_one_values() -> None:
    tuning = ObservationTuning()

    assert tuning.photons == MENU_STAGE_MIN
    assert tuning.grass == MENU_STAGE_MIN
    assert tuning.wind == MENU_STAGE_MIN
    assert tuning.rain == MENU_STAGE_MIN
    assert tuning.rotate == MENU_STAGE_MIN
    assert tuning.photon_count == LIGHT_PARTICLE_COUNT
    assert tuning.grass_count == GRASS_COUNT
    assert tuning.wind_multiplier == MENU_WIND_MULTIPLIERS[0]
    assert tuning.wind_speed_multiplier == MENU_WIND_SPEED_MULTIPLIERS[0]
    assert tuning.rain_intensity == RAIN_DEFAULT_INTENSITY


def test_observation_tuning_adjusts_and_clamps_stages() -> None:
    tuning = ObservationTuning()

    tuning.adjust_stage("rain", 9)
    assert tuning.rain == MENU_STAGE_MAX
    assert tuning.rain_intensity == MENU_RAIN_INTENSITIES[-1]

    tuning.adjust_stage("rain", -9)
    assert tuning.rain == MENU_STAGE_MIN

    tuning.adjust_stage("wind", 9)
    assert tuning.wind == MENU_STAGE_MAX
    assert tuning.wind_multiplier == MENU_WIND_MULTIPLIERS[-1]
    assert tuning.wind_speed_multiplier == MENU_WIND_SPEED_MULTIPLIERS[-1]


def test_observation_tuning_rejects_unknown_keys() -> None:
    tuning = ObservationTuning()

    with pytest.raises(ValueError):
        tuning.stage_for("mist")
