#!/usr/bin/env python3
"""Pure-standard-library Tripo Studio export manifest and game-asset QA policy."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ASSET_ID = re.compile(r"^[A-Za-z0-9._-]{3,80}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
ENGINES = {"unity", "godot"}
LICENSES = {"unverified", "noncommercial", "commercial_evidence_recorded"}


def hash_file(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def validate_manifest(payload: dict, expected_sha: str) -> list[str]:
    """Validate *claims*, not payment, studio login, or source authenticity."""
    failures = []
    if not isinstance(payload, dict):
        return ["manifest_must_be_object"]
    required = {
        "schema_version": 1,
        "source": "tripo_studio",
        "source_file_sha256": expected_sha,
    }
    for key, value in required.items():
        if payload.get(key) != value:
            failures.append(f"bad_{key}")
    if not isinstance(payload.get("asset_id"), str) or not ASSET_ID.fullmatch(payload["asset_id"]):
        failures.append("invalid_asset_id")
    if payload.get("target_engine") not in ENGINES:
        failures.append("invalid_target_engine")
    if payload.get("license_status") not in LICENSES:
        failures.append("invalid_license_status")
    if not isinstance(payload.get("export_method"), str) or payload.get("export_method") not in {"studio_download", "studio_dcc_bridge"}:
        failures.append("invalid_export_method")
    if not isinstance(payload.get("notes"), str):
        failures.append("missing_notes")
    return failures


def evaluate(metrics: dict, budget: dict, manifest: dict | None) -> dict:
    """Independent technical QA; never grants approval to ship."""
    errors = []
    warnings = []
    if metrics.get("mesh_count", 0) <= 0 or metrics.get("triangles", 0) <= 0:
        errors.append("no_renderable_mesh")
    if metrics.get("nonfinite_coordinate_count", 0) != 0:
        errors.append("nonfinite_vertex_coordinate")
    if metrics.get("triangles", 0) > budget["max_triangles"]:
        errors.append("triangle_budget_exceeded")
    if metrics.get("material_count", 0) > budget["max_materials"]:
        errors.append("material_budget_exceeded")
    if budget["require_uv"] and metrics.get("uv_layer_count", 0) == 0:
        errors.append("uv_required_but_missing")
    if budget["expect_rig"] and (metrics.get("armatures", 0) == 0 or metrics.get("bones", 0) == 0):
        errors.append("rig_expected_missing")
    if budget["expect_rig"] and metrics.get("weighted_vertices", 0) == 0:
        errors.append("skin_weights_expected_missing")
    if budget["expect_animation"] and metrics.get("animation_actions", 0) == 0:
        errors.append("animation_expected_missing")
    if metrics.get("uv_layer_count", 0) == 0:
        warnings.append("uv_absent_check_texturing")
    if metrics.get("image_count", 0) == 0:
        warnings.append("no_images_embedded_or_loaded")
    if metrics.get("armatures", 0) and metrics.get("weighted_vertices", 0) == 0:
        warnings.append("rig_present_without_skin_weights")
    if not manifest:
        warnings.append("studio_source_not_attested")
    elif manifest.get("license_status") != "commercial_evidence_recorded":
        warnings.append("commercial_license_not_verified")
    return {
        "technical_status": "FIX" if errors else "PASS_WITH_WARNINGS" if warnings else "PASS",
        "shipping_status": "HOLD_OWNER_REVIEW",
        "failures": errors,
        "warnings": warnings,
    }


def read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON root must be object")
    return data
