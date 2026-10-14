#!/usr/bin/env python3
"""Read-only Cloverwood project & Codex MCP preflight; no game/editor execution."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

EXTERNAL_PREFIX = Path("/Volumes/CLOVERWOOD_DEV")
DISK_GUARD = EXTERNAL_PREFIX / "Tools/require-dev-disk.sh"
CODEX_APP_CLI = Path("/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex")


def call(argv: list[str], cwd: Path | None = None, timeout: int = 10) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(argv, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(argv, 127, "", type(exc).__name__)


def engine_for(root: Path) -> str:
    if (root / "ProjectSettings/ProjectVersion.txt").is_file() and (root / "Assets").is_dir():
        return "unity"
    if (root / "project.godot").is_file():
        return "godot"
    if (root / "Package.swift").is_file() or any(root.glob("*.xcodeproj")):
        return "apple-native"
    return "unknown"


def get_mcp(root: Path) -> dict[str, str]:
    file = root / ".codex/config.toml"
    if not file.exists():
        return {"state": "not_configured"}
    try:
        data = tomllib.loads(file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {"state": "invalid_toml", "reason": type(exc).__name__}
    unity = data.get("mcp_servers", {}).get("unity")
    if unity is None:
        return {"state": "no_unity_entry"}
    args = unity.get("args", [])
    command = unity.get("command")
    if command != "/opt/homebrew/bin/unity" or args != ["mcp", "--project-path", str(root)]:
        return {"state": "wrong_target_or_command"}
    return {"state": "exact_project_match"}


def inspect(root: Path, expected_engine: str | None, check_codex: bool) -> dict:
    result: dict = {
        "project": str(root),
        "engine": "unknown",
        "git": "not_checked",
        "repo_root": None,
        "agent_rules": "missing",
        "mcp": {"state": "not_checked"},
        "codex_runtime": "not_checked",
        "external_disk": "not_applicable",
        "errors": [],
        "warnings": [],
    }
    if not root.is_dir():
        result["errors"].append("project_not_found")
        return result
    result["engine"] = engine_for(root)
    if expected_engine and expected_engine != result["engine"]:
        result["errors"].append("engine_mismatch")
    if result["engine"] == "unknown":
        result["errors"].append("unsupported_or_unidentified_engine")
    if root == EXTERNAL_PREFIX or EXTERNAL_PREFIX in root.parents:
        guard = call([str(DISK_GUARD)], timeout=5)
        result["external_disk"] = "verified" if guard.returncode == 0 and "CLOVERWOOD_DEV_READY" in guard.stdout else "failed"
        if result["external_disk"] != "verified":
            result["errors"].append("external_disk_guard_failed")
    else:
        result["warnings"].append("project_not_on_external_ssd")
    rev = call(["git", "rev-parse", "--show-toplevel"], cwd=root)
    if rev.returncode != 0:
        result["errors"].append("not_a_git_repository")
    else:
        repo = Path(rev.stdout.strip()).resolve()
        result["repo_root"] = str(repo)
        if repo != root and (result["engine"] != "godot" or repo not in root.parents):
            result["errors"].append("project_is_not_git_root")
        if (root / "AGENTS.md").is_file() or (repo / "AGENTS.md").is_file():
            result["agent_rules"] = "present"
        else:
            result["warnings"].append("project_AGENTS_md_missing")
        status = call(["git", "status", "--porcelain=v1"], cwd=repo)
        if status.returncode:
            result["errors"].append("git_status_failed")
        else:
            dirty = len(status.stdout.splitlines())
            result["git"] = "clean" if not dirty else f"dirty_entries:{dirty}"
            if dirty:
                result["warnings"].append("preserve_existing_changes_before_edits")
    if result["repo_root"] is None:
        if (root / "AGENTS.md").is_file():
            result["agent_rules"] = "present"
        else:
            result["warnings"].append("project_AGENTS_md_missing")
    if result["engine"] == "unity":
        result["mcp"] = get_mcp(root)
        if result["mcp"]["state"] == "wrong_target_or_command":
            result["errors"].append("unity_mcp_points_to_wrong_project")
        elif result["mcp"]["state"] == "invalid_toml":
            result["errors"].append("unity_mcp_config_invalid")
        elif result["mcp"]["state"] != "exact_project_match":
            result["warnings"].append("unity_mcp_not_available_for_this_project")
    if check_codex:
        cli = shutil.which("codex") or (str(CODEX_APP_CLI) if CODEX_APP_CLI.is_file() else None)
        if cli is None:
            result["codex_runtime"] = "cli_missing"
            result["warnings"].append("codex_cli_not_found")
        else:
            probe = call([cli, "mcp", "get", "unity", "--json"], cwd=root)
            if probe.returncode != 0:
                result["codex_runtime"] = "no_unity_mcp"
                if result["engine"] == "unity" and result["mcp"]["state"] == "exact_project_match":
                    result["errors"].append("codex_did_not_load_project_mcp")
            else:
                try:
                    info = json.loads(probe.stdout)
                    transport = info.get("transport", {})
                    target = transport.get("args", [])[-1] if transport.get("args") else None
                    result["codex_runtime"] = "exact_project_match" if target == str(root) else "wrong_project"
                except (ValueError, TypeError):
                    result["codex_runtime"] = "invalid_codex_reply"
                if result["codex_runtime"] == "wrong_project":
                    result["errors"].append("codex_resolved_wrong_unity_project")
                elif result["codex_runtime"] == "invalid_codex_reply":
                    result["errors"].append("invalid_codex_mcp_response")
                elif result["engine"] != "unity":
                    result["errors"].append("unity_mcp_unexpected_for_nonunity_project")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Absolute path to an existing game repository root")
    parser.add_argument("--expected-engine", choices=["unity", "godot", "apple-native"])
    parser.add_argument("--check-codex", action="store_true", help="Read-only Codex CLI MCP resolution probe")
    parser.add_argument("--json", action="store_true", help="Machine-readable report")
    args = parser.parse_args(argv)
    original = Path(args.project).expanduser()
    if not original.is_absolute():
        parser.error("--project must be an absolute path; no implicit cwd routing")
    result = inspect(original.resolve(), args.expected_engine, args.check_codex)
    result["verdict"] = "FAIL" if result["errors"] else "PASS_WITH_WARNINGS" if result["warnings"] else "PASS"
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for name in ("project", "engine", "repo_root", "git", "agent_rules", "external_disk", "codex_runtime", "verdict"):
            print(f"{name}: {result[name]}")
        print("unity_mcp:", result["mcp"]["state"])
        if result["errors"]:
            print("ERRORS:", ", ".join(result["errors"]))
        if result["warnings"]:
            print("WARNINGS:", ", ".join(result["warnings"]))
    return 2 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
