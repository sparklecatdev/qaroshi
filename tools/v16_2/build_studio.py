#!/usr/bin/env python3
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'data/v16_2'
def read(p):
 with open(p,encoding='utf8',newline='') as f:return list(csv.DictReader(f))
data={
 'summary':json.loads((D/'review_summary.json').read_text(encoding='utf8')),
 'candidates':read(D/'all_3817_candidates_screened.csv'),
 'roots':read(D/'eight_root_decision_dossiers.csv'),
 'reuse':read(D/'reuse_before_coinage.csv'),
 'derivatives':read(D/'hypothetical_new_root_derivatives.csv'),
 'lessons':read(D/'sixteen_grammar_and_learnability_examples.csv'),
 'dictionary':[{k:x[k] for k in ['qaroshi','english','pos','ipa','type']} for x in read(ROOT/'data/lexicon.csv')]
}
s=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
p=(Path(__file__).parent/'studio_template.html').read_text(encoding='utf8').replace('__DATA__',s)
out=ROOT/'Qaroshi_16_2_Root_Standardization_Studio.html';out.write_text(p,encoding='utf8')
print(out, out.stat().st_size)
