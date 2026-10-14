"""Offline, synthetic tests; no real game files or MCP commands are modified."""
import importlib.util
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts/game_agent_preflight.py"
spec = importlib.util.spec_from_file_location("game_agent_preflight", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class RouterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="cw-router-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "AGENTS.md").write_text("# Synthetic game authority\n")

    def make_unity(self):
        (self.root / "Assets").mkdir(exist_ok=True)
        p = self.root / "ProjectSettings"
        p.mkdir(exist_ok=True)
        (p / "ProjectVersion.txt").write_text("m_EditorVersion: 6000.3.25f1\n")

    def configure(self, target=None):
        p = self.root / ".codex"
        p.mkdir(exist_ok=True)
        (p / "config.toml").write_text(
            '[mcp_servers.unity]\n'
            'command = "/opt/homebrew/bin/unity"\n'
            f'args = ["mcp", "--project-path", "{target or self.root}"]\n'
        )

    def test_exact_unity_target(self):
        self.make_unity()
        self.configure()
        report = mod.inspect(self.root, "unity", False)
        self.assertEqual(report["engine"], "unity")
        self.assertEqual(report["mcp"]["state"], "exact_project_match")
        self.assertEqual(report["errors"], [])

    def test_wrong_unity_target_hard_stop(self):
        self.make_unity()
        self.configure(self.root / "OTHER-GAME")
        report = mod.inspect(self.root, "unity", False)
        self.assertIn("unity_mcp_points_to_wrong_project", report["errors"])

    def test_unconfigured_unity_cannot_silently_use_mcp(self):
        self.make_unity()
        report = mod.inspect(self.root, "unity", False)
        self.assertEqual(report["mcp"]["state"], "not_configured")
        self.assertIn("unity_mcp_not_available_for_this_project", report["warnings"])

    def test_godot_detection_without_unity_mcp(self):
        (self.root / "project.godot").write_text('config_version=5\n')
        report = mod.inspect(self.root, "godot", False)
        self.assertEqual(report["engine"], "godot")
        self.assertEqual(report["errors"], [])

    def test_engine_mismatch(self):
        (self.root / "project.godot").write_text('config_version=5\n')
        report = mod.inspect(self.root, "unity", False)
        self.assertIn("engine_mismatch", report["errors"])

    def test_missing_project_fails(self):
        report = mod.inspect(self.root / "missing", "unity", False)
        self.assertIn("project_not_found", report["errors"])

    def test_untracked_source_warns(self):
        self.make_unity()
        report = mod.inspect(self.root, "unity", False)
        self.assertTrue(report["git"].startswith("dirty_entries:"))
        self.assertIn("preserve_existing_changes_before_edits", report["warnings"])

    def test_nested_godot_under_game_repo_root(self):
        nested = self.root / "game"
        nested.mkdir()
        (nested / "project.godot").write_text("config_version=5\n")
        report = mod.inspect(nested, "godot", False)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["repo_root"], str(self.root))
        self.assertEqual(report["agent_rules"], "present")

    def test_dont_accidentally_load_unity_for_godot(self):
        (self.root / "project.godot").write_text('config_version=5\n')
        self.configure()
        self.assertEqual(mod.engine_for(self.root), "godot")
        self.assertEqual(mod.get_mcp(self.root)["state"], "exact_project_match")
        # File-level MCP is not enough: runtime probing can detect unexpected providers.
        # Actual Codex runtime probe is covered against TWO real games in the local QA.
        report = mod.inspect(self.root, "godot", False)
        self.assertEqual(report["engine"], "godot")


if __name__ == "__main__":
    unittest.main()
