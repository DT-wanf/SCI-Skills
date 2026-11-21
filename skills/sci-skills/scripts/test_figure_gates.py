from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def result_render_allowed(
    real_inputs: bool,
    semantics: bool,
    transformations: bool,
    backend: str | None,
    source: bool,
    execution: bool,
    traceability: bool,
    source_risk: bool = True,
    image_generation: bool = False,
    invented_values: bool = False,
) -> bool:
    return all(
        [
            real_inputs,
            semantics,
            transformations,
            backend in {"python", "r"},
            source,
            execution,
            traceability,
            source_risk,
            not image_generation,
            not invented_values,
        ]
    )


def explanatory_render_allowed(
    location: bool,
    purpose: bool,
    boundary: bool,
    decomposition: bool,
    route: bool,
    approval: bool,
) -> bool:
    return all([location, purpose, boundary, decomposition, route, approval])


result_cases = [
    ("all result gates pass", (True, True, True, "python", True, True, True), True),
    ("text conclusion only", (False, True, True, "python", True, True, True), False),
    ("no semantics", (True, False, True, "python", True, True, True), False),
    ("no Python/R", (True, True, True, None, True, True, True), False),
    ("script not executed", (True, True, True, "r", True, False, True), False),
    ("no traceability", (True, True, True, "python", True, True, False), False),
]
for label, args, expected in result_cases:
    actual = result_render_allowed(*args)
    if actual != expected:
        errors.append(f"Result gate {label}: expected {expected}, got {actual}")

if result_render_allowed(True, True, True, "python", True, True, True, image_generation=True):
    errors.append("Result gate allowed image generation")
if result_render_allowed(True, True, True, "python", True, True, True, invented_values=True):
    errors.append("Result gate allowed invented values")
if result_render_allowed(True, True, True, "python", True, True, True, source_risk=False):
    errors.append("Result gate allowed a failed source-risk preflight")

explanatory_cases = [
    ("approved proposal", (True, True, True, True, True, True), True),
    ("no manuscript location", (False, True, True, True, True, True), False),
    ("no decomposition", (True, True, True, False, True, True), False),
    ("no user approval", (True, True, True, True, True, False), False),
]
for label, args, expected in explanatory_cases:
    actual = explanatory_render_allowed(*args)
    if actual != expected:
        errors.append(f"Explanatory gate {label}: expected {expected}, got {actual}")

figure_skill = None
for candidate in ROOT.parent.glob("*/SKILL.md"):
    text = candidate.read_text(encoding="utf-8")
    if re.search(r"^name:\s*sci-skills-scientific-figures\s*$", text, re.M):
        figure_skill = candidate
        break

required_literals = {
    "SKILL.md": [
        "## Scientific-figure gate",
        "real data or verified result files",
        "overview plus module-level decomposition",
    ],
    "manifest.yaml": [
        "figure_activation_conditions:",
        "actual_execution_evidence_available is true",
        "image_generation_model_used_for_result_pixels is true",
        "user_rendering_approval is true",
        "user_final_approval is true",
    ],
    "references/core/figure-readiness-gate.md": [
        "only a textual conclusion is available",
        "backend in [python, r]",
        "user_rendering_approval = true",
        "user_final_approval = true",
        "source_risk_gate_passed = true",
        "blocking failure, not a warning",
    ],
    "templates/figure-proposal-card.md": [
        "只做全览图",
        "我先上传一张对标图片",
        "暂时不制作",
    ],
    "templates/figure-review-card.md": [
        "真实输入",
        "实际运行证据",
        "允许插入论文",
        "不使用这张图",
    ],
}

if figure_skill is None:
    errors.append("Missing independent scientific-figures expert")
else:
    text = figure_skill.read_text(encoding="utf-8")
    for literal in [
        "## Result-figure hard gate",
        "successful local execution evidence",
        "## Explanatory and enhancement gate",
        "Do not force the whole method into one crowded panel",
        "## Reference adaptation",
    ]:
        if literal not in text:
            errors.append(f"scientific-figures expert missing: {literal}")

for relative, literals in required_literals.items():
    path = ROOT / relative
    if not path.exists():
        errors.append(f"Missing figure file: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for literal in literals:
        if literal not in text:
            errors.append(f"{relative} missing: {literal}")

if errors:
    print("FIGURE GATE TESTS FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("FIGURE GATE TESTS PASSED")
print(f"Result cases: {len(result_cases) + 3}")
print(f"Explanatory cases: {len(explanatory_cases)}")
