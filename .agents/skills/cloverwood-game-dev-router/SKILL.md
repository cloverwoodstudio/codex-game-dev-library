---
name: cloverwood-game-dev-router
description: Route Cloverwood game-development tasks to the correct Unity, Godot, or Apple-native repository and verify project rules, Git state, external SSD, and Unity MCP before engine work.
---

# Cloverwood Game Dev Router

Read project AGENTS.md first; then the shared library START_HERE.md,
AGENTS.md and relevant capability registry entry. The game's Bible and
the owner's task scope always outrank this skill. Do not reimplement a
mature engine tool or game-specific workflow.

1. Resolve the explicit exact project repository path. Never infer it from
   the current open Editor or reuse the previously active game.
2. Run read-only preflight from this library's root:
   python3 -B scripts/game_agent_preflight.py --project /absolute/game/path --check-codex --json
   Unity MCP must target that same exact project.
3. Treat FAIL as a hard stop. PASS_WITH_WARNINGS requires checking the
   warnings before any write. Dirty Git files are user work: preserve them.
4. Select the official Unity plugin and Unity CLI for Unity 6+, or the
   existing godot-development skill for Godot. Use the game's documented
   Blender/Tripo import route for art. MCP availability never proves a live
   Editor connection or permission to modify scenes.
5. Produce a short task packet: project/repo/branch, Bible authority,
   task goal, read/write limits, relevant engine, rollback plan, QA evidence,
   owner gate. Prefer one agent implementing and an independent reviewer.
6. For heavy local execution use the target project's approved lock/cleanup
   wrapper, verify the correct external disk, and capture a cleanup receipt.
7. Do not auto-merge, deploy, publish, spend paid asset credits, generate
   art or move credentials based on a task-routing suggestion.
8. Report actual PASS/FAIL receipts; never claim tests you did not run.

This skill is intentionally routing only. The per-engine guides, real
Unity plugin, project contracts, and shared game-development loop do the work.
