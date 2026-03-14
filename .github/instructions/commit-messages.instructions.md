---
description: "Use when drafting git commit messages. Follow Conventional Commits format and keep the subject concise and imperative."
name: "Conventional Commit Messages"
---
# Conventional Commit Messages

- Before drafting a commit message, review pending changes with `git status` and `git diff` so the subject/body reflect the actual delta.
- If changes are staged, also review `git diff --staged` before finalizing the commit message.

Recommended commit workflow:

1. `git status`
2. `git diff`
3. `git add <paths>`
4. `git diff --staged`
5. Draft and run `git commit`

- Use Conventional Commits format: `<type>(<optional-scope>): <subject>`.
- Keep the subject line concise, imperative, and lowercase (except proper nouns).
- Prefer these types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `revert`.
- Use a scope when it improves clarity (for example `docs(manual)`, `fix(tex)`).
- Do not end the subject with a period.
- If a breaking change is introduced, include `!` after type or scope (for example `feat(api)!: ...`) and add a `BREAKING CHANGE:` footer.
- Add a body when needed to explain why, tradeoffs, or migration details.

Examples:

- `docs(manual): clarify triage section language`
- `fix(tex): correct broken hyperlink in contents`
- `chore(repo): add commit message instruction file`