REFERENCE_WIDTH = 393
REFERENCE_HEIGHT = 852

RENDER_WIDTH = 448
RENDER_HEIGHT = 852

COMPOSITION_SAFE_WIDTH = 393

SAFE_LEFT = (RENDER_WIDTH - COMPOSITION_SAFE_WIDTH) // 2
SAFE_RIGHT = SAFE_LEFT + COMPOSITION_SAFE_WIDTH

TARGET_FPS = 30

DISPLAY_TITLE_JA = "光の標本"
DISPLAY_TITLE_EN = "Specimen of Light"
PROJECT_TITLE = DISPLAY_TITLE_EN

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
CAMERA_INERTIA_DECAY = 0.68
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
MICRO_WIND_RATE = 0.19
MICRO_WIND_AMOUNT = 0.1
MICRO_WIND_PHASE_SCALE = 1.7
WIND_MAX_BEND_RATIO = 0.42
WIND_TIME_WRAP_SECONDS = 3600.0

GUST_INTERVAL = 12.0
GUST_DURATION = 5.5
GUST_STRENGTH = 0.36

LIGHT_SEED = 4055
LIGHT_PARTICLE_COUNT = 48
LIGHT_PARTICLE_MAX_COUNT = 80
LIGHT_GROUND_SPARK_COUNT = 28
LIGHT_BEAM_ORIGIN = (-34.0, 246.0, -22.0)
LIGHT_BEAM_DIRECTION = (0.22, -1.0, 0.18)
LIGHT_BEAM_LENGTH = 285.0
LIGHT_BEAM_RADIUS = 44.0
LIGHT_BEAM_CORE_RADIUS = 14.0
LIGHT_BEAM_END_FADE = 32.0
LIGHT_CLOUD_SHADOW_RATE = 0.075
LIGHT_CLOUD_SHADOW_AMOUNT = 0.16
LIGHT_CLOUD_SHADOW_FLOOR = 0.78
LIGHT_PARTICLE_SWAY_RATE = 0.23
LIGHT_PARTICLE_SWAY_AMOUNT = 0.12
LIGHT_PARTICLE_AXIS_ATTRACTION = 0.07
LIGHT_PARTICLE_WALK_RATE = 0.31
LIGHT_PARTICLE_WALK_AMOUNT = 2.8
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

RAIN_SEED = 9182
RAIN_DROP_COUNT = 64
RAIN_DEFAULT_INTENSITY = 0.45
RAIN_INTENSITY_STEP = 0.15
RAIN_MIN_FALL_SPEED = 96.0
RAIN_MAX_FALL_SPEED = 142.0
RAIN_MIN_LENGTH = 8.0
RAIN_MAX_LENGTH = 15.0
RAIN_WIND_DRIFT_SCALE = 34.0
RAIN_WIND_TILT_SCALE = 10.0
RAIN_LIGHT_VISIBILITY_THRESHOLD = 0.16
RAIN_BRIGHT_VISIBILITY_THRESHOLD = 0.52
RAIN_SPLASH_LIFETIME = 0.22
RAIN_SPLASH_GRAVITY = 92.0
RAIN_SPLASH_SPEED = 16.0
RAIN_SPLASHES_PER_IMPACT = 2
RAIN_GROUND_WETNESS_GAIN = 0.004
RAIN_GROUND_DRY_RATE = 0.035
RAIN_GRASS_IMPACT_RADIUS = 12.0
RAIN_GRASS_IMPACT_DECAY_RATE = 4.2
RAIN_GRASS_REACTION_BEND_SCALE = 4.8

MENU_STAGE_MIN = 1
MENU_STAGE_MAX = 3
MENU_PHOTON_COUNTS = (LIGHT_PARTICLE_COUNT, 64, LIGHT_PARTICLE_MAX_COUNT)
MENU_GRASS_COUNTS = (GRASS_COUNT, 520, 620)
MENU_WIND_MULTIPLIERS = (1.0, 1.35, 1.7)
MENU_RAIN_INTENSITIES = (RAIN_DEFAULT_INTENSITY, 0.65, 0.85)
MENU_AUTO_ROTATE_MULTIPLIERS = (1.0, 1.45, 1.9)

