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
