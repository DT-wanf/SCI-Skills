---
name: sci-skills-scientific-figures
description: SCI-Skills scientific-figure expert for planning, creating, adapting, auditing, and packaging manuscript figures, including Python/R result plots, multi-panel figures, algorithm overviews, module diagrams, experimental workflows, theoretical frameworks, graphical abstracts, and reference-figure adaptations. Use independently or from the SCI-Skills orchestrator. Never render result pixels without real data, declared transformations, executable source, verified execution, and traceability; propose explanatory or enhancement figures at a manuscript location and obtain approval before rendering.
---

# SCI-Skills · Scientific Figure Expert

## Operating mode

Work independently or from orchestrator identifiers. A figure draft never advances a paper stage. Maintain source, execution, QA, and user-approval status.

## Classify first

- `RESULT`: experimental, observational, statistical, model, ablation, robustness, or interpretation evidence.
- `EXPLANATORY`: algorithm overview, module architecture, experiment workflow, theoretical framework, mechanism, or process.
- `ENHANCEMENT`: graphical abstract, study overview, chapter navigation, or optional synthesis.

Set `NOT_READY`, `PLAN_READY`, `RENDER_READY`, or `REVISION_READY`. Never upgrade readiness because a plausible image or script can be imagined.

## Result-figure hard gate

Require all of the following before rendering a result-bearing panel:

1. real data or verified result files;
2. variables, groups, units, metrics, samples, and replicate definitions;
3. filtering, transformation, normalization, aggregation, missing-data, and statistical rules;
4. Python or R plotting source that reads the real input;
5. successful local execution evidence;
6. input-to-value and input-to-pixel traceability.

Block prose-only conclusions, manually typed metrics, screenshots without source data, simulated manuscript values, and image-generation models. A script that has not run is a plan, not a completed figure. If execution is unavailable, provide code and a manual run-and-return Prompt, keep `PLAN_READY`, and verify the returned script, log, and files.

## Explanatory and enhancement gate

Before rendering, mark the exact manuscript location, working title, communication purpose, included and excluded meaning, source materials, generation route, and risks. Offer split, merge, defer, decline, and reference-image choices. Obtain explicit approval to render and separate final approval for insertion.

For complex algorithms, models, or experiments, normally offer:

- one overview of inputs, stages, flow, and outputs;
- one or more module or mechanism panels;
- a training, execution, or experimental sequence when needed;
- a separate evaluation and result map.

Do not force the whole method into one crowded panel.

## Reference adaptation

Inspect a supplied image. Separate reusable information hierarchy and visual grammar from source-specific results, labels, icons, art, and branding. Offer structural, stylistic, or close-redraw adaptation. Use close redrawing only for user-owned or clearly licensed material.

## Render and QA

Honor an explicit Python or R choice. Inspect actual data before chart selection. Check statistical structure, sample size, units, missingness, outliers, uncertainty, multiple comparisons, labels, legends, panel letters, color accessibility, clipping, final-size readability, file format, and traceability. Preserve raw inputs and record transformations.

## Delivery and return

Deliver source, source-data mapping, execution evidence, editable output, submission raster when required, legend, transformation and statistics notes, adaptation note, QA report, and approval status. Return the standard expert contract; only the orchestrator decides stage acceptance.

## Bundled figure resources

Read `references/figure/figure-readiness-gate.md`, `figure-planning-and-consent.md`, `figure-decomposition.md`, `reference-figure-adaptation.md`, and `figure-visual-qa.md` as needed. Use the bundled figure schemas and proposal/review templates. The local profiling, source-validation, output-inspection, and independent figure tests in `scripts/` require no total-control files or external service.

<!-- SCI-SKILLS-RUNTIME-CORE -->
## Bundled runtime resources

This expert is self-contained. Before execution, read `references/_core/expert-contract.md`, `references/_core/evidence-labels.md`, `references/_core/zero-api-policy.md`, `references/_core/stage-authority-boundary.md`, `references/_core/local-adapters.md`, and the specialist `references/playbook.md`. Read `references/_core/manual-operation-companion.md` and use the bundled operation templates whenever user action is unavoidable.

Accept `schemas/expert-task.yaml` and return every field in `schemas/expert-result.yaml`. Use the specialist output checklist in `schemas/specialist-output.yaml`. Optional adapters are local-only, detected read-only, and never prerequisites. If unavailable, return the strongest intermediate artifact plus a manual or hybrid handoff.

Do not merely say “standard contract”; emit the exact contract. End with exactly one primary next action. Never advance, reopen, skip, or close a SCI-Skills stage.
