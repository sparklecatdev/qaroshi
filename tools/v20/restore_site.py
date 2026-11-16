#!/usr/bin/env python3
"""Recover the byte-identical Qaroshi 20 offline HTML from the compressed repo asset."""
import gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
output=ROOT/'Qaroshi_20_Speech_Studio.html'
packed=ROOT/'Qaroshi_20_Speech_Studio.html.gz'
manifest=json.loads((ROOT/'data/v20/release_manifest.json').read_text(encoding='utf8'))
expected=manifest.get('site_html_sha256')
if not expected:
 print('Missing verified site HTML checksum; refusing unverified restoration',file=sys.stderr);sys.exit(2)
if output.exists() and hashlib.sha256(output.read_bytes()).hexdigest()==expected:
 print('Already verified',output);sys.exit(0)
if not packed.exists():
 print('No compressed site archive; run python tools/v20/build_release.py',file=sys.stderr);sys.exit(2)
body=gzip.decompress(packed.read_bytes());sha=hashlib.sha256(body).hexdigest()
if sha!=expected:raise RuntimeError(f'HTML hash mismatch: expected {expected}, got {sha}')
output.write_bytes(body)
print('Restored and verified',output, len(body),'bytes')
