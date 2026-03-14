#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def obscure(secret: str) -> str:
    result = subprocess.run(
        ["rclone", "obscure", secret],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"Error obscuring secret: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def configure_rclone_protondrive(username: str, password: str, mailbox_password: str = "") -> None:
    config_dir = Path.home() / ".config" / "rclone"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_content = (
        "[protondrive]\n"
        "type = protondrive\n"
        f"username = {username}\n"
        f"password = {obscure(password)}\n"
    )
    if mailbox_password:
        config_content += f"mailbox_password = {obscure(mailbox_password)}\n"

    (config_dir / "rclone.conf").write_text(config_content)


def main() -> None:
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(
            "Usage: configure-rclone-protondrive.py <proton_username> <proton_password> [proton_mailbox_password]",
            file=sys.stderr,
        )
        sys.exit(1)

    mailbox_password = sys.argv[3] if len(sys.argv) > 3 else ""
    configure_rclone_protondrive(sys.argv[1], sys.argv[2], mailbox_password)


if __name__ == "__main__":
    main()