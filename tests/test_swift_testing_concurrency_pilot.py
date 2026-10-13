"""Offline pilot contract tests; no Swift compiler or external accounts required.

Real Swift compiler/runtime proof is a separate macOS CI job and owner Mac receipt.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/swift-testing-concurrency/SKILL.md"
CONTRACT = SKILL.parent / "references/DIRECT_QA_CONTRACT.md"
PACKAGE = ROOT / "samples/swift-testing-concurrency-pilot"
LOCAL_LINK = re.compile(r"(?<!!)\]\(([^)]+)\)")


class SwiftTestingConcurrencyPilotContract(unittest.TestCase):
    def test_manual_only_pilot_frontmatter(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: swift-testing-concurrency\n"))
        self.assertIn('  opencode/autoinvoke: "false"\n', text.split("\n---\n", 1)[0])
        self.assertIn("DRAFT / NOT ADOPTED", text)

    def test_complements_existing_apple_skill(self):
        self.assertTrue((ROOT / ".agents/skills/apple-platform-development/SKILL.md").is_file())
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("apple-platform-development", content)
        self.assertIn("swiftui-pro", content)
        self.assertIn("XCTest", content)

    def test_all_local_skill_reference_links_exist(self):
        for path in [SKILL, CONTRACT, PACKAGE / "README.md"]:
            for match in LOCAL_LINK.finditer(path.read_text(encoding="utf-8")):
                link = match.group(1).split("#", 1)[0]
                if not link or "://" in link or link.startswith("mailto:"):
                    continue
                candidate = (path.parent / link).resolve()
                self.assertTrue(candidate.is_relative_to(ROOT), f"path escapes: {path}: {link}")
                self.assertTrue(candidate.is_file(), f"missing target: {path}: {link}")

    def test_samples_use_native_swift_testing_without_network_dependencies(self):
        manifest = (PACKAGE / "Package.swift").read_text(encoding="utf-8")
        tests = (PACKAGE / "Tests/CloverwoodConcurrencyPilotTests/RevisionedInboxTests.swift").read_text(encoding="utf-8")
        self.assertIn("swift-tools-version: 6.0", manifest)
        self.assertNotIn(".package(", manifest)
        self.assertIn("import Testing", tests)
        self.assertGreaterEqual(tests.count("@Test("), 4)
        self.assertIn("async let", tests)
        self.assertIn("withUnsafeCurrentTask", tests)
        self.assertNotIn("Task.sleep(", tests)

    def test_negative_fixture_is_bounded_and_checked(self):
        script = (PACKAGE / "verify-negative-regression.sh").read_text(encoding="utf-8")
        self.assertIn('"${CLOVERWOOD_RUN_ROOT:?', script)
        self.assertIn("guard token == generation, !Task.isCancelled else", script)
        self.assertIn("EXPECTED_RED_TEST_PASS", script)
        self.assertIn("NEGATIVE_REGRESSION_FAIL", script)

    def test_no_implicit_app_permissions(self):
        text = SKILL.read_text(encoding="utf-8")
        for guard in ["No simulator creation/deletion", "No MERGE, DEPLOY", "dirty", "source SHA", "NOT_RUN"]:
            self.assertIn(guard, text)

    def test_decision_fixtures_are_not_misrepresented_as_runtime(self):
        text = CONTRACT.read_text(encoding="utf-8")
        ids = re.findall(r"^\| ST\d\d \|", text, flags=re.M)
        self.assertEqual(len(ids), 16)
        self.assertIn("conceptual review fixtures", text)
        self.assertIn("NOT_MEASURED", text)


if __name__ == "__main__":
    unittest.main()
