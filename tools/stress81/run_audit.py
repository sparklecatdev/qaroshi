#!/usr/bin/env python3
"""Reproducible conservative evaluation of 500 English composition challenges.

Do not classify the absence of an automatic translation as lack of an expressive
construction in Qaroshi. Each generated string is explicitly labeled by the
existing translator's evidentiary status and the feature under investigation.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/'data/stress81';sys.path.insert(0,str(ROOT/'tools/v21_23'))
from translator import interpret,indices,norm
from scenarios import create
from quantifier_composition import compose

def records(path):
    with path.open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
def save_csv(path,items):
    with path.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,list(items[0]),lineterminator='\n');w.writeheader();w.writerows(items)

def run():
    stimuli=create();all_source,_,english_index,_,_=indices()
    existing={norm(r['english']) for r in all_source}
    assert len(stimuli)==500 and all(norm(s['english']) not in existing for s in stimuli),'Adversarial stimuli must not repeat documented translations'
    output=[]
    for item in stimuli:
        response=interpret(item['english'],direction='to-qr')
        label=response['status']; qr=response['translation'] or ''
        # This field describes *translator output*, never human linguistic correctness.
        if label.startswith('exact documented'):cat='exact_source_match'
        elif label.startswith('provisional constrained'):cat='provisional_builder_output'
        else:cat='abstained'
        candidate=compose(item)
        output.append({**item,'tool_result':cat,'qaroshi_candidate':qr,'tool_warning':' | '.join(response['warnings'][:3]),
                       'normative_compositional_draft':candidate['candidate'] if candidate else '',
                       'draft_basis':candidate['source_lemmas'] if candidate else '',
                       'draft_status':candidate['status'] if candidate else 'no source-licensed compositional draft',
                       'source_exact_match': 'no',
                       'human_checked_semantics':'no',
                       'language_gap_proven':'no; unsupported tooling cannot establish that',
                       'requires_manual_translation_review':'yes'})
    save_csv(DATA/'audit_results_500.csv',output)
    # Baseline controls MUST be known supported source pairs; these are not part
    # of the 500 unseen probes and demonstrate that retrieval actually works.
    canon=[r for r in all_source if r['kind']=='canonical controlled bilingual example' and len(r['english'].split())>=3]
    distinct={};
    for r in canon:
        key=norm(r['english'])
        if key not in distinct:distinct[key]=r
        if len(distinct)>=30:break
    controls=[]
    for r in distinct.values():
        actual=interpret(r['english'],'to-qr');ok=actual['status'].startswith('exact documented')
        controls.append({'source_id':r['id'],'english':r['english'],'qaroshi':actual['translation'] or '',
                         'status':actual['status'],'retrieval_pass': 'yes' if ok else 'no'})
    assert len(controls)==30 and all(r['retrieval_pass']=='yes' for r in controls)
    save_csv(DATA/'positive_controls_30.csv',controls)
    category=Counter(x['tool_result'] for x in output)
    drafted=sum(bool(x['normative_compositional_draft']) for x in output)
    group={d:Counter(x['tool_result'] for x in output if x['domain']==d) for d in sorted({x['domain'] for x in output})}
    report={'edition':'Qaroshi Standard 8.1 stress audit','scope':'English-to-Qaroshi *tool coverage*, not proof of language nonexpressibility',
       'challenges':len(output),'distinct_scenario_families':len({x['scenario_family'] for x in output}),
       'domains':len(group),'novel_vs_all_covered_source_english':True,'positive_known_source_controls':len(controls),
       'positive_controls_passed':sum(x['retrieval_pass']=='yes' for x in controls),
       'translator_results':dict(category),'editorial_rule_based_drafts':drafted,'remaining_without_documented_draft':len(output)-drafted,
       'draft_status':'Constructed from current adopted rules and source lexemes; NOT source-attested or peer-reviewed translations',
       'by_domain':{d:dict(group[d]) for d in sorted(group)},
       'automatically_verified_semantic_equivalence':0,
       'independent_human_comprehension_participants':0,
       'identified_documentation_gap':'Indirect yes/no complement he/do segmentation and matrix-vs-embedded negation not fully specified in current chapter 73',
       'remedial_rule':'Standard 8.1 amendment: he before do = embedded polar operator; he at end = direct matrix question',
       'remaining_work':'Independent adjudication for verb frames, lexical selection, nested reference and naturalness'}
    (DATA/'audit_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
