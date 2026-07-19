# Controls Spec

LC001 implements keyboard controls for orbit-camera inspection. LC004 adds mouse
controls so the scene can be tested quickly during visual iteration. LC005 adds
light comparison and makes debug mode the place for light-axis inspection. LC006
starts in a viewing state and adds camera reset. LC007 adds optional rain
comparison while keeping the clear scene as the default:

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
- Q and E: decrease and increase rain amount
- R: reset camera to the viewing composition
- D: toggle debug HUD, camera details, reference axes, and light guides
- Top-right MENU button: open the observation tuning panel
- ESC: exit

The MENU panel exposes five 1-3 stage controls: photon density, grass density,
wind strength, rain amount, and auto-rotate speed. Stage 1 is the current
baseline composition for all five controls. Settings are session-only and reset
to stage 1 on restart. The rain stage changes only the rain amount preset; rain
ON/OFF remains controlled by `N`. The panel captures mouse input only inside its
button and panel region, so normal drag rotation continues elsewhere.

Touch controls are planned for a later wave after camera and scene behavior are
stable enough to test on mobile layouts.
