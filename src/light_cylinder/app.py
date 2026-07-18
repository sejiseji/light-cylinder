from light_cylinder.config import (
    COMPOSITION_SAFE_WIDTH,
    PROJECT_TITLE,
    RENDER_HEIGHT,
    RENDER_WIDTH,
    SAFE_LEFT,
    SAFE_RIGHT,
    TARGET_FPS,
    validate_display_config,
)


class LightCylinderApp:
    def __init__(self) -> None:
        validate_display_config()

    def run(self) -> None:
        import pyxel

        pyxel.init(RENDER_WIDTH, RENDER_HEIGHT, title=PROJECT_TITLE, fps=TARGET_FPS)
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        import pyxel

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    def draw(self) -> None:
        import pyxel

        center_x = RENDER_WIDTH // 2
        center_y = RENDER_HEIGHT // 2

        pyxel.cls(1)
        pyxel.rectb(0, 0, RENDER_WIDTH, RENDER_HEIGHT, 5)
        pyxel.line(center_x, 0, center_x, RENDER_HEIGHT - 1, 13)
        pyxel.line(0, center_y, RENDER_WIDTH - 1, center_y, 13)
        pyxel.rectb(SAFE_LEFT, 0, COMPOSITION_SAFE_WIDTH, RENDER_HEIGHT, 11)
        pyxel.line(SAFE_LEFT, 0, SAFE_LEFT, RENDER_HEIGHT - 1, 3)
        pyxel.line(SAFE_RIGHT - 1, 0, SAFE_RIGHT - 1, RENDER_HEIGHT - 1, 3)

        pyxel.text(SAFE_LEFT + 8, 16, PROJECT_TITLE, 7)
        pyxel.text(SAFE_LEFT + 8, 28, f"RENDER {RENDER_WIDTH}x{RENDER_HEIGHT}", 6)
        pyxel.text(SAFE_LEFT + 8, 40, f"SAFE {COMPOSITION_SAFE_WIDTH}x{RENDER_HEIGHT}", 6)
        pyxel.text(SAFE_LEFT + 8, 52, f"FPS {TARGET_FPS}", 6)
        pyxel.text(SAFE_LEFT + 8, 64, "ESC TO QUIT", 6)
