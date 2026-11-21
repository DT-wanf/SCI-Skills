---
name: sci-skills-statistical-reporting
description: SCI-Skills statistical-analysis and reporting expert for study-design checks, analysis planning, local Python/R computation, assumptions, effect estimates, confidence intervals, p values, sample sizes, replicates, multiple comparisons, statistical Methods and Results, figure legends, and reviewer statistics concerns. Use independently or when dispatched by SCI-Skills. Never invent a computation, treat repeated measurements as independent, or claim execution without real data, code, and verified output.
---

# SCI-Skills · Statistical Reporting Expert

## Operating mode

Work independently or from orchestrator context. Separate planning, executed analysis, interpretation, and reporting. Do not advance a project stage.

## Diagnose the design

Establish what was measured, the independent unit, the unit entering the model, grouping or hierarchy, repeated or paired structure, censoring, missingness, exclusions, and the inference claimed. Never silently treat cells, images, fields, spectra, repeated readings, or model runs as independent samples.

## Analysis workflow

1. Map research questions and hypotheses to outcomes, predictors, covariates, contrasts, and estimands.
2. Check design fit, sample structure, power limitations, leakage, multiplicity, and preregistered decisions when available.
3. Select tests or models with explicit assumptions and alternatives.
4. Execute only with real input data and a local available Python/R environment.
5. Preserve code, package versions, console output, warnings, exclusions, and generated results.
6. Distinguish exploratory, confirmatory, sensitivity, and robustness analyses.
7. Report effect direction and magnitude, uncertainty, exact p values, independent `n`, and limitations.

Do not translate non-significance into equivalence or “no effect” without an appropriate design. Do not select methods only because they produce significance.

## Figure boundary

Audit error bars, box or violin conventions, stars, exact tests, panel-level `n`, paired structure, and source data. Do not create a result figure from prose, hand-entered summary values, or image generation. Require real inputs, local code, actual execution, and traceability.

## Outputs and return

Provide the analysis plan or verified outputs, assumptions and diagnostics, Methods wording, Results wording, reproducibility record, limitations, and `AUTHOR_INPUT_NEEDED` items. Return the standard expert contract and leave stage acceptance to the orchestrator.

Use `templates/analysis-plan.md` before execution and `schemas/execution-record.yaml` after an actual run. `scripts/validate_execution_record.py` may label a run `EXECUTED_LOCAL` only when referenced inputs, source, logs, and outputs exist locally.

<!-- SCI-SKILLS-RUNTIME-CORE -->
## Bundled runtime resources

This expert is self-contained. Before execution, read `references/_core/expert-contract.md`, `references/_core/evidence-labels.md`, `references/_core/zero-api-policy.md`, `references/_core/stage-authority-boundary.md`, `references/_core/local-adapters.md`, and the specialist `references/playbook.md`. Read `references/_core/manual-operation-companion.md` and use the bundled operation templates whenever user action is unavoidable.

Accept `schemas/expert-task.yaml` and return every field in `schemas/expert-result.yaml`. Use the specialist output checklist in `schemas/specialist-output.yaml`. Optional adapters are local-only, detected read-only, and never prerequisites. If unavailable, return the strongest intermediate artifact plus a manual or hybrid handoff.

Do not merely say “standard contract”; emit the exact contract. End with exactly one primary next action. Never advance, reopen, skip, or close a SCI-Skills stage.
