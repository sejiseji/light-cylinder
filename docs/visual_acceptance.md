# Visual Acceptance

Visual acceptance is required from LC005 onward. Automated checks prove the
scene runs; visual acceptance asks whether it is worth watching.

For each review, check:

- Light column direction is readable at a glance.
- Grass still feels like the main subject.
- Particles read as air and are not too numerous.
- Cylinder presence is not broken by the added light media.
- With HUD off, the scene can be watched for 30 seconds.
- The scene creates a small desire to keep looking.

LC005-specific completion checks:

- A light column is perceptible.
- The light beam is not directly drawn in normal view.
- Grass tips catch more light than blade middles and roots.
- Particles appear only in the light volume.
- Normal viewing hides the bottom floor rings and radial lines.
- Mixed-width light bands include some thin cuts and do not read as a single slab.
- Wind moves grass in and out of the light.
- `L` toggles the light comparison on and off.
- No meaningful FPS drop is visible.

LC006-specific completion checks:

- HUD off keeps grass as the main subject.
- Light direction is recognizable within a few seconds.
- Light is not directly drawn, but its presence is readable.
- Particles do not read as snow or insects.
- Grass root thickness and thin tips remain legible.
- Wind reads as neither fully synchronized nor fully random.
- Light pulse reads as breathing, not blinking.
- Cylinder boundary does not read as a cage.
- Boundary off still leaves a coherent contained space.
- Initial composition can be used as a presentation screenshot.
- Auto rotate can be watched for at least one minute without feeling too fast.
- HUD off can be watched for at least one minute.
- The scene creates a small desire to keep looking.

LC006.5-specific completion checks:

- Camera motion has a short, pleasant afterglow without feeling slippery.
- Micro wind makes the grass breathe without adding a new visible phenomenon.
- Cloud shadow reads as a slow dimming and return, not a pulse effect.
- Particles feel gently alive without becoming snow, insects, or noise.
- Active palette preset remains coherent, and alternate presets are settings.
- `Specimen of Light` / `光の標本` reads as the work title.

LC007-specific completion checks:

- The clear scene remains the default and still feels like the v0.1.0 prototype.
- Rain becomes visible through the light, not as a full-screen curtain.
- Wind makes rain fall diagonally without making the cylinder feel chaotic.
- Rain disappears at the floor without splash or wet-ground behavior.
- `N` gives an immediate clear/rain comparison.
- `Q` and `E` adjust rain amount without making the scene feel like snow.
- Grass remains the main subject when rain is on.
- No meaningful FPS drop is visible.

LC008-specific completion checks:

- Rain impacts create small splashes on ground arrival.
- Splashes disappear within a few frames.
- Grass press reactions are local and shorter than wind motion.
- Grass reaction strength stays smaller than wind and does not become a second
  wave animation.
- Ground wetness increases while rain is on.
- Wetness dries slowly after rain is turned off.
- Wet ground darkens without becoming a filled surface.
- Only wet floor areas in light gain a weak reflection cue.
- Puddles, ripples, water drops, thunder, and rain audio remain absent.
- The clear initial scene remains unchanged.
- Grass count 300 baseline / 450 stage-3 and 30 FPS feel are preserved.

LC009-specific completion checks:

- Toggling rain off enters `AFTER_RAIN` when the ground is still wet.
- After-rain returns naturally to `CLEAR`.
- CloudShadow feels like it slowly lifts rather than snapping brighter.
- Wet-floor reflection lingers a little after rain stops.
- Drying speed changes with remaining wetness.
- Only a small subset of grass tips can hold droplets.
- Droplets are visible only in light.
- Droplets fall and disappear without becoming rain or sparkle noise.
- The MENU button remains in the top right, readable, and does not become the
  focal point.
- All MENU stages start at 1 so the initial viewing state remains the baseline.
- Puddles, ripples, thunder, rain audio, and all-grass droplets remain absent.
- The clear initial scene remains unchanged.

LC010-specific completion checks:

- `M` starts and stops the observation cycle.
- The cycle reads as clear, shadow, light rain, rain, after-rain, and clear
  recovery without adding new weather effects.
- MENU stages remain user settings and are not overwritten by the cycle.
- Rain stage is used as the base amount for the cycle's rain multiplier.
- Manual `N`, `Q`, or `E` rain input exits the cycle cleanly.
- CloudShadow deepens and lifts softly rather than snapping.
- The cycle remains quiet enough that grass and light stay the subject.
- The scene still starts in manual clear state.

## Artistic Review

Each wave after LC006 should end with an artistic review in addition to technical
validation:

### First Impression

- What is communicated in the first five seconds?

### Focal Point

- Where does the eye go first?
- Does that match the intended design?

### Atmosphere

- Quietness
- Immersion
- Air
- Rhythm

### Visual Noise

- Distracting elements
- Causes of visual scatter

### Time Worth Watching

- How many minutes does HUD-off viewing feel sustainable?
- Did this improve over the previous wave?
