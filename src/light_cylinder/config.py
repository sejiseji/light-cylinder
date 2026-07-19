REFERENCE_WIDTH = 393
REFERENCE_HEIGHT = 852

RENDER_WIDTH = 448
RENDER_HEIGHT = 852

COMPOSITION_SAFE_WIDTH = 393

SAFE_LEFT = (RENDER_WIDTH - COMPOSITION_SAFE_WIDTH) // 2
SAFE_RIGHT = SAFE_LEFT + COMPOSITION_SAFE_WIDTH

TARGET_FPS = 30

PROJECT_TITLE = "Light Cylinder"

CAMERA_INITIAL_YAW = -0.22
CAMERA_INITIAL_PITCH = 0.34
CAMERA_INITIAL_DISTANCE = 430.0
CAMERA_MIN_DISTANCE = 180.0
CAMERA_MAX_DISTANCE = 900.0
CAMERA_MIN_PITCH = -1.3962634015954636
CAMERA_MAX_PITCH = 1.3962634015954636
CAMERA_FOCAL_LENGTH = 300.0
CAMERA_YAW_SPEED = 0.035
CAMERA_PITCH_SPEED = 0.025
CAMERA_ZOOM_SPEED = 12.0
MOUSE_YAW_SPEED = 0.006
MOUSE_PITCH_SPEED = 0.005
MOUSE_WHEEL_ZOOM_SPEED = 24.0
AUTO_ROTATE_SPEED = 0.0035

CYLINDER_RADIUS = 96.0
CYLINDER_HEIGHT = 240.0
CYLINDER_RADIAL_SEGMENTS = 32
CYLINDER_VERTICAL_GUIDES = 8
CYLINDER_TARGET_HEIGHT_FACTOR = 0.43

GRASS_SEED = 1729
GRASS_COUNT = 420
GRASS_SEGMENTS = 5
GRASS_MIN_HEIGHT = 18.0
GRASS_MAX_HEIGHT = 46.0
GRASS_MIN_BEND = 2.0
GRASS_MAX_BEND = 15.0
GRASS_MIN_STIFFNESS = 0.45
GRASS_MAX_STIFFNESS = 1.0

WIND_SEED = 2718
WIND_BASE_DIRECTION_ANGLE = 0.35
WIND_BASE_SPEED = 0.55
WIND_RESPONSE_SCALE = 13.0
WIND_SLOW_PULSE_RATE = 0.42
WIND_SLOW_PULSE_AMOUNT = 0.22
WIND_SPATIAL_FREQUENCY_X = 0.018
WIND_SPATIAL_FREQUENCY_Z = 0.026
WIND_BLADE_PHASE_SCALE = 0.65
WIND_DIRECTION_SWAY_AMOUNT = 0.16
WIND_DIRECTION_SWAY_RATE = 0.37
WIND_MAX_BEND_RATIO = 0.42
WIND_TIME_WRAP_SECONDS = 3600.0

GUST_INTERVAL = 12.0
GUST_DURATION = 5.5
GUST_STRENGTH = 0.36

LIGHT_SEED = 4055
LIGHT_PARTICLE_COUNT = 48
LIGHT_GROUND_SPARK_COUNT = 28
LIGHT_BEAM_ORIGIN = (-34.0, 246.0, -22.0)
LIGHT_BEAM_DIRECTION = (0.22, -1.0, 0.18)
LIGHT_BEAM_LENGTH = 285.0
LIGHT_BEAM_RADIUS = 44.0
LIGHT_BEAM_CORE_RADIUS = 14.0
LIGHT_BEAM_END_FADE = 32.0
LIGHT_PULSE_RATE = 0.11
LIGHT_PULSE_AMOUNT = 0.13
LIGHT_PARTICLE_SWAY_RATE = 0.23
LIGHT_PARTICLE_SWAY_AMOUNT = 0.12
LIGHT_PARTICLE_DRIFT_MIN = -2.6
LIGHT_PARTICLE_DRIFT_MAX = 4.8
LIGHT_PARTICLE_VISIBILITY_THRESHOLD = 0.28
LIGHT_GROUND_SPARK_THRESHOLD = 0.38
LIGHT_GRASS_THRESHOLD_LOW = 0.14
LIGHT_GRASS_THRESHOLD_MEDIUM = 0.34
LIGHT_GRASS_THRESHOLD_HIGH = 0.58
LIGHT_FLOOR_THRESHOLD_LOW = 0.18
LIGHT_FLOOR_THRESHOLD_MEDIUM = 0.4
LIGHT_FLOOR_THRESHOLD_HIGH = 0.78

PALETTE_BACKGROUND = 1
PALETTE_BACKGROUND_BAND = 2
PALETTE_DISTANT_GRASS = 3
PALETTE_NORMAL_GRASS = 11
PALETTE_FOREGROUND_GRASS = 10
PALETTE_LIT_GRASS = 10
PALETTE_STRONGLY_LIT_GRASS = 7
PALETTE_GROUND_SHADOW = 5
PALETTE_GROUND_LIGHT = 13
PALETTE_GROUND_STRONG_LIGHT = 10
PALETTE_DIM_PARTICLE = 6
PALETTE_BRIGHT_PARTICLE = 7
PALETTE_CYLINDER_FAR_EDGE = 5
PALETTE_CYLINDER_NEAR_EDGE = 13
PALETTE_CYLINDER_VERTICAL = 5
PALETTE_DEBUG_ACCENT = 12
PALETTE_DEBUG_TEXT = 6
PALETTE_DEBUG_FRAME = 5
PALETTE_SAFE_AREA = 11
PALETTE_AXIS_X = 8
PALETTE_AXIS_Y = 11
PALETTE_AXIS_Z = 12


