#!/usr/bin/env python3
"""News image entry for 20 November 2026.

Copies the finished front page (``entry.png``, stored next to this file)
into the output directory the grader provides, byte for byte, and then
checks that the copy really is identical.  Standard library only, no
network access, no randomness: the same input always yields the same
output.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def locate_source() -> Path:
    """Return the path of the image sitting beside this script."""
    here = Path(__file__).resolve().parent
    return here / SOURCE_NAME


def destination_for(source: Path) -> Path:
    """Return where the copy should land, creating the folder if needed."""
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / source.name


def copy_and_check(source: Path, target: Path) -> int:
    """Copy ``source`` to ``target`` and confirm the copy is identical.

    Both the byte size and the SHA-256 digest of the written file are
    compared against the source, so a truncated or corrupted copy is
    caught even when its size happens to look right.  Returns the
    number of bytes written.  Raises ``SystemExit`` with a clear
    message if anything looks wrong, so a bad copy can never pass
    silently.
    """
    if not source.is_file():
        raise SystemExit(f"error: source image not found: {source}")

    payload = source.read_bytes()
    if not payload:
        raise SystemExit(f"error: source image is empty: {source}")

    expected_digest = hashlib.sha256(payload).hexdigest()
    target.write_bytes(payload)

    written = target.stat().st_size
    if written != len(payload):
        raise SystemExit(
            f"error: size mismatch after copy: wrote {written} bytes "
            f"but source has {len(payload)} bytes ({target})"
        )

    actual_digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual_digest != expected_digest:
        raise SystemExit(
            f"error: content mismatch after copy: {target} has "
            f"SHA-256 {actual_digest}, expected {expected_digest}"
        )

    print(
        f"wrote {target} ({written} bytes, "
        f"SHA-256 {actual_digest[:16]}..., matches source)"
    )
    return written


def main() -> int:
    source = locate_source()
    target = destination_for(source)
    copy_and_check(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
