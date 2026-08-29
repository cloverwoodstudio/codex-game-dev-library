# Idle and incremental game playbook

Reviewed: 2026-08-29

## Product loop

Generate resources → buy production/capacity multipliers → unlock a new decision layer → optimize → optionally reset/prestige for changed future growth. The player needs meaningful choices, not only increasingly large numbers.

## Smallest vertical slice

One primary resource, three producers, two upgrades with competing value, one capacity or timing constraint, offline progress, save/migration, notation/localization, a short reset/prestige decision and a seeded balance simulation.

## High-risk contracts

- authoritative monotonic time and bounded offline duration;
- numeric representation, rounding, overflow and stable formatting;
- source/sink graph and analytic/simulated time-to-purchase;
- transactional purchases and idempotent reward collection;
- save versioning, clock-tamper policy and multi-device conflicts;
- notifications/monetization that respect consent and player wellbeing.

## Balance lab

Simulate active, periodic and absent players. Measure unlock cadence, dominant purchase order, time walls, prestige value, runaway compounding and recovery after a poor choice. Sweep parameters instead of hand-checking one path.

## Typical traps

Trusting device wall clock, float overflow, offline progress dominating all play, false choice, prestige that merely repeats identical content, notification pressure, unbounded ad rewards and tuning only the first hour.

## References

- Library economy/balancing guide: ../design/economy-balancing.md
- Library save-data guide: ../systems/save-data.md
- Library ethical commerce guide: ../systems/commerce-entitlements.md
