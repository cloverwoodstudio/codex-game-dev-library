# Platformer playbook

Reviewed: 2026-08-29

## Product loop

Read space → commit to movement → correct in flight where allowed → land/recover → learn route → reach checkpoint/goal. The controller and camera are the game; content production starts only after they survive a metrics gym.

## Smallest vertical slice

One character, one screen/room chain, run/jump/fall, moving platform or wall interaction, one hazard, checkpoint, collectible/optional route, win/fail/restart and final camera. Use placeholder art but final collision dimensions.

## High-risk contracts

- measurable acceleration, stopping, apex, jump height/distance and air control;
- coyote/input buffer rules, variable jump and corner/ceiling behavior;
- moving-platform velocity inheritance and one-way surfaces;
- camera look-ahead, dead zone, landing behavior and motion reduction;
- hazard telegraph, knockback/invulnerability and fast restart;
- animation that never changes authoritative collision unexpectedly.

## Test gym

Build tiles for minimum/maximum jump, low ceiling, corner, slope, moving platform, wall, drop, hazard chain and camera boundary. Replay at multiple frame rates and input devices. Log takeoff/landing velocity and reason for every state transition.

## Typical traps

Physics-body defaults that feel inconsistent, tuning art before metrics, camera lag during reversals, input prompts tied to physical keys, long death downtime, and levels requiring untested edge-case exploits.

## References

- Godot official Platformer 2D demo: https://github.com/godotengine/godot-demo-projects/tree/master/2d/platformer
- Godot 2D movement overview: https://docs.godotengine.org/en/stable/tutorials/2d/2d_movement.html
- Library movement/camera guide: ../design/movement-camera-feel.md
