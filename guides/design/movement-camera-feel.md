# Movement, camera and game feel

Reviewed: 2026-08-29

Treat feel as measurable response curves plus coordinated feedback. Tune in a minimal test room before building levels around unstable movement.

## Movement specification

Record input device/dead zones, maximum speed, time to maximum speed, stopping time, air control, turn rate, slope/step behavior, jump apex height/time, gravity phases, coyote time, input buffer, dash duration/cooldown and collision dimensions. Derive values from the desired motion instead of stacking arbitrary forces.

Keep input sampling, movement simulation, animation and camera separate. Log speed, grounded state, input age and state transitions. Test at low/high render frame rates and after focus/input-device changes.

## Camera specification

Define target framing, look-ahead, dead/soft zones, damping per axis, FOV, collision/occlusion behavior, recenter policy, transitions and motion-reduction options. Smooth with time-aware functions; never tune a fixed per-frame interpolation factor.

Camera shake should communicate source, direction and magnitude with a bounded envelope. Layer impulses after stable framing and allow players to reduce or disable them.

## Feedback stack

Animation pose/timing, VFX, audio, hit stop, controller rumble, UI response and camera impulse must share the same event semantics. Add layers one at a time and retest readability; more effects do not automatically improve feel.

Sources:

- Unity Cinemachine Impulse: https://docs.unity3d.com/Packages/com.unity.cinemachine@6.6/manual/CinemachineImpulse.html
- Unreal cameras: https://dev.epicgames.com/documentation/en-us/unreal-engine/cameras-in-unreal-engine
- Godot 2D movement: https://docs.godotengine.org/en/stable/tutorials/2d/2d_movement.html
