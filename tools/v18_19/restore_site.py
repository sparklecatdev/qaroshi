#!/usr/bin/env python3
"""Restore the byte-for-byte Qaroshi 18+19 standalone studio from the checked-in gzip.

This wrapper keeps the upstream branch additive and avoids changing canonical data.
The full app can alternatively be regenerated from sources with build_release.py.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "Qaroshi_18_19_Living_Language_Studio.html.gz"
DEST = ROOT / "Qaroshi_18_19_Living_Language_Studio.html"
EXPECTED_SHA256 = "08531faa297c44e8cbad7339fa3619178438403b549be1118974f4f9ffb1deeb"

def restore(force: bool = False) -> Path:
    data = gzip.decompress(ARCHIVE.read_bytes())
    actual = hashlib.sha256(data).hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError(f"Studio archive checksum mismatch: {actual}")
    if DEST.exists():
        existing = hashlib.sha256(DEST.read_bytes()).hexdigest()
        if existing == EXPECTED_SHA256:
            return DEST
        if not force:
            raise FileExistsError(f"{DEST} exists with different content; use --force to replace")
    DEST.write_bytes(data)
    return DEST

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="replace an existing nonmatching generated app")
    args = parser.parse_args()
    print(restore(force=args.force))
