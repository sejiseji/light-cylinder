from __future__ import annotations

from dataclasses import dataclass

from light_cylinder.config import (
    MENU_AUTO_ROTATE_MULTIPLIERS,
    MENU_FIREFLY_COUNTS,
    MENU_GRASS_COUNTS,
    MENU_PHOTON_COUNTS,
    MENU_RAIN_INTENSITIES,
    MENU_STAGE_MAX,
    MENU_STAGE_MIN,
    MENU_WIND_MULTIPLIERS,
    MENU_WIND_SPEED_MULTIPLIERS,
)

MENU_SETTING_KEYS = ("photons", "grass", "wind", "rain", "rotate", "fireflies")


@dataclass(slots=True)
class ObservationTuning:
    photons: int = MENU_STAGE_MIN
    grass: int = MENU_STAGE_MIN
    wind: int = MENU_STAGE_MIN
    rain: int = MENU_STAGE_MIN
    rotate: int = MENU_STAGE_MIN
    fireflies: int = MENU_STAGE_MIN

    def stage_for(self, key: str) -> int:
        _validate_key(key)
        return getattr(self, key)

    def set_stage(self, key: str, stage: int) -> None:
        _validate_key(key)
        setattr(self, key, _clamp_stage(stage))

    def adjust_stage(self, key: str, delta: int) -> None:
        self.set_stage(key, self.stage_for(key) + delta)

    @property
    def photon_count(self) -> int:
        return MENU_PHOTON_COUNTS[self.photons - MENU_STAGE_MIN]

    @property
    def max_photon_count(self) -> int:
        return max(MENU_PHOTON_COUNTS)

    @property
    def grass_count(self) -> int:
        return MENU_GRASS_COUNTS[self.grass - MENU_STAGE_MIN]

    @property
    def max_grass_count(self) -> int:
        return max(MENU_GRASS_COUNTS)

    @property
    def wind_multiplier(self) -> float:
        return MENU_WIND_MULTIPLIERS[self.wind - MENU_STAGE_MIN]

    @property
    def wind_speed_multiplier(self) -> float:
        return MENU_WIND_SPEED_MULTIPLIERS[self.wind - MENU_STAGE_MIN]

    @property
    def rain_intensity(self) -> float:
        return MENU_RAIN_INTENSITIES[self.rain - MENU_STAGE_MIN]

    @property
    def auto_rotate_multiplier(self) -> float:
        return MENU_AUTO_ROTATE_MULTIPLIERS[self.rotate - MENU_STAGE_MIN]

    @property
    def firefly_count(self) -> int:
        return MENU_FIREFLY_COUNTS[self.fireflies - MENU_STAGE_MIN]


def _clamp_stage(stage: int) -> int:
    return max(MENU_STAGE_MIN, min(MENU_STAGE_MAX, stage))


def _validate_key(key: str) -> None:
    if key not in MENU_SETTING_KEYS:
        raise ValueError(f"unknown tuning key: {key}")
