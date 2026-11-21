# Manual Operation Companion

## Trigger

Use this protocol when a task requires a website, software installation, institutional login, paid access, repository deposit, experiment, local execution, submission system, or more than a trivial manual action. Also trigger whenever the user says they do not know how to operate the interface.

## Procedure

1. Keep the original project and stage open.
2. Assign a unique `operation_task_id`.
3. Explain why the action cannot be completed inside the current conversation.
4. Generate `templates/operation-companion-prompt.md` with the minimum necessary project context.
5. Ask the user to open a new conversation and paste the Prompt.
6. Require one-step-at-a-time guidance, screenshot-based recovery, credential safety, and output verification.
7. Require `templates/operation-return-card.md` at completion.
8. Match the returned project ID, stage ID, and task ID before accepting evidence.
9. Inspect returned files, logs, screenshots, identifiers, filters, and limitations.
10. Resume or repair the original stage; never auto-pass it.

## Safety

- Never ask the user to paste passwords, verification codes, private keys, session cookies, or complete access tokens.
- Tell the side chat not to claim success before the expected file or identifier exists.
- Preserve raw downloads and record source, date, filters, and access limitations.
- Treat screenshots as navigation evidence, not as a substitute for source data when files are required.
