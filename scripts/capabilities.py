#!/usr/bin/env python3
"""Offline, read-only capability discovery. Never executes catalog entries."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 2_000_000
KINDS = {"PLAYBOOK", "PLAYBOOK_AND_PSEUDOCODE", "REFERENCE_CATALOG",
         "EXECUTABLE_HELPER", "RUNNABLE_SAMPLE", "EXTERNAL_TOOL_LAB_FIXTURE"}
LEVELS = {"SOURCE_REVIEWED", "HISTORICAL_FIXTURE", "LIMITED_TEST_WITH_GAPS",
          "HOST_DISCOVERY_ONLY"}
INTEGRATIONS = {"NONE", "PROPOSED", "PER_PROJECT", "NOT_SHARED_IMPLEMENTATION", "REFERENCE_ONLY"}
ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
SHA256 = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}")

class RegistryError(ValueError):
    """Invalid structure, unsafe path, or stale source identity."""

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RegistryError(message)

def fields(value: Any, names: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label}: expected object")
    require(set(value) == names, f"{label}: missing or unknown fields")

def text(value: Any, label: str) -> None:
    require(isinstance(value, str) and 0 < len(value) <= 2000 and value == value.strip()
            and all(c.isprintable() for c in value), f"{label}: invalid text")

def texts(value: Any, label: str) -> None:
    require(isinstance(value, list) and 0 < len(value) <= 32, f"{label}: expected nonempty bounded list")
    for item in value:
        text(item, label)
    require(len(set(value)) == len(value), f"{label}: duplicate value")

def dated(value: Any, label: str) -> date:
    require(isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is not None,
            f"{label}: expected YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise RegistryError(f"{label}: invalid date") from exc

def local_file(root: Path, raw: Any) -> Path:
    text(raw, "source path")
    require(re.fullmatch(r"[A-Za-z0-9_. /-]+", raw) is not None, f"unsafe source path: {raw}")
    parts = raw.split("/")
    require(not PurePosixPath(raw).is_absolute() and all(p not in ("", ".", "..", ".git") for p in parts),
            f"unsafe source path: {raw}")
    current = root.resolve()
    for part in parts:
        current = current / part
        require(not current.is_symlink(), f"symlink source rejected: {raw}")
    require(current.resolve().is_relative_to(root.resolve()), f"source escapes repository: {raw}")
    require(current.is_file(), f"source missing: {raw}")
    require(current.stat().st_size <= MAX_BYTES, f"source exceeds size bound: {raw}")
    return current

def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result

def reject_constant(value: str) -> None:
    raise RegistryError(f"non-JSON numeric constant: {value}")

def read_json(path: Path) -> Any:
    require(path.is_file() and path.stat().st_size <= MAX_BYTES, "registry missing or oversized")
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates,
                          parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise RegistryError("registry is not valid bounded UTF-8 JSON") from exc

def validate(data: Any, root: Path) -> dict[str, Any]:
    fields(data, {"schemaVersion", "mode", "repository", "sourceCommit", "reviewedOn",
                  "isExecutionAuthority", "capabilities", "externalWorkflows"}, "registry")
    require(type(data["schemaVersion"]) is int and data["schemaVersion"] == 1, "unsupported schemaVersion")
    require(data["mode"] == "DISCOVERY_ONLY" and data["isExecutionAuthority"] is False,
            "registry must not grant execution authority")
    require(data["repository"] == "cloverwoodstudio/codex-game-dev-library", "repository identity mismatch")
    require(isinstance(data["sourceCommit"], str) and COMMIT.fullmatch(data["sourceCommit"]) is not None,
            "sourceCommit must be a full commit SHA")
    reviewed = dated(data["reviewedOn"], "reviewedOn")
    entries = data["capabilities"]
    require(isinstance(entries, list) and 0 < len(entries) <= 100, "invalid capability count")
    seen: set[str] = set()
    source_hashes: dict[str, str] = {}
    for entry in entries:
        fields(entry, {"id", "title", "kind", "entrypoint", "sources", "requiredTools", "inputs", "outputs",
                       "integrationStatus", "verification", "limitations", "authorizationRequired"}, "capability")
        ident = entry["id"]
        require(isinstance(ident, str) and len(ident) <= 80 and ID.fullmatch(ident) is not None, "invalid capability id")
        require(ident not in seen, f"duplicate id: {ident}")
        seen.add(ident)
        text(entry["title"], f"{ident}.title")
        require(isinstance(entry["kind"], str) and entry["kind"] in KINDS, f"{ident}: unknown kind")
        require(isinstance(entry["integrationStatus"], str) and entry["integrationStatus"] in INTEGRATIONS,
                f"{ident}: unknown integration status")
        for key in ("requiredTools", "inputs", "outputs", "limitations", "authorizationRequired"):
            texts(entry[key], f"{ident}.{key}")
        sources = entry["sources"]
        require(isinstance(sources, dict) and 0 < len(sources) <= 32, f"{ident}: invalid sources")
        for raw, expected in sources.items():
            require(isinstance(expected, str) and SHA256.fullmatch(expected) is not None, f"{ident}: invalid SHA-256")
            path = local_file(root, raw)
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            require(actual == expected, f"{ident}: source hash changed: {raw}; review required")
            require(raw not in source_hashes or source_hashes[raw] == expected, f"{ident}: conflicting source pin")
            source_hashes[raw] = expected
        text(entry["entrypoint"], f"{ident}.entrypoint")
        require(entry["entrypoint"] in sources, f"{ident}: entrypoint must be a pinned local source")
        verification = entry["verification"]
        fields(verification, {"level", "date", "scope", "evidence"}, f"{ident}.verification")
        require(isinstance(verification["level"], str) and verification["level"] in LEVELS,
                f"{ident}: unknown verification level")
        require(dated(verification["date"], f"{ident}.date") <= reviewed, f"{ident}: evidence postdates review")
        text(verification["scope"], f"{ident}.scope")
        texts(verification["evidence"], f"{ident}.evidence")
        require(all(item in sources for item in verification["evidence"]), f"{ident}: unpinned evidence")
        if verification["level"] == "LIMITED_TEST_WITH_GAPS":
            require(entry["kind"] == "RUNNABLE_SAMPLE" and entry["integrationStatus"] == "NONE",
                    f"{ident}: limited sample cannot be promoted by registry")
    external = data["externalWorkflows"]
    require(isinstance(external, list) and len(external) <= 20, "invalid external workflows")
    for item in external:
        fields(item, {"id", "title", "sourceUrl", "sourceBlobSha", "verification", "preserveOwnerReview",
                      "viewerSourceVerified", "liveDeploymentVerified", "note"}, "external workflow")
        require(isinstance(item["id"], str) and ID.fullmatch(item["id"]) is not None and item["id"] not in seen,
                "invalid or duplicate external workflow id")
        seen.add(item["id"])
        for key in ("title", "sourceUrl", "note"):
            text(item[key], key)
        url = urlsplit(item["sourceUrl"])
        require(url.scheme == "https" and url.netloc == "github.com" and not url.query and not url.fragment
                and re.fullmatch(r"/cloverwoodstudio/[A-Za-z0-9_.-]+/blob/[0-9a-f]{40}/[A-Za-z0-9_./-]+", url.path)
                is not None and ".." not in url.path.split("/"), "external source must pin a GitHub commit")
        require(isinstance(item["sourceBlobSha"], str) and COMMIT.fullmatch(item["sourceBlobSha"]) is not None,
                "external source needs Git blob identity")
        require(item["verification"] == "DOCUMENT_REVIEW_ONLY" and item["preserveOwnerReview"] is True
                and item["viewerSourceVerified"] is False and item["liveDeploymentVerified"] is False,
                "external reference cannot claim execution, deployment or owner approval")
    return {"capabilities": len(entries), "pinnedLocalFiles": len(source_hashes),
            "externalReferences": len(external), "mode": "DISCOVERY_ONLY",
            "networkVerification": "NOT_PERFORMED", "toolExecution": "NOT_PERFORMED"}

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="validate registry (default)")
    group.add_argument("--list", action="store_true", help="list routing entries; execute nothing")
    group.add_argument("--show", metavar="ID", help="print one validated entry as JSON")
    args = parser.parse_args(argv)
    try:
        data = read_json(local_file(ROOT, "capabilities/registry.json"))
        summary = validate(data, ROOT)
        if args.show is not None:
            match = next((c for c in data["capabilities"] + data["externalWorkflows"] if c["id"] == args.show), None)
            require(match is not None, f"unknown capability: {args.show}")
            print(json.dumps(match, ensure_ascii=False, indent=2))
        elif args.list:
            for c in data["capabilities"]:
                print(f"{c['id']} | {c['kind']} | {c['verification']['level']} | {c['entrypoint']}")
            for c in data["externalWorkflows"]:
                print(f"{c['id']} | EXTERNAL_WORKFLOW | DOCUMENT_REVIEW_ONLY | {c['sourceUrl']}")
        else:
            print(json.dumps({"status": "REGISTRY_CHECK_PASS", **summary}, sort_keys=True))
        return 0
    except (RegistryError, OSError, ValueError) as exc:
        print(f"REGISTRY_CHECK_FAIL: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
