# Party and social game playbook

Reviewed: 2026-08-29

## Product loop

Gather quickly → understand a tiny rule → play a short round → laugh/react/compare → rotate outcome or role → rematch. Social friction, downtime and unclear joining can destroy the loop faster than shallow mechanics.

## Smallest vertical slice

Lobby/party, join/leave/reconnect, one 2–5 minute mode, clear countdown/rules, score/end/rematch, bots or reduced-player fallback, controller assignment, moderation/report path and network fault test.

## High-risk contracts

- party/lobby lifecycle distinct from authoritative match gameplay;
- late join, disconnect, leader migration and minimum-player policy;
- local input-device ownership and guest identity;
- synchronized round state, timers and tie resolution;
- readable rules within seconds and low downtime;
- chat/UGC safety, blocking, reporting and age/audience defaults.

## Chaos lab

Simulate simultaneous joins, full party, leader exit, duplicate device, spectator, AFK, mid-round disconnect, network loss, host migration and rematch spam. Measure time from launch/invite to first action and active-versus-waiting time.

## Typical traps

Party messages driving authoritative gameplay, one player blocking everyone, eliminated players waiting too long, host advantage, inaccessible color-only identity, account requirements before local play and opening communication without moderation.

## References

- Nakama real-time parties: https://heroiclabs.com/docs/nakama/concepts/parties/
- Nakama multiplayer models: https://heroiclabs.com/docs/nakama/concepts/multiplayer/
- Library community-moderation guide: ../workflows/community-moderation.md
