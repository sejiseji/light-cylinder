from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ControlIntent:
    yaw_delta: float = 0.0
    pitch_delta: float = 0.0
    zoom_delta: float = 0.0
    toggle_auto_rotate: bool = False
    toggle_debug: bool = False
    quit_requested: bool = False


def read_control_intent(
    pyxel_module,
    yaw_speed: float,
    pitch_speed: float,
    zoom_speed: float,
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

    return ControlIntent(
        yaw_delta=yaw_delta,
        pitch_delta=pitch_delta,
        zoom_delta=zoom_delta,
        toggle_auto_rotate=pyxel_module.btnp(pyxel_module.KEY_X),
        toggle_debug=pyxel_module.btnp(pyxel_module.KEY_D),
        quit_requested=pyxel_module.btnp(pyxel_module.KEY_ESCAPE),
    )
