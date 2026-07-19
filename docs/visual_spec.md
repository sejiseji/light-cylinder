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
width class vary by fixed-seed generation.

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

## Vertical Composition

The composition is tall and mobile-first. The internal render size is 448 x 852,
while the centered safe composition width is 393 pixels.

## Overscan

The left and right overscan regions are for grass tips, background, rain, and
particles that can be clipped without harming the composition. Important UI and
important scene beats should remain in the central safe area.
