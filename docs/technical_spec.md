# Technical Spec

## Stack

Light Cylinder uses Python and Pyxel with a src package layout.

## Layout

`main.py` is a thin launcher. Package code lives under `src/light_cylinder`.
Configuration constants are centralized in `light_cylinder.config`.

## Coordinate System

LC001 adopts a right-handed coordinate system. X is horizontal, Y is vertical,
and Z is depth. The future cylinder center axis is Y, and the ground plane
starts at y = 0. The origin represents the future cylinder bottom center.

## Resolution Model

The reference device area is 393 x 852. The internal Pyxel render size is
448 x 852. The central 393-pixel region is the composition safe area. CSS display
scale and Pyxel internal resolution must remain separate concerns.

## Mobile Web Direction

The future web wrapper should preserve aspect ratio with contain-style fitting,
prefer 100dvh, account for safe-area insets, and use VisualViewport measurement
where needed. Browser UI changes must not alter the game coordinate system.

## Dependency Boundaries

Pyxel-specific rendering and input should stay close to the app layer. Pure
logic, math, procedural rules, and state transitions should remain testable
without importing Pyxel.

LC001 keeps `math3d.py`, `camera.py`, and `ControlIntent` Pyxel-independent.
`app.py` reads Pyxel input and renders projected debug geometry.

LC002 adds `CylinderWorld` as the Pyxel-independent geometry model for the
observation volume. The default cylinder is centered on the Y axis with radius
96 and height 300. Its bottom center is the origin and its top center is
`Vec3(0, 300, 0)`.

Cylinder containment uses:

```text
(x - center_x)^2 + (z - center_z)^2 <= radius^2
bottom_y <= y <= top_y
```

Boundary points are considered inside, with a small epsilon for floating-point
rounding. Ring points start at +X for theta = 0 and proceed with consistent
angle order for top and bottom rings. Bottom sampling uses `radius *
sqrt(u_radius)` and `2*pi*u_angle`, clamping normalized inputs to 0..1 so future
callers can inject deterministic random values safely.

## Orbit Camera

Light Cylinder uses an orbit camera because the work observes a subject from
around a fixed target rather than moving freely through a world. At yaw = 0 and
pitch = 0, the camera is conceptually in front of the target and looks along
positive Z. Camera-space depth is positive in front of the camera.

Projection uses:

```text
screen_x = center_x + camera_x * focal_length / depth
screen_y = center_y - camera_y * focal_length / depth
```

The negative sign in the Y projection maps world-up to screen-up because screen
Y increases downward. Points at or behind the near clip are not projected.

LC001 intentionally avoids a general Matrix library and Quaternion support.
The camera transform is target subtraction, inverse yaw, inverse pitch, distance
offset, near-clip rejection, and perspective projection.

LC002 targets the camera at 45 percent of the cylinder height, slightly below
center, to keep future grass placement visually important. Cylinder debug lines
are drawn as depth-sorted line segments by camera-space midpoint. No Z-buffer,
general renderer framework, or near-plane line clipping is introduced yet.

## Procedural Grass

LC003 adds `GrassBlade` and `GrassField` in `grass.py`. They do not import Pyxel.
Generation uses `random.Random(seed)` with `GRASS_SEED = 1729`, so identical
world and config inputs produce the same grass field.

Each blade stores:

- base point on the cylinder bottom
- height
- natural XZ bend
- stiffness
- phase
- width class
- color variant

The static centerline is sampled with:

```text
point = base + Vec3(0, height * t, 0) + natural_bend * (t * t)
```

`stiffness` and `phase` are stored for LC004 wind but are not animated in LC003.
Grass is generated from `CylinderWorld.sample_bottom_point`, then a simple
deterministic density weight makes the center and outer rim slightly sparser
than the middle band. Drawing sorts grass by the camera depth of each blade's
middle point, then draws each sampled segment from root to tip.

## Layered Wind

LC004 adds `WindField` in `weather.py`. It is Pyxel-independent and keeps
elapsed time internally. `app.py` advances it with `1 / TARGET_FPS` each frame.
The time value wraps at a long fixed interval to keep trigonometric inputs
bounded.

`WindField.sample(position, phase)` combines:

- a constant base direction
- slow sinusoidal wind-speed pulsing
- spatial phase from X/Z position
- each blade's stored phase
- a deterministic smooth gust envelope
- a small local direction sway

Wind vectors are horizontal: Y is always zero. The grass response computes a
wind bend from the sampled wind, blade height, and blade stiffness, then clamps
the result to a maximum ratio of blade height. `sample_blade_points` still keeps
the root fixed and applies bend progressively toward the tip.

