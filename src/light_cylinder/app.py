from light_cylinder.camera import Camera
from light_cylinder.config import (
    AUTO_ROTATE_SPEED,
    CAMERA_PITCH_SPEED,
    CAMERA_YAW_SPEED,
    CAMERA_ZOOM_SPEED,
    COMPOSITION_SAFE_WIDTH,
    PROJECT_TITLE,
    RENDER_HEIGHT,
    RENDER_WIDTH,
    SAFE_LEFT,
    SAFE_RIGHT,
    TARGET_FPS,
    validate_display_config,
)
from light_cylinder.input import read_control_intent
from light_cylinder.math3d import Vec3


class LightCylinderApp:
    def __init__(self) -> None:
        validate_display_config()
        self.camera = Camera.create_default()
        self.auto_rotate = False
        self.debug_visible = True

    def run(self) -> None:
        import pyxel

        pyxel.init(RENDER_WIDTH, RENDER_HEIGHT, title=PROJECT_TITLE, fps=TARGET_FPS)
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        import pyxel

        intent = read_control_intent(pyxel, CAMERA_YAW_SPEED, CAMERA_PITCH_SPEED, CAMERA_ZOOM_SPEED)
        if intent.quit_requested:
            pyxel.quit()
            return

        if intent.toggle_auto_rotate:
            self.auto_rotate = not self.auto_rotate
        if intent.toggle_debug:
            self.debug_visible = not self.debug_visible

        yaw_delta = intent.yaw_delta
        if self.auto_rotate:
            yaw_delta += AUTO_ROTATE_SPEED
        self.camera.orbit(yaw_delta, intent.pitch_delta)
        self.camera.zoom(intent.zoom_delta)

    def draw(self) -> None:
        import pyxel

        pyxel.cls(1)
        self._draw_reference_grid(pyxel)
        self._draw_axes(pyxel)
        self._draw_debug(pyxel)

    def _draw_reference_grid(self, pyxel) -> None:
        grid_color = 5
        for value in range(-120, 121, 60):
            self._draw_world_line(
                pyxel,
                Vec3(-120.0, 0.0, value),
                Vec3(120.0, 0.0, value),
                grid_color,
            )
            self._draw_world_line(
                pyxel,
                Vec3(value, 0.0, -120.0),
                Vec3(value, 0.0, 120.0),
                grid_color,
            )

        for point in (
            Vec3(-80.0, 0.0, 80.0),
            Vec3(80.0, 0.0, 80.0),
            Vec3(-80.0, 80.0, -60.0),
            Vec3(80.0, 120.0, -60.0),
        ):
            projected = self.camera.project(point)
            if projected is not None:
                pyxel.circ(int(projected.x), int(projected.y), 2, 6)

    def _draw_axes(self, pyxel) -> None:
        origin = Vec3(0.0, 0.0, 0.0)
        axes = (
            (Vec3(140.0, 0.0, 0.0), 8, "X"),
            (Vec3(0.0, 160.0, 0.0), 11, "Y"),
            (Vec3(0.0, 0.0, 140.0), 12, "Z"),
        )

        projected_origin = self.camera.project(origin)
        if projected_origin is not None:
            pyxel.circ(int(projected_origin.x), int(projected_origin.y), 3, 7)
            pyxel.text(int(projected_origin.x) + 5, int(projected_origin.y) + 4, "O", 7)

        for end, color, label in axes:
            self._draw_world_line(pyxel, origin, end, color)
            projected = self.camera.project(end)
            if projected is not None:
                pyxel.text(int(projected.x) + 4, int(projected.y) - 3, label, color)

    def _draw_debug(self, pyxel) -> None:
        pyxel.text(SAFE_LEFT + 8, 12, PROJECT_TITLE, 7)
        pyxel.text(SAFE_LEFT + 8, 24, "LC001 CAMERA FOUNDATION", 6)
        pyxel.text(SAFE_LEFT + 8, 36, "ARROWS YAW/PITCH  A/S ZOOM", 6)
        pyxel.text(SAFE_LEFT + 8, 48, "X AUTO  D DEBUG  ESC QUIT", 6)
        pyxel.text(SAFE_LEFT + 8, 60, f"AUTO {'ON' if self.auto_rotate else 'OFF'}", 10)
        pyxel.text(SAFE_LEFT + 8, 72, f"DEBUG {'ON' if self.debug_visible else 'OFF'}", 10)

        if not self.debug_visible:
            return

        center_x = RENDER_WIDTH // 2
        center_y = RENDER_HEIGHT // 2
        pyxel.rectb(0, 0, RENDER_WIDTH, RENDER_HEIGHT, 5)
        pyxel.line(center_x, 0, center_x, RENDER_HEIGHT - 1, 13)
        pyxel.line(0, center_y, RENDER_WIDTH - 1, center_y, 13)
        pyxel.rectb(SAFE_LEFT, 0, COMPOSITION_SAFE_WIDTH, RENDER_HEIGHT, 11)
        pyxel.line(SAFE_LEFT, 0, SAFE_LEFT, RENDER_HEIGHT - 1, 3)
        pyxel.line(SAFE_RIGHT - 1, 0, SAFE_RIGHT - 1, RENDER_HEIGHT - 1, 3)
        pyxel.text(SAFE_LEFT + 8, 90, f"yaw {self.camera.yaw:.2f}", 6)
        pyxel.text(SAFE_LEFT + 8, 102, f"pitch {self.camera.pitch:.2f}", 6)
        pyxel.text(SAFE_LEFT + 8, 114, f"distance {self.camera.distance:.1f}", 6)
        pyxel.text(SAFE_LEFT + 8, 126, f"near {self.camera.near_clip:.1f}", 6)

    def _draw_world_line(self, pyxel, start: Vec3, end: Vec3, color: int) -> None:
        projected_start = self.camera.project(start)
        projected_end = self.camera.project(end)
        if projected_start is None or projected_end is None:
            return
        pyxel.line(
            self._screen_int(projected_start.x),
            self._screen_int(projected_start.y),
            self._screen_int(projected_end.x),
            self._screen_int(projected_end.y),
            color,
        )

    def _screen_int(self, value: float) -> int:
        return max(-32768, min(32767, int(value)))
