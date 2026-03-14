#!/usr/bin/env python3

import subprocess
import sys


def configure_rclone_megaio(username: str, password: str) -> None:
    username = username.strip()
    password = password.strip()

    if not username:
        print(
            "Missing Mega.io username. Set the mega_io_username secret in the calling workflow.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not password:
        print(
            "Missing Mega.io password. Set the mega_io_password secret in the calling workflow.",
            file=sys.stderr,
        )
        sys.exit(1)

    subprocess.run(
        [
            "rclone",
            "config",
            "delete",
            "mega",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    create_result = subprocess.run(
        [
            "rclone",
            "config",
            "create",
            "mega",
            "mega",
            f"user={username}",
            f"pass={password}",
            "--obscure",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if create_result.returncode != 0:
        print(
            f"Failed to create Mega.io rclone remote: {create_result.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)

    validate_result = subprocess.run(
        ["rclone", "lsd", "mega:"],
        capture_output=True,
        text=True,
        check=False,
    )
    if validate_result.returncode != 0:
        stderr = validate_result.stderr.strip()
        print(
            "Mega.io login validation failed. Confirm the MEGA account has been initialized in the browser, "
            "the username/password secrets are correct, the account does not require unsupported interactive 2FA, "
            f"and the remote is not temporarily blocked. rclone output: {stderr}",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: configure_rclone_megaio.py <mega_io_username> <mega_io_password>", file=sys.stderr)
        sys.exit(1)

    configure_rclone_megaio(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
