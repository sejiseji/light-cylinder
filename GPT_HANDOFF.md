# GPT Handoff

## Project

Light Cylinder is a mobile-first Pyxel observation work centered on sliced light
inside a tall cylindrical natural space.

## Current Wave

LC006 visual integration and presentation polish.

## Completed

- Python src layout
- Thin `main.py` launcher
- Centralized display configuration
- Minimal Pyxel debug screen
- Documentation set
- Public safety scanner
- Full verification script
- Unit tests for display configuration and safety scanning
- Pyxel-independent Vec2 and Vec3 math
- Orbit camera projection with near-clip rejection
- Pyxel-independent `ControlIntent`
- LC001 debug view with origin, X/Y/Z axes, grid, camera state, and controls
- Pyxel-independent `CylinderWorld`
- Cylinder containment, ring generation, vertical guides, and bottom sampling
- LC002 debug view with top and bottom rings, vertical guides, bottom grid, and
  boundary toggle
- Pyxel-independent `GrassBlade` and `GrassField`
- Fixed-seed curved grass generation on the cylinder bottom
- Depth-sorted static grass rendering with height, bend, width, and color variety
- Pyxel-independent `WindField`
- Layered wind with base direction, slow pulse, spatial phase, blade phase, and
  smooth gust envelope
- Stiffness and height-aware grass wind response
- Wind toggle with `W`
- Pyxel-independent `LightBeam` and `LightField`
- 48 deterministic light particles inside the beam volume
- Grass lighting from root/middle/tip samples, weighted toward blade tips
- Bottom-grid light color changes and sparse floor spark points
- Light media toggle with `L`
- Debug-only light axis and radius guide rings
- LC006 palette consolidation with named `PALETTE_*` config constants
- Viewing-first default state: HUD off, boundary off, wind on, light on
- Camera reset with `R`
- Slower auto rotate for presentation
- Debug HUD counters for visible blades, lit segments, approximate line calls,
  and visible particles

## Not Completed

Rain, touch controls, audio, web packaging, and iOS packaging are intentionally
not implemented yet.

## Run

```sh
python main.py
```

## Validate

```sh
python scripts/check_all.py
```

## Screen Contract

- Reference device: 393 x 852
- Internal render: 448 x 852
- Centered safe width: 393
- Target FPS: 30

## Controls

- Left and Right: yaw
- Up and Down: pitch
- Mouse drag: yaw and pitch
- A and S: zoom
- Mouse wheel: zoom
- X: toggle auto rotate
- B: toggle cylinder boundary
- W: toggle wind
- L: toggle light media
- R: reset camera
- D: toggle debug HUD, reference axes, and light guides
- ESC: quit

## Camera

The LC001 camera is an orbit camera. At yaw = 0 and pitch = 0, it looks along
positive Z toward the target. Camera-space depth is positive in front of the
camera. Points at or behind the near clip are skipped rather than clipped.

The LC006 camera target is `Vec3(0, CYLINDER_HEIGHT * 0.43, 0)`, with default
radius 96, height 240, 32 radial segments, and 8 vertical guides.

Initial camera:

- yaw: -0.22
- pitch: 0.34
- distance: 430
- auto rotate speed: 0.0035 radians per frame
- auto pitch: not added

## Grass

- Count: 420
- Segments per blade: 5
- Seed: 1729
- Height range: 18 to 46
- Bend range: 2 to 15
- Stiffness range: 0.45 to 1.0
- Density: slightly sparse at center and rim, densest around the middle band
- Animation: layered wind in LC004

## Wind

- Base direction angle: 0.35 radians
- Base speed: 0.55
- Response scale: 13.0
- Slow pulse: sinusoidal
- Spatial phase: X/Z position
- Blade phase: `GrassBlade.phase`
- Gust: deterministic sin-squared envelope
- Wind max bend: 42 percent of blade height
- Base pulse rate: 0.42
- Base pulse amount: 0.22
- Direction sway rate: 0.37
- Gust interval: 12.0
- Gust duration: 5.5

## Light

- Beam origin: `(-34, 246, -22)`
- Beam direction: `(0.22, -1.0, 0.18)` normalized
- Beam length: 285
- Beam radius: 44
- Core radius: 14
- Particles: 48
- Floor sparks: 28
- Pulse rate: 0.11
- Pulse amount: 0.13
- Particle drift range: -2.6 to 4.8
- Normal rendering: no direct beam drawing
- Debug rendering: axis line and three radius rings

## Palette

- background: 1
- background band: 2
- distant grass: 3
- normal grass: 11
- foreground/lit grass: 10
- strongly lit grass: 7
- ground shadow: 5
- ground light: 13
- ground strong light: 10
- dim particle: 6
- bright particle: 7
- cylinder far edge: 5
- cylinder near edge: 13
- cylinder vertical: 5
- debug accent: 12

## Presentation State

Initial viewing state:

- debug HUD: off
- boundary: off
- wind: on
- light media: on
- auto rotate: off

Use `D` for inspection and `B` to compare the restrained cylinder boundary.
Use `R` to restore the presentation camera.

## Visual Acceptance

From LC005 onward, review `docs/visual_acceptance.md` after implementation.
LC006 GUI review found the HUD-off scene readable as a viewing screen: grass
remains primary, light direction reads through sparse particles and tip lighting,
particles do not read as snow, boundary ON is subdued, and HUD OFF can be
watched for at least one minute without the auto rotate feeling too fast.

## Performance

- Grass count: 420
- Nominal segments: 2,100
- Typical visible particles in debug review: about 29 to 36
- Approximate line draw calls are reported in debug HUD
- GUI review kept a stable 30 FPS feel with light, wind, particles, boundary
  on/off, zoom, and slow auto rotate.

## Public Safety

Run the public safety check before publishing or pushing. Do not store
environment-specific absolute paths, personal identifiers, tokens, private keys,
or temporary logs in tracked files.

## Git

LC000 through LC005 were committed and pushed with approval. LC006 changes are
not committed or pushed yet. Future commits and pushes require user approval.

## Next Wave

LC007 should add rain without disturbing the LC006 presentation balance.

## Design Decisions

Keep Pyxel-specific code in the app layer and keep logic testable without Pyxel.
Use pathlib for relative resource resolution. Avoid speculative abstractions and
future directories until a wave needs them.
