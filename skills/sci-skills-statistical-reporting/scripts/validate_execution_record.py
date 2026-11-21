#!/usr/bin/env python3
"""Reject statistical execution claims without local provenance fields."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_SCALARS = ["software_version", "sample_unit"]
REQUIRED_PATH_LISTS = ["input_files", "analysis_source", "execution_log", "output_files"]


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{key}:\s*([^#\n]+)", text)
    if not match:
        return None
    value = match.group(1).strip().strip("\"'")
    return None if value in ("", "null", "~") else value


def list_values(text: str, key: str) -> list[str]:
    match = re.search(rf"(?m)^{key}:\s*([^#\n]*)", text)
    if not match:
        return []
    inline = match.group(1).strip()
    if inline.startswith("[") and inline.endswith("]"):
        return [item.strip().strip("\"'") for item in inline[1:-1].split(",") if item.strip()]
    values = []
    for line in text[match.end():].splitlines():
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")):
            break
        item = re.match(r"^\s*-\s+(.+)$", line)
        if item:
            values.append(item.group(1).strip().strip("\"'"))
    return values


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_execution_record.py RECORD.yaml")
        return 2
    record = Path(sys.argv[1]).resolve()
    text = record.read_text(encoding="utf-8")
    missing = [key for key in REQUIRED_SCALARS if not scalar(text, key)]
    path_groups = {key: list_values(text, key) for key in REQUIRED_PATH_LISTS}
    missing.extend(key for key, values in path_groups.items() if not values)
    nonexistent = []
    for key, values in path_groups.items():
        for value in values:
            candidate = Path(value)
            candidate = candidate if candidate.is_absolute() else record.parent / candidate
            if not candidate.exists():
                nonexistent.append(f"{key}:{value}")
    if scalar(text, "execution_status") != "EXECUTED_LOCAL":
        missing.append("execution_status=EXECUTED_LOCAL")
    if missing or nonexistent:
        print("FAIL: missing execution evidence: " + ", ".join(missing))
        if nonexistent:
            print("FAIL: referenced files do not exist: " + ", ".join(nonexistent))
        return 1
    print("PASS: statistical execution record has required provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