The grass field itself is not regenerated per frame, and no per-frame random
sampling is used. LC004 recomputes curve points each frame so LC005 can add light
without depending on a heavy animation framework.

## Light Media

LC005 adds `LightBeam`, `LightParticle`, `LightGroundSpark`, and `LightField` in
`light.py`. These classes do not import Pyxel. `LightBeam` is a non-rendered
domain object: normal drawing code must not draw the beam surface or volume
directly. It only answers:

```text
intensity = LightBeam.intensity_at(point)
```

The beam intensity is based on axial range, radial distance from the beam axis,
a core radius, and end fading. `LightField` owns 360 deterministic particles and
28 deterministic floor spark points. The app advances light time once per frame
and draws only media that has sampled non-zero beam intensity:

- mixed-size particles inside the light volume
- grass root, middle, and tip samples, weighted tip > middle > root
- optional bottom grid midpoint color changes when boundary display is enabled
- a small number of floor spark pixels
- five mixed-width tapered light bands with dynamic angle and width

`L` toggles light media application for visual comparison. `D` toggles debug
mode; only debug mode draws the light axis and three radius guide rings. This is
the deliberate exception to the "do not draw the beam" rule.

## Presentation Integration

LC006 centralizes Pyxel palette choices in `config.py` as named `PALETTE_*`
constants. `app.py` uses small pure helpers for color selection:

- `select_grass_color`
- `select_grass_light_color`
- `select_floor_color`
- `select_particle_color`

These helpers are covered by tests and keep threshold decisions out of raw
draw calls.

The default view is an exhibition state: debug hidden, boundary hidden, light
on, wind on, auto rotate off. `R` resets only the camera to the default viewing
composition; it does not regenerate grass, wind, particles, or light data.

LC006 draw order is:

1. fixed dark background with atmospheric depth dither
2. optional floor grid and cylinder boundary
3. depth-sorted grass, light particles, and mixed-width tapered light bands
4. floor spark pixels
5. debug-only safe area, counters, light axis, and light guide rings

The initial camera values are yaw -0.22, pitch 0.34, distance 455, and target Y
at `CYLINDER_HEIGHT * 0.43`. Auto rotate uses a slow 0.0035 radians per frame,
roughly a one-minute orbit at 30 FPS. Auto rotate also adds a subtle pitch sway
around a mutable pitch center.

LC006.5 adds observation polish without adding a new natural phenomenon. Manual
camera input uses short inertia through app-level yaw, pitch, and zoom velocity
state with `CAMERA_INERTIA_DECAY = 0.68`. Manual pitch input updates the auto
pitch sway center so automatic viewing continues from the observer's chosen
vertical angle. `R` resets the camera, pitch sway center, and these velocities.

Light pulse is reframed as cloud shadow. `LightField.intensity_multiplier`
slowly darkens and returns between 0.84 and 1.0 using
`LIGHT_CLOUD_SHADOW_RATE = 0.075`, `LIGHT_CLOUD_SHADOW_AMOUNT = 0.16`, and
`LIGHT_CLOUD_SHADOW_FLOOR = 0.78`. Wind adds a small micro-breath term on top of
the LC006 base wind and gust model. Particle positions add a mild axis attraction
and sinusoidal walk so particles drift toward and away from the light column
without increasing count.

Palette settings remain in `config.py`. Three preset dictionaries are available:
`morning`, `noon`, and `evening`. The active preset is `morning`; changing the
setting updates the named `PALETTE_*` constants at import time. LC006.5 does not
add a runtime palette toggle.

## Rain Through Light

LC007 adds `RainDrop` and `RainField` in `rain.py`. They do not import Pyxel.
The clear observation state remains the default; `N` toggles rain, and `Q` / `E`
decrease or increase the rain amount. Rain amount clamps to the normalized range
0..1 and selects a prefix of the deterministic 64-drop candidate field.

Rain samples the cylinder top disk with a fixed seed. Candidates cover the full
cylinder rather than being biased toward the light corridor. Drops fall downward
over time and disappear when they reach the floor by wrapping back to the top on
the next cycle. Wind no longer affects rain drift or tail tilt; rain is rendered
as 1px-wide vertical streaks across the cylinder. Falling drops use three fixed
short lengths. Longer rain legs are separate static streak candidates: they do
not fall, move, or stretch, and they flash for only an instant at fixed
positions among the falling short drops. Their candidate count is intentionally
higher than before, with varied head heights so the long flashes can appear low,
mid, or high in the cylinder.
Rain color uses four depth tiers from far to near: palette colors 5, 12, 6, and
7. Bright near/mid rain can also resolve to the nearest tier color 7, preserving
depth while keeping strong streaks visible.