AFTER_RAIN_MIN_WETNESS = 0.05
AFTER_RAIN_CLEAR_WETNESS = 0.035
AFTER_RAIN_MIN_DURATION = 7.0
AFTER_RAIN_CLOUD_RECOVERY_RATE = 0.055
AFTER_RAIN_LIGHT_SHADOW_AMOUNT = 0.1
AFTER_RAIN_REFLECTION_DECAY_RATE = 0.045
AFTER_RAIN_DRY_RATE_MIN = 0.38
AFTER_RAIN_DRY_RATE_MAX = 1.25
TIP_DROPLET_MAX_COUNT = 28
TIP_DROPLET_LIGHT_THRESHOLD = 0.24
TIP_DROPLET_HOLD_MIN = 18.0
TIP_DROPLET_HOLD_MAX = 32.0
TIP_DROPLET_FALL_SPEED = 8.0
TIP_DROPLET_SEED = 6149

PALETTE_PRESET = "morning"
PALETTE_PRESETS = {
    "morning": {
        "background": 1,
        "background_band": 2,
        "distant_grass": 3,
        "normal_grass": 11,
        "foreground_grass": 10,
        "lit_grass": 10,
        "strongly_lit_grass": 7,
        "ground_shadow": 5,
        "ground_light": 13,
        "ground_strong_light": 10,
        "dim_particle": 6,
        "bright_particle": 7,
        "cylinder_far_edge": 5,
        "cylinder_near_edge": 13,
        "cylinder_vertical": 5,
        "debug_accent": 12,
        "debug_text": 6,
        "debug_frame": 5,
        "safe_area": 11,
        "axis_x": 8,
        "axis_y": 11,
        "axis_z": 12,
    },
    "noon": {
        "background": 1,
        "background_band": 5,
        "distant_grass": 3,
        "normal_grass": 11,
        "foreground_grass": 10,
        "lit_grass": 7,
        "strongly_lit_grass": 7,
        "ground_shadow": 5,
        "ground_light": 10,
        "ground_strong_light": 7,
        "dim_particle": 6,
        "bright_particle": 7,
        "cylinder_far_edge": 5,
        "cylinder_near_edge": 6,
        "cylinder_vertical": 5,
        "debug_accent": 12,
        "debug_text": 6,
        "debug_frame": 5,
        "safe_area": 11,
        "axis_x": 8,
        "axis_y": 11,
        "axis_z": 12,
    },
    "evening": {
        "background": 1,
        "background_band": 2,
        "distant_grass": 3,
        "normal_grass": 3,
        "foreground_grass": 11,
        "lit_grass": 10,
        "strongly_lit_grass": 9,
        "ground_shadow": 5,
        "ground_light": 4,
        "ground_strong_light": 10,
        "dim_particle": 13,
        "bright_particle": 10,
        "cylinder_far_edge": 5,
        "cylinder_near_edge": 4,
        "cylinder_vertical": 5,
        "debug_accent": 12,
        "debug_text": 6,
        "debug_frame": 5,
        "safe_area": 11,
        "axis_x": 8,
        "axis_y": 11,
        "axis_z": 12,
    },
}
ACTIVE_PALETTE = PALETTE_PRESETS[PALETTE_PRESET]

