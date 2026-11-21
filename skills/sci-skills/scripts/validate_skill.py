from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT.parent
errors: list[str] = []


def read(path: Path) -> str:
    if not path.exists():
        errors.append(f"Missing: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


skill = read(ROOT / "SKILL.md")
manifest = read(ROOT / "manifest.yaml")

if not skill.startswith("---\nname: sci-skills\n"):
    errors.append("SKILL.md must use name: sci-skills")
for literal in [
    "# SCI-Skills 3.0",
    "Preserve five paper families and exactly 35 stage modules",
    "## Zero-API boundary",
    "## Expert routing",
    "## Manual operation companion",
    "## AIGC and journal boundaries",
]:
    if literal not in skill:
        errors.append(f"SKILL.md missing: {literal}")
for literal in ["name: sci-skills", "display_name: SCI-Skills", "version: 3.0.2", 'contract_version: "1.0"', "core_stage_count: 35"]:
    if literal not in manifest:
        errors.append(f"manifest.yaml missing: {literal}")

modules = sorted((ROOT / "workflows").glob("*/*.md"))
if len(modules) != 35:
    errors.append(f"Expected 35 stage modules, found {len(modules)}")
expected_ids = {f"{family}{index}" for family in "EIMTR" for index in range(1, 8)}
found_ids: set[str] = set()
for path in modules:
    text = read(path)
    match = re.search(r"^stage_id:\s*([EIMTR][1-7])\s*$", text, re.M)
    if not match:
        errors.append(f"Missing valid stage_id: {path.relative_to(ROOT)}")
        continue
    stage_id = match.group(1)
    found_ids.add(stage_id)
    for key in ["action_type_default:", "expert_candidates:", "external_playbook:"]:
        if key not in text:
            errors.append(f"{stage_id} missing {key}")
if found_ids != expected_ids:
    errors.append(f"Stage ID mismatch: missing={sorted(expected_ids - found_ids)} extra={sorted(found_ids - expected_ids)}")

expert_names = [
    "sci-skills-literature-search",
    "sci-skills-paper-deep-reading",
    "sci-skills-manuscript-writing",
    "sci-skills-academic-polishing",
    "sci-skills-scientific-figures",
    "sci-skills-statistical-reporting",
    "sci-skills-paper-presentation",
    "sci-skills-presubmission-review",
    "sci-skills-reviewer-response",
    "sci-skills-data-availability",
    "sci-skills-web-data-acquisition",
    "sci-skills-aigc-authorial-rewriting",
    "sci-skills-journal-recommendation",
]
discovered: dict[str, Path] = {}
for path in SKILLS_ROOT.glob("*/SKILL.md"):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", text, re.M)
    if match:
        discovered[match.group(1)] = path
for name in expert_names:
    if name not in discovered:
        errors.append(f"Missing independent expert skill: {name}")
    if f": {name}" not in manifest:
        errors.append(f"Manifest missing expert route: {name}")

if (ROOT / "references" / "capabilities").exists() and list((ROOT / "references" / "capabilities").glob("*.md")):
    errors.append("Legacy internal capability modules still exist")

for relative in [
    "references/core/expert-skill-routing.md",
    "references/core/zero-api-policy.md",
    "references/core/manual-operation-companion.md",
    "templates/operation-companion-prompt.md",
    "templates/operation-return-card.md",
    "schemas/project-state.yaml",
]:
    read(ROOT / relative)

for path in [ROOT / "SKILL.md", ROOT / "manifest.yaml", ROOT / "NOTICE", *modules, *list((ROOT / "templates").glob("*.md"))]:
    text = path.read_text(encoding="utf-8")
    if "SCI-skill" in text or "name: sci-skill\n" in text or "SCI保姆" in text:
        errors.append(f"Legacy product name found: {path.relative_to(ROOT)}")

for path in (ROOT / "scripts").glob("*.py"):
    text = path.read_text(encoding="utf-8")
    if re.search(r"\b(requests\.(get|post|put|delete)|urllib\.request|httpx\.(get|post)|aiohttp\.)", text):
        errors.append(f"Direct network request found: {path.relative_to(ROOT)}")

if errors:
    print("VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("VALIDATION PASSED")
print(f"Stage modules: {len(modules)}")
print(f"Independent experts: {len(expert_names)}")
print("External API integrations: 0")
