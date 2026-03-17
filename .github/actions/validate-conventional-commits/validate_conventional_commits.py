#!/usr/bin/env python3

import os
import re
import subprocess
import sys
from dataclasses import dataclass


CONVENTIONAL_COMMIT_PATTERN = re.compile(
    r"^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)"
    r"(\([a-z0-9._,/-]+\))?(!)?: [a-z0-9].+"
)


@dataclass(frozen=True)
class CommitRecord:
    sha: str
    subject: str
    parent_count: int


def resolve_range() -> str:
    event_name = os.environ.get("EVENT_NAME", "")
    before_sha = os.environ.get("BEFORE_SHA", "")
    after_sha = os.environ.get("AFTER_SHA", "")
    pr_base_sha = os.environ.get("PR_BASE_SHA", "")
    pr_head_sha = os.environ.get("PR_HEAD_SHA", "")

    if event_name == "pull_request":
        if not pr_base_sha or not pr_head_sha:
            raise ValueError("PR_BASE_SHA and PR_HEAD_SHA are required for pull_request events")
        return f"{pr_base_sha}..{pr_head_sha}"

    if not after_sha:
        raise ValueError("AFTER_SHA is required for non-pull_request events")

    if before_sha == "0000000000000000000000000000000000000000" or not before_sha:
        return after_sha

    return f"{before_sha}..{after_sha}"


def load_commits(commit_range: str) -> list[CommitRecord]:
    result = subprocess.run(
        ["git", "log", "--format=%H%x1f%s%x1f%P", commit_range],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git log failed")

    commits: list[CommitRecord] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        sha, subject, parents = line.split("\x1f")
        commits.append(
            CommitRecord(
                sha=sha,
                subject=subject,
                parent_count=len(parents.split()) if parents else 0,
            )
        )
    return commits


def validate_commit_subjects(commits: list[CommitRecord]) -> int:
    failures = 0
    checked = 0

    for commit in commits:
        if commit.parent_count > 1:
            continue

        checked += 1
        if CONVENTIONAL_COMMIT_PATTERN.match(commit.subject):
            continue

        print(
            f"::error::Non-conventional commit: {commit.sha} -> {commit.subject}",
            file=sys.stderr,
        )
        failures += 1

    print(f"Checked {checked} non-merge commit(s).")

    if failures:
        print(
            "One or more commits are not in Conventional Commits format. "
            "Expected: <type>(<optional-scope>)<optional-!>: <subject>",
            file=sys.stderr,
        )
        return 1

    print("All checked commits follow Conventional Commits.")
    return 0


def main() -> None:
    try:
        commit_range = resolve_range()
        print(f"Checking commits in range: {commit_range}")
        commits = load_commits(commit_range)
    except (ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

    sys.exit(validate_commit_subjects(commits))


if __name__ == "__main__":
    main()