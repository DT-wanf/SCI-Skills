#!/usr/bin/env python3
"""Self-test journal-ledger empty, mutable-variant, and verified cases."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(path: Path) -> int:
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_journal_ledger.py"), str(path)], capture_output=True, text=True).returncode


def run_gate(path: Path) -> int:
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_recommendation_gate.py"), str(path)], capture_output=True, text=True).returncode


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        empty = directory / "empty.csv"
        empty.write_text("journal,fact,value,source,checked_date\n", encoding="utf-8")
        unverified = directory / "unverified.csv"
        unverified.write_text("journal,fact,value,source,checked_date\nTest,Impact Factor 2025,3.2,,\n", encoding="utf-8")
        verified = directory / "verified.csv"
        verified.write_text("journal,fact,value,source,checked_date\nTest,Impact Factor 2025,3.2,official journal page,2026-08-11\n", encoding="utf-8")
        outcomes = (run(empty), run(unverified), run(verified))
        unsafe = directory / "unsafe-recommendation.yaml"
        unsafe.write_text("\n".join([
            "materials_complete: false",
            "missing_essentials: [methods, results]",
            "task_status: COMPLETE",
            "stage_acceptance_recommendation: PASS_CANDIDATE",
            "quality_assessment_status: NOT_ASSESSED",
            "candidates: [Journal A]",
            "",
        ]), encoding="utf-8")
        safe = directory / "safe-block.yaml"
        safe.write_text("\n".join([
            "materials_complete: false",
            "missing_essentials: [methods, results]",
            "task_status: BLOCKED",
            "stage_acceptance_recommendation: NOT_ASSESSED",
            "quality_assessment_status: NOT_ASSESSED",
            "candidates: []",
            "",
        ]), encoding="utf-8")
        gate_outcomes = (run_gate(unsafe), run_gate(safe))
    if outcomes[0] == 0 or outcomes[1] == 0 or outcomes[2] != 0 or gate_outcomes[0] == 0 or gate_outcomes[1] != 0:
        print(f"JOURNAL LEDGER SELF-TEST FAILED: {outcomes}")
        print(f"JOURNAL RECOMMENDATION GATE SELF-TEST FAILED: {gate_outcomes}")
        return 1
    print("JOURNAL LEDGER AND MATERIAL-GATE SELF-TEST PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
