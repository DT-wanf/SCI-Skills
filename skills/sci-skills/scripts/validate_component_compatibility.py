#!/usr/bin/env python3
"""Validate SCI-Skills 3.0.2 component, contract, and core compatibility."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT.parent
EXPECTED = {
    "sci-skills-literature-search",
    "sci-skills-paper-deep-reading",
    "sci-skills-manuscript-writing",
    "sci-skills-academic-polishing",
    "sci-skills-scientific-figures",
    "sci-skills-statistical-reporting",
    "sci-skills-paper-presentation",
    "sci-skills-presubmission-review",
    "sci-skills-reviewer-response",
    "sci-skills-data-availability",
    "sci-skills-web-data-acquisition",
    "sci-skills-aigc-authorial-rewriting",
    "sci-skills-journal-recommendation",
}
CORE_FILES = [
    ROOT / "references" / "expert-core" / name
    for name in ("expert-contract.md", "evidence-labels.md", "zero-api-policy.md", "manual-operation-companion.md", "stage-authority-boundary.md")
] + [ROOT / "references" / "adapters" / "local-adapters.md"]


def value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^#\n]+)", text)
    return match.group(1).strip().strip("\"'") if match else None


def core_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(CORE_FILES):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    discovered: dict[str, Path] = {}
    for skill_path in SKILLS_ROOT.glob("*/SKILL.md"):
        text = skill_path.read_text(encoding="utf-8")
        name = value(text, "name")
        if name in EXPECTED:
            discovered[name] = skill_path.parent
    if set(discovered) != EXPECTED:
        errors.append(f"expert set mismatch missing={sorted(EXPECTED - discovered.keys())}")
    expected_hash = core_hash()
    required_files = [
        "component.yaml",
        "references/playbook.md",
        "references/_core/expert-contract.md",
        "references/_core/manual-operation-companion.md",
        "references/_core/local-adapters.md",
        "schemas/expert-task.yaml",
        "schemas/expert-result.yaml",
        "schemas/expert-conflict.yaml",
        "schemas/specialist-output.yaml",
        "templates/operation-companion-prompt.md",
        "templates/operation-return-card.md",
        "scripts/validate_expert_contract.py",
    ]
    for name, directory in sorted(discovered.items()):
        for relative in required_files:
            if not (directory / relative).exists():
                errors.append(f"{name} missing {relative}")
        component = (directory / "component.yaml").read_text(encoding="utf-8")
        for key, expected in (("suite_version", "3.0.2"), ("contract_version", "1.0"), ("core_snapshot_version", "1.0"), ("core_snapshot_sha256", expected_hash), ("zero_external_api", "true"), ("stage_authority", "sci-skills")):
            if value(component, key) != expected:
                errors.append(f"{name} incompatible {key}: {value(component, key)}")
        for core in CORE_FILES:
            snapshot = directory / "references" / "_core" / core.name
            if snapshot.exists() and snapshot.read_bytes() != core.read_bytes():
                errors.append(f"{name} core drift: {core.name}")
        conflict_schema = (directory / "schemas" / "expert-conflict.yaml").read_text(encoding="utf-8")
        for field in ("conflict_id:", "project_id:", "paper_family:", "stage_id:", "task_ids:", "expert_skills:", "conflict_type:", "claim_or_decision:", "positions:", "resolution_status:", "orchestrator_decision:", "decision_basis:"):
            if field not in conflict_schema:
                errors.append(f"{name} conflict schema missing {field}")
    if errors:
        print("COMPONENT COMPATIBILITY FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("COMPONENT COMPATIBILITY PASSED: 1 orchestrator + 13 self-contained experts")
    print(f"Core snapshot sha256: {expected_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
