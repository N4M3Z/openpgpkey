#!/usr/bin/env python3
"""Render keys.yaml into a Web Key Directory (draft-koch-openpgp-webkey-service).

Layout, advanced method, served from openpgpkey.<domain>:

    site/.well-known/openpgpkey/<domain>/policy        empty file, required
    site/.well-known/openpgpkey/<domain>/hu/<hash>     binary key, one per address

<hash> is the Z-Base-32 encoding of the SHA-1 of the lowercased local part.
The file holds the key in binary (not armored) transferable public key
format, exported from the block under pubkeys/<fingerprint>.asc. Every
export is checked: the imported primary fingerprint must equal the file
name, and the key must carry a user id for <local>@<domain>.

Usage: build-wkd.py [--check]   (--check renders to a temp dir and diffs)
"""

from __future__ import annotations

import base64
import hashlib
import pathlib
import re
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site" / ".well-known" / "openpgpkey"
ZBASE32 = "ybndrfg8ejkmcpqxot1uwisza345h769"
STD32 = "abcdefghijklmnopqrstuvwxyz234567"


def zbase32_sha1(local_part: str) -> str:
    digest = hashlib.sha1(local_part.lower().encode()).digest()  # noqa: S324  WKD mandates SHA-1
    encoded = base64.b32encode(digest).decode().lower().rstrip("=")
    return encoded.translate(str.maketrans(STD32, ZBASE32))


def gpg(home: pathlib.Path, *args: str, stdin: bytes | None = None) -> bytes:
    result = subprocess.run(  # noqa: S603  fixed argv, no shell
        ["gpg", "--homedir", str(home), "--batch", "--quiet", "--no-autostart", *args],
        input=stdin,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"gpg {' '.join(args)} failed: {result.stderr.decode(errors='replace').strip()}"
        )
    return result.stdout


def load_key(home: pathlib.Path, fingerprint: str) -> tuple[bytes, set[str]]:
    """Dearmor pubkeys/<fingerprint>.asc, prove the fingerprint, return the
    binary key and the addresses its user ids carry. No keyring and no
    agent: `--dearmor` and `--show-keys` read the file alone, so the build
    runs in a sandbox and in CI without gpg state."""
    block = ROOT / "pubkeys" / f"{fingerprint}.asc"
    if not block.is_file():
        raise SystemExit(f"keys.yaml names {fingerprint} but pubkeys/{fingerprint}.asc is missing")
    binary = gpg(home, "--dearmor", stdin=block.read_bytes())
    listing = gpg(home, "--with-colons", "--with-fingerprint", "--show-keys", str(block)).decode()
    primaries = [line.split(":")[9] for line in listing.splitlines() if line.startswith("fpr:")]
    if not primaries or primaries[0] != fingerprint:
        raise SystemExit(
            f"pubkeys/{fingerprint}.asc holds primary {primaries[:1]}, not {fingerprint}"
        )
    if len([line for line in listing.splitlines() if line.startswith("pub:")]) != 1:
        raise SystemExit(f"pubkeys/{fingerprint}.asc must hold exactly one key")
    addresses = set()
    for line in listing.splitlines():
        if line.startswith("uid:"):
            uid = line.split(":")[9]
            if "<" in uid and ">" in uid:
                addresses.add(uid[uid.index("<") + 1 : uid.index(">")].lower())
    return binary, addresses


def validate_domain(domain: object) -> str:
    """Reject domain values that can escape the output directory."""
    if (
        not isinstance(domain, str)
        or not 1 <= len(domain) <= 253
        or any(
            re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label) is None
            for label in domain.split(".")
        )
    ):
        raise SystemExit("keys.yaml domain must be an ASCII DNS name.")
    return domain


def render(out: pathlib.Path) -> dict[str, str]:
    config = yaml.safe_load((ROOT / "keys.yaml").read_text())
    domain = validate_domain(config["domain"])
    directory = out / domain
    hu = directory / "hu"
    hu.mkdir(parents=True, exist_ok=True)
    (directory / "policy").write_bytes(b"")
    written: dict[str, str] = {}
    with tempfile.TemporaryDirectory() as home_dir:
        home = pathlib.Path(home_dir)
        home.chmod(0o700)
        for entry in config["keys"]:
            fingerprint = entry["fingerprint"].upper()
            binary, carried = load_key(home, fingerprint)
            for local in entry["addresses"]:
                address = f"{local.lower()}@{domain}"
                if address not in carried:
                    raise SystemExit(
                        f"{fingerprint} carries no user id for {address}; it has {sorted(carried)}"
                    )
                name = zbase32_sha1(local)
                (hu / name).write_bytes(binary)
                written[f"{domain}/hu/{name}"] = f"{address} -> {fingerprint}"
    return written


def main(argv: list[str]) -> int:
    if "--check" in argv:
        with tempfile.TemporaryDirectory() as scratch:
            expected = pathlib.Path(scratch) / "openpgpkey"
            render(expected)
            drift = []
            for path in sorted(expected.rglob("*")):
                if path.is_file():
                    rel = path.relative_to(expected)
                    live = SITE / rel
                    if not live.is_file() or live.read_bytes() != path.read_bytes():
                        drift.append(str(rel))
            for path in sorted(SITE.rglob("*")) if SITE.exists() else []:
                if path.is_file() and not (expected / path.relative_to(SITE)).is_file():
                    drift.append(f"{path.relative_to(SITE)} (stale)")
            if drift:
                print(
                    "site/ does not match keys.yaml; run scripts/build-wkd.py:\n  "
                    + "\n  ".join(drift)
                )
                return 1
            print("site/ matches keys.yaml")
            return 0
    written = render(SITE)
    for path, what in sorted(written.items()):
        print(f"{path}  {what}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
