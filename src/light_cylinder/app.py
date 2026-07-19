from itertools import pairwise

from light_cylinder.camera import Camera
from light_cylinder.config import (
    AUTO_ROTATE_SPEED,
    CAMERA_PITCH_SPEED,
    CAMERA_YAW_SPEED,
    CAMERA_ZOOM_SPEED,
    COMPOSITION_SAFE_WIDTH,
    CYLINDER_HEIGHT,
    CYLINDER_RADIAL_SEGMENTS,
    CYLINDER_RADIUS,
    CYLINDER_VERTICAL_GUIDES,
    GRASS_COUNT,
    GRASS_SEED,
    GRASS_SEGMENTS,
    PROJECT_TITLE,
    RENDER_HEIGHT,
    RENDER_WIDTH,
    SAFE_LEFT,
    SAFE_RIGHT,
    TARGET_FPS,
    validate_display_config,
)
from light_cylinder.grass import GrassBlade, GrassField, sample_blade_points
from light_cylinder.input import read_control_intent
from light_cylinder.math3d import Vec3
from light_cylinder.world import CylinderWorld

WorldLine = tuple[Vec3, Vec3, int]
GrassPath = tuple[GrassBlade, tuple[Vec3, ...]]


class LightCylinderApp:
    def __init__(self) -> None:
        validate_display_config()
        self.world = CylinderWorld()
        self.camera = Camera.create_default()
        self.auto_rotate = False
        self.debug_visible = True
        self.boundary_visible = True
        self.cylinder_lines = self._build_cylinder_lines()
        self.floor_lines = self._build_floor_lines()
        self.axis_lines = self._build_axis_lines()
        self.grass_field = GrassField.generate(self.world, seed=GRASS_SEED, grass_count=GRASS_COUNT)
        self.grass_paths = tuple(
            (blade, sample_blade_points(blade, GRASS_SEGMENTS)) for blade in self.grass_field.blades
        )
        self.visible_blade_count = 0
        self.visible_segment_count = 0

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
        if intent.toggle_boundary:
            self.boundary_visible = not self.boundary_visible

        yaw_delta = intent.yaw_delta
        if self.auto_rotate:
            yaw_delta += AUTO_ROTATE_SPEED
        self.camera.orbit(yaw_delta, intent.pitch_delta)
        self.camera.zoom(intent.zoom_delta)

    def draw(self) -> None:
        import pyxel

        pyxel.cls(1)
        self._draw_cylinder_scene(pyxel)
        self._draw_debug(pyxel)

    def _draw_cylinder_scene(self, pyxel) -> None:
        self._draw_depth_sorted_lines(pyxel, self.floor_lines)
        if self.boundary_visible:
            self._draw_depth_sorted_lines(pyxel, self.cylinder_lines)
        self._draw_grass(pyxel)
        self._draw_depth_sorted_lines(pyxel, self.axis_lines)
        self._draw_reference_points(pyxel)

    def _draw_grass(self, pyxel) -> None:
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        sortable: list[tuple[float, GrassPath]] = []
        for blade, points in self.grass_paths:
            midpoint = points[len(points) // 2]
            sortable.append((self.camera.world_to_camera(midpoint).z, (blade, points)))

        for depth, (blade, points) in sorted(sortable, key=lambda item: item[0], reverse=True):
            color = self._grass_color(blade, depth)
            blade_visible = False
            for start, end in pairwise(points):
                if self._draw_grass_segment(pyxel, start, end, color, blade.width_class):
                    blade_visible = True
                    self.visible_segment_count += 1
            if blade_visible:
                self.visible_blade_count += 1

            tip = self.camera.project(points[-1])
            if blade_visible and tip is not None and blade.color_variant == 2:
                pyxel.pset(self._screen_int(tip.x), self._screen_int(tip.y), 11)

    def _draw_grass_segment(
        self,
        pyxel,
        start: Vec3,
        end: Vec3,
        color: int,
        width_class: int,
    ) -> bool:
        projected_start = self.camera.project(start)
        projected_end = self.camera.project(end)
        if projected_start is None or projected_end is None:
            return False

        x1 = self._screen_int(projected_start.x)
        y1 = self._screen_int(projected_start.y)
        x2 = self._screen_int(projected_end.x)
        y2 = self._screen_int(projected_end.y)
        pyxel.line(x1, y1, x2, y2, color)
        if width_class == 2:
            pyxel.line(x1 + 1, y1, x2 + 1, y2, color)
        return True

    def _grass_color(self, blade: GrassBlade, depth: float) -> int:
        if depth > self.camera.distance + 80:
            return 3
        if blade.color_variant == 0:
            return 11
        if blade.color_variant == 1:
            return 10
        return 3

    def _draw_reference_points(self, pyxel) -> None:
        origin = self.world.bottom_center
        projected_origin = self.camera.project(origin)
        if projected_origin is not None:
            pyxel.circ(int(projected_origin.x), int(projected_origin.y), 3, 7)
            pyxel.text(int(projected_origin.x) + 5, int(projected_origin.y) + 4, "O", 7)

        for point, color, label in (
            (self.world.sample_bottom_point(0.0, 0.0), 7, "C"),
            (self.world.sample_bottom_point(1.0, 0.0), 8, "+X"),
            (self.world.sample_bottom_point(1.0, 0.25), 12, "+Z"),
            (self.world.top_center, 11, "TOP"),
        ):
            projected = self.camera.project(point)
            if projected is not None:
                pyxel.circ(int(projected.x), int(projected.y), 2, color)
                pyxel.text(int(projected.x) + 4, int(projected.y) - 3, label, color)

    def _draw_debug(self, pyxel) -> None:
        pyxel.text(SAFE_LEFT + 8, 12, PROJECT_TITLE, 7)
        pyxel.text(SAFE_LEFT + 8, 24, "LC003 CURVED GRASS FIELD", 6)
        pyxel.text(SAFE_LEFT + 8, 36, "ARROWS YAW/PITCH  A/S ZOOM", 6)
        pyxel.text(SAFE_LEFT + 8, 48, "X AUTO  B BOUNDARY  D DEBUG", 6)
        pyxel.text(SAFE_LEFT + 8, 60, "ESC QUIT", 6)
        pyxel.text(SAFE_LEFT + 8, 72, f"AUTO {'ON' if self.auto_rotate else 'OFF'}", 10)
        pyxel.text(SAFE_LEFT + 8, 84, f"BOUNDARY {'ON' if self.boundary_visible else 'OFF'}", 10)
        pyxel.text(SAFE_LEFT + 8, 96, f"DEBUG {'ON' if self.debug_visible else 'OFF'}", 10)

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
        pyxel.text(SAFE_LEFT + 8, 114, f"yaw {self.camera.yaw:.2f}", 6)
        pyxel.text(SAFE_LEFT + 8, 126, f"pitch {self.camera.pitch:.2f}", 6)
        pyxel.text(SAFE_LEFT + 8, 138, f"distance {self.camera.distance:.1f}", 6)
        pyxel.text(SAFE_LEFT + 8, 150, f"radius {self.world.radius:.1f}", 6)
        pyxel.text(SAFE_LEFT + 8, 162, f"height {self.world.height:.1f}", 6)
        pyxel.text(SAFE_LEFT + 8, 174, f"near {self.camera.near_clip:.1f}", 6)
        pyxel.text(SAFE_LEFT + 8, 186, f"grass {len(self.grass_field)}", 6)
        pyxel.text(SAFE_LEFT + 8, 198, f"segments {GRASS_SEGMENTS}", 6)
        pyxel.text(SAFE_LEFT + 8, 210, f"seed {self.grass_field.seed}", 6)
        pyxel.text(SAFE_LEFT + 8, 222, f"visible {self.visible_blade_count}", 6)
        pyxel.text(SAFE_LEFT + 8, 234, f"lines {self.visible_segment_count}", 6)

    def _build_cylinder_lines(self) -> tuple[WorldLine, ...]:
        bottom = self.world.bottom_ring_points(CYLINDER_RADIAL_SEGMENTS)
        top = self.world.top_ring_points(CYLINDER_RADIAL_SEGMENTS)
        lines: list[WorldLine] = []

        for index in range(CYLINDER_RADIAL_SEGMENTS):
            next_index = (index + 1) % CYLINDER_RADIAL_SEGMENTS
            color = 5 if bottom[index].z < self.world.center_z else 13
            lines.append((bottom[index], bottom[next_index], color))
            lines.append((top[index], top[next_index], color))

        for start, end in self.world.vertical_guide_segments(CYLINDER_VERTICAL_GUIDES):
            lines.append((start, end, 6))

        lines.append((self.world.bottom_center, self.world.top_center, 11))
        return tuple(lines)

    def _build_floor_lines(self) -> tuple[WorldLine, ...]:
        lines: list[WorldLine] = []
        for angle_index in range(8):
            end = self.world.sample_bottom_point(1.0, angle_index / 8)
            lines.append((self.world.bottom_center, end, 5))

        for radius_factor in (0.33, 0.66):
            ring = self.world.ring_points_at(
                CYLINDER_RADIAL_SEGMENTS,
                self.world.bottom_y,
                self.world.radius * radius_factor,
            )
            for index in range(CYLINDER_RADIAL_SEGMENTS):
                lines.append((ring[index], ring[(index + 1) % CYLINDER_RADIAL_SEGMENTS], 5))

        return tuple(lines)

    def _build_axis_lines(self) -> tuple[WorldLine, ...]:
        origin = self.world.bottom_center
        return (
            (origin, Vec3(CYLINDER_RADIUS * 1.25, 0.0, 0.0), 8),
            (origin, Vec3(0.0, CYLINDER_HEIGHT * 1.08, 0.0), 11),
            (origin, Vec3(0.0, 0.0, CYLINDER_RADIUS * 1.25), 12),
        )

    def _draw_depth_sorted_lines(self, pyxel, lines: tuple[WorldLine, ...]) -> None:
        sortable: list[tuple[float, WorldLine]] = []
        for line in lines:
            start, end, _color = line
            midpoint = (start + end) * 0.5
            sortable.append((self.camera.world_to_camera(midpoint).z, line))

        for _depth, (start, end, color) in sorted(sortable, key=lambda item: item[0], reverse=True):
            self._draw_world_line(pyxel, start, end, color)

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
