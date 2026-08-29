# First-person shooter playbook

Reviewed: 2026-08-29

## Product loop

Acquire target/threat information → move and position → aim/fire/use ability → receive hit feedback → manage ammo/health/cooldowns → secure objective or recover.

## Smallest vertical slice

One movement controller and camera, one hitscan/projectile weapon, reload/ammo, two enemy roles or one network opponent, compact arena, health/damage/death/respawn, objective, HUD/settings and complete replay. Include mouse and controller aim.

## High-risk contracts

- input-to-photon latency, sensitivity units, acceleration, FOV and aim assist;
- authoritative shot origin/time, lag compensation and hit validation;
- spread/recoil model separated from visual camera kick;
- weapon state machine with equip/fire/reload/interrupt priorities;
- readable damage direction, team/enemy silhouettes and audio cues;
- movement collision, peeking, stairs/slopes and network reconciliation.

## Shooter gym

Static/moving targets, reaction target, recoil wall, range falloff, projectile lead, cover/peek, vertical fight, spawn safety and latency/loss bots. Record hit accuracy by range, time-to-kill, first-shot latency and server/client hit disagreement.

## Typical traps

Frame-dependent fire rate, camera animation changing aim authority, client-trusted hits, inconsistent sensitivity/scopes, unreadable VFX, spawn kills, aim assist choosing hidden targets and balance based only on average accuracy.

## References

- Unreal First Person template: https://dev.epicgames.com/documentation/en-us/unreal-engine/first-person-template-in-unreal-engine
- Unreal Lyra sample/shooter gym: https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-in-unreal-engine
- Library multiplayer guide: ../systems/multiplayer.md
