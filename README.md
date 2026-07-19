# Light Cylinder

Light Cylinder is the development name for `Specimen of Light` / `光の標本`, a
quiet, mobile-first Pyxel work about observing a narrow cylindrical slice of
nature. Its central motif is cutting out incoming light: grass, wind, rain,
particles, shade, and bright bands will eventually gather inside a tall
observation space.

This repository is currently in early development. Before publishing or pushing
changes, run the public safety check and the full verification script.

## Current Stage

LC011 adds optional firefly visitors. The scene still starts clear and manual,
with fireflies off, but pressing `F` or using MENU can allow adjustable visitors
into the cylinder. They drift farther across the volume with slow blinking,
appear far less often during rain, and never replace grass, light, rain, or the
observation cycle as the main subject. Puddles, ripples, thunder, rain audio,
all-grass droplets, touch input, and web packaging remain later waves.

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

The LC011 screen starts in a clear viewing state: light on, wind on, rain off,
fireflies off, boundary off, debug off, auto rotate off. It shows wind-animated
grass, denser mixed-size light particles, tip lighting, subtle floor light, and
five quiet mixed-width tapered light bands. Bottom floor rings and radial lines stay hidden until the
cylinder boundary is shown.
Debug mode adds camera state, draw counters, the centered composition safe area,
environment phase, rain counters, splash count, wetness, grass reaction count,
tip droplet count, observation cycle phase, and light axis/radius guides. Bottom
coordinate axes stay hidden.

The top-right `MENU` button opens a readable observation panel. Photon density,
grass density, wind strength, rain amount, auto-rotate speed, and firefly visitor
count are adjustable from stage 1 to 3, and auto-rotate, rain, and fireflies can
also be toggled ON/OFF there.
WIND strengthens the stage 1 sway around the same steady bend instead of moving
to a different resting bend, and higher stages also advance the wind motion time
faster. Stage 1 is the current baseline look. These settings are session-only
and reset to stage 1 after restart. `AMOUNT` changes only the rain amount
preset; rain starts and stops through either `N` or the MENU `RAIN` toggle.

`M` toggles the observation cycle. While enabled, the cycle applies temporary
rain and light multipliers on top of the current MENU stages. Pressing `N`,
`Q`, or `E` exits the cycle and returns to manual rain control.

Auto rotate slowly orbits left/right and adds a small vertical sway. Manual
pitch steering through arrow keys or drag updates the sway center, so the viewing
angle follows the observer's chosen baseline.

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
- F: toggle firefly visitors
- M: toggle observation cycle
- Q and E: decrease and increase rain amount
- R: reset camera
- D: toggle debug HUD and light guides
- MENU button: open the observation tuning panel
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
