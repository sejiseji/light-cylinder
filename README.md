# Light Cylinder

Light Cylinder is a quiet, mobile-first Pyxel work about observing a narrow
cylindrical slice of nature. Its central motif is cutting out incoming light:
grass, wind, rain, particles, shade, and bright bands will eventually gather
inside a tall observation space.

This repository is currently in early development. Before publishing or pushing
changes, run the public safety check and the full verification script.

## Current Stage

LC006 integrates the cylinder, grass, wind, particles, light media, camera, HUD,
and palette into a calmer presentation state. It keeps the light beam
non-rendered, preserves 420 tapered grass blades, starts in an HUD-off viewing
composition, and leaves rain, audio, touch input, and web packaging for later
waves.

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

The LC006 screen starts in a viewing state: light on, wind on, boundary off,
debug off, auto rotate off. It shows wind-animated grass, sparse particles, tip
lighting, and subtle floor light without drawing the beam itself. Debug mode adds
camera state, draw counters, the centered composition safe area, and light
axis/radius guides.

## Controls

- Left and Right: yaw around the target
- Up and Down: pitch around the target
- Mouse drag: yaw and pitch around the target
- A and S: zoom in and out
- Mouse wheel: zoom in and out
- X: toggle auto rotate
- B: toggle cylinder boundary
- W: toggle wind application
- L: toggle light media
- R: reset camera
- D: toggle debug HUD, reference axes, and light guides
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
