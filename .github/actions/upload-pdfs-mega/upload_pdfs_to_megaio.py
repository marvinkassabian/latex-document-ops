#!/usr/bin/env python3

import subprocess
import sys


def upload_pdfs_to_megaio(release_tag: str, mega_io_path: str) -> None:
    remote_release_path = f"mega:{mega_io_path}/{release_tag}"

    purge_result = subprocess.run(
        ["rclone", "purge", remote_release_path],
        capture_output=True,
        text=True,
        check=False,
    )
    if purge_result.returncode != 0:
        stderr = purge_result.stderr.strip().lower()
        if "not found" not in stderr and "directory not found" not in stderr:
            raise subprocess.CalledProcessError(
                purge_result.returncode,
                purge_result.args,
                output=purge_result.stdout,
                stderr=purge_result.stderr,
            )

    subprocess.run(
        [
            "rclone",
            "copy",
            "build",
            remote_release_path,
            "--include",
            "**/*.pdf",
            "--include",
            "*.pdf",
            "--exclude",
            "**",
        ],
        check=True,
    )


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: upload_pdfs_to_megaio.py <release_tag> <mega_io_path>", file=sys.stderr)
        sys.exit(1)

    upload_pdfs_to_megaio(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
