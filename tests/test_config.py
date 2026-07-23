from light_cylinder import config


def test_display_constants() -> None:
    assert config.REFERENCE_WIDTH == 393
    assert config.REFERENCE_HEIGHT == 852
    assert config.RENDER_WIDTH == 448
    assert config.RENDER_HEIGHT == 852
    assert config.COMPOSITION_SAFE_WIDTH == 393
    assert config.TARGET_FPS == 30
    assert config.UI_TEXT_SCALE == 3
    assert config.ATMOSPHERIC_DITHER_STEP == 4
    assert 0.08 <= config.ATMOSPHERIC_DITHER_BASE_DENSITY <= 0.12
    assert 0.0 < config.ATMOSPHERIC_DITHER_LIGHT_BOOST < config.ATMOSPHERIC_DITHER_BASE_DENSITY
    assert 0.0 <= config.ATMOSPHERIC_DITHER_SHADOW_REDUCTION <= 1.0
    assert config.ATMOSPHERIC_DITHER_PHASE_RATE > 0
    assert config.ATMOSPHERIC_DITHER_HASH_MODULUS > 0


def test_safe_area_invariants() -> None:
    assert config.RENDER_WIDTH >= config.COMPOSITION_SAFE_WIDTH
    assert config.SAFE_LEFT >= 0
    assert config.SAFE_RIGHT <= config.RENDER_WIDTH
    assert config.SAFE_RIGHT - config.SAFE_LEFT == config.COMPOSITION_SAFE_WIDTH
    assert config.RENDER_HEIGHT == config.REFERENCE_HEIGHT
    assert config.TARGET_FPS > 0


def test_config_validation_accepts_lc000_values() -> None:
    config.validate_display_config()


