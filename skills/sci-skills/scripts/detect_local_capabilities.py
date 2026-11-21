#!/usr/bin/env python3
"""Read-only capability detection for optional local SCI-Skills adapters."""

from __future__ import annotations

import importlib.util
import json
import shutil


def available(command: str) -> bool:
    return shutil.which(command) is not None


def main() -> int:
    result = {
        "contract_version": "1.0",
        "external_api_used": False,
        "adapters": {
            "local-python": {
                "status": "AVAILABLE" if available("python3") else "UNAVAILABLE",
                "evidence": {"executable": shutil.which("python3")},
            },
            "local-r": {
                "status": "AVAILABLE" if available("Rscript") else "UNAVAILABLE",
                "evidence": {"executable": shutil.which("Rscript")},
            },
            "local-document-rendering": {
                "status": "AVAILABLE" if any(available(x) for x in ("libreoffice", "soffice", "pdftoppm")) else "UNAVAILABLE",
                "evidence": {x: shutil.which(x) for x in ("libreoffice", "soffice", "pdftoppm")},
            },
            "local-file-import": {
                "status": "AVAILABLE",
                "evidence": {
                    "python_zipfile": importlib.util.find_spec("zipfile") is not None,
                    "python_csv": importlib.util.find_spec("csv") is not None,
                },
            },
            "manual-database-export": {
                "status": "USER_ACTION_REQUIRED",
                "evidence": {"credentials_requested": False},
            },
            "local-model-already-available": {
                "status": "NOT_CHECKED",
                "evidence": {"default_enabled": False, "user_opt_in_required": True},
            },
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

