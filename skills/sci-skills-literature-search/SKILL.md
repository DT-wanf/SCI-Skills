---
name: sci-skills-literature-search
description: SCI-Skills literature-search expert for topic reconnaissance, benchmark-paper discovery, reproducible search design, citation verification, screening, deduplication, evidence matrices, and bibliography exports. Use independently when users ask to search, verify, organize, or audit scholarly literature, or when the SCI-Skills orchestrator dispatches a literature task. Use no third-party API integration; rely on platform-native web search, official webpages, user-uploaded papers, and manually exported database files.
---

# SCI-Skills · Literature Search Expert

## Operating mode

Work independently for a bounded search task or accept an orchestrated task containing `project_id`, `paper_family`, `stage_id`, and `task_id`. Do not advance a paper stage. Return a pass candidate only for orchestrator review.

## Zero-API boundary

Do not request keys, tokens, endpoints, SDKs, or direct database integrations. Use platform-native browsing, official journal or database webpages, user-provided files, and manual exports such as RIS, BibTeX, NBIB, CSV, or PDF. When institutional login or batch export is necessary, produce a side-chat operation Prompt with one-step guidance and a return card.

## Workflow

1. Define the research question, evidence purpose, discipline, date, language, document type, population, method, and access constraints.
2. Distinguish representative discovery, benchmark-paper search, systematic search, citation verification, and gap support.
3. Convert the question into concept blocks with synonyms, controlled terms, abbreviations, spelling variants, and cautious wildcards.
4. Build a broad discovery query and a narrower confirmation query.
5. Select suitable ordinary webpage interfaces: PubMed, IEEE Xplore, ACM Digital Library, arXiv, journal sites, publisher sites, CNKI, Web of Science, Scopus, or discipline-specific sources as access permits.
6. Record source, complete query, date, filters, hit count, and access limitations.
7. Verify title, authors, year, venue, DOI, article type, correction or retraction status, and direct relevance from source pages or uploaded records.
8. Deduplicate by DOI, then normalized title, then author-year-title comparison.
9. Label each item as `精确同方向`, `同领域近似`, or `仅作类型示例`.
10. Separate verified findings from inferred research gaps.

Do not call a search systematic unless complete sources, dates, queries, filters, inclusion and exclusion rules, deduplication, and screening records are documented.

## Outputs

Provide the applicable concept table, search strings, source plan, verified paper table, screening log, deduplication summary, evidence matrix, candidate gap statements, and export guidance. Never invent bibliographic fields or claim full-text verification from an abstract.

Use `references/search/literature-database-export.md` for institutional or batch export, and `scripts/audit_bibliography_records.py` for local record identity and duplicate checks. Neither route calls a database API.

## Return contract

Return: expert skill, project and task identifiers when supplied, status, inputs reviewed, outputs, verified and pending evidence, assumptions, author inputs needed, manual actions, quality checks, and `PASS_CANDIDATE`, `REPAIR`, `BLOCKED`, or `NOT_ASSESSED`.

<!-- SCI-SKILLS-RUNTIME-CORE -->
## Bundled runtime resources

This expert is self-contained. Before execution, read `references/_core/expert-contract.md`, `references/_core/evidence-labels.md`, `references/_core/zero-api-policy.md`, `references/_core/stage-authority-boundary.md`, `references/_core/local-adapters.md`, and the specialist `references/playbook.md`. Read `references/_core/manual-operation-companion.md` and use the bundled operation templates whenever user action is unavoidable.

Accept `schemas/expert-task.yaml` and return every field in `schemas/expert-result.yaml`. Use the specialist output checklist in `schemas/specialist-output.yaml`. Optional adapters are local-only, detected read-only, and never prerequisites. If unavailable, return the strongest intermediate artifact plus a manual or hybrid handoff.

Do not merely say “standard contract”; emit the exact contract. End with exactly one primary next action. Never advance, reopen, skip, or close a SCI-Skills stage.
