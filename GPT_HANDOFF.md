# GPT Handoff

## Project

Light Cylinder is the development name for `Specimen of Light` / `光の標本`, a
mobile-first Pyxel observation work centered on sliced light inside a tall
cylindrical natural space.

## Current Wave

LC008 Rain Reactions.

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
- Work title set to `Specimen of Light` / `光の標本`
- Short camera inertia for yaw, pitch, and zoom
- Micro wind term layered into `WindField.sample`
- Cloud-shadow light multiplier replacing direct pulse wording
- Particle axis attraction and small random-walk motion
- Setting-only palette presets for morning, noon, and evening
- Pyxel-independent `RainDrop` and `RainField`
- Optional rain with `N`, using `Q` and `E` for amount changes
- Wind-slanted rain segments that disappear at the cylinder floor
- Rain rendering gated by light intensity so only the light-crossing drops show
- Rain candidates biased toward the light corridor so visible rain stays sparse
  but legible
- Pyxel-independent `GroundReactionField` and `GrassReactionField`
- Ground impact events from active rain drops
- Short-lived splash pixels at ground arrival
- Global ground wetness with slow drying after rain stops
- Local grass press reactions stored separately from static `GrassBlade` data
- Wet floor darkening and weak light reflection

## Not Completed

Puddles, ripple simulation, retained grass-tip droplets, thunder, rain audio,
after-rain weather transition, touch controls, web packaging, and iOS packaging
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
- Mouse drag: yaw and pitch
- A and S: zoom
- Mouse wheel: zoom
- X: toggle auto rotate
- B: toggle cylinder boundary
- W: toggle wind
- L: toggle light media
- N: toggle rain
- Q and E: decrease and increase rain amount
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
- camera inertia decay: 0.68
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
- Micro wind rate: 0.19
- Micro wind amount: 0.10

## Light

- Beam origin: `(-34, 246, -22)`
- Beam direction: `(0.22, -1.0, 0.18)` normalized
- Beam length: 285
- Beam radius: 44
- Core radius: 14
- Particles: 48
- Floor sparks: 28
- Cloud shadow rate: 0.075
- Cloud shadow amount: 0.16
- Cloud shadow floor: 0.78
- Particle drift range: -2.6 to 4.8
- Particle axis attraction: 0.07
- Particle walk rate: 0.31
- Particle walk amount: 2.8
- Normal rendering: no direct beam drawing
- Debug rendering: axis line and three radius rings

## Rain

- Seed: 9182
- Candidate drops: 64
- Default amount: 0.45
- Amount step: 0.15
- Fall speed range: 96 to 142 world units per second
- Segment length range: 8 to 15 world units
- Wind drift scale: 34
- Wind tilt scale: 10
- Light visibility threshold: 0.16
- Bright rain threshold: 0.52
- Initial state: rain off, clear scene preserved
- Generation: fixed-seed top-disk candidates, mostly biased to the light corridor
- Rendering: line segments only, no direct rain volume or splash effect

## Rain Reactions

- Splash lifetime: 0.22 seconds
- Splashes per impact: 2
- Splash speed: 16
- Splash gravity: 92
- Ground wetness gain per impact: 0.004
- Ground dry rate: 0.035 per second
- Grass impact radius: 12
- Grass impact decay rate: 4.2 per second
- Grass reaction bend scale: 4.8
- Grass reaction state is separate from immutable `GrassBlade` data
- Initial state: wetness zero, no splashes, no active grass reactions

## Palette

- active preset: morning
- available presets: morning, noon, evening
- runtime palette toggle: not implemented
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
- rain: off
- auto rotate: off

Use `D` for inspection and `B` to compare the restrained cylinder boundary.
Use `N` to compare clear and rainy observation states. Use `R` to restore the
presentation camera.

## Visual Acceptance

From LC005 onward, review `docs/visual_acceptance.md` after implementation.
LC006 GUI review found the HUD-off scene readable as a viewing screen: grass
remains primary, light direction reads through sparse particles and tip lighting,
particles do not read as snow, boundary ON is subdued, and HUD OFF can be
watched for at least one minute without the auto rotate feeling too fast.
LC006.5 added Artistic Review notes to every wave result from now on.

## Performance

- Grass count: 420
- Nominal segments: 2,100
- Typical visible particles in debug review: about 29 to 36
- Rain candidates: 64, with about 29 active at the default 0.45 amount before
  light gating
- LC008 reaction work is impact-event based; no puddle grid, ripple simulation,
  audio, or per-frame random sampling is added
- Approximate line draw calls are reported in debug HUD
- GUI review kept a stable 30 FPS feel with light, wind, particles, boundary
  on/off, zoom, and slow auto rotate.

## Public Safety

Run the public safety check before publishing or pushing. Do not store
environment-specific absolute paths, personal identifiers, tokens, private keys,
or temporary logs in tracked files.

## Git

LC000 through LC007 were committed and pushed with approval, and
`prototype-v0.1.0` marks the first observation prototype. LC008 is in the working
tree until explicitly approved for commit. Future commits, pushes, and tags
require user approval.

## Next Wave

Next work should review whether LC008 needs visual balancing before moving into
weather transitions. Puddles, ripples, retained droplets, and after-rain states
remain intentionally separate.

## Design Decisions

Keep Pyxel-specific code in the app layer and keep logic testable without Pyxel.
Use pathlib for relative resource resolution. Avoid speculative abstractions and
future directories until a wave needs them.
