#!/usr/bin/env python3
"""Run the deterministic SCI-Skills 3.0.2 release gate."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SKILLS_ROOT = ROOT.parent
CHECKS = [
    (SCRIPTS / "validate_skill.py", []),
    (SCRIPTS / "validate_routes.py", []),
    (SCRIPTS / "validate_stage_integrity.py", []),
    (SCRIPTS / "validate_component_compatibility.py", []),
    (SCRIPTS / "validate_zero_api.py", []),
    (SCRIPTS / "validate_prompt_cards.py", []),
    (SCRIPTS / "audit_output_contract.py", [str(SCRIPTS / "fixtures" / "valid-expert-response.md")]),
    (SCRIPTS / "test_scenarios.py", []),
    (SCRIPTS / "test_runtime_contracts.py", []),
    (SCRIPTS / "test_data_acquisition_gates.py", []),
    (SCRIPTS / "test_figure_gates.py", []),
    (SCRIPTS / "test_figure_tools.py", []),
    (SKILLS_ROOT / "sci-skills-scientific-figures" / "scripts" / "test_figure_gates.py", []),
    (SKILLS_ROOT / "sci-skills-scientific-figures" / "scripts" / "test_figure_tools.py", []),
    (SKILLS_ROOT / "sci-skills-web-data-acquisition" / "scripts" / "test_data_acquisition_gates.py", []),
    (SKILLS_ROOT / "sci-skills-statistical-reporting" / "scripts" / "test_execution_record.py", []),
    (SKILLS_ROOT / "sci-skills-journal-recommendation" / "scripts" / "test_journal_ledger.py", []),
]


def main() -> int:
    failures: list[str] = []
    for script, arguments in CHECKS:
        process = subprocess.run([sys.executable, str(script), *arguments], cwd=script.parents[1], text=True, capture_output=True)
        print(f"\n== {script.parent.parent.name}/{script.name} ==")
        print(process.stdout.rstrip())
        if process.stderr:
            print(process.stderr.rstrip())
        if process.returncode:
            failures.append(f"{script.parent.parent.name}/{script.name}")
    if failures:
        print(f"\nSCI-Skills 3.0.2 RELEASE GATE FAILED: {', '.join(failures)}")
        return 1
    print("\nSCI-Skills 3.0.2 RELEASE GATE PASSED")
    print("5 paper families; 35 stages; 1 orchestrator; 13 experts; 0 external API dependencies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