Normal rendering still does not draw the light beam directly. Rain is visible
throughout the cylinder when enabled; light is carried by particles, grass tips,
floor response, and the mixed light bands.

LC007 draw order is:

1. fixed dark background with atmospheric depth dither
2. optional floor grid and cylinder boundary
3. full-cylinder vertical rain segments
4. depth-sorted grass, light particles, mixed-width tapered light bands, and yellow accents
5. floor spark pixels
6. debug-only safe area, counters, light axis, and light guide rings

## Rain Reactions

LC008 adds `RainImpact` events in `rain.py` and reaction state in
`reactions.py`. These classes do not import Pyxel. `RainDrop` reports a ground
impact only when its normalized fall cycle wraps between the previous and current
frame. The app uses active rain drops only, so the clear default scene does not
accumulate hidden reaction state.

`GroundReactionField` owns:

- short-lived `SplashParticle` instances generated from impact events
- a single wetness value that increases from impacts
- slow drying after rain stops

`GrassReactionField` owns per-blade reaction state separate from immutable
`GrassBlade` data. Each impact checks for the nearest blade within a small
horizontal radius and applies a short downward-biased bend. The reaction decays
quickly and is added to, not substituted for, wind bend. It should read as a
local press rather than a second wind system.

LC008 draw order is:

1. fixed dark background with atmospheric depth dither
2. optional floor grid and cylinder boundary with light/wetness-aware midpoint color
3. full-cylinder vertical rain segments
4. splash pixels
5. depth-sorted grass/reactions, light particles, mixed-width tapered light bands, and yellow accents
6. floor spark pixels
7. debug-only safe area, counters, light axis, and light guide rings

Wet floor shading is intentionally coarse: it can darken the optional floor grid
and allows a weak reflection color only where light is already present. LC008
does not add puddles, ripple simulation, grass-tip water retention, thunder, rain
audio, or after-rain transitions.

## After Rain

LC009 adds `EnvironmentState` in `environment.py`. It is Pyxel-independent and
keeps the weather model deliberately small:

```text
CLEAR
RAIN
AFTER_RAIN
```

`N` still toggles rain. Turning rain off while ground wetness remains enters
`AFTER_RAIN`; otherwise the scene returns to `CLEAR`. During after-rain, the
environment slowly reduces its extra cloud shadow, keeps a weak wet-floor
reflection afterglow, changes drying speed based on remaining wetness, and
returns naturally to `CLEAR` after a short minimum duration and enough drying.

LC009 does not alter `LightField` internals. Instead, app-level light sampling
multiplies the existing CloudShadow value by `EnvironmentState.light_multiplier`.
This preserves the LC006.5 CloudShadow implementation while allowing rain clouds
to clear after rainfall.

Tip droplets are stored in `TipDropletField` in `reactions.py`. Only a fixed
small candidate set of grass blades can receive droplets, and droplets are seeded
only when transitioning from `RAIN` to `AFTER_RAIN`. They are rendered only if
their sampled point is inside enough light. Each droplet holds for a short
deterministic time, then falls vertically and disappears. LC009 intentionally
does not attach water to all baseline blades.

LC009 draw order keeps droplets quiet:

1. fixed dark background with atmospheric depth dither
2. optional floor grid and cylinder boundary with light/wetness/reflection-aware midpoint color
3. full-cylinder vertical rain segments
4. splash pixels
5. depth-sorted grass/reactions, light particles, mixed-width tapered light bands, and yellow accents
6. light-gated tip droplet pixels
7. floor spark pixels
8. debug-only safe area, counters, light axis, and light guide rings

Puddles, ripple simulation, thunder, rain audio, and all-grass droplet retention
remain out of scope.

## Observation Menu

The top-right MENU button opens an overlay panel with six 1-3 stage controls
and an auto-rotate ON/OFF toggle.
All controls start at stage 1, which is the LC009 baseline:

- photon density: draws the first 360, 720, or 1080 generated light particles
- grass density: draws the first 300, 375, or 450 generated grass blades
- wind strength: keeps the steady wind anchor, amplifies motion by 1.0, 1.85, or
  2.7, and advances wind motion time by 1.0, 1.45, or 2.0
- rain amount: sets rain intensity to 0.45, 0.65, or 0.85
- auto rotate speed: multiplies auto-rotate by 1.0, 1.45, or 1.9
- firefly visitor count: caps active visitors at 3, 6, or 9
- AUTO toggle: changes the same auto-rotate state as the `X` key
- RAIN toggle: changes the same rain ON/OFF state as the `N` key
- FIREFLY toggle: changes the same optional visitor state as the `F` key

