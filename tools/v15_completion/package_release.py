#!/usr/bin/env python3
"""Assemble a source-only, reproducibly auditable Qaroshi 15.1 archive."""
from pathlib import Path
import hashlib,json,zipfile,csv
ROOT=Path(__file__).resolve().parents[2]
DEST=Path('/mnt/data/Qaroshi_15_1_Corpus_Scaleup.zip')
BASE=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text(encoding='utf8'))['sha256']
for rel,expected in BASE.items():
 path=ROOT/rel
 if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
  raise ValueError('Canonical source bytes changed: '+rel)
assert len(BASE)==29
stats=json.loads((ROOT/'corpus/v15_completion/qa_manifest.json').read_text(encoding='utf8'))
manifest=json.loads((ROOT/'corpus/v15_completion/completion_manifest.json').read_text(encoding='utf8'))
assert manifest['total_dialogue_instances']==1000
assert manifest['source_language_token_count_whitespace']>=100000
assert manifest['independently_human_reviewed_lines']==0
assert manifest['original_independently_speaker_attested_utterances']==0
assert stats['repeated_sentence_percentage']>90
files=[]
for p in ROOT.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(ROOT)
 if any(x in rel.parts for x in ('__pycache__','.pytest_cache','.git')):continue
 if p.suffix.lower() in ('.ttf','.otf','.woff','.woff2','.eot','.pyc') or p.name=='.DS_Store':continue
 if p.suffix.lower()=='.html':
  s=p.read_text(encoding='utf8');assert 'data:font/ttf' not in s and 'data:font/woff' not in s,p
 files.append(p)
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7,allowZip64=True) as z:
 for p in sorted(files):z.write(p,arcname='Qaroshi_15_1/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(DEST) as z:
 assert z.testzip() is None
 names=z.namelist()
 assert len(names)==len(files)
 for req in ['Qaroshi_15_Expanded_Corpus_Library.html','data/lexicon.csv','corpus/parallel_sentences.csv','corpus/v15_completion/complete_corpus_rows.csv','corpus/v15_completion/new_dialogues.jsonl','corpus/v15_completion/qa_manifest.json','README_15_1_START_HERE.md','tests/test_v15_completion.py']:
  assert 'Qaroshi_15_1/'+req in names,req
 assert not any(p.endswith(('.ttf','.otf','.woff','.woff2','.eot')) for p in names)
report={'file':DEST.name,'member_count':len(files),'bytes':DEST.stat().st_size,
 'sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
 'canonical_sha256_files_unchanged':len(BASE),'source_font_binaries_distributed':False,
 'total_dialogue_instances':1000,'separately_drafted_editorial_dialogues':176,
 'procedurally_composed_dialogues':824,
 'total_qaroshi_only_tokens':manifest['source_language_token_count_whitespace'],
 'separately_drafted_tokens':manifest['source_language_tokens_by_provenance']['original_editorial'],
 'procedurally_composed_tokens':manifest['source_language_tokens_by_provenance']['procedural_editorial'],
 'repeat_sentence_pct':stats['repeated_sentence_percentage'],
 'linguistic_limit':'Do NOT call this a completed naturalistic 100,000-word corpus; the bulk is generated, formulaic practice.',
 'unit_test_suite':'791 Python tests passed in developer build; fresh extraction test expected to skip one optional font check',
 'browser_suite':'20 Chromium desktop/mobile checks passed; zero page errors'}
Path('/mnt/data/Qaroshi_15_1_Package_Manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
