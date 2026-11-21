#!/usr/bin/env python3
"""Validate the human-facing release layout without changing Skill behavior."""

from __future__ import annotations

import re
import sys
from pathlib import Path


RELEASE_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = RELEASE_ROOT / "skills"
ORCHESTRATOR = "sci-skills"
EXPERTS = {
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
}
EXPECTED = EXPERTS | {ORCHESTRATOR}
RESOURCE_PATTERN = re.compile(
    r"`((?:references|scripts|templates|schemas|assets)/[A-Za-z0-9._/-]+|manifest\.yaml|component\.yaml)`"
)


def frontmatter(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1).strip().strip("\"'") if match else None


def main() -> int:
    errors: list[str] = []
    required_release_files = [
        "README.md",
        "VALIDATION.md",
        "LICENSE",
        "NOTICE",
        "VERSION",
        "suite.yaml",
        "docs/architecture.md",
        "docs/installation.md",
        "docs/expert-catalog.md",
        "docs/paper-routes.md",
        "docs/academic-safety.md",
        "assets/SCI-Skills-promo-3.0.2.png",
    ]
    for relative in required_release_files:
        if not (RELEASE_ROOT / relative).is_file():
            errors.append(f"missing release file: {relative}")

    readme_path = RELEASE_ROOT / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        local_links = re.findall(r"!?\[[^\]]*\]\((\./[^)#]+)(?:#[^)]+)?\)", readme)
        for link in local_links:
            if not (RELEASE_ROOT / link.removeprefix("./")).exists():
                errors.append(f"README contains broken local link: {link}")

    discovered = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
    if discovered != EXPECTED:
        errors.append(
            f"skill set mismatch missing={sorted(EXPECTED - discovered)} "
            f"extra={sorted(discovered - EXPECTED)}"
        )

    descriptions: dict[str, str] = {}
    for name in sorted(discovered & EXPECTED):
        directory = SKILLS_ROOT / name
        skill_file = directory / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{name}: SKILL.md is not at the skill root")
            continue
        text = skill_file.read_text(encoding="utf-8")
        declared_name = frontmatter(text, "name")
        description = frontmatter(text, "description")
        if declared_name != name:
            errors.append(f"{name}: frontmatter name is {declared_name!r}")
        if not description or len(description) < 80:
            errors.append(f"{name}: trigger description is missing or too short")
        else:
            descriptions[name] = description
        agent_file = directory / "agents" / "openai.yaml"
        if not agent_file.is_file():
            errors.append(f"{name}: missing agents/openai.yaml")
        else:
            agent_text = agent_file.read_text(encoding="utf-8")
            display_name = frontmatter(agent_text, "display_name")
            if not display_name or not display_name.startswith("SCI-Skills"):
                errors.append(f"{name}: display_name is not unified under SCI-Skills")
            if f"${name}" not in agent_text:
                errors.append(f"{name}: default_prompt does not reference its public skill name")
            for icon_path in re.findall(r"(?m)^\s*icon_(?:small|large):\s*(\S+)\s*$", agent_text):
                if not (directory / icon_path).is_file():
                    errors.append(f"{name}: missing interface icon {icon_path}")
        if (directory / "README.md").exists():
            errors.append(f"{name}: user README must stay at release root, not inside a Skill")

        for relative in sorted(set(RESOURCE_PATTERN.findall(text))):
            if not (directory / relative).exists():
                errors.append(f"{name}: broken SKILL.md resource path {relative}")

    orchestrator_description = descriptions.get(ORCHESTRATOR, "")
    for trigger in ("宝宝巴士", "山海", "35 stages", "13 independent"):
        if trigger not in orchestrator_description:
            errors.append(f"orchestrator trigger description missing {trigger!r}")
    orchestrator_agent = (SKILLS_ROOT / ORCHESTRATOR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "allow_implicit_invocation: true" not in orchestrator_agent:
        errors.append("orchestrator implicit invocation is not enabled")

    manifest_path = SKILLS_ROOT / ORCHESTRATOR / "manifest.yaml"
    manifest = manifest_path.read_text(encoding="utf-8") if manifest_path.exists() else ""
    for expert in EXPERTS:
        if f": {expert}" not in manifest:
            errors.append(f"manifest missing expert route: {expert}")

    stage_modules = list((SKILLS_ROOT / ORCHESTRATOR / "workflows").glob("*/*.md"))
    if len(stage_modules) != 35:
        errors.append(f"expected 35 stage modules, found {len(stage_modules)}")

    suite = (RELEASE_ROOT / "suite.yaml").read_text(encoding="utf-8")
    for name in EXPECTED:
        if name not in suite:
            errors.append(f"suite.yaml missing component: {name}")

    internal_id_pattern = re.compile(r"skill-[0-9a-f]{20,}")
    for path in SKILLS_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if internal_id_pattern.search(text):
            errors.append(f"internal installation directory leaked into release: {path.relative_to(RELEASE_ROOT)}")

    if errors:
        print("RELEASE LAYOUT VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("RELEASE LAYOUT VALIDATION PASSED")
    print("Skill roots discovered: 14/14")
    print("Folder/frontmatter names matched: 14/14")
    print("Trigger descriptions present: 14/14")
    print("Display/default-prompt metadata matched: 14/14")
    print("Orchestrator expert routes present: 13/13")
    print("Stage modules present: 35/35")
    print("Broken SKILL.md resource paths: 0")
    print("Internal installation-directory references: 0")
    print("Broken README local links: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
