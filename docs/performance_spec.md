# Performance Spec

The project targets a 448 x 852 internal render size at 30 FPS.

Grass, rain, particles, lighting, and reactions should each receive an explicit
cost budget as they are introduced. Avoid unnecessary object allocation in
per-frame loops. Trigonometric caches, level of detail, batching, and other
optimizations should be introduced when profiling or visual stress tests show a
real need.

Visual quality and measured performance should be reviewed separately. A scene
can look calm while still wasting frame time, and a fast scene can still fail the
intended atmosphere.
