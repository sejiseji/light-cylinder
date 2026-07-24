from itertools import pairwise
from math import cos, sin, sqrt, tau
from random import Random

from light_cylinder.camera import Camera
from light_cylinder.config import (
    ATMOSPHERIC_DITHER_BASE_DENSITY,
    ATMOSPHERIC_DITHER_HASH_MODULUS,
    ATMOSPHERIC_DITHER_LIGHT_BOOST,
    ATMOSPHERIC_DITHER_PHASE_RATE,
    ATMOSPHERIC_DITHER_SHADOW_REDUCTION,
    ATMOSPHERIC_DITHER_STEP,
    AUTO_ROTATE_PITCH_FOLLOW,
    AUTO_ROTATE_PITCH_SWAY_AMOUNT,
    AUTO_ROTATE_PITCH_SWAY_RATE,
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
    FIREFLY_BRIGHT_THRESHOLD,
    FIREFLY_RING_THRESHOLD,
    FIREFLY_VISIBLE_THRESHOLD,
    FOXTAIL_SEED,
    GRASS_SEED,
    GRASS_SEGMENTS,
    GRASS_WIDTH_MULTIPLIER,
    GROUND_SOIL_MARK_COUNT,
    GROUND_SOIL_MARK_MAX_RADIUS,
    GROUND_SOIL_MARK_MIN_RADIUS,
    GROUND_SOIL_SEED,
    LIGHT_ACCENT_BAND_COUNT,
    LIGHT_ACCENT_BAND_RATE,
    LIGHT_ACCENT_BAND_WIDTHS,
    LIGHT_BAND_ALPHA_PATTERN,
    LIGHT_BAND_COUNT,
    LIGHT_BAND_WIDTH_FACTORS,
    LIGHT_BAND_WIDTH_MAX,
    LIGHT_BAND_WIDTH_MIN,
    LIGHT_BAND_WIDTH_RATE,
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
    PALETTE_GROUND_WET,
    PALETTE_LIT_GRASS,
    PALETTE_NORMAL_GRASS,
    PALETTE_SAFE_AREA,
    PALETTE_STRONGLY_LIT_GRASS,
    PROJECT_TITLE,
    RAIN_BRIGHT_VISIBILITY_THRESHOLD,
    RAIN_DEFAULT_INTENSITY,
    RAIN_DEPTH_COLORS,
    RENDER_HEIGHT,
    RENDER_WIDTH,
    SAFE_LEFT,
    SAFE_RIGHT,
    TARGET_FPS,
    TIP_DROPLET_LIGHT_THRESHOLD,
    UI_TEXT_SCALE,
    WIND_TIME_WRAP_SECONDS,
    validate_display_config,
)
from light_cylinder.environment import EnvironmentState
from light_cylinder.firefly import Firefly, FireflyField
from light_cylinder.foxtail import Foxtail, FoxtailField, FoxtailShape, sample_foxtail_shape
from light_cylinder.grass import GrassBlade, GrassField, compute_wind_bend, sample_blade_points
from light_cylinder.input import MouseInputState, read_control_intent
from light_cylinder.light import LightField, LightParticle
from light_cylinder.math3d import Vec3
from light_cylinder.observation_cycle import ObservationCycle
from light_cylinder.rain import RainField
from light_cylinder.reactions import GrassReactionField, GroundReactionField, TipDropletField
from light_cylinder.tuning import MENU_SETTING_KEYS, ObservationTuning
from light_cylinder.weather import WindField
from light_cylinder.world import CylinderWorld

WorldLine = tuple[Vec3, Vec3, int]
GroundSoilMark = tuple[Vec3, int]
GrassPath = tuple[GrassBlade, tuple[Vec3, ...]]
LitGrassPath = tuple[GrassBlade, tuple[Vec3, ...], tuple[int, int, int]]
LightBandQuad = tuple[int, int, int, int, int, int, int, int, int]
LightBandLine = tuple[int, int, int, int, int]
MenuRect = tuple[int, int, int, int]

