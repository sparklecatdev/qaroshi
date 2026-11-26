#!/usr/bin/env python3
"""Verify and restore Qaroshi 21–23's packaged offline assets safely.

Existing user/contributor edits are NOT overwritten by default. Both compressed
archives and the uncompressed HTML must match the committed release manifest.
"""
from __future__ import annotations
import argparse
import bz2
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'Qaroshi_21_23_Translation_Immersion_Academy.html'
ARCHIVE = ROOT / 'Qaroshi_21_23_Precomputed_Data.zip'
COMPRESSED = ROOT / 'Qaroshi_21_23_Translation_Immersion_Academy.html.bz2'
MANIFEST = ROOT / 'Qaroshi_21_23_SOURCE_MANIFEST.json'


def _sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def restore(force: bool = False) -> Path:
    meta = json.loads(MANIFEST.read_text(encoding='utf-8'))
    expected_html = meta['site_sha256']
    if len(expected_html) != 64:
        raise ValueError('Missing or malformed site checksum')

    body_to_write = None
    if COMPRESSED.exists():
        compressed = COMPRESSED.read_bytes()
        if _sha(compressed) != meta['files'][COMPRESSED.name]:
            raise ValueError('Compressed HTML checksum mismatch')
        body = bz2.decompress(compressed)
        if _sha(body) != expected_html:
            raise ValueError('Restored site HTML checksum mismatch')
        if not body[:120].lstrip().lower().startswith(b'<!doctype html>'):
            raise ValueError('Restored site is not a standalone HTML page')
        existing = SITE.read_bytes() if SITE.exists() else None
        if existing is not None and existing != body and not force:
            raise FileExistsError('Local HTML differs. Refusing overwrite without --force')
        if existing != body:
            body_to_write = body
    elif not SITE.exists() or _sha(SITE.read_bytes()) != expected_html:
        raise FileNotFoundError('Neither verified packed site nor matching standalone HTML exists')

    if ARCHIVE.exists():
        packed = ARCHIVE.read_bytes()
        if _sha(packed) != meta['files'][ARCHIVE.name]:
            raise ValueError('Precomputed archive checksum mismatch')
        with zipfile.ZipFile(ARCHIVE) as z:
            bad = z.testzip()
            if bad is not None:
                raise ValueError(f'Damaged precomputed archive: {bad}')
            items = [item for item in z.infolist() if not item.is_dir()]
            names = [item.filename for item in items]
            if len(set(names)) != len(names):
                raise ValueError('Duplicate paths in precomputed archive')
            for item in items:
                name = item.filename
                if (name.startswith('/') or '\\' in name or
                    '..' in Path(name).parts or not name.startswith('data/')):
                    raise ValueError('Invalid packaged data path: '+name)
            # Validate all existing destinations before writing ANY file.
            conflicts = [item.filename for item in items
                         if (ROOT/item.filename).exists()
                         and (ROOT/item.filename).read_bytes() != z.read(item)]
            if conflicts and not force:
                raise FileExistsError('Precomputed data differs from local edits. '
                                      'Refusing overwrite without --force: '+', '.join(conflicts))
            for item in items:
                path = ROOT/item.filename
                if not path.exists() or path.read_bytes() != z.read(item):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(z.read(item))

    if body_to_write is not None:
        SITE.write_bytes(body_to_write)
    return SITE


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true', help='Explicitly replace locally edited packaged data and HTML')
    args = parser.parse_args()
    print(restore(force=args.force))
