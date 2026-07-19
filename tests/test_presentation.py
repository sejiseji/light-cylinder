from light_cylinder.app import (
    LightCylinderApp,
    select_floor_color,
    select_grass_color,
    select_grass_light_color,
    select_particle_color,
    select_rain_color,
)
from light_cylinder.config import (
    PALETTE_BRIGHT_PARTICLE,
    PALETTE_DIM_PARTICLE,
    PALETTE_DISTANT_GRASS,
    PALETTE_GROUND_SHADOW,
    PALETTE_LIT_GRASS,
    PALETTE_NORMAL_GRASS,
    PALETTE_STRONGLY_LIT_GRASS,
)


def test_grass_depth_color_mapping() -> None:
    assert select_grass_color(0, False) == PALETTE_NORMAL_GRASS
    assert select_grass_color(1, False) == PALETTE_LIT_GRASS
    assert select_grass_color(2, False) == PALETTE_DISTANT_GRASS
    assert select_grass_color(0, True) == PALETTE_DISTANT_GRASS


def test_grass_light_mapping_prefers_tips() -> None:
    assert select_grass_light_color(PALETTE_DISTANT_GRASS, 0.7, 1.0) == PALETTE_STRONGLY_LIT_GRASS
    assert select_grass_light_color(PALETTE_DISTANT_GRASS, 0.38, 1.0) == PALETTE_LIT_GRASS
    assert select_grass_light_color(PALETTE_DISTANT_GRASS, 0.16, 1.0) == PALETTE_NORMAL_GRASS
    assert select_grass_light_color(PALETTE_DISTANT_GRASS, 0.16, 0.46) == PALETTE_DISTANT_GRASS


def test_floor_light_mapping_has_three_levels() -> None:
    assert select_floor_color(PALETTE_GROUND_SHADOW, 0.0) == PALETTE_GROUND_SHADOW
    assert select_floor_color(PALETTE_GROUND_SHADOW, 0.5) != PALETTE_GROUND_SHADOW
    assert select_floor_color(PALETTE_GROUND_SHADOW, 0.9) != PALETTE_GROUND_SHADOW


def test_particle_color_mapping_uses_dim_and_bright_levels() -> None:
    assert select_particle_color(0.3) == PALETTE_DIM_PARTICLE
    assert select_particle_color(0.8) == PALETTE_BRIGHT_PARTICLE


def test_rain_color_mapping_stays_quiet_until_strong_light() -> None:
    assert select_rain_color(0.3) == PALETTE_DIM_PARTICLE
    assert select_rain_color(0.8) == PALETTE_BRIGHT_PARTICLE


def test_camera_motion_has_short_inertia() -> None:
    app = LightCylinderApp()

    first = app._camera_motion_delta("yaw", 0.1)
    second = app._camera_motion_delta("yaw", 0.0)
    third = app._camera_motion_delta("yaw", 0.0)

    assert first == 0.1
    assert 0.0 < third < second < first


def test_camera_reset_clears_inertia() -> None:
    app = LightCylinderApp()
    app._camera_motion_delta("pitch", 0.1)

    app._reset_camera()

    assert app.camera_pitch_velocity == 0.0