MENU_SAFE_RIGHT = COMPOSITION_SAFE_WIDTH - 8
MENU_BUTTON_RECT: MenuRect = (MENU_SAFE_RIGHT - 70, 64, 70, 22)
MENU_PANEL_RECT: MenuRect = (MENU_SAFE_RIGHT - 262, 94, 262, 254)
MENU_ROW_TOP = MENU_PANEL_RECT[1] + 28
MENU_ROW_HEIGHT = 22
MENU_AUTO_ROW_INDEX = 6
MENU_RAIN_TOGGLE_ROW_INDEX = 7
MENU_FIREFLY_TOGGLE_ROW_INDEX = 8
MENU_ZOOM_ROW_INDEX = 9
MENU_ZOOM_STEP = CAMERA_ZOOM_SPEED * 4.0
MENU_ROW_LABELS = {
    "photons": "PHOTON",
    "grass": "GRASS",
    "wind": "WIND",
    "rain": "AMOUNT",
    "rotate": "ROTATE",
    "fireflies": "FIREFLY",
}
PIXEL_FONT = {
    "A": ("111", "101", "111", "101", "101"),
    "B": ("110", "101", "110", "101", "110"),
    "C": ("111", "100", "100", "100", "111"),
    "D": ("110", "101", "101", "101", "110"),
    "E": ("111", "100", "110", "100", "111"),
    "F": ("111", "100", "110", "100", "100"),
    "G": ("111", "100", "101", "101", "111"),
    "H": ("101", "101", "111", "101", "101"),
    "I": ("111", "010", "010", "010", "111"),
    "J": ("001", "001", "001", "101", "111"),
    "K": ("101", "101", "110", "101", "101"),
    "L": ("100", "100", "100", "100", "111"),
    "M": ("101", "111", "111", "101", "101"),
    "N": ("101", "111", "111", "111", "101"),
    "O": ("111", "101", "101", "101", "111"),
    "P": ("111", "101", "111", "100", "100"),
    "Q": ("111", "101", "101", "111", "001"),
    "R": ("110", "101", "110", "101", "101"),
    "S": ("111", "100", "111", "001", "111"),
    "T": ("111", "010", "010", "010", "010"),
    "U": ("101", "101", "101", "101", "111"),
    "V": ("101", "101", "101", "101", "010"),
    "W": ("101", "101", "111", "111", "101"),
    "X": ("101", "101", "010", "101", "101"),
    "Y": ("101", "101", "010", "010", "010"),
    "Z": ("111", "001", "010", "100", "111"),
    "0": ("111", "101", "101", "101", "111"),
    "1": ("010", "110", "010", "010", "111"),
    "2": ("111", "001", "111", "100", "111"),
    "3": ("111", "001", "111", "001", "111"),
    "4": ("101", "101", "111", "001", "001"),
    "5": ("111", "100", "111", "001", "111"),
    "6": ("111", "100", "111", "101", "111"),
    "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"),
    "9": ("111", "101", "111", "001", "111"),
    "-": ("000", "000", "111", "000", "000"),
    "+": ("000", "010", "111", "010", "000"),
    ".": ("000", "000", "000", "000", "010"),
    ":": ("000", "010", "000", "010", "000"),
    "/": ("001", "001", "010", "100", "100"),
    "_": ("000", "000", "000", "000", "111"),
    "@": ("111", "101", "111", "100", "111"),
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
        self.firefly_enabled = False
        self.environment = EnvironmentState()
        self.tuning = ObservationTuning()
        self.observation_cycle = ObservationCycle()
        self.menu_open = False
        self.cylinder_lines = self._build_cylinder_lines()
        self.floor_lines = self._build_floor_lines()
        self.ground_soil_marks = self._build_ground_soil_marks()
        self.axis_lines = self._build_axis_lines()
        self.grass_field = GrassField.generate(
            self.world,
            seed=GRASS_SEED,
            grass_count=self.tuning.max_grass_count,
        )
        self.foxtail_field = FoxtailField.generate(self.world, seed=FOXTAIL_SEED)
        self.wind_field = WindField.create_default()
        self.wind_motion_time = 0.0
        self.light_field = LightField.create_default(
            self.world,
            particle_count=self.tuning.max_photon_count,
        )
        self.rain_field = RainField.create_default(self.world, self.light_field.beam)
        self.rain_field.set_intensity(self.tuning.rain_intensity)
        self.firefly_field = FireflyField.create_default(self.world)
        self.ground_reactions = GroundReactionField()
        self.grass_reactions = GrassReactionField.create(len(self.grass_field.blades))
        self.tip_droplets = TipDropletField.create(
            self.grass_field.blades[: self.tuning.grass_count]
        )
        self.after_rain_droplets_seeded = False
        self.camera_yaw_velocity = 0.0
        self.camera_pitch_velocity = 0.0
        self.camera_zoom_velocity = 0.0
        self.auto_pitch_center = self.camera.pitch
        self.auto_pitch_phase = 0.0
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        self.visible_particle_count = 0
        self.visible_rain_count = 0
        self.visible_splash_count = 0
        self.visible_droplet_count = 0
        self.visible_firefly_count = 0
        self.visible_foxtail_count = 0
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
            self._set_auto_rotate(not self.auto_rotate)
        if intent.toggle_debug:
            self.debug_visible = not self.debug_visible
        if intent.toggle_boundary:
            self.boundary_visible = not self.boundary_visible
        if intent.toggle_wind:
            self.wind_enabled = not self.wind_enabled
        if intent.toggle_light:
            self.light_enabled = not self.light_enabled
        if intent.toggle_firefly:
            self._set_firefly_enabled(not self.firefly_enabled)
        if intent.toggle_observation_cycle:
            self._set_observation_cycle_enabled(not self.observation_cycle.enabled)
        if self.observation_cycle.enabled and (
            intent.toggle_rain or intent.rain_intensity_delta != 0.0
        ):
            self._set_observation_cycle_enabled(False)
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
        self.observation_cycle.update(dt)
        self._apply_observation_cycle()
        previous_rain_time = self.rain_field.elapsed_time
        self.wind_field.update(dt)
        self._update_wind_motion_time(dt)
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
        if self.firefly_enabled:
            firefly_wind = (
                self._wind_sample(self.world.bottom_center)
                if self.wind_enabled
                else Vec3(0.0, 0.0, 0.0)
            )
            self.firefly_field.update(
                dt,
                firefly_wind,
                self.environment.phase.value,
                self.rain_field.intensity if self.environment.is_raining else 0.0,
                self.tuning.firefly_count,
            )
        yaw_delta = self._camera_motion_delta("yaw", intent.yaw_delta)
        pitch_delta = self._camera_motion_delta("pitch", intent.pitch_delta)
        zoom_delta = self._camera_motion_delta("zoom", intent.zoom_delta)
        self._update_auto_pitch_center_from_manual_pitch(pitch_delta)
        if self.auto_rotate:
            yaw_delta += AUTO_ROTATE_SPEED * self.tuning.auto_rotate_multiplier
            pitch_delta += self._auto_rotate_pitch_delta(dt, pitch_delta)
        self.camera.orbit(yaw_delta, pitch_delta)
        self.camera.zoom(zoom_delta)

    def _set_firefly_enabled(self, enabled: bool) -> None:
        self.firefly_enabled = enabled
        if not enabled:
            self.firefly_field.clear()

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

    def _set_observation_cycle_enabled(self, enabled: bool) -> None:
        self.observation_cycle.set_enabled(enabled)
        if not enabled:
            self.rain_field.set_intensity(self.tuning.rain_intensity)

    def _apply_observation_cycle(self) -> None:
        if not self.observation_cycle.enabled:
            return
        sample = self.observation_cycle.sample()
        self.rain_field.set_intensity(self.tuning.rain_intensity * sample.rain_multiplier)
        self._set_rain_enabled(sample.is_raining)

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
        if _point_in_rect(mouse_x, mouse_y, self._menu_auto_toggle_rect()):
            self._set_auto_rotate(not self.auto_rotate)
            return True
        if _point_in_rect(mouse_x, mouse_y, self._menu_rain_toggle_rect()):
            if self.observation_cycle.enabled:
                self._set_observation_cycle_enabled(False)
            self._set_rain_enabled(not self.rain_enabled)
            if self.rain_enabled and self.rain_field.intensity == 0.0:
                self.rain_field.set_intensity(self.tuning.rain_intensity)
            return True
        if _point_in_rect(mouse_x, mouse_y, self._menu_firefly_toggle_rect()):
            self._set_firefly_enabled(not self.firefly_enabled)
            return True
        zoom_in_rect, zoom_out_rect = self._menu_zoom_rects()
        if _point_in_rect(mouse_x, mouse_y, zoom_in_rect):
            self.camera.zoom(-MENU_ZOOM_STEP)
            return True
        if _point_in_rect(mouse_x, mouse_y, zoom_out_rect):
            self.camera.zoom(MENU_ZOOM_STEP)
            return True
        return True

    def _apply_tuning_change(self, key: str) -> None:
        if key == "rain":
            if self.observation_cycle.enabled:
                self._apply_observation_cycle()
            else:
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
        self.auto_pitch_center = self.camera.pitch
        self.auto_pitch_phase = 0.0

    def _set_auto_rotate(self, enabled: bool) -> None:
        if enabled and not self.auto_rotate:
            self.auto_pitch_center = self.camera.pitch
            self.auto_pitch_phase = 0.0
        self.auto_rotate = enabled

    def _update_auto_pitch_center_from_manual_pitch(self, pitch_delta: float) -> None:
        if pitch_delta == 0.0:
            return
        self.auto_pitch_center = self.camera.clamp_pitch(self.camera.pitch + pitch_delta)

    def _auto_rotate_pitch_delta(self, dt: float, pending_pitch_delta: float) -> float:
        self.auto_pitch_phase += dt * AUTO_ROTATE_PITCH_SWAY_RATE
        target_pitch = self.camera.clamp_pitch(
            self.auto_pitch_center + sin(self.auto_pitch_phase) * AUTO_ROTATE_PITCH_SWAY_AMOUNT
        )
        predicted_pitch = self.camera.clamp_pitch(self.camera.pitch + pending_pitch_delta)
        return (target_pitch - predicted_pitch) * AUTO_ROTATE_PITCH_FOLLOW

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
        axis = self._light_axis_screen_points()
        phase = int(self.light_field.elapsed_time * ATMOSPHERIC_DITHER_PHASE_RATE)
        cloud_shadow = max(
            self.environment.cloud_shadow,
            1.0 - self.observation_cycle.sample().light_multiplier,
        )
        for y in range(0, RENDER_HEIGHT, ATMOSPHERIC_DITHER_STEP):
            for x in range(SAFE_LEFT, SAFE_RIGHT, ATMOSPHERIC_DITHER_STEP):
                light_factor = atmospheric_light_factor(x, y, axis)
                density = atmospheric_dither_density(x, y, light_factor, cloud_shadow)
                if atmospheric_dither_visible(x, y, phase, density):
                    pyxel.pset(x + phase % 2, y, PALETTE_BACKGROUND_BAND)

    def _light_axis_screen_points(self) -> tuple[tuple[float, float], tuple[float, float]] | None:
        if not self.light_enabled:
            return None
        beam = self.light_field.beam
        start = self.camera.project(beam.axis_point_at(0.08))
        end = self.camera.project(beam.axis_point_at(0.92))
        if start is None or end is None:
            return None
        return ((start.x, start.y), (end.x, end.y))

    def _draw_cylinder_scene(self, pyxel) -> None:
        self._draw_ground_soil(pyxel)
        if self.boundary_visible:
            self._draw_floor(pyxel)
            self._draw_depth_sorted_lines(pyxel, self.cylinder_lines)
        self._draw_rain(pyxel)
        self._draw_splashes(pyxel)
        self._draw_grass_and_light_bands(pyxel)
        self._draw_tip_droplets(pyxel)
        self._draw_ground_sparks(pyxel)
        if self.debug_visible:
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

    def _draw_ground_soil(self, pyxel) -> None:
        sortable: list[tuple[float, GroundSoilMark]] = []
        for mark in self.ground_soil_marks:
            point, _width = mark
            sortable.append((self.camera.world_to_camera(point).z, mark))

        for _depth, (point, width) in sorted(sortable, key=lambda item: item[0], reverse=True):
            projected = self.camera.project(point)
            if projected is None:
                continue
            x = self._screen_int(projected.x)
            y = self._screen_int(projected.y)
            color = self._floor_color(point, PALETTE_GROUND_SHADOW)
            pyxel.pset(x, y, color)
            if width > 1:
                pyxel.pset(x + 1, y, color)

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

    def _light_band_quads(self) -> tuple[tuple[float, LightBandQuad], ...]:
        if not self.light_enabled:
            return ()

        beam = self.light_field.beam
        basis_u, basis_v = beam.basis()
        color = PALETTE_DIM_PARTICLE if LIGHT_BAND_ALPHA_PATTERN == 1 else PALETTE_GROUND_LIGHT
        quads: list[tuple[float, LightBandQuad]] = []
        for index in range(LIGHT_BAND_COUNT):
            phase = self.light_field.elapsed_time * LIGHT_BAND_WIDTH_RATE + index * 1.73
            pulse = (1.0 + sin(phase)) * 0.5
            angle = tau * index / LIGHT_BAND_COUNT + sin(phase * 0.71) * 0.28
            lateral = basis_u * cos(angle) + basis_v * sin(angle)
            drift = basis_u * cos(angle + tau / 4.0) + basis_v * sin(angle + tau / 4.0)
            centered_index = index - (LIGHT_BAND_COUNT - 1) * 0.5
            spread = centered_index * 13.0
            width = (
                LIGHT_BAND_WIDTH_MIN + (LIGHT_BAND_WIDTH_MAX - LIGHT_BAND_WIDTH_MIN) * pulse
            ) * LIGHT_BAND_WIDTH_FACTORS[index]
            top = (
                beam.axis_point_at(0.03 + 0.018 * (index % 3))
                + drift * (spread * 0.42 + sin(phase * 0.43) * 5.0)
                + lateral * sin(phase * 0.31) * 3.0
            )
            bottom = (
                beam.axis_point_at(0.9 - 0.018 * (index % 2))
                + drift * (spread * 1.28 + sin(phase * 0.37 + 1.1) * 9.0)
                - lateral * sin(phase * 0.29 + 0.8) * 5.0
            )
            points = (
                self.camera.project(top - lateral * (width * 0.18)),
                self.camera.project(top + lateral * (width * 0.18)),
                self.camera.project(bottom + lateral * width),
                self.camera.project(bottom - lateral * width),
            )
            if any(point is None for point in points):
                continue

            projected = [point for point in points if point is not None]
            midpoint = (top + bottom) * 0.5
            depth = self.camera.world_to_camera(midpoint).z
            x1, y1 = self._screen_int(projected[0].x), self._screen_int(projected[0].y)
            x2, y2 = self._screen_int(projected[1].x), self._screen_int(projected[1].y)
            x3, y3 = self._screen_int(projected[2].x), self._screen_int(projected[2].y)
            x4, y4 = self._screen_int(projected[3].x), self._screen_int(projected[3].y)
            quads.append((depth, (x1, y1, x2, y2, x3, y3, x4, y4, color)))
        return tuple(quads)

    def _light_accent_bands(self) -> tuple[tuple[float, str, object], ...]:
        if not self.light_enabled:
            return ()

        beam = self.light_field.beam
        basis_u, basis_v = beam.basis()
        accents: list[tuple[float, str, object]] = []
        for index in range(LIGHT_ACCENT_BAND_COUNT):
            phase = self.light_field.elapsed_time * LIGHT_ACCENT_BAND_RATE + index * 2.11
            angle = tau * (index + 0.35) / LIGHT_ACCENT_BAND_COUNT + sin(phase * 0.91) * 0.34
            lateral = basis_u * cos(angle) + basis_v * sin(angle)
            drift = basis_u * cos(angle + tau / 4.0) + basis_v * sin(angle + tau / 4.0)
            spread = (index - (LIGHT_ACCENT_BAND_COUNT - 1) * 0.5) * 17.0
            top = (
                beam.axis_point_at(0.02 + 0.025 * index)
                + drift * (spread * 0.48 + sin(phase * 0.53) * 7.0)
                + lateral * sin(phase * 0.77) * 3.5
            )
            bottom = (
                beam.axis_point_at(0.92 - 0.03 * (index % 2))
                + drift * (spread * 1.34 + sin(phase * 0.61 + 0.9) * 10.0)
                - lateral * sin(phase * 0.69 + 1.2) * 5.5
            )
            midpoint = (top + bottom) * 0.5
            depth = self.camera.world_to_camera(midpoint).z
            color = PALETTE_GROUND_STRONG_LIGHT
            width = LIGHT_ACCENT_BAND_WIDTHS[index]
            if index in (0, 2):
                start = self.camera.project(top)
                end = self.camera.project(bottom)
                if start is None or end is None:
                    continue
                accents.append(
                    (
                        depth,
                        "accent_line",
                        (
                            self._screen_int(start.x),
                            self._screen_int(start.y),
                            self._screen_int(end.x),
                            self._screen_int(end.y),
                            color,
                        ),
                    )
                )
                continue

            points = (
                self.camera.project(top - lateral * (width * 0.22)),
                self.camera.project(top + lateral * (width * 0.22)),
                self.camera.project(bottom + lateral * width),
                self.camera.project(bottom - lateral * width),
            )
            if any(point is None for point in points):
                continue

            projected = [point for point in points if point is not None]
            accents.append(
                (
                    depth,
                    "accent_band",
                    (
                        self._screen_int(projected[0].x),
                        self._screen_int(projected[0].y),
                        self._screen_int(projected[1].x),
                        self._screen_int(projected[1].y),
                        self._screen_int(projected[2].x),
                        self._screen_int(projected[2].y),
                        self._screen_int(projected[3].x),
                        self._screen_int(projected[3].y),
                        color,
                    ),
                )
            )
        return tuple(accents)

    def _draw_light_band_quad(self, pyxel, quad: LightBandQuad) -> None:
        x1, y1, x2, y2, x3, y3, x4, y4, color = quad
        pyxel.tri(x1, y1, x2, y2, x3, y3, color)
        pyxel.tri(x1, y1, x3, y3, x4, y4, color)

    def _draw_light_band_line(self, pyxel, line: LightBandLine) -> None:
        x1, y1, x2, y2, color = line
        pyxel.line(x1, y1, x2, y2, color)

    def _draw_light_particles(self, pyxel) -> None:
        self.visible_particle_count = 0
        for _depth, particle, position in sorted(
            self._light_particle_items(),
            key=lambda item: item[0],
            reverse=True,
        ):
            self._draw_light_particle(pyxel, particle, position)

    def _light_particle_items(self) -> tuple[tuple[float, LightParticle, Vec3], ...]:
        if not self.light_enabled:
            return ()

        items: list[tuple[float, LightParticle, Vec3]] = []
        for particle, position in self.light_field.particle_positions()[: self.tuning.photon_count]:
            depth = self.camera.world_to_camera(position).z
            items.append((depth, particle, position))
        return tuple(items)

    def _draw_light_particle(self, pyxel, particle: LightParticle, position: Vec3) -> bool:
        intensity = self._light_intensity_at(position) * particle.brightness
        if intensity < LIGHT_PARTICLE_VISIBILITY_THRESHOLD:
            return False
        projected = self.camera.project(position)
        if projected is None:
            return False

        color = select_particle_color(intensity)
        x = self._screen_int(projected.x)
        y = self._screen_int(projected.y)
        radius = particle_draw_radius(particle.size, intensity)
        if radius >= 2:
            pyxel.circ(x, y, radius, color)
            if intensity > 0.76:
                pyxel.pset(x, y, PALETTE_BRIGHT_PARTICLE)
        elif radius == 1:
            pyxel.circ(x, y, 1, color)
        else:
            pyxel.pset(x, y, color)
        self.visible_particle_count += 1
        return True

    def _draw_rain(self, pyxel) -> None:
        self.visible_rain_count = 0
        if not self.rain_enabled:
            return

        wind = self._rain_wind()
        sortable: list[tuple[float, Vec3, Vec3, int]] = []
        for drop, start, end in self.rain_field.segments(self.world, wind):
            midpoint = (start + end) * 0.5
            depth = self.camera.world_to_camera(midpoint).z
            color = select_rain_color(drop.brightness, self._rain_depth_tier(depth))
            sortable.append((depth, start, end, color))
        for streak, start, end in self.rain_field.static_segments(self.world):
            midpoint = (start + end) * 0.5
            depth = self.camera.world_to_camera(midpoint).z
            color = select_rain_color(streak.brightness, self._rain_depth_tier(depth))
            sortable.append((depth, start, end, color))

        for _depth, start, end, color in sorted(sortable, key=lambda item: item[0], reverse=True):
            if self._draw_vertical_rain_line(pyxel, start, end, color):
                self.visible_rain_count += 1

    def _draw_vertical_rain_line(self, pyxel, start: Vec3, end: Vec3, color: int) -> bool:
        projected_start = self.camera.project(start)
        projected_end = self.camera.project(end)
        if projected_start is None or projected_end is None:
            return False

        x = self._screen_int(projected_start.x)
        y1 = self._screen_int(projected_start.y)
        y2 = self._screen_int(projected_end.y)
        pyxel.line(x, min(y1, y2), x, max(y1, y2), color)
        return True

    def _rain_depth_tier(self, depth: float) -> int:
        if depth > self.camera.distance + 96.0:
            return 0
        if depth > self.camera.distance + 24.0:
            return 1
        if depth > self.camera.distance - 56.0:
            return 2
        return 3

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

    def _draw_grass_and_light_bands(self, pyxel) -> None:
        self.visible_blade_count = 0
        self.visible_segment_count = 0
        self.lit_segment_count = 0
        self.visible_particle_count = 0
        self.visible_firefly_count = 0
        self.visible_foxtail_count = 0
        sortable: list[tuple[float, str, object]] = [
            (depth, "band", quad) for depth, quad in self._light_band_quads()
        ]
        sortable.extend(self._light_accent_bands())
        sortable.extend(
            (depth, "particle", (particle, position))
            for depth, particle, position in self._light_particle_items()
        )
        sortable.extend((depth, "firefly", firefly) for depth, firefly in self._firefly_items())
        sortable.extend(
            (depth, "foxtail", (foxtail, shape)) for depth, foxtail, shape in self._foxtail_items()
        )
        for blade_index, blade in enumerate(self.grass_field.blades[: self.tuning.grass_count]):
            points = self._sample_current_blade_points(blade_index, blade)
            midpoint = points[len(points) // 2]
            depth = self.camera.world_to_camera(midpoint).z
            base_color = self._grass_color(blade, depth)
            light_colors = self._grass_light_colors(points, base_color)
            sortable.append((depth, "grass", (blade, points, light_colors)))

        for _depth, kind, payload in sorted(
            sortable,
            key=lambda item: item[0],
            reverse=True,
        ):
            if kind in ("band", "accent_band"):
                self._draw_light_band_quad(pyxel, payload)
                continue
            if kind == "accent_line":
                self._draw_light_band_line(pyxel, payload)
                continue
            if kind == "particle":
                particle, position = payload
                self._draw_light_particle(pyxel, particle, position)
                continue
            if kind == "firefly":
                self._draw_firefly(pyxel, payload)
                continue
            if kind == "foxtail":
                foxtail, shape = payload
                self._draw_foxtail(pyxel, foxtail, shape)
                continue

            blade, points, light_colors = payload
            blade_visible = False
            segment_count = len(points) - 1
            self._draw_soil_anchor(pyxel, points[0])
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

    def _foxtail_items(self) -> tuple[tuple[float, Foxtail, FoxtailShape], ...]:
        items: list[tuple[float, Foxtail, FoxtailShape]] = []
        rain_weight = 1.0 if self.environment.is_raining else 0.0
        after_rain_weight = (
            self.environment.effective_floor_wetness(self.ground_reactions.wetness)
            if self.environment.is_after_rain
            else 0.0
        )
        for foxtail in self.foxtail_field.foxtails:
            wind = (
                self._wind_sample(foxtail.base, foxtail.phase)
                if self.wind_enabled
                else Vec3(0, 0, 0)
            )
            shape = sample_foxtail_shape(foxtail, wind, rain_weight, after_rain_weight)
            depth = self.camera.world_to_camera(shape.stem_points[-1]).z
            items.append((depth, foxtail, shape))
        return tuple(items)

    def _draw_foxtail(self, pyxel, foxtail: Foxtail, shape: FoxtailShape) -> None:
        visible = False
        self._draw_soil_anchor(pyxel, shape.stem_points[0])
        for start, end in pairwise(shape.stem_points):
            midpoint = (start + end) * 0.5
            if self._draw_world_line(pyxel, start, end, self._foxtail_stem_color(midpoint)):
                visible = True
        for segment_index, (start, end) in enumerate(pairwise(shape.head_points)):
            midpoint = (start + end) * 0.5
            color = self._foxtail_head_color(midpoint)
            if self._draw_world_line(pyxel, start, end, color):
                visible = True
            self._draw_foxtail_bristles(pyxel, end, segment_index, color)
        for droplet in shape.droplet_points:
            self._draw_foxtail_droplet(pyxel, droplet)
        if visible:
            self.visible_foxtail_count += 1

    def _draw_foxtail_bristles(self, pyxel, point: Vec3, index: int, color: int) -> None:
        projected = self.camera.project(point)
        if projected is None:
            return
        x = self._screen_int(projected.x)
        y = self._screen_int(projected.y)
        offset = 1 + index % 2
        pyxel.pset(x, y, color)
        pyxel.pset(x + offset, y, color)
        pyxel.pset(x - offset, y, color)
        if index % 3 == 0:
            pyxel.pset(x, y - 1, color)

    def _draw_foxtail_droplet(self, pyxel, point: Vec3) -> bool:
        intensity = self._light_intensity_at(point) if self.light_enabled else 0.0
        if intensity < 0.16:
            return False
        projected = self.camera.project(point)
        if projected is None:
            return False
        color = PALETTE_BRIGHT_PARTICLE if intensity > 0.54 else PALETTE_DIM_PARTICLE
        pyxel.pset(self._screen_int(projected.x), self._screen_int(projected.y), color)
        return True

    def _foxtail_stem_color(self, point: Vec3) -> int:
        intensity = self._light_intensity_at(point) if self.light_enabled else 0.0
        if intensity > 0.42:
            return PALETTE_STRONGLY_LIT_GRASS
        return PALETTE_NORMAL_GRASS

    def _foxtail_head_color(self, point: Vec3) -> int:
        intensity = self._light_intensity_at(point) if self.light_enabled else 0.0
        if intensity > 0.36:
            return PALETTE_STRONGLY_LIT_GRASS
        return PALETTE_NORMAL_GRASS

    def _firefly_items(self) -> tuple[tuple[float, Firefly], ...]:
        if not self.firefly_enabled:
            return ()
        return tuple(
            (self.camera.world_to_camera(firefly.position).z, firefly)
            for firefly in self.firefly_field.active_fireflies()
        )

    def _draw_firefly(self, pyxel, firefly: Firefly) -> bool:
        glow = firefly.glow()
        if self.light_enabled:
            glow = min(1.0, glow + self._light_intensity_at(firefly.position) * 0.12)
        if glow < FIREFLY_VISIBLE_THRESHOLD:
            return False

        projected = self.camera.project(firefly.position)
        if projected is None:
            return False

        x = self._screen_int(projected.x)
        y = self._screen_int(projected.y)
        depth = self.camera.world_to_camera(firefly.position).z
        radius = firefly_draw_radius(depth, self.camera.distance, glow)
        center_color = (
            PALETTE_GROUND_STRONG_LIGHT
            if glow >= FIREFLY_BRIGHT_THRESHOLD
            else PALETTE_GROUND_LIGHT
        )
        if radius >= 2:
            pyxel.circ(x, y, radius, PALETTE_GROUND_LIGHT)
        elif glow >= FIREFLY_BRIGHT_THRESHOLD:
            for offset_x, offset_y in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                pyxel.pset(x + offset_x, y + offset_y, PALETTE_GROUND_LIGHT)
        if glow >= FIREFLY_RING_THRESHOLD:
            pyxel.circb(x, y, min(4, radius + 1), PALETTE_GROUND_STRONG_LIGHT)
        pyxel.pset(x, y, center_color)
        self.visible_firefly_count += 1
        return True

    def _draw_soil_anchor(self, pyxel, point: Vec3) -> bool:
        projected = self.camera.project(point)
        if projected is None:
            return False
        color = self._floor_color(point, PALETTE_GROUND_SHADOW)
        x = self._screen_int(projected.x)
        y = self._screen_int(projected.y)
        pyxel.pset(x, y, color)
        pyxel.pset(x + 1, y, color)
        return True

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
        width = int(round((1 + width_class) * root_weight * GRASS_WIDTH_MULTIPLIER))
        if width <= 1:
            return ()

        dx = x2 - x1
        dy = y2 - y1
        perpendicular = (0, 1) if abs(dx) > abs(dy) else (1, 0)

        offsets: list[tuple[int, int]] = []
        half_width = width // 2
        for amount in range(1, half_width + 1):
            offsets.append((perpendicular[0] * amount, perpendicular[1] * amount))
            offsets.append((-perpendicular[0] * amount, -perpendicular[1] * amount))
        return tuple(offsets)

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
            * self.observation_cycle.sample().light_multiplier
        )

    def _rain_wind(self) -> Vec3:
        return Vec3(0.0, 0.0, 0.0)

    def _update_wind_motion_time(self, dt: float) -> None:
        self.wind_motion_time = (
            self.wind_motion_time + dt * self.tuning.wind_speed_multiplier
        ) % WIND_TIME_WRAP_SECONDS

    def _wind_sample(self, position: Vec3, phase: float = 0.0) -> Vec3:
        return self.wind_field.amplified_sample(
            position,
            phase,
            self.tuning.wind_multiplier,
            self.wind_motion_time,
        )

    def _draw_reference_points(self, pyxel) -> None:
        origin = self.world.bottom_center
        projected_origin = self.camera.project(origin)
        if projected_origin is not None:
            pyxel.circ(int(projected_origin.x), int(projected_origin.y), 3, PALETTE_DEBUG_TEXT)
            self._draw_text(
                pyxel,
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
                self._draw_text(pyxel, int(projected.x) + 4, int(projected.y) - 3, label, color)

    def _draw_debug(self, pyxel) -> None:
        if not self.debug_visible:
            return

        center_x = RENDER_WIDTH // 2
        center_y = RENDER_HEIGHT // 2
        pyxel.rectb(0, 0, RENDER_WIDTH, RENDER_HEIGHT, PALETTE_DEBUG_FRAME)
        pyxel.line(center_x, 0, center_x, RENDER_HEIGHT - 1, PALETTE_DEBUG_ACCENT)
        pyxel.line(0, center_y, RENDER_WIDTH - 1, center_y, PALETTE_DEBUG_ACCENT)
        pyxel.rectb(SAFE_LEFT, 0, COMPOSITION_SAFE_WIDTH, RENDER_HEIGHT, PALETTE_SAFE_AREA)
        pyxel.line(SAFE_LEFT, 0, SAFE_LEFT, RENDER_HEIGHT - 1, PALETTE_DISTANT_GRASS)
        pyxel.line(SAFE_RIGHT - 1, 0, SAFE_RIGHT - 1, RENDER_HEIGHT - 1, PALETTE_DISTANT_GRASS)
        cycle_sample = self.observation_cycle.sample()
        left_x = SAFE_LEFT + 8
        right_x = SAFE_LEFT + 202
        line = UI_TEXT_SCALE * 6
        right_y = 12 + line * 2
        rows = (
            (left_x, 12, DISPLAY_TITLE_EN, PALETTE_BRIGHT_PARTICLE),
            (left_x, 12 + line, "LC010 VIEW", PALETTE_DEBUG_TEXT),
            (
                left_x,
                12 + line * 2,
                f"AUTO {'ON' if self.auto_rotate else 'OFF'}",
                PALETTE_LIT_GRASS,
            ),
            (
                left_x,
                12 + line * 3,
                f"WIND {'ON' if self.wind_enabled else 'OFF'}",
                PALETTE_LIT_GRASS,
            ),
            (
                left_x,
                12 + line * 4,
                f"LIGHT {'ON' if self.light_enabled else 'OFF'}",
                PALETTE_LIT_GRASS,
            ),
            (left_x, 12 + line * 5, f"RAIN {self.rain_field.intensity:.2f}", PALETTE_LIT_GRASS),
            (
                left_x,
                12 + line * 6,
                f"CYCLE {'ON' if self.observation_cycle.enabled else 'OFF'}",
                PALETTE_LIT_GRASS,
            ),
            (left_x, 12 + line * 7, cycle_sample.phase.value, PALETTE_LIT_GRASS),
            (
                left_x,
                12 + line * 8,
                f"FF {'ON' if self.firefly_enabled else 'OFF'}",
                PALETTE_LIT_GRASS,
            ),
            (left_x, 12 + line * 9, f"YAW {self.camera.yaw:.2f}", PALETTE_DEBUG_TEXT),
            (left_x, 12 + line * 10, f"PITCH {self.camera.pitch:.2f}", PALETTE_DEBUG_TEXT),
            (right_x, right_y, f"GRASS {self.visible_blade_count}", PALETTE_DEBUG_TEXT),
            (right_x, right_y + line, f"LIT {self.lit_segment_count}", PALETTE_DEBUG_TEXT),
            (right_x, right_y + line * 2, f"PT {self.visible_particle_count}", PALETTE_DEBUG_TEXT),
            (right_x, right_y + line * 3, f"RAIN {self.visible_rain_count}", PALETTE_DEBUG_TEXT),
            (right_x, right_y + line * 4, f"FOX {self.visible_foxtail_count}", PALETTE_DEBUG_TEXT),
            (
                right_x,
                right_y + line * 5,
                f"WET {self.ground_reactions.wetness:.2f}",
                PALETTE_DEBUG_TEXT,
            ),
            (right_x, right_y + line * 6, f"DROP {self.visible_droplet_count}", PALETTE_DEBUG_TEXT),
            (
                right_x,
                right_y + line * 7,
                f"FF {self.visible_firefly_count}",
                PALETTE_DEBUG_TEXT,
            ),
            (
                right_x,
                right_y + line * 8,
                f"GUST {self.wind_field.current_gust_strength:.2f}",
                PALETTE_DEBUG_TEXT,
            ),
            (
                right_x,
                right_y + line * 9,
                f"TIME {self.wind_field.elapsed_time:.1f}",
                PALETTE_DEBUG_TEXT,
            ),
        )
        for x, y, text, color in rows:
            self._draw_text(pyxel, x, y, text, color)

    def _draw_menu(self, pyxel) -> None:
        button_x, button_y, button_w, button_h = MENU_BUTTON_RECT
        button_fill = PALETTE_GROUND_LIGHT if self.menu_open else PALETTE_BACKGROUND_BAND
        pyxel.rect(button_x, button_y, button_w, button_h, button_fill)
        pyxel.rectb(button_x, button_y, button_w, button_h, PALETTE_BRIGHT_PARTICLE)
        self._draw_text(pyxel, button_x + 8, button_y + 4, "MENU", PALETTE_BRIGHT_PARTICLE)

        if not self.menu_open:
            return

        panel_x, panel_y, panel_w, panel_h = MENU_PANEL_RECT
        pyxel.rect(panel_x, panel_y, panel_w, panel_h, PALETTE_BACKGROUND)
        pyxel.rectb(panel_x, panel_y, panel_w, panel_h, PALETTE_GROUND_LIGHT)
        self._draw_text(pyxel, panel_x + 10, panel_y + 8, "OBSERVATION", PALETTE_BRIGHT_PARTICLE)
        self._draw_text(pyxel, panel_x + panel_w - 46, panel_y + 8, "1-3", PALETTE_DEBUG_TEXT)

        for index, key in enumerate(MENU_SETTING_KEYS):
            row_y = MENU_ROW_TOP + index * MENU_ROW_HEIGHT
            stage = self.tuning.stage_for(key)
            self._draw_text(
                pyxel, panel_x + 10, row_y + 2, MENU_ROW_LABELS[key], PALETTE_DEBUG_TEXT
            )
            minus_rect, plus_rect = self._menu_stepper_rects(index)
            self._draw_menu_step_button(pyxel, minus_rect, "-")
            self._draw_text(pyxel, panel_x + 172, row_y + 2, str(stage), PALETTE_BRIGHT_PARTICLE)
            self._draw_menu_step_button(pyxel, plus_rect, "+")
        auto_y = MENU_ROW_TOP + MENU_AUTO_ROW_INDEX * MENU_ROW_HEIGHT
        self._draw_text(pyxel, panel_x + 10, auto_y + 2, "AUTO", PALETTE_DEBUG_TEXT)
        self._draw_menu_toggle_button(
            pyxel,
            self._menu_auto_toggle_rect(),
            self.auto_rotate,
            "ON" if self.auto_rotate else "OFF",
        )
        rain_y = MENU_ROW_TOP + MENU_RAIN_TOGGLE_ROW_INDEX * MENU_ROW_HEIGHT
        self._draw_text(pyxel, panel_x + 10, rain_y + 2, "RAIN", PALETTE_DEBUG_TEXT)
        self._draw_menu_toggle_button(
            pyxel,
            self._menu_rain_toggle_rect(),
            self.rain_enabled,
            "ON" if self.rain_enabled else "OFF",
        )
        firefly_y = MENU_ROW_TOP + MENU_FIREFLY_TOGGLE_ROW_INDEX * MENU_ROW_HEIGHT
        self._draw_text(pyxel, panel_x + 10, firefly_y + 2, "FIREFLY", PALETTE_DEBUG_TEXT)
        self._draw_menu_toggle_button(
            pyxel,
            self._menu_firefly_toggle_rect(),
            self.firefly_enabled,
            "ON" if self.firefly_enabled else "OFF",
        )
        zoom_y = MENU_ROW_TOP + MENU_ZOOM_ROW_INDEX * MENU_ROW_HEIGHT
        self._draw_text(pyxel, panel_x + 10, zoom_y + 2, "ZOOM", PALETTE_DEBUG_TEXT)
        zoom_in_rect, zoom_out_rect = self._menu_zoom_rects()
        self._draw_menu_step_button(pyxel, zoom_in_rect, "IN")
        self._draw_menu_step_button(pyxel, zoom_out_rect, "OUT")

    def _draw_menu_step_button(self, pyxel, rect: MenuRect, label: str) -> None:
        x, y, width, height = rect
        pyxel.rect(x, y, width, height, PALETTE_BACKGROUND_BAND)
        pyxel.rectb(x, y, width, height, PALETTE_GROUND_LIGHT)
        self._draw_text(pyxel, x + 4, y + 4, label, PALETTE_BRIGHT_PARTICLE)

    def _draw_menu_toggle_button(self, pyxel, rect: MenuRect, enabled: bool, label: str) -> None:
        x, y, width, height = rect
        fill = PALETTE_GROUND_LIGHT if enabled else PALETTE_BACKGROUND_BAND
        pyxel.rect(x, y, width, height, fill)
        pyxel.rectb(x, y, width, height, PALETTE_GROUND_LIGHT)
        self._draw_text(pyxel, x + 10, y + 4, label, PALETTE_BRIGHT_PARTICLE)

    def _menu_stepper_rects(self, index: int) -> tuple[MenuRect, MenuRect]:
        panel_x, _panel_y, _panel_w, _panel_h = MENU_PANEL_RECT
        row_y = MENU_ROW_TOP + index * MENU_ROW_HEIGHT
        return (
            (panel_x + 132, row_y, 20, 20),
            (panel_x + 204, row_y, 20, 20),
        )

    def _menu_auto_toggle_rect(self) -> MenuRect:
        panel_x, _panel_y, _panel_w, _panel_h = MENU_PANEL_RECT
        row_y = MENU_ROW_TOP + MENU_AUTO_ROW_INDEX * MENU_ROW_HEIGHT
        return (panel_x + 132, row_y, 92, 20)

    def _menu_rain_toggle_rect(self) -> MenuRect:
        panel_x, _panel_y, _panel_w, _panel_h = MENU_PANEL_RECT
        row_y = MENU_ROW_TOP + MENU_RAIN_TOGGLE_ROW_INDEX * MENU_ROW_HEIGHT
        return (panel_x + 132, row_y, 92, 20)

    def _menu_firefly_toggle_rect(self) -> MenuRect:
        panel_x, _panel_y, _panel_w, _panel_h = MENU_PANEL_RECT
        row_y = MENU_ROW_TOP + MENU_FIREFLY_TOGGLE_ROW_INDEX * MENU_ROW_HEIGHT
        return (panel_x + 132, row_y, 92, 20)

    def _menu_zoom_rects(self) -> tuple[MenuRect, MenuRect]:
        panel_x, _panel_y, _panel_w, _panel_h = MENU_PANEL_RECT
        row_y = MENU_ROW_TOP + MENU_ZOOM_ROW_INDEX * MENU_ROW_HEIGHT
        return (
            (panel_x + 132, row_y, 44, 20),
            (panel_x + 180, row_y, 44, 20),
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

    def _build_ground_soil_marks(self) -> tuple[GroundSoilMark, ...]:
        rng = Random(GROUND_SOIL_SEED)
        marks: list[GroundSoilMark] = []
        radius_span = GROUND_SOIL_MARK_MAX_RADIUS - GROUND_SOIL_MARK_MIN_RADIUS
        for _index in range(GROUND_SOIL_MARK_COUNT):
            radius = GROUND_SOIL_MARK_MIN_RADIUS + radius_span * rng.random()
            point = self.world.sample_bottom_point(radius * radius, rng.random())
            width = 2 if rng.random() > 0.78 else 1
            marks.append((point, width))
        return tuple(marks)

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

    def _draw_text(self, pyxel, x: int, y: int, text: str, color: int) -> None:
        cursor_x = x
        for char in text.upper():
            if char == " ":
                cursor_x += UI_TEXT_SCALE * 2
                continue
            glyph = PIXEL_FONT.get(char)
            if glyph is None:
                cursor_x += UI_TEXT_SCALE * 4
                continue
            for row, pattern in enumerate(glyph):
                for col, pixel in enumerate(pattern):
                    if pixel == "1":
                        pyxel.rect(
                            cursor_x + col * UI_TEXT_SCALE,
                            y + row * UI_TEXT_SCALE,
                            UI_TEXT_SCALE,
                            UI_TEXT_SCALE,
                            color,
                        )
            cursor_x += UI_TEXT_SCALE * 4


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
        return PALETTE_GROUND_WET
    if wetness > 0.28 and intensity > LIGHT_FLOOR_THRESHOLD_MEDIUM:
        return PALETTE_GROUND_LIGHT
    if intensity > LIGHT_FLOOR_THRESHOLD_HIGH:
        return PALETTE_GROUND_STRONG_LIGHT
    if intensity > LIGHT_FLOOR_THRESHOLD_MEDIUM:
        return PALETTE_GROUND_LIGHT
    if intensity > LIGHT_FLOOR_THRESHOLD_LOW:
        return PALETTE_GROUND_LIGHT
    return base_color


def select_particle_color(intensity: float) -> int:
    if intensity > 0.72:
        return PALETTE_BRIGHT_PARTICLE
    if intensity > 0.48:
        return PALETTE_LIT_GRASS
    return PALETTE_DIM_PARTICLE


def particle_draw_radius(size: float, intensity: float) -> int:
    score = size * 0.72 + intensity * 0.28
    if score > 0.93:
        return 3
    if score > 0.76:
        return 2
    if score > 0.44:
        return 1
    return 0


def firefly_draw_radius(depth: float, camera_distance: float, glow: float) -> int:
    if glow < FIREFLY_VISIBLE_THRESHOLD:
        return 0
    radius = 2
    if glow >= FIREFLY_RING_THRESHOLD:
        radius += 1
    if depth < camera_distance - 48.0:
        radius += 1
    if depth < camera_distance - 120.0:
        radius += 1
    return min(4, radius)


def atmospheric_dither_density(
    x: int,
    y: int,
    light_factor: float = 0.0,
    cloud_shadow: float = 0.0,
) -> float:
    center_x = (SAFE_LEFT + SAFE_RIGHT) * 0.5
    half_width = COMPOSITION_SAFE_WIDTH * 0.5
    distance_from_center = min(1.0, abs(x - center_x) / half_width)
    center_density = 1.0 - distance_from_center * distance_from_center

    height = y / max(1, RENDER_HEIGHT - 1)
    mid_air = max(0.0, 1.0 - abs(height - 0.42) / 0.34)
    grass_suppression = 0.35 if height > 0.68 else 1.0
    top_suppression = 0.55 if height < 0.08 else 1.0
    shadow = 1.0 - ATMOSPHERIC_DITHER_SHADOW_REDUCTION * max(0.0, min(1.0, cloud_shadow))
    density = (
        ATMOSPHERIC_DITHER_BASE_DENSITY * center_density * mid_air * grass_suppression
        + ATMOSPHERIC_DITHER_LIGHT_BOOST * max(0.0, min(1.0, light_factor))
    )
    return max(0.0, min(1.0, density * top_suppression * shadow))


def atmospheric_light_factor(
    x: int,
    y: int,
    axis: tuple[tuple[float, float], tuple[float, float]] | None,
) -> float:
    if axis is None:
        return 0.0
    distance = _point_to_segment_distance(float(x), float(y), axis[0], axis[1])
    return max(0.0, min(1.0, 1.0 - distance / 42.0))


def atmospheric_dither_visible(x: int, y: int, phase: int, density: float) -> bool:
    if density <= 0.0:
        return False
    threshold = int(max(0.0, min(1.0, density)) * ATMOSPHERIC_DITHER_HASH_MODULUS)
    if threshold <= 0:
        return False
    value = (
        x * 17
        + y * 31
        + phase * 13
        + ((x + phase) // ATMOSPHERIC_DITHER_STEP) * 7
        + ((y - phase) // ATMOSPHERIC_DITHER_STEP) * 11
    ) % ATMOSPHERIC_DITHER_HASH_MODULUS
    return value < threshold


def _point_to_segment_distance(
    x: float,
    y: float,
    start: tuple[float, float],
    end: tuple[float, float],
) -> float:
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    length_squared = dx * dx + dy * dy
    if length_squared == 0.0:
        return sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / length_squared))
    nearest_x = x1 + dx * t
    nearest_y = y1 + dy * t
    return sqrt((x - nearest_x) * (x - nearest_x) + (y - nearest_y) * (y - nearest_y))


def select_rain_color(brightness: float, depth_tier: int = 1) -> int:
    if brightness > RAIN_BRIGHT_VISIBILITY_THRESHOLD and depth_tier >= 2:
        return RAIN_DEPTH_COLORS[3]
    safe_tier = max(0, min(len(RAIN_DEPTH_COLORS) - 1, depth_tier))
    return RAIN_DEPTH_COLORS[safe_tier]


def select_splash_color(intensity: float, normalized_age: float) -> int:
    if normalized_age > 0.72:
        return PALETTE_DIM_PARTICLE
    if intensity > 0.5:
        return PALETTE_BRIGHT_PARTICLE
    return PALETTE_CYLINDER_NEAR_EDGE


def _point_in_rect(x: int, y: int, rect: MenuRect) -> bool:
    rect_x, rect_y, width, height = rect
    return rect_x <= x < rect_x + width and rect_y <= y < rect_y + height
