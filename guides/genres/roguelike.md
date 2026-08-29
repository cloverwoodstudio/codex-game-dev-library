# Roguelike and roguelite playbook

Reviewed: 2026-08-29

## Product loop

Explore imperfect information → evaluate risk/resources → make irreversible or costly decision → survive/learn → build a run → win or lose → start again with knowledge and, for roguelites, bounded progression.

## Smallest vertical slice

One generated floor, three enemy roles, one hazard interaction, six items that create at least two builds, resource pressure, stairs/boss goal, death/restart, seed display and complete replay. Prove generation validity and decision variety before adding meta-progression.

## High-risk contracts

- deterministic named random streams and versioned seed;
- guaranteed connectivity, required resources and bounded difficulty;
- turn/action order, visibility and enemy knowledge rules;
- data-driven items/effects with compositional interaction policy;
- save/replay around run state and permanent progression;
- discovery/identification rules that inform rather than merely obscure.

## Validation lab

Run thousands of seeds headlessly. Measure unwinnable results, path length, resource timing, encounter density, dominant builds, unused items, damage spikes and generator time. Preserve every failure and balance outlier as a seed artifact.

## Typical traps

Randomness without meaningful adaptation, progression that replaces skill, impossible combinations, hidden rules without feedback, shared PRNG streams, save scumming policy left undefined and content volume masking a weak decision space.

## References

- Brogue Community Edition source: https://github.com/tmewett/BrogueCE
- Library procedural-generation guide: ../design/procedural-generation.md
- Library economy guide: ../design/economy-balancing.md
