# Cloverwood Game Dev Codex — Router 01

Reviewed: 2026-10-14
Status: DRAFT / READ-ONLY PILOT; no merges, installs, game changes, paid generations or deploys.

## Goal
Reuse the current codex-game-dev-library, Godot skill, official Unity plugin,
per-project Unity MCP and Game Lab — not build a second operating system.
Provide a minimal **preflight gate** that fails closed when an agent is about
to work on the wrong game or wrong Unity Editor.

## Actual existing environment at this gate
- Unity CLI 1.0.0-beta.13, official Unity Codex plugin 0.1.8-beta.
- BETWEEN and NUKU have distinct Codex Unity MCP project routing.
- Godot 4.7.2 with the existing global godot-development skill.
- Blender and Tripo CLI present. Availability is NOT model/animation QA.
- External CLOVERWOOD_DEV disk: UUID-gated; all experimental repo/test work
  goes there; do not relocate tokens/sessions to unencrypted APFS.
- No live Godot MCP is asserted; evaluate community MCP addons separately,
  including arbitrary code execution risk and local-only/network policies.

## Usage
From the library repository root:

    python3 -B scripts/game_agent_preflight.py --project /Volumes/CLOVERWOOD_DEV/Development/NUKU --expected-engine unity --check-codex --json

Or for another engine:

    python3 -B scripts/game_agent_preflight.py --project /ABSOLUTE/GODOT/PROJECT --expected-engine godot --json

The report uses exit code 2 on failures and 0 for success or warnings.
Warnings (dirty Git, missing game-specific AGENTS.md, missing MCP) are never
permission to continue with writes automatically; examine them first.
No engine, asset converter, Editor or build is executed by this script.

## QA and acceptance
- Synthetic offline tests for engine detection, wrong target, missing
  project, dirty working tree and no-MCP behavior.
- Live read-only Codex CLI routing on BETWEEN and NUKU, and negative cases
  on other project paths. Never claim a live Editor was tested via routing.
- Verify that script runs without prompts/paid Codex requests.
- Require an independent change review before merge and before activating
  the global skill. This branch is not an automatic production rollout.

## Future gated improvements
1. Godot MCP: compare maintained community alternatives; prefer local
   sessions, strict project-root enforcement and read-only-by-default.
   Run on disposable test Godot project before a shipping game.
2. Blender/Tripo: art pipeline checks for master/derivative provenance,
   geometry scale, rig naming, animation clips, materials and optimized
   mobile export — preserve provider source models.
3. Engine QA: deterministic test -> real editor launch -> screenshot
   proof -> on-device feel test -> independent review. Match each game.
4. Avoid sprawling AGENTS.md, unreviewed plugin installations and
   unauthorized cross-game automation.

## Supporting current references
- OpenAI, Rethinking skills and prompts for GPT-6 Astra (2026-09-11):
  https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- Unity, Official Unity Plugin for Codex:
  https://unity.com/blog/unity-plugin-codex
- Godot Asset Library Godot MCP Toolkit (community, not endorsed by Godot):
  https://godotengine.org/asset-library/asset/5375
