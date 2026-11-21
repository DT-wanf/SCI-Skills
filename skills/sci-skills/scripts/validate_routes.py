from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
errors: list[str] = []
expert_keys = set(re.findall(r"^  ([a-z0-9-]+): sci-skills-[a-z0-9-]+$", manifest, re.M))
stage_paths = sorted((ROOT / "workflows").glob("*/*.md"))

for path in stage_paths:
    text = path.read_text(encoding="utf-8")
    id_match = re.search(r"^stage_id:\s*(\w+)\s*$", text, re.M)
    action_match = re.search(r"^action_type_default:\s*(\S+)\s*$", text, re.M)
    playbook_match = re.search(r"^external_playbook:\s*(\S+)\s*$", text, re.M)
    expert_match = re.search(r"^expert_candidates:\s*\n((?:  - .+\n)+)", text, re.M)
    if not all([id_match, action_match, playbook_match, expert_match]):
        errors.append(f"Incomplete route metadata: {path.relative_to(ROOT)}")
        continue
    stage_id = id_match.group(1)
    experts = [line.removeprefix("  - ").strip() for line in expert_match.group(1).splitlines()]
    if not re.search(rf"^  {stage_id}:\s*\[", manifest, re.M):
        errors.append(f"Manifest missing stage route: {stage_id}")
    for expert in experts:
        if expert not in expert_keys:
            errors.append(f"{stage_id} references unknown expert: {expert}")
    action = action_match.group(1)
    playbook = playbook_match.group(1)
    if action == "conditional_external" and playbook == "null":
        errors.append(f"{stage_id} is conditional but has no external playbook")
    if action == "prompt" and playbook != "null":
        errors.append(f"{stage_id} is prompt-first but declares playbook: {playbook}")
    if action not in {"prompt", "conditional_external"}:
        errors.append(f"{stage_id} has invalid action type: {action}")
    if playbook != "null" and not (ROOT / "references" / "action-playbooks" / f"{playbook}.md").exists():
        errors.append(f"{stage_id} references missing playbook: {playbook}")

if errors:
    print("ROUTE VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)
print("ROUTE VALIDATION PASSED")
print(f"Stages checked: {len(stage_paths)}")
