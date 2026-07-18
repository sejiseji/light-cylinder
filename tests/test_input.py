from light_cylinder.input import ControlIntent, read_control_intent


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
    KEY_ESCAPE = "escape"

    def __init__(self, held: set[str] | None = None, pressed: set[str] | None = None) -> None:
        self.held = held or set()
        self.pressed = pressed or set()

    def btn(self, key: str) -> bool:
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
    assert not intent.quit_requested


def test_control_intent_holds_values() -> None:
    intent = ControlIntent(
        yaw_delta=1.0,
        pitch_delta=2.0,
        zoom_delta=3.0,
        toggle_auto_rotate=True,
        toggle_debug=True,
        toggle_boundary=True,
        quit_requested=True,
    )

    assert intent.yaw_delta == 1.0
    assert intent.pitch_delta == 2.0
    assert intent.zoom_delta == 3.0
    assert intent.toggle_auto_rotate
    assert intent.toggle_debug
    assert intent.toggle_boundary
    assert intent.quit_requested


def test_read_control_intent_from_key_state() -> None:
    pyxel = FakePyxel(
        held={FakePyxel.KEY_RIGHT, FakePyxel.KEY_UP, FakePyxel.KEY_A},
        pressed={FakePyxel.KEY_X, FakePyxel.KEY_D, FakePyxel.KEY_B, FakePyxel.KEY_ESCAPE},
    )

    intent = read_control_intent(pyxel, yaw_speed=0.1, pitch_speed=0.2, zoom_speed=3.0)

    assert intent.yaw_delta == 0.1
    assert intent.pitch_delta == 0.2
    assert intent.zoom_delta == -3.0
    assert intent.toggle_auto_rotate
    assert intent.toggle_debug
    assert intent.toggle_boundary
    assert intent.quit_requested


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
