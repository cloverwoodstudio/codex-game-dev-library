"""Pure Python safety gate tests (no Blender installation needed in CI)."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/studio_asset_contract.py"
spec = importlib.util.spec_from_file_location("studio_asset_contract", SCRIPT)
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)


class StudioAssetContractTest(unittest.TestCase):
    def setUp(self):
        self.sha = "a" * 64
        self.valid = {
            "schema_version": 1,
            "source": "tripo_studio",
            "asset_id": "NUKU-ASSET-001",
            "source_file_sha256": self.sha,
            "target_engine": "unity",
            "export_method": "studio_download",
            "license_status": "unverified",
            "notes": "Owner-supplied Studio export notes",
        }
        self.stats = {
            "mesh_count": 2,
            "triangles": 10000,
            "nonfinite_coordinate_count": 0,
            "material_count": 2,
            "uv_layer_count": 1,
            "armatures": 1,
            "bones": 25,
            "weighted_vertices": 5000,
            "animation_actions": 3,
            "image_count": 2,
        }
        self.budget = {
            "max_triangles": 25000,
            "max_materials": 8,
            "require_uv": True,
            "expect_rig": True,
            "expect_animation": True,
        }

    def test_valid_tripo_studio_provenance(self):
        self.assertEqual(contract.validate_manifest(self.valid, self.sha), [])

    def test_api_origin_not_accepted(self):
        fake = dict(self.valid, source="tripo_api")
        self.assertIn("bad_source", contract.validate_manifest(fake, self.sha))

    def test_sha_binding_rejects_mismatch(self):
        fake = dict(self.valid, source_file_sha256="b"*64)
        self.assertIn("bad_source_file_sha256", contract.validate_manifest(fake, self.sha))

    def test_wrong_engine(self):
        fake = dict(self.valid, target_engine="unreal")
        self.assertIn("invalid_target_engine", contract.validate_manifest(fake, self.sha))

    def test_no_license_autopromotion(self):
        result = contract.evaluate(self.stats, self.budget, dict(self.valid, license_status="commercial_evidence_recorded"))
        self.assertEqual(result["technical_status"], "PASS")
        self.assertEqual(result["shipping_status"], "HOLD_OWNER_REVIEW")

    def test_missing_skin_weights_is_fix(self):
        stats = dict(self.stats, weighted_vertices=0)
        self.assertIn("skin_weights_expected_missing", contract.evaluate(stats, self.budget, self.valid)["failures"])

    def test_missing_animation_is_fix(self):
        stats = dict(self.stats, animation_actions=0)
        self.assertIn("animation_expected_missing", contract.evaluate(stats, self.budget, self.valid)["failures"])

    def test_triangle_budget_is_enforced(self):
        stats = dict(self.stats, triangles=25001)
        self.assertEqual(contract.evaluate(stats, self.budget, self.valid)["technical_status"], "FIX")

    def test_negative_zero_geometry(self):
        stats = dict(self.stats, triangles=0)
        self.assertIn("no_renderable_mesh", contract.evaluate(stats, self.budget, self.valid)["failures"])

    def test_uv_required(self):
        stats = dict(self.stats, uv_layer_count=0)
        self.assertIn("uv_required_but_missing", contract.evaluate(stats, self.budget, self.valid)["failures"])

    def test_provenance_unknown_is_hold(self):
        result = contract.evaluate(self.stats, self.budget, None)
        self.assertIn("studio_source_not_attested", result["warnings"])

    def test_streamed_source_hash(self):
        with tempfile.TemporaryDirectory() as t:
            file = Path(t) / "original.glb"
            file.write_bytes(b"safe source")
            before = contract.hash_file(file)
            self.assertEqual(before, contract.hash_file(file))
            self.assertEqual(len(before), 64)


if __name__ == "__main__":
    unittest.main()
