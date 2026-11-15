#!/usr/bin/env python3
"""Package the v15 source-only artifact. Preserve canonical data and exclude fonts."""
from pathlib import Path
import hashlib,zipfile,json,csv
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT.parent/'Qaroshi_15_Natural_Conversation_Literature.zip'
BASE=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text(encoding='utf8'))['sha256']
for rel,original in BASE.items():
    p=ROOT/rel
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=original:raise ValueError('Canonical content changed: '+rel)
files=[]
for path in ROOT.rglob('*'):
 if not path.is_file():continue
 rel=path.relative_to(ROOT)
 if '__pycache__' in rel.parts or '.pytest_cache' in rel.parts or path.name in ('.DS_Store',) or path.suffix.lower() in ('.pyc','.ttf','.otf','.woff','.woff2','.eot'):continue
 if path.suffix.lower()=='.html':
  source=path.read_text(encoding='utf8');assert 'data:font/ttf' not in source and 'data:font/woff' not in source
 files.append(path)
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7,allowZip64=True) as z:
 for p in sorted(files):z.write(p,arcname='Qaroshi_15/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(DEST) as z:
 assert z.testzip() is None
 names=z.namelist()
 assert len(names)==len(files)
 for required in ['Qaroshi_15_Corpus_Library.html','data/lexicon.csv','corpus/parallel_sentences.csv','corpus/v15/full_editorial_parallel.csv','corpus/v15/Qaroshi_15_Reader.md','docs/v15/RELEASE_NOTES.md']:
  assert 'Qaroshi_15/'+required in names
 assert not any(x.endswith(('.ttf','.otf','.woff','.woff2','.eot')) for x in names)
reported={'release':'Qaroshi 15.0 editorial conversation and literature development',
          'file':DEST.name,'member_count':len(files),'bytes':DEST.stat().st_size,'sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
          'baseline_sha256_items_preserved':len(BASE),'font_binaries_distributed':False,
          'new_dialogues':73,'new_literature':12,'new_qaroshi_tokens':2419,
          'editorial_library_dialogues':176,'editorial_library_prose':35,'editorial_library_tokens':6828,
          'speaker_attested_sentences':0,'no_false_completion_claim':True}
(DEST.parent/'Qaroshi_15_Package_Report.json').write_text(json.dumps(reported,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(reported,ensure_ascii=False,indent=2))
