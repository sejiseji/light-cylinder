from itertools import pairwise
from math import cos, sin, tau

from light_cylinder.camera import Camera
from light_cylinder.config import (
    AUTO_ROTATE_SPEED,
    CAMERA_INERTIA_DECAY,
    CAMERA_PITCH_SPEED,
    CAMERA_YAW_SPEED,
    CAMERA_ZOOM_SPEED,
    COMPOSITION_SAFE_WIDTH,
    CYLINDER_HEIGHT,
    CYLINDER_RADIAL_SEGMENTS,
    CYLINDER_RADIUS,
    CYLINDER_VERTICAL_GUIDES,
    DISPLAY_TITLE_EN,
    DISPLAY_TITLE_JA,
    GRASS_COUNT,
    GRASS_SEED,
    GRASS_SEGMENTS,
    LIGHT_FLOOR_THRESHOLD_HIGH,
    LIGHT_FLOOR_THRESHOLD_LOW,
    LIGHT_FLOOR_THRESHOLD_MEDIUM,
    LIGHT_GRASS_THRESHOLD_HIGH,
    LIGHT_GRASS_THRESHOLD_LOW,
    LIGHT_GRASS_THRESHOLD_MEDIUM,
    LIGHT_GROUND_SPARK_THRESHOLD,
    LIGHT_PARTICLE_VISIBILITY_THRESHOLD,
    MOUSE_PITCH_SPEED,
    MOUSE_WHEEL_ZOOM_SPEED,
    MOUSE_YAW_SPEED,
    PALETTE_AXIS_X,
    PALETTE_AXIS_Y,
    PALETTE_AXIS_Z,
    PALETTE_BACKGROUND,
    PALETTE_BACKGROUND_BAND,
    PALETTE_BRIGHT_PARTICLE,
    PALETTE_CYLINDER_FAR_EDGE,
    PALETTE_CYLINDER_NEAR_EDGE,
    PALETTE_CYLINDER_VERTICAL,
    PALETTE_DEBUG_ACCENT,
    PALETTE_DEBUG_FRAME,
    PALETTE_DEBUG_TEXT,
    PALETTE_DIM_PARTICLE,
    PALETTE_DISTANT_GRASS,
    PALETTE_FOREGROUND_GRASS,
    PALETTE_GROUND_LIGHT,
    PALETTE_GROUND_SHADOW,
    PALETTE_GROUND_STRONG_LIGHT,
    PALETTE_LIT_GRASS,
    PALETTE_NORMAL_GRASS,
    PALETTE_SAFE_AREA,
    PALETTE_STRONGLY_LIT_GRASS,
    PROJECT_TITLE,
    RAIN_BRIGHT_VISIBILITY_THRESHOLD,
    RAIN_DEFAULT_INTENSITY,
    RAIN_LIGHT_VISIBILITY_THRESHOLD,
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
from light_cylinder.rain import RainField
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
        self.debug_visible = False
        self.boundary_visible = False
        self.wind_enabled = True
        self.light_enabled = True
        self.rain_enabled = False
        self.cylinder_lines = self._build_cylinder_lines()
        self.floor_lines = self._build_floor_lines()
        self.axis_lines = self._build_axis_lines()
        self.grass_field = GrassField.generate(self.world, seed=GRASS_SEED, grass_count=GRASS_COUNT)
        self.wind_field = WindField.create_default()
        self.light_field = LightField.create_default(self.world)
        self.rain_field = RainField.create_default(self.world, self.light_field.beam)
        self.camera_yaw_velocity = 0.0
        self.camera_pitch_velocity = 0.0
        self.camera_zoom_velocity = 0.0
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        self.visible_particle_count = 0
        self.visible_rain_count = 0
        self.lit_segment_count = 0
        self.approx_line_draw_calls = 0

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
        if intent.toggle_rain:
            self.rain_enabled = not self.rain_enabled
            if self.rain_field.intensity == 0.0:
                self.rain_field.set_intensity(RAIN_DEFAULT_INTENSITY)
        if intent.rain_intensity_delta != 0.0:
            self.rain_field.adjust_intensity(intent.rain_intensity_delta)
            if self.rain_field.intensity > 0.0:
                self.rain_enabled = True
        if intent.reset_camera:
            self._reset_camera()

        dt = 1.0 / TARGET_FPS
        self.wind_field.update(dt)
        self.light_field.update(dt)
        self.rain_field.update(dt)
        yaw_delta = self._camera_motion_delta("yaw", intent.yaw_delta)
        pitch_delta = self._camera_motion_delta("pitch", intent.pitch_delta)
        zoom_delta = self._camera_motion_delta("zoom", intent.zoom_delta)
        if self.auto_rotate:
            yaw_delta += AUTO_ROTATE_SPEED
        self.camera.orbit(yaw_delta, pitch_delta)
        self.camera.zoom(zoom_delta)

    def _reset_camera(self) -> None:
        self.camera = Camera.create_default()
        self.camera_yaw_velocity = 0.0
        self.camera_pitch_velocity = 0.0
        self.camera_zoom_velocity = 0.0

    def _camera_motion_delta(self, axis: str, input_delta: float) -> float:
        attr_name = f"camera_{axis}_velocity"
        if input_delta != 0.0:
            setattr(self, attr_name, input_delta)
            return input_delta

        velocity = getattr(self, attr_name) * CAMERA_INERTIA_DECAY
        if abs(velocity) < 0.0005:
            velocity = 0.0
        setattr(self, attr_name, velocity)
        return velocity

    def draw(self) -> None:
        import pyxel

        self.approx_line_draw_calls = 0
        self._draw_background(pyxel)
        self._draw_cylinder_scene(pyxel)
        self._draw_debug(pyxel)

    def _draw_background(self, pyxel) -> None:
        pyxel.cls(PALETTE_BACKGROUND)
        for x in range(SAFE_LEFT, SAFE_RIGHT, 16):
            if x % 32 == 0:
                pyxel.line(x, 0, x, RENDER_HEIGHT - 1, PALETTE_BACKGROUND_BAND)

    def _draw_cylinder_scene(self, pyxel) -> None:
        self._draw_floor(pyxel)
        if self.boundary_visible:
            self._draw_depth_sorted_lines(pyxel, self.cylinder_lines)
        self._draw_light_particles(pyxel)
        self._draw_rain(pyxel)
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
            intensity = self._light_intensity_at(spark.position) * spark.brightness
            if intensity < LIGHT_GROUND_SPARK_THRESHOLD:
                continue
            projected = self.camera.project(spark.position)
            if projected is not None:
                color = PALETTE_GROUND_STRONG_LIGHT if intensity > 0.7 else PALETTE_GROUND_LIGHT
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
            intensity = self._light_intensity_at(position) * particle.brightness
            if intensity < LIGHT_PARTICLE_VISIBILITY_THRESHOLD:
                continue
            projected = self.camera.project(position)
            if projected is None:
                continue

            color = select_particle_color(intensity)
            x = self._screen_int(projected.x)
            y = self._screen_int(projected.y)
            if intensity > 0.78:
                pyxel.circ(x, y, 1, color)
            else:
                pyxel.pset(x, y, color)
            self.visible_particle_count += 1

    def _draw_rain(self, pyxel) -> None:
        self.visible_rain_count = 0
        if not self.rain_enabled or not self.light_enabled:
            return

        wind = (
            self.wind_field.sample(self.world.top_center)
            if self.wind_enabled
            else Vec3(0.0, 0.0, 0.0)
        )
        sortable: list[tuple[float, Vec3, Vec3, int]] = []
        for drop, start, end in self.rain_field.segments(self.world, wind):
            midpoint = (start + end) * 0.5
            intensity = self._light_intensity_at(midpoint) * drop.brightness
            if intensity < RAIN_LIGHT_VISIBILITY_THRESHOLD:
                continue
            depth = self.camera.world_to_camera(midpoint).z
            color = select_rain_color(intensity)
            sortable.append((depth, start, end, color))

        for _depth, start, end, color in sorted(sortable, key=lambda item: item[0], reverse=True):
            if self._draw_world_line(pyxel, start, end, color):
                self.visible_rain_count += 1

    def _draw_grass(self, pyxel) -> None:
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        self.lit_segment_count = 0
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
                draw_calls = self._draw_grass_segment(
                    pyxel,
                    start,
                    end,
                    color,
                    blade.width_class,
                    segment_index,
                    segment_count,
                )
                if draw_calls:
                    blade_visible = True
                    self.visible_segment_count += 1
                    self.approx_line_draw_calls += draw_calls
                    if color in (PALETTE_LIT_GRASS, PALETTE_STRONGLY_LIT_GRASS):
                        self.lit_segment_count += 1
            if blade_visible:
                self.visible_blade_count += 1

            tip = self.camera.project(points[-1])
            if blade_visible and tip is not None:
                if light_colors[2] != light_colors[1]:
                    pyxel.pset(self._screen_int(tip.x), self._screen_int(tip.y), light_colors[2])
                elif blade.color_variant == 2:
                    pyxel.pset(
                        self._screen_int(tip.x), self._screen_int(tip.y), PALETTE_NORMAL_GRASS
                    )

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
    ) -> int:
        projected_start = self.camera.project(start)
        projected_end = self.camera.project(end)
        if projected_start is None or projected_end is None:
            return 0

        x1 = self._screen_int(projected_start.x)
        y1 = self._screen_int(projected_start.y)
        x2 = self._screen_int(projected_end.x)
        y2 = self._screen_int(projected_end.y)
        pyxel.line(x1, y1, x2, y2, color)
        draw_calls = 1
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
            draw_calls += 1
        return draw_calls

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
        return select_grass_color(blade.color_variant, depth > self.camera.distance + 80)

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
        intensity = self._light_intensity_at(point) * tier_weight
        return select_grass_light_color(base_color, intensity, tier_weight)

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
        return select_floor_color(base_color, self._light_intensity_at(point))

    def _light_intensity_at(self, point: Vec3) -> float:
        return self.light_field.beam.intensity_at(point) * self.light_field.intensity_multiplier

    def _draw_reference_points(self, pyxel) -> None:
        origin = self.world.bottom_center
        projected_origin = self.camera.project(origin)
        if projected_origin is not None:
            pyxel.circ(int(projected_origin.x), int(projected_origin.y), 3, PALETTE_DEBUG_TEXT)
            pyxel.text(
                int(projected_origin.x) + 5,
                int(projected_origin.y) + 4,
                "O",
                PALETTE_DEBUG_TEXT,
            )

        for point, color, label in (
            (self.world.sample_bottom_point(0.0, 0.0), PALETTE_DEBUG_TEXT, "C"),
            (self.world.sample_bottom_point(1.0, 0.0), PALETTE_AXIS_X, "+X"),
            (self.world.sample_bottom_point(1.0, 0.25), PALETTE_AXIS_Z, "+Z"),
            (self.world.top_center, PALETTE_AXIS_Y, "TOP"),
        ):
            projected = self.camera.project(point)
            if projected is not None:
                pyxel.circ(int(projected.x), int(projected.y), 2, color)
                pyxel.text(int(projected.x) + 4, int(projected.y) - 3, label, color)

    def _draw_debug(self, pyxel) -> None:
        if not self.debug_visible:
            return

        pyxel.text(SAFE_LEFT + 8, 12, DISPLAY_TITLE_EN, PALETTE_BRIGHT_PARTICLE)
        pyxel.text(SAFE_LEFT + 8, 24, DISPLAY_TITLE_JA, PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 36, "LC007 RAIN THROUGH LIGHT", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 48, "ARROWS/DRAG YAW-PITCH", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 60, "A/S/WHEEL ZOOM  R RESET", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 72, "X AUTO  B/W/L/N TOGGLES", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 84, "D HIDE DEBUG  ESC QUIT", PALETTE_DEBUG_TEXT)
        pyxel.text(
            SAFE_LEFT + 8, 96, f"AUTO {'ON' if self.auto_rotate else 'OFF'}", PALETTE_LIT_GRASS
        )
        pyxel.text(
            SAFE_LEFT + 8,
            108,
            f"BOUNDARY {'ON' if self.boundary_visible else 'OFF'}",
            PALETTE_LIT_GRASS,
        )
        pyxel.text(
            SAFE_LEFT + 8, 120, f"WIND {'ON' if self.wind_enabled else 'OFF'}", PALETTE_LIT_GRASS
        )
        pyxel.text(
            SAFE_LEFT + 8,
            132,
            f"LIGHT {'ON' if self.light_enabled else 'OFF'}",
            PALETTE_LIT_GRASS,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            144,
            f"RAIN {'ON' if self.rain_enabled else 'OFF'} {self.rain_field.intensity:.2f} Q/E",
            PALETTE_LIT_GRASS,
        )

        center_x = RENDER_WIDTH // 2
        center_y = RENDER_HEIGHT // 2
        pyxel.rectb(0, 0, RENDER_WIDTH, RENDER_HEIGHT, PALETTE_DEBUG_FRAME)
        pyxel.line(center_x, 0, center_x, RENDER_HEIGHT - 1, PALETTE_DEBUG_ACCENT)
        pyxel.line(0, center_y, RENDER_WIDTH - 1, center_y, PALETTE_DEBUG_ACCENT)
        pyxel.rectb(SAFE_LEFT, 0, COMPOSITION_SAFE_WIDTH, RENDER_HEIGHT, PALETTE_SAFE_AREA)
        pyxel.line(SAFE_LEFT, 0, SAFE_LEFT, RENDER_HEIGHT - 1, PALETTE_DISTANT_GRASS)
        pyxel.line(SAFE_RIGHT - 1, 0, SAFE_RIGHT - 1, RENDER_HEIGHT - 1, PALETTE_DISTANT_GRASS)
        pyxel.text(SAFE_LEFT + 8, 162, f"yaw {self.camera.yaw:.2f}", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 174, f"pitch {self.camera.pitch:.2f}", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 186, f"distance {self.camera.distance:.1f}", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 198, f"grass {len(self.grass_field)}", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 210, f"segments {GRASS_SEGMENTS}", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 222, f"visible {self.visible_blade_count}", PALETTE_DEBUG_TEXT)
        pyxel.text(SAFE_LEFT + 8, 234, f"lit seg {self.lit_segment_count}", PALETTE_DEBUG_TEXT)
        pyxel.text(
            SAFE_LEFT + 8,
            246,
            f"line calls {self.approx_line_draw_calls}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            258,
            f"particles {self.visible_particle_count}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            270,
            f"rain seg {self.visible_rain_count}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(SAFE_LEFT + 8, 282, f"wind {self.wind_field.base_speed:.2f}", PALETTE_DEBUG_TEXT)
        pyxel.text(
            SAFE_LEFT + 8,
            294,
            f"gust {self.wind_field.current_gust_strength:.2f}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            306,
            f"cloud {self.light_field.intensity_multiplier:.2f}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8, 318, f"time {self.wind_field.elapsed_time:.1f}", PALETTE_DEBUG_TEXT
        )

    def _draw_light_debug(self, pyxel) -> None:
        beam = self.light_field.beam
        self._draw_world_line(
            pyxel,
            beam.axis_point_at(0.0),
            beam.axis_point_at(1.0),
            PALETTE_BRIGHT_PARTICLE,
        )
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
            self._draw_world_line(
                pyxel, start, points[(index + 1) % len(points)], PALETTE_LIT_GRASS
            )

    def _build_cylinder_lines(self) -> tuple[WorldLine, ...]:
        bottom = self.world.bottom_ring_points(CYLINDER_RADIAL_SEGMENTS)
        top = self.world.top_ring_points(CYLINDER_RADIAL_SEGMENTS)
        lines: list[WorldLine] = []

        for index in range(CYLINDER_RADIAL_SEGMENTS):
            next_index = (index + 1) % CYLINDER_RADIAL_SEGMENTS
            color = (
                PALETTE_CYLINDER_FAR_EDGE
                if bottom[index].z < self.world.center_z
                else PALETTE_CYLINDER_NEAR_EDGE
            )
            lines.append((bottom[index], bottom[next_index], color))
            lines.append((top[index], top[next_index], color))

        for start, end in self.world.vertical_guide_segments(CYLINDER_VERTICAL_GUIDES):
            lines.append((start, end, PALETTE_CYLINDER_VERTICAL))

        lines.append((self.world.bottom_center, self.world.top_center, PALETTE_CYLINDER_VERTICAL))
        return tuple(lines)

    def _build_floor_lines(self) -> tuple[WorldLine, ...]:
        lines: list[WorldLine] = []
        for angle_index in range(8):
            end = self.world.sample_bottom_point(1.0, angle_index / 8)
            lines.append((self.world.bottom_center, end, PALETTE_GROUND_SHADOW))

        for radius_factor in (0.33, 0.66):
            ring = self.world.ring_points_at(
                CYLINDER_RADIAL_SEGMENTS,
                self.world.bottom_y,
                self.world.radius * radius_factor,
            )
            for index in range(CYLINDER_RADIAL_SEGMENTS):
                lines.append(
                    (
                        ring[index],
                        ring[(index + 1) % CYLINDER_RADIAL_SEGMENTS],
                        PALETTE_GROUND_SHADOW,
                    )
                )

        return tuple(lines)

    def _build_axis_lines(self) -> tuple[WorldLine, ...]:
        origin = self.world.bottom_center
        return (
            (origin, Vec3(CYLINDER_RADIUS * 1.25, 0.0, 0.0), PALETTE_AXIS_X),
            (origin, Vec3(0.0, CYLINDER_HEIGHT * 1.08, 0.0), PALETTE_AXIS_Y),
            (origin, Vec3(0.0, 0.0, CYLINDER_RADIUS * 1.25), PALETTE_AXIS_Z),
        )

    def _draw_depth_sorted_lines(self, pyxel, lines: tuple[WorldLine, ...]) -> None:
        sortable: list[tuple[float, WorldLine]] = []
        for line in lines:
            start, end, _color = line
            midpoint = (start + end) * 0.5
            sortable.append((self.camera.world_to_camera(midpoint).z, line))

        for _depth, (start, end, color) in sorted(sortable, key=lambda item: item[0], reverse=True):
            self._draw_world_line(pyxel, start, end, color)

    def _draw_world_line(self, pyxel, start: Vec3, end: Vec3, color: int) -> bool:
        projected_start = self.camera.project(start)
        projected_end = self.camera.project(end)
        if projected_start is None or projected_end is None:
            return False
        pyxel.line(
            self._screen_int(projected_start.x),
            self._screen_int(projected_start.y),
            self._screen_int(projected_end.x),
            self._screen_int(projected_end.y),
            color,
        )
        self.approx_line_draw_calls += 1
        return True

    def _screen_int(self, value: float) -> int:
        return max(-32768, min(32767, int(value)))


def select_grass_color(color_variant: int, is_distant: bool) -> int:
    if is_distant:
        return PALETTE_DISTANT_GRASS
    if color_variant == 1:
        return PALETTE_FOREGROUND_GRASS
    if color_variant == 2:
        return PALETTE_DISTANT_GRASS
    return PALETTE_NORMAL_GRASS


def select_grass_light_color(base_color: int, intensity: float, tier_weight: float) -> int:
    if tier_weight >= 1.0:
        if intensity > LIGHT_GRASS_THRESHOLD_HIGH:
            return PALETTE_STRONGLY_LIT_GRASS
        if intensity > LIGHT_GRASS_THRESHOLD_MEDIUM:
            return PALETTE_LIT_GRASS
        if intensity > LIGHT_GRASS_THRESHOLD_LOW:
            return PALETTE_NORMAL_GRASS
        return base_color
    if intensity > LIGHT_GRASS_THRESHOLD_HIGH + 0.06:
        return PALETTE_STRONGLY_LIT_GRASS
    if intensity > LIGHT_GRASS_THRESHOLD_MEDIUM + 0.08:
        return PALETTE_LIT_GRASS
    return base_color


def select_floor_color(base_color: int, intensity: float) -> int:
    if intensity > LIGHT_FLOOR_THRESHOLD_HIGH:
        return PALETTE_GROUND_STRONG_LIGHT
    if intensity > LIGHT_FLOOR_THRESHOLD_MEDIUM:
        return PALETTE_GROUND_LIGHT
    if intensity > LIGHT_FLOOR_THRESHOLD_LOW:
        return PALETTE_CYLINDER_NEAR_EDGE
    return base_color


def select_particle_color(intensity: float) -> int:
    if intensity > 0.72:
        return PALETTE_BRIGHT_PARTICLE
    if intensity > 0.48:
        return PALETTE_LIT_GRASS
    return PALETTE_DIM_PARTICLE


def select_rain_color(intensity: float) -> int:
    if intensity > RAIN_BRIGHT_VISIBILITY_THRESHOLD:
        return PALETTE_BRIGHT_PARTICLE
    return PALETTE_DIM_PARTICLE
