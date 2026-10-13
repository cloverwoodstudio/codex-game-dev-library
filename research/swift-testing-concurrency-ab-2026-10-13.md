# CW-SWIFT-TESTING-CONCURRENCY — completed isolated A/B evaluation

**Date:** 2026-10-13 (Europe/Prague)  
**PR:** [DRAFT #10](https://github.com/cloverwoodstudio/codex-game-dev-library/pull/10), code/skill frozen at `4e6dd2b501a05efe0aad74ee00ad2f24274a40ef`  
**Actual result:** `FIXTURE_ORACLE_PASS`, **`MODEL_A_B_COMPLETED` (4/4 valid model reviews)**. Both arms identified all three seeded bugs in both repetitions. The candidate skill showed a *small* extra spinner-state detection signal (2/2 vs 1/2) with higher prompt/response/time cost. **No robust demonstrated advantage or approval for global adoption/MERGE.** Earlier OpenCode access blocker and its resolution are retained below as historical evidence.

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

**Historical OpenCode readiness probe (before resolving config schema):**

- Existing OpenCode **v2.0.27** was available at `/Volumes/CLOVERWOOD_DEV/Pilots/OpenCode-01/bin/opencode`.
- `opencode auth list --standalone --format json` showed **zero connected provider accounts**.
- `opencode models --standalone` listed free model names; an isolated **real** `opencode run --standalone --model opencode/ling-3.1-flash-free` with only the harmless string `Respond with exactly the word READY.` returned **HTTP 403 / FreeTierError**, with the service stating that its free tier can only be used from within OpenCode. A source-code request was **not** sent to the model after this failure.
- Attempt log: `evidence/smoke.ndjson`, SHA-256 `4a5303bfef9142d60846cad3ab6d7d6db40c84b01cffeb418e7216c5b0e14266`.
- **At that initial probe only**, no model/tool invocation was completed, **A=NOT_RUN**, **B=NOT_RUN**. Subsequent work revealed that the isolated local config was using the wrong legacy `permission` object instead of OpenCode V2's ordered `permissions` array. Once corrected, the supported free model `opencode/big-pickle` returned a valid READY response, and all four A/B sessions succeeded without tools. Neither the original 403 nor the timed-out legacy-config probe should be attributed to an unavoidable account/billing restriction. The existing OpenCode GUI/service and stored user config were not modified.

## Actual model A/B — 2026-10-13 (after resolving OpenCode V2 permissions)

**Runtime:** existing native OpenCode v2.0.27 on owner Mac, model `opencode/big-pickle` free, **four independent and isolated model sessions** in pre-registered order `A1, B1, B2, A2`. A uses the original Apple platform skill; B adds exactly the candidate Swift Testing skill and its QA contract. The actual Swift source and requested review contract were identical. Original prompt lengths were **4,587 bytes (A)** and **23,011 bytes (B)**.

The supported OpenCode V2 config uses the ordered `permissions` array (not legacy `permission`), with all tool actions approval-required by default, `edit = deny`, `external_directory = deny`, and `shell = ask` (no approval granted). **All four model results: exit 0, answered, tool call count 0, no shell/edit/network tool use.** This was a legitimate supported runtime, not an auth/proxy bypass. Synthetic source and instructions only; no production code, credentials or user data were submitted. Reference: https://dev.opencode.ai/v2/docs/permissions/.

**Scoring:** four outputs saved under random opaque IDs; a criterion-based reviewer recorded seeded TP, additional spinner finding and unsupported claims **before revealing arm mapping**. Locked `blind_scores_LOCKED.json` SHA-256: `bb5df2ef0c3b0da9d2b334d3c8bdce4e815c13a724b20d87e0ae605c3973bacf`. Ground truth was from the earlier Swift compiler oracle. This is **pseudonymized, single-reviewer scoring**, not independent third-party double-blind: visible response lengths could provide imperfect clues about arm identity, and the task is synthetic. Reviewer did not execute the model-proposed test snippets.

| Measured item | Baseline A (2 runs) | Candidate B (2 runs) |
| --- | ---: | ---: |
| Seeded proven correctness failures identified | **6/6** | **6/6** |
| Distinct post-hoc spinner-ownership issue identified | 1/2 | **2/2** |
| Unsupported/false extra claims | 1 | 1 |
| Average model response elapsed time | **38.87 s** | **50.07 s** |
| Average response text characters | **6,220.5** | **9,020** |
| Actual tool calls | 0 | 0 |

All four independently found (1) stale completion overwriting a newer value, (2) cancelled async work publishing, and (3) `clear()` failing to invalidate an outstanding load. B delivered **no additional seeded true positives**. The extra spinner/ownership problem found in 2/2 B but only 1/2 A is real: after an older request finishes while a newer one is still suspended, the old request clears `loading` prematurely. It was independently tested **after blind scores were locked** in a disposable Swift Testing check: **buggy source FAIL** with the exact `#expect(inFlight.loading == true)` failure; corrected oracle **PASS**. The post-hoc test, including a cleanup-PASS wrapper, is at `/Volumes/CLOVERWOOD_DEV/Pilots/SwiftSkillAB-01/evidence/spinner-verification.log`, source script `verify_unseeded_spinner.sh`. It was never silently inserted into the original frozen benchmark.

**Counter-signals:** B used roughly **5× the input prompt bytes**, produced **45% longer responses** and took **29% longer on average**, for a modest extra observation in a two-run sample. One answer in each arm incorrectly concluded no test suite existed from a **source-only excerpt**; the actual hidden SwiftPM benchmark had tests. One B cancellation remedy was also incomplete because it did not clear the current request's loading state. Thus this study supports **at most weak incremental depth**, not a validated cross-project improvement in agent quality. A/B under a single tiny example cannot justify global adoption.

**Raw evidence retained locally:** `/Volumes/CLOVERWOOD_DEV/Pilots/SwiftSkillAB-01/model_ab/` stores isolated session receipts, raw events, four answers, the locked blind score, sealed assignment map and `final_assessment.json`. The run recipe is `run_model_ab.py` and execution receipt is `evidence/actual_model_ab.log`. No raw responses or hidden reference implementation were committed to GitHub. All benchmark source, prompt, and test hashes still match the initial frozen manifest.

**Decision:** `AGENT_A_B=PASS` (executed as designed), `SEEDED_RECALL_ADVANTAGE=NONE`, `EXTRA_CORRECTNESS_SIGNAL=SMALL`, `GENERALIZED_SKILL_BENEFIT=NOT_ESTABLISHED`. Keep PR #10 **DRAFT**; do not MERGE or install globally without an explicit owner decision and a more representative test.

## Next gate — not automatic

The requested isolated, same-model **A1/B1/B2/A2** comparison is complete. No broad adoption can be inferred from one synthetic problem with just two repetitions per arm. A future, separately authorized representative evaluation should compare additional real-world-shaped Swift Testing/concurrency bugs on frozen safe fixtures, record confirmed false positives and actual instruction/token costs, and respect the existing Apple/SwiftUI skills. **`SKILL_A_B=COMPLETED`; `INCREMENTAL_BENEFIT=WEAK/NOT GENERALIZED`; `OWNER_ADOPTION=NO`.**

Keep **PR #10 DRAFT**, do not MERGE or globally install the candidate. Existing Apple and SwiftUI skills remain authoritative. This benchmark is a completed, narrow synthetic model evaluation, not an Apple application integration or product-code improvement.
