# Shared Cloverwood agent entry point

Reviewed: 2026-09-22

Use this library from ChatGPT + Remote Desktop Commander, Codex, or another
explicitly authorized agent. This is a shared reading and verification contract,
not a new backend, automatic skill installation, or remote-control service.
The repository name and existing paths remain unchanged.

## Start each task

1. Read the target project's current `AGENTS.md`, plan and work status. Establish
   the live remote source commit and inspect local changes before editing.
   Project-specific contracts and the owner's scope are not overridden here.
2. Read this library's [AGENTS.md](AGENTS.md), then find the relevant entry in
   [capabilities/registry.json](capabilities/registry.json). Load only the listed
   sources needed for the task, including nested skill instructions where relevant.
3. Distinguish playbook, helper, sample and historical evidence. Read limitations,
   evidence date, tool requirements and authorization boundaries before planning.
   A listed tool is not necessarily installed; a test receipt is not owner approval.
4. Use the project's existing build/asset scripts. On an authorized Mac, DC may
   execute the scoped work; Codex may use its available authorized environment.
   Neither access route changes the acceptance criteria or permits extra actions.
5. Follow the [shared development loop](guides/workflows/codex-loop.md). Record
   the exact commit/build, test results, observed limitations and cleanup evidence.
   Verify writes against GitHub after committing/pushing; do not infer remote
   success from an intention, timeout, or local file alone.

Reading a skill file through a connector is explicit loading. Do not assume that
ChatGPT automatically discovers `.agents/skills/`, and do not remove those paths
or Codex configuration merely because another agent can read the same files.

## Offline discovery on the Mac

The following commands only inspect the local registry and its pinned sources.
They make no network requests and do not execute any registered capability.

```sh
bash scripts/cloverwood-local-run.sh -- python3 -B scripts/capabilities.py --list
bash scripts/cloverwood-local-run.sh -- python3 -B scripts/capabilities.py --show text-to-cad
bash scripts/cloverwood-local-run.sh -- python3 -B scripts/capabilities.py --show asset-viewer
```

Without a local shell, fetch this file and the JSON via the authorized GitHub
connector at a known ref. Read entries manually; do not invent a validator PASS.

## Preserve the useful boundaries

**Library:** reusable knowledge, fixtures and tools. **Game Lab:** its existing
asset authority/routing/QA contracts, not a newly authorized whole-game platform.
**DC:** authorized local execution. **Codex:** another supported agent, not a
required intermediary. **Game repositories:** authoritative runtime and release
contracts. **GitHub:** durable source and review history.

**Asset Viewer is not ViewForge.** Preserve the existing owner workflow:
model -> technical/runtime QA -> authorized review publication -> working link ->
owner rotates/inspects the exact revision -> PASS/FIX. Promotion to a shipping game
is a separate gate. The registry's Viewer entry points to PROJECT FORGE evidence,
not a newly verified live Viewer URL or a discovered Viewer source repository.

No catalog entry authorizes installation, paid generation, source upload, signing,
account changes, model publication, game changes, merge, TestFlight or App Store
release. Obtain the task's appropriate authorization before those operations.

## Small next steps, not another OS

The [registry contract](capabilities/README.md) and
[implementation scope](research/library-shared-entry-2026-09-22.md) define this
slice. Replay hardening, shared Mac-lock repair, new adapters, and game integration
remain separate work. No accepted model, Viewer deployment or game is changed.
