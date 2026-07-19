from light_cylinder import config


def test_display_constants() -> None:
    assert config.REFERENCE_WIDTH == 393
    assert config.REFERENCE_HEIGHT == 852
    assert config.RENDER_WIDTH == 448
    assert config.RENDER_HEIGHT == 852
    assert config.COMPOSITION_SAFE_WIDTH == 393
    assert config.TARGET_FPS == 30


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
    assert config.CYLINDER_RADIUS == 96.0
    assert config.CYLINDER_HEIGHT == 240.0
    assert config.CYLINDER_RADIAL_SEGMENTS == 32
    assert config.CYLINDER_VERTICAL_GUIDES == 8
    assert 0.0 <= config.CYLINDER_TARGET_HEIGHT_FACTOR <= 1.0
    assert config.GRASS_SEED == 1729
    assert config.GRASS_COUNT == 420
    assert config.GRASS_SEGMENTS == 5
    assert config.GRASS_MIN_HEIGHT > 0
    assert config.GRASS_MIN_HEIGHT <= config.GRASS_MAX_HEIGHT
    assert config.GRASS_MIN_BEND <= config.GRASS_MAX_BEND
    assert config.GRASS_MIN_STIFFNESS <= config.GRASS_MAX_STIFFNESS
    assert config.WIND_SEED == 2718
    assert config.WIND_BASE_SPEED >= 0
    assert config.WIND_RESPONSE_SCALE >= 0
    assert 0.0 <= config.WIND_SLOW_PULSE_AMOUNT <= 1.0
    assert config.WIND_MAX_BEND_RATIO > 0
    assert config.WIND_TIME_WRAP_SECONDS > 0
    assert config.GUST_INTERVAL > 0
    assert config.GUST_DURATION > 0
    assert config.GUST_STRENGTH >= 0
    assert config.LIGHT_SEED == 4055
    assert config.LIGHT_PARTICLE_COUNT == 48
    assert 20 <= config.LIGHT_GROUND_SPARK_COUNT <= 40
    assert len(config.LIGHT_BEAM_ORIGIN) == 3
    assert len(config.LIGHT_BEAM_DIRECTION) == 3
    assert config.LIGHT_BEAM_LENGTH > 0
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
    assert config.LIGHT_PARTICLE_VISIBILITY_THRESHOLD >= 0
    assert config.LIGHT_GROUND_SPARK_THRESHOLD >= 0
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
    assert config.RAIN_WIND_DRIFT_SCALE >= 0
    assert config.RAIN_WIND_TILT_SCALE >= 0
    assert (
        0.0
        <= config.RAIN_LIGHT_VISIBILITY_THRESHOLD
        <= config.RAIN_BRIGHT_VISIBILITY_THRESHOLD
        <= 1.0
    )
    for name in dir(config):
        if name.startswith("PALETTE_"):
            value = getattr(config, name)
            if isinstance(value, int):
                assert 0 <= value <= 15
    assert set(config.PALETTE_PRESETS) == {"morning", "noon", "evening"}
    assert config.PALETTE_PRESET in config.PALETTE_PRESETS
