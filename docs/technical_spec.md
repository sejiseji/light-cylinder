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
96 and height 240. Its bottom center is the origin and its top center is
`Vec3(0, 240, 0)`.

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
a core radius, and end fading. `LightField` owns 48 deterministic particles and
28 deterministic floor spark points. The app advances light time once per frame
and draws only media that has sampled non-zero beam intensity:

- sparse particles inside the light volume
- grass root, middle, and tip samples, weighted tip > middle > root
- bottom grid midpoint color changes
- a small number of floor spark pixels

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

1. fixed dark background with sparse vertical bands
2. floor grid with light-aware midpoint color
3. optional cylinder boundary
4. light particles
5. wind-sampled, depth-sorted grass
6. floor spark pixels
7. debug-only axes, reference points, safe area, and light guides

The initial camera values are yaw -0.22, pitch 0.34, distance 430, and target Y
at `CYLINDER_HEIGHT * 0.43`. Auto rotate uses a slow 0.0035 radians per frame,
roughly a one-minute orbit at 30 FPS. No automatic pitch oscillation is added in
LC006.

LC006.5 adds observation polish without adding a new natural phenomenon. Manual
camera input uses short inertia through app-level yaw, pitch, and zoom velocity
state with `CAMERA_INERTIA_DECAY = 0.68`. `R` resets both the camera and these
velocities.

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

Rain samples the cylinder top disk with a fixed seed. Most candidates are biased
toward the light corridor so the rain can reveal the beam without requiring a
full-screen downpour. Drops fall downward over time and disappear when they
reach the floor by wrapping back to the top on the next cycle. Wind affects the
horizontal drift and tail tilt, so the rain moves as diagonal streaks rather than
vertical bars.

Normal rendering still does not draw the light beam. Rain is drawn only when a
segment midpoint samples enough light from `LightBeam.intensity_at(point)` after
the cloud-shadow multiplier is applied. This keeps rain as another medium for
seeing the light, not a separate weather spectacle.

LC007 draw order is:

1. fixed dark background with sparse vertical bands
2. floor grid with light-aware midpoint color
3. optional cylinder boundary
4. light particles
5. light-gated rain segments
6. wind-sampled, depth-sorted grass
7. floor spark pixels
8. debug-only axes, reference points, safe area, counters, and light guides

Grass contact, splash points, wet ground, rain sound, and after-rain state are
left for later waves.

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
