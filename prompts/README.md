# Reusable prompt library

Prompts are starting contracts, not magic spells. Attach repository context, references, constraints and acceptance tests. Ask Codex to inspect actual files and run actual builds. For image generation, preserve the complete approved prompt and reference images so later batches remain coherent.

## Game concept to plan

```text
Inspect this repository and turn the game brief below into PLAN.md. Define the player fantasy, core loop, controls, win/fail/restart states, target platform, content boundaries, engine choice, architecture, performance budgets, accessibility requirements, milestones and objective acceptance checks. Identify the five largest risks and design the smallest experiment for each. Do not implement until the plan is internally consistent.
```

## Vertical slice

```text
Implement the smallest complete playable loop from PLAN.md using placeholder assets. The player must be able to launch, understand the goal, play, win or fail, and restart. Keep simulation separate from presentation, seed randomness, add high-value automated checks, run the real game, exercise every control, and capture visual evidence. Report remaining defects and scope explicitly.
```

## World bible

```text
Create a concise world bible that supports the specified gameplay rather than adding lore for its own sake. Include pillars, physical/magic rules and costs, geography/ecology, timeline, factions with conflicting goals, cultures, everyday life, location grammar, visual motifs, gameplay opportunities, contradictions, and open questions. Label immutable pillars separately from changeable ideas.
```

## Character production brief

```text
Create a production-ready character brief: gameplay role, narrative desire/need/fear/contradiction, silhouette and shape language, palette/materials, scale, movement personality, required animations and facial range, equipment/variants, accessibility/readability risks, topology/bone/material/texture budgets, LOD plan, and engine import acceptance tests. Avoid copyrighted character imitation.
```

## 3D asset brief

```text
Write a game-ready 3D asset specification from these references. Include real-world dimensions, silhouette priorities, modularity, topology and triangle targets by LOD, UV/texel-density rules, PBR texture sets and resolutions, pivots, collision, sockets, naming, export format/axes/scale, engine import preset, worst-case scene density, provenance/license record, and visual/performance acceptance checks.
```

## Bug reproduction

```text
Reproduce the reported gameplay bug before editing. Record build/version, platform, seed, initial state, exact input sequence, observed state and expected state. Convert the smallest stable reproduction into an automated test or replay, implement the narrowest fix, then rerun relevant unit, integration, input and visual checks.
```

## Performance pass

```text
Profile the representative worst-case scene on target-like hardware. Record frame-time breakdown, memory, loading and build configuration. Rank bottlenecks by measured impact. Change only the top justified bottleneck, compare before/after captures, inspect visual regressions, and stop when the agreed budget is met.
```

## Multiplayer architecture

```text
Design the smallest multiplayer architecture for this game. State topology, authority per system, tick and replication rates, synchronization method, prediction/reconciliation needs, transport assumptions, bandwidth budget, late join/reconnect/version mismatch behavior, persistence and threat model. Define a deterministic multi-process test harness with latency, jitter, loss, reordering and malicious-input cases before implementation.
```

## Gameplay AI

```text
Design this NPC from player-facing behaviors backward. Specify allowed perception, memory and forgetting, decision model, actions, navigation, fairness limitations, telegraphs, difficulty parameters, debug visualization and deterministic scenario tests. Choose the simplest of scripted logic, FSM, behavior tree, utility system or planning and justify the complexity.
```

## Save system

```text
Design versioned save data around stable domain state. Define the envelope, schema, bounds, atomic write and backup recovery, cloud conflict policy, sequential migrations, fixtures from every shipped version, corruption behavior and untrusted-input validation. Do not serialize arbitrary runtime objects.
```

## Movement and camera tuning

```text
Create a measurable movement and camera specification before changing code. Record acceleration, stopping, turn, air control, jump apex/time, coyote/input-buffer windows, collision metrics, camera framing/dead zones/damping/look-ahead/FOV/collision and motion-reduction settings. Build a minimal test room, expose live debug graphs, test multiple frame rates and inputs, and change one parameter family per comparison.
```

## Quest and dialogue system

```text
Design a data-driven quest/dialogue graph with stable IDs, typed conditions/events, explicit terminal states, save migrations, localization/voice hooks and allowlisted game commands. Produce automated graph validation for unreachable nodes, missing localization, dead ends, cycles without exit, duplicate rewards and representative full traversals.
```

## Economy simulation

```text
Map every currency/resource source, sink, conversion, cap and cadence. Build a seeded simulation for several player strategies, measure time-to-goal and accumulation distributions, detect infinite/dominant loops, and run sensitivity analysis. Keep tuning data versioned and define ethical/technical guardrails before proposing monetization.
```

## Localization readiness audit

```text
Audit the repository for player-facing strings, concatenation, unstable keys, placeholder typing, plurals, locale-sensitive formatting, font coverage, RTL assumptions, fixed-size UI, embedded text in art, subtitles, input glyphs and voice-line IDs. Add pseudo-localization and completeness checks without translating content. Report every remaining manual linguistic QA case.
```

## Asset provenance audit

```text
Inventory all code, art, audio, fonts, models, plugins and generated assets. For each, record hash, creator/source, acquisition evidence, exact license/version, attribution, engine/seat/redistribution restrictions, modifications and AI provenance. Quarantine unknown or incompatible items; do not infer commercial permission from “free”. Generate release notices and storefront disclosure inputs.
```

## Platform readiness

```text
Build a target-device matrix and audit input, safe areas/DPI, lifecycle/resume, storage, networking, audio focus, memory, sustained thermal performance, shader/API support, packaging/signing and storefront installation. Define per-tier budgets and graceful quality scaling. Verify on representative physical devices rather than editor emulation alone.
```
