#!/usr/bin/env python3
"""Compare locked scientific tokens before and after language editing."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

PATTERNS = [
    r"\b\d+(?:\.\d+)?(?:e[+-]?\d+)?%?\b",
    r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+",
    r"\[[0-9,;\-– ]+\]",
    r"\([^)]*\b(?:p|P)\s*[<=>]\s*0?\.\d+[^)]*\)",
]


def tokens(path: Path) -> Counter[str]:
    text = path.read_text(encoding="utf-8")
    return Counter(match for pattern in PATTERNS for match in re.findall(pattern, text, flags=re.I))


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_locked_tokens.py ORIGINAL.txt REVISED.txt")
        return 2
    before, after = tokens(Path(sys.argv[1])), tokens(Path(sys.argv[2]))
    missing = list((before - after).elements())
    added = list((after - before).elements())
    print({"missing_locked_tokens": missing, "added_locked_tokens": added})
    return 1 if missing or added else 0


if __name__ == "__main__":
    raise SystemExit(main())

