# Statistical Analysis and Reporting Playbook

## Design before computation

Identify the research question, estimand, experimental or observational unit, sampling, groups, repeated measures, hierarchy, missingness, confounding, outcome type, predictors, planned contrasts, and multiplicity. Do not treat technical replicates or repeated measurements as independent biological or participant-level samples.

## Analysis plan

For every analysis record inputs, inclusion and exclusion, preprocessing, assumptions, model or test, effect estimate, uncertainty interval, multiplicity control, sensitivity analysis, diagnostic, software, version, random seed when relevant, and output location.

## Execution evidence

Distinguish a proposed analysis from an actual local run. `EXECUTED_LOCAL` requires accessible input identifiers, code or command, environment details, logs, and output. If computation cannot run, return a plan and code labelled `NOT_EXECUTED`.

## Reporting

Report sample sizes and replicate definitions, effect sizes, confidence intervals, exact p values where appropriate, assumptions and diagnostics, missing-data handling, correction method, model specification, and limitations. Do not substitute significance for importance or imply causation from association.

