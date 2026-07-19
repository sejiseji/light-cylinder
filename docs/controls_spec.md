# Controls Spec

LC001 implements keyboard controls for orbit-camera inspection. LC004 adds mouse
controls so the scene can be tested quickly during visual iteration. LC005 adds
light comparison and makes debug mode the place for light-axis inspection. LC006
starts in a viewing state and adds camera reset. LC007 adds optional rain
comparison while keeping the clear scene as the default. LC010 adds an optional
observation cycle:

- Left and Right: yaw left and right around the target
- Up and Down: pitch the view up and down
- Mouse drag: yaw and pitch around the target
- A and S: zoom in and out
- Mouse wheel: zoom in and out
- X: toggle auto rotate
- B: toggle cylinder boundary visibility
- W: toggle wind application
- L: toggle light media application
- N: toggle rain
- M: toggle observation cycle
- Q and E: decrease and increase rain amount
- R: reset camera to the viewing composition
- D: toggle debug HUD, camera details, and light guides
- Top-right MENU button: open the observation tuning panel
- ESC: exit

The readable MENU panel exposes five 1-3 stage controls: photon density, grass
density, wind strength, rain amount, and auto-rotate speed. WIND stages use
clearer 1.0, 1.85, and 2.7 motion multipliers around the same steady wind
anchor, so the stage 1 sway becomes more energetic instead of shifting to a new
resting bend. WIND stages also speed up the wind motion time by 1.0, 1.45, and
2.0, so higher stages sway faster as well as wider. It also exposes an
`AUTO` ON/OFF toggle for auto rotate and a `RAIN` ON/OFF toggle for rain. Stage
1 is the current baseline composition for all five stage controls. Settings are
session-only and reset to stage 1 on restart. The `AMOUNT` stage changes only
the rain amount preset; rain ON/OFF is controlled by either `N` or MENU `RAIN`.
The panel captures mouse input only inside its button and panel region, so
normal drag rotation continues elsewhere.

When auto rotate is enabled, the camera orbits horizontally and adds a subtle
vertical sway. Manual pitch steering through Up/Down or drag changes the pitch
baseline for that sway instead of snapping back to the startup angle.

The observation cycle is a temporary playback layer over the existing scene. It
does not change MENU stages. It multiplies the current rain stage while moving
through light rain and normal rain, and it applies a temporary cloud-shadow
multiplier while clouds gather and clear. Pressing `N`, `Q`, or `E` exits the
cycle and returns to manual rain control.

Touch controls are planned for a later wave after camera and scene behavior are
stable enough to test on mobile layouts.
