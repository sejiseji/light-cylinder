# GPT Handoff

## Project

Light Cylinder is the development name for `Specimen of Light` / `光の標本`, a
mobile-first Pyxel observation work centered on sliced light inside a tall
cylindrical natural space.

## Current Wave

LC012 Foxtail Grass.

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
- 360 deterministic light particles inside the beam volume at baseline
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
- Auto rotate includes subtle pitch sway around the latest manual pitch baseline
- Micro wind term layered into `WindField.sample`
- Cloud-shadow light multiplier replacing direct pulse wording
- Particle axis attraction and small random-walk motion
- Setting-only palette presets for morning, noon, and evening
- Pyxel-independent `RainDrop` and `RainField`
- Optional rain with `N`, using `Q` and `E` for amount changes
- Vertical 1px-wide rain lines across the full cylinder, independent from light
  visibility; falling short drops use three fixed lengths, while separate static
  long rain streaks flash for an instant at varied heights without moving or
  stretching
- Rain candidates sample the cylinder disk instead of the light corridor
- Pyxel-independent `GroundReactionField` and `GrassReactionField`
- Ground impact events from active rain drops
- Short-lived splash pixels at ground arrival
- Global ground wetness with slow drying after rain stops
- Local grass press reactions stored separately from static `GrassBlade` data
- Wet floor darkening and weak light reflection
- Pyxel-independent `EnvironmentState` with `CLEAR`, `RAIN`, and `AFTER_RAIN`
- Rain OFF transition into after-rain recovery when wetness remains
- CloudShadow recovery multiplier layered over the existing light field
- Wet-floor reflection afterglow that can outlive raw wetness
- Small fixed candidate set for grass-tip droplets after rain
- Tip droplets visible only when they sample enough light
- Tip droplets naturally fall and disappear
- Top-right MENU panel for 1-3 stage observation tuning
- Stage 1 keeps the baseline look for photons, grass, wind, rain, and auto rotate
- FIREFLY stage caps active visitors at 3, 6, or 9
- MENU `AUTO` toggle changes the same auto-rotate state as the `X` key
- MENU `RAIN` toggle changes the same rain ON/OFF state as the `N` key
- Pyxel-independent `ObservationCycle`
- `M` toggle for clear, shadow, light-rain, rain, after-rain, clear playback
- Observation cycle uses MENU rain stage as a base amount without mutating stages
- Manual `N`, `Q`, or `E` input exits the observation cycle before applying rain
  control
- Readable 3x pixel HUD and MENU text
- 2x grass root width multiplier with tapered tips
- 360-particle baseline light field and 1080-particle stage-3 budget
- Photon draw sizes vary clearly from pixel points to radius-3 circles
- Five dynamic mixed-width tapered light bands from upper beam to floor
- Bottom coordinate axes hidden in normal and debug viewing
- Bottom floor rings and radial lines hidden unless boundary display is enabled
- Optional firefly visitors with `F` and MENU `FIREFLY`, initial state OFF
- Pyxel-independent `Firefly` and `FireflyField`
- Fireflies stay inside the cylinder, cap at nine active visitors, blink slowly,
  and use fixed-seed target-seeking drift with a preferred minimum target
  distance
- Firefly screen size grows toward the camera for stronger front/back depth
- Strong rain prevents new firefly arrivals; light rain and after-rain stretch
  the spawn delay
- Sparse two-color atmospheric background dither, ON by default and not exposed
  in MENU
- Background dither density varies by safe-area center distance, height, light
  axis proximity, and CloudShadow
- Pyxel-independent `Foxtail`, `FoxtailShape`, and `FoxtailField`
- Three fixed-seed foxtail specimens inside the cylinder
- Foxtail stems sway slowly; seed heads use lagged wind response
- Rain makes foxtail heads droop slightly; after-rain can leave a couple of head
  raindrops

## Not Completed

Puddles, ripple simulation, thunder, rain audio, all-grass water drops, touch
controls, web packaging, and iOS packaging are intentionally not implemented yet.

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
- F: toggle firefly visitors
- M: toggle observation cycle
- Q and E: decrease and increase rain amount
- R: reset camera
- D: toggle debug HUD and light guides
- ESC: quit

## Camera

The LC001 camera is an orbit camera. At yaw = 0 and pitch = 0, it looks along
positive Z toward the target. Camera-space depth is positive in front of the
camera. Points at or behind the near clip are skipped rather than clipped.

The LC006 camera target is `Vec3(0, CYLINDER_HEIGHT * 0.43, 0)`, with default
radius 96, height 300, 32 radial segments, and 8 vertical guides.

Initial camera:

- yaw: -0.22
- pitch: 0.34
- distance: 455
- auto rotate speed: 0.0035 radians per frame
- camera inertia decay: 0.68
- auto pitch: subtle sway around the latest manual pitch baseline

## Grass

- Count: 300 baseline, 450 stage-3 draw budget
- Segments per blade: 5
- Seed: 1729
- Height range: 18 to 46
- Bend range: 2 to 15
- Stiffness range: 0.45 to 1.0
- Density: slightly sparse at center and rim, densest around the middle band
- Animation: layered wind in LC004

## Wind

