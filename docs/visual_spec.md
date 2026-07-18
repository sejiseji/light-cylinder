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

## Light And Dark

Darkness is the baseline. Brightness should feel discovered, with clear contrast
between shaded regions and lit surfaces.

LC002 uses temporary Pyxel palette colors to separate far rings, near rings,
vertical guides, the center axis, and the bottom grid. These colors are for
debug readability and are not the final palette.

## Vertical Composition

The composition is tall and mobile-first. The internal render size is 448 x 852,
while the centered safe composition width is 393 pixels.

## Overscan

The left and right overscan regions are for grass tips, background, rain, and
particles that can be clipped without harming the composition. Important UI and
important scene beats should remain in the central safe area.
