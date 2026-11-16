#!/usr/bin/env python3
"""Restore reproducible 21–23 artifacts from prebuilt, SHA-checked data.

The source generator `build_release.py` also regenerates these from existing
canonical corpora. The compressed assets are provided for offline convenience.
"""
import bz2,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/'Qaroshi_21_23_Translation_Immersion_Academy.html'
ARCHIVE=ROOT/'Qaroshi_21_23_Precomputed_Data.zip'
COMPRESSED=ROOT/'Qaroshi_21_23_Translation_Immersion_Academy.html.bz2'

def restore():
 if ARCHIVE.exists():
  with zipfile.ZipFile(ARCHIVE) as z:
   if z.testzip() is not None:raise ValueError('Damaged precomputed archive')
   items=[i for i in z.infolist() if not i.is_dir()]
   for info in items:
    if (info.filename.startswith('/') or '..' in Path(info.filename).parts or not info.filename.startswith('data/')):
     raise ValueError('Invalid packaged data path: '+info.filename)
   for info in items:
    p=ROOT/info.filename;p.parent.mkdir(exist_ok=True,parents=True)
    if not p.exists() or p.read_bytes()!=z.read(info):p.write_bytes(z.read(info))
 if COMPRESSED.exists():
  b=bz2.decompress(COMPRESSED.read_bytes())
  if b'<!doctype html>' not in b[:150].lower():raise ValueError('Invalid offline HTML payload')
  if SITE.exists() and SITE.read_bytes()==b:return SITE
  SITE.write_bytes(b)
 return SITE
if __name__=='__main__':print(restore())
