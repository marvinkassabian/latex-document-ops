#!/usr/bin/env python3

import os
import sys
from pathlib import Path


def validate_release_version(ref_name: str = "") -> None:
    if ref_name:
        resolved_ref = ref_name
    elif os.environ.get("GITHUB_REF_NAME"):
        resolved_ref = os.environ["GITHUB_REF_NAME"]
    else:
        version_path = Path("VERSION")
        if not version_path.exists():
            print("VERSION file not found", file=sys.stderr)
            sys.exit(1)
        resolved_ref = f"v{version_path.read_text().strip()}"

    version_path = Path("VERSION")
    if not version_path.exists():
        print("VERSION file not found", file=sys.stderr)
        sys.exit(1)

    file_version = version_path.read_text().strip()
    if not file_version:
        print("VERSION is empty or missing", file=sys.stderr)
        sys.exit(1)

    tag_version = resolved_ref.lstrip("v")
    if tag_version != file_version:
        print(
            f"Tag version ({tag_version}) does not match VERSION ({file_version})",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Version check passed: v{tag_version}")


def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: validate_release_version.py [vX.Y.Z]", file=sys.stderr)
        sys.exit(1)

    ref_name = sys.argv[1] if len(sys.argv) > 1 else ""
    validate_release_version(ref_name)


if __name__ == "__main__":
    main()
