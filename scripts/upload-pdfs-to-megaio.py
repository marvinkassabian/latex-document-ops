#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def upload_directory(local_dir: Path, remote_dir: str) -> None:
    if not local_dir.exists():
        return

    subprocess.run(["rclone", "mkdir", remote_dir], check=True)
    for pdf in sorted(local_dir.glob("*.pdf")):
        subprocess.run(["rclone", "copyto", str(pdf), f"{remote_dir}/{pdf.name}"], check=True)


def upload_pdfs_to_megaio(release_tag: str, mega_io_path: str) -> None:
    remote_release_path = f"mega:{mega_io_path}/{release_tag}"

    result = subprocess.run(
        ["rclone", "lsf", remote_release_path],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        subprocess.run(["rclone", "purge", remote_release_path], check=True)

    subprocess.run(["rclone", "mkdir", remote_release_path], check=True)
    upload_directory(Path("build"), remote_release_path)
    upload_directory(Path("build/sections"), f"{remote_release_path}/sections")
    upload_directory(Path("build/frontmatter"), f"{remote_release_path}/frontmatter")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: upload-pdfs-to-megaio.py <release_tag> <mega_io_path>", file=sys.stderr)
        sys.exit(1)

    upload_pdfs_to_megaio(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()