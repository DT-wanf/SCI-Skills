#!/usr/bin/env python3
"""Validate a SCI-Skills expert-result YAML without third-party packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = [
    "contract_version",
    "expert_skill",
    "project_id",
    "paper_family",
    "stage_id",
    "task_id",
    "task_status",
    "inputs_reviewed",
    "outputs",
    "evidence_status",
    "assumptions",
    "author_input_needed",
    "manual_actions",
    "quality_checks",
    "conflicts",
    "conflict_resolution_status",
    "merge_permission",
    "recommended_next_action",
    "stage_acceptance_recommendation",
]

ALLOWED_STATUS = {"COMPLETE", "PARTIAL", "BLOCKED", "PROVISIONAL"}
ALLOWED_RECOMMENDATION = {"PASS_CANDIDATE", "REPAIR", "BLOCKED", "NOT_ASSESSED"}
ALLOWED_CONFLICT = {"NOT_REQUIRED", "UNRESOLVED", "RESOLVED_BY_ORCHESTRATOR"}
LIST_FIELDS = {"inputs_reviewed", "outputs", "evidence_status", "assumptions", "author_input_needed", "manual_actions", "quality_checks", "conflicts"}


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^#\n]*)", text)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def list_items(text: str, key: str) -> list[str] | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^#\n]*)", text)
    if not match:
        return None
    inline = match.group(1).strip()
    if inline:
        if not (inline.startswith("[") and inline.endswith("]")):
            return None
        content = inline[1:-1].strip()
        return [] if not content else [item.strip().strip("\"'") for item in content.split(",") if item.strip()]
    tail = text[match.end():]
    items = []
    for line in tail.splitlines():
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")):
            break
        item = re.match(r"^\s*-\s+(.+)$", line)
        if item:
            items.append(item.group(1).strip())
    return items


def meaningful(value: str | None) -> bool:
    return value not in (None, "", "null", "~")


def validate(path: Path, task_path: Path | None = None) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [f"missing field: {key}" for key in REQUIRED if not re.search(rf"(?m)^{re.escape(key)}:", text)]
    if scalar(text, "contract_version") != "1.0":
        errors.append("contract_version must be 1.0")
    for key in LIST_FIELDS:
        if list_items(text, key) is None:
            errors.append(f"{key} must be a YAML list")
    for key in ("expert_skill", "task_status", "recommended_next_action", "stage_acceptance_recommendation"):
        if not meaningful(scalar(text, key)):
            errors.append(f"{key} must not be empty")
    status = scalar(text, "task_status")
    if status and status not in ALLOWED_STATUS:
        errors.append(f"invalid task_status: {status}")
    recommendation = scalar(text, "stage_acceptance_recommendation")
    if recommendation and recommendation not in ALLOWED_RECOMMENDATION:
        errors.append(f"invalid stage_acceptance_recommendation: {recommendation}")
    conflict_status = scalar(text, "conflict_resolution_status")
    if conflict_status not in ALLOWED_CONFLICT:
        errors.append(f"invalid conflict_resolution_status: {conflict_status}")
    if scalar(text, "merge_permission") != "orchestrator_only":
        errors.append("merge_permission must be orchestrator_only")
    conflicts = list_items(text, "conflicts") or []
    if conflicts and conflict_status == "NOT_REQUIRED":
        errors.append("non-empty conflicts require UNRESOLVED or RESOLVED_BY_ORCHESTRATOR")
    if recommendation == "PASS_CANDIDATE":
        if status != "COMPLETE":
            errors.append("PASS_CANDIDATE requires task_status COMPLETE")
        for key in ("inputs_reviewed", "outputs", "evidence_status", "quality_checks"):
            if not list_items(text, key):
                errors.append(f"PASS_CANDIDATE requires non-empty {key}")
        if conflict_status == "UNRESOLVED":
            errors.append("PASS_CANDIDATE cannot contain unresolved conflicts")

    component = Path(__file__).resolve().parents[1] / "component.yaml"
    if component.exists():
        component_text = component.read_text(encoding="utf-8")
        expected_skill = scalar(component_text, "component_name")
        component_type = scalar(component_text, "component_type")
        if component_type == "expert" and expected_skill and scalar(text, "expert_skill") != expected_skill:
            errors.append(f"expert_skill must match component_name: {expected_skill}")

    if task_path is not None:
        task = task_path.read_text(encoding="utf-8")
        for key in ("contract_version", "project_id", "paper_family", "stage_id", "task_id", "expert_skill"):
            expected = scalar(task, key)
            actual = scalar(text, key)
            if meaningful(expected) and expected != actual:
                errors.append(f"task identity mismatch for {key}: expected {expected}, got {actual}")
    return errors


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("usage: validate_expert_contract.py EXPERT_RESULT.yaml [EXPERT_TASK.yaml]")
        return 2
    errors = validate(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) == 3 else None)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: SCI-Skills expert contract 1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
