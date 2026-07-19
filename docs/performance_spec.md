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

LC004 raises the field to 360 blades with 5 segments each, about 1,800 nominal
grass segments before near-clip rejection. It recomputes curve points every frame
from deterministic wind math, sorts blades by representative depth, and does not
regenerate the grass field or call random each frame. LC005 should re-check the
budget when sliced light adds more draw work.

LC005 first added light particles and 28 bottom-floor spark points. Current
tuning uses a 360-particle baseline with visible size variation from pixel
points to rare radius-3 circles. Grass lighting
evaluates only three points per blade: root, middle, and tip. Tip response is
weighted strongest, middle response is weaker, and root response is intentionally
rare. The bottom grid changes color from line midpoints instead of introducing a
large separate light-spot field. The light beam itself is not drawn in normal
view.

LC006 originally kept 360 grass blades, 5 nominal segments per blade, 48
particles, and 28 floor spark points. Current observation controls lower the
grass draw budget to 300 / 375 / 450 to avoid stage-3 spikes. Tapering means the
visible grass segment count is not the same as line draw calls; the debug HUD
reports visible blades, nominal segments, approximate line draw calls, lit
segments, and visible particles. In GUI review, HUD off, boundary on/off, light
on/off, wind on/off, zoom, and slow auto rotate held a stable 30 FPS feel. Web
packaging should re-profile background bands, taper line calls, and particle
drawing after browser scaling is introduced.

LC006.5 does not increase grass, particle, or spark counts. Camera inertia is
constant-time app state. Micro wind, cloud shadow, and particle random walk add a
few trigonometric calls per existing sample, keeping the performance profile in
the same shape as LC006.

LC007 adds 64 deterministic rain candidates. The default amount is 0.45, so
about 29 short drops are active when rain is enabled. Rain now draws vertical
segments across the cylinder without midpoint light gating, plus sparse
deterministic static rain streak flashes. There is no collision grid, splash
simulation, wet-ground surface, or per-frame random sampling in LC007.

LC008 keeps the 64 rain-candidate budget. Reaction work is driven by ground
impact events rather than every visible rain line. Each impact can create two
short-lived splash particles and can affect at most one nearby grass blade. Grass
reaction state is one small record per blade and decays each frame. Ground
wetness is a single scalar, not a surface simulation. There is still no puddle
grid, ripple solver, audio engine, or per-frame random sampling.

LC009 adds one constant-time environment state object and at most 28 active
grass-tip droplets. Droplet candidates are selected once, and droplets update by
simple hold/fall arithmetic. There is no all-blade water state, no puddle grid,
no ripple solver, no audio engine, and no per-frame random sampling.

The observation MENU pre-generates the stage-3 budgets, then draws active
prefixes. Stage 1 now uses 360 light particles and 300 grass blades; stage 3
raises those draw budgets to 1080 particles and 450 grass blades. Grass line
width is a drawing multiplier, not additional blade geometry. The rain stage
changes intensity only and does not increase the fixed drop pool size.
Light bands are five projected quadrilaterals with mixed width factors; they add
a fixed small draw cost and no new particle simulation.

LC010 adds one constant-time observation cycle object. It emits a phase, rain
multiplier, and light multiplier each frame. It does not allocate per-frame
weather objects, does not change the fixed rain drop pool, and does not
regenerate grass or particles.

LC011 adds at most nine active fireflies. Spawn and movement are fixed-seed and
kept in `FireflyField`, with no per-frame random target churn. Each firefly adds
only one small depth-sorted draw item and a few pixel operations when its blink
is visible. The FIREFLY stage changes only the active cap, through 3, 6, and 9
visitors.
