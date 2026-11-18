#!/usr/bin/env python3
"""Publish the 18 November 2026 front page.

This is the entry program for make.fun's news-image-20261118 bounty:
it takes the artwork stored in this repository (``entry.png``) and
writes it to the judging location ``/output/entry.png``.

The copy is fully deterministic: no network access, no clock, no
randomness. After copying, the program hashes both files and only
reports success when the two digests match, so a truncated or
corrupted write can never pass silently.
"""

import argparse
import hashlib
import shutil
import sys
from pathlib import Path


OK = 0
SOURCE_MISSING = 2
DESTINATION_ERROR = 3
DIGEST_MISMATCH = 4
SAME_FILE = 5

COPY_CHUNK = 128 * 1024


def sha256_hex(path):
    """Return the SHA-256 hex digest of a file, read in chunks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(COPY_CHUNK)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def publish(artwork, target, verify=True, quiet=False):
    """Copy ``artwork`` to ``target`` and optionally verify the copy."""
    if not artwork.is_file():
        print(f"error: artwork not found: {artwork}", file=sys.stderr)
        return SOURCE_MISSING

    try:
        resolved_source = artwork.resolve()
        resolved_target = target.resolve()
    except OSError:
        resolved_source = artwork
        resolved_target = target

    if resolved_source == resolved_target:
        print("error: source and destination are the same file",
              file=sys.stderr)
        return SAME_FILE

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory: {exc}",
              file=sys.stderr)
        return DESTINATION_ERROR

    try:
        with artwork.open("rb") as source_handle, \
                target.open("wb") as target_handle:
            shutil.copyfileobj(source_handle, target_handle,
                               length=COPY_CHUNK)
    except OSError as exc:
        print(f"error: cannot write {target}: {exc}", file=sys.stderr)
        return DESTINATION_ERROR

    if verify:
        source_digest = sha256_hex(artwork)
        target_digest = sha256_hex(target)
        if source_digest != target_digest:
            print("error: digest mismatch after copy", file=sys.stderr)
            return DIGEST_MISMATCH
        if not quiet:
            print(f"wrote {target} ({target.stat().st_size} bytes)")
            print(f"sha256: {target_digest}")
    elif not quiet:
        print(f"wrote {target} ({target.stat().st_size} bytes)")

    return OK


def build_parser():
    """Build the command line parser for this program."""
    parser = argparse.ArgumentParser(
        description="Publish the 18 November 2026 front page to "
                    "/output/entry.png.")
    parser.add_argument(
        "--artwork",
        type=Path,
        default=Path(__file__).resolve().parent / "entry.png",
        help="artwork file to publish (default: entry.png next to this script)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("/output/entry.png"),
        help="destination path (default: /output/entry.png)",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="skip the digest check after copying",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print nothing on success (errors still go to stderr)",
    )
    return parser


def main(argv=None):
    """Parse arguments and publish the artwork."""
    args = build_parser().parse_args(argv)
    return publish(args.artwork, args.out, verify=not args.no_verify,
                   quiet=args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
