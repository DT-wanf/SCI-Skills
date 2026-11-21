# Expert Skill Routing

## Purpose

Dispatch specialist work to independent SCI-Skills experts while preserving the orchestrator's exclusive control over project state and stage acceptance.

## Routing rules

- Load the current stage before selecting an expert.
- Select no more than two primary experts by default.
- Do not ask beginners to choose an expert by technical name.
- Pass the smallest sufficient project context: project ID, paper family, stage ID, task ID, inputs, expected outputs, evidence boundaries, and acceptance criteria.
- Build the task with `schemas/expert-task.yaml` and accept only a return that passes `schemas/expert-result.yaml` and contract version `1.0`.
- Treat direct expert outputs as provisional until the orchestrator reviews them.
- Never let an expert advance, skip, close, or reopen a stage.
- Track tasks as `QUEUED`, `DISPATCHED`, `RETURNED`, `VERIFIED`, or `REJECTED_FOR_REPAIR`.
- Require exact project, family, stage, task, expert, and contract identity before merging results.
- If an expert is missing or incompatible, preserve the stage, label any fallback provisional, and issue a bounded repair or manual action rather than pretending dispatch succeeded.

## Expert registry

| Need | Expert skill |
| --- | --- |
| Search, citation verification, evidence matrix | `sci-skills-literature-search` |
| One-paper or multi-paper deep reading | `sci-skills-paper-deep-reading` |
| Section planning and evidence-based drafting | `sci-skills-manuscript-writing` |
| Academic language, translation, and terminology | `sci-skills-academic-polishing` |
| Real-data profiling, chart selection, result plots, method diagrams, layout/export QA | `sci-skills-scientific-figures` |
| Design, computation, inference, and reporting | `sci-skills-statistical-reporting` |
| Journal club, defense, and paper presentation | `sci-skills-paper-presentation` |
| Mock review and submission-readiness audit | `sci-skills-presubmission-review` |
| Point-by-point reviewer response | `sci-skills-reviewer-response` |
| Data/code availability and repository planning | `sci-skills-data-availability` |
| Web data only after insufficiency is verified | `sci-skills-web-data-acquisition` |
| AIGC-risk audit and authorial rewriting | `sci-skills-aigc-authorial-rewriting` |
| Quality-first journal recommendation | `sci-skills-journal-recommendation` |

## Common combinations

- Literature stage: literature search + paper deep reading.
- Analysis stage: statistical reporting + scientific figures.
- Writing stage: manuscript writing + academic polishing; add authorial rewriting only after scientific meaning is stable.
- Finalization stage: presubmission review + journal recommendation; add data availability or presentation when relevant.
- Reviewer revision: reviewer response + the specialist needed for the requested repair.

Before data acquisition, apply the data-sufficiency gate. Before rendering any figure, apply the figure-readiness gate and use the independent figure expert's current source-risk and design-risk checks rather than the orchestrator's legacy utility copies. Before journal recommendation, assess current manuscript quality. Before AIGC rewriting, confirm that the goal is authentic authorship rather than detector evasion.