def validate_display_config() -> None:
    if RENDER_WIDTH < COMPOSITION_SAFE_WIDTH:
        raise ValueError("render width must contain the composition safe width")
    if SAFE_LEFT < 0:
        raise ValueError("safe area must start inside the render area")
    if SAFE_RIGHT > RENDER_WIDTH:
        raise ValueError("safe area must end inside the render area")
    if SAFE_RIGHT - SAFE_LEFT != COMPOSITION_SAFE_WIDTH:
        raise ValueError("safe area width must match the configured safe width")
    if RENDER_HEIGHT != REFERENCE_HEIGHT:
        raise ValueError("render height must match the reference height")
    if TARGET_FPS <= 0:
        raise ValueError("target FPS must be positive")
    if CAMERA_MIN_DISTANCE <= 0:
        raise ValueError("minimum camera distance must be positive")
    if CAMERA_INITIAL_DISTANCE < CAMERA_MIN_DISTANCE:
        raise ValueError("initial camera distance must be at least the minimum")
    if CAMERA_INITIAL_DISTANCE > CAMERA_MAX_DISTANCE:
        raise ValueError("initial camera distance must be at most the maximum")
    if CAMERA_MIN_PITCH >= CAMERA_MAX_PITCH:
        raise ValueError("minimum camera pitch must be lower than maximum pitch")
    if CYLINDER_RADIUS <= 0:
        raise ValueError("cylinder radius must be positive")
    if CYLINDER_HEIGHT <= 0:
        raise ValueError("cylinder height must be positive")
    if CYLINDER_RADIAL_SEGMENTS < 3:
        raise ValueError("cylinder radial segments must be at least 3")
    if CYLINDER_VERTICAL_GUIDES < 1:
        raise ValueError("cylinder vertical guides must be positive")
    if not 0.0 <= CYLINDER_TARGET_HEIGHT_FACTOR <= 1.0:
        raise ValueError("cylinder target height factor must be normalized")
    if GRASS_COUNT <= 0:
        raise ValueError("grass count must be positive")
    if GRASS_SEGMENTS < 1:
        raise ValueError("grass segments must be positive")
    if GRASS_MIN_HEIGHT <= 0 or GRASS_MAX_HEIGHT < GRASS_MIN_HEIGHT:
        raise ValueError("grass height range must be positive and ordered")
    if GRASS_MIN_BEND < 0 or GRASS_MAX_BEND < GRASS_MIN_BEND:
        raise ValueError("grass bend range must be non-negative and ordered")
    if GRASS_MIN_STIFFNESS <= 0 or GRASS_MAX_STIFFNESS < GRASS_MIN_STIFFNESS:
        raise ValueError("grass stiffness range must be positive and ordered")
    if WIND_BASE_SPEED < 0:
        raise ValueError("wind base speed must be non-negative")
    if WIND_RESPONSE_SCALE < 0:
        raise ValueError("wind response scale must be non-negative")
    if not 0.0 <= WIND_SLOW_PULSE_AMOUNT <= 1.0:
        raise ValueError("wind slow pulse amount must be normalized")
    if WIND_MAX_BEND_RATIO <= 0:
        raise ValueError("wind max bend ratio must be positive")
    if WIND_TIME_WRAP_SECONDS <= 0:
        raise ValueError("wind time wrap must be positive")
    if GUST_INTERVAL <= 0 or GUST_DURATION <= 0 or GUST_STRENGTH < 0:
        raise ValueError("gust timing and strength must be positive")
    if LIGHT_PARTICLE_COUNT <= 0:
        raise ValueError("light particle count must be positive")
    if LIGHT_GROUND_SPARK_COUNT < 0:
        raise ValueError("light ground spark count must be non-negative")
    if LIGHT_BEAM_LENGTH <= 0:
        raise ValueError("light beam length must be positive")
    if LIGHT_BEAM_RADIUS <= 0:
        raise ValueError("light beam radius must be positive")
    if not 0 <= LIGHT_BEAM_CORE_RADIUS < LIGHT_BEAM_RADIUS:
        raise ValueError("light beam core radius must be smaller than radius")
    if LIGHT_BEAM_END_FADE <= 0:
        raise ValueError("light beam end fade must be positive")
    if not 0.0 <= LIGHT_PULSE_AMOUNT <= 1.0:
        raise ValueError("light pulse amount must be normalized")
    if LIGHT_PULSE_RATE < 0:
        raise ValueError("light pulse rate must be non-negative")
    if LIGHT_PARTICLE_SWAY_RATE < 0 or LIGHT_PARTICLE_SWAY_AMOUNT < 0:
        raise ValueError("light particle sway must be non-negative")
    if LIGHT_PARTICLE_DRIFT_MIN > LIGHT_PARTICLE_DRIFT_MAX:
        raise ValueError("light particle drift range must be ordered")
    if LIGHT_PARTICLE_VISIBILITY_THRESHOLD < 0 or LIGHT_GROUND_SPARK_THRESHOLD < 0:
        raise ValueError("light visibility thresholds must be non-negative")
    if not (
        0.0
        <= LIGHT_GRASS_THRESHOLD_LOW
        <= LIGHT_GRASS_THRESHOLD_MEDIUM
        <= LIGHT_GRASS_THRESHOLD_HIGH
    ):
        raise ValueError("light grass thresholds must be ordered")
    if not (
        0.0
        <= LIGHT_FLOOR_THRESHOLD_LOW
        <= LIGHT_FLOOR_THRESHOLD_MEDIUM
        <= LIGHT_FLOOR_THRESHOLD_HIGH
    ):
        raise ValueError("light floor thresholds must be ordered")
