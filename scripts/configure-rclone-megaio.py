#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def configure_rclone_megaio(username: str, password: str) -> None:
    config_dir = Path.home() / ".config" / "rclone"
    config_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["rclone", "obscure", password],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"Error obscuring password: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    config_content = (
        "[mega]\n"
        "type = mega\n"
        f"user = {username}\n"
        f"pass = {result.stdout.strip()}\n"
    )
    (config_dir / "rclone.conf").write_text(config_content)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: configure-rclone-megaio.py <mega_io_username> <mega_io_password>", file=sys.stderr)
        sys.exit(1)

    configure_rclone_megaio(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()