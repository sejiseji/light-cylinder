# Technical Spec

## Stack

Light Cylinder uses Python and Pyxel with a src package layout.

## Layout

`main.py` is a thin launcher. Package code lives under `src/light_cylinder`.
Configuration constants are centralized in `light_cylinder.config`.

## Coordinate System

Future 3D-like logic will use X for horizontal movement, Y for vertical movement,
and Z for depth. The cylinder center axis is Y. The ground plane starts at y = 0.

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
