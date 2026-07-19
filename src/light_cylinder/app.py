from itertools import pairwise
from math import cos, sin, tau

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
    MOUSE_PITCH_SPEED,
    MOUSE_WHEEL_ZOOM_SPEED,
    MOUSE_YAW_SPEED,
    PROJECT_TITLE,
    RENDER_HEIGHT,
    RENDER_WIDTH,
    SAFE_LEFT,
    SAFE_RIGHT,
    TARGET_FPS,
    validate_display_config,
)
from light_cylinder.grass import GrassBlade, GrassField, compute_wind_bend, sample_blade_points
from light_cylinder.input import MouseInputState, read_control_intent
from light_cylinder.light import LightField, LightParticle
from light_cylinder.math3d import Vec3
from light_cylinder.weather import WindField
from light_cylinder.world import CylinderWorld

WorldLine = tuple[Vec3, Vec3, int]
GrassPath = tuple[GrassBlade, tuple[Vec3, ...]]
LitGrassPath = tuple[GrassBlade, tuple[Vec3, ...], tuple[int, int, int]]


class LightCylinderApp:
    def __init__(self) -> None:
        validate_display_config()
        self.world = CylinderWorld()
        self.camera = Camera.create_default()
        self.mouse_state = MouseInputState()
        self.auto_rotate = False
        self.debug_visible = True
        self.boundary_visible = True
        self.wind_enabled = True
        self.light_enabled = True
        self.cylinder_lines = self._build_cylinder_lines()
        self.floor_lines = self._build_floor_lines()
        self.axis_lines = self._build_axis_lines()
        self.grass_field = GrassField.generate(self.world, seed=GRASS_SEED, grass_count=GRASS_COUNT)
        self.wind_field = WindField.create_default()
        self.light_field = LightField.create_default(self.world)
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        self.visible_particle_count = 0

    def run(self) -> None:
        import pyxel

        pyxel.init(RENDER_WIDTH, RENDER_HEIGHT, title=PROJECT_TITLE, fps=TARGET_FPS)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        import pyxel

        intent = read_control_intent(
            pyxel,
            CAMERA_YAW_SPEED,
            CAMERA_PITCH_SPEED,
            CAMERA_ZOOM_SPEED,
            self.mouse_state,
            MOUSE_YAW_SPEED,
            MOUSE_PITCH_SPEED,
            MOUSE_WHEEL_ZOOM_SPEED,
        )
        if intent.quit_requested:
            pyxel.quit()
            return

        if intent.toggle_auto_rotate:
            self.auto_rotate = not self.auto_rotate
        if intent.toggle_debug:
            self.debug_visible = not self.debug_visible
        if intent.toggle_boundary:
            self.boundary_visible = not self.boundary_visible
        if intent.toggle_wind:
            self.wind_enabled = not self.wind_enabled
        if intent.toggle_light:
            self.light_enabled = not self.light_enabled

        dt = 1.0 / TARGET_FPS
        self.wind_field.update(dt)
        self.light_field.update(dt)
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
        self._draw_floor(pyxel)
        if self.boundary_visible:
            self._draw_depth_sorted_lines(pyxel, self.cylinder_lines)
        self._draw_light_particles(pyxel)
        self._draw_grass(pyxel)
        self._draw_ground_sparks(pyxel)
        if self.debug_visible:
            self._draw_depth_sorted_lines(pyxel, self.axis_lines)
            self._draw_reference_points(pyxel)
            self._draw_light_debug(pyxel)

    def _draw_floor(self, pyxel) -> None:
        sortable: list[tuple[float, WorldLine]] = []
        for line in self.floor_lines:
            start, end, _color = line
            midpoint = (start + end) * 0.5
            sortable.append((self.camera.world_to_camera(midpoint).z, line))

        for _depth, (start, end, color) in sorted(sortable, key=lambda item: item[0], reverse=True):
            midpoint = (start + end) * 0.5
            self._draw_world_line(pyxel, start, end, self._floor_color(midpoint, color))

    def _draw_ground_sparks(self, pyxel) -> None:
        if not self.light_enabled:
            return

        for spark in self.light_field.ground_sparks:
            intensity = self.light_field.beam.intensity_at(spark.position) * spark.brightness
            if intensity < 0.28:
                continue
            projected = self.camera.project(spark.position)
            if projected is not None:
                color = 7 if intensity > 0.7 else 10
                pyxel.pset(self._screen_int(projected.x), self._screen_int(projected.y), color)

    def _draw_light_particles(self, pyxel) -> None:
        self.visible_particle_count = 0
        if not self.light_enabled:
            return

        sortable: list[tuple[float, LightParticle, Vec3]] = []
        for particle, position in self.light_field.particle_positions():
            depth = self.camera.world_to_camera(position).z
            sortable.append((depth, particle, position))

        for _depth, particle, position in sorted(sortable, key=lambda item: item[0], reverse=True):
            intensity = self.light_field.beam.intensity_at(position) * particle.brightness
            if intensity < 0.24:
                continue
            projected = self.camera.project(position)
            if projected is None:
                continue

            color = 7 if intensity > 0.72 else 10 if intensity > 0.45 else 6
            x = self._screen_int(projected.x)
            y = self._screen_int(projected.y)
            if intensity > 0.78:
                pyxel.circ(x, y, 1, color)
            else:
                pyxel.pset(x, y, color)
            self.visible_particle_count += 1

    def _draw_grass(self, pyxel) -> None:
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        sortable: list[tuple[float, LitGrassPath]] = []
        for blade in self.grass_field.blades:
            points = self._sample_current_blade_points(blade)
            midpoint = points[len(points) // 2]
            depth = self.camera.world_to_camera(midpoint).z
            base_color = self._grass_color(blade, depth)
            light_colors = self._grass_light_colors(points, base_color)
            sortable.append((depth, (blade, points, light_colors)))

        for _depth, (blade, points, light_colors) in sorted(
            sortable,
            key=lambda item: item[0],
            reverse=True,
        ):
            blade_visible = False
            segment_count = len(points) - 1
            for segment_index, (start, end) in enumerate(pairwise(points)):
                color = self._grass_segment_color(light_colors, segment_index, segment_count)
                if self._draw_grass_segment(
                    pyxel,
                    start,
                    end,
                    color,
                    blade.width_class,
                    segment_index,
                    segment_count,
                ):
                    blade_visible = True
                    self.visible_segment_count += 1
            if blade_visible:
                self.visible_blade_count += 1

            tip = self.camera.project(points[-1])
            if blade_visible and tip is not None:
                if light_colors[2] != light_colors[1]:
                    pyxel.pset(self._screen_int(tip.x), self._screen_int(tip.y), light_colors[2])
                elif blade.color_variant == 2:
                    pyxel.pset(self._screen_int(tip.x), self._screen_int(tip.y), 11)

    def _sample_current_blade_points(self, blade: GrassBlade) -> tuple[Vec3, ...]:
        if not self.wind_enabled:
            return sample_blade_points(blade, GRASS_SEGMENTS)
        wind_bend = compute_wind_bend(blade, self.wind_field.sample(blade.base, blade.phase))
        return sample_blade_points(blade, GRASS_SEGMENTS, wind_bend)

    def _draw_grass_segment(
        self,
        pyxel,
        start: Vec3,
        end: Vec3,
        color: int,
        width_class: int,
        segment_index: int,
        segment_count: int,
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
        for offset_x, offset_y in self._grass_taper_offsets(
            x1,
            y1,
            x2,
            y2,
            width_class,
            segment_index,
            segment_count,
        ):
            pyxel.line(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y, color)
        return True

    def _grass_taper_offsets(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        width_class: int,
        segment_index: int,
        segment_count: int,
    ) -> tuple[tuple[int, int], ...]:
        if segment_count <= 0:
            return ()

        root_weight = 1.0 - segment_index / segment_count
        width = int(round((1 + width_class) * root_weight))
        if width <= 1:
            return ()

        dx = x2 - x1
        dy = y2 - y1
        perpendicular = (0, 1) if abs(dx) > abs(dy) else (1, 0)

        if width == 2:
            return (perpendicular,)
        return (perpendicular, (-perpendicular[0], -perpendicular[1]))

    def _grass_color(self, blade: GrassBlade, depth: float) -> int:
        if depth > self.camera.distance + 80:
            return 3
        if blade.color_variant == 0:
            return 11
        if blade.color_variant == 1:
            return 10
        return 3

    def _grass_light_colors(
        self,
        points: tuple[Vec3, ...],
        base_color: int,
    ) -> tuple[int, int, int]:
        if not self.light_enabled:
            return (base_color, base_color, base_color)

        root = self._grass_light_color(points[0], base_color, 0.16)
        middle = self._grass_light_color(points[len(points) // 2], base_color, 0.46)
        tip = self._grass_light_color(points[-1], base_color, 1.0)
        return (root, middle, tip)

    def _grass_light_color(self, point: Vec3, base_color: int, tier_weight: float) -> int:
        intensity = self.light_field.beam.intensity_at(point) * tier_weight
        if tier_weight >= 1.0:
            if intensity > 0.52:
                return 7
            if intensity > 0.28:
                return 10
            if intensity > 0.12:
                return 11
            return base_color
        if intensity > 0.64:
            return 7
        if intensity > 0.4:
            return 10
        return base_color

    def _grass_segment_color(
        self,
        light_colors: tuple[int, int, int],
        segment_index: int,
        segment_count: int,
    ) -> int:
        if segment_count <= 1:
            return light_colors[2]
        if segment_index >= segment_count - 1:
            return light_colors[2]
        if segment_index >= segment_count // 2:
            return light_colors[1]
        return light_colors[0]

    def _floor_color(self, point: Vec3, base_color: int) -> int:
        if not self.light_enabled:
            return base_color
        intensity = self.light_field.beam.intensity_at(point)
        if intensity > 0.72:
            return 7
        if intensity > 0.36:
            return 10
        if intensity > 0.16:
            return 13
        return base_color

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
        if not self.debug_visible:
            return

        pyxel.text(SAFE_LEFT + 8, 12, PROJECT_TITLE, 7)
        pyxel.text(SAFE_LEFT + 8, 24, "LC005 LIGHT MEDIUM", 6)
        pyxel.text(SAFE_LEFT + 8, 36, "ARROWS/DRAG YAW-PITCH", 6)
        pyxel.text(SAFE_LEFT + 8, 48, "A/S/WHEEL ZOOM  L LIGHT", 6)
        pyxel.text(SAFE_LEFT + 8, 60, "D DEBUG  ESC QUIT", 6)
        pyxel.text(SAFE_LEFT + 8, 72, f"AUTO {'ON' if self.auto_rotate else 'OFF'}", 10)
        pyxel.text(SAFE_LEFT + 8, 84, f"BOUNDARY {'ON' if self.boundary_visible else 'OFF'}", 10)
        pyxel.text(SAFE_LEFT + 8, 96, f"WIND {'ON' if self.wind_enabled else 'OFF'}", 10)
        pyxel.text(SAFE_LEFT + 8, 108, f"LIGHT {'ON' if self.light_enabled else 'OFF'}", 10)

        center_x = RENDER_WIDTH // 2
        center_y = RENDER_HEIGHT // 2
        pyxel.rectb(0, 0, RENDER_WIDTH, RENDER_HEIGHT, 5)
        pyxel.line(center_x, 0, center_x, RENDER_HEIGHT - 1, 13)
        pyxel.line(0, center_y, RENDER_WIDTH - 1, center_y, 13)
        pyxel.rectb(SAFE_LEFT, 0, COMPOSITION_SAFE_WIDTH, RENDER_HEIGHT, 11)
        pyxel.line(SAFE_LEFT, 0, SAFE_LEFT, RENDER_HEIGHT - 1, 3)
        pyxel.line(SAFE_RIGHT - 1, 0, SAFE_RIGHT - 1, RENDER_HEIGHT - 1, 3)
        pyxel.text(SAFE_LEFT + 8, 126, f"yaw {self.camera.yaw:.2f}", 6)
        pyxel.text(SAFE_LEFT + 8, 138, f"pitch {self.camera.pitch:.2f}", 6)
        pyxel.text(SAFE_LEFT + 8, 150, f"distance {self.camera.distance:.1f}", 6)
        pyxel.text(SAFE_LEFT + 8, 162, f"grass {len(self.grass_field)}", 6)
        pyxel.text(SAFE_LEFT + 8, 174, f"segments {GRASS_SEGMENTS}", 6)
        pyxel.text(SAFE_LEFT + 8, 186, f"seed {self.grass_field.seed}", 6)
        pyxel.text(SAFE_LEFT + 8, 198, f"visible {self.visible_blade_count}", 6)
        pyxel.text(SAFE_LEFT + 8, 210, f"lines {self.visible_segment_count}", 6)
        pyxel.text(SAFE_LEFT + 8, 222, f"particles {self.visible_particle_count}", 6)
        pyxel.text(SAFE_LEFT + 8, 234, f"wind {self.wind_field.base_speed:.2f}", 6)
        pyxel.text(SAFE_LEFT + 8, 246, f"gust {self.wind_field.current_gust_strength:.2f}", 6)
        pyxel.text(SAFE_LEFT + 8, 258, f"time {self.wind_field.elapsed_time:.1f}", 6)

    def _draw_light_debug(self, pyxel) -> None:
        beam = self.light_field.beam
        self._draw_world_line(pyxel, beam.axis_point_at(0.0), beam.axis_point_at(1.0), 7)
        for normalized_position in (0.28, 0.5, 0.72):
            self._draw_light_radius_ring(pyxel, normalized_position)

    def _draw_light_radius_ring(self, pyxel, normalized_position: float) -> None:
        beam = self.light_field.beam
        center = beam.axis_point_at(normalized_position)
        basis_u, basis_v = beam.basis()
        points = tuple(
            center
            + basis_u * (beam.radius * cos(tau * index / 16))
            + basis_v * (beam.radius * sin(tau * index / 16))
            for index in range(16)
        )
        for index, start in enumerate(points):
            self._draw_world_line(pyxel, start, points[(index + 1) % len(points)], 10)

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
