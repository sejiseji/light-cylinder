import pytest

from light_cylinder.input import ControlIntent, MouseInputState, read_control_intent


class FakePyxel:
    KEY_LEFT = "left"
    KEY_RIGHT = "right"
    KEY_UP = "up"
    KEY_DOWN = "down"
    KEY_A = "a"
    KEY_S = "s"
    KEY_X = "x"
    KEY_D = "d"
    KEY_B = "b"
    KEY_W = "w"
    KEY_L = "l"
    KEY_N = "n"
    KEY_Q = "q"
    KEY_E = "e"
    KEY_R = "r"
    KEY_ESCAPE = "escape"
    MOUSE_BUTTON_LEFT = "mouse-left"
    MOUSE_POS_X = "mouse-x"
    MOUSE_POS_Y = "mouse-y"
    MOUSE_WHEEL_Y = "mouse-wheel-y"

    def __init__(
        self,
        held: set[str] | None = None,
        pressed: set[str] | None = None,
        values: dict[str, float] | None = None,
    ) -> None:
        self.held = held or set()
        self.pressed = pressed or set()
        self.values = values or {}

    def btn(self, key: str) -> bool | float:
        if key in self.values:
            return self.values[key]
        return key in self.held

    def btnp(self, key: str) -> bool:
        return key in self.pressed


def test_control_intent_defaults() -> None:
    intent = ControlIntent()

    assert intent.yaw_delta == 0.0
    assert intent.pitch_delta == 0.0
    assert intent.zoom_delta == 0.0
    assert not intent.toggle_auto_rotate
    assert not intent.toggle_debug
    assert not intent.toggle_boundary
    assert not intent.toggle_wind
    assert not intent.toggle_light
    assert not intent.toggle_rain
    assert intent.rain_intensity_delta == 0.0
    assert not intent.reset_camera
    assert not intent.quit_requested


def test_control_intent_holds_values() -> None:
    intent = ControlIntent(
        yaw_delta=1.0,
        pitch_delta=2.0,
        zoom_delta=3.0,
        toggle_auto_rotate=True,
        toggle_debug=True,
        toggle_boundary=True,
        toggle_wind=True,
        toggle_light=True,
        toggle_rain=True,
        rain_intensity_delta=1.0,
        reset_camera=True,
        quit_requested=True,
    )

    assert intent.yaw_delta == 1.0
    assert intent.pitch_delta == 2.0
    assert intent.zoom_delta == 3.0
    assert intent.toggle_auto_rotate
    assert intent.toggle_debug
    assert intent.toggle_boundary
    assert intent.toggle_wind
    assert intent.toggle_light
    assert intent.toggle_rain
    assert intent.rain_intensity_delta == 1.0
    assert intent.reset_camera
    assert intent.quit_requested


def test_read_control_intent_from_key_state() -> None:
    pyxel = FakePyxel(
        held={FakePyxel.KEY_RIGHT, FakePyxel.KEY_UP, FakePyxel.KEY_A},
        pressed={
            FakePyxel.KEY_X,
            FakePyxel.KEY_D,
            FakePyxel.KEY_B,
            FakePyxel.KEY_W,
            FakePyxel.KEY_L,
            FakePyxel.KEY_N,
            FakePyxel.KEY_E,
            FakePyxel.KEY_R,
            FakePyxel.KEY_ESCAPE,
        },
    )

    intent = read_control_intent(pyxel, yaw_speed=0.1, pitch_speed=0.2, zoom_speed=3.0)

    assert intent.yaw_delta == 0.1
    assert intent.pitch_delta == 0.2
    assert intent.zoom_delta == -3.0
    assert intent.toggle_auto_rotate
    assert intent.toggle_debug
    assert intent.toggle_boundary
    assert intent.toggle_wind
    assert intent.toggle_light
    assert intent.toggle_rain
    assert intent.rain_intensity_delta == 1.0
    assert intent.reset_camera
    assert intent.quit_requested


def test_read_control_intent_decreases_rain_intensity() -> None:
    pyxel = FakePyxel(pressed={FakePyxel.KEY_Q})

    intent = read_control_intent(pyxel, yaw_speed=0.1, pitch_speed=0.2, zoom_speed=3.0)

    assert intent.rain_intensity_delta == -1.0


def test_opposing_keys_cancel() -> None:
    pyxel = FakePyxel(
        held={
            FakePyxel.KEY_LEFT,
            FakePyxel.KEY_RIGHT,
            FakePyxel.KEY_UP,
            FakePyxel.KEY_DOWN,
            FakePyxel.KEY_A,
            FakePyxel.KEY_S,
        }
    )

    intent = read_control_intent(pyxel, yaw_speed=0.1, pitch_speed=0.2, zoom_speed=3.0)

    assert intent.yaw_delta == 0.0
    assert intent.pitch_delta == 0.0
    assert intent.zoom_delta == 0.0


def test_mouse_drag_updates_yaw_pitch() -> None:
    state = MouseInputState(previous_x=100.0, previous_y=100.0, dragging=True)
    pyxel = FakePyxel(
        held={FakePyxel.MOUSE_BUTTON_LEFT},
        values={
            FakePyxel.MOUSE_POS_X: 112.0,
            FakePyxel.MOUSE_POS_Y: 90.0,
            FakePyxel.MOUSE_WHEEL_Y: 0.0,
        },
    )

    intent = read_control_intent(
        pyxel,
        yaw_speed=0.1,
        pitch_speed=0.2,
        zoom_speed=3.0,
        mouse_state=state,
        mouse_yaw_speed=0.01,
        mouse_pitch_speed=0.02,
        mouse_wheel_zoom_speed=4.0,
    )

    assert intent.yaw_delta == pytest.approx(0.12)
    assert intent.pitch_delta == pytest.approx(0.2)
    assert state.previous_x == 112.0
    assert state.previous_y == 90.0
    assert state.dragging


def test_mouse_wheel_updates_zoom() -> None:
    state = MouseInputState()
    pyxel = FakePyxel(
        values={
            FakePyxel.MOUSE_POS_X: 0.0,
            FakePyxel.MOUSE_POS_Y: 0.0,
            FakePyxel.MOUSE_WHEEL_Y: 2.0,
        }
    )

    intent = read_control_intent(
        pyxel,
        yaw_speed=0.1,
        pitch_speed=0.2,
        zoom_speed=3.0,
        mouse_state=state,
        mouse_yaw_speed=0.01,
        mouse_pitch_speed=0.02,
        mouse_wheel_zoom_speed=4.0,
    )

    assert intent.zoom_delta == -8.0
    assert not state.dragging
