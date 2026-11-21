#!/usr/bin/env python3
"""Require a source and check date for mutable journal facts."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

MUTABLE_PATTERNS = [
    r"impact\s*factor|\bif\b|影响因子",
    r"quartile|\bq[1-4]\b|分区",
    r"cas\s*zone|中科院",
    r"index(?:ed|ing)|收录",
    r"\boa\b|open\s*access|开放获取",
    r"\bapc\b|article\s*processing|版面费",
    r"review\s*time|审稿",
    r"deadline|截止",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_journal_ledger.py LEDGER.csv")
        return 2
    errors = []
    rows = []
    with Path(sys.argv[1]).open(encoding="utf-8-sig", newline="") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), 2):
            rows.append(row)
            fact = (row.get("fact") or "").casefold()
            mutable = any(re.search(pattern, fact, flags=re.I) for pattern in MUTABLE_PATTERNS)
            date = row.get("checked_date") or ""
            if mutable and (not row.get("source") or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date)):
                errors.append(row_number)
    if not rows:
        print("FAIL: verification ledger is empty")
        return 1
    if errors:
        print(f"FAIL: mutable journal facts lack source/date on rows {errors}")
        return 1
    print("PASS: mutable journal facts have verification evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
