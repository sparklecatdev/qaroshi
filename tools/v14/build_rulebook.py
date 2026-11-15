#!/usr/bin/env python3
"""Produce a machine-readable index of documented v14 consistency decisions."""
import re,json,csv,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'data/v14'
md=(ROOT/'docs/v14/FORMAL_DECISIONS.md').read_text(encoding='utf8')
items=[]
for l in md.splitlines():
 if not l.startswith('| D14-'):continue
 cols=[x.strip() for x in l.strip().strip('|').split('|')]
 assert len(cols)==5,(len(cols),l)
 id_,meaning,contrast,source,status=cols
 assert re.fullmatch(r'D14-\d{2}',id_)
 items.append({'decision_id':id_,'interpretation':meaning,'contrastive_example':contrast,
               'source':source,'status':status,'speaker_ratified':False,'human_reviewer':''})
assert len(items)==20,len(items)
(OUT/'decision_register.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
with (OUT/'decision_register.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
checks=['data/lexicon.csv','corpus/parallel_sentences.csv','docs/grammar.md']
checks += sorted('assets/glyphs/'+x.name for x in (ROOT/'assets/glyphs').glob('*.png'))
sums={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in checks}
(OUT/'baseline_sha256.json').write_text(json.dumps({'source_release':'Qaroshi 12–13','sha256':sums,'immutable_check_files':len(checks)},indent=2))
print('rulebook decisions',len(items),'source file checksums',len(checks))
