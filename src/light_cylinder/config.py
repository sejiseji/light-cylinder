REFERENCE_WIDTH = 393
REFERENCE_HEIGHT = 852

RENDER_WIDTH = 448
RENDER_HEIGHT = 852

COMPOSITION_SAFE_WIDTH = 393

SAFE_LEFT = (RENDER_WIDTH - COMPOSITION_SAFE_WIDTH) // 2
SAFE_RIGHT = SAFE_LEFT + COMPOSITION_SAFE_WIDTH

TARGET_FPS = 30

PROJECT_TITLE = "Light Cylinder"

CAMERA_INITIAL_YAW = 0.0
CAMERA_INITIAL_PITCH = 0.32
CAMERA_INITIAL_DISTANCE = 460.0
CAMERA_MIN_DISTANCE = 180.0
CAMERA_MAX_DISTANCE = 900.0
CAMERA_MIN_PITCH = -1.3962634015954636
CAMERA_MAX_PITCH = 1.3962634015954636
CAMERA_FOCAL_LENGTH = 300.0
CAMERA_YAW_SPEED = 0.035
CAMERA_PITCH_SPEED = 0.025
CAMERA_ZOOM_SPEED = 12.0
AUTO_ROTATE_SPEED = 0.01

CYLINDER_RADIUS = 96.0
CYLINDER_HEIGHT = 240.0
CYLINDER_RADIAL_SEGMENTS = 32
CYLINDER_VERTICAL_GUIDES = 8
CYLINDER_TARGET_HEIGHT_FACTOR = 0.45


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
