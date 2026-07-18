import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

# Keep `python main.py` working before the package is installed in editable mode.
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def main() -> None:
    from light_cylinder.app import LightCylinderApp

    LightCylinderApp().run()


if __name__ == "__main__":
    main()
