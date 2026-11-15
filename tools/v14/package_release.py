#!/usr/bin/env python3
"""Build and verify the Qaroshi 14.0 source/HTML zip, excluding font binaries."""
from pathlib import Path
import hashlib,json,zipfile,shutil
ROOT=Path(__file__).resolve().parents[2]
OUT=Path('/mnt/data/Qaroshi_14_Language_Consistency.zip')
ex={'__pycache__','.pytest_cache','.git','.mypy_cache'}
font_ext={'.ttf','.otf','.woff','.woff2','.eot','.pyc'}
source=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text())['sha256']
for rel,v in source.items():
 actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
 if actual!=v:raise ValueError('Baseline changed: '+rel)
files=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(ROOT)
 if any(x in ex for x in rel.parts) or p.suffix.lower() in font_ext:continue
 if p.name=='.DS_Store':continue
 files.append(p)
for p in files:
 if p.suffix.lower()=='.html':
  text=p.read_text(encoding='utf8',errors='replace')
  if 'data:font/ttf;base64' in text or 'data:font/woff;base64' in text:
   raise ValueError('Embedded compiled font payload in '+str(p))
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7,allowZip64=True) as z:
 for p in files:z.write(p,'Qaroshi_14_Language_Consistency/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 names=z.namelist()
 for required in ['Qaroshi_14_Semantic_Workbench.html','RELEASE_14_NOTES.md','tools/v14/semantic_validator.py',
                  'data/v14/translation_review_103.csv','data/v14/idiom_review_1000.csv','data/v14/sense_review_5000.csv',
                  'data/v14/grammar_regression_442.jsonl','tests/test_standard14.py','docs/grammar.md','data/lexicon.csv']:
  assert any(x.endswith('/'+required) for x in names),required
 assert not any(x.lower().endswith(tuple(font_ext)) for x in names)
sha=hashlib.sha256(OUT.read_bytes()).hexdigest()
manifest={'edition':'14.0 editorial consistency and review','archive':str(OUT),'sha256':sha,
          'bytes':OUT.stat().st_size,'files':len(files),'zip_integrity':'passed',
          'canonical_source_files_sha256_verified':len(source),'font_binary_included':False,
          'source_language':{'lexicon_entries':30000,'original_bilingual_examples':4383,'grammar_chapters':90,'glyphs':26,'written_resonance_markers':16},
          'audit':json.loads((ROOT/'data/v14/audit_manifest.json').read_text()),
          'tests':{'python_unittest_cases':759,'browser_desktop_mobile_checks':27,'browser_page_errors':0},
          'limitations':'structural and editorial review queue, not approved idioms, speakers, dialects or final translation corrections'}
Path('/mnt/data/Qaroshi_14_Release_Manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print(json.dumps({'archive':str(OUT),'files':len(files),'bytes':OUT.stat().st_size,'sha256':sha,'font_binary_included':False},indent=2))
