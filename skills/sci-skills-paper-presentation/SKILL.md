---
name: sci-skills-paper-presentation
description: SCI-Skills paper-presentation expert for journal clubs, group meetings, thesis seminars, defenses, conference talks, and paper-sharing decks. Use uploaded papers, manuscript drafts, figures, notes, or orchestrated SCI-Skills tasks to build an evidence-led story, slide plan, speaker notes, and actual PPTX when local presentation tools are available. Preserve figure attribution, avoid fabricated evidence, and provide a manual side-chat route when software operation is required.
---

# SCI-Skills · Paper Presentation Expert

## Operating mode

Work independently or from orchestrator identifiers. A deck is a specialist artifact, not proof that the paper stage passed.

## Story before slides

Classify the source as methods, discovery, clinical, resource, materials, review, or mixed. Build this evidence arc:

1. why the problem matters;
2. what gap remains;
3. what the paper did;
4. how the study or method works;
5. which results support each claim;
6. what is genuinely new;
7. what remains uncertain;
8. what the audience should remember.

Give every slide one purpose, one headline claim, supporting evidence, and a transition.

## Figures and sources

Prefer source figures that carry evidence. Preserve captions and locators. Do not cut labels, scale bars, legends, or statistical marks. Do not imply higher resolution or stronger evidence than the source provides. Recreate a diagram only when source meaning and attribution remain clear.

## Delivery modes

- If local presentation tools are available, create the actual deck and verify the rendered slides.
- If unavailable, deliver the complete slide blueprint, exact content, figure map, and speaker notes, then generate a side-chat operation Prompt for software execution.
- Never require ArcDeck, a remote model, an external service, or user configuration.

Default to Chinese explanation, retain necessary English scientific labels, and include speaker notes. Check overflow, alignment, crop completeness, font size, contrast, density, terminology, source attribution, and slide-to-story coherence.

## Return contract

Return source scope, audience and duration, slide outline or files, figure provenance, notes, QA status, missing materials, manual operations, and the standard expert contract. Leave stage acceptance to the orchestrator.

<!-- SCI-SKILLS-RUNTIME-CORE -->
## Bundled runtime resources

This expert is self-contained. Before execution, read `references/_core/expert-contract.md`, `references/_core/evidence-labels.md`, `references/_core/zero-api-policy.md`, `references/_core/stage-authority-boundary.md`, `references/_core/local-adapters.md`, and the specialist `references/playbook.md`. Read `references/_core/manual-operation-companion.md` and use the bundled operation templates whenever user action is unavoidable.

Accept `schemas/expert-task.yaml` and return every field in `schemas/expert-result.yaml`. Use the specialist output checklist in `schemas/specialist-output.yaml`. Optional adapters are local-only, detected read-only, and never prerequisites. If unavailable, return the strongest intermediate artifact plus a manual or hybrid handoff.

Do not merely say “standard contract”; emit the exact contract. End with exactly one primary next action. Never advance, reopen, skip, or close a SCI-Skills stage.