The app pre-generates the maximum particle and grass budgets, then draws the
active prefix for the selected stage. This keeps stage changes deterministic and
avoids regenerating scene data while the observation is running.
The grass control changes draw density, not the deterministic generated field.
Light bands are inserted into the same depth-sorted draw list as grass blades so
rotation can affect the apparent front/back relationship between blades and
bands.
The rain amount control changes only the amount preset and does not toggle rain
on or off. Settings are not persisted; every launch starts from stage 1.

## Observation Cycle

LC010 adds `ObservationCycle` in `observation_cycle.py`. It is Pyxel-independent
and emits temporary playback values:

```text
CLEAR
SHADOW
LIGHT_RAIN
RAIN
AFTER_RAIN
```

The app owns the bridge between cycle samples and existing systems. While the
cycle is enabled, rain intensity is:

```text
MENU rain stage intensity * cycle rain multiplier
```

The stored MENU stage is not changed. `LIGHT_RAIN` ramps up to a partial
multiplier; `RAIN` uses the full selected stage amount; `AFTER_RAIN` turns rain
off and lets the existing `EnvironmentState`, wetness, reflection, and droplet
logic resolve naturally. The cycle also applies a temporary light multiplier for
deepening and lifting CloudShadow without altering `LightField` internals.

Manual `N`, `Q`, or `E` rain input disables the cycle before applying the manual
operation, so returning to direct control does not inherit hidden cycle state.

## Firefly Visitors

LC011 adds `Firefly` and `FireflyField` in `firefly.py`. They do not import
Pyxel. Fireflies are optional visitors, not a permanent ambient particle field:
the default state is OFF, the active cap is nine at stage 3, and fixed-seed
spawn delays still create periods with no fireflies at all.

Each firefly stores position, velocity, target, age, lifetime, glow phase, and
glow speed. Update uses target attraction, slow wander, boundary avoidance, and
a very weak wind influence. Targets are sampled inside the cylinder from just
above the grass layer to the mid-volume, with a preferred minimum travel
distance, so movement stays smooth, contained, and visibly crosses more of the
scene.
Strong rain prevents new firefly spawns; lighter rain stretches the spawn delay,
and after-rain allows rare returns. Rendering remains in `app.py`, where
fireflies are inserted into the same depth-sorted list as grass, light bands, and
photons. Unlike photons and rain, fireflies remain visible outside the light beam
because they are their own small light source. Screen size also uses camera
depth: nearer fireflies can draw as larger glow circles, while far visitors stay
near single-pixel points.

## Atmospheric Background Depth

LC011.5 changes only the background rendering. `app.py` draws a two-color
pseudo-transparency layer after clearing the screen: black remains the base, and
palette background-band color appears as sparse fixed-hash points. Density is
highest around the centered safe composition and middle air, fades near the
screen edges, weakens around the grass/floor region, and gains a small boost near
the projected light axis. CloudShadow reduces the density slightly so the air
darkens with the existing light state.

The pattern is not random per frame. It uses a deterministic hash over screen
coordinates plus a slow integer phase derived from light-field elapsed time, so
the layer breathes by a pixel-scale drift rather than becoming noise. No MENU
control is added in this wave.

## Foxtail Grass

LC012 adds `Foxtail`, `FoxtailShape`, and `FoxtailField` in `foxtail.py`. They do
not import Pyxel. Foxtails are treated as grass relatives rather than generic
decorations: the fixed-seed field creates three tall, singular specimens inside
the cylinder. Heights are 1.4 to 1.8 times the ordinary grass max height, with a
five-segment stem and a six-to-ten-section seed head.

`sample_foxtail_shape` accepts wind, rain weight, and after-rain weight. The
stem follows wind slowly, while the seed head uses a smaller lagged bend so it
trails the stem. Rain adds a modest downward droop, and after-rain can emit a
couple of deterministic head droplet positions. Rendering remains in `app.py`,
where foxtails join the same depth-sorted list as grass, light bands, photons,
and fireflies.

## Resource Resolution

Runtime resources should be resolved relative to source files with pathlib or
project-root-relative paths. Environment-specific absolute paths must not be
stored in tracked files.

## Randomness

Future procedural systems should accept seed injection so scenes can be reproduced
for tests and visual review.

## Abstraction Policy

Avoid broad frameworks and speculative layers. Add structure when a later wave
creates real duplication, shared behavior, or testable domain logic.
