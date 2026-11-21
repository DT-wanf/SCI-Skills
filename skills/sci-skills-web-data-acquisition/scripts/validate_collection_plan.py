#!/usr/bin/env python3
"""Validate a zero-API web-data collection plan before a pilot."""

from __future__ import annotations

import re
import sys
from pathlib import Path

FORBIDDEN = [r"api[_ -]?key", r"bearer\s+", r"bypass\s+(?:captcha|paywall|login)"]


def parse_yaml_subset(text: str) -> tuple[dict[str, str], dict[str, list[str]]]:
    """Parse the mapping/list subset used by the bundled plan without PyYAML."""
    scalars: dict[str, str] = {}
    lists: dict[str, list[str]] = {}
    stack: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if stripped.startswith("- "):
            if stack:
                path = ".".join(key for _, key in stack)
                lists.setdefault(path, []).append(stripped[2:].strip().strip("\"'"))
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", stripped)
        if not match:
            continue
        key, value = match.groups()
        path = ".".join([*(item[1] for item in stack), key])
        if value:
            scalars[path] = value.strip().strip("\"'")
        else:
            stack.append((indent, key))
    return scalars, lists


def meaningful(value: str | None) -> bool:
    return value not in (None, "", "null", "~")


def boolean(value: str | None) -> bool | None:
    if value is None:
        return None
    if value.casefold() == "true":
        return True
    if value.casefold() == "false":
        return False
    return None


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_collection_plan.py PLAN.yaml")
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    scalars, lists = parse_yaml_subset(text)
    missing = []
    status = scalars.get("activation_gate.data_sufficiency")
    if status not in {"INSUFFICIENT", "ABSENT"}:
        missing.append("activated insufficiency")
    required_scalars = {
        "critical gap": "activation_gate.critical_gap",
        "unit of analysis": "research_link.unit_of_analysis",
        "selected source": "selected_source.name",
        "source access route": "selected_source.access_route",
        "research-use rights": "selected_source.research_use_rights",
        "sampling rule": "scope.sampling_rule",
        "pilot target": "pilot.target_size",
    }
    missing.extend(label for label, path in required_scalars.items() if not meaningful(scalars.get(path)))
    for label, path in (("content fields", "output.content_fields"), ("provenance fields", "output.provenance_fields")):
        if not lists.get(path):
            missing.append(label)

    gate_errors = []
    if boolean(scalars.get("activation_gate.cleaning_or_derivation_can_repair")) is not False:
        gate_errors.append("cleaning_or_derivation_can_repair must be false")
    if boolean(scalars.get("activation_gate.web_evidence_methodologically_appropriate")) is not True:
        gate_errors.append("web_evidence_methodologically_appropriate must be true")
    if boolean(scalars.get("activation_gate.acquisition_activated")) is not True:
        gate_errors.append("acquisition_activated must be true")
    if scalars.get("crawl_gate.crawl_necessity") == "JUSTIFIED":
        for key in ("official_download_checked", "open_repository_checked", "paid_licensed_source_checked", "authorized_export_checked"):
            if boolean(scalars.get(f"crawl_gate.{key}")) is not True:
                gate_errors.append(f"crawl escalation requires {key}: true")
        if not meaningful(scalars.get("crawl_gate.permission_status")):
            gate_errors.append("crawl escalation requires permission_status")
    forbidden = [pattern for pattern in FORBIDDEN if re.search(pattern, text, flags=re.I)]
    if missing or gate_errors or forbidden:
        print({"missing": missing, "gate_errors": gate_errors, "forbidden": forbidden})
        return 1
    print("PASS: collection plan is pilot-ready and zero-API")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
