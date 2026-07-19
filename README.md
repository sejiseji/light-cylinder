# Light Cylinder

Light Cylinder is the development name for `Specimen of Light` / `光の標本`, a
quiet, mobile-first Pyxel work about observing a narrow cylindrical slice of
nature. Its central motif is cutting out incoming light: grass, wind, rain,
particles, shade, and bright bands will eventually gather inside a tall
observation space.

This repository is currently in early development. Before publishing or pushing
changes, run the public safety check and the full verification script.

## Current Stage

LC008 adds restrained rain reactions. The scene still starts clear; pressing `N`
introduces sparse wind-slanted rain, small ground splashes, local grass presses,
ground wetness, and weak wet-floor light reflection. Rain amount can be adjusted
with `Q` and `E`. Puddles, ripples, thunder, rain audio, retained water drops,
touch input, and web packaging remain later waves.

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

The LC008 screen starts in a clear viewing state: light on, wind on, rain off,
boundary off, debug off, auto rotate off. It shows wind-animated grass, sparse
particles, tip lighting, and subtle floor light without drawing the beam itself.
Debug mode adds camera state, draw counters, the centered composition safe area,
rain counters, splash count, wetness, grass reaction count, and light axis/radius
guides.

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
- N: toggle rain
- Q and E: decrease and increase rain amount
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
