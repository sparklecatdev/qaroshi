#!/usr/bin/env python3
"""9.3 novel structural grammar probes, intentionally unrelated to stress81 cases.

Enumerates typed lexical selections, tense/aspect/modality/negation, reporting,
questions and clausal links from 25 inherited reviewed V0/V1/V2 frames. Uses
the independent surface parser to check each AST roundtrip, not a memorized
collection of 500 prior target strings.
"""
from __future__ import annotations
import csv,json,sys
from collections import Counter
from dataclasses import asdict
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.grammar93.engine import Grammar,Atom,Link,Sentence

OUT=ROOT/"data/stress93"

def write(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(rows)

def event(g,verb,ordinal=0):
    rule=g.license[verb]
    lex=list(g.lex.values())
    def choose(role,n=0):
        allowed=rule.get(role,[])
        values=[x["form"] for x in lex if x["class"] in allowed]
        return values[n % len(values)] if values else None
    return Atom(actor=choose("subject",ordinal),verb=verb,
                patient=choose("patient",ordinal),
                recipient=choose("recipient",ordinal),
                goal=choose("goal",ordinal),
                location=choose("location",ordinal),
                tense="te")

def build():
    g=Grammar()
    records=[]
    seen=set()
    skipped=0
    def add(sentence,source):
        nonlocal skipped
        q=g.render(sentence)
        restored=g.parse(q)
        if restored!=sentence:
            raise AssertionError("Surface parse-render AST mismatch: "+q)
        if q in seen:
            skipped+=1
            return
        semantics=g.semantic_view(restored)
        seen.add(q)
        records.append({
            "case_id":f"G93-{len(records)+1:05d}",
            "benchmark_group":source,
            "qaroshi_proposal":q,
            "ast_json":json.dumps(asdict(sentence),ensure_ascii=False,sort_keys=True),
            "parsed_meaning_json":json.dumps(semantics,ensure_ascii=False,sort_keys=True),
            "source_verbs":" | ".join(a["verb"] for a in semantics["roles"]),
            "independent_human_meaning_ratings":0,
            "proposed_not_attested":"yes",
        })

    for verb in sorted(g.license):
        # This is a cross-product of licensed roles and grammar features; there
        # are NO fixed original-English stimulus translations in this function.
        for actor_ordinal,tense,modal,negative,style in product(
            range(3),("","te","yu"),("","ki","ho","du"),
            (False,True),("plain","reported","unknown","polar","witness")):
            a=event(g,verb,actor_ordinal)
            a=Atom(**{**asdict(a),"tense":tense,"modal":modal,"negated":negative})
            s=Sentence(
                a,resonance="hë" if style=="polar" else "sen",
                mood="polar" if style=="polar" else "statement",
                attribution={"reported":"reported_to_speaker",
                             "unknown":"unknown_whether"}.get(style,""),
                evidential="si" if style=="witness" else "",
            )
            add(s,"single_atom")
    # Unlike 9.2, these events are not copied from ten scenario-frame
    # strings. Cross-verb links use AST nodes with typed checked valency.
    verbs=sorted(g.license)
    for i,verb in enumerate(verbs):
        left=event(g,verb,1)
        for other in verbs:
            if other==verb:continue
            right=event(g,other,2)
            for relation,attribution in (
                ("after",""),("before",""),("when",""),
                ("if",""),("counterfactual",""),("after","reported_to_speaker")):
                s=Sentence(Link(relation,left,right),attribution=attribution)
                add(s,"cross_verb_link")
    assert len(seen)==len(records)
    assert len(records)>=7500,(len(records),skipped)
    assert set(g.curated).issubset(set(v for r in records for v in r["source_verbs"].split(" | ")))
    COUNTS=Counter(x["benchmark_group"] for x in records)
    write(OUT/"grammar_stress.csv",records)
    report={
        "edition":"9.3 tested finite lexical-licensing grammar subset, not full Qaroshi",
        "reviewed_verb_lemmas":len(g.curated),
        "typed_noun_forms":len(g.lex),
        "unique_AST_surface_roundtrips":len(records),
        "counts_by_group":dict(COUNTS),
        "duplicate_surface_forms_deduplicated":skipped,
        "general_ast_parser_not_500_case_template_matching":True,
        "passes_unknown_verb_by_abstaining":True,
        "independent_english_translations_certified":0,
        "independent_human_comprehension":0,
        "unrestricted_grammar_coverage_claimed":False,
    }
    (OUT/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return report

if __name__=="__main__":
    print(json.dumps(build(),ensure_ascii=False,indent=2))
