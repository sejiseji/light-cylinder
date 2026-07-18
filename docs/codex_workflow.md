# Codex Workflow

- Do not implement ahead of the selected wave.
- Do not create unused files or empty future directories.
- Do not revert existing user changes.
- Do not remove or weaken tests to make checks pass.
- Do not record local absolute paths in tracked files.
- Do not commit or push without user approval.
- Run `python scripts/check_all.py` after implementation.
- Run `git diff --check` after implementation.
- Report `git status --short`.
- Always report public safety check status.
- Do not claim visual verification for anything that was not actually viewed.
- Mark work as PARTIAL or BLOCKED when a problem remains.
