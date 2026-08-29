# Game physics

Reviewed: 2026-08-29

Use physics for the interactions it improves; scripted character controllers and authored rules are often more predictable than general rigid-body simulation.

## Foundations

- simulate with a fixed timestep and bounded catch-up
- separate physics state from interpolated rendering
- define world units, scale, gravity and velocity limits
- use simple stable collision shapes and an explicit layer/mask matrix
- distinguish trigger/query, kinematic, dynamic and static roles
- enable continuous collision only for justified fast objects
- tune solver/substeps from measured instability and cost
- consume collision events after the step; avoid mutating the world from unsafe callbacks

Physics is not automatically deterministic across machines or engine versions. Record initial state, inputs, tick and engine configuration for reproduction. For multiplayer, pick an authority/prediction model explicitly instead of replicating transforms blindly.

Create stress scenes for stacking, joints, fast projectiles, tunneling, slopes/steps, moving platforms, spawn overlap, sleep/wake, origin distance and worst-case contact counts.

Sources:

- Box2D simulation: https://box2d.org/documentation/md_simulation.html
- Godot physics interpolation: https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/physics_interpolation_introduction.html
- Unreal constraints: https://dev.epicgames.com/documentation/en-us/unreal-engine/physics-constraints-in-unreal-engine
