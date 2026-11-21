#!/usr/bin/env python3
"""Materialize the SCI-Skills 3.0.2 runtime core into every expert skill."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

ORCHESTRATOR = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ORCHESTRATOR.parent

EXPERTS = {
    "sci-skills-literature-search": ("sci-skills-literature-search", "literature-search", ["local-file-import", "manual-database-export"]),
    "sci-skills-paper-deep-reading": ("sci-skills-paper-deep-reading", "paper-deep-reading", ["local-file-import"]),
    "sci-skills-manuscript-writing": ("sci-skills-manuscript-writing", "manuscript-writing", ["local-file-import"]),
    "sci-skills-academic-polishing": ("sci-skills-academic-polishing", "academic-polishing", ["local-file-import"]),
    "sci-skills-scientific-figures": ("sci-skills-scientific-figures", "scientific-figures", ["local-python", "local-r", "local-file-import"]),
    "sci-skills-statistical-reporting": ("sci-skills-statistical-reporting", "statistical-reporting", ["local-python", "local-r", "local-file-import"]),
    "sci-skills-paper-presentation": ("sci-skills-paper-presentation", "paper-presentation", ["local-file-import", "local-document-rendering"]),
    "sci-skills-presubmission-review": ("sci-skills-presubmission-review", "presubmission-review", ["local-file-import", "local-document-rendering"]),
    "sci-skills-reviewer-response": ("sci-skills-reviewer-response", "reviewer-response", ["local-file-import", "local-document-rendering"]),
    "sci-skills-aigc-authorial-rewriting": ("sci-skills-aigc-authorial-rewriting", "aigc-authorial-rewriting", ["local-file-import"]),
    "sci-skills-data-availability": ("sci-skills-data-availability", "data-availability", ["local-file-import", "manual-database-export"]),
    "sci-skills-web-data-acquisition": ("sci-skills-web-data-acquisition", "web-data-acquisition", ["local-file-import", "manual-database-export"]),
    "sci-skills-journal-recommendation": ("sci-skills-journal-recommendation", "journal-recommendation", ["local-file-import", "manual-database-export"]),
}

CORE_FILES = [
    "expert-contract.md",
    "evidence-labels.md",
    "zero-api-policy.md",
    "manual-operation-companion.md",
    "stage-authority-boundary.md",
]
ADAPTER_FILE = "local-adapters.md"
SCHEMAS = ["expert-task.yaml", "expert-result.yaml", "expert-conflict.yaml", "operation-handoff.yaml", "operation-return.yaml", "adapter-status.yaml"]
TEMPLATES = ["operation-companion-prompt.md", "operation-return-card.md"]
MARKER = "<!-- SCI-SKILLS-RUNTIME-CORE -->"


def checksum(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def write_component(path: Path, name: str, capability: str, adapters: list[str], snapshot_hash: str) -> None:
    lines = [
        "product: SCI-Skills",
        "suite_version: 3.0.2",
        f"component_name: {name}",
        "component_type: expert",
        "component_version: 3.0.1",
        'contract_version: "1.0"',
        'core_snapshot_version: "1.0"',
        f"core_snapshot_sha256: {snapshot_hash}",
        'compatible_orchestrator: \">=3.0.1 <4.0.0\"',
        "capabilities:",
        f"  - {capability}",
        "manual_routes:",
        "  - website-or-database",
        "  - software-or-local-runtime",
        "  - repository-or-submission-system",
        "optional_adapters:",
        *[f"  - {adapter}" for adapter in adapters],
        "zero_external_api: true",
        "stage_authority: sci-skills",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def ensure_skill_section(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return
    section = f"""

{MARKER}
## Bundled runtime resources

This expert is self-contained. Before execution, read `references/_core/expert-contract.md`, `references/_core/evidence-labels.md`, `references/_core/zero-api-policy.md`, `references/_core/stage-authority-boundary.md`, and the specialist `references/playbook.md`. Read `references/_core/local-adapters.md` before local execution. Read `references/_core/manual-operation-companion.md` and use the bundled operation templates whenever user action is unavoidable.

Accept `schemas/expert-task.yaml` and return every field in `schemas/expert-result.yaml`. Use the specialist output checklist in `schemas/specialist-output.yaml`. Optional adapters are local-only, detected read-only, and never prerequisites. If unavailable, return the strongest intermediate artifact plus a manual or hybrid handoff.

Do not merely say “standard contract”; emit the exact contract. End with exactly one primary next action. Never advance, reopen, skip, or close a SCI-Skills stage.
"""
    path.write_text(text.rstrip() + section, encoding="utf-8")


def main() -> int:
    source_core = ORCHESTRATOR / "references" / "expert-core"
    source_paths = [source_core / name for name in CORE_FILES]
    source_paths.append(ORCHESTRATOR / "references" / "adapters" / ADAPTER_FILE)
    snapshot_hash = checksum(source_paths)
    for skill_name, (directory, playbook, adapters) in EXPERTS.items():
        root = SKILLS_ROOT / directory
        if not (root / "SKILL.md").exists():
            raise SystemExit(f"missing expert: {skill_name} at {root}")
        core_dir = root / "references" / "_core"
        schema_dir = root / "schemas"
        template_dir = root / "templates"
        script_dir = root / "scripts"
        for directory_path in (core_dir, schema_dir, template_dir, script_dir):
            directory_path.mkdir(parents=True, exist_ok=True)
        for name in CORE_FILES:
            shutil.copy2(source_core / name, core_dir / name)
        shutil.copy2(ORCHESTRATOR / "references" / "adapters" / ADAPTER_FILE, core_dir / ADAPTER_FILE)
        shutil.copy2(ORCHESTRATOR / "references" / "expert-playbooks" / f"{playbook}.md", root / "references" / "playbook.md")
        for name in SCHEMAS:
            shutil.copy2(ORCHESTRATOR / "schemas" / name, schema_dir / name)
        for name in TEMPLATES:
            shutil.copy2(ORCHESTRATOR / "templates" / name, template_dir / name)
        shutil.copy2(Path(__file__).with_name("validate_expert_contract.py"), script_dir / "validate_expert_contract.py")
        specialist = "\n".join([
            'contract_version: "1.0"',
            f"expert_skill: {skill_name}",
            f"artifact_type: {playbook}",
            "required_sections:",
            "  - scope_and_inputs",
            "  - specialist_findings",
            "  - evidence_and_execution_status",
            "  - deliverables",
            "  - limitations_and_risks",
            "  - quality_checks",
            "  - one_next_action",
            "",
        ])
        (schema_dir / "specialist-output.yaml").write_text(specialist, encoding="utf-8")
        (core_dir / "snapshot.yaml").write_text(
            f'core_snapshot_version: "1.0"\nsha256: {snapshot_hash}\nsource_product: SCI-Skills\n',
            encoding="utf-8",
        )
        write_component(root / "component.yaml", skill_name, playbook, adapters, snapshot_hash)
        ensure_skill_section(root / "SKILL.md")
    print(f"synced {len(EXPERTS)} experts; core sha256={snapshot_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
