#!/usr/bin/env python3
"""Enforce the quality-and-material gate before naming journals."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{key}:\s*([^#\n]*)", text)
    return match.group(1).strip().strip("\"'") if match else None


def list_empty(text: str, key: str) -> bool:
    match = re.search(rf"(?m)^{key}:\s*([^#\n]*)", text)
    if not match:
        return True
    inline = match.group(1).strip()
    if inline == "[]":
        return True
    if inline:
        return False
    for line in text[match.end():].splitlines():
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")):
            break
        if re.match(r"^\s*-\s+", line):
            return False
    return True


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_recommendation_gate.py RESULT.yaml")
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    complete = scalar(text, "materials_complete") == "true"
    errors = []
    if not complete:
        if scalar(text, "task_status") != "BLOCKED":
            errors.append("incomplete materials require task_status BLOCKED")
        if scalar(text, "stage_acceptance_recommendation") != "NOT_ASSESSED":
            errors.append("incomplete materials require NOT_ASSESSED")
        if not list_empty(text, "candidates"):
            errors.append("incomplete materials require an empty candidate list")
        if list_empty(text, "missing_essentials"):
            errors.append("incomplete materials require explicit missing_essentials")
    elif scalar(text, "quality_assessment_status") not in {"ASSESSED", "PROVISIONAL"}:
        errors.append("complete materials require a quality assessment status")
    if errors:
        print("JOURNAL RECOMMENDATION GATE FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("JOURNAL RECOMMENDATION GATE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
