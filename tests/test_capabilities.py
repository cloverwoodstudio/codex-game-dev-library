"""Contract tests use isolated local fixtures; no provider or game execution."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("capabilities", ROOT / "scripts/capabilities.py")
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)

class CapabilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="registry-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = registry.read_json(ROOT / "capabilities/registry.json")
        for cap in self.data["capabilities"]:
            for name in cap["sources"]:
                dst = self.root / name
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes((ROOT / name).read_bytes())

    def valid(self):
        return registry.validate(self.data, self.root)

    def rejected(self, message=None):
        with self.assertRaises(registry.RegistryError) as caught:
            self.valid()
        if message:
            self.assertIn(message, str(caught.exception))

    def rewrite_path(self, value):
        cap = self.data["capabilities"][0]
        old = cap["entrypoint"]
        expected = cap["sources"].pop(old)
        cap["sources"][value] = expected
        cap["entrypoint"] = value

    def cli(self, args):
        path = self.root / "capabilities/registry.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.data))
        out, err = io.StringIO(), io.StringIO()
        with patch.object(registry, "ROOT", self.root), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = registry.main(args)
        return status, out.getvalue(), err.getvalue()

    def test_real_registry_and_counts(self):
        result = self.valid()
        self.assertEqual(result["capabilities"], 12)
        self.assertEqual(result["externalReferences"], 1)
        self.assertEqual(result["toolExecution"], "NOT_PERFORMED")
        self.assertEqual(result["networkVerification"], "NOT_PERFORMED")

    def test_cli_check(self):
        code, out, err = self.cli(["--check"])
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["status"], "REGISTRY_CHECK_PASS")

    def test_cli_lists_capabilities_and_external_viewer_separately(self):
        code, out, err = self.cli(["--list"])
        self.assertEqual(code, 0, err)
        self.assertEqual(len(out.splitlines()), 13)
        self.assertIn("viewforge | EXECUTABLE_HELPER", out)
        self.assertIn("asset-viewer | EXTERNAL_WORKFLOW", out)

    def test_cli_show(self):
        code, out, err = self.cli(["--show", "text-to-cad"])
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["verification"]["level"], "HISTORICAL_FIXTURE")

    def test_cli_unknown_id_fails_without_entry(self):
        code, out, err = self.cli(["--show", "not-a-tool"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("unknown capability", err)

    def test_all_entries_validated_before_show(self):
        self.data["capabilities"][-1]["kind"] = "PRODUCTION_READY"
        code, out, err = self.cli(["--show", "text-to-cad"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")

    def test_no_execution_authority(self):
        self.data["isExecutionAuthority"] = True
        self.rejected("execution authority")

    def test_no_command_field(self):
        self.data["capabilities"][0]["command"] = "touch never-executed"
        self.rejected("unknown fields")
        self.assertFalse((self.root / "never-executed").exists())

    def test_unsupported_schema(self):
        self.data["schemaVersion"] = 999
        self.rejected("schemaVersion")

    def test_boolean_not_version_one(self):
        self.data["schemaVersion"] = True
        self.rejected("schemaVersion")

    def test_duplicate_id(self):
        self.data["capabilities"].append(copy.deepcopy(self.data["capabilities"][0]))
        self.rejected("duplicate id")

    def test_empty_catalog(self):
        self.data["capabilities"] = []
        self.rejected("capability count")

    def test_unknown_status(self):
        self.data["capabilities"][0]["verification"]["level"] = "APPROVED"
        self.rejected("verification level")

    def test_malformed_kind_does_not_crash(self):
        self.data["capabilities"][0]["kind"] = ["RUNNABLE_SAMPLE"]
        self.rejected("unknown kind")

    def test_invalid_date(self):
        self.data["capabilities"][0]["verification"]["date"] = "2026-02-30"
        self.rejected("invalid date")

    def test_evidence_after_review_date(self):
        self.data["capabilities"][0]["verification"]["date"] = "2027-01-01"
        self.rejected("postdates review")

    def test_missing_limitations(self):
        self.data["capabilities"][0]["limitations"] = []
        self.rejected("nonempty")

    def test_unpinned_entrypoint(self):
        self.data["capabilities"][0]["entrypoint"] = "not-registered.py"
        self.rejected("pinned local source")

    def test_unpinned_evidence(self):
        self.data["capabilities"][0]["verification"]["evidence"] = ["invented-receipt.json"]
        self.rejected("unpinned evidence")

    def test_tampered_source(self):
        cap = self.data["capabilities"][0]
        (self.root / cap["entrypoint"]).write_text("changed")
        self.rejected("hash changed")

    def test_missing_source(self):
        (self.root / self.data["capabilities"][0]["entrypoint"]).unlink()
        self.rejected("missing")

    def test_absolute_path(self):
        self.rewrite_path("/etc/passwd")
        self.rejected("unsafe source path")

    def test_path_traversal(self):
        self.rewrite_path("../outside.md")
        self.rejected("unsafe source path")

    def test_git_metadata_is_not_a_source(self):
        self.rewrite_path(".git/config")
        self.rejected("unsafe source path")

    def test_noncanonical_paths(self):
        original = copy.deepcopy(self.data)
        for path in ("./file.md", "dir//file.md", "dir\\file.md", "file.md%00", "file.md?x=1"):
            with self.subTest(path=path):
                self.data = copy.deepcopy(original)
                self.rewrite_path(path)
                self.rejected("unsafe source path")

    def test_symlink_file(self):
        path = self.root / self.data["capabilities"][0]["entrypoint"]
        target = self.root / "symlink-target.md"
        path.rename(target)
        path.symlink_to(target)
        self.rejected("symlink")

    def test_symlink_directory(self):
        parent = self.root / ".agents"
        target = self.root / "renamed-agents"
        parent.rename(target)
        parent.symlink_to(target, target_is_directory=True)
        self.rejected("symlink")

    def test_source_size_limit(self):
        path = self.root / self.data["capabilities"][0]["entrypoint"]
        path.write_bytes(b"x" * (registry.MAX_BYTES + 1))
        self.rejected("size bound")

    def test_bad_hash_encoding(self):
        cap = self.data["capabilities"][0]
        cap["sources"][cap["entrypoint"]] = "not-a-hash"
        self.rejected("SHA-256")

    def test_sample_with_gaps_not_promoted(self):
        cap = next(c for c in self.data["capabilities"] if c["id"] == "determinism-reference")
        cap["integrationStatus"] = "PER_PROJECT"
        self.rejected("cannot be promoted")

    def test_external_live_claim_rejected(self):
        self.data["externalWorkflows"][0]["liveDeploymentVerified"] = True
        self.rejected("cannot claim")

    def test_external_branch_ref_rejected(self):
        item = self.data["externalWorkflows"][0]
        item["sourceUrl"] = re.sub(r"/blob/[0-9a-f]{40}/", "/blob/main/", item["sourceUrl"])
        self.rejected("pin a GitHub commit")

    def test_external_non_github_source_rejected(self):
        item = self.data["externalWorkflows"][0]
        item["sourceUrl"] = item["sourceUrl"].replace("https://github.com/", "https://example.com/")
        self.rejected("pin a GitHub commit")

    def test_duplicate_external_id_rejected(self):
        self.data["externalWorkflows"][0]["id"] = "viewforge"
        self.rejected("duplicate external")

    def test_duplicate_json_key_rejected(self):
        path = self.root / "bad.json"
        path.write_text('{"schemaVersion":1,"schemaVersion":2}')
        with self.assertRaisesRegex(registry.RegistryError, "duplicate JSON key"):
            registry.read_json(path)

    def test_non_json_constant_rejected(self):
        path = self.root / "bad.json"
        path.write_text('{"value":NaN}')
        with self.assertRaisesRegex(registry.RegistryError, "numeric constant"):
            registry.read_json(path)

    def test_malformed_json_rejected(self):
        path = self.root / "bad.json"
        path.write_text('{')
        with self.assertRaises(registry.RegistryError):
            registry.read_json(path)

    def test_control_characters_in_display_text_rejected(self):
        self.data["capabilities"][0]["title"] = "bad\x1b[2J"
        self.rejected("invalid text")

    def test_shared_document_local_links_resolve(self):
        for name in ("START_HERE.md", "README.md", "capabilities/README.md",
                     "research/library-shared-entry-2026-09-22.md", "guides/workflows/codex-loop.md"):
            path = ROOT / name
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
                if target.startswith(("https://", "http://", "#")):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).exists(), f"{name}: {target}")

if __name__ == "__main__":
    unittest.main()
