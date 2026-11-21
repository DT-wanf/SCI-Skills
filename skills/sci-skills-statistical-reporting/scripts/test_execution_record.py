#!/usr/bin/env python3
"""Self-test the independent statistical execution-record validator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        for name in ("input.csv", "analysis.py", "run.log", "result.csv"):
            (directory / name).write_text("test\n", encoding="utf-8")
        valid = directory / "execution.yaml"
        valid.write_text(
            "\n".join([
                "execution_status: EXECUTED_LOCAL",
                "sample_unit: participant",
                'input_files: ["input.csv"]',
                'analysis_source: ["analysis.py"]',
                "software_version: Python test runtime",
                'execution_log: ["run.log"]',
                'output_files: ["result.csv"]',
                "",
            ]), encoding="utf-8"
        )
        validator = ROOT / "scripts" / "validate_execution_record.py"
        passed = subprocess.run([sys.executable, str(validator), str(valid)], capture_output=True, text=True)
        (directory / "result.csv").unlink()
        failed = subprocess.run([sys.executable, str(validator), str(valid)], capture_output=True, text=True)
    if passed.returncode != 0 or failed.returncode == 0:
        print("STATISTICAL EXECUTION SELF-TEST FAILED")
        print(passed.stdout, failed.stdout)
        return 1
    print("STATISTICAL EXECUTION SELF-TEST PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

