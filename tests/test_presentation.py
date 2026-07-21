from light_cylinder.app import (
    MENU_BUTTON_RECT,
    LightCylinderApp,
    atmospheric_dither_density,
    atmospheric_dither_visible,
    atmospheric_light_factor,
    firefly_draw_radius,
    particle_draw_radius,
    select_floor_color,
    select_grass_color,
    select_grass_light_color,
    select_particle_color,
    select_rain_color,
    select_splash_color,
)
from light_cylinder.config import (
    ATMOSPHERIC_DITHER_BASE_DENSITY,
    GRASS_WIDTH_MULTIPLIER,
    LIGHT_ACCENT_BAND_COUNT,
    MENU_RAIN_INTENSITIES,
    OBSERVATION_CYCLE_CLEAR_DURATION,
    OBSERVATION_CYCLE_LIGHT_RAIN_DURATION,
    OBSERVATION_CYCLE_SHADOW_DURATION,
    PALETTE_BRIGHT_PARTICLE,
    PALETTE_DIM_PARTICLE,
    PALETTE_DISTANT_GRASS,
    PALETTE_FOREGROUND_GRASS,
    PALETTE_GROUND_SHADOW,
    PALETTE_GROUND_STRONG_LIGHT,
    PALETTE_LIT_GRASS,
    PALETTE_NORMAL_GRASS,
    PALETTE_STRONGLY_LIT_GRASS,
)


def test_grass_depth_color_mapping() -> None:
    assert select_grass_color(0, False) == PALETTE_NORMAL_GRASS
    assert select_grass_color(1, False) == PALETTE_FOREGROUND_GRASS
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
    assert select_floor_color(PALETTE_GROUND_SHADOW, 0.0, 0.8) != PALETTE_GROUND_SHADOW


def test_particle_color_mapping_uses_dim_and_bright_levels() -> None:
    assert select_particle_color(0.3) == PALETTE_DIM_PARTICLE
    assert select_particle_color(0.8) == PALETTE_BRIGHT_PARTICLE


def test_particle_draw_radius_has_clear_size_steps() -> None:
    assert particle_draw_radius(0.2, 0.3) == 0
    assert particle_draw_radius(0.7, 0.6) == 1
    assert particle_draw_radius(0.85, 0.65) == 2
    assert particle_draw_radius(1.0, 0.9) == 3


def test_atmospheric_dither_density_prefers_center_mid_air() -> None:
    center = atmospheric_dither_density(224, 360)
    edge = atmospheric_dither_density(30, 360)
    floor = atmospheric_dither_density(224, 760)

    assert center <= ATMOSPHERIC_DITHER_BASE_DENSITY
    assert center > edge
    assert center > floor


def test_atmospheric_dither_light_and_shadow_modulate_density() -> None:
    baseline = atmospheric_dither_density(224, 360, light_factor=0.0, cloud_shadow=0.0)
    lit = atmospheric_dither_density(224, 360, light_factor=1.0, cloud_shadow=0.0)
    shadow = atmospheric_dither_density(224, 360, light_factor=0.0, cloud_shadow=1.0)

    assert lit > baseline
    assert shadow < baseline


def test_atmospheric_light_factor_fades_from_axis() -> None:
    axis = ((200.0, 100.0), (240.0, 500.0))

    near = atmospheric_light_factor(220, 300, axis)
    far = atmospheric_light_factor(320, 300, axis)

    assert near > far
    assert atmospheric_light_factor(220, 300, None) == 0.0


def test_atmospheric_dither_visible_uses_stable_sparse_pattern() -> None:
    density = atmospheric_dither_density(224, 360, light_factor=1.0)

    first = atmospheric_dither_visible(224, 360, phase=2, density=density)
    second = atmospheric_dither_visible(224, 360, phase=2, density=density)

    assert first is second
    assert not atmospheric_dither_visible(224, 360, phase=2, density=0.0)


def test_firefly_draw_radius_increases_toward_camera() -> None:
    far = firefly_draw_radius(depth=560.0, camera_distance=455.0, glow=0.8)
    near = firefly_draw_radius(depth=300.0, camera_distance=455.0, glow=0.8)

    assert far == 2
    assert near > far


