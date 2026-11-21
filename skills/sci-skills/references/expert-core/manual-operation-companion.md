# Manual Operation Companion Contract

Use this contract whenever the user must operate a website, database, repository, submission system, office application, statistical environment, or other software outside the current conversation.

## Required behavior

1. Pause the current task without discarding project or stage state.
2. Explain the operation goal, required files, expected evidence, privacy constraints, and what will happen after return.
3. Provide the complete copyable Prompt from `templates/operation-companion-prompt.md`.
4. Tell the side conversation to give one step at a time and use screenshots when the interface differs.
5. Require `templates/operation-return-card.md` plus the actual files, screenshots, logs, or identifiers.
6. Verify the return before claiming completion.

An instruction list is not execution evidence. If login is required, the user logs in privately; neither conversation may request credentials. If software installation would be needed, keep it outside the mainline and first offer a no-install fallback.

