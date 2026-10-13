# CW-SWIFT-TESTING-CONCURRENCY — A/B readiness and real blocker

**Date:** 2026-10-13 (Europe/Prague)  
**PR:** [DRAFT #10](https://github.com/cloverwoodstudio/codex-game-dev-library/pull/10), code/skill frozen at `4e6dd2b501a05efe0aad74ee00ad2f24274a40ef`  
**Actual result:** `FIXTURE_ORACLE_PASS`, **`MODEL_A_B_BLOCKED`** (0/4 agent outputs; no effectiveness comparison). Do **not** infer incremental skill value or approve installation based on the synthetic compiler results.

## Goal and pre-registered conditions

Assess whether an otherwise identical OpenCode reviewer detects **more independently confirmed Swift concurrency correctness defects** with the candidate `swift-testing-concurrency` skill than with existing `apple-platform-development` instructions alone.

- **Arm A (baseline):** Apple platform skill + frozen synthetic requirement and line-numbered Swift source.
- **Arm B (treatment):** exactly the same task, Apple skill plus candidate Swift Testing/Concurrency skill and its direct QA contract.
- **Agent/model constraint:** same supported model+variant, same permissions, output format, source hash, prompt instructions and token/time budget; two independent runs per arm in alternating order (`A1 B1 B2 A2`). No reused conversations, cached findings, uncontrolled branch differences, oracle/source-test exposure, network tools or writes.
- **Safety:** only synthetic example code may be supplied to external services; no source or credentials from CRYVIQ, Personal OS, games, Mac `HOME`, private logs or production repos. Run in isolated workspaces with all tools denied; do not use Codex credits.

### Ground truth and scoring (sealed until all four answers)

An owner-local oracle records three distinct, deterministic behavioral failures plus one passing control:

| Code behavior | Actual compiler/run result |
| --- | --- |
| Earlier asynchronous fetch finishes after newer request | FAIL (old completion overwrites new state) |
| Canceled fetch returns late | FAIL (canceled result still published) |
| `clear()` while a fetch is pending | FAIL (pending fetch repopulates cleared state) |
| Ordinary synchronous completion | PASS |

Scoring must be performed by a reviewer blind to arm identity until judgments are fixed. A defect counts as **TP** only when it gives the correct source, mechanism and reproducer/minimal correction. Claims without reproducible evidence count as unverified; verified nonexistent bugs are **FP**. Record recall out of three, confirmed FP, unsupported confidence claims, token usage, elapsed time and extra instruction cost for each run. Do not count the three symptoms as proof of three independent code changes. A/B value requires a reproducible gain above baseline without more harmful false positives or excessive overhead; results on one synthetic fixture **cannot prove** app-wide benefit.

## Actual frozen artifacts — on the authorized Mac development disk

Path: `/Volumes/CLOVERWOOD_DEV/Pilots/SwiftSkillAB-01`.

- `benchmark/buggy/` and `benchmark/oracle/`: isolated Swift 6 SwiftPM packages, no external dependencies, no user content.
- `benchmark/requirements.md`: same source contract for A/B.
- `A/work/review_task.txt` and `B/work/review_task.txt`: generated from the same immutable task/source with only the intended skill-instruction condition changed.
- `evidence/sealed_oracle.json`: private ground-truth rubric, not sent to agents; **do not open before freezing A/B answer files**.
- `evidence/benchmark_manifest.json`: checksums and repo identity.
- `prepare_ab.py` and `run_oracle.sh`: bounded fixture creation and compiler oracle verification.
- `evidence/buggy-swift-test.log`, `evidence/oracle-swift-test.log`, `evidence/oracle-run.log`: retained real Swift Testing evidence.
- **Frozen buggy source SHA-256:** `46e1703a61f51256325b6219b69119285ab82214a6290475f8193bfb53fef25d`.
- **Frozen tests SHA-256:** `3e6457feed485349cb35ccfd089c5faca0d6e43d5e95193ea70dd0765dff269b`.
- **Frozen candidate skill SHA-256:** `b5160c7105664941fb9177d30c939380553d6c68f04a38de036ef79fe3e0317a`.
- **A prompt SHA-256:** `22ca3d96151d4b90f4ed725c0c4727cf7e8c446d9f4e4653d4917685600f396c`; **B prompt SHA-256:** `1396959935377e951c152e8abc2455b97d04ec049c3bd998415c4d5c81d10fa9`.
- A prompt **4,587 bytes**, B prompt **23,011 bytes**. Difference reflects much more detailed context; real token and wall-time costs have **not** been measured.

## Actual run and observed outcome

- Owner Mac Apple Swift 6.4, isolated external-disk checkout of library, no product repo edits.
- Real `swift test` on **buggy synthetic package:** exit `1`, exactly **3 failing behavioral tests and 1 passing control**. No compile failure.
- Real `swift test` on **private corrected oracle package:** exit `0`, **4/4 PASS**.
- Wrapper result: `SWIFT_AB_BENCHMARK_ORACLE_PASS 3_NEGATIVE_1_POSITIVE`; `CLOVERWOOD_CLEANUP_RECEIPT ... command_exit=0 cleanup=PASS`.
- Local evidence `oracle-run.log` SHA-256 `80029611dd9190409aed93ee8be5794ff71f4ea11790a64fbdba4026065cea83`.

**OpenCode readiness probe:**

- Existing OpenCode **v2.0.27** was available at `/Volumes/CLOVERWOOD_DEV/Pilots/OpenCode-01/bin/opencode`.
- `opencode auth list --standalone --format json` showed **zero connected provider accounts**.
- `opencode models --standalone` listed free model names; an isolated **real** `opencode run --standalone --model opencode/ling-3.1-flash-free` with only the harmless string `Respond with exactly the word READY.` returned **HTTP 403 / FreeTierError**, with the service stating that its free tier can only be used from within OpenCode. A source-code request was **not** sent to the model after this failure.
- Attempt log: `evidence/smoke.ndjson`, SHA-256 `4a5303bfef9142d60846cad3ab6d7d6db40c84b01cffeb418e7216c5b0e14266`.
- No model/tool invocation was completed, **A=NOT_RUN**, **B=NOT_RUN**, no paid calls, and the provider restriction was **not** bypassed. The existing OpenCode GUI/service and stored user config were not changed.

## Next gate — not automatic

A valid actual A/B requires permitted model access from a supported OpenCode environment or an independently authorized alternative. Use only this frozen synthetic benchmark and recheck exact hashes; never substitute a human write-up, static keyword inspection, single model response or compiled oracle for actual agent outputs. Measure each arm at least twice and score blind. Until then: **`SKILL_A_B=BLOCKED`; `INCREMENTAL_BENEFIT=NOT_MEASURED`; `OWNER_ADOPTION=NO`.**

Keep **PR #10 DRAFT**, do not MERGE or globally install the candidate. Existing Apple and SwiftUI skills remain authoritative. This benchmark is an infrastructure probe, not a product-code improvement.
