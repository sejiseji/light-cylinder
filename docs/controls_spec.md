# Controls Spec

LC001 implements keyboard controls for orbit-camera inspection. LC004 adds mouse
controls so the scene can be tested quickly during visual iteration. LC005 adds
light comparison and makes debug mode the place for light-axis inspection. LC006
starts in a viewing state and adds camera reset:

- Left and Right: yaw left and right around the target
- Up and Down: pitch the view up and down
- Mouse drag: yaw and pitch around the target
- A and S: zoom in and out
- Mouse wheel: zoom in and out
- X: toggle auto rotate
- B: toggle cylinder boundary visibility
- W: toggle wind application
- L: toggle light media application
- R: reset camera to the viewing composition
- D: toggle debug HUD, camera details, reference axes, and light guides
- ESC: exit

Touch controls are planned for a later wave after camera and scene behavior are
stable enough to test on mobile layouts.
