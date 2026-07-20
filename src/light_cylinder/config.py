REFERENCE_WIDTH = 393
REFERENCE_HEIGHT = 852

RENDER_WIDTH = 448
RENDER_HEIGHT = 852

COMPOSITION_SAFE_WIDTH = 393

SAFE_LEFT = (RENDER_WIDTH - COMPOSITION_SAFE_WIDTH) // 2
SAFE_RIGHT = SAFE_LEFT + COMPOSITION_SAFE_WIDTH

TARGET_FPS = 30
UI_TEXT_SCALE = 3

ATMOSPHERIC_DITHER_STEP = 4
ATMOSPHERIC_DITHER_BASE_DENSITY = 0.1
ATMOSPHERIC_DITHER_LIGHT_BOOST = 0.035
ATMOSPHERIC_DITHER_SHADOW_REDUCTION = 0.25
ATMOSPHERIC_DITHER_PHASE_RATE = 0.25
ATMOSPHERIC_DITHER_HASH_MODULUS = 64

DISPLAY_TITLE_JA = "光の標本"
DISPLAY_TITLE_EN = "Specimen of Light"
PROJECT_TITLE = DISPLAY_TITLE_EN

CAMERA_INITIAL_YAW = -0.22
CAMERA_INITIAL_PITCH = 0.34
CAMERA_INITIAL_DISTANCE = 455.0
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
AUTO_ROTATE_PITCH_SWAY_AMOUNT = 0.07
AUTO_ROTATE_PITCH_SWAY_RATE = 0.48
AUTO_ROTATE_PITCH_FOLLOW = 0.08

CYLINDER_RADIUS = 96.0
CYLINDER_HEIGHT = 300.0
CYLINDER_RADIAL_SEGMENTS = 32
CYLINDER_VERTICAL_GUIDES = 8
CYLINDER_TARGET_HEIGHT_FACTOR = 0.43

GRASS_SEED = 1729
GRASS_COUNT = 300
GRASS_SEGMENTS = 5
GRASS_MIN_HEIGHT = 18.0
GRASS_MAX_HEIGHT = 46.0
GRASS_MIN_BEND = 2.0
GRASS_MAX_BEND = 15.0
GRASS_MIN_STIFFNESS = 0.45
GRASS_MAX_STIFFNESS = 1.0
GRASS_WIDTH_MULTIPLIER = 2

WIND_SEED = 2718
WIND_BASE_DIRECTION_ANGLE = 0.35
WIND_BASE_SPEED = 0.65
WIND_RESPONSE_SCALE = 17.0
WIND_SLOW_PULSE_RATE = 0.42
WIND_SLOW_PULSE_AMOUNT = 0.38
WIND_SPATIAL_FREQUENCY_X = 0.018
WIND_SPATIAL_FREQUENCY_Z = 0.026
WIND_BLADE_PHASE_SCALE = 0.65
WIND_DIRECTION_SWAY_AMOUNT = 0.28
WIND_DIRECTION_SWAY_RATE = 0.37
MICRO_WIND_RATE = 0.19
MICRO_WIND_AMOUNT = 0.16
MICRO_WIND_PHASE_SCALE = 1.7
WIND_MAX_BEND_RATIO = 0.68
WIND_TIME_WRAP_SECONDS = 3600.0

GUST_INTERVAL = 12.0
GUST_DURATION = 5.5
GUST_STRENGTH = 0.5

