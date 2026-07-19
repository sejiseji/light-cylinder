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

LC003 uses 280 grass blades with 5 segments each, for about 1,400 nominal grass
line segments before near-clip rejection. Grass parameters and static curve
points are generated once at app startup. The draw loop does not regenerate grass
or call random each frame. LC004 should re-check this budget when wind begins to
modify blade curves over time.
