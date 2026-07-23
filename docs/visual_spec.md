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
particles should reveal depth with clear small/large variation without
overwhelming the quiet mood.

Future natural elements should be admitted only when they thicken the feeling of
summer air. The intended sequence is foreground plant variation, rain memory,
sky, heat, horizon, and finally sound. This keeps the work anchored in a
midsummer afternoon and after-rain timeline instead of becoming a catalog of
summer symbols.

LC003 introduces static curved grass. Each blade uses a base point on the
cylinder bottom, a height, a natural XZ bend, and a quadratic curve so the bend
is weak near the root and strongest at the tip. Blade height, bend, color, and
width class vary by fixed-seed generation. Rendering keeps roots clearly
thicker and tapers toward the tip, so blades read as thin flat grass rather than
uniform wires.

The grass density later shifts from an even field to fixed-seed clumps. This
keeps the floor from becoming uniform noise, leaves visible soil openings, and
lets foxtails remain memory points without requiring a dense ordinary-grass
carpet.

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

LC005 makes light visible through media first. Particles stay air-like rather
than snow-like, and quiet tapered bands can hint at the shaft without becoming
the focal subject. The bands vary in angle and width, including a few thin
cuts of light rather than one uniform slab. Grass lighting is biased toward
blade tips: each blade samples only root, middle, and tip, with tip response
strongest. This should make leaves appear to cross into light while wind moves
them. The bottom grid can support boundary inspection, but normal viewing keeps
floor rings and radial lines hidden.
Light bands, grass, and particles are depth-sorted together so camera rotation
can change which elements appear in front of each band.

When debug is off, light-axis lines and radius circles must disappear. The viewer
should infer the beam from particles, grass tips, and the floor.

LC006 sets the visual priority order as grass, light, wind motion, particles,
cylinder space, then debug information. The default viewing state hides the HUD
and cylinder boundary so the first impression is a small illuminated grass field,
not a development screen. Boundary lines remain available with `B`, but use dim
far/vertical colors and a restrained near edge so the cylinder reads as an
observation volume rather than a cage.

The palette is centralized by use: dark background and bands, distant/normal/
foreground grass, lit/strongly lit grass, dry/wet/lit ground, dim/bright
particles, cylinder far/near edges, and debug accents. The colors stay within
Pyxel's standard palette and keep grass in green tones rather than yellow
blades.

The initial camera uses yaw -0.22, pitch 0.34, distance 430, and a target at 43
percent of cylinder height. This keeps grass centered in the safe composition,
leaves upper air for particles, and lets the light direction read without debug
guides.

HUD off must remove light debug rings, center/safe guide lines, and labels.
Bottom coordinate axes stay hidden by default. Debug mode is strictly an
inspection layer.

LC006.5 names the work `光の標本` / `Specimen of Light` while keeping Light
Cylinder as the development name. Observation polish adds short camera inertia,
micro wind, cloud-shadow breathing, and particle walk. These adjustments should
make the field feel held in air rather than mechanically animated. The active
palette remains `morning`, with `noon` and `evening` presets available as
configuration options for later curation.

LC007 introduces rain as a quiet environmental layer. The clear scene remains
the default. When rain is toggled on, drops are drawn across the full cylinder as
thin 1px-wide vertical streaks rather than only inside sampled light. Most drops
remain one of three fixed short lengths. Occasional longer vertical rain legs
flash for an instant at fixed positions and varied heights as a separate layer,
so they read as rainfall texture rather than stretched drops. Grass remains the
focal subject. Floor arrival is silent disappearance only; splashes, wet ground,
and grass contact are reserved for a later wave.
Rain uses palette colors 5, 12, 6, and 7 from far to near, adding depth without
changing the simple 1px vertical line language.