- Base direction angle: 0.35 radians
- Base speed: 0.65
- Response scale: 17.0
- Slow pulse: sinusoidal
- Spatial phase: X/Z position
- Blade phase: `GrassBlade.phase`
- Gust: deterministic sin-squared envelope
- Wind max bend: 68 percent of blade height
- Base pulse rate: 0.42
- Base pulse amount: 0.38
- Direction sway rate: 0.37
- Gust interval: 12.0
- Gust duration: 5.5
- Micro wind rate: 0.19
- Micro wind amount: 0.16

## Light

- Beam origin: `(-34, 312, -22)`
- Beam direction: `(0.22, -1.0, 0.18)` normalized
- Beam length: 360
- Beam radius: 44
- Core radius: 14
- Particles: 360 baseline, 1080 stage-3 draw budget
- Floor sparks: 28
- Cloud shadow rate: 0.075
- Cloud shadow amount: 0.16
- Cloud shadow floor: 0.78
- Particle drift range: -2.6 to 4.8
- Particle axis attraction: 0.07
- Particle walk rate: 0.31
- Particle walk amount: 2.8
- Normal rendering: particles, grass tips, floor light, restrained mixed-width
  tapered light bands, and three thin yellow accent streaks
- Debug rendering: light axis line and three radius rings

## Rain

- Seed: 9182
- Candidate drops: 64
- Default amount: 0.45
- Amount step: 0.15
- Fall speed range: 96 to 142 world units per second
- Segment lengths: fixed 7, 10, or 13 world units
- Long static streaks: 126 to 258 world units, flash for an instant
- Wind drift scale: 0
- Wind tilt scale: 0
- Bright rain threshold: 0.94
- Initial state: rain off, clear scene preserved
- Generation: fixed-seed top-disk candidates across the cylinder
- Rendering: vertical 1px line segments across the cylinder, with depth colors
  5, 12, 6, and 7

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

## After Rain

- Environment phases: `CLEAR`, `RAIN`, `AFTER_RAIN`
- Minimum after-rain duration: 7.0 seconds
- After-rain entry wetness: 0.05
- Clear return wetness: 0.035
- Cloud recovery rate: 0.055
- Additional shadow amount: 0.10
- Wet reflection decay rate: 0.045
- After-rain dry-rate range: 0.38 to 1.25
- Tip droplet candidates: 28 blades
- Tip droplet light threshold: 0.24
- Tip droplet hold range: 2.8 to 8.4 seconds
- Tip droplet fall speed: 18

## Palette

- active preset: morning
- available presets: morning, noon, evening
- runtime palette toggle: not implemented
- background: 1
- background band: 2
- distant grass: 3
- normal grass: 11
- foreground/lit grass: 3
- strongly lit grass: 11
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
- fireflies: off
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

- Grass count: 300 baseline, 450 stage-3 draw budget
- Nominal segments: 1,800 baseline, 2,700 stage-3 draw budget
- Typical visible particles in debug review: expected to rise with the 360
  particle baseline
- Light particles: 360 baseline, 1080 stage-3 draw budget
- Rain candidates: 64, with about 29 active at the default 0.45 amount
- LC008 reaction work is impact-event based; no puddle grid, ripple simulation,
  audio, or per-frame random sampling is added
- LC009 adds one small environment state object and at most 28 tip droplets;
  droplet candidates are fixed and no per-frame random sampling is added
- LC010 adds one constant-time observation cycle object; it does not regenerate
  grass, particles, or rain candidates
- LC011 adds at most nine fireflies, depth-sorted with grass, light bands, and
  photons; the FIREFLY stage changes the cap through 3, 6, and 9
- LC011.5 adds sparse fixed-hash background dither every 4 pixels, with no
  per-frame random sampling
- LC012 adds three foxtails with five stem segments and six to ten head sections
- Approximate line draw calls are reported in debug HUD
- GUI review kept a stable 30 FPS feel with light, wind, particles, boundary
  on/off, zoom, and slow auto rotate.

## Public Safety

Run the public safety check before publishing or pushing. Do not store
environment-specific absolute paths, personal identifiers, tokens, private keys,
or temporary logs in tracked files.

## Git

LC000 through LC011.5 plus environmental-control refinements were committed and
pushed with approval, and `prototype-v0.1.0` marks the first observation
prototype. LC012 is in the working tree until explicitly approved for commit.
Future commits, pushes, and tags require user approval.

## Next Wave

Next work should move to LC013 After-Rain Droplets after visually reviewing
whether foxtails stay plant-like and do not steal focus. The roadmap is now:
LC013 After-Rain Droplets, LC014 Summer Cumulus, LC014.5 Heat Haze, LC015 Distant
Horizon, LC016 Summer Ambience, LC017 Presentation Pass, then `prototype-v0.3.0`.

The selection rule is to add only what makes the summer air feel denser. Avoid
summer-coded objects that introduce a different speed, human story, or season.
Puddles, ripples, thunder, and rain audio remain intentionally separate.

## Design Decisions

Keep Pyxel-specific code in the app layer and keep logic testable without Pyxel.
Use pathlib for relative resource resolution. Avoid speculative abstractions and
future directories until a wave needs them.
