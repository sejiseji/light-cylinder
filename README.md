# Light Cylinder

Light Cylinder is a quiet, mobile-first Pyxel work about observing a narrow
cylindrical slice of nature. Its central motif is cutting out incoming light:
grass, wind, rain, particles, shade, and bright bands will eventually gather
inside a tall observation space.

This repository is currently in early development. Before publishing or pushing
changes, run the public safety check and the full verification script.

## Current Stage

LC002 adds the cylindrical observation volume. It provides a Pyxel-independent
`CylinderWorld`, ring and guide generation, area-uniform bottom sampling, and a
debug view where the orbit camera can inspect the cylinder wireframe. Grass,
light, wind, rain, audio, touch input, and web packaging are intentionally left
for later waves.

## Display Model

- Reference device area: 393 x 852
- Pyxel internal render size: 448 x 852
- Composition safe width: 393
- Target FPS: 30

The important composition area is the centered 393-pixel region inside the
448-pixel render width. The side overscan area is reserved for visuals that can
be clipped gracefully in future browser and mobile layouts.

## Requirements

- Python 3.11 or newer
- Pyxel

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run

```sh
python main.py
```

The LC002 screen shows the cylinder top and bottom rings, vertical guides, bottom
grid, center axis, camera state, boundary state, auto-rotate state, debug state,
and the centered composition safe area while debug is visible.

## Controls

- Left and Right: yaw around the target
- Up and Down: pitch around the target
- A and S: zoom in and out
- X: toggle auto rotate
- B: toggle cylinder boundary
- D: toggle debug frame
- ESC: quit

## Validate

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
python scripts/check_public_safety.py
python scripts/check_all.py
```

Run `python scripts/check_all.py` before requesting review or pushing.
