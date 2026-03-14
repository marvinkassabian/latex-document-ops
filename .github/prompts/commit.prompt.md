---
description: "Generate a commit message following Conventional Commits format based on git diff"
name: "generate-commit-message"
argument-hint: "Optional: additional context or scope"
tools:
   - execute/runInTerminal
   - execute/getTerminalOutput
   - read/terminalLastCommand
   - read/terminalSelection
---

Generate a commit message following the Conventional Commits format defined in [commit-messages.instructions.md](../instructions/commit-messages.instructions.md).

## Workflow

1. Run `git status` to see pending changes
2. Run `git diff` to review unstaged changes
3. If changes are staged, run `git diff --staged` (this is most important for commit messages)
4. Analyze the changes and determine:
   - The appropriate type (`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `revert`)
   - An optional scope if it improves clarity
   - A concise, imperative subject line (lowercase except proper nouns)
   - Whether a body is needed to explain why, tradeoffs, or migration details
   - Whether this is a breaking change (requires `!` and `BREAKING CHANGE:` footer)

## Output Format

Provide the commit message in a code block, ready to copy and paste or use with `git commit -m`:

```
<type>(<optional-scope>): <subject>

<optional body - prefer bullet points for multiple changes>

<optional footer>
```

## Rules

- Subject line must be concise, imperative, and lowercase (except proper nouns)
- Do NOT end the subject with a period
- Body is optional but recommended for complex changes
- **Prefer bullet points in the body** for listing multiple changes or details
- If a breaking change exists, add `!` after type/scope AND include `BREAKING CHANGE:` footer
- Review the actual changes before generating the message - don't guess

## Additional Context

{Additional context or preferred scope if provided by user}
