#!/usr/bin/env python3
"""Twenty-seven deterministic SCI-Skills 3.0.2 runtime contract scenarios."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT.parent
errors: list[str] = []
passed: list[str] = []


def check(name: str, condition: bool, detail: str) -> None:
    if condition:
        passed.append(name)
    else:
        errors.append(f"{name}: {detail}")


experts: dict[str, Path] = {}
for path in SKILLS_ROOT.glob("*/SKILL.md"):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*(sci-skills-[a-z0-9-]+)\s*$", text)
    if match:
        experts[match.group(1)] = path.parent

expected = [
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

# 13 direct-expert scenarios
for name in expected:
    directory = experts.get(name)
    condition = bool(directory) and all(
        (directory / relative).exists()
        for relative in (
            "references/playbook.md",
            "references/_core/expert-contract.md",
            "schemas/expert-task.yaml",
            "schemas/expert-result.yaml",
            "templates/operation-companion-prompt.md",
            "component.yaml",
        )
    )
    skill_text = (directory / "SKILL.md").read_text(encoding="utf-8") if directory else ""
    condition = condition and "Do not merely say “standard contract”; emit the exact contract." in skill_text
    if directory:
        invalid = subprocess.run(
            [sys.executable, str(directory / "scripts" / "validate_expert_contract.py"), str(directory / "schemas" / "expert-result.yaml")],
            capture_output=True,
            text=True,
        )
        with tempfile.TemporaryDirectory() as temporary:
            valid_path = Path(temporary) / "result.yaml"
            valid_path.write_text(
                "\n".join([
                    'contract_version: "1.0"',
                    f"expert_skill: {name}",
                    "project_id: null",
                    "paper_family: null",
                    "stage_id: null",
                    "task_id: null",
                    "task_status: COMPLETE",
                    'inputs_reviewed: ["synthetic bounded input"]',
                    'outputs: ["validated specialist artifact"]',
                    'evidence_status: ["AI_INFERENCE"]',
                    "assumptions: []",
                    "author_input_needed: []",
                    "manual_actions: []",
                    'quality_checks: ["contract self-test"]',
                    "conflicts: []",
                    "conflict_resolution_status: NOT_REQUIRED",
                    "merge_permission: orchestrator_only",
                    'recommended_next_action: "Return for orchestrator review."',
                    "stage_acceptance_recommendation: PASS_CANDIDATE",
                    "",
                ]),
                encoding="utf-8",
            )
            valid = subprocess.run(
                [sys.executable, str(directory / "scripts" / "validate_expert_contract.py"), str(valid_path)],
                capture_output=True,
                text=True,
            )
        condition = condition and invalid.returncode != 0 and valid.returncode == 0
    check(f"direct:{name}", condition, "expert is not self-contained or exact-contract capable")

with tempfile.TemporaryDirectory() as temporary:
    temporary_path = Path(temporary)
    task_path = temporary_path / "task.yaml"
    result_path = temporary_path / "result.yaml"
    task_path.write_text(
        "\n".join([
            'contract_version: "1.0"',
            "project_id: PROJECT-ROUNDTRIP",
            "paper_family: empirical",
            "stage_id: E2",
            "task_id: TASK-ROUNDTRIP",
            "expert_skill: sci-skills-literature-search",
            "",
        ]), encoding="utf-8"
    )
    base_result = [
        'contract_version: "1.0"',
        "expert_skill: sci-skills-literature-search",
        "project_id: PROJECT-ROUNDTRIP",
        "paper_family: empirical",
        "stage_id: E2",
        "task_id: TASK-ROUNDTRIP",
        "task_status: COMPLETE",
        'inputs_reviewed: ["topic brief"]',
        'outputs: ["verified search strategy"]',
        'evidence_status: ["VERIFIED_USER_MATERIAL"]',
        "assumptions: []",
        "author_input_needed: []",
        "manual_actions: []",
        'quality_checks: ["identity and evidence checked"]',
        "conflicts: []",
        "conflict_resolution_status: NOT_REQUIRED",
        "merge_permission: orchestrator_only",
        'recommended_next_action: "Return to E2 stage review."',
        "stage_acceptance_recommendation: PASS_CANDIDATE",
        "",
    ]
    result_path.write_text("\n".join(base_result), encoding="utf-8")
    central_validator = ROOT / "scripts" / "validate_expert_contract.py"
    central_valid = subprocess.run([sys.executable, str(central_validator), str(result_path), str(task_path)], capture_output=True, text=True)
    conflict_text = "\n".join(base_result).replace("conflicts: []", 'conflicts: ["CONFLICT-1"]\nconflict_resolution_status: UNRESOLVED').replace("conflict_resolution_status: NOT_REQUIRED\n", "")
    result_path.write_text(conflict_text, encoding="utf-8")
    central_conflict = subprocess.run([sys.executable, str(central_validator), str(result_path), str(task_path)], capture_output=True, text=True)
    central_roundtrip_ok = central_valid.returncode == 0
    unresolved_conflict_rejected = central_conflict.returncode != 0

# 5 paper-family scenarios
for family in "EIMTR":
    modules = []
    for path in (ROOT / "workflows").glob("*/*.md"):
        text = path.read_text(encoding="utf-8")
        if re.search(rf"(?m)^stage_id:\s*{family}[1-7]\s*$", text):
            modules.append(path)
    check(f"family:{family}", len(modules) == 7, f"expected 7 stages, found {len(modules)}")

# 5 guard scenarios
figure = (experts["sci-skills-scientific-figures"] / "references" / "playbook.md").read_text(encoding="utf-8")
aigc = (experts["sci-skills-aigc-authorial-rewriting"] / "references" / "playbook.md").read_text(encoding="utf-8")
journal = (experts["sci-skills-journal-recommendation"] / "references" / "playbook.md").read_text(encoding="utf-8")
manual = (ROOT / "templates" / "operation-companion-prompt.md").read_text(encoding="utf-8")
zero = (ROOT / "references" / "expert-core" / "zero-api-policy.md").read_text(encoding="utf-8")
check("guard:no-data-result-figure", "real data" in figure and "Never use invented values" in figure, "result gate missing")
check("guard:no-detector-evasion", "detector evasion" in aigc and "Do not" in aigc, "AIGC boundary missing")
check("guard:journal-mutable-facts", "source page" in journal and "checked date" in journal, "journal verification ledger missing")
check("guard:no-external-api", "without third-party APIs" in zero and "keys" in zero, "zero-API policy missing")
check("guard:no-credentials", all(token in manual for token in ("密码", "验证码", "截图", "无安装替代方案")), "manual safety guidance incomplete")

# 4 orchestrator round-trip scenarios
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
task_schema = (ROOT / "schemas" / "expert-task.yaml").read_text(encoding="utf-8")
result_schema = (ROOT / "schemas" / "expert-result.yaml").read_text(encoding="utf-8")
state = (ROOT / "schemas" / "project-state.yaml").read_text(encoding="utf-8")
check("roundtrip:task-identity", all(x in task_schema and x in result_schema for x in ("project_id:", "stage_id:", "task_id:", "contract_version:")) and central_roundtrip_ok, "identity fields or central inbound validation failed")
check("roundtrip:stage-authority", "sole stage authority" in skill and "stage_acceptance_recommendation" in result_schema and unresolved_conflict_rejected, "stage authority or unresolved-conflict rejection missing")
operation_schema = (ROOT / "schemas" / "operation-return.yaml").read_text(encoding="utf-8")
operation_template = (ROOT / "templates" / "operation-return-card.md").read_text(encoding="utf-8")
check("roundtrip:manual-return", all(token in operation_schema and token in operation_template for token in ("operation_task_id:", "credentials_or_secrets_included:")) and "evidence_verified" in state, "manual return cannot be verified")
check("roundtrip:expert-unavailable", "If an expert is unavailable or incompatible" in skill and "REJECTED_FOR_REPAIR" in state and "conflict_resolution_status" in result_schema, "expert failure or conflict recovery missing")

if errors:
    print("RUNTIME CONTRACT TESTS FAILED")
    for error in errors:
        print(f"- {error}")
    print(f"Passed: {len(passed)}/27")
    sys.exit(1)
print("RUNTIME CONTRACT TESTS PASSED")
print("Scenarios: 27/27")