LIGHT_SEED = 4055
LIGHT_PARTICLE_COUNT = 360
LIGHT_PARTICLE_MAX_COUNT = 1080
LIGHT_GROUND_SPARK_COUNT = 28
LIGHT_BEAM_ORIGIN = (-34.0, 312.0, -22.0)
LIGHT_BEAM_DIRECTION = (0.22, -1.0, 0.18)
LIGHT_BEAM_LENGTH = 360.0
LIGHT_BEAM_RADIUS = 44.0
LIGHT_BEAM_CORE_RADIUS = 14.0
LIGHT_BEAM_END_FADE = 40.0
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
LIGHT_PARTICLE_SIZE_MIN = 0.18
LIGHT_PARTICLE_SIZE_MAX = 1.0
LIGHT_PARTICLE_VISIBILITY_THRESHOLD = 0.28
LIGHT_BAND_COUNT = 5
LIGHT_BAND_WIDTH_MIN = 3.0
LIGHT_BAND_WIDTH_MAX = 12.0
LIGHT_BAND_WIDTH_FACTORS = (0.35, 0.52, 0.7, 0.92, 1.18)
LIGHT_BAND_WIDTH_RATE = 0.33
LIGHT_BAND_ALPHA_PATTERN = 1
LIGHT_ACCENT_BAND_COUNT = 3
LIGHT_ACCENT_BAND_WIDTHS = (0.55, 1.8, 0.8)
LIGHT_ACCENT_BAND_RATE = 0.58
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
RAIN_SHORT_LENGTHS = (7.0, 10.0, 13.0)
RAIN_MIN_LENGTH = RAIN_SHORT_LENGTHS[0]
RAIN_MAX_LENGTH = RAIN_SHORT_LENGTHS[-1]
RAIN_STATIC_STREAK_COUNT = 48
RAIN_STATIC_STREAK_MIN_LENGTH = 126.0
RAIN_STATIC_STREAK_MAX_LENGTH = 258.0
RAIN_STATIC_STREAK_MIN_HEIGHT_FACTOR = 0.24
RAIN_STATIC_STREAK_MAX_HEIGHT_FACTOR = 0.99
RAIN_STATIC_STREAK_FLASH_RATE = 1.15
RAIN_STATIC_STREAK_FLASH_THRESHOLD = 0.998
RAIN_WIND_DRIFT_SCALE = 0.0
RAIN_WIND_TILT_SCALE = 0.0
RAIN_BRIGHT_VISIBILITY_THRESHOLD = 0.94
RAIN_DEPTH_COLORS = (5, 12, 6, 7)
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
MENU_PHOTON_COUNTS = (LIGHT_PARTICLE_COUNT, 720, LIGHT_PARTICLE_MAX_COUNT)
MENU_GRASS_COUNTS = (GRASS_COUNT, 375, 450)
MENU_WIND_MULTIPLIERS = (1.0, 1.85, 2.7)
MENU_WIND_SPEED_MULTIPLIERS = (1.0, 1.45, 2.0)
MENU_RAIN_INTENSITIES = (RAIN_DEFAULT_INTENSITY, 0.65, 0.85)
MENU_AUTO_ROTATE_MULTIPLIERS = (1.0, 1.45, 1.9)

OBSERVATION_CYCLE_CLEAR_DURATION = 8.0
OBSERVATION_CYCLE_SHADOW_DURATION = 10.0
OBSERVATION_CYCLE_LIGHT_RAIN_DURATION = 12.0
OBSERVATION_CYCLE_RAIN_DURATION = 18.0
OBSERVATION_CYCLE_AFTER_RAIN_DURATION = 24.0
OBSERVATION_CYCLE_CLOUD_SHADOW_AMOUNT = 0.18
OBSERVATION_CYCLE_LIGHT_RAIN_MULTIPLIER = 0.45

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

FIREFLY_SEED = 7341
FIREFLY_MAX_COUNT = 9
FIREFLY_TARGET_MIN_HEIGHT_FACTOR = 0.12
FIREFLY_TARGET_MAX_HEIGHT_FACTOR = 0.58
FIREFLY_TARGET_REACH_RADIUS = 14.0
FIREFLY_TARGET_MIN_DISTANCE = 54.0
FIREFLY_LIFETIME_MIN = 14.0
FIREFLY_LIFETIME_MAX = 30.0
FIREFLY_SPAWN_DELAY_MIN = 2.0
FIREFLY_SPAWN_DELAY_MAX = 5.0
FIREFLY_CLEAR_SPAWN_MULTIPLIER = 1.0
FIREFLY_AFTER_RAIN_SPAWN_MULTIPLIER = 0.36
FIREFLY_RAIN_SPAWN_MULTIPLIER = 0.12
FIREFLY_STRONG_RAIN_THRESHOLD = 0.7
FIREFLY_MAX_SPEED = 30.0
FIREFLY_TARGET_ACCELERATION = 18.0
FIREFLY_WANDER_ACCELERATION = 3.0
FIREFLY_BOUNDARY_MARGIN = 18.0
FIREFLY_BOUNDARY_ACCELERATION = 8.0
FIREFLY_WIND_INFLUENCE = 0.08
FIREFLY_VELOCITY_DAMPING = 0.97
FIREFLY_GLOW_SPEED_MIN = 0.65
FIREFLY_GLOW_SPEED_MAX = 1.25
FIREFLY_VISIBLE_THRESHOLD = 0.35
FIREFLY_BRIGHT_THRESHOLD = 0.7
FIREFLY_RING_THRESHOLD = 0.9

