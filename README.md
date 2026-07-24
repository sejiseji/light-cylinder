# Light Cylinder

Light Cylinder is the development name for `Specimen of Light` / `光の標本`, a
quiet, mobile-first Pyxel work about observing a narrow cylindrical slice of
nature. Its central motif is cutting out incoming light: grass, wind, rain,
particles, shade, and bright bands will eventually gather inside a tall
observation space.

This repository is currently in early development. Before publishing or pushing
changes, run the public safety check and the full verification script.

## Current Stage

LC012.6 optimizes the ground and grass field for the web preview. The scene
still starts clear and manual, but the bottom plane now reads as dark soil with
weaker wet and light-reflection states, ordinary grass uses lower
`120 / 180 / 240` density stages, and fixed-seed clumps leave intentional soil
openings around the foxtails. Puddles, ripples, thunder, rain audio, all-grass
droplets, touch input, and iOS packaging remain later waves. GitHub Pages entry
points are generated at `index.html` and `docs/index.html` for browser launch
checks, and the web launcher fits the Pyxel canvas to the visible mobile Safari
viewport so the top-right MENU stays inside the usable screen area.

The next development sequence is focused on making the summer air denser rather
than adding summer symbols: foxtail grass, after-rain droplets, summer cumulus,
heat haze, distant horizon, summer ambience, then a presentation pass toward
`prototype-v0.3.0`.

## Display Model

- Reference device area: 393 x 852
- Pyxel internal render size: 393 x 852
- Composition safe width: 393
- Target FPS: 30

The Pyxel render width now matches the mobile reference width, following the
Fireworks Observer-style browser profile. UI and important composition beats no
longer depend on side overscan that mobile Safari may clip.

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

The LC012.6 screen starts in a clear viewing state: light on, wind on, rain off,
fireflies off, boundary off, debug off, auto rotate off. It shows wind-animated
clustered grass, dark soil, denser mixed-size light particles, tip lighting,
subtle floor light, and five quiet mixed-width tapered light bands, with a few
taller foxtails as foreground memory points. Bottom floor rings and radial lines
stay hidden until the cylinder boundary is shown.
Debug mode adds camera state, draw counters, the centered composition safe area,
environment phase, rain counters, splash count, wetness, grass reaction count,
tip droplet count, observation cycle phase, and light axis/radius guides. Bottom
coordinate axes stay hidden.

The top-right `MENU` button opens a readable observation panel. Photon density,
grass density, wind strength, rain amount, auto-rotate speed, and firefly visitor
count are adjustable from stage 1 to 3, and auto-rotate, rain, and fireflies can
also be toggled ON/OFF there. The same panel includes ZOOM IN/OUT buttons for
mobile viewing without keyboard or wheel input. Grass stages draw 120, 180, or
240 blades.
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
- MENU ZOOM IN/OUT: adjust camera distance
- ESC: quit

## Web Preview

Build the GitHub Pages entry point with:

```sh
python scripts/build_web.py
```

This writes `index.html` and `docs/index.html` as self-contained Pyxel Web
pages. The generated launcher disables Pyxel's virtual gamepad, matching the
Fireworks Observer-style browser preview without mobile gamepad controls. It
also uses the browser's visible viewport on mobile Safari and keeps the MENU
button inside the 393-pixel Pyxel render width.
On iOS Safari, the launcher reserves a small browser-UI guard height because the
reported viewport can still include part of the bottom bar.
The web page also adds a small fixed `MENU` entry button outside the Pyxel
canvas as a Safari fallback. It forwards a tap to the in-game MENU button,
keeps itself above Pyxel's generated DOM, and does not enable Pyxel's virtual
gamepad.

For local browser confirmation:

```sh
python -m http.server 8000
```

Then open `http://127.0.0.1:8000/`. After pushing, GitHub Pages can serve the
same launcher whether the repository Pages source is configured to `main` /
root or `main` / `docs`.

## Validate

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
python scripts/check_public_safety.py
python scripts/check_all.py
```

Run `python scripts/check_all.py` before requesting review or pushing.
