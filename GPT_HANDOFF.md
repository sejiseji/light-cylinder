# GPT Handoff

## Project

Light Cylinder is a mobile-first Pyxel observation work centered on sliced light
inside a tall cylindrical natural space.

## Current Wave

LC002 cylindrical observation volume.

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

## Not Completed

Grass, light, wind, rain, touch controls, audio, web packaging, and iOS packaging
are intentionally not implemented yet.

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
- A and S: zoom
- X: toggle auto rotate
- B: toggle cylinder boundary
- D: toggle debug
- ESC: quit

## Camera

The LC001 camera is an orbit camera. At yaw = 0 and pitch = 0, it looks along
positive Z toward the target. Camera-space depth is positive in front of the
camera. Points at or behind the near clip are skipped rather than clipped.

The LC002 camera target is `Vec3(0, CYLINDER_HEIGHT * 0.45, 0)`, with default
radius 96, height 240, 32 radial segments, and 8 vertical guides.

## Public Safety

Run the public safety check before publishing or pushing. Do not store
environment-specific absolute paths, personal identifiers, tokens, private keys,
or temporary logs in tracked files.

## Git

LC000 and LC001 were committed and pushed with approval. LC002 changes are not
committed or pushed yet. Future commits and pushes require user approval.

## Next Wave

LC003 should introduce procedural curved grass using the LC002 bottom sampling
and containment rules.

## Design Decisions

Keep Pyxel-specific code in the app layer and keep logic testable without Pyxel.
Use pathlib for relative resource resolution. Avoid speculative abstractions and
future directories until a wave needs them.