MENU_FIREFLY_COUNTS = (3, 6, FIREFLY_MAX_COUNT)

PALETTE_PRESET = "morning"
PALETTE_PRESETS = {
    "morning": {
        "background": 1,
        "background_band": 2,
        "distant_grass": 3,
        "normal_grass": 11,
        "foreground_grass": 3,
        "lit_grass": 3,
        "strongly_lit_grass": 11,
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
        "foreground_grass": 3,
        "lit_grass": 3,
        "strongly_lit_grass": 11,
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
        "foreground_grass": 3,
        "lit_grass": 3,
        "strongly_lit_grass": 11,
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
    if UI_TEXT_SCALE < 1:
        raise ValueError("UI text scale must be positive")
    if ATMOSPHERIC_DITHER_STEP < 1:
        raise ValueError("atmospheric dither step must be positive")
    if not 0.0 <= ATMOSPHERIC_DITHER_BASE_DENSITY <= 1.0:
        raise ValueError("atmospheric dither density must be normalized")
    if not 0.0 <= ATMOSPHERIC_DITHER_LIGHT_BOOST <= 1.0:
        raise ValueError("atmospheric dither light boost must be normalized")
    if not 0.0 <= ATMOSPHERIC_DITHER_SHADOW_REDUCTION <= 1.0:
        raise ValueError("atmospheric dither shadow reduction must be normalized")
    if ATMOSPHERIC_DITHER_PHASE_RATE < 0:
        raise ValueError("atmospheric dither phase rate must be non-negative")
    if ATMOSPHERIC_DITHER_HASH_MODULUS <= 0:
        raise ValueError("atmospheric dither hash modulus must be positive")
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
    if GRASS_WIDTH_MULTIPLIER < 1:
        raise ValueError("grass width multiplier must be positive")
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
    if LIGHT_PARTICLE_SIZE_MIN <= 0 or LIGHT_PARTICLE_SIZE_MAX < LIGHT_PARTICLE_SIZE_MIN:
        raise ValueError("light particle size range must be positive and ordered")
    if LIGHT_PARTICLE_AXIS_ATTRACTION < 0:
        raise ValueError("light particle axis attraction must be non-negative")
    if LIGHT_PARTICLE_WALK_RATE < 0 or LIGHT_PARTICLE_WALK_AMOUNT < 0:
        raise ValueError("light particle random walk must be non-negative")
    if LIGHT_PARTICLE_VISIBILITY_THRESHOLD < 0 or LIGHT_GROUND_SPARK_THRESHOLD < 0:
        raise ValueError("light visibility thresholds must be non-negative")
    if LIGHT_PARTICLE_COUNT <= 0 or LIGHT_PARTICLE_MAX_COUNT < LIGHT_PARTICLE_COUNT:
        raise ValueError("light particle counts must be positive and ordered")
    if not 1 <= LIGHT_BAND_COUNT <= 5:
        raise ValueError("light band count must be between one and five")
    if LIGHT_BAND_WIDTH_MIN <= 0 or LIGHT_BAND_WIDTH_MAX < LIGHT_BAND_WIDTH_MIN:
        raise ValueError("light band width range must be positive and ordered")
    if len(LIGHT_BAND_WIDTH_FACTORS) != LIGHT_BAND_COUNT:
        raise ValueError("light band width factors must match the band count")
    if any(factor <= 0 for factor in LIGHT_BAND_WIDTH_FACTORS):
        raise ValueError("light band width factors must be positive")
    if LIGHT_BAND_WIDTH_RATE < 0:
        raise ValueError("light band width rate must be non-negative")
    if LIGHT_BAND_ALPHA_PATTERN < 0:
        raise ValueError("light band alpha pattern must be non-negative")
    if len(LIGHT_ACCENT_BAND_WIDTHS) != LIGHT_ACCENT_BAND_COUNT:
        raise ValueError("light accent band widths must match the accent count")
    if LIGHT_ACCENT_BAND_COUNT <= 0:
        raise ValueError("light accent band count must be positive")
    if any(width <= 0.0 for width in LIGHT_ACCENT_BAND_WIDTHS):
        raise ValueError("light accent band widths must be positive")
    if LIGHT_ACCENT_BAND_RATE < 0:
        raise ValueError("light accent band rate must be non-negative")
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
    if len(RAIN_SHORT_LENGTHS) != 3:
        raise ValueError("rain short lengths must define three fixed sizes")
    if tuple(sorted(RAIN_SHORT_LENGTHS)) != RAIN_SHORT_LENGTHS:
        raise ValueError("rain short lengths must be ordered")
    if RAIN_MIN_LENGTH <= 0 or RAIN_MAX_LENGTH < RAIN_MIN_LENGTH:
        raise ValueError("rain length range must be positive and ordered")
    if RAIN_SHORT_LENGTHS[0] != RAIN_MIN_LENGTH or RAIN_SHORT_LENGTHS[-1] != RAIN_MAX_LENGTH:
        raise ValueError("rain min and max lengths must match the fixed short lengths")
    if RAIN_STATIC_STREAK_COUNT < 0:
        raise ValueError("rain static streak count must be non-negative")
    if (
        RAIN_STATIC_STREAK_MIN_LENGTH <= RAIN_MAX_LENGTH
        or RAIN_STATIC_STREAK_MAX_LENGTH < RAIN_STATIC_STREAK_MIN_LENGTH
    ):
        raise ValueError("rain static streak lengths must be ordered above short rain")
    if not (
        0.0 <= RAIN_STATIC_STREAK_MIN_HEIGHT_FACTOR < RAIN_STATIC_STREAK_MAX_HEIGHT_FACTOR <= 1.0
    ):
        raise ValueError("rain static streak height factors must be normalized and ordered")
    if RAIN_STATIC_STREAK_FLASH_RATE < 0:
        raise ValueError("rain static streak flash rate must be non-negative")
    if not 0.0 <= RAIN_STATIC_STREAK_FLASH_THRESHOLD <= 1.0:
        raise ValueError("rain static streak flash threshold must be normalized")
    if RAIN_WIND_DRIFT_SCALE < 0 or RAIN_WIND_TILT_SCALE < 0:
        raise ValueError("rain wind scales must be non-negative")
    if not 0.0 <= RAIN_BRIGHT_VISIBILITY_THRESHOLD <= 1.0:
        raise ValueError("rain brightness threshold must be normalized")
    if len(RAIN_DEPTH_COLORS) != 4:
        raise ValueError("rain depth colors must define four tiers")
    if any(not 0 <= color <= 15 for color in RAIN_DEPTH_COLORS):
        raise ValueError("rain depth colors must use the Pyxel palette")
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
    if FIREFLY_MAX_COUNT < 0:
        raise ValueError("firefly count must be non-negative")
    if not (0.0 <= FIREFLY_TARGET_MIN_HEIGHT_FACTOR < FIREFLY_TARGET_MAX_HEIGHT_FACTOR <= 1.0):
        raise ValueError("firefly height factors must be normalized and ordered")
    if FIREFLY_TARGET_REACH_RADIUS <= 0:
        raise ValueError("firefly target reach radius must be positive")
    if FIREFLY_TARGET_MIN_DISTANCE <= FIREFLY_TARGET_REACH_RADIUS:
        raise ValueError("firefly target distance must exceed reach radius")
    if FIREFLY_LIFETIME_MIN <= 0 or FIREFLY_LIFETIME_MAX < FIREFLY_LIFETIME_MIN:
        raise ValueError("firefly lifetime range must be positive and ordered")
    if FIREFLY_SPAWN_DELAY_MIN <= 0 or FIREFLY_SPAWN_DELAY_MAX < FIREFLY_SPAWN_DELAY_MIN:
        raise ValueError("firefly spawn delay range must be positive and ordered")
    if not (
        0.0
        <= FIREFLY_RAIN_SPAWN_MULTIPLIER
        <= FIREFLY_AFTER_RAIN_SPAWN_MULTIPLIER
        <= FIREFLY_CLEAR_SPAWN_MULTIPLIER
    ):
        raise ValueError("firefly spawn multipliers must be normalized and ordered")
    if not 0.0 <= FIREFLY_STRONG_RAIN_THRESHOLD <= 1.0:
        raise ValueError("firefly rain threshold must be normalized")
    if FIREFLY_MAX_SPEED <= 0 or FIREFLY_TARGET_ACCELERATION < 0 or FIREFLY_WANDER_ACCELERATION < 0:
        raise ValueError("firefly motion values must be positive")
    if FIREFLY_BOUNDARY_MARGIN <= 0 or FIREFLY_BOUNDARY_ACCELERATION < 0:
        raise ValueError("firefly boundary values must be positive")
    if FIREFLY_WIND_INFLUENCE < 0:
        raise ValueError("firefly wind influence must be non-negative")
    if not 0.0 < FIREFLY_VELOCITY_DAMPING <= 1.0:
        raise ValueError("firefly damping must be normalized")
    if FIREFLY_GLOW_SPEED_MIN <= 0 or FIREFLY_GLOW_SPEED_MAX < FIREFLY_GLOW_SPEED_MIN:
        raise ValueError("firefly glow speed range must be positive and ordered")
    if (
        not 0.0
        <= FIREFLY_VISIBLE_THRESHOLD
        <= FIREFLY_BRIGHT_THRESHOLD
        <= FIREFLY_RING_THRESHOLD
        <= 1.0
    ):
        raise ValueError("firefly glow thresholds must be normalized and ordered")
    if not 0.0 <= CAMERA_INERTIA_DECAY < 1.0:
        raise ValueError("camera inertia decay must be normalized below one")
    if AUTO_ROTATE_PITCH_SWAY_AMOUNT < 0:
        raise ValueError("auto rotate pitch sway amount must be non-negative")
    if AUTO_ROTATE_PITCH_SWAY_RATE < 0:
        raise ValueError("auto rotate pitch sway rate must be non-negative")
    if not 0.0 < AUTO_ROTATE_PITCH_FOLLOW <= 1.0:
        raise ValueError("auto rotate pitch follow must be normalized")
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
        MENU_WIND_SPEED_MULTIPLIERS,
        MENU_RAIN_INTENSITIES,
        MENU_AUTO_ROTATE_MULTIPLIERS,
        MENU_FIREFLY_COUNTS,
    )
    if any(len(values) != MENU_STAGE_MAX for values in stage_sets):
        raise ValueError("menu stage value sets must have three entries")
    if MENU_PHOTON_COUNTS[0] != LIGHT_PARTICLE_COUNT:
        raise ValueError("menu photon stage 1 must match the current particle count")
    if MENU_GRASS_COUNTS[0] != GRASS_COUNT:
        raise ValueError("menu grass stage 1 must match the current grass count")
    if MENU_RAIN_INTENSITIES[0] != RAIN_DEFAULT_INTENSITY:
        raise ValueError("menu rain stage 1 must match the current rain intensity")
    if MENU_FIREFLY_COUNTS[-1] != FIREFLY_MAX_COUNT:
        raise ValueError("menu firefly stage 3 must match the firefly cap")
    if any(value <= 0 for value in MENU_PHOTON_COUNTS + MENU_GRASS_COUNTS):
        raise ValueError("menu density stage values must be positive")
    if any(value <= 0 for value in MENU_FIREFLY_COUNTS):
        raise ValueError("menu firefly stage values must be positive")
    if any(
        value <= 0.0
        for value in (
            MENU_WIND_MULTIPLIERS + MENU_WIND_SPEED_MULTIPLIERS + MENU_AUTO_ROTATE_MULTIPLIERS
        )
    ):
        raise ValueError("menu motion multipliers must be positive")
    if any(not 0.0 <= value <= 1.0 for value in MENU_RAIN_INTENSITIES):
        raise ValueError("menu rain intensities must be normalized")
    for values in stage_sets:
        if tuple(sorted(values)) != values:
            raise ValueError("menu stage values must be ordered")
    _validate_observation_cycle()


def _validate_observation_cycle() -> None:
    durations = (
        OBSERVATION_CYCLE_CLEAR_DURATION,
        OBSERVATION_CYCLE_SHADOW_DURATION,
        OBSERVATION_CYCLE_LIGHT_RAIN_DURATION,
        OBSERVATION_CYCLE_RAIN_DURATION,
        OBSERVATION_CYCLE_AFTER_RAIN_DURATION,
    )
    if any(duration <= 0.0 for duration in durations):
        raise ValueError("observation cycle durations must be positive")
    if not 0.0 <= OBSERVATION_CYCLE_CLOUD_SHADOW_AMOUNT <= 1.0:
        raise ValueError("observation cycle cloud shadow amount must be normalized")
    if not 0.0 <= OBSERVATION_CYCLE_LIGHT_RAIN_MULTIPLIER <= 1.0:
        raise ValueError("observation cycle light rain multiplier must be normalized")