def test_camera_config_invariants() -> None:
    assert config.CAMERA_MIN_DISTANCE > 0
    assert config.CAMERA_MIN_DISTANCE <= config.CAMERA_INITIAL_DISTANCE
    assert config.CAMERA_INITIAL_DISTANCE <= config.CAMERA_MAX_DISTANCE
    assert config.CAMERA_MIN_PITCH < config.CAMERA_MAX_PITCH
    assert config.CAMERA_FOCAL_LENGTH > 0
    assert config.CAMERA_YAW_SPEED > 0
    assert config.CAMERA_PITCH_SPEED > 0
    assert config.CAMERA_ZOOM_SPEED > 0
    assert config.MOUSE_YAW_SPEED > 0
    assert config.MOUSE_PITCH_SPEED > 0
    assert config.MOUSE_WHEEL_ZOOM_SPEED > 0
    assert 0.0 <= config.CAMERA_INERTIA_DECAY < 1.0
    assert config.AUTO_ROTATE_SPEED > 0
    assert 6.283185307179586 / (config.AUTO_ROTATE_SPEED * config.TARGET_FPS) >= 30
    assert config.AUTO_ROTATE_PITCH_SWAY_AMOUNT > 0
    assert config.AUTO_ROTATE_PITCH_SWAY_RATE > 0
    assert 0.0 < config.AUTO_ROTATE_PITCH_FOLLOW <= 1.0
    assert config.CYLINDER_RADIUS == 96.0
    assert config.CYLINDER_HEIGHT == 300.0
    assert config.CYLINDER_RADIAL_SEGMENTS == 32
    assert config.CYLINDER_VERTICAL_GUIDES == 8
    assert 0.0 <= config.CYLINDER_TARGET_HEIGHT_FACTOR <= 1.0
    assert config.GRASS_SEED == 1729
    assert config.GRASS_COUNT == 120
    assert config.GRASS_SEGMENTS == 5
    assert config.GRASS_MIN_HEIGHT > 0
    assert config.GRASS_MIN_HEIGHT <= config.GRASS_MAX_HEIGHT
    assert config.GRASS_MIN_BEND <= config.GRASS_MAX_BEND
    assert config.GRASS_MIN_STIFFNESS <= config.GRASS_MAX_STIFFNESS
    assert config.GRASS_WIDTH_MULTIPLIER == 2
    assert config.GRASS_CLUSTER_LAYOUT
    assert 0.0 <= config.GRASS_OPEN_SPACE_WEIGHT <= 1.0
    assert 0.0 <= config.GRASS_RADIAL_DENSITY_WEIGHT <= 1.0
    assert config.GROUND_SOIL_MARK_COUNT >= 100
    assert 0.0 <= config.GROUND_SOIL_MARK_MIN_RADIUS < config.GROUND_SOIL_MARK_MAX_RADIUS <= 1.0
    assert config.FOXTAIL_SEED == 8123
    assert 2 <= config.FOXTAIL_COUNT <= 3
    assert config.FOXTAIL_STEM_SEGMENTS == 5
    assert 1.4 <= config.FOXTAIL_HEIGHT_MIN_FACTOR <= config.FOXTAIL_HEIGHT_MAX_FACTOR <= 1.8
    assert config.FOXTAIL_HEAD_SEGMENTS_MIN >= 6
    assert config.FOXTAIL_HEAD_SEGMENTS_MAX <= 10
    assert 0.0 < config.FOXTAIL_HEAD_LAG_FACTOR < 1.0
    assert config.FOXTAIL_WIND_RESPONSE_SCALE > 0.0
    assert 0.0 <= config.FOXTAIL_RAIN_DROOP_SCALE <= 1.0
    assert config.WIND_SEED == 2718
    assert config.WIND_BASE_SPEED >= 0.65
    assert config.WIND_RESPONSE_SCALE >= 17.0
    assert 0.0 <= config.WIND_SLOW_PULSE_AMOUNT <= 1.0
    assert config.WIND_DIRECTION_SWAY_AMOUNT >= 0.25
    assert config.MICRO_WIND_AMOUNT >= 0.16
    assert config.WIND_MAX_BEND_RATIO > 0
    assert config.WIND_TIME_WRAP_SECONDS > 0
    assert config.GUST_INTERVAL > 0
    assert config.GUST_DURATION > 0
    assert config.GUST_STRENGTH >= 0
    assert config.LIGHT_SEED == 4055
    assert config.LIGHT_PARTICLE_COUNT == 360
    assert 20 <= config.LIGHT_GROUND_SPARK_COUNT <= 40
    assert len(config.LIGHT_BEAM_ORIGIN) == 3
    assert config.LIGHT_BEAM_ORIGIN[1] > config.CYLINDER_HEIGHT
    assert len(config.LIGHT_BEAM_DIRECTION) == 3
    assert config.LIGHT_BEAM_LENGTH > config.CYLINDER_HEIGHT
    assert config.LIGHT_BEAM_RADIUS > 0
    assert 0 <= config.LIGHT_BEAM_CORE_RADIUS < config.LIGHT_BEAM_RADIUS
    assert config.LIGHT_BEAM_END_FADE > 0
    assert config.PROJECT_TITLE == config.DISPLAY_TITLE_EN
    assert config.DISPLAY_TITLE_JA == "光の標本"
    assert 0.0 <= config.LIGHT_CLOUD_SHADOW_AMOUNT <= 1.0
    assert 0.0 <= config.LIGHT_CLOUD_SHADOW_FLOOR <= 1.0
    assert config.LIGHT_CLOUD_SHADOW_RATE >= 0
    assert config.LIGHT_PARTICLE_SWAY_RATE >= 0
    assert config.LIGHT_PARTICLE_SWAY_AMOUNT >= 0
    assert config.LIGHT_PARTICLE_AXIS_ATTRACTION >= 0
    assert config.LIGHT_PARTICLE_WALK_RATE >= 0
    assert config.LIGHT_PARTICLE_WALK_AMOUNT >= 0
    assert config.LIGHT_PARTICLE_DRIFT_MIN <= config.LIGHT_PARTICLE_DRIFT_MAX
    assert 0 < config.LIGHT_PARTICLE_SIZE_MIN <= config.LIGHT_PARTICLE_SIZE_MAX
    assert config.LIGHT_PARTICLE_VISIBILITY_THRESHOLD >= 0
    assert config.LIGHT_GROUND_SPARK_THRESHOLD >= 0
    assert 1 <= config.LIGHT_BAND_COUNT <= 5
    assert 0 < config.LIGHT_BAND_WIDTH_MIN <= config.LIGHT_BAND_WIDTH_MAX
    assert len(config.LIGHT_BAND_WIDTH_FACTORS) == config.LIGHT_BAND_COUNT
    assert min(config.LIGHT_BAND_WIDTH_FACTORS) < max(config.LIGHT_BAND_WIDTH_FACTORS)
    assert min(config.LIGHT_BAND_WIDTH_FACTORS) < 0.5
    assert config.LIGHT_BAND_WIDTH_RATE >= 0
    assert config.LIGHT_BAND_ALPHA_PATTERN >= 0
    assert (
        config.LIGHT_GRASS_THRESHOLD_LOW
        <= config.LIGHT_GRASS_THRESHOLD_MEDIUM
        <= config.LIGHT_GRASS_THRESHOLD_HIGH
    )
    assert (
        config.LIGHT_FLOOR_THRESHOLD_LOW
        <= config.LIGHT_FLOOR_THRESHOLD_MEDIUM
        <= config.LIGHT_FLOOR_THRESHOLD_HIGH
    )
    assert config.RAIN_SEED == 9182
    assert config.RAIN_DROP_COUNT == 64
    assert 0.0 <= config.RAIN_DEFAULT_INTENSITY <= 1.0
    assert 0.0 < config.RAIN_INTENSITY_STEP <= 1.0
    assert config.RAIN_MIN_FALL_SPEED <= config.RAIN_MAX_FALL_SPEED
    assert config.RAIN_MIN_LENGTH <= config.RAIN_MAX_LENGTH
    assert len(config.RAIN_SHORT_LENGTHS) == 3
    assert tuple(sorted(config.RAIN_SHORT_LENGTHS)) == config.RAIN_SHORT_LENGTHS
    assert config.RAIN_SHORT_LENGTHS[0] == config.RAIN_MIN_LENGTH
    assert config.RAIN_SHORT_LENGTHS[-1] == config.RAIN_MAX_LENGTH
    assert config.RAIN_STATIC_STREAK_COUNT >= 48
    assert config.RAIN_STATIC_STREAK_MIN_LENGTH >= config.RAIN_MAX_LENGTH * 3
    assert config.RAIN_STATIC_STREAK_MIN_LENGTH <= config.RAIN_STATIC_STREAK_MAX_LENGTH
    assert (
        0.0
        <= config.RAIN_STATIC_STREAK_MIN_HEIGHT_FACTOR
        < config.RAIN_STATIC_STREAK_MAX_HEIGHT_FACTOR
        <= 1.0
    )
    assert config.RAIN_STATIC_STREAK_FLASH_RATE > 0.0
    assert 0.998 <= config.RAIN_STATIC_STREAK_FLASH_THRESHOLD <= 1.0
    assert config.RAIN_WIND_DRIFT_SCALE >= 0
    assert config.RAIN_WIND_TILT_SCALE >= 0
    assert 0.0 <= config.RAIN_BRIGHT_VISIBILITY_THRESHOLD <= 1.0
    assert config.RAIN_DEPTH_COLORS == (5, 12, 6, 7)
    assert config.RAIN_SPLASH_LIFETIME > 0
    assert config.RAIN_SPLASH_GRAVITY >= 0
    assert config.RAIN_SPLASH_SPEED >= 0
    assert config.RAIN_SPLASHES_PER_IMPACT >= 0
    assert 0.0 <= config.RAIN_GROUND_WETNESS_GAIN <= 1.0
    assert config.RAIN_GROUND_DRY_RATE >= 0
    assert config.RAIN_GRASS_IMPACT_RADIUS > 0
    assert config.RAIN_GRASS_IMPACT_DECAY_RATE >= 0
    assert config.RAIN_GRASS_REACTION_BEND_SCALE >= 0
    assert 0.0 <= config.AFTER_RAIN_CLEAR_WETNESS <= config.AFTER_RAIN_MIN_WETNESS <= 1.0
    assert config.AFTER_RAIN_MIN_DURATION >= 0
    assert config.AFTER_RAIN_CLOUD_RECOVERY_RATE >= 0
    assert 0.0 <= config.AFTER_RAIN_LIGHT_SHADOW_AMOUNT <= 1.0
    assert config.AFTER_RAIN_REFLECTION_DECAY_RATE >= 0
    assert 0.0 <= config.AFTER_RAIN_DRY_RATE_MIN <= config.AFTER_RAIN_DRY_RATE_MAX
    assert config.TIP_DROPLET_MAX_COUNT >= 0
    assert 0.0 <= config.TIP_DROPLET_LIGHT_THRESHOLD <= 1.0
    assert config.TIP_DROPLET_HOLD_MIN <= config.TIP_DROPLET_HOLD_MAX
    assert config.TIP_DROPLET_FALL_SPEED >= 0
    assert config.FIREFLY_SEED == 7341
    assert config.FIREFLY_MAX_COUNT == 9
    assert 0.0 <= config.FIREFLY_TARGET_MIN_HEIGHT_FACTOR < config.FIREFLY_TARGET_MAX_HEIGHT_FACTOR
    assert config.FIREFLY_TARGET_MAX_HEIGHT_FACTOR <= 1.0
    assert config.FIREFLY_TARGET_REACH_RADIUS > 0
    assert config.FIREFLY_TARGET_MIN_DISTANCE > config.FIREFLY_TARGET_REACH_RADIUS
    assert 0.0 < config.FIREFLY_LIFETIME_MIN <= config.FIREFLY_LIFETIME_MAX
    assert 0.0 < config.FIREFLY_SPAWN_DELAY_MIN <= config.FIREFLY_SPAWN_DELAY_MAX
    assert config.FIREFLY_RAIN_SPAWN_MULTIPLIER >= 0.0
    assert config.FIREFLY_RAIN_SPAWN_MULTIPLIER < config.FIREFLY_AFTER_RAIN_SPAWN_MULTIPLIER
    assert config.FIREFLY_AFTER_RAIN_SPAWN_MULTIPLIER < config.FIREFLY_CLEAR_SPAWN_MULTIPLIER
    assert 0.0 <= config.FIREFLY_STRONG_RAIN_THRESHOLD <= 1.0
    assert config.FIREFLY_MAX_SPEED > 0
    assert config.FIREFLY_WIND_INFLUENCE < 0.2
    assert 0.0 <= config.FIREFLY_VISIBLE_THRESHOLD < config.FIREFLY_BRIGHT_THRESHOLD
    assert config.FIREFLY_BRIGHT_THRESHOLD < config.FIREFLY_RING_THRESHOLD <= 1.0
    assert config.LIGHT_PARTICLE_MAX_COUNT >= config.LIGHT_PARTICLE_COUNT
    assert config.LIGHT_ACCENT_BAND_COUNT == 3
    assert len(config.LIGHT_ACCENT_BAND_WIDTHS) == config.LIGHT_ACCENT_BAND_COUNT
    assert min(config.LIGHT_ACCENT_BAND_WIDTHS) < 1.0
    assert config.MENU_STAGE_MIN == 1
    assert config.MENU_STAGE_MAX == 3
    assert config.MENU_PHOTON_COUNTS[0] == config.LIGHT_PARTICLE_COUNT
    assert config.MENU_PHOTON_COUNTS == (config.LIGHT_PARTICLE_COUNT, 720, 1080)
    assert config.MENU_GRASS_COUNTS[0] == config.GRASS_COUNT
    assert config.MENU_GRASS_COUNTS == (config.GRASS_COUNT, 180, 240)
    assert config.MENU_RAIN_INTENSITIES[0] == config.RAIN_DEFAULT_INTENSITY
    assert config.MENU_FIREFLY_COUNTS == (3, 6, config.FIREFLY_MAX_COUNT)
    assert len(config.MENU_WIND_MULTIPLIERS) == config.MENU_STAGE_MAX
    assert config.MENU_WIND_MULTIPLIERS == (1.0, 1.85, 2.7)
    assert len(config.MENU_WIND_SPEED_MULTIPLIERS) == config.MENU_STAGE_MAX
    assert config.MENU_WIND_SPEED_MULTIPLIERS == (1.0, 1.45, 2.0)
    assert len(config.MENU_AUTO_ROTATE_MULTIPLIERS) == config.MENU_STAGE_MAX
    assert config.OBSERVATION_CYCLE_CLEAR_DURATION > 0
    assert config.OBSERVATION_CYCLE_SHADOW_DURATION > 0
    assert config.OBSERVATION_CYCLE_LIGHT_RAIN_DURATION > 0
    assert config.OBSERVATION_CYCLE_RAIN_DURATION > 0
    assert config.OBSERVATION_CYCLE_AFTER_RAIN_DURATION > 0
    assert 0.0 <= config.OBSERVATION_CYCLE_CLOUD_SHADOW_AMOUNT <= 1.0
    assert 0.0 <= config.OBSERVATION_CYCLE_LIGHT_RAIN_MULTIPLIER <= 1.0
    for name in dir(config):
        if name.startswith("PALETTE_"):
            value = getattr(config, name)
            if isinstance(value, int):
                assert 0 <= value <= 15
    assert set(config.PALETTE_PRESETS) == {"morning", "noon", "evening"}
    assert config.PALETTE_PRESET in config.PALETTE_PRESETS
    grass_keys = ("foreground_grass", "lit_grass", "strongly_lit_grass")
    for preset in config.PALETTE_PRESETS.values():
        assert all(preset[key] != 10 for key in grass_keys)
