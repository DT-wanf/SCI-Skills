#!/usr/bin/env python3
"""Rebuild the compact 35-stage diagnosis matrix from authoritative modules."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "references" / "stage-diagnosis.md"
FAMILY_ORDER = {"E": 0, "I": 1, "M": 2, "T": 3, "R": 4}
FAMILY_NAMES = {"E": "Empirical / 实证类", "I": "Interpretive / 阐释类", "M": "Method-Application / 方法应用类", "T": "Theoretical / 理论类", "R": "Review / 综述类"}


def section(text: str, heading: str, next_pattern: str = r"^## ") -> str:
    match = re.search(rf"(?ms)^{re.escape(heading)}\s*\n(.*?)(?={next_pattern}|\Z)", text)
    return match.group(1).strip() if match else ""


def bullets(block: str) -> list[str]:
    return [re.sub(r"\s+", " ", item.strip()) for item in re.findall(r"(?m)^-\s+(.+)$", block)]


def main() -> int:
    stages = []
    for path in (ROOT / "workflows").glob("*/*.md"):
        text = path.read_text(encoding="utf-8")
        stage_match = re.search(r"(?m)^stage_id:\s*([EIMTR][1-7])\s*$", text)
        title_match = re.search(r"(?m)^#\s+[EIMTR][1-7]\s+-\s+(.+)$", text)
        if not stage_match or not title_match:
            continue
        stage = stage_match.group(1)
        deliverables = bullets(section(text, "## Source-defined deliverables"))
        acceptance_match = re.search(r"(?ms)^### Acceptance criteria\s*\n(.*?)(?=\nA stage is|^## |\Z)", text)
        acceptance = bullets(acceptance_match.group(1) if acceptance_match else "")
        if not deliverables or not acceptance:
            raise SystemExit(f"cannot summarize {stage}: missing deliverables or acceptance criteria")
        stages.append((stage, title_match.group(1).strip(), deliverables, acceptance))
    stages.sort(key=lambda item: (FAMILY_ORDER[item[0][0]], int(item[0][1:])))
    if len(stages) != 35:
        raise SystemExit(f"expected 35 stages, found {len(stages)}")

    lines = [
        "# Stage Diagnosis",
        "",
        "## Rule",
        "",
        "The actual stage is the earliest essential stage that has not met its acceptance criteria. A manuscript draft, code repository, dataset, figure, or partial result does not automatically validate preceding stages.",
        "",
        "## Procedure",
        "",
        "1. Record the user's self-reported stage and available artifacts.",
        "2. Select the likely paper family and scan that family's compact matrix from stage 1 onward.",
        "3. Compare artifacts with each stage's core outputs and minimum pass evidence; mark `passed`, `partially_passed`, `failed`, or `not_assessed`.",
        "4. Stop at the earliest critical non-passed stage and load that authoritative stage module.",
        "5. If the boundary is ambiguous, load only that stage and the immediately adjacent candidate, then decide.",
        "6. Preserve usable downstream materials as provisional assets and explain the missing evidence in Chinese.",
        "",
        "The matrix is a diagnosis index, not a replacement for the selected stage module. A matrix match identifies the candidate stage; formal acceptance uses the full module.",
        "",
        "<!-- BEGIN GENERATED 35-STAGE MATRIX -->",
        "## Compact 35-stage diagnosis matrix",
        "",
    ]
    active_family = None
    for stage, title, deliverables, acceptance in stages:
        family = stage[0]
        if family != active_family:
            lines.extend([f"### {FAMILY_NAMES[family]}", ""])
            active_family = family
        lines.extend([
            f"#### {stage} — {title}",
            "",
            "Core outputs: " + "; ".join(deliverables),
            "",
            "Minimum pass evidence: " + "; ".join(acceptance),
            "",
        ])
    lines.extend([
        "<!-- END GENERATED 35-STAGE MATRIX -->",
        "",
        "## Confidence",
        "",
        "- High: direct artifacts support every earlier pass decision.",
        "- Medium: sufficient descriptions exist but some source files are missing.",
        "- Low: the user description is sparse, contradictory, or cannot support earlier-stage acceptance.",
        "",
        "Low confidence does not authorize skipping. Ask no more than three critical questions, retain the earliest plausible stage, and label downstream help provisional.",
        "",
        "## Skip handling",
        "",
        "If the user requests downstream writing before upstream validation, provide provisional assistance, label upstream dependencies, and keep stage status unchanged.",
        "",
    ])
    TARGET.write_text("\n".join(lines), encoding="utf-8")
    print("rebuilt compact diagnosis matrix: 35 stages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

