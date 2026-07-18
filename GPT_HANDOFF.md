# GPT Handoff

## Project

Light Cylinder is a mobile-first Pyxel observation work centered on sliced light
inside a tall cylindrical natural space.

## Current Wave

LC000 bootstrap.

## Completed

- Python src layout
- Thin `main.py` launcher
- Centralized display configuration
- Minimal Pyxel debug screen
- Documentation set
- Public safety scanner
- Full verification script
- Unit tests for display configuration and safety scanning

## Not Completed

Grass, light, rain, camera math, touch controls, audio, web packaging, and iOS
packaging are intentionally not implemented yet.

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

## Public Safety

Run the public safety check before publishing or pushing. Do not store
environment-specific absolute paths, personal identifiers, tokens, private keys,
or temporary logs in tracked files.

## Git

Commit and push require user approval.

## Next Wave

LC001 should build 3D math and camera foundations with tests before visual
feature work begins.

## Design Decisions

Keep Pyxel-specific code in the app layer and keep logic testable without Pyxel.
Use pathlib for relative resource resolution. Avoid speculative abstractions and
future directories until a wave needs them.
