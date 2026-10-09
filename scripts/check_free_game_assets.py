#!/usr/bin/env python3
"""Validate Cloverwood free-game-assets catalog and deterministic Markdown index.

No network requests, no downloading, no changes to game repositories.
Use --write-index to regenerate INDEX.md from canonical catalog.json.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "resources" / "free-game-assets"
CATALOG = DIRECTORY / "catalog.json"
INDEX = DIRECTORY / "INDEX.md"

CATEGORIES = (
    ("3d-models", "3D modely a kompletné balíky"),
    ("characters-animation", "Postavy, rigy a animácie"),
    ("materials", "Textúry, HDRI a materiály"),
    ("sfx", "Zvukové efekty"),
    ("music", "Hudba"),
    ("ui-2d", "2D grafika, ikony a UI"),
    ("vfx-shaders", "VFX a shadery"),
    ("tools", "Nástroje na tvorbu hier"),
    ("mixed-catalog", "Zmiešané katalógy"),
)
CATS = {item[0] for item in CATEGORIES}
PROJECTS = {"BB", "HOTEL_PANIC", "STARFALL_RESCUE", "SPLIT", "NELUVO", "GENERAL"}
COMMERCIAL = {"yes", "verify-item", "no"}
ATTRIBUTION = {"none", "required", "per-item", "n-a"}
ACCESS = {"free", "free-tier", "free-account"}
# Enumerated licenses are *classifications*, not proof of asset-specific clearance.
LICENSES = {
    "Apache-2.0", "CC-BY-3.0", "CC-BY-4.0", "CC0", "CC0-page",
    "GPL", "ISC", "MIT", "Mixamo-FAQ", "Mixkit-Music", "Mixkit-SFX",
    "QAL", "Sonniss", "Soundimage", "custom", "open-source",
    "per-item", "tool-terms",
}
NO_BLANKET_APPROVAL = {"custom", "per-item", "open-source", "tool-terms"}

REQUIRED = {
    "id", "name", "category", "url", "license", "license_url",
    "commercial_game_use", "attribution", "access", "projects",
    "notes", "reviewed",
}

def safe_https_url(s: str) -> bool:
    try:
        p = urlparse(s)
        return (
            p.scheme == "https"
            and bool(p.hostname)
            and p.username is None
            and p.password is None
            and not p.fragment
            and all(c not in s for c in "\r\n<>[]()\\`'\"")
        )
    except ValueError:
        return False

def validate(data: object) -> list[str]:
    errors = []
    if not isinstance(data, dict):
        return ["catalog root is not an object"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    if not isinstance(data.get("resources"), list) or not data["resources"]:
        return errors + ["resources must be non-empty array"]
    try:
        catalog_reviewed = date.fromisoformat(data["reviewed"])
        if catalog_reviewed > date.today():
            errors.append("catalog review date is in the future")
    except (KeyError, ValueError, TypeError):
        errors.append("catalog reviewed must be an ISO date")
        catalog_reviewed = None
    seen_ids = set()
    seen_urls = set()
    for i, asset in enumerate(data["resources"]):
        ref = f"resources[{i}]"
        if not isinstance(asset, dict):
            errors.append(f"{ref} is not an object")
            continue
        missing = REQUIRED - set(asset)
        if missing:
            errors.append(f"{ref} missing {sorted(missing)}")
            continue

        def string_field(field: str, minimum: int = 1) -> bool:
            value = asset[field]
            if not isinstance(value, str) or len(value.strip()) < minimum:
                errors.append(f"{ref} invalid {field}")
                return False
            if any(ord(c) < 32 or ord(c) == 127 for c in value):
                errors.append(f"{ref} control characters in {field}")
                return False
            return True

        for name, min_length in (
            ("id", 1), ("name", 3), ("category", 1),
            ("license", 1), ("commercial_game_use", 1),
            ("attribution", 1), ("access", 1),
            ("notes", 14), ("reviewed", 10),
        ):
            string_field(name, min_length)

        slug = asset["id"]
        if isinstance(slug, str):
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                errors.append(f"{ref} invalid slug")
            elif slug in seen_ids:
                errors.append(f"{ref} duplicate id {slug}")
            else:
                seen_ids.add(slug)
        for field, choices in (
            ("category", CATS),
            ("license", LICENSES),
            ("commercial_game_use", COMMERCIAL),
            ("attribution", ATTRIBUTION),
            ("access", ACCESS),
        ):
            value = asset[field]
            if not isinstance(value, str) or value not in choices:
                errors.append(f"{ref} invalid/unknown {field}")
        check_mode = asset.get("link_check_mode", "automated")
        if not isinstance(check_mode, str) or check_mode not in {"automated", "manual"}:
            errors.append(f"{ref} invalid link_check_mode")
        if check_mode == "manual" and asset["commercial_game_use"] != "verify-item":
            errors.append(f"{ref} manual link check cannot imply provider-approved use")

        for field in ("url", "license_url"):
            value = asset[field]
            if not isinstance(value, str) or not safe_https_url(value):
                errors.append(f"{ref} invalid {field}")
        url = asset["url"]
        if isinstance(url, str):
            if url in seen_urls:
                errors.append(f"{ref} duplicate URL")
            seen_urls.add(url)
        try:
            resource_reviewed = date.fromisoformat(asset["reviewed"])
            if catalog_reviewed is not None and resource_reviewed > catalog_reviewed:
                errors.append(f"{ref} resource reviewed after catalog")
        except (ValueError, TypeError):
            errors.append(f"{ref} invalid reviewed date")

        projects = asset["projects"]
        if (not isinstance(projects, list) or not projects or
            not all(isinstance(p, str) and p in PROJECTS for p in projects)):
            errors.append(f"{ref} invalid projects")
        elif len(set(projects)) != len(projects):
            errors.append(f"{ref} duplicate project IDs")

        if isinstance(asset["license"], str) and asset["license"] in NO_BLANKET_APPROVAL and asset["commercial_game_use"] == "yes":
            errors.append(f"{ref} unproven blanket commercial approval")
        if asset["commercial_game_use"] == "verify-item" and asset["attribution"] != "per-item":
            errors.append(f"{ref} mixed license needs per-item credit review")
        if asset["commercial_game_use"] == "no" and asset["attribution"] != "n-a":
            errors.append(f"{ref} prohibited game resource must have n-a attribution")
    if "mixkit-music-blocked" not in seen_ids:
        errors.append("missing mandatory Mixkit music exclusion")
    else:
        mm = next((a for a in data["resources"] if isinstance(a, dict) and a.get("id")=="mixkit-music-blocked"),None)
        if mm and mm.get("commercial_game_use") != "no":
            errors.append("Mixkit stock music MUST stay blocked for games")
    if len(data["resources"]) < 45:
        errors.append("unexpected truncation: expected at least 45 curated sources")
    return errors

def esc(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ").strip()

def make_index(data: dict) -> str:
    counts = Counter(a["category"] for a in data["resources"])
    parts = [
        "# Free Game Assets & Tools — kompletný katalóg",
        "",
        f"**{len(data['resources'])} zdrojov · Reviewed: {data['reviewed']}**",
        "",
        "Strojový register: [catalog.json](catalog.json) · "
        "[Licenčná politika](LICENSE_POLICY.md) · "
        "[Výber pre naše hry](PROJECT_RECIPES.md) · "
        "[Úvod](README.md)",
        "",
        "**Licencie:** ✅ = povolené za podmienok zdroja; "
        "⚠️ = over konkrétnu položku; ⛔ = zakázané pre videohry. "
        "Ani ✅ nenahrádza kontrolu stiahnutého archívu.",
        "",
    ]
    for category, label in CATEGORIES:
        assets = sorted((a for a in data["resources"] if a["category"]==category),key=lambda a:a["name"].casefold())
        if not assets:
            continue
        parts.extend([
            f"## {label} ({counts[category]})",
            "",
            "| Zdroj | Licencia | Hra | Dostupnosť | Odporúčané projekty | Poznámka |",
            "| --- | --- | :---: | --- | --- | --- |",
        ])
        for a in assets:
            code = {"yes":"✅","verify-item":"⚠️","no":"⛔"}[a["commercial_game_use"]]
            if a.get("link_check_mode") == "manual":
                # Preserve the canonical HTTPS URLs in JSON, but do not claim that a
                # CI-blocked provider has passed our tracked-Markdown link checker.
                u, license_u = urlparse(a["url"]), urlparse(a["license_url"])
                label_link = f"{esc(a['name'])} (`{u.netloc}{u.path}`)"
                license_link = f"{esc(a['license'])} (`{license_u.netloc}{license_u.path}`)"
            else:
                label_link = f"[{esc(a['name'])}]({a['url']})"
                license_link = f"[{esc(a['license'])}]({a['license_url']})"
            projects = ", ".join(a["projects"])
            access = a["access"].replace("free-tier","free časť").replace("free-account","účet zdarma").replace("free","zdarma")
            parts.append(f"| {label_link} | {license_link} | {code} | {access} | {esc(projects)} | {esc(a['notes'])} |")
        parts.append("")
    parts.extend([
        "## Výslovné upozornenia",
        "",
        "- **Mixkit:** zvukové efekty sú povolené vo videohrách, stock music nie.",
        "- **QAL:** distribúcia hotovej hry je povolená, samostatné rehostovanie zdrojových modelov nie.",
        "- **Trhoviská:** cena zdarma neznamená povolenie komerčného použitia.",
        "- **KayKit a Quaternius:** bezplatný pack nemusí obsahovať platené varianty ani zdrojové .blend súbory.",
        "- **Licencie sa môžu zmeniť.** Ukladaj doklad z dňa stiahnutia a SHA originálu.",
        "",
        "Táto knižnica neobsahuje binárne assety a nie je povolením na ich integráciu do hry.",
        "",
    ])
    return "\n".join(parts)

def main() -> int:
    parser=argparse.ArgumentParser()
    grp=parser.add_mutually_exclusive_group()
    grp.add_argument("--write-index",action="store_true")
    grp.add_argument("--check",action="store_true")
    args=parser.parse_args()
    try:
        data=json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        print(f"CATALOG_PARSE_FAIL {exc}",file=sys.stderr)
        return 1
    errors=validate(data)
    if errors:
        print("\n".join("CATALOG_ERROR "+e for e in errors),file=sys.stderr)
        return 1
    rendered=make_index(data)
    if args.write_index:
        INDEX.write_text(rendered,encoding="utf-8")
        print(f"CATALOG_INDEX_WRITTEN {len(data['resources'])} sources")
        return 0
    if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != rendered:
        print("INDEX_OUT_OF_SYNC: python3 scripts/check_free_game_assets.py --write-index",file=sys.stderr)
        return 1
    print(f"CATALOG_CHECK_PASS sources={len(data['resources'])} categories={len(CATS)} index=SYNC")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
