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

LC003 used 280 grass blades with 5 segments each, for about 1,400 nominal grass
line segments before near-clip rejection. Grass parameters and static curve
points are generated once at app startup. The draw loop does not regenerate grass
or call random each frame. LC004 should re-check this budget when wind begins to
modify blade curves over time.

LC004 raises the field to 420 blades with 5 segments each, about 2,100 nominal
grass segments before near-clip rejection. It recomputes curve points every frame
from deterministic wind math, sorts blades by representative depth, and does not
regenerate the grass field or call random each frame. LC005 should re-check the
budget when sliced light adds more draw work.

LC005 adds 48 light particles and 28 bottom-floor spark points. Grass lighting
evaluates only three points per blade: root, middle, and tip. Tip response is
weighted strongest, middle response is weaker, and root response is intentionally
rare. The bottom grid changes color from line midpoints instead of introducing a
large separate light-spot field. The light beam itself is not drawn in normal
view.

LC006 keeps 420 grass blades, 5 nominal segments per blade, 48 particles, and 28
floor spark points. Tapering means the visible grass segment count is not the
same as line draw calls; the debug HUD reports visible blades, nominal segments,
approximate line draw calls, lit segments, and visible particles. In GUI review,
HUD off, boundary on/off, light on/off, wind on/off, zoom, and slow auto rotate
held a stable 30 FPS feel. Web packaging should re-profile background bands,
taper line calls, and particle drawing after browser scaling is introduced.

LC006.5 does not increase grass, particle, or spark counts. Camera inertia is
constant-time app state. Micro wind, cloud shadow, and particle random walk add a
few trigonometric calls per existing sample, keeping the performance profile in
the same shape as LC006.

LC007 adds 64 deterministic rain candidates. The default amount is 0.45, so
about 29 drops are active before light gating. Rain draws line segments only
after midpoint light checks pass, and it reuses one sampled wind vector per
frame. There is no collision grid, splash simulation, wet-ground surface, or
per-frame random sampling in LC007.
