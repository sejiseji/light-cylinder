# Visual Spec

## Cylindrical Observation Area

The main scene is a tall cylindrical observation volume. LC002 represents this
with top and bottom rings, vertical guide lines, a center axis, and a sparse
bottom grid. Future waves should make the cylinder legible through light,
particles, grass silhouettes, rain, and occlusion rather than through a heavy
outline.

## Debug Boundary

The LC002 boundary display is a wireframe inspection tool, not final art. The
top and bottom rings make the volume readable, vertical guides establish height,
and the bottom grid makes orientation and depth clear while avoiding filled
surfaces that would hide line relationships in Pyxel.

## Natural Elements

Grass should eventually curve and react to wind. Light should arrive as sliced
bands or shafts. Wind should layer motion across height and depth. Rain and
particles should reveal depth without overwhelming the quiet mood.

LC003 introduces static curved grass. Each blade uses a base point on the
cylinder bottom, a height, a natural XZ bend, and a quadratic curve so the bend
is weak near the root and strongest at the tip. Blade height, bend, color, and
width class vary by fixed-seed generation. Rendering keeps roots slightly
thicker and tapers toward the tip, so blades read as thin flat grass rather than
uniform wires.

The grass density is biased toward the middle band of the cylinder floor, with
the center and outer edge slightly less dense. This keeps the floor direction and
cylinder boundary readable while avoiding a perfectly even artificial carpet.

## Light And Dark

Darkness is the baseline. Brightness should feel discovered, with clear contrast
between shaded regions and lit surfaces.

LC002 uses temporary Pyxel palette colors to separate far rings, near rings,
vertical guides, the center axis, and the bottom grid. These colors are for
debug readability and are not the final palette.

LC003 adds temporary green variants and depth shading for grass. Boundary lines
remain available with `B`, but grass remains the main visual subject when the
boundary is hidden.

LC004 animates the grass with layered wind. A shared base direction gives the
field coherence, while slow pulsing, spatial phase, and each blade's stored
phase prevent the grass from moving as one sheet. Height and stiffness affect
response: taller and softer blades move more, and roots remain visually stable
while tips carry most of the motion.

Gusts use a smooth envelope so the field gradually strengthens and relaxes. They
should read as a slow breath through the grass rather than a sudden snap.

LC005 makes light visible through media rather than drawing the light column
itself. Particles are sparse so they read as air, not snow. Grass lighting is
biased toward blade tips: each blade samples only root, middle, and tip, with
tip response strongest. This should make leaves appear to cross into light while
wind moves them. The bottom grid carries the first ground light impression, with
only a few extra bright floor points.

When debug is off, light-axis lines and radius circles must disappear. The viewer
should infer the beam from particles, grass tips, and the floor.

LC006 sets the visual priority order as grass, light, wind motion, particles,
cylinder space, then debug information. The default viewing state hides the HUD
and cylinder boundary so the first impression is a small illuminated grass field,
not a development screen. Boundary lines remain available with `B`, but use dim
far/vertical colors and a restrained near edge so the cylinder reads as an
observation volume rather than a cage.

The palette is centralized by use: dark background and bands, distant/normal/
foreground grass, lit/strongly lit grass, ground shadow/light, dim/bright
particles, cylinder far/near edges, and debug accents. The colors stay within
Pyxel's standard palette and favor a quiet green/yellow light relationship over
large bright surfaces.

The initial camera uses yaw -0.22, pitch 0.34, distance 430, and a target at 43
percent of cylinder height. This keeps grass centered in the safe composition,
leaves upper air for particles, and lets the light direction read without debug
guides.

HUD off must remove reference axes, light debug rings, center/safe guide lines,
and labels. Debug mode is strictly an inspection layer.

LC006.5 names the work `光の標本` / `Specimen of Light` while keeping Light
Cylinder as the development name. Observation polish adds short camera inertia,
micro wind, cloud-shadow breathing, and particle walk. These adjustments should
make the field feel held in air rather than mechanically animated. The active
palette remains `morning`, with `noon` and `evening` presets available as
configuration options for later curation.

LC007 introduces rain as a light-revealing medium. The clear scene remains the
default. When rain is toggled on, only drops that pass through enough sampled
light are drawn, so rain should read as thin illuminated streaks inside the beam
rather than a full weather layer. Wind gives the streaks a diagonal fall, but
grass remains the focal subject. Floor arrival is silent disappearance only;
splashes, wet ground, and grass contact are reserved for a later wave.

LC008 gives rain a restrained consequence. Ground impacts create tiny splash
pixels that vanish quickly, nearby grass can be pressed down for a moment, and
the floor grid can darken as wetness accumulates. When wet ground is also in
light, it may catch a weak reflection color. These reactions should feel like
touch, not spectacle: no puddles, ripples, retained droplets, thunder, or rain
audio are added.

## Vertical Composition

The composition is tall and mobile-first. The internal render size is 448 x 852,
while the centered safe composition width is 393 pixels.

## Overscan

The left and right overscan regions are for grass tips, background, rain, and
particles that can be clipped without harming the composition. Important UI and
important scene beats should remain in the central safe area.
