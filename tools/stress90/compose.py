#!/usr/bin/env python3
"""Standard 9.0: additive source-controlled editorial compositions and evidence.

Do NOT silently fill a challenge just because a familiar English word is found.
Every newly translated item must have a specific scope-licensed Qaroshi phrase
and source-linked ledger entry. No generated candidate is human certified.
"""
from __future__ import annotations
import csv,json,sys
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.stress89.compose import build as build89,rows
from tools.stress90.consent import compose as consent_compose,semantic_record as consent_semantics
from tools.stress90.relatives import compose as relative_compose,semantics as relative_semantics
from tools.stress90.technical import compose as technical_compose,semantics as technical_semantics
from tools.stress90.modals import compose as modal_compose,semantics as modal_semantics

STD=ROOT/"data/standard_8"
OUT=ROOT/"data/stress90"

def read(name):
    return json.loads((STD/name).read_text(encoding="utf8"))

def save(path,records):
    assert records
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf8",newline="") as fp:
        writer=csv.DictWriter(fp,fieldnames=list(records[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(records)

def proposals():
    consent=read("consent_action_frames_8_9.json")
    relative=read("relative_frames_9_0.json")
    technical=read("technical_propositions_9_0.json")
    modal=read("modal_barrier_frames_9_0.json")
    assert len(consent)==8 and len(relative)==5 and len(technical)==10 and len(modal)==3
    seen={}
    for frame in consent:
        for variant in (4,5):
            id_=f"QS81-{100+(frame['family']-1)*5+variant:04d}"
            source=[frame.get("actor_id"),frame.get("actor_base_id"),frame["other_id"],*frame["action_ids"],frame["id"],"CON90"]
            seen[id_]=dict(
                candidate=consent_compose(frame,variant),
                status="9_0_explicit_no_inferred_consent_or_action_specific_revocation",
                witness=" | ".join(str(x) for x in source if x),
                semantics=consent_semantics(frame,variant),
                caveat=frame["boundary"]+" The prior grant, withdrawal and potential act are not conflated.",
                license="New narrow consent non-inference and revocation temporal scope"
            )
    for frame in relative:
        for variant in range(1,6):
            candidate=relative_compose(frame,variant)
            if candidate is None:continue
            id_=f"QS81-{250+(frame['family']-1)*5+variant:04d}"
            source=[frame["head_id"],*frame["source_ids"],*(
                frame.get("consequence_source_ids",[]) if variant==4 else
                frame.get("reason_ids",[]) if variant==5 else []),frame["id"],"REL90"]
            assert id_ not in seen
            seen[id_]=dict(
                candidate=candidate,
                status="9_0_prenominal_relative_head_gap_with_scoped_matrix",
                witness=" | ".join(str(x) for x in source if x),
                semantics=relative_semantics(frame,variant),
                caveat=" | ".join(frame["lexical_decisions"])+
                    (" | "+frame["conditional_sense"] if variant==4 else
                     " | "+frame["causal_sense"] if variant==5 else ""),
                license="New 9.0 source-specific reference-gap+scope combination"
            )
    for frame in modal:
        for variant in range(1,6):
            candidate=modal_compose(frame,variant)
            id_=f"QS81-{300+(frame['family']-1)*5+variant:04d}"
            # QS81-0336 already has a historical 8.3 candidate. Do not
            # overwrite or count it as new merely because a second form exists.
            if id_=="QS81-0336":
                continue
            assert id_ not in seen
            source=[*frame["action_ids"],*frame["barrier_ids"],
                    *(frame["consequent_ids"] if variant==1 else []),frame["id"],"MOD90"]
            seen[id_]=dict(
                candidate=candidate,
                status="9_0_past_counterfactual_or_barrier_modality_editorial",
                witness=" | ".join(str(x) for x in source),
                semantics=modal_semantics(frame,variant),
                caveat=frame["semantic_decision"]+" | "+frame["boundary"],
                license="9.0 modals and conditional scope; no action or result automatically actual"
            )
    for frame in technical:
        for variant in range(1,6):
            candidate=technical_compose(frame,variant)
            if candidate is None:continue
            id_=f"QS81-{450+(frame['family']-1)*5+variant:04d}"
            assert id_ not in seen
            witness=[*frame["p_ids"],*(frame["recommendation_ids"] if variant==4 else []),
                     *(frame["unsupported_ids"] if variant==5 else []),frame["id"],"TEC90"]
            seen[id_]=dict(
                candidate=candidate,
                status="9_0_technical_reporting_unverified_possibility_or_nonentailment",
                witness=" | ".join(str(x) for x in witness),
                semantics=technical_semantics(frame,variant),
                caveat=frame["decision"]+" | "+frame["risk"],
                license="Technical source+proposition scope, modal recommendation and proof-insufficiency"
            )
    return seen

def build():
    base_summary=build89()
    original=rows(ROOT/"data/stress81/challenges_500.csv")
    previous=rows(ROOT/"data/stress89/case_evidence_500.csv")
    assert len(original)==len(previous)==500
    assert sum(bool(x["qaroshi_full_candidate"]) for x in previous)==190
    original_map={x["id"]:x for x in original}
    proposal_map=proposals()
    out=[]
    for item in previous:
        id_=item["id"]
        assert item["english"]==original_map[id_]["english"]
        row=dict(item)
        row["prior_8_9_candidate"]=item["qaroshi_full_candidate"]
        row["edition_9_0_semantic_signature_json"]=""
        row["edition_9_0_witness_ids"]=""
        row["edition_9_0_license"]=""
        row["edition_9_0_replacement_reason"]=""
        p=proposal_map.get(id_)
        if p is not None:
            if row["qaroshi_full_candidate"]:
                raise AssertionError(f"9.0 overlay would replace 8.9 candidate without specific adjudication: {id_}")
            assert p["candidate"] and p["candidate"].startswith("sen ")
            row["qaroshi_full_candidate"]=p["candidate"]
            row["candidate_status"]=p["status"]
            row["editorial_scope_warning"]=p["caveat"]
            row["witness_ids"]=p["witness"]
            row["edition_9_0_semantic_signature_json"]=json.dumps(p["semantics"],ensure_ascii=False,sort_keys=True)
            row["edition_9_0_witness_ids"]=p["witness"]
            row["edition_9_0_license"]=p["license"]
        row["human_backtranslation"]="not performed"
        row["external_comprehension"]="not performed"
        row["independently_semantically_verified"]="no"
        out.append(row)
    assert len(out)==len({r["id"] for r in out})==500
    assert set(proposal_map)=={x["id"] for x in out if x["edition_9_0_witness_ids"]}
    total=sum(bool(x["qaroshi_full_candidate"]) for x in out)
    assert total==190+len(proposal_map)
    report={
        "edition":"Standard 9.0 editorial draft coverage, NOT independently understood fluency",
        "fixed_challenges":500,
        "original_8_9_editorial_draft_count":190,
        "9_0_new_full_editorial_draft_count":len(proposal_map),
        "total_editorial_drafts":total,
        "remaining_no_complete_draft":500-total,
        "by_domain":dict(sorted(Counter(x["domain"] for x in out if x["edition_9_0_witness_ids"]).items())),
        "new_ids":sorted(proposal_map),
        "unsupported_cases_reported_as_solved":0,
        "independent_human_backtranslations":0,
        "independent_human_comprehension":0,
        "certified_general_language_completeness":False,
        "frozen_baselines_changed":False
    }
    OUT.mkdir(parents=True,exist_ok=True)
    save(OUT/"case_evidence_500.csv",out)
    (OUT/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return report

if __name__=="__main__":
    print(json.dumps(build(),ensure_ascii=False,indent=2))
