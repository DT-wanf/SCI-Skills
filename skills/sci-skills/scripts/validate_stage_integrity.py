#!/usr/bin/env python3
"""Protect the five SCI-Skills paper families and all 35 stage contracts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {f"{family}{number}" for family in "EIMTR" for number in range(1, 8)}
FAMILY_NAMES = {"E": "empirical", "I": "interpretive", "M": "method-application", "T": "theoretical", "R": "review"}
REQUIRED = ["stage_id:", "required fields", "optional fields", "defaultable fields", "evidence-locked fields", "deliverables", "acceptance", "expert_candidates:", "action_type_default:", "external_playbook:"]


def main() -> int:
    errors: list[str] = []
    found: dict[str, Path] = {}
    for path in (ROOT / "workflows").glob("*/*.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^stage_id:\s*([EIMTR][1-7])\s*$", text)
        if not match:
            errors.append(f"invalid stage id: {path.relative_to(ROOT)}")
            continue
        stage = match.group(1)
        if stage in found:
            errors.append(f"duplicate stage: {stage}")
        found[stage] = path
        family_match = re.search(r"(?m)^paper_family:\s*([a-z-]+)\s*$", text)
        expected_family = FAMILY_NAMES[stage[0]]
        if not family_match or family_match.group(1) != expected_family:
            errors.append(f"{stage} paper_family must be {expected_family}")
        for token in REQUIRED:
            if token.casefold() not in text.casefold():
                errors.append(f"{stage} missing {token}")
    missing, extra = EXPECTED - found.keys(), found.keys() - EXPECTED
    if missing or extra:
        errors.append(f"stage set mismatch missing={sorted(missing)} extra={sorted(extra)}")
    diagnosis = (ROOT / "references" / "stage-diagnosis.md").read_text(encoding="utf-8")
    diagnosis_ids = set(re.findall(r"(?m)^####\s+([EIMTR][1-7])\s+—", diagnosis))
    if diagnosis_ids != EXPECTED:
        errors.append(f"diagnosis matrix mismatch missing={sorted(EXPECTED - diagnosis_ids)} extra={sorted(diagnosis_ids - EXPECTED)}")
    if diagnosis.count("Core outputs:") != 35 or diagnosis.count("Minimum pass evidence:") != 35:
        errors.append("diagnosis matrix must contain 35 output summaries and 35 pass-evidence summaries")
    for stage, tokens in {
        "E5": ["data", "statistical-reporting", "scientific-figures"],
        "E7": ["presubmission-review", "journal-recommendation"],
        "R2": ["literature-search"],
        "M5": ["statistical-reporting", "scientific-figures"],
    }.items():
        text = found.get(stage, Path()).read_text(encoding="utf-8") if stage in found else ""
        for token in tokens:
            if token.casefold() not in text.casefold():
                errors.append(f"{stage} safety route missing {token}")
    if errors:
        print("STAGE INTEGRITY FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("STAGE INTEGRITY PASSED: 5 families, 35 stages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
