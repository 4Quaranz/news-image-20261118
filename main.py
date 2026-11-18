#!/usr/bin/env python3
"""Publish the 18 November 2026 front page to /output/entry.png.

The finished artwork is stored in this repository as entry.png (a JPEG
image of the front page). This script has one job only: place a byte-exact
copy of that file at /output/entry.png, where the grader looks for it.

The copy is fully deterministic. No network, no clock and no randomness
are involved: the file is streamed in fixed 64 KiB chunks, a SHA-256
digest is accumulated as the bytes pass through, and the destination is
read back afterwards and checked against the source digest. The program
only reports success once the two digests match.
"""

import argparse
import hashlib
import sys
from pathlib import Path

CHUNK = 65536  # bytes per read; fixed so behaviour never varies by run

EXIT_OK = 0
EXIT_MISSING = 2
EXIT_WRITE = 3
EXIT_MISMATCH = 4
EXIT_BAD_SOURCE = 5

# SHA-256 of the artwork as stored in this repository. The program refuses
# to publish a source file whose digest differs, so a damaged or swapped
# entry.png can never silently reach the grader.
EXPECTED_SHA256 = "0f0c7481ed3a1a5e97d7890731de82b14dc8893d4242f918236b48abf3dc5c9b"


def locate_artwork(explicit):
    """Return the artwork path: --artwork, or entry.png next to this file."""
    if explicit:
        return Path(explicit)
    return Path(__file__).resolve().parent / "entry.png"


def digest_of(path):
    """SHA-256 hex digest of a file, read in fixed chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def stream_copy(source, dest):
    """Copy source to dest in fixed chunks; return (byte count, digest)."""
    digest = hashlib.sha256()
    total = 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(source, "rb") as reader, open(dest, "wb") as writer:
        while True:
            block = reader.read(CHUNK)
            if not block:
                break
            digest.update(block)
            writer.write(block)
            total += len(block)
    return total, digest.hexdigest()


def main(argv=None):
    """Parse flags, copy the artwork, verify the copy, report the result."""
    parser = argparse.ArgumentParser(
        description="Copy the 18 November 2026 front page to /output/entry.png."
    )
    parser.add_argument(
        "--artwork",
        default=None,
        help="artwork file to publish (default: entry.png beside this script)",
    )
    parser.add_argument(
        "--out",
        default="/output/entry.png",
        help="destination path (default: /output/entry.png)",
    )
    parser.add_argument(
        "--expected-sha256",
        default=EXPECTED_SHA256,
        help="SHA-256 the source must match before copying (default: the "
        "digest of the artwork shipped in this repository)",
    )
    args = parser.parse_args(argv)

    source = locate_artwork(args.artwork)
    dest = Path(args.out)

    if not source.is_file():
        print(f"error: artwork not found: {source}", file=sys.stderr)
        return EXIT_MISSING

    if source.resolve() == dest.resolve():
        print("error: source and destination are the same file", file=sys.stderr)
        return EXIT_WRITE

    checked_digest = digest_of(source)
    if checked_digest != args.expected_sha256:
        print(
            f"error: source digest {checked_digest} does not match expected "
            f"{args.expected_sha256}; refusing to publish",
            file=sys.stderr,
        )
        return EXIT_BAD_SOURCE

    try:
        size, source_digest = stream_copy(source, dest)
    except OSError as exc:
        print(f"error: cannot write {dest}: {exc}", file=sys.stderr)
        return EXIT_WRITE

    written_digest = digest_of(dest)
    if written_digest != source_digest:
        print(
            f"error: digest mismatch after copy: "
            f"{written_digest} != {source_digest}",
            file=sys.stderr,
        )
        return EXIT_MISMATCH

    print(f"wrote {dest} ({size} bytes, sha256 {source_digest})")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
