#!/usr/bin/env python3

import subprocess
import sys
import time
from pathlib import Path


def reset_release_dir(remote_release_path: str) -> None:
    result = subprocess.run(
        ["rclone", "lsf", remote_release_path],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        subprocess.run(["rclone", "purge", remote_release_path], check=True)
        time.sleep(45)

    subprocess.run(["rclone", "mkdir", remote_release_path], check=True)
    time.sleep(5)


def upload_one_file(source_file: Path, dest_path: str) -> None:
    subprocess.run(
        [
            "rclone",
            "copyto",
            str(source_file),
            f"{dest_path}/{source_file.name}",
            "--retries",
            "8",
            "--low-level-retries",
            "15",
            "--retries-sleep",
            "15s",
            "--timeout",
            "5m",
        ],
        check=True,
    )
    time.sleep(5)


def upload_directory(local_dir: Path, remote_dir: str) -> None:
    if not local_dir.exists():
        return

    subprocess.run(["rclone", "mkdir", remote_dir], check=True)
    time.sleep(5)
    for pdf in sorted(local_dir.glob("*.pdf")):
        upload_one_file(pdf, remote_dir)


def upload_once(remote_release_path: str) -> bool:
    try:
        upload_directory(Path("build"), remote_release_path)
        upload_directory(Path("build/sections"), f"{remote_release_path}/sections")
        upload_directory(Path("build/frontmatter"), f"{remote_release_path}/frontmatter")
        return True
    except subprocess.CalledProcessError:
        return False


def upload_pdfs_to_protondrive(release_tag: str, proton_drive_path: str) -> None:
    remote_release_path = f"protondrive:{proton_drive_path}/{release_tag}"
    for attempt in range(1, 4):
        reset_release_dir(remote_release_path)
        if upload_once(remote_release_path):
            return
        if attempt < 3:
            time.sleep(30 * attempt)

    print("Upload failed after 3 attempts", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: upload_pdfs_to_protondrive.py <release_tag> <proton_drive_path>", file=sys.stderr)
        sys.exit(1)

    upload_pdfs_to_protondrive(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
