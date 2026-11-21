# SCI-Skills Expert Contract 1.0

Every expert accepts either a bounded direct task or `schemas/expert-task.yaml`. Every expert returns `schemas/expert-result.yaml`; naming the contract without emitting its fields is invalid.

## Authority

- Experts execute specialist work and may recommend `PASS_CANDIDATE`, `REPAIR`, `BLOCKED`, or `NOT_ASSESSED`.
- Only the SCI-Skills orchestrator may pass, reopen, skip, or change a paper stage.
- Direct expert outputs are provisional until the orchestrator verifies task identity, evidence, outputs, manual returns, and acceptance criteria.

## Task identity

When identifiers are supplied, return the same `project_id`, `paper_family`, `stage_id`, and `task_id`. Do not merge or overwrite outputs from another task. If identifiers are absent in a direct call, set them to `null` instead of inventing them.

## Exact result fields

Return all fields below, using empty lists rather than omitting fields:

```yaml
contract_version: "1.0"
expert_skill:
project_id:
paper_family:
stage_id:
task_id:
task_status: COMPLETE | PARTIAL | BLOCKED | PROVISIONAL
inputs_reviewed: []
outputs: []
evidence_status: []
assumptions: []
author_input_needed: []
manual_actions: []
quality_checks: []
conflicts: []
conflict_resolution_status: NOT_REQUIRED | UNRESOLVED | RESOLVED_BY_ORCHESTRATOR
merge_permission: orchestrator_only
recommended_next_action:
stage_acceptance_recommendation: PASS_CANDIDATE | REPAIR | BLOCKED | NOT_ASSESSED
```

## Validation rules

- `PASS_CANDIDATE` requires every requested output and quality check to be supported by reviewed evidence.
- Use `PROVISIONAL` when source access is partial or upstream evidence is incomplete.
- Use `BLOCKED` when a required real-world action or missing source prevents responsible completion.
- Record claim-level conflicts with a `conflict_id`, conflict type, claim, source or locator, competing values or interpretations, and recommended resolution. Experts must not silently choose one result or merge conflicting evidence.
- Never report execution, upload, deposit, analysis, rendering, search coverage, or verification that did not occur.
- End user-facing output with exactly one primary next action.
