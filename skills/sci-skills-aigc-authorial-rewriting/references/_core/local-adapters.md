# Optional Local Adapter Contracts

Adapters are local execution routes, not user-facing skills and not mainline dependencies.

| Adapter | Availability evidence | Allowed work | Fallback |
| --- | --- | --- | --- |
| `local-python` | executable plus required local packages | deterministic analysis, plotting, validation, file processing | source code, input contract, and manual run companion |
| `local-r` | executable plus required local packages | statistical analysis and R figures | R script, package list, and manual run companion |
| `local-file-import` | readable user file of a supported type | parse PDF/RIS/BibTeX/NBIB/CSV/XLSX/JSON/PPTX/DOCX | upload or conversion instructions |
| `manual-database-export` | user has lawful interface access | guided export through an ordinary webpage | query and field checklist without claiming export |
| `local-document-rendering` | local renderer already available | render and visually verify documents or decks | complete content blueprint and software companion |
| `local-model-already-available` | capability is already exposed and user opts in | bounded auxiliary processing | disabled; continue with the primary model |

Detection is read-only. Do not install software, modify user environments, request credentials, or call external APIs. Record status as `AVAILABLE`, `UNAVAILABLE`, `NOT_CHECKED`, `USER_ACTION_REQUIRED`, or `DEGRADED`.

