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
        self.assertTrue(any("globally approved" in x for x in lib.validate(data)))

    def test_mixkit_music_cannot_be_allowed(self):
        data=copy.deepcopy(BASE)
        x=next(a for a in data["resources"] if a["id"]=="mixkit-music-blocked")
        x["commercial_game_use"]="yes"
        self.assertTrue(any("MUST stay blocked" in x for x in lib.validate(data)))

    def test_https_only(self):
        data=copy.deepcopy(BASE)
        data["resources"][0]["url"]="http://kenney.nl/"
        self.assertTrue(any("invalid url" in x for x in lib.validate(data)))

    def test_index_deterministic(self):
        idx=lib.make_index(BASE)
        self.assertIn("Mixkit Stock Music",idx)
        self.assertIn("## 3D modely",idx)
        self.assertEqual(idx,lib.make_index(BASE))

if __name__=="__main__":
    unittest.main()
