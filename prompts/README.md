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

## Modding and UGC threat model

```text
Design the smallest safe mod/UGC surface that enables the requested creator behavior. Define package manifest, stable API/versioning, dependencies/load order, allowed capabilities, parser and sandbox boundaries, size/rate limits, signing/hash policy, save and multiplayer compatibility, moderation/takedown workflow and recovery from corrupt or removed content. Treat every downloaded field and file as untrusted; produce adversarial tests before implementing loaders.
```

## Live-ops readiness

```text
Design an observable and reversible live-ops change. State the player question or reliability goal, versioned telemetry events and privacy class, dashboards/alerts, typed remote-config schema, safe defaults, approval/audit path, staged rollout cohorts, kill switch, rollback trigger and post-deploy verification. Never allow remote config to bypass server authority.
```

## Store-page evidence pack

```text
Build a store asset brief from the current playable build and the platform's current official requirements. Define the player fantasy, three observable differentiators, capture states, gameplay-first trailer beats, screenshot/capsule matrix, localization, provenance, accessibility/maturity checks and exact build evidence for every claim. Flag anything promised but not demonstrable in the release candidate.
```

## Procedural generator contract

```text
Design this procedural generator from invariants and measurable output distributions backward. Define reproduction key, generator/config/content versions, stable named random streams, structural pipeline, bounded validation/repair, safe fallback, performance budget, golden/regression/fuzz seed corpora and player-facing seed compatibility. Produce property tests and a failure artifact that reports the exact seed, first invalid stage and output hash.
```

## Replay-driven regression

```text
Turn this gameplay defect into a minimal versioned replay. Record build/content/simulation versions, fixed tick rate, seed and random-stream state, semantic quantized commands, checkpoints and subsystem hashes. Reproduce the first divergent tick before editing, implement the narrowest fix, preserve the replay as a regression test and report any replay compatibility implications.
```

## CI evidence design

```text
Design the cheapest CI pipeline that proves a clean machine can validate, test, package and smoke-run this game. Separate pull-request, main, nightly and release gates; define the justified platform matrix, pinned toolchain, cache boundaries, secret permissions, timeouts and local command equivalents. On failure retain uniquely named logs, test reports, screenshots/diffs, seeds/replays and build manifest. Do not deploy a rebuild that differs from the tested artifact.
```

## Level blockout and encounter brief

```text
Design a greybox level from gameplay metrics and player decisions backward. Define entry/exit state, verbs and knowledge tested, critical/optional routes, spatial grammar, landmarks, encounters, recovery, checkpoints, accessibility, performance worst case and acceptance checks. Use the real controller, camera, collision and deterministic encounter seeds; do not begin art polish until traversal and objective clarity survive uncoached playtests.
```

## Animation production contract

```text
Create a runtime animation contract covering skeleton/bind pose/axes, root motion, control-versus-deformation bones, IK and attachment markers, skinning limits, clip inventory, contacts/events, interrupt rules, retarget families, compression/LOD budgets and an animation test gym. Separate authoritative gameplay from presentation and define visual checks for every body family and transition.
```

## Skippable cinematic

```text
Design this cinematic as a safe state transition. Specify trigger/preconditions, actor bindings, camera/input/HUD/audio ownership, subtitles/localization, save/checkpoint behavior, idempotent gameplay events, skip-to-end state, pause/disconnect/unload recovery and exact post-sequence acceptance tests. Exercise first play, replay and skips at multiple timestamps.
```

## Player-data audit

```text
Inventory every player-data flow in the game, backend, platform service and third-party SDK. For each field record source, purpose, destination, identity link, consent/basis, retention, deletion/export, security class, child-audience impact and storefront disclosure. Compare runtime network behavior with the privacy policy and store labels; flag unnecessary collection and mismatches. This is an engineering audit, not legal advice.
```

## Safe patch rollout

```text
Plan this update as promotion of one immutable tested artifact. Define build/content/schema identity, upgrade paths, save/network/backend compatibility, storefront beta/canary/default stages, health metrics and thresholds, expand/contract migrations, retained rollback artifacts, exact rollback limitations, patch notes and post-release verification. Rehearse clean install, storefront-client upgrade and rollback before default rollout.
```

## Community launch readiness

```text
Design the community operating model before opening channels. Define rules with examples, moderator roles/least privilege/training/confidentiality, report-block-appeal flows, high-severity escalation, evidence privacy/retention, automation boundaries, support/bug/announcement routing, response targets and moderator wellbeing. Produce tabletop scenarios for spam, harassment, doxxing, child safety, account compromise and false reports.
```

## Data-driven content compiler

```text
Design a versioned content pipeline with stable IDs, schema/defaults/bounds, localization and reference rules, source-to-runtime compilation, dependency manifest, actionable structural/semantic validators, preview, migrations and compatibility with saves/replays/mods. Separate author source from generated runtime output and provide a dry-run report for batch changes.
```

## Large-world streaming audit

```text
Design the world as a cancellation-safe cell lifecycle. Define coordinates, cell hierarchy, streaming sources/radii/hysteresis, dependencies, stable entity identity, persistent-versus-transient state, cross-cell handles, activation gates, teleport prefetch, memory/I/O budgets and failure fallback. Produce automated boundary, oscillation, save-during-load, far-apart multiplayer and corrupt-I/O scenarios with cell timeline evidence.
```

## Purchase and entitlement threat model

```text
Model the complete purchase lifecycle across storefront, client and backend. Define catalog IDs/types, platform-owned price display, pending/completed/cancelled states, server verification, unique transaction token, idempotent atomic grant, acknowledgement/consumption, restore, refund/revocation, subscription expiry, reconciliation and support evidence. Test duplicate/out-of-order notifications and never grant from an unverified client callback.
```
