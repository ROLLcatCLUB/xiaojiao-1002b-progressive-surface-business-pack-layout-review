from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

STAGE = "1002B_PROGRESSIVE_SURFACE_MODE_AND_BUSINESS_PACK_LAYOUT_PRESET_FIXTURE"
FINAL = "XIAOJIAO_PROGRESSIVE_SURFACE_MODE_AND_BUSINESS_PACK_LAYOUT_PRESET_FIXTURE_PASS"
SLUG = "xiaojiao_progressive_surface_mode_and_business_pack_layout_preset_fixture_1002B"
MARKER = "ALL_1002B_PROGRESSIVE_SURFACE_MODE_AND_BUSINESS_PACK_LAYOUT_PRESET_FIXTURE_CHECKS_OK"
REQUIRED_PACKS = {
    "teaching_plan_pack",
    "lesson_design_pack",
    "classroom_teaching_studio_pack",
    "student_evaluation_pack",
    "resource_library_pack",
    "resource_curation_pack",
}
REQUIRED_MODES = {
    "guided_flow",
    "focus_surface",
    "grid_studio",
    "analysis_board",
    "support_layer",
    "resource_drawer",
    "resource_picker",
    "teacher_control_surface",
    "public_display_surface",
}
BAD_PARTS = [".env", "token", "secret", "key", "node_modules", "__pycache__", ".db", ".sqlite", "dist", "build", "coverage", ".DS_Store"]


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION_FAILED: {message}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    required = [
        "docs/audit/xiaojiao_grid_based_dynamic_work_surface_tech_survey_and_contract_1002A_review_decision.json",
        f"docs/foundation/{SLUG}.md",
        f"docs/foundation/{SLUG}.json",
        f"samples/{SLUG}/progressive_surface_business_pack_fixture_1002B.json",
        f"docs/audit/{SLUG}_result.json",
        f"docs/audit/{SLUG}_report.md",
        f"docs/audit/{SLUG}_checklist.json",
        f"docs/audit_packages/{SLUG}_manifest.json",
        f"scripts/validate_{SLUG}.py",
    ]
    for rel in required:
        if not (root / rel).exists():
            fail(f"missing required file: {rel}")

    decision = load_json(root / "docs/audit/xiaojiao_grid_based_dynamic_work_surface_tech_survey_and_contract_1002A_review_decision.json")
    if decision.get("review_decision") != "ACCEPT":
        fail("1002A review decision not accepted")
    contract = load_json(root / f"docs/foundation/{SLUG}.json")
    sample = load_json(root / f"samples/{SLUG}/progressive_surface_business_pack_fixture_1002B.json")
    result = load_json(root / f"docs/audit/{SLUG}_result.json")
    manifest = load_json(root / f"docs/audit_packages/{SLUG}_manifest.json")

    if contract.get("stage_code") != STAGE or sample.get("stage_code") != STAGE or result.get("stage_code") != STAGE:
        fail("stage identity mismatch")
    if result.get("final_status") != FINAL or result.get("pass") is not True or result.get("marker") != MARKER:
        fail("result pass/final_status/marker mismatch")

    modes = {mode.get("mode") for mode in sample.get("surface_modes", [])}
    if not REQUIRED_MODES.issubset(modes):
        fail("required surface modes missing")
    packs = {pack.get("business_pack"): pack for pack in sample.get("business_pack_layout_presets", [])}
    if set(packs) != REQUIRED_PACKS:
        fail("business pack set mismatch")
    if packs["teaching_plan_pack"].get("recommended_surface_mode") != "guided_flow" or packs["teaching_plan_pack"].get("not_default_grid_studio") is not True:
        fail("teaching plan must be guided_flow and not default grid studio")
    if packs["resource_library_pack"].get("recommended_surface_mode") != "support_layer" or packs["resource_library_pack"].get("not_default_grid_studio") is not True:
        fail("resource library must be support layer and not default grid studio")
    if "resource_drawer" not in packs["resource_library_pack"].get("additional_surfaces", []) or "resource_picker" not in packs["resource_library_pack"].get("additional_surfaces", []):
        fail("resource library drawer/picker missing")
    if packs["classroom_teaching_studio_pack"].get("recommended_surface_mode") != "grid_studio":
        fail("classroom teaching studio must be grid_studio")
    if "teacher_control_surface" not in packs["classroom_teaching_studio_pack"].get("additional_surfaces", []) or "public_display_surface" not in packs["classroom_teaching_studio_pack"].get("additional_surfaces", []):
        fail("classroom teaching studio surfaces missing")
    if packs["student_evaluation_pack"].get("recommended_surface_mode") != "analysis_board":
        fail("student evaluation must be analysis_board")
    if packs["resource_curation_pack"].get("recommended_surface_mode") != "grid_studio":
        fail("resource curation must be grid_studio")
    if sample.get("resource_layer_policy", {}).get("resource_library_as_main_studio_default") is not False:
        fail("resource library cannot be main studio by default")
    if sample.get("classroom_teaching_studio_future_scope", {}).get("runtime_implemented") is not False:
        fail("classroom runtime must not be implemented")

    for mapping in [contract.get("hard_boundaries", {}), sample.get("boundary_flags", {}), result.get("boundary_flags", {})]:
        for key, value in mapping.items():
            if value is not False:
                fail(f"unsafe boundary: {key}")

    zip_path = root / f"docs/audit_packages/{SLUG}.zip"
    if not zip_path.exists():
        fail("missing zip")
    with zipfile.ZipFile(zip_path) as zf:
        zip_entries = zf.namelist()
    for entry in zip_entries:
        normalized = entry.replace("\\", "/")
        if normalized.startswith("/") or ":" in normalized or "\\" in entry:
            fail(f"unsafe zip path: {entry}")
        if any(part.lower() in normalized.lower() for part in BAD_PARTS):
            fail(f"forbidden zip entry: {entry}")
    if manifest.get("manifest_minus_zip") != [] or manifest.get("zip_minus_manifest") != []:
        fail("manifest alignment not empty")
    if sorted(manifest.get("zip_entries", [])) != sorted(zip_entries):
        fail("manifest zip entries mismatch")

    print(MARKER)
    return 0


if __name__ == "__main__":
    sys.exit(main())