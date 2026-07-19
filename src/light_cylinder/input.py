from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ControlIntent:
    yaw_delta: float = 0.0
    pitch_delta: float = 0.0
    zoom_delta: float = 0.0
    toggle_auto_rotate: bool = False
    toggle_debug: bool = False
    toggle_boundary: bool = False
    toggle_wind: bool = False
    toggle_light: bool = False
    toggle_rain: bool = False
    toggle_firefly: bool = False
    toggle_observation_cycle: bool = False
    rain_intensity_delta: float = 0.0
    reset_camera: bool = False
    quit_requested: bool = False


@dataclass(slots=True)
class MouseInputState:
    previous_x: float | None = None
    previous_y: float | None = None
    dragging: bool = False


def _read_mouse_axis(pyxel_module, attr_name: str, button_name: str) -> float:
    if hasattr(pyxel_module, attr_name):
        return float(getattr(pyxel_module, attr_name))
    return float(pyxel_module.btn(getattr(pyxel_module, button_name)))


def read_control_intent(
    pyxel_module,
    yaw_speed: float,
    pitch_speed: float,
    zoom_speed: float,
    mouse_state: MouseInputState | None = None,
    mouse_yaw_speed: float = 0.0,
    mouse_pitch_speed: float = 0.0,
    mouse_wheel_zoom_speed: float = 0.0,
) -> ControlIntent:
    yaw_delta = 0.0
    pitch_delta = 0.0
    zoom_delta = 0.0

    if pyxel_module.btn(pyxel_module.KEY_LEFT):
        yaw_delta -= yaw_speed
    if pyxel_module.btn(pyxel_module.KEY_RIGHT):
        yaw_delta += yaw_speed
    if pyxel_module.btn(pyxel_module.KEY_UP):
        pitch_delta += pitch_speed
    if pyxel_module.btn(pyxel_module.KEY_DOWN):
        pitch_delta -= pitch_speed
    if pyxel_module.btn(pyxel_module.KEY_A):
        zoom_delta -= zoom_speed
    if pyxel_module.btn(pyxel_module.KEY_S):
        zoom_delta += zoom_speed
    if mouse_state is not None:
        mouse_x = _read_mouse_axis(pyxel_module, "mouse_x", "MOUSE_POS_X")
        mouse_y = _read_mouse_axis(pyxel_module, "mouse_y", "MOUSE_POS_Y")
        wheel_y = _read_mouse_axis(pyxel_module, "mouse_wheel", "MOUSE_WHEEL_Y")
        if pyxel_module.btn(pyxel_module.MOUSE_BUTTON_LEFT):
            if (
                mouse_state.dragging
                and mouse_state.previous_x is not None
                and mouse_state.previous_y is not None
            ):
                yaw_delta += (mouse_x - mouse_state.previous_x) * mouse_yaw_speed
                pitch_delta -= (mouse_y - mouse_state.previous_y) * mouse_pitch_speed
            mouse_state.dragging = True
            mouse_state.previous_x = mouse_x
            mouse_state.previous_y = mouse_y
        else:
            mouse_state.dragging = False
            mouse_state.previous_x = mouse_x
            mouse_state.previous_y = mouse_y

        zoom_delta -= wheel_y * mouse_wheel_zoom_speed

    return ControlIntent(
        yaw_delta=yaw_delta,
        pitch_delta=pitch_delta,
        zoom_delta=zoom_delta,
        toggle_auto_rotate=pyxel_module.btnp(pyxel_module.KEY_X),
        toggle_debug=pyxel_module.btnp(pyxel_module.KEY_D),
        toggle_boundary=pyxel_module.btnp(pyxel_module.KEY_B),
        toggle_wind=pyxel_module.btnp(pyxel_module.KEY_W),
        toggle_light=pyxel_module.btnp(pyxel_module.KEY_L),
        toggle_rain=pyxel_module.btnp(pyxel_module.KEY_N),
        toggle_firefly=pyxel_module.btnp(pyxel_module.KEY_F),
        toggle_observation_cycle=pyxel_module.btnp(pyxel_module.KEY_M),
        rain_intensity_delta=float(pyxel_module.btnp(pyxel_module.KEY_E))
        - float(pyxel_module.btnp(pyxel_module.KEY_Q)),
        reset_camera=pyxel_module.btnp(pyxel_module.KEY_R),
        quit_requested=pyxel_module.btnp(pyxel_module.KEY_ESCAPE),
    )
