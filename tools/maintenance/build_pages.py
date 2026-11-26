#!/usr/bin/env python3
"""Publish only verified, readable Qaroshi pages, not the source/log archive.

This preserves legacy HTML URLs while keeping raw datasets, test logs, drafts,
manifests, scripts and zipped release files out of GitHub Pages. Source data
remains in Git and is never deleted by this command.
"""
from __future__ import annotations
import argparse
import bz2
import gzip
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT/'_site'
RELEASES = (
    ('Qaroshi_18_19_Living_Language_Studio.html',
     'Qaroshi_18_19_Living_Language_Studio.html.gz',
     '08531faa297c44e8cbad7339fa3619178438403b549be1118974f4f9ffb1deeb', gzip.decompress),
    ('Qaroshi_20_Speech_Studio.html',
     'Qaroshi_20_Speech_Studio.html.gz', None, gzip.decompress),
    ('Qaroshi_21_23_Translation_Immersion_Academy.html',
     'Qaroshi_21_23_Translation_Immersion_Academy.html.bz2', None, bz2.decompress),
)


def expected_sha(filename):
    if filename.startswith('Qaroshi_20_'):
        return json.loads((ROOT/'data/v20/release_manifest.json').read_text(encoding='utf-8'))['site_html_sha256']
    return json.loads((ROOT/'Qaroshi_21_23_SOURCE_MANIFEST.json').read_text(encoding='utf-8'))['site_sha256']


def restored_files():
    """Validate checksums and return raw bytes, without modifying any source file."""
    results = {}
    for name, archive, expected, decompressor in RELEASES:
        sha = expected or expected_sha(name)
        packed = ROOT/archive
        if not packed.is_file():
            # A correctly restored standalone page is also a valid release source.
            available = ROOT/name
            if not available.is_file() or hashlib.sha256(available.read_bytes()).hexdigest() != sha:
                raise FileNotFoundError(f'Missing verified release asset: {archive}')
            raw = available.read_bytes()
        else:
            raw = decompressor(packed.read_bytes())
        if hashlib.sha256(raw).hexdigest() != sha:
            raise ValueError(f'Release HTML checksum mismatch: {archive}')
        if not raw[:120].lstrip().lower().startswith(b'<!doctype html>'):
            raise ValueError(f'Invalid HTML header: {archive}')
        results[name] = raw
    return results


def stage(destination: Path):
    from build_portal import build
    build()
    current = ROOT/'Qaroshi_Wiki.html'
    academy = ROOT/'Qaroshi_Academy.html'
    if not current.is_file() or not academy.is_file():
        raise FileNotFoundError('Build the Wiki and Academy first with `make build`.')
    raw = restored_files()
    catalog = json.loads((ROOT/'data/site_catalog.json').read_text(encoding='utf-8'))
    destination.mkdir(parents=True, exist_ok=True)
    for file in sorted(ROOT.glob('*.html')):
        if file.name == 'index.html':
            # Prevent stale tracked index snapshots from hiding the rebuilt Wiki.
            continue
        shutil.copyfile(file, destination/file.name)
    shutil.copyfile(current, destination/'index.html')
    assets = destination/'web'
    assets.mkdir(exist_ok=True)
    for name in ('theme.js', 'tool-theme.js', 'tool-theme.css'):
        shutil.copyfile(ROOT/'web'/name, assets/name)
    theme_tags = b'<script src="web/theme.js"></script><link rel="stylesheet" href="web/tool-theme.css"><script defer src="web/tool-theme.js"></script>'
    for name, content in raw.items():
        if b'web/tool-theme.css' not in content:
            if b'</head>' not in content:
                raise ValueError(f'Missing HTML head: {name}')
            content = content.replace(b'</head>', theme_tags + b'</head>', 1)
        (destination/name).write_bytes(content)
    for metadata in ('CNAME', '.nojekyll'):
        if (ROOT/metadata).is_file():
            shutil.copyfile(ROOT/metadata,destination/metadata)
    deployed = {p.name for p in destination.iterdir() if p.is_file()}
    for item in catalog['apps']:
        if item['href'] not in deployed:
            raise FileNotFoundError(f"Navigation target missing: {item['href']}")
    forbidden = [p.name for p in destination.iterdir()
                 if p.suffix.lower() in {'.json','.csv','.zip','.py','.log','.md','.gz','.bz2'}]
    if forbidden:
        raise ValueError(f'Raw source/report files exposed in Pages artifact: {forbidden}')
    if (destination/'index.html').read_bytes() != current.read_bytes():
        raise AssertionError('Index must be the current rebuilt Wiki, not historical HTML.')
    return {'files':len(deployed),'html_files':sum(n.endswith('.html') for n in deployed),
            'bytes':sum(p.stat().st_size for p in destination.iterdir() if p.is_file()),
            'excludes_raw_data':True,'latest_site_sha256':hashlib.sha256(raw[RELEASES[-1][0]]).hexdigest()}


def publish(destination: Path):
    if destination.is_symlink():
        raise ValueError('Pages output must not be a symlink')
    destination = destination.resolve()
    if destination == ROOT:
        raise ValueError('Choose a dedicated output directory for the Pages artifact')
    default_output = destination == SITE
    if destination.exists():
        if not destination.is_dir():
            raise ValueError('Pages output must be a directory')
        if not default_output and any(destination.iterdir()):
            raise ValueError('Custom Pages output directory must be empty')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='qaroshi-pages-', dir=destination.parent) as temp:
        staged = Path(temp)/'site'
        stats = stage(staged)
        previous = Path(temp)/'previous'
        if default_output and destination.exists():
            destination.replace(previous)
        try:
            staged.replace(destination)
        except OSError:
            if previous.exists():
                previous.replace(destination)
            raise
    return stats


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Build in a temporary directory to verify without changing _site')
    parser.add_argument('--output',type=Path,default=SITE,help='Output directory (custom paths must be empty)')
    args=parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory(prefix='qaroshi-pages-check-') as t:
            stats=stage(Path(t))
    else:
        stats=publish(args.output)
    print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
