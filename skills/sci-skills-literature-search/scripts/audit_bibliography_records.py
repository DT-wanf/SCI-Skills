#!/usr/bin/env python3
"""Audit local bibliography records for identity and missing fields; no network calls."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


def normalize(value: str) -> str:
    return re.sub(r"\W+", " ", value.casefold()).strip()


def records(path: Path) -> list[dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, list) else payload.get("records", [])
    text = path.read_text(encoding="utf-8", errors="replace")
    chunks = re.split(r"(?m)^\s*(?:ER\s*-|@\w+\s*\{)", text)
    return [{"raw": chunk} for chunk in chunks if chunk.strip()]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: audit_bibliography_records.py FILE.csv|json|ris|bib")
        return 2
    rows = records(Path(sys.argv[1]))
    seen: dict[str, int] = {}
    duplicates: list[tuple[int, int]] = []
    incomplete = 0
    for index, row in enumerate(rows, 1):
        lower = {str(k).casefold(): str(v or "") for k, v in row.items()}
        title = lower.get("title") or lower.get("ti") or lower.get("t1") or lower.get("raw", "")[:240]
        doi = lower.get("doi") or lower.get("do") or ""
        key = normalize(doi) if doi else normalize(title)
        if not key:
            incomplete += 1
            continue
        if key in seen:
            duplicates.append((seen[key], index))
        else:
            seen[key] = index
        if not title:
            incomplete += 1
    print(json.dumps({"records": len(rows), "possible_duplicates": duplicates, "incomplete_identity": incomplete, "network_used": False}, ensure_ascii=False, indent=2))
    return 1 if incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())