PALETTE_BACKGROUND = ACTIVE_PALETTE["background"]
PALETTE_BACKGROUND_BAND = ACTIVE_PALETTE["background_band"]
PALETTE_DISTANT_GRASS = ACTIVE_PALETTE["distant_grass"]
PALETTE_NORMAL_GRASS = ACTIVE_PALETTE["normal_grass"]
PALETTE_FOREGROUND_GRASS = ACTIVE_PALETTE["foreground_grass"]
PALETTE_LIT_GRASS = ACTIVE_PALETTE["lit_grass"]
PALETTE_STRONGLY_LIT_GRASS = ACTIVE_PALETTE["strongly_lit_grass"]
PALETTE_GROUND_SHADOW = ACTIVE_PALETTE["ground_shadow"]
PALETTE_GROUND_LIGHT = ACTIVE_PALETTE["ground_light"]
PALETTE_GROUND_STRONG_LIGHT = ACTIVE_PALETTE["ground_strong_light"]
PALETTE_DIM_PARTICLE = ACTIVE_PALETTE["dim_particle"]
PALETTE_BRIGHT_PARTICLE = ACTIVE_PALETTE["bright_particle"]
PALETTE_CYLINDER_FAR_EDGE = ACTIVE_PALETTE["cylinder_far_edge"]
PALETTE_CYLINDER_NEAR_EDGE = ACTIVE_PALETTE["cylinder_near_edge"]
PALETTE_CYLINDER_VERTICAL = ACTIVE_PALETTE["cylinder_vertical"]
PALETTE_DEBUG_ACCENT = ACTIVE_PALETTE["debug_accent"]
PALETTE_DEBUG_TEXT = ACTIVE_PALETTE["debug_text"]
PALETTE_DEBUG_FRAME = ACTIVE_PALETTE["debug_frame"]
PALETTE_SAFE_AREA = ACTIVE_PALETTE["safe_area"]
PALETTE_AXIS_X = ACTIVE_PALETTE["axis_x"]
PALETTE_AXIS_Y = ACTIVE_PALETTE["axis_y"]
PALETTE_AXIS_Z = ACTIVE_PALETTE["axis_z"]


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
    if not 0.0 <= LIGHT_CLOUD_SHADOW_AMOUNT <= 1.0:
        raise ValueError("light cloud shadow amount must be normalized")
    if not 0.0 <= LIGHT_CLOUD_SHADOW_FLOOR <= 1.0:
        raise ValueError("light cloud shadow floor must be normalized")
    if LIGHT_CLOUD_SHADOW_RATE < 0:
        raise ValueError("light cloud shadow rate must be non-negative")
    if LIGHT_PARTICLE_SWAY_RATE < 0 or LIGHT_PARTICLE_SWAY_AMOUNT < 0:
        raise ValueError("light particle sway must be non-negative")
    if LIGHT_PARTICLE_DRIFT_MIN > LIGHT_PARTICLE_DRIFT_MAX:
        raise ValueError("light particle drift range must be ordered")
    if LIGHT_PARTICLE_AXIS_ATTRACTION < 0:
        raise ValueError("light particle axis attraction must be non-negative")
    if LIGHT_PARTICLE_WALK_RATE < 0 or LIGHT_PARTICLE_WALK_AMOUNT < 0:
        raise ValueError("light particle random walk must be non-negative")
    if LIGHT_PARTICLE_VISIBILITY_THRESHOLD < 0 or LIGHT_GROUND_SPARK_THRESHOLD < 0:
        raise ValueError("light visibility thresholds must be non-negative")
    if LIGHT_PARTICLE_COUNT <= 0 or LIGHT_PARTICLE_MAX_COUNT < LIGHT_PARTICLE_COUNT:
        raise ValueError("light particle counts must be positive and ordered")
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
    if RAIN_DROP_COUNT <= 0:
        raise ValueError("rain drop count must be positive")
    if not 0.0 <= RAIN_DEFAULT_INTENSITY <= 1.0:
        raise ValueError("rain default intensity must be normalized")
    if not 0.0 < RAIN_INTENSITY_STEP <= 1.0:
        raise ValueError("rain intensity step must be normalized")
    if RAIN_MIN_FALL_SPEED <= 0 or RAIN_MAX_FALL_SPEED < RAIN_MIN_FALL_SPEED:
        raise ValueError("rain fall speed range must be positive and ordered")
    if RAIN_MIN_LENGTH <= 0 or RAIN_MAX_LENGTH < RAIN_MIN_LENGTH:
        raise ValueError("rain length range must be positive and ordered")
    if RAIN_WIND_DRIFT_SCALE < 0 or RAIN_WIND_TILT_SCALE < 0:
        raise ValueError("rain wind scales must be non-negative")
    if not (0.0 <= RAIN_LIGHT_VISIBILITY_THRESHOLD <= RAIN_BRIGHT_VISIBILITY_THRESHOLD <= 1.0):
        raise ValueError("rain light thresholds must be ordered")
    if RAIN_SPLASH_LIFETIME <= 0 or RAIN_SPLASH_GRAVITY < 0 or RAIN_SPLASH_SPEED < 0:
        raise ValueError("rain splash timing and motion must be positive")
    if RAIN_SPLASHES_PER_IMPACT < 0:
        raise ValueError("rain splash count must be non-negative")
    if not 0.0 <= RAIN_GROUND_WETNESS_GAIN <= 1.0:
        raise ValueError("rain wetness gain must be normalized")
    if RAIN_GROUND_DRY_RATE < 0:
        raise ValueError("rain dry rate must be non-negative")
    if RAIN_GRASS_IMPACT_RADIUS <= 0:
        raise ValueError("rain grass impact radius must be positive")
    if RAIN_GRASS_IMPACT_DECAY_RATE < 0 or RAIN_GRASS_REACTION_BEND_SCALE < 0:
        raise ValueError("rain grass reaction values must be non-negative")
    _validate_menu_stages()
    if not 0.0 <= AFTER_RAIN_CLEAR_WETNESS <= AFTER_RAIN_MIN_WETNESS <= 1.0:
        raise ValueError("after-rain wetness thresholds must be ordered")
    if AFTER_RAIN_MIN_DURATION < 0:
        raise ValueError("after-rain minimum duration must be non-negative")
    if not 0.0 <= AFTER_RAIN_LIGHT_SHADOW_AMOUNT <= 1.0:
        raise ValueError("after-rain light shadow amount must be normalized")
    if AFTER_RAIN_CLOUD_RECOVERY_RATE < 0 or AFTER_RAIN_REFLECTION_DECAY_RATE < 0:
        raise ValueError("after-rain recovery rates must be non-negative")
    if not 0.0 <= AFTER_RAIN_DRY_RATE_MIN <= AFTER_RAIN_DRY_RATE_MAX:
        raise ValueError("after-rain dry rate range must be ordered")
    if TIP_DROPLET_MAX_COUNT < 0:
        raise ValueError("tip droplet count must be non-negative")
    if not 0.0 <= TIP_DROPLET_LIGHT_THRESHOLD <= 1.0:
        raise ValueError("tip droplet light threshold must be normalized")
    if TIP_DROPLET_HOLD_MIN < 0 or TIP_DROPLET_HOLD_MAX < TIP_DROPLET_HOLD_MIN:
        raise ValueError("tip droplet hold range must be ordered")
    if TIP_DROPLET_FALL_SPEED < 0:
        raise ValueError("tip droplet fall speed must be non-negative")
    if not 0.0 <= CAMERA_INERTIA_DECAY < 1.0:
        raise ValueError("camera inertia decay must be normalized below one")
    if PALETTE_PRESET not in PALETTE_PRESETS:
        raise ValueError("active palette preset must exist")
    if set(PALETTE_PRESETS) != {"morning", "noon", "evening"}:
        raise ValueError("palette presets must include morning, noon, and evening")
    for preset in PALETTE_PRESETS.values():
        for color in preset.values():
            if not 0 <= color <= 15:
                raise ValueError("palette color values must use the Pyxel palette")