def test_rain_color_mapping_stays_quiet_until_strong_light() -> None:
    assert select_rain_color(0.3, 0) == 5
    assert select_rain_color(0.3, 1) == 12
    assert select_rain_color(0.3, 2) == 6
    assert select_rain_color(0.3, 3) == 7
    assert select_rain_color(0.98, 2) == 7


def test_rain_depth_tier_marks_far_rain_for_shadow_color() -> None:
    app = LightCylinderApp()

    assert app._rain_depth_tier(app.camera.distance + 120.0) == 0
    assert app._rain_depth_tier(app.camera.distance + 48.0) == 1
    assert app._rain_depth_tier(app.camera.distance) == 2
    assert app._rain_depth_tier(app.camera.distance - 80.0) == 3


def test_splash_color_mapping_fades_quickly() -> None:
    assert select_splash_color(0.8, 0.1) == PALETTE_BRIGHT_PARTICLE
    assert select_splash_color(0.8, 0.9) == PALETTE_DIM_PARTICLE


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
    app._set_auto_rotate(True)
    app.auto_pitch_center = 0.7

    app._reset_camera()

    assert app.camera_pitch_velocity == 0.0
    assert app.auto_pitch_center == app.camera.pitch
    assert app.auto_pitch_phase == 0.0


def test_auto_rotate_pitch_sways_around_manual_center() -> None:
    app = LightCylinderApp()
    app._set_auto_rotate(True)
    app._update_auto_pitch_center_from_manual_pitch(0.12)

    assert app.auto_pitch_center == app.camera.clamp_pitch(app.camera.pitch + 0.12)

    delta = app._auto_rotate_pitch_delta(1.0, 0.0)

    assert delta != 0.0
    assert app.auto_pitch_phase > 0.0


def test_auto_rotate_enable_uses_current_pitch_as_center() -> None:
    app = LightCylinderApp()
    app.camera.orbit(0.0, 0.18)

    app._set_auto_rotate(True)

    assert app.auto_rotate
    assert app.auto_pitch_center == app.camera.pitch


def test_grass_taper_offsets_use_wider_base_multiplier() -> None:
    app = LightCylinderApp()

    root_offsets = app._grass_taper_offsets(0, 0, 8, 0, 2, 0, 5)
    tip_offsets = app._grass_taper_offsets(0, 0, 8, 0, 2, 4, 5)

    assert GRASS_WIDTH_MULTIPLIER == 2
    assert len(root_offsets) >= len(tip_offsets) * 2
    assert root_offsets


def test_light_band_quads_are_available_for_depth_sorting() -> None:
    app = LightCylinderApp()

    quads = app._light_band_quads()

    assert quads
    assert all(len(quad) == 9 for _depth, quad in quads)
    assert all(depth > 0.0 for depth, _quad in quads)


def test_yellow_light_accent_bands_add_lines_and_a_band() -> None:
    app = LightCylinderApp()

    accents = app._light_accent_bands()

    assert len(accents) == LIGHT_ACCENT_BAND_COUNT
    kinds = {kind for _depth, kind, _payload in accents}
    assert kinds == {"accent_line", "accent_band"}
    assert all(payload[-1] == PALETTE_GROUND_STRONG_LIGHT for _depth, _kind, payload in accents)


def test_photons_are_available_for_depth_sorting_with_light_bands() -> None:
    app = LightCylinderApp()

    particle_items = app._light_particle_items()
    band_depths = [depth for depth, _quad in app._light_band_quads()]

    assert particle_items
    assert band_depths
    assert all(depth > 0.0 for depth, _particle, _position in particle_items)


def test_foxtails_are_available_for_depth_sorting() -> None:
    app = LightCylinderApp()

    items = app._foxtail_items()

    assert len(items) == 3
    assert all(depth > 0.0 for depth, _foxtail, _shape in items)


