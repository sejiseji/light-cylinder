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
    assert config.AUTO_ROTATE_SPEED > 0