def _validate_menu_stages() -> None:
    if MENU_STAGE_MIN != 1 or MENU_STAGE_MAX != 3:
        raise ValueError("menu stages must be the 1..3 range")
    stage_sets = (
        MENU_PHOTON_COUNTS,
        MENU_GRASS_COUNTS,
        MENU_WIND_MULTIPLIERS,
        MENU_RAIN_INTENSITIES,
        MENU_AUTO_ROTATE_MULTIPLIERS,
    )
    if any(len(values) != MENU_STAGE_MAX for values in stage_sets):
        raise ValueError("menu stage value sets must have three entries")
    if MENU_PHOTON_COUNTS[0] != LIGHT_PARTICLE_COUNT:
        raise ValueError("menu photon stage 1 must match the current particle count")
    if MENU_GRASS_COUNTS[0] != GRASS_COUNT:
        raise ValueError("menu grass stage 1 must match the current grass count")
    if MENU_RAIN_INTENSITIES[0] != RAIN_DEFAULT_INTENSITY:
        raise ValueError("menu rain stage 1 must match the current rain intensity")
    if any(value <= 0 for value in MENU_PHOTON_COUNTS + MENU_GRASS_COUNTS):
        raise ValueError("menu density stage values must be positive")
    if any(value <= 0.0 for value in MENU_WIND_MULTIPLIERS + MENU_AUTO_ROTATE_MULTIPLIERS):
        raise ValueError("menu motion multipliers must be positive")
    if any(not 0.0 <= value <= 1.0 for value in MENU_RAIN_INTENSITIES):
        raise ValueError("menu rain intensities must be normalized")
    for values in stage_sets:
        if tuple(sorted(values)) != values:
            raise ValueError("menu stage values must be ordered")
