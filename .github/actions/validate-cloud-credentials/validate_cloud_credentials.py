#!/usr/bin/env python3

import json
import os
import sys
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SecretShape:
    name: str
    provided: bool
    length: int
    trimmed_length: int
    has_whitespace: bool


def describe_secret(name: str, value: str) -> SecretShape:
    return SecretShape(
        name=name,
        provided=bool(value),
        length=len(value),
        trimmed_length=len(value.strip()),
        has_whitespace=(any(ch.isspace() for ch in value) if value else False),
    )


def print_shape(shape: SecretShape) -> None:
    status = "set" if shape.provided else "missing"
    print(
        f"[{shape.name}] status={status} length={shape.length} "
        f"trimmed_length={shape.trimmed_length} has_whitespace={shape.has_whitespace}"
    )


def normalize_secret_map(raw: Dict[str, str]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in raw.items():
        normalized[key.lower()] = value
    return normalized


def get_secret(secret_map: Dict[str, str], key: str) -> str:
    return secret_map.get(key.lower(), "")


def validate(provider: str, secrets_json: str) -> int:
    print(f"Validating credentials for provider: {provider}")

    try:
        loaded = json.loads(secrets_json or "{}")
    except json.JSONDecodeError as exc:
        print(f"Unable to parse secrets_json: {exc}", file=sys.stderr)
        return 1

    if not isinstance(loaded, dict):
        print("secrets_json must decode to an object/map", file=sys.stderr)
        return 1

    secret_map = normalize_secret_map({str(k): "" if v is None else str(v) for k, v in loaded.items()})
    visible_keys = sorted(secret_map.keys())

    print(f"Visible secrets in context: {len(visible_keys)}")
    if visible_keys:
        print(f"Visible secret keys: {', '.join(visible_keys)}")
    else:
        print("Visible secret keys: (none)")

    mega_user_shape = describe_secret("mega_io_username", get_secret(secret_map, "mega_io_username"))
    mega_pass_shape = describe_secret("mega_io_password", get_secret(secret_map, "mega_io_password"))
    proton_user_shape = describe_secret("proton_drive_username", get_secret(secret_map, "proton_drive_username"))
    proton_pass_shape = describe_secret("proton_drive_password", get_secret(secret_map, "proton_drive_password"))
    proton_mailbox_shape = describe_secret(
        "proton_drive_mailbox_password",
        get_secret(secret_map, "proton_drive_mailbox_password"),
    )

    if provider == "mega-io":
        print_shape(mega_user_shape)
        print_shape(mega_pass_shape)

        if not mega_user_shape.provided or not mega_pass_shape.provided:
            print(
                "Missing Mega.io credentials. Configure repository secrets "
                "MEGA_IO_USERNAME and MEGA_IO_PASSWORD in the source repository.",
                file=sys.stderr,
            )
            return 1

    elif provider == "proton-drive":
        print_shape(proton_user_shape)
        print_shape(proton_pass_shape)
        print_shape(proton_mailbox_shape)

        if not proton_user_shape.provided or not proton_pass_shape.provided:
            print(
                "Missing Proton Drive credentials. Configure repository secrets "
                "PROTON_DRIVE_USERNAME and PROTON_DRIVE_PASSWORD in the source repository.",
                file=sys.stderr,
            )
            return 1

    else:
        print(f"Unknown provider '{provider}'. Expected mega-io or proton-drive.", file=sys.stderr)
        return 1

    print("Credential validation passed.")
    return 0


def main() -> None:
    provider = os.environ.get("PROVIDER", "")
    secrets_json = os.environ.get("SECRETS_JSON", "{}")

    # Backward compatibility for local/manual invocation.
    if len(sys.argv) == 3:
        provider, secrets_json = sys.argv[1:]
    elif len(sys.argv) not in (1,):
        print(
            "Usage: validate_cloud_credentials.py [<provider> <secrets_json>]",
            file=sys.stderr,
        )
        sys.exit(1)

    if not provider:
        print("PROVIDER is required", file=sys.stderr)
        sys.exit(1)

    exit_code = validate(provider, secrets_json)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
