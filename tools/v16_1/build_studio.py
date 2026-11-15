#!/usr/bin/env python3
"""Build self-contained offline Qaroshi 16.1 lexical-transparency review/study app."""
from pathlib import Path
import csv,json,re
ROOT=Path(__file__).resolve().parents[2]

def read_csv(p):
 with (ROOT/p).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
lex=read_csv('data/lexicon.csv')
audit=read_csv('data/v16_1/headword_learnability_audit_16525.csv')
gaps=read_csv('data/v16_1/root_gap_priorities.csv')
core=read_csv('data/v16_1/prioritized_core_1200.csv')
report=json.loads((ROOT/'data/v16_1/audit_report.json').read_text(encoding='utf8'))
assert len(lex)==30000 and len(audit)==16525 and len(core)==1200
payload={'lex':[{'q':x['qaroshi'],'en':x['english'],'pos':x['pos'],'ipa':x['ipa'],'type':x['type']} for x in lex],
 'audit':[{'id':x['id'],'q':x['qaroshi'],'pos':x['part_of_speech'],'en':x['english'],'domain':x['domain'],
           's':x['analysis_status'],'decomp':x['possible_existing_component_sequence'],'alt':x['proposed_transparent_form'],'mod':x['proposed_modifier'],
           'head':x['proposed_head'],'modEn':x['modifier_meaning'],'headEn':x['head_meaning'],
           'primary':x['primary_sense_component_match']=='true','ref':int(x['reference_examples']),
           'orig':int(x['independent_editorial_occurrences']),'anchors':x['grounded_english_anchors'],
           'note':x['rationale']} for x in audit],
 'gaps':[{'concept':x['missing_english_concept'],'role':x['role'],'count':int(x['priority_count']),
          'examples':x['examples']} for x in gaps],
 'roots':[{'q':x['qaroshi'],'en':x['english'],'pos':x['pos'],'ipa':x['ipa'],
           'ref':int(x['example_count']),'orig':int(x['editorial_count']),'reuse':int(x['compounds_using_word'])} for x in core],
 'report':report,'compCount':13379}
template=(Path(__file__).parent/'studio_template.html').read_text(encoding='utf8')
blob=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
out=ROOT/'Qaroshi_16_1_Root_Reform_Studio.html'
out.write_text(template.replace('/*DATA*/','const DATA='+blob+';'),encoding='utf8')
print('Built',str(out),'bytes',out.stat().st_size,'audit',len(audit),'proposals',sum(bool(x['proposed_transparent_form']) for x in audit),'gaps',len(gaps))
