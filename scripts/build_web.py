from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

import pyxel

from light_cylinder.app import MENU_BUTTON_RECT
from light_cylinder.config import RENDER_HEIGHT, RENDER_WIDTH

ENABLED_GAMEPAD = 'gamepad: "enabled"'
DISABLED_GAMEPAD = 'gamepad: "disabled"'
APP_NAME = "light-cylinder-web"
FIXED_ZIP_DATE = (1980, 1, 1, 0, 0, 0)
DEFAULT_OUTPUTS = ("index.html", "docs/index.html")
MOBILE_VIEWPORT_MARKER = "--light-cylinder-visible-height"
WEB_MENU_BUTTON_ID = "light-cylinder-menu-button"
WEB_APP_HASH_LENGTH = 12
WEB_PAGE_STYLE = """
<style>
:root {
  --light-cylinder-visible-width: 100vw;
  --light-cylinder-visible-height: 100svh;
  --light-cylinder-safari-ui-guard: 0px;
}

html,
body {
  margin: 0;
  padding: 0;
  width: var(--light-cylinder-visible-width);
  height: calc(var(--light-cylinder-visible-height) - var(--light-cylinder-safari-ui-guard));
  overflow: hidden;
  background: #11172c;
  overscroll-behavior: none;
}

body {
  position: fixed;
  left: 0;
  top: 0;
  touch-action: none;
}

#WEB_MENU_BUTTON_ID {
  position: fixed;
  left: 12px;
  top: calc(env(safe-area-inset-top, 0px) + 72px);
  z-index: 2147483647;
  min-width: 82px;
  height: 34px;
  padding: 0 12px;
  border: 1px solid #d8e8ff;
  border-radius: 4px;
  background: rgba(17, 23, 44, 0.82);
  color: #d8e8ff;
  font: 700 16px/34px system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  letter-spacing: 0;
  text-align: center;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

</style>
"""
WEB_PAGE_STYLE = WEB_PAGE_STYLE.replace("WEB_MENU_BUTTON_ID", WEB_MENU_BUTTON_ID)
WEB_VIEWPORT_SCRIPT = """
<script>
(() => {
  const root = document.documentElement;
  const userAgent = navigator.userAgent || "";
  const isIosLike = /iPad|iPhone|iPod/.test(userAgent)
    || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  const isSafari = /Safari/.test(userAgent)
    && !/(CriOS|FxiOS|EdgiOS|Chrome|Chromium)/.test(userAgent);

  const safariChromeGuard = (height) => {
    if (!isIosLike || !isSafari) {
      return 0;
    }
    return Math.round(Math.min(118, Math.max(72, height * 0.13)));
  };

  const applyVisibleViewport = () => {
    const viewport = window.visualViewport;
    const width = viewport ? viewport.width : window.innerWidth;
    const height = viewport ? viewport.height : window.innerHeight;
    const guard = safariChromeGuard(height);

    root.style.setProperty("--light-cylinder-visible-width", `${Math.floor(width)}px`);
    root.style.setProperty("--light-cylinder-visible-height", `${Math.floor(height)}px`);
    root.style.setProperty("--light-cylinder-safari-ui-guard", `${guard}px`);
  };

  applyVisibleViewport();
  window.addEventListener("resize", applyVisibleViewport, { passive: true });
  window.addEventListener("orientationchange", applyVisibleViewport, { passive: true });

  if (window.visualViewport) {
    window.visualViewport.addEventListener("resize", applyVisibleViewport, { passive: true });
    window.visualViewport.addEventListener("scroll", applyVisibleViewport, { passive: true });
  }
})();
</script>
"""
WEB_MENU_SCRIPT = """
<script>
(() => {
  const internalMenuX = MENU_CLICK_X;
  const internalMenuY = MENU_CLICK_Y;

  const dispatchCanvasEvent = (canvas, type, clientX, clientY) => {
    const options = {
      bubbles: true,
      cancelable: true,
      composed: true,
      clientX,
      clientY,
      screenX: clientX,
      screenY: clientY,
      button: 0,
      buttons: type.endsWith("down") || type === "mousemove" ? 1 : 0,
    };
    if (window.PointerEvent && type.startsWith("pointer")) {
      canvas.dispatchEvent(new PointerEvent(type, {
        ...options,
        pointerId: 1,
        pointerType: "touch",
        isPrimary: true,
      }));
      return;
    }
    if (!type.startsWith("pointer")) {
      canvas.dispatchEvent(new MouseEvent(type, options));
    }
  };

  const clickPyxelMenu = () => {
    const canvas = document.querySelector("#canvas");
    if (!canvas) {
      return;
    }
    const rect = canvas.getBoundingClientRect();
    const clientX = rect.left + (internalMenuX / GAME_WIDTH) * rect.width;
    const clientY = rect.top + (internalMenuY / GAME_HEIGHT) * rect.height;
    canvas.focus();
    dispatchCanvasEvent(canvas, "pointermove", clientX, clientY);
    dispatchCanvasEvent(canvas, "mousemove", clientX, clientY);
    dispatchCanvasEvent(canvas, "pointerdown", clientX, clientY);
    dispatchCanvasEvent(canvas, "mousedown", clientX, clientY);
    window.setTimeout(() => {
      dispatchCanvasEvent(canvas, "pointerup", clientX, clientY);
      dispatchCanvasEvent(canvas, "mouseup", clientX, clientY);
      dispatchCanvasEvent(canvas, "click", clientX, clientY);
    }, 34);
  };

  window.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("WEB_MENU_BUTTON_ID");
    if (!button) {
      return;
    }
    const keepMenuButtonOnTop = () => {
      if (button.parentElement === document.body && button.nextElementSibling === null) {
        return;
      }
      document.body.appendChild(button);
    };
    button.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      clickPyxelMenu();
    });
    keepMenuButtonOnTop();
    window.setTimeout(keepMenuButtonOnTop, 250);
    window.setTimeout(keepMenuButtonOnTop, 1000);
    window.setInterval(keepMenuButtonOnTop, 1000);
    if (window.MutationObserver) {
      const observer = new MutationObserver(keepMenuButtonOnTop);
      observer.observe(document.body, { childList: true });
    }
  });
})();
</script>
"""