LC008 gives rain a restrained consequence. Ground impacts create tiny splash
pixels that vanish quickly, nearby grass can be pressed down for a moment, and
the floor grid can darken as wetness accumulates. When wet ground is also in
light, it may catch a weak reflection color. These reactions should feel like
touch, not spectacle: no puddles, ripples, retained droplets, thunder, or rain
audio are added.

LC009 adds after-rain as a quiet return toward clear air. Rain clouds should lift
slowly, wet floor cues should linger briefly, and only a few grass tips may hold
water. Droplets should appear as rare light catches, not jewelry or sparkle
noise, and should fall away naturally. The state should make time feel preserved
inside the cylinder without changing the work into a rain scene.

LC010 adds an optional observation cycle. The cycle should feel like the existing
piece breathing through one chapter: clear air, gathering shade, light rain,
fuller rain, stopping, after-rain, and return. It should not feel like a broad
weather simulator. MENU density and motion stages remain the viewer's chosen
baseline, while the cycle quietly moves temporary rain and light multipliers.

LC011 adds optional firefly visitors. They should read as visitors inside the
specimen, not a new subject or insect swarm. The default is OFF. When
enabled, zero fireflies for a while is acceptable, and the MENU count stage can
raise the active cap enough for the visitors to read clearly. They should drift
through the grass-top to middle-air region with slow, uneven blinking and longer
target paths than tiny local hovering. They may be slightly brighter inside the
light, but remain visible outside it because they carry their own glow. Near
visitors should become visibly larger than far visitors so the screen reads as a
shallow observed volume, not a flat sparkle layer. Rain should make them scarce,
and strong rain should stop new arrivals.

LC011.5 adds atmospheric background depth. The background should not read as
static, wallpaper, or all-over noise. It should feel like black air with a barely
visible dark-gray particulate layer, strongest in the middle air and near the
cylinder center. The floor/grass region and screen edges should remain quieter,
while the light-column neighborhood can raise density just enough to imply air
catching light. The effect is always on and intentionally has no MENU control.

LC012 adds foxtail grass as a grass relative, not as a new scene subject. It uses
three fixed-seed specimens. Compared with ordinary grass, they should
be taller, more singular, slightly yellow-green, and defined by seed heads with
six to ten sections. Stems sway slowly, while the heads lag slightly behind wind
motion. Rain can make them droop a little, and after-rain can leave a few
lingering raindrops on the seed heads. They should act as foreground memory
points, not compete with the grass field as the main subject.

LC012.6 turns the bottom plane into visible dark soil and reduces ordinary grass
budgets to 120, 180, and 240 blades. The soil should appear as sparse fixed
marks in normal viewing, not as the debug floor grid. Wetness can darken those
marks, and light can lift them toward a weak ocher reflection. Grass placement
uses fixed clumps with intentional open soil between them, so the lower count
reads as natural growth rather than missing detail. Boundary floor rings and
radial lines stay hidden until `B` is enabled.

LC013 should deepen after-rain droplets as rain memory, not morning dew. Use
language and behavior around `raindrop`, `lingering droplet`, or `after-rain
droplet`; avoid `dew` as the concept label.

LC014 should introduce summer cumulus through backlight rather than full scenic
cloud painting. On the current dark background, cloud edges can step through
yellow, white, dark gray, and black instead of a bright blue-sky palette.

LC014.5 should add heat haze only to distant sky elements such as cloud, mountain,
and sea layers. Grass, rain, fireflies, and the cylinder boundary should not
warp.

LC015 should keep the horizon minimal: mountain silhouette, a quiet sea line, and
weak reflection. Avoid detailed scenic illustration.

LC016 should add sound only after the image is strong enough to hold itself.
Cicadas and very weak wave sound are finishing ambience, not substitutes for
visual density.

## Vertical Composition

The composition is tall and mobile-first. The internal render size is 448 x 852,
while the centered safe composition width is 393 pixels.

## Overscan

The left and right overscan regions are for grass tips, background, rain, and
particles that can be clipped without harming the composition. Important UI and
important scene beats should remain in the central safe area.
