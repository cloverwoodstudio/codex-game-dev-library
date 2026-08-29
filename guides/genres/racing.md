# Racing game playbook

Reviewed: 2026-08-29

## Product loop

Read upcoming track → choose line/braking/acceleration → manage grip and opponents → recover from error → improve lap/race result. Decide arcade, simcade or simulation target before tuning; realism is not a substitute for readable handling.

## Smallest vertical slice

One vehicle, short closed circuit, start countdown, ordered checkpoints, valid lap, timer/best lap, reset/recovery, chase camera, controller/keyboard support and one AI or ghost. Use final target tick/frame policy.

## High-risk contracts

- tire/grip, suspension, torque/gearing, braking, steering versus speed and assists;
- fixed-step physics and frame-independent input filtering;
- track checkpoint ordering, shortcuts, wrong-way and finish validity;
- camera horizon/FOV/shake and motion-reduction settings;
- deterministic-enough ghost or authoritative replay representation;
- multiplayer reconciliation without destabilizing vehicles.

## Test track

Include straight-line acceleration/braking, constant-radius skidpad, slalom, bumps/curbs, hairpin, crest/jump, off-track recovery and checkpoint exploit routes. Graph speed, slip, steering, suspension and lap sectors.

## Typical traps

Tuning only by feel without telemetry, steering too sensitive at speed, camera amplifying instability, reset enabling shortcuts, physics changing with frame rate, AI using different grip rules and low graphics removing track/braking cues.

## References

- Unreal Chaos Vehicles: https://dev.epicgames.com/documentation/en-us/unreal-engine/chaos-vehicles
- Unreal Vehicle template/time trial: https://dev.epicgames.com/documentation/en-us/unreal-engine/vehicle-template-in-unreal-engine
- Library physics guide: ../systems/physics.md
