from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def stage_text(stage_id: str) -> str:
    for path in (ROOT / "workflows").glob("*/*.md"):
        text = path.read_text(encoding="utf-8")
        if re.search(rf"^stage_id:\s*{stage_id}\s*$", text, re.M):
            return text
    raise RuntimeError(stage_id)


checks = {
    "E1": ["literature-search"],
    "E5": ["statistical-reporting", "scientific-figures"],
    "E6": ["manuscript-writing", "academic-polishing", "aigc-authorial-rewriting"],
    "E7": ["presubmission-review", "reviewer-response", "journal-recommendation"],
    "I2": ["paper-deep-reading", "web-data-acquisition"],
    "M4": ["scientific-figures", "data-availability"],
    "R7": ["literature-search", "journal-recommendation"],
}
for stage_id, required in checks.items():
    text = stage_text(stage_id)
    for expert in required:
        if f"  - {expert}\n" not in text:
            errors.append(f"{stage_id} missing expert {expert}")

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
for literal in ["宝宝巴士", "山海", "35 stage modules", "13 independent expert skills", "operation-companion-prompt.md"]:
    if literal not in skill:
        errors.append(f"Orchestrator missing: {literal}")

manual = (ROOT / "templates" / "operation-companion-prompt.md").read_text(encoding="utf-8")
for literal in ["每次只告诉我一个步骤", "发送截图", "不要索取", "操作回传卡"]:
    if literal not in manual:
        errors.append(f"Manual companion missing: {literal}")

manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
for literal in ["third_party_api_calls: forbidden", "api_keys_or_tokens: forbidden", "stage_authority: sci-skills"]:
    if literal not in manifest:
        errors.append(f"Manifest missing: {literal}")

if errors:
    print("SCENARIO TESTS FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)
print("SCENARIO TESTS PASSED")
print(f"Scenarios checked: {len(checks)}")
