---
name: sci-skills-web-data-acquisition
description: SCI-Skills web-data-acquisition expert for lawful research-data planning when existing evidence is verified as absent or critically insufficient. Use for official webpage downloads, repository files, licensed manual exports, authenticated user exports, permitted public-page collection, pilots, provenance, user audits, and cleaning handoffs. Use independently only after a data-sufficiency check or when dispatched by SCI-Skills. Never use third-party APIs, bypass access controls, or collect before the research-to-data mapping passes.
---

# SCI-Skills · Web Data Acquisition Expert

## Activation gate

Proceed only when reviewed evidence sets data status to `ABSENT` or `INSUFFICIENT`, the exact critical gap cannot be repaired through cleaning, derivation, coding, or existing linkage, and web evidence is methodologically appropriate. Stop for `UNKNOWN` or `SUFFICIENT`. A request to “crawl” does not override the gate.

## Zero-API source ladder

Evaluate in order and stop at the first adequate lawful route:

1. verified user-held data;
2. official files downloaded through ordinary webpages;
3. open repository or institutional archive files;
4. paid licensed data manually exported by the user;
5. authorized export from an authenticated interface;
6. permitted public-page collection as a documented last resort.

Do not call or configure any external API. Do not bypass authentication, paywalls, CAPTCHAs, technical protections, explicit prohibitions, or access limits.

## Research-to-data mapping

Map `research question -> construct -> observable signal -> unit -> field -> source -> analysis use`. Define population, time, geography, language, inclusion, exclusion, sampling, stopping, expected volume, provenance fields, output format, rights, privacy, bias, and cost before collection.

Offer two or three ranked source plans when unresolved. Verify mutable access, pricing, and licence facts from ordinary official webpages; otherwise mark them `待核实`.

## Pilot and audit

Require a pilot of 1-3 pages or about 10-50 records. Inspect fields, parsing, identifiers, duplicates, missingness, scope, bias, permissions, and raw-data preservation. Do not scale until the pilot passes.

After collection, preserve raw files and produce a data dictionary, provenance record, sample rows, logs, deviations, rights notes, and known-bias summary. Require explicit user approval before cleaning, transformation, deduplication, imputation, translation, or analysis.

## Manual companion

For login, download, export, software, or browser steps, generate a side-chat Prompt that gives one step at a time, requests screenshots when the interface differs, protects credentials, verifies files, and returns an operation card.

## Bundled acquisition resources

Read `references/data/data-sufficiency-gate.md`, `web-source-families.md`, and `web-data-collection.md`. Build plans with `schemas/web-data-collection-plan.yaml`, validate a populated plan with `scripts/validate_collection_plan.py`, and use `templates/data-acquisition-review-card.md` before any cleaning handoff. These resources run independently of the total-control skill.

## Return contract

Return the sufficiency decision, critical gap, source comparison, mapping table, field schema, pilot plan or evidence, provenance, audit status, cleaning handoff status, manual actions, and the standard expert contract. Stage acceptance belongs only to the orchestrator.

<!-- SCI-SKILLS-RUNTIME-CORE -->
## Bundled runtime resources

This expert is self-contained. Before execution, read `references/_core/expert-contract.md`, `references/_core/evidence-labels.md`, `references/_core/zero-api-policy.md`, `references/_core/stage-authority-boundary.md`, `references/_core/local-adapters.md`, and the specialist `references/playbook.md`. Read `references/_core/manual-operation-companion.md` and use the bundled operation templates whenever user action is unavoidable.

Accept `schemas/expert-task.yaml` and return every field in `schemas/expert-result.yaml`. Use the specialist output checklist in `schemas/specialist-output.yaml`. Optional adapters are local-only, detected read-only, and never prerequisites. If unavailable, return the strongest intermediate artifact plus a manual or hybrid handoff.

Do not merely say “standard contract”; emit the exact contract. End with exactly one primary next action. Never advance, reopen, skip, or close a SCI-Skills stage.
