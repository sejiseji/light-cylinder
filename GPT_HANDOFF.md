# GPT Handoff

## Project

Light Cylinder is a mobile-first Pyxel observation work centered on sliced light
inside a tall cylindrical natural space.

## Current Wave

LC005 light media and tip lighting.

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
- D: toggle debug HUD, reference axes, and light guides
- ESC: quit

## Camera

The LC001 camera is an orbit camera. At yaw = 0 and pitch = 0, it looks along
positive Z toward the target. Camera-space depth is positive in front of the
camera. Points at or behind the near clip are skipped rather than clipped.

The LC002 camera target is `Vec3(0, CYLINDER_HEIGHT * 0.45, 0)`, with default
radius 96, height 240, 32 radial segments, and 8 vertical guides.

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

## Light

- Beam origin: `(-34, 246, -22)`
- Beam direction: `(0.22, -1.0, 0.18)` normalized
- Beam length: 285
- Beam radius: 42
- Core radius: 13
- Particles: 48
- Floor sparks: 28
- Normal rendering: no direct beam drawing
- Debug rendering: axis line and three radius rings

## Visual Acceptance

From LC005 onward, review `docs/visual_acceptance.md` after implementation.
LC005 should make the light column readable through particles, grass tips, and
floor lighting while keeping grass as the main subject.

## Public Safety

Run the public safety check before publishing or pushing. Do not store
environment-specific absolute paths, personal identifiers, tokens, private keys,
or temporary logs in tracked files.

## Git

LC000 through LC003 were committed and pushed with approval. LC004/LC005 changes are
not committed or pushed yet. Future commits and pushes require user approval.

## Next Wave

LC006 should tune time, palette, HUD-off beauty, camera auto speed, wind rhythm,
particle speed, and cylinder presence.

## Design Decisions

Keep Pyxel-specific code in the app layer and keep logic testable without Pyxel.
Use pathlib for relative resource resolution. Avoid speculative abstractions and
future directories until a wave needs them.
