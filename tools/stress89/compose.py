#!/usr/bin/env python3
"""Edition 8.9 semantically delimited full editorial compositions.

This consumes, never rewrites, the frozen 8.8 source ledger. All added
translations are editorial hypotheses, not speaker-ratified meaning matches.
The full 500-case challenge list is kept intact with exact item provenance.
"""
from __future__ import annotations
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from tools.stress88.compose import run as build88, rows

OUT=ROOT/"data/stress89"
STD=ROOT/"data/standard_8"

def readjson(name):
    return json.loads((STD/name).read_text(encoding="utf8"))

def savecsv(path,records):
    assert records
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf8",newline="") as fp:
        writer=csv.DictWriter(fp,fieldnames=list(records[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

def evidence(event,variant):
    """License four full speech acts for one *exact* editorial event frame."""
    p=event["clause"]
    return {
        1:f"sen {p} si.",
        2:f"sen {p} do yano mi-tu shiri-te.",
        3:f"sen {p} ye.",
        4:f"sen {p} he do mi nu sëmi.",
    }[variant]

def consent_action(frame,variant):
    """Independently distinguish requesting permission, refusing and declining an offer."""
    actor,other,action=frame["actor"],frame["other"],frame["action"]
    question=f"{actor} {action}-ho he do {actor} {other}-tu sharoa-te"
    if variant==1:
        return f"sen {question}."
    if variant==2:
        return f"sen yaro {question}, {other} toru «nu.» shiri-te."
    if variant==3:
        return f"sen {actor} {action} do {actor} {other}-tu pëli-te nao {other} noharo-te."
    raise ValueError("Consent scenario variant lacks an editorially licensed structure")

def build():
    build88()
    base=rows(ROOT/"data/stress88/case_evidence_500.csv")
    examples=rows(ROOT/"data/stress81/challenges_500.csv")
    byid={x["id"]:x for x in examples}
    assert len(base)==len(byid)==500
    assert sum(bool(x["qaroshi_full_candidate"]) for x in base)==135
    social=readjson("consent_action_frames_8_9.json")
    events=readjson("evidential_propositions_8_9.json")
    nonassertions=readjson("epistemic_nonassertions_8_9.json")
    motion=readjson("motion_frames_8_9.json")
    misc=readjson("conditional_and_voice_8_9.json")
    assert len(events)==5 and len(motion)==3
    socialmap={x["family"]:x for x in social}
    assert len(socialmap)==8 and len(social)==8
    eventmap={x["family"]:x for x in events}
    nonassertionmap={x["family"]:x for x in nonassertions}
    motionmap={x["family"]:x for x in motion}
    assert len(nonassertionmap)==7
    assert len(eventmap)==5 and len(motionmap)==3
    cfmap={x["daily_family"]:x for x in misc["counterfactuals"]}
    carpenter=misc["additional_voice"]
    insmap={x["voice_family"]:x for x in misc["additional_instruments"]}
    assert len(cfmap)==2 and carpenter["voice_family"]==8 and set(insmap)=={9}
    # Keep the source original English fixed, and never conflate the wrapped
    # proposition with independent assertion of the source event.
    out=[]
    for item in base:
        row=dict(item)
        assert item["english"]==byid[item["id"]]["english"]
        domain=item["domain"]
        fam=int(item["family"])
        variant=int(item["variant"])
        old=item["qaroshi_full_candidate"]
        candidate=None
        witness=[]
        label=None
        boundary=None
        semantic_signature=None
        if domain=="social_consent" and fam in socialmap and variant in (1,2,3):
            sf=socialmap[fam]
            candidate=consent_action(sf,variant)
            witness=[sf["actor_id"],sf.get("actor_base_id"),sf["other_id"],*sf["action_ids"],sf["id"]]
            label="8_9_licensed_permission_request_or_refusal_editorial"
            boundary=sf["boundary"]
            semantic_signature={
                "question_actor":sf["actor"],"permission_addressee":sf["other"],
                "requested_action":sf["action"],"action_already_performed":False,
                "permission_granted_or_inferred":False,
                "kind":"asked_permission" if variant==1 else
                       ("explicit_negative_reply" if variant==2 else "offered_action_then_refused"),
                "negative_reply_did_not_assert_action_failure":True}
        if domain=="evidentiality" and fam in eventmap and variant in (1,2,3,4):
            ev=eventmap[fam]
            candidate=evidence(ev,variant)
            witness=[ev["actor_id"],ev["verb_id"],ev.get("patient_id"),ev["id"]]
            label="8_9_evidential_editorial_composition"
            boundary=ev["boundary"]
            semantic_signature={
                "event":ev["english_event"],"event_content_asserted":variant==1,
                "source":"speaker_witness" if variant==1 else
                    ("specific_indefinite_person_told_speaker" if variant==2 else
                     ("speaker_inference" if variant==3 else "unknown_polar_content")),
                "matrix_polar_knowledge_negated":variant==4,
                "embedded_event_entailed":False if variant in (2,4) else None}
        if domain=="evidentiality" and variant==5 and fam in nonassertionmap:
            n=nonassertionmap[fam]
            candidate=f"sen {n['event_clause']} do mi nu shërawëhu."
            witness=n["source_ids"]+[n["id"]]
            label="8_9_explicit_negative_claim_scope_editorial"
            boundary=n["boundary"]
            semantic_signature={
                "underlying_english_alternative":n["alternative"],
                "matrix_reporting_negated":True,
                "embedded_event_asserted":False,
                "embedded_event_negated":False,
                "claim_act_asserted":False,
                "speaker_position_on_event_truth":"unspecified"}
        if domain=="time_motion" and fam in motionmap:
            mo=motionmap[fam]
            candidate=mo["candidates"].get(str(variant))
            if candidate:
                witness=[mo["actor_id"],mo["object_id"],mo["event_verb_id"],
                         mo.get("related_actor_id"),mo.get("related_verb_id"),
                         mo.get("boundary_actor_id"),mo.get("boundary_verb_id"),mo["id"]]
                label="8_9_temporal_two_event_editorial"
                boundary=mo["scope_limits"]
                semantic_signature={
                    "before_after_while_question":variant,
                    "matrix_question":variant==5,
                    "matrix_event_asserted":variant!=5,
                    "unmentioned_event_causation":False,
                    "negative_until_implication_promoted":False}
        if domain=="daily" and variant==5 and fam in cfmap:
            cf=cfmap[fam]
            assert byid[item["id"]]["english"]==cf["english"]
            candidate=cf["qaroshi"]
            witness=cf["source_ids"]+[cf["id"]]
            label="8_9_past_counterfactual_editorial"
            boundary=cf["limit"]
            semantic_signature={
                "antecedent":cf["antecedent"],"consequent":cf["consequent"],
                "antecedent_nonactual":True,
                "consequent_asserted_actual":False,
                "coindexed_object":cf.get("anaphoric_identity")}
        if domain=="voice_valency" and fam==carpenter["voice_family"]:
            candidate=carpenter["candidates"].get(str(variant))
            if candidate:
                witness=carpenter["source_ids"]+[carpenter["id"]]
                label="8_9_carpenter_active_passive_editorial"
                boundary=carpenter["limit"]
                semantic_signature={
                    "actor":carpenter["actor"],"patient":carpenter["patient"],
                    "voice":"passive" if variant in (2,5) else "active",
                    "instrument_unspecified":True,
                    "question":variant==5,
                    "negative":variant==4}
        if domain=="voice_valency" and fam in insmap and variant==3:
            ins=insmap[fam]
            candidate=ins["qaroshi"]
            witness=[ins["instrument_id"],ins["id"]]
            label="8_9_specific_instrument_editorial"
            boundary=ins["limit"]
            semantic_signature={"actor":ins["actor"],"patient":ins["patient"],
                                "instrument":ins["instrument"],
                                "instrument_case":"-shi","passive_agent_case":None}
        row["prior_8_8_candidate"]=old
        row["edition_8_9_candidate_replacement_reason"]=""
        row["edition_8_9_semantic_signature_json"]=""
        row["edition_8_9_specific_witnesses"]=""
        if candidate:
            if old and old != candidate:
                row["edition_8_9_candidate_replacement_reason"] = (
                    "Revised source attribution, lexical frame or event proposition. "
                    "Prior 8.8 draft preserved in prior_8_8_candidate.")
            elif not old:
                row["edition_8_9_candidate_replacement_reason"]="Previously undrafted; new restricted editorial composition."
            row["qaroshi_full_candidate"]=candidate
            row["candidate_status"]=label
            row["witness_ids"]=" | ".join(str(w) for w in witness if w)
            row["editorial_scope_warning"]=boundary
            row["edition_8_9_semantic_signature_json"]=json.dumps(semantic_signature,ensure_ascii=False,sort_keys=True)
            row["edition_8_9_specific_witnesses"]=row["witness_ids"]
        row["external_comprehension"]="not performed"
        row["human_backtranslation"]="not performed"
        row["independently_semantically_verified"]="no"
        out.append(row)
    assert len(out)==500 and len({x["id"] for x in out})==500
    before=sum(bool(x["qaroshi_full_candidate"]) for x in base)
    after=sum(bool(x["qaroshi_full_candidate"]) for x in out)
    truly_added=[x for x in out if not x["prior_8_8_candidate"] and x["qaroshi_full_candidate"]]
    replaced=[x for x in out if x["prior_8_8_candidate"] and x["prior_8_8_candidate"]!=x["qaroshi_full_candidate"]]
    assert before==135 and after==before+len(truly_added)
    assert all(x["independently_semantically_verified"]=="no" for x in out)
    report={
      "edition":"Qaroshi 8.9 editorial full-expression coverage, not independent comprehension",
      "challenge_count":500,
      "previous_8_8_editorial_candidates":before,
      "new_8_9_editorial_candidates":len(truly_added),
      "total_8_9_editorial_candidates":after,
      "challenges_still_without_full_draft":500-after,
      "existing_drafts_revised_not_counted_as_new":len(replaced),
      "new_by_domain":dict(sorted(Counter(x["domain"] for x in truly_added).items())),
      "new_candidate_ids":[x["id"] for x in truly_added],
      "revised_candidate_ids":[x["id"] for x in replaced],
      "independent_human_comprehension":0,
      "independent_human_backtranslations":0,
      "all_challenges_solved":False,
      "old_baselines_unchanged":True,
      "warning":"Even complete editorial candidates are not established truth-condition equivalents without external review. Neither missing candidates nor parser abstentions prove Qaroshi cannot express the target."
    }
    OUT.mkdir(parents=True,exist_ok=True)
    savecsv(OUT/"case_evidence_500.csv",out)
    (OUT/"composition_summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return report

if __name__=="__main__":
    print(json.dumps(build(),ensure_ascii=False,indent=2))
