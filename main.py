#!/usr/bin/env python3
"""News image entry for make.fun news-image-20261118.

Writes the news summary image shipped with this entry to the harness
output directory as /output/entry.png, byte for byte.

The image is a front page for Wednesday 18 November 2026: six panels sum up
the day's world news (Trump lands in Manila for Quad talks; Ukraine strikes
the Crimea bridge for a second day; Iran drones target a US radar in
Bahrain; Nvidia revenue doubles to $115.8bn; Dhoni retires from the IPL;
Cyclone Akvan bears down on the Bay of Bengal), with a ticker for the
Canada-China trade extension, Britain's sanctions on settlement firms, and
the UN's count of 372 civilians killed in Ukraine in October.

The program is deliberately simple: it copies the bundled image file. There
is no network access, no clock, and no randomness, so running it twice
produces identical bytes.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    source = os.path.join(os.path.dirname(os.path.abspath(__file__)), SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)
    # Prove the copy is exact: the output hash must equal the source hash.
    # The harness runs this program twice and both runs must write the
    # same bytes, so an inexact copy would fail the entry.
    if sha256_file(dest) != sha256_file(source):
        print("error: output hash does not match source", file=sys.stderr)
        return 1
    print("wrote", dest, sha256_file(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
