#!/usr/bin/env python3
"""Check that the three SCI-Skills pre-submission lenses are represented."""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED = ["CONTRIBUTION", "METHODS", "COMMUNICATION", "BLOCKER", "readiness"]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_review_coverage.py REVIEW.md")
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    missing = [value for value in REQUIRED if value.casefold() not in text.casefold()]
    if missing:
        print("FAIL: missing review coverage: " + ", ".join(missing))
        return 1
    print("PASS: contribution, methods, communication, blockers, and readiness covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

