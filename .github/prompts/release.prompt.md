---
description: "Prepare and cut a release by inferring the next version from the latest tag and diff, confirming it with the user, then updating changelog/version files, committing, tagging, and pushing"
name: "cut-release"
argument-hint: "Optional: release version and date, for example: 0.3.1 03/11/2026"
tools:
   - execute/runInTerminal
   - execute/getTerminalOutput
   - read/terminalLastCommand
---

Prepare and cut a release for this repository.

Arguments:
- Preferred input is `<VERSION> <DATE>`.
- Example: `0.3.1 03/11/2026`
- If the user provides only a version, infer the release date from today.
- If the user does not provide a version, infer the most likely next version from the latest SemVer tag and the commits/diff since that tag, then ask the user to confirm before making edits.
- Do not edit files, commit, tag, or push until the version is explicitly confirmed by the user.

Primary files:
- [CHANGELOG.md](../../CHANGELOG.md)
- [VERSION](../../VERSION)
- [commit-messages.instructions.md](../instructions/commit-messages.instructions.md)

Workflow:

1. Validate repo state first.
- Run `git status --short`.
- If the working tree is not clean, stop and summarize what must be resolved before cutting the release.
- Run `git tag --list | sort -V` and identify the latest SemVer tag.

2. Infer the next version when needed.
- If the user already supplied a version, use it.
- Otherwise, inspect commits and the diff from the latest SemVer tag to `HEAD`.
- Make a best-effort SemVer recommendation based on user-visible changes:
   - Patch for fixes only with no meaningful surface-area change.
   - Minor for backward-compatible additions or meaningful feature expansion.
   - Major for breaking changes to outputs, interfaces, documented workflows, or release artifacts.
- In `0.x` releases, treat breaking changes as a minor bump unless the user clearly wants to declare `1.0.0` stability.
- Present the guessed version and a short justification, then stop and ask the user to confirm or override it.
- After the user confirms, confirm the new tag `v<VERSION>` does not already exist.

3. Build the release summary from the actual delta.
- Review changes from the latest tag to `HEAD` using git history and diff tools.
- Draft a changelog entry based on the real user-visible changes, not just commit subjects.
- Focus on Added, Changed, and Fixed items when they are supported by the diff.

4. Update release files.
- Update [CHANGELOG.md](../../CHANGELOG.md) with a new version section using the provided release date.
- Update [VERSION](../../VERSION) to `<VERSION>`.
- Preserve existing formatting and file structure.

5. Verify before release.
- Review the edited diff.
- Run the strict release build for this repo.
- If the build fails, stop and report the failure instead of tagging.

6. Commit, tag, and push.
- Stage only the release files unless the user explicitly asked for more.
- Create a release commit using Conventional Commits format.
- Preferred subject: `chore(release): cut v<VERSION>`.
- Create an annotated tag: `git tag -a v<VERSION> -m "release v<VERSION>"`.
- Push the branch and the tag to `origin`.

7. Final response.
- Summarize the files changed.
- Report the commit SHA and tag name.
- Confirm whether the strict build passed.
- If any step was blocked, explain exactly why.

Rules:
- Do not guess changelog content; derive it from the diff since the latest tag.
- Do not guess the release version silently; if it was inferred, present it and wait for confirmation.
- Do not create the tag if the build or file updates fail.
- Do not push if commit or tag creation fails.
- Do not include unrelated working tree changes in the release commit.