"""Offline validation regressions for the free-game-assets catalog."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("check_free_game_assets",ROOT/"scripts"/"check_free_game_assets.py")
lib=importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)
BASE=json.loads(lib.CATALOG.read_text(encoding="utf-8"))

class CatalogTest(unittest.TestCase):
    def test_real_catalog_valid(self):
        self.assertEqual([],lib.validate(BASE))
        self.assertGreaterEqual(len(BASE["resources"]),45)

    def test_duplicate_slug_rejected(self):
        data=copy.deepcopy(BASE)
        data["resources"][1]["id"]=data["resources"][0]["id"]
        self.assertTrue(any("duplicate id" in x for x in lib.validate(data)))

    def test_bad_licenses_rejected(self):
        data=copy.deepcopy(BASE)
        x=next(a for a in data["resources"] if a["id"]=="freesound")
        x["commercial_game_use"]="yes"
        self.assertTrue(any("unproven blanket commercial approval" in x for x in lib.validate(data)))

    def test_mixkit_music_cannot_be_allowed(self):
        data=copy.deepcopy(BASE)
        x=next(a for a in data["resources"] if a["id"]=="mixkit-music-blocked")
        x["commercial_game_use"]="yes"
        self.assertTrue(any("MUST stay blocked" in x for x in lib.validate(data)))

    def test_https_only(self):
        data=copy.deepcopy(BASE)
        data["resources"][0]["url"]="http://kenney.nl/"
        self.assertTrue(any("invalid url" in x for x in lib.validate(data)))

    def test_provider_blocked_urls_keep_manual_gate(self):
        data=copy.deepcopy(BASE)
        godot=next(x for x in data["resources"] if x["id"]=="godot-shaders")
        self.assertEqual("manual",godot["link_check_mode"])
        self.assertEqual("verify-item",godot["commercial_game_use"])
        index=lib.make_index(data)
        self.assertIn("godotshaders.com/license/",index)
        self.assertNotIn("https://godotshaders.com/",index)
        incompetech=next(x for x in data["resources"] if x["id"]=="incompetech")
        self.assertEqual("incompetech.com",__import__("urllib.parse",fromlist=["urlparse"]).urlparse(incompetech["license_url"]).hostname)

    def test_bad_field_types_do_not_crash(self):
        examples = [
            ("id", {}),
            ("category", []),
            ("license", {"wrong": True}),
            ("url", ["https://example.com"]),
            ("notes", None),
            ("projects", [["BB"]]),
            ("commercial_game_use", None),
            ("attribution", []),
            ("reviewed", {}),
        ]
        for field, bad in examples:
            with self.subTest(field=field):
                data = copy.deepcopy(BASE)
                data["resources"][0][field] = bad
                self.assertTrue(lib.validate(data), f"bad {field} accepted")

    def test_unknown_licenses_and_unsafe_urls_rejected(self):
        data = copy.deepcopy(BASE)
        data["resources"][0]["license"] = "INVENTED"
        self.assertTrue(any("unknown license" in x for x in lib.validate(data)))
        data = copy.deepcopy(BASE)
        data["resources"][0]["url"] = "https://example.com/foo)(bad"
        self.assertTrue(any("invalid url" in x for x in lib.validate(data)))

    def test_unverified_tool_and_material_entries_gated(self):
        for resource_id in ("texturecan", "material-maker", "jfxr", "bosca-ceoil-blue"):
            with self.subTest(resource_id=resource_id):
                rec = next(x for x in BASE["resources"] if x["id"] == resource_id)
                self.assertEqual(rec["commercial_game_use"], "verify-item")
                self.assertEqual(rec["attribution"], "per-item")

    def test_ambiguous_tool_licensing_cannot_be_marked_approved(self):
        data = copy.deepcopy(BASE)
        x = next(x for x in data["resources"] if x["id"] == "material-maker")
        x["commercial_game_use"] = "yes"
        self.assertTrue(any("unproven blanket" in x for x in lib.validate(data)))

    def test_generated_markdown_rejects_spoofed_links(self):
        data = copy.deepcopy(BASE)
        entry = data["resources"][0]
        entry["name"] = "Kenney Source](https://evil.invalid/collect)[Impostor"
        entry["notes"] = "Helpful! [Download](https://evil.invalid/) <img src='https://evil.invalid/pixel'>"
        # Invalid catalog entries are rejected before generation; rendering
        # remains safely escaped as defense in depth.
        self.assertTrue(any("URL-like content" in x for x in lib.validate(data)))
        index = lib.make_index(data)
        self.assertIn("https://kenney.nl/assets", index)
        self.assertNotIn("](https://evil.invalid", index)
        self.assertNotIn("<img", index)
        self.assertIn("&lt;img", index)
        self.assertIn(r"\]\(https://evil.invalid/collect\)\[", index)

    def test_generated_markdown_table_text_is_escaped(self):
        data = copy.deepcopy(BASE)
        record = data["resources"][0]
        record["name"] = "Safe | widgets *bold* and backslash \\\\"
        record["notes"] = "A | B & <script>alert(1)</script> ![image](malicious)"
        self.assertEqual([], lib.validate(data))
        index = lib.make_index(data)
        self.assertIn(r"Safe \| widgets \*bold\*", index)
        self.assertIn("&amp;", index)
        self.assertIn("&lt;script&gt;", index)
        self.assertNotIn("<script>", index)
        self.assertNotIn("![image](", index)

    def test_autolinks_are_rejected_in_plain_text_fields(self):
        for field, value in (
            ("name", "Free asset https://evil.invalid/redirect"),
            ("notes", "Check www.evil.invalid for more details"),
        ):
            with self.subTest(field=field):
                data = copy.deepcopy(BASE)
                data["resources"][0][field] = value
                self.assertTrue(any("URL-like content not allowed" in x for x in lib.validate(data)))

    def test_url_rejects_nonpublic_and_numeric_hosts(self):
        unsafe = (
            "https://127.0.0.1:8443/admin",
            "https://127.0.0.1/",
            "https://8.8.8.8/",
            "https://169.254.169.254/latest/meta-data/",
            "https://192.168.1.1/",
            "https://10.0.0.10/",
            "https://172.16.2.3/",
            "https://[::1]/",
            "https://[fe80::1]/",
            "https://[::ffff:127.0.0.1]/",
            "https://2130706433/",
            "https://0x7f000001/",
            "https://0177.0.0.1/",
            "https://localhost/",
            "https://localhost./",
            "https://renderer.internal/private",
            "https://server.local/",
            "https://foo.lan/",
            "https://metadata.google.internal/",
            "https://example.com:8443/private",
            "https://example.com@127.0.0.1/",
            "https://exa%6dple.com/",
            "https://example.com\\@evil.invalid/",
        )
        for url in unsafe:
            with self.subTest(url=url):
                self.assertFalse(lib.safe_https_url(url), url)
                data = copy.deepcopy(BASE)
                data["resources"][0]["license_url"] = url
                self.assertTrue(any("invalid license_url" in e for e in lib.validate(data)))
        for url in ("https://kenney.nl/assets", "https://quaternius.com/license.html",
                    "https://github.com/YuriSizov/boscaceoil-blue"):
            with self.subTest(good=url):
                self.assertTrue(lib.safe_https_url(url), url)

    def test_index_deterministic(self):
        idx=lib.make_index(BASE)
        self.assertIn("Mixkit Stock Music",idx)
        self.assertIn("## 3D modely",idx)
        self.assertEqual(idx,lib.make_index(BASE))

if __name__=="__main__":
    unittest.main()
