#!/usr/bin/env python3
"""Evidence-separated review of every 8.8 candidate (not invented human data).

The blind packet contains Qaroshi only. The answer key and English truth-condition
targets are saved separately. Formal structural checks cover restricted patterns;
the rest remain unverified, not automatically promoted to correct translations.
"""
from __future__ import annotations
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from tools.stress88.compose import run as build_88, rows
from tools.stress88.scope import scope as restricted_scope
from tools.stress81.quantifier_composition import compose as quantifier_compose

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"data/stress89"

def write(path,records):
    path.parent.mkdir(parents=True,exist_ok=True)
    assert records
    with path.open("w",encoding="utf8",newline="") as fp:
        writer=csv.DictWriter(fp,fieldnames=list(records[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

def status(item):
    q=item["qaroshi_full_candidate"]
    domain=item["domain"]
    if not q:return "no_candidate",["A complete sentence is absent"]
    issues=[]
    if q.startswith(("sen ","hë ","zher ","më ","wen ","qor ","rëm ","hol ","lën ","shur ","rak ","nëm ","dal ")):
        pass
    else:issues.append("Unrecognized resonance; check source register")
    if item["variant"]=="3" and domain=="daily":
        if not (q.endswith(" he?") and q.startswith("hë ")):
            issues.append("Past-action polar question lacks exact independent question shape")
    if domain=="voice_valency" and int(item["variant"]) in (2,5):
        if "-za " not in q or "-li-" not in q:
            issues.append("Required passive actor or voice absent")
    if item["candidate_status"]=="8_8_specific_actor_patient_voice_license_unverified":
        if restricted_scope(q)["status"]!="licensed_8_8_restricted":
            issues.append("8.8 role checker did not recognize exact licensed frame")
    if item["candidate_status"]=="new_8_8_editorial_full_composition_not_independently_validated":
        if restricted_scope(q)["status"]!="licensed_8_8_restricted":
            issues.append("8.8 narrow scope checker does not recognize this candidate")
    if domain=="quantifier_logic":
        if int(item["variant"])==2 and "nëgëra" not in q:issues.append("Not-all operator missing")
        if int(item["variant"])==3 and "ngënao" not in q:issues.append("Every-not predicate absent")
        if int(item["variant"])==5 and "ngëshi" not in q:issues.append("Exclusive focus missing")
    if domain=="evidentiality" and int(item["variant"])==2:
        # 'Somebody told me P' must include actual telling and recipient, not merely hu.
        if not (" mi-tu " in q and "do" in q and "shiri" in q):
            issues.append("Reported-source grammar does not explicitly identify somebody telling the speaker")
    if domain=="evidentiality" and int(item["variant"])==3:
        if " ye" not in q and "zhëwëra" not in q:
            issues.append("Inferential evidential not present")
    if issues:return "review_flagged",issues
    exact=restricted_scope(q)
    if exact["status"]=="licensed_8_8_restricted":
        return "exact_8_8_structural_model_match_not_semantic_verification",[]
    if domain=="quantifier_logic":
        return "limited_quantifier_rule_check_without_external_comprehension",[]
    return "form_only_not_independently_semantically_checked",[]

def run():
    build_88()
    source=rows(ROOT/"data/stress88/case_evidence_500.csv")
    original={x["id"]:x for x in rows(ROOT/"data/stress81/challenges_500.csv")}
    assert len(source)==len(original)==500
    reviews=[];public=[];answers=[]
    for x in source:
        id_=x["id"]
        qr=x["qaroshi_full_candidate"]
        s,problems=status(x)
        family=x["domain"]
        version="v1"
        # A stable pseudo-random assignment minimizes repeated domain sequence
        # without relying on hidden global state or stochastic test feedback.
        digest=hashlib.sha256(("Qaroshi-89-blind-"+id_).encode()).digest()
        packet="ABC"[digest[0]%3]
        reviews.append({
            "id":id_,
            "domain":family,
            "english_target":original[id_]["english"],
            "qaroshi_candidate":qr,
            "formal_review":s,
            "formal_issues_json":json.dumps(problems,ensure_ascii=False),
            "semantic_requirements":x["required_semantic_factors"],
            "role_or_lexical_sources":x["witness_ids"],
            "editorial_assumptions":x["editorial_scope_warning"],
            "exact_meaning_human_verified":"no",
            "adjudicator": "",
            "adjudication_decision": "",
            "adjudication_notes":"",
            "independent_backtranslation":"",
            "participant_id":"",
            "evidence_of_independent_comprehension":"none",
            "true_translation_certified":"no"
        })
        if not qr:continue
        public.append({
            "id":id_,
            "packet":packet,
            "qaroshi_only_stimulus":qr,
            "task":"Without seeing an English source, translate into natural English. Identify actor, patient, negation, time, source, and any uncertainty. Do not guess unknown words; mark uncertain.",
            "participant_response":"",
            "participant_uncertainty":"",
            "self_reported_fluency":"",
            "informed_consent_record":"",
        })
        answers.append({
            "id":id_,
            "packet":packet,
            "original_english_target":original[id_]["english"],
            "semantic_components":x["required_semantic_factors"],
            "restricted_form_review":s,
            "known_editorial_limit":x["editorial_scope_warning"],
            "reviewer_equivalence_decision":"",
            "reviewer_notes":"",
        })
    assert len(reviews)==500 and len(public)==len(answers)==135
    write(OUT/"all_candidate_form_audit_500.csv",reviews)
    write(OUT/"blind_qaroshi_prompts_135.csv",public)
    write(OUT/"separate_answer_key_135.csv",answers)
    counts=dict(sorted(Counter(x["formal_review"] for x in reviews).items()))
    report={
        "scope":"independent-of-generator structural diagnostic and ready-to-administer blind prompts",
        "all_500_cases_scanned":len(reviews),
        "existing_8_8_candidate_count":len(public),
        "candidate_structural_review_statuses":counts,
        "blind_packets":dict(sorted(Counter(x["packet"] for x in public).items())),
        "external_participants":0,
        "external_responses":0,
        "meaning_independently_validated":0,
        "all_135_human_checked":False,
        "invalid_forms_not_inferred_from_abstention":True,
        "no_public_answer_key_in_blind_packet":True,
        "notes":"Automated checking of known structural properties is not independent human backtranslation. The original English targets remain in separate keys."
    }
    (OUT/"audit_summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return report

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,indent=2))