def test_menu_button_toggles_observation_panel() -> None:
    app = LightCylinderApp()
    x, y, width, height = MENU_BUTTON_RECT

    handled = app._handle_menu_click_at(x + width // 2, y + height // 2)

    assert handled
    assert app.menu_open


def test_menu_stepper_updates_stage_and_rain_amount() -> None:
    app = LightCylinderApp()
    app.menu_open = True
    rain_index = 3
    _minus_rect, plus_rect = app._menu_stepper_rects(rain_index)
    x, y, width, height = plus_rect

    handled = app._handle_menu_click_at(x + width // 2, y + height // 2)

    assert handled
    assert app.tuning.rain == 2
    assert app.rain_field.intensity == MENU_RAIN_INTENSITIES[1]


def test_menu_stepper_updates_firefly_count_stage() -> None:
    app = LightCylinderApp()
    app.menu_open = True
    firefly_index = 5
    _minus_rect, plus_rect = app._menu_stepper_rects(firefly_index)
    x, y, width, height = plus_rect

    handled = app._handle_menu_click_at(x + width // 2, y + height // 2)

    assert handled
    assert app.tuning.fireflies == 2
    assert app.tuning.firefly_count == 6


def test_menu_auto_toggle_changes_auto_rotate() -> None:
    app = LightCylinderApp()
    app.menu_open = True
    x, y, width, height = app._menu_auto_toggle_rect()

    handled = app._handle_menu_click_at(x + width // 2, y + height // 2)

    assert handled
    assert app.auto_rotate


def test_wind_stage_amplifies_sampled_wind_motion() -> None:
    app = LightCylinderApp()
    position = app.world.sample_bottom_point(0.6, 0.2)
    steady = app.wind_field.steady_sample()
    stage_one_motion = (app._wind_sample(position, phase=0.5) - steady).length()

    app.tuning.set_stage("wind", 3)
    stage_three_motion = (app._wind_sample(position, phase=0.5) - steady).length()

    assert stage_three_motion > stage_one_motion * 2.0


def test_wind_stage_speeds_up_wind_motion_time() -> None:
    app = LightCylinderApp()

    app._update_wind_motion_time(1.0)
    stage_one_time = app.wind_motion_time
    app.wind_motion_time = 0.0
    app.tuning.set_stage("wind", 3)
    app._update_wind_motion_time(1.0)

    assert app.wind_motion_time == stage_one_time * 2.0


def test_menu_rain_toggle_changes_rain_enabled() -> None:
    app = LightCylinderApp()
    app.menu_open = True
    x, y, width, height = app._menu_rain_toggle_rect()

    handled = app._handle_menu_click_at(x + width // 2, y + height // 2)

    assert handled
    assert app.rain_enabled


def test_menu_firefly_toggle_changes_firefly_enabled() -> None:
    app = LightCylinderApp()
    app.menu_open = True
    x, y, width, height = app._menu_firefly_toggle_rect()

    handled = app._handle_menu_click_at(x + width // 2, y + height // 2)

    assert handled
    assert app.firefly_enabled


def test_firefly_items_are_hidden_until_enabled() -> None:
    app = LightCylinderApp()
    app.firefly_field.spawn_timer = 0.0
    app.firefly_field.update(0.0, app._wind_sample(app.world.bottom_center), "CLEAR", 0.0)

    assert app._firefly_items() == ()

    app._set_firefly_enabled(True)

    assert app._firefly_items()


def test_observation_cycle_uses_menu_rain_stage_as_base_amount() -> None:
    app = LightCylinderApp()
    app.tuning.set_stage("rain", 2)
    app._set_observation_cycle_enabled(True)
    app.observation_cycle.update(
        OBSERVATION_CYCLE_CLEAR_DURATION
        + OBSERVATION_CYCLE_SHADOW_DURATION
        + OBSERVATION_CYCLE_LIGHT_RAIN_DURATION
    )

    app._apply_observation_cycle()

    assert app.rain_field.intensity == MENU_RAIN_INTENSITIES[1]
    assert app.rain_enabled


def test_manual_rain_control_disables_observation_cycle_without_changing_stage() -> None:
    app = LightCylinderApp()
    app.tuning.set_stage("rain", 3)
    app._set_observation_cycle_enabled(True)

    app._set_observation_cycle_enabled(False)

    assert app.tuning.rain == 3
    assert app.rain_field.intensity == MENU_RAIN_INTENSITIES[2]
