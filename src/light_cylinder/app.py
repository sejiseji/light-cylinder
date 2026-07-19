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
    TIP_DROPLET_LIGHT_THRESHOLD,
    validate_display_config,
)
from light_cylinder.environment import EnvironmentState
from light_cylinder.grass import GrassBlade, GrassField, compute_wind_bend, sample_blade_points
from light_cylinder.input import MouseInputState, read_control_intent
from light_cylinder.light import LightField, LightParticle
from light_cylinder.math3d import Vec3
from light_cylinder.rain import RainField
from light_cylinder.reactions import GrassReactionField, GroundReactionField, TipDropletField
from light_cylinder.tuning import MENU_SETTING_KEYS, ObservationTuning
from light_cylinder.weather import WindField
from light_cylinder.world import CylinderWorld

WorldLine = tuple[Vec3, Vec3, int]
GrassPath = tuple[GrassBlade, tuple[Vec3, ...]]
LitGrassPath = tuple[GrassBlade, tuple[Vec3, ...], tuple[int, int, int]]
MenuRect = tuple[int, int, int, int]

MENU_BUTTON_RECT: MenuRect = (SAFE_RIGHT - 54, 8, 46, 16)
MENU_PANEL_RECT: MenuRect = (SAFE_RIGHT - 190, 30, 182, 132)
MENU_ROW_TOP = 54
MENU_ROW_HEIGHT = 20
MENU_ROW_LABELS = {
    "photons": "PHOTON",
    "grass": "GRASS",
    "wind": "WIND",
    "rain": "RAIN",
    "rotate": "ROTATE",
}


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
        self.environment = EnvironmentState()
        self.tuning = ObservationTuning()
        self.menu_open = False
        self.cylinder_lines = self._build_cylinder_lines()
        self.floor_lines = self._build_floor_lines()
        self.axis_lines = self._build_axis_lines()
        self.grass_field = GrassField.generate(
            self.world,
            seed=GRASS_SEED,
            grass_count=self.tuning.max_grass_count,
        )
        self.wind_field = WindField.create_default()
        self.light_field = LightField.create_default(
            self.world,
            particle_count=self.tuning.max_photon_count,
        )
        self.rain_field = RainField.create_default(self.world, self.light_field.beam)
        self.rain_field.set_intensity(self.tuning.rain_intensity)
        self.ground_reactions = GroundReactionField()
        self.grass_reactions = GrassReactionField.create(len(self.grass_field.blades))
        self.tip_droplets = TipDropletField.create(
            self.grass_field.blades[: self.tuning.grass_count]
        )
        self.after_rain_droplets_seeded = False
        self.camera_yaw_velocity = 0.0
        self.camera_pitch_velocity = 0.0
        self.camera_zoom_velocity = 0.0
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        self.visible_particle_count = 0
        self.visible_rain_count = 0
        self.visible_splash_count = 0
        self.visible_droplet_count = 0
        self.lit_segment_count = 0
        self.approx_line_draw_calls = 0

    def run(self) -> None:
        import pyxel

        pyxel.init(RENDER_WIDTH, RENDER_HEIGHT, title=PROJECT_TITLE, fps=TARGET_FPS)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        import pyxel

        menu_captures_mouse = self._menu_captures_mouse(pyxel)
        intent = read_control_intent(
            pyxel,
            CAMERA_YAW_SPEED,
            CAMERA_PITCH_SPEED,
            CAMERA_ZOOM_SPEED,
            None if menu_captures_mouse else self.mouse_state,
            MOUSE_YAW_SPEED,
            MOUSE_PITCH_SPEED,
            MOUSE_WHEEL_ZOOM_SPEED,
        )
        self._update_menu_input(pyxel)
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
            self._set_rain_enabled(not self.rain_enabled)
            if self.rain_field.intensity == 0.0:
                self.rain_field.set_intensity(RAIN_DEFAULT_INTENSITY)
        if intent.rain_intensity_delta != 0.0:
            self.rain_field.adjust_intensity(intent.rain_intensity_delta)
            if self.rain_field.intensity > 0.0:
                self._set_rain_enabled(True)
        if intent.reset_camera:
            self._reset_camera()

        dt = 1.0 / TARGET_FPS
        previous_rain_time = self.rain_field.elapsed_time
        self.wind_field.update(dt)
        self.light_field.update(dt)
        self.rain_field.update(dt)
        rain_wind = self._rain_wind()
        impacts = (
            self.rain_field.ground_impacts_since(self.world, previous_rain_time, rain_wind)
            if self.environment.is_raining
            else ()
        )
        dry_rate = self.environment.dry_rate_multiplier(self.ground_reactions.wetness)
        self.ground_reactions.update(dt, impacts, dry_rate)
        self.grass_reactions.update(dt)
        self.grass_reactions.apply_impacts(self.grass_field.blades, impacts)
        self.environment.update(dt, self.ground_reactions.wetness)
        self._seed_after_rain_droplets()
        self.rain_enabled = self.environment.is_raining
        self.tip_droplets.update(dt, self.grass_field.blades)
        yaw_delta = self._camera_motion_delta("yaw", intent.yaw_delta)
        pitch_delta = self._camera_motion_delta("pitch", intent.pitch_delta)
        zoom_delta = self._camera_motion_delta("zoom", intent.zoom_delta)
        if self.auto_rotate:
            yaw_delta += AUTO_ROTATE_SPEED * self.tuning.auto_rotate_multiplier
        self.camera.orbit(yaw_delta, pitch_delta)
        self.camera.zoom(zoom_delta)

    def _set_rain_enabled(self, enabled: bool) -> None:
        if enabled:
            self.after_rain_droplets_seeded = False
        self.rain_enabled = enabled
        self.environment.set_rain(enabled, self.ground_reactions.wetness)
        self._seed_after_rain_droplets()

    def _seed_after_rain_droplets(self) -> None:
        if not self.environment.is_after_rain or self.after_rain_droplets_seeded:
            return
        previous_count = self.tip_droplets.active_count
        self.tip_droplets.seed_after_rain(self.ground_reactions.wetness)
        self.after_rain_droplets_seeded = self.tip_droplets.active_count > previous_count

    def _update_menu_input(self, pyxel) -> None:
        if not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        mouse_x, mouse_y = self._mouse_position(pyxel)
        self._handle_menu_click_at(mouse_x, mouse_y)

    def _handle_menu_click_at(self, mouse_x: int, mouse_y: int) -> bool:
        if _point_in_rect(mouse_x, mouse_y, MENU_BUTTON_RECT):
            self.menu_open = not self.menu_open
            return True
        if not self.menu_open:
            return False

        if not _point_in_rect(mouse_x, mouse_y, MENU_PANEL_RECT):
            self.menu_open = False
            return False

        for index, key in enumerate(MENU_SETTING_KEYS):
            minus_rect, plus_rect = self._menu_stepper_rects(index)
            if _point_in_rect(mouse_x, mouse_y, minus_rect):
                self.tuning.adjust_stage(key, -1)
                self._apply_tuning_change(key)
                return True
            if _point_in_rect(mouse_x, mouse_y, plus_rect):
                self.tuning.adjust_stage(key, 1)
                self._apply_tuning_change(key)
                return True
        return True

    def _apply_tuning_change(self, key: str) -> None:
        if key == "rain":
            self.rain_field.set_intensity(self.tuning.rain_intensity)

    def _menu_captures_mouse(self, pyxel) -> bool:
        if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            return False
        mouse_x, mouse_y = self._mouse_position(pyxel)
        return _point_in_rect(mouse_x, mouse_y, MENU_BUTTON_RECT) or (
            self.menu_open and _point_in_rect(mouse_x, mouse_y, MENU_PANEL_RECT)
        )

    def _mouse_position(self, pyxel) -> tuple[int, int]:
        return int(getattr(pyxel, "mouse_x", 0)), int(getattr(pyxel, "mouse_y", 0))

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
        self._draw_menu(pyxel)

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
        self._draw_splashes(pyxel)
        self._draw_grass(pyxel)
        self._draw_tip_droplets(pyxel)
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
        for particle, position in self.light_field.particle_positions()[: self.tuning.photon_count]:
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

        wind = self._rain_wind()
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

    def _draw_splashes(self, pyxel) -> None:
        self.visible_splash_count = 0
        for splash in self.ground_reactions.splashes:
            projected = self.camera.project(splash.position)
            if projected is None:
                continue
            intensity = self._light_intensity_at(splash.position) if self.light_enabled else 0.0
            color = select_splash_color(intensity, splash.normalized_age)
            pyxel.pset(self._screen_int(projected.x), self._screen_int(projected.y), color)
            self.visible_splash_count += 1

    def _draw_tip_droplets(self, pyxel) -> None:
        self.visible_droplet_count = 0
        if not self.light_enabled:
            return

        for droplet in self.tip_droplets.droplets:
            if droplet.blade_index >= self.tuning.grass_count:
                continue
            blade = self.grass_field.blades[droplet.blade_index]
            points = self._sample_current_blade_points(droplet.blade_index, blade)
            position = droplet.position_from_tip(points[-1], blade.height)
            intensity = self._light_intensity_at(position)
            if intensity < TIP_DROPLET_LIGHT_THRESHOLD:
                continue
            projected = self.camera.project(position)
            if projected is None:
                continue
            color = PALETTE_BRIGHT_PARTICLE if intensity > 0.62 else PALETTE_DIM_PARTICLE
            pyxel.pset(self._screen_int(projected.x), self._screen_int(projected.y), color)
            self.visible_droplet_count += 1

    def _draw_grass(self, pyxel) -> None:
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        self.lit_segment_count = 0
        sortable: list[tuple[float, LitGrassPath]] = []
        for blade_index, blade in enumerate(self.grass_field.blades[: self.tuning.grass_count]):
            points = self._sample_current_blade_points(blade_index, blade)
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

    def _sample_current_blade_points(
        self,
        blade_index: int,
        blade: GrassBlade,
    ) -> tuple[Vec3, ...]:
        wind_bend = (
            compute_wind_bend(blade, self._wind_sample(blade.base, blade.phase))
            if self.wind_enabled
            else Vec3(0.0, 0.0, 0.0)
        )
        reaction_bend = self.grass_reactions.bend_for(blade_index)
        return sample_blade_points(blade, GRASS_SEGMENTS, wind_bend + reaction_bend)

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
        intensity = self._light_intensity_at(point) if self.light_enabled else 0.0
        wetness = self.environment.effective_floor_wetness(self.ground_reactions.wetness)
        return select_floor_color(base_color, intensity, wetness)

    def _light_intensity_at(self, point: Vec3) -> float:
        return (
            self.light_field.beam.intensity_at(point)
            * self.light_field.intensity_multiplier
            * self.environment.light_multiplier
        )

    def _rain_wind(self) -> Vec3:
        if not self.wind_enabled:
            return Vec3(0.0, 0.0, 0.0)
        return self._wind_sample(self.world.top_center)

    def _wind_sample(self, position: Vec3, phase: float = 0.0) -> Vec3:
        return self.wind_field.sample(position, phase) * self.tuning.wind_multiplier

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
        pyxel.text(SAFE_LEFT + 8, 36, "LC009 AFTER RAIN", PALETTE_DEBUG_TEXT)
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
            f"{self.environment.phase.value} RAIN {self.rain_field.intensity:.2f} Q/E",
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
        pyxel.text(
            SAFE_LEFT + 8,
            198,
            f"grass {self.tuning.grass_count}/{len(self.grass_field)}",
            PALETTE_DEBUG_TEXT,
        )
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
            f"particles {self.visible_particle_count}/{self.tuning.photon_count}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            270,
            f"rain seg {self.visible_rain_count}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            282,
            f"splash {self.visible_splash_count}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            294,
            f"wet {self.ground_reactions.wetness:.2f}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            306,
            f"react {self.grass_reactions.active_count}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            318,
            f"drops {self.visible_droplet_count}/{self.tip_droplets.active_count}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(SAFE_LEFT + 8, 330, f"wind {self.wind_field.base_speed:.2f}", PALETTE_DEBUG_TEXT)
        pyxel.text(
            SAFE_LEFT + 8,
            342,
            f"gust {self.wind_field.current_gust_strength:.2f}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            354,
            f"cloud {self.light_field.intensity_multiplier:.2f}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8,
            366,
            f"recover {self.environment.light_multiplier:.2f}",
            PALETTE_DEBUG_TEXT,
        )
        pyxel.text(
            SAFE_LEFT + 8, 378, f"time {self.wind_field.elapsed_time:.1f}", PALETTE_DEBUG_TEXT
        )

    def _draw_menu(self, pyxel) -> None:
        button_x, button_y, button_w, button_h = MENU_BUTTON_RECT
        button_fill = PALETTE_GROUND_LIGHT if self.menu_open else PALETTE_BACKGROUND_BAND
        pyxel.rect(button_x, button_y, button_w, button_h, button_fill)
        pyxel.rectb(button_x, button_y, button_w, button_h, PALETTE_BRIGHT_PARTICLE)
        pyxel.text(button_x + 9, button_y + 5, "MENU", PALETTE_BRIGHT_PARTICLE)

        if not self.menu_open:
            return

        panel_x, panel_y, panel_w, panel_h = MENU_PANEL_RECT
        pyxel.rect(panel_x, panel_y, panel_w, panel_h, PALETTE_BACKGROUND)
        pyxel.rectb(panel_x, panel_y, panel_w, panel_h, PALETTE_GROUND_LIGHT)
        pyxel.text(panel_x + 10, panel_y + 8, "OBSERVATION", PALETTE_BRIGHT_PARTICLE)
        pyxel.text(panel_x + panel_w - 42, panel_y + 8, "1-3", PALETTE_DEBUG_TEXT)

        for index, key in enumerate(MENU_SETTING_KEYS):
            row_y = MENU_ROW_TOP + index * MENU_ROW_HEIGHT
            stage = self.tuning.stage_for(key)
            pyxel.text(panel_x + 10, row_y + 2, MENU_ROW_LABELS[key], PALETTE_DEBUG_TEXT)
            minus_rect, plus_rect = self._menu_stepper_rects(index)
            self._draw_menu_step_button(pyxel, minus_rect, "-")
            pyxel.text(panel_x + 126, row_y + 2, str(stage), PALETTE_BRIGHT_PARTICLE)
            self._draw_menu_step_button(pyxel, plus_rect, "+")

    def _draw_menu_step_button(self, pyxel, rect: MenuRect, label: str) -> None:
        x, y, width, height = rect
        pyxel.rect(x, y, width, height, PALETTE_BACKGROUND_BAND)
        pyxel.rectb(x, y, width, height, PALETTE_GROUND_LIGHT)
        pyxel.text(x + 5, y + 4, label, PALETTE_BRIGHT_PARTICLE)

    def _menu_stepper_rects(self, index: int) -> tuple[MenuRect, MenuRect]:
        panel_x, _panel_y, _panel_w, _panel_h = MENU_PANEL_RECT
        row_y = MENU_ROW_TOP + index * MENU_ROW_HEIGHT
        return (
            (panel_x + 104, row_y, 16, 16),
            (panel_x + 142, row_y, 16, 16),
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


def select_floor_color(base_color: int, intensity: float, wetness: float = 0.0) -> int:
    if wetness > 0.68 and intensity <= LIGHT_FLOOR_THRESHOLD_LOW:
        return PALETTE_BACKGROUND_BAND
    if wetness > 0.28 and intensity > LIGHT_FLOOR_THRESHOLD_MEDIUM:
        return PALETTE_GROUND_LIGHT
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


def select_splash_color(intensity: float, normalized_age: float) -> int:
    if normalized_age > 0.72:
        return PALETTE_DIM_PARTICLE
    if intensity > 0.5:
        return PALETTE_BRIGHT_PARTICLE
    return PALETTE_CYLINDER_NEAR_EDGE


def _point_in_rect(x: int, y: int, rect: MenuRect) -> bool:
    rect_x, rect_y, width, height = rect
    return rect_x <= x < rect_x + width and rect_y <= y < rect_y + height