_menu_x, _menu_y, _menu_width, _menu_height = MENU_BUTTON_RECT
WEB_MENU_SCRIPT = (
    WEB_MENU_SCRIPT.replace("MENU_CLICK_X", str(_menu_x + _menu_width // 2))
    .replace("MENU_CLICK_Y", str(_menu_y + _menu_height // 2))
    .replace("GAME_WIDTH", str(RENDER_WIDTH))
    .replace("GAME_HEIGHT", str(RENDER_HEIGHT))
    .replace("WEB_MENU_BUTTON_ID", WEB_MENU_BUTTON_ID)
)


def disable_pyxel_web_gamepad(html: str) -> str:
    if DISABLED_GAMEPAD in html:
        return html
    if ENABLED_GAMEPAD not in html:
        msg = "Pyxel web gamepad setting was not found"
        raise ValueError(msg)
    return html.replace(ENABLED_GAMEPAD, DISABLED_GAMEPAD, 1)


def copy_runtime_files(root: Path, app_dir: Path) -> None:
    if app_dir.exists():
        shutil.rmtree(app_dir)
    app_dir.mkdir(parents=True)

    shutil.copy2(root / "main.py", app_dir / "main.py")
    shutil.copytree(
        root / "src",
        app_dir / "src",
        ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"),
    )


def runtime_files(app_dir: Path) -> list[Path]:
    return sorted(path for path in app_dir.rglob("*") if path.is_file())


def write_zip_text(zf: zipfile.ZipFile, arcname: str, text: str) -> None:
    info = zipfile.ZipInfo(arcname, FIXED_ZIP_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, text.encode("utf-8"))


def write_zip_file(zf: zipfile.ZipFile, app_dir: Path, path: Path) -> None:
    arcname = str(Path(APP_NAME) / path.relative_to(app_dir))
    info = zipfile.ZipInfo(arcname, FIXED_ZIP_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, path.read_bytes())


def write_pyxapp(app_dir: Path, pyxapp: Path) -> None:
    with zipfile.ZipFile(pyxapp, "w") as zf:
        write_zip_text(zf, f"{APP_NAME}/{pyxel.APP_STARTUP_SCRIPT_FILE}", "main.py")
        for path in runtime_files(app_dir):
            write_zip_file(zf, app_dir, path)


def cache_busted_pyxapp_name(pyxapp: Path) -> str:
    digest = hashlib.sha256(pyxapp.read_bytes()).hexdigest()[:WEB_APP_HASH_LENGTH]
    return f"{APP_NAME}-{digest}.pyxapp"


def write_html(pyxapp: Path, html: Path) -> None:
    base64_string = base64.b64encode(pyxapp.read_bytes()).decode("ascii")
    pyxapp_name = json.dumps(cache_busted_pyxapp_name(pyxapp), ensure_ascii=True)
    html.write_text(
        "<!doctype html>\n"
        "<html>\n"
        "<head>\n"
        '<meta name="viewport" '
        'content="width=device-width, initial-scale=1, viewport-fit=cover, '
        'user-scalable=no">\n'
        f"{WEB_PAGE_STYLE}\n"
        f"{WEB_VIEWPORT_SCRIPT}\n"
        f"{WEB_MENU_SCRIPT}\n"
        f'<script src="https://cdn.jsdelivr.net/gh/kitao/pyxel@{pyxel.VERSION}/wasm/pyxel.js">'
        "</script>\n"
        "</head>\n"
        "<body>\n"
        f'<button id="{WEB_MENU_BUTTON_ID}" type="button" aria-label="Open observation menu">'
        "MENU</button>\n"
        "<script>\n"
        f'launchPyxel({{ command: "play", name: {pyxapp_name}, '
        f'{DISABLED_GAMEPAD}, base64: "{base64_string}" }});\n'
        "</script>\n"
        "</body>\n"
        "</html>\n",
        encoding="utf-8",
    )


def build_web(root: Path, outputs: list[Path]) -> tuple[Path, ...]:
    build_dir = root / "web" / "build"
    app_dir = build_dir / APP_NAME
    build_dir.mkdir(parents=True, exist_ok=True)
    copy_runtime_files(root, app_dir)

    pyxapp = build_dir / f"{APP_NAME}.pyxapp"
    html = build_dir / f"{APP_NAME}.html"
    pyxapp.unlink(missing_ok=True)
    html.unlink(missing_ok=True)

    write_pyxapp(app_dir, pyxapp)
    write_html(pyxapp, html)

    patched = disable_pyxel_web_gamepad(html.read_text(encoding="utf-8"))
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(patched, encoding="utf-8")
    return tuple(outputs)


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build GitHub Pages HTML for Light Cylinder.")
    parser.add_argument(
        "--output",
        action="append",
        type=Path,
        help="HTML output path. May be repeated. Defaults to root and docs entries.",
    )
    args = parser.parse_args(argv)

    outputs = args.output or [Path(path) for path in DEFAULT_OUTPUTS]
    resolved_outputs = [output if output.is_absolute() else root / output for output in outputs]
    built_outputs = build_web(root, resolved_outputs)
    built_names = ", ".join(str(path.relative_to(root)) for path in built_outputs)
    print(f"Built {built_names} with Pyxel virtual gamepad disabled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
