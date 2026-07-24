from pathlib import Path

import pytest

from scripts.build_web import (
    DISABLED_GAMEPAD,
    ENABLED_GAMEPAD,
    MOBILE_VIEWPORT_MARKER,
    cache_busted_pyxapp_name,
    disable_pyxel_web_gamepad,
    write_pyxapp,
)


def test_disable_pyxel_web_gamepad_replaces_enabled_setting() -> None:
    html = f'launchPyxel({{ command: "play", {ENABLED_GAMEPAD}, base64: "..." }});'

    patched = disable_pyxel_web_gamepad(html)

    assert ENABLED_GAMEPAD not in patched
    assert DISABLED_GAMEPAD in patched


def test_disable_pyxel_web_gamepad_is_idempotent() -> None:
    html = f'launchPyxel({{ command: "play", {DISABLED_GAMEPAD}, base64: "..." }});'

    assert disable_pyxel_web_gamepad(html) == html


def test_disable_pyxel_web_gamepad_rejects_unrecognized_html() -> None:
    with pytest.raises(ValueError, match="gamepad setting"):
        disable_pyxel_web_gamepad("<!doctype html>")


def test_committed_github_pages_entry_disables_virtual_gamepad() -> None:
    for entry in (Path("index.html"), Path("docs/index.html")):
        html = entry.read_text(encoding="utf-8")

        assert 'launchPyxel({ command: "play"' in html
        assert "<pyxel-run" not in html
        assert "Pythonのファイル名.py" not in html
        assert DISABLED_GAMEPAD in html
        assert ENABLED_GAMEPAD not in html
        assert "light-cylinder-menu-button" not in html
        assert "Open observation menu" not in html
        assert "clickPyxelMenu" not in html
        assert "keepMenuButtonOnTop" not in html
        assert "MutationObserver" not in html
        assert 'document.querySelector("#canvas")' not in html
        assert "new PointerEvent" not in html
        assert "new MouseEvent" not in html
        assert 'name: "light-cylinder-web-' in html
        assert 'name: "light-cylinder-web.pyxapp"' not in html


def test_committed_github_pages_entry_fits_mobile_safari_viewport() -> None:
    for entry in (Path("index.html"), Path("docs/index.html")):
        html = entry.read_text(encoding="utf-8")

        assert "<body>" in html
        assert html.index("<body>") < html.index("launchPyxel")
        assert "viewport-fit=cover" in html
        assert "window.visualViewport" in html
        assert MOBILE_VIEWPORT_MARKER in html
        assert "100svh" in html
        assert "--light-cylinder-safari-ui-guard" not in html
        assert "safariChromeGuard" not in html
        assert "height: var(--light-cylinder-visible-height)" in html
        assert "touch-action: none" in html
        assert "#pyxel-screen" not in html
        assert "canvas {" not in html


def test_cache_busted_pyxapp_name_is_content_based(tmp_path: Path) -> None:
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    (app_dir / "main.py").write_text("print('hello')\n", encoding="utf-8")
    pyxapp = tmp_path / "sample.pyxapp"

    write_pyxapp(app_dir, pyxapp)
    first = cache_busted_pyxapp_name(pyxapp)
    second = cache_busted_pyxapp_name(pyxapp)

    assert first == second
    assert first.startswith("light-cylinder-web-")
    assert first.endswith(".pyxapp")
    assert first != "light-cylinder-web.pyxapp"


def test_pyxapp_archive_is_deterministic(tmp_path: Path) -> None:
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    (app_dir / "main.py").write_text("print('hello')\n", encoding="utf-8")
    first = tmp_path / "first.pyxapp"
    second = tmp_path / "second.pyxapp"

    write_pyxapp(app_dir, first)
    write_pyxapp(app_dir, second)

    assert first.read_bytes() == second.read_bytes()
