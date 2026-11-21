from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def acquisition_active(status: str, web_appropriate: bool, repairable: bool) -> bool:
    return status in {"ABSENT", "INSUFFICIENT"} and web_appropriate and not repairable


def crawl_active(
    acquisition: bool,
    non_crawl_checked: bool,
    non_crawl_adequate: bool,
    permission_acceptable: bool,
    necessity: str,
) -> bool:
    return all(
        [
            acquisition,
            non_crawl_checked,
            not non_crawl_adequate,
            permission_acceptable,
            necessity == "JUSTIFIED",
        ]
    )


acquisition_cases = [
    ("UNKNOWN", True, False, False),
    ("SUFFICIENT", True, False, False),
    ("INSUFFICIENT", True, True, False),
    ("INSUFFICIENT", False, False, False),
    ("INSUFFICIENT", True, False, True),
    ("ABSENT", True, False, True),
]
for status, web_appropriate, repairable, expected in acquisition_cases:
    actual = acquisition_active(status, web_appropriate, repairable)
    if actual != expected:
        errors.append(f"Acquisition case failed: {status}, expected {expected}, got {actual}")

crawl_cases = [
    (True, True, False, True, "JUSTIFIED", True),
    (False, True, False, True, "JUSTIFIED", False),
    (True, False, False, True, "JUSTIFIED", False),
    (True, True, True, True, "JUSTIFIED", False),
    (True, True, False, False, "JUSTIFIED", False),
    (True, True, False, True, "BLOCKED", False),
]
for acquisition, checked, adequate, permitted, necessity, expected in crawl_cases:
    actual = crawl_active(acquisition, checked, adequate, permitted, necessity)
    if actual != expected:
        errors.append(f"Crawler case failed: expected {expected}, got {actual}")

required_literals = {
    "SKILL.md": [
        "Proceed only when reviewed evidence sets data status to `ABSENT` or `INSUFFICIENT`",
        "permitted public-page collection as a documented last resort",
        "Do not call or configure any external API",
    ],
    "references/data/data-sufficiency-gate.md": [
        "`UNKNOWN`",
        "`SUFFICIENT`",
        "`INSUFFICIENT`",
        "`ABSENT`",
        "Otherwise set `crawl_necessity` to `BLOCKED`",
    ],
    "references/data/web-data-collection.md": [
        "If data status is `UNKNOWN` or `SUFFICIENT`, stop this playbook",
        "Do not begin with crawler code",
        "Do not bypass login, paywalls, CAPTCHAs",
    ],
    "schemas/web-data-collection-plan.yaml": [
        "data_sufficiency: UNKNOWN | SUFFICIENT | INSUFFICIENT | ABSENT",
        "crawl_necessity: BLOCKED",
    ],
    "templates/data-acquisition-review-card.md": [
        "采集结果摘要",
        "宝宝巴士的审核建议",
        "我的选择：A / B / C",
    ],
}
for relative, literals in required_literals.items():
    text = (ROOT / relative).read_text(encoding="utf-8")
    for literal in literals:
        if literal not in text:
            errors.append(f"{relative} missing gate literal: {literal}")

validated = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "validate_collection_plan.py"), str(ROOT / "scripts" / "fixtures" / "valid-collection-plan.yaml")],
    capture_output=True,
    text=True,
)
if validated.returncode != 0:
    errors.append(f"Bundled collection-plan validator rejected bundled valid fixture: {validated.stdout or validated.stderr}")
try:
    blank = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_collection_plan.py"), str(ROOT / "schemas" / "web-data-collection-plan.yaml")],
        capture_output=True,
        text=True,
        timeout=2,
    )
    if blank.returncode == 0:
        errors.append("Blank collection-plan schema was accepted")
except subprocess.TimeoutExpired:
    errors.append("Blank collection-plan validation exceeded two seconds")

conflicting = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "validate_collection_plan.py"), str(ROOT / "scripts" / "fixtures" / "invalid-conflicting-plan.yaml")],
    capture_output=True,
    text=True,
    timeout=2,
)
if conflicting.returncode == 0:
    errors.append("Conflicting activation gate was accepted")

if errors:
    print("DATA ACQUISITION GATE TESTS FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("DATA ACQUISITION GATE TESTS PASSED")
print(f"Acquisition cases: {len(acquisition_cases)}")
print(f"Crawler cases: {len(crawl_cases)}")
