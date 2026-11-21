from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT.parent
errors: list[str] = []

skill_names = {"sci-skills"}
manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
skill_names.update(re.findall(r":\s*(sci-skills-[a-z0-9-]+)\s*$", manifest, re.M))

resolved: dict[str, Path] = {}
for path in SKILLS_ROOT.glob("*/SKILL.md"):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", text, re.M)
    if match and match.group(1) in skill_names:
        resolved[match.group(1)] = path.parent

for name in sorted(skill_names):
    directory = resolved.get(name)
    if directory is None:
        errors.append(f"Missing skill for zero-API audit: {name}")
        continue
    agent = directory / "agents" / "openai.yaml"
    if agent.exists() and re.search(r"^dependencies:\s*$", agent.read_text(encoding="utf-8"), re.M):
        errors.append(f"External dependency declared: {name}/agents/openai.yaml")
    for script in directory.rglob("*.py"):
        if script.resolve() == Path(__file__).resolve():
            continue
        text = script.read_text(encoding="utf-8")
        if re.search(r"\b(requests\.(get|post|put|delete)|urllib\.request|httpx\.(get|post)|aiohttp\.|openai\.|anthropic\.)", text):
            errors.append(f"Direct external request code: {name}/{script.relative_to(directory)}")
        if re.search(r"OPENAI_API_KEY|ANTHROPIC_API_KEY|SEMANTIC_SCHOLAR_API_KEY|api_key\s*=", text, re.I):
            errors.append(f"External credential code: {name}/{script.relative_to(directory)}")

for literal in ["third_party_api_calls: forbidden", "api_keys_or_tokens: forbidden", "remote_model_services: forbidden"]:
    if literal not in manifest:
        errors.append(f"Manifest missing zero-API declaration: {literal}")

if errors:
    print("ZERO-API VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("ZERO-API VALIDATION PASSED")
print(f"Skills checked: {len(skill_names)}")
print("External dependencies: 0")
print("Credential requirements: 0")
