#!/usr/bin/env python3
"""Edition 9.0: source-separated formal audit and ready-to-run blind reading.

Re-running a generator does not reproduce a human interpretation. All review
and participant fields start empty; machine pattern matching is not semantics.
"""
from __future__ import annotations
import csv,hashlib,json,sys
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from tools.stress90.compose import build,rows,OUT
from tools.stress89.audit import run as audit89

def write(path,records):
    assert records
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf8",newline="") as fp:
        w=csv.DictWriter(fp,fieldnames=list(records[0]),lineterminator="\n")
        w.writeheader();w.writerows(records)

def structural_flags(r):
    q=r["qaroshi_full_candidate"]
    if not q:return ["no full draft"], "no_candidate"
    flags=[]
    if not q.startswith(("sen ","hë ","qor ","më ","zha ","rak ","wen ","zher ","rëm ","hol ","nëm ","dal ","sur ","khar ","lën ","yë ")):
        flags.append("No recognized sentence-initial resonance")
    # Multi-sentence Qaroshi: every new sentence begins with a new register.
    sentences=[x.strip() for x in q.split(".") if x.strip()]
    # Do not split nested quotes, only catch obvious positive cases.
    if " toru «" not in q:
        for x in sentences:
            if x and not x.startswith(("sen ","hë ","qor ","më ","zha ","rak ","wen ","zher ","rëm ","hol ","nëm ","dal ","sur ","khar ","lën ","yë ")):
                flags.append("Some independent sentence may lack its own resonance")
                break
    domain=r["domain"];v=int(r["variant"])
    if domain=="evidentiality":
        if v==1 and not q.endswith(" si."):
            flags.append("Direct-witness marker absent or misplaced")
        if v==2 and (" do yano mi-tu shiri-te" not in q):
            flags.append("Reported-speech source and recipient not both explicit")
        if v==4 and not q.endswith(" he do mi nu sëmi."):
            flags.append("Embedded polar unknown-scope not explicit")
        if v==5 and " nu shërawëhu." not in q:
            flags.append("Matrix nonassertion unmarked")
    if domain=="social_consent":
        if v==1 and not q.endswith(" sharoa-te."):
            flags.append("Ask/permission outer event not explicit")
        if v==2 and "«nu.»" not in q:
            flags.append("Actual refusal quote unexpressed")
        if v==3 and " noharo-te." not in q:
            flags.append("Decline event missing")
        if v==4 and " nu shërawë-te." not in q:
            flags.append("Refusal to infer permission absent")
        if v==5 and " maho-m keleyu-te." not in q:
            flags.append("Withdrawal event absent")
    if domain=="technical_precision":
        if v==1 and " zhikasasho shërawëhu-te." not in q:
            flags.append("Named report source missing")
        if v==3 and " tequyu nu shërawëhe-li-te." not in q:
            flags.append("Explicit lack of independent verification missing")
        if v==4 and "-du." not in q:
            flags.append("Recommendation modality absent")
        if v==5 and " zotenga nu eri." not in q:
            flags.append("Inference nonentailment absent")
    if domain=="embedding_reference":
        if " sha" not in q:
            flags.append("Relative head-gap boundary absent")
        if v==2 and not q.endswith(" do mi tëmiro-te."):
            flags.append("Think scope absent")
        if v==3 and not q.endswith(" he do mi nu sëmi."):
            flags.append("Unknown-embedded-polar scope absent")
    if domain=="voice_valency" and v in (2,5) and not ("-li-" in q and "-za" in q):
        flags.append("Passive actor/voice contrast incomplete")
    if flags:return flags,"needs_editorial_structural_review"
    return [],"preliminary_form_check_passed_NOT_meaning_certification"

def run():
    audit89()
    report90=build()
    ledger=rows(OUT/"case_evidence_500.csv")
    inherited=rows(ROOT/"data/stress89/case_evidence_500.csv")
    assert len(ledger)==500 and len(inherited)==500
    assert sum(bool(r["qaroshi_full_candidate"]) for r in inherited)==190
    inherited_ids={r["id"] for r in inherited if r["qaroshi_full_candidate"]}
    no_old={r["id"] for r in ledger if r["edition_9_0_witness_ids"]}
    assert not inherited_ids.intersection(no_old)
    reviews=[];blind=[];key=[];missing=[]
    for r in ledger:
        q=r["qaroshi_full_candidate"];id_=r["id"]
        flags,status=structural_flags(r)
        if not q:
            missing.append({
                "id":id_,"domain":r["domain"],"variant":r["variant"],"english":r["english"],
                "semantic_components_required":r["required_semantic_factors"],
                "why_unresolved":"No documented whole-proposition, all-role license yet. Must check original English against canonical lexical senses, reference, modality and scope.",
                "needs_attested_speaker_review":"yes",
                "proven_inexpressible_in_qaroshi":"no"
            })
        reviews.append({
            "id":id_,"domain":r["domain"],"source_edition":"8.9_or_earlier" if id_ in inherited_ids else "9.0",
            "english_target":r["english"],
            "qaroshi_candidate":q,
            "specific_semantic_requirements":r["required_semantic_factors"],
            "canonical_sources":r["witness_ids"],
            "candidate_risks":r["editorial_scope_warning"],
            "automatic_structural_flags":json.dumps(flags,ensure_ascii=False),
            "formal_check_not_human":status,
            "independent_backtranslation_status":"not undertaken",
            "external_reader_count":"0",
            "semantic_equivalence_decision":"unadjudicated",
            "reviewer_name":"","reviewer_notes":"",
            "attestation_claim":"none"
        })
        if not q:continue
        packet="ABC"[hashlib.sha256(("Qaroshi90/isolated/"+id_).encode()).digest()[1]%3]
        blind.append({
            "case_id":id_,"packet":packet,
            "qaroshi_only":q,
            "instruction":"Read without the English original. Render literal English, actors, patients, temporal order, negation scope, evidence, uncertainty and any parts not understood.",
            "human_translation":"","uncertain_parts":"","reader_consent":"","reader_id":""
        })
        key.append({
            "case_id":id_,"packet":packet,
            "original_english":r["english"],
            "required_semantic_components":r["required_semantic_factors"],
            "candidate_source_edition":"8.9_or_earlier" if id_ in inherited_ids else "9.0",
            "editorial_warning":r["editorial_scope_warning"],
            "independent_rater_score":"","rater_reasoning":"","rater_id":""
        })
    assert len(reviews)==500
    assert len(blind)==len(key)==report90["total_editorial_drafts"]
    assert len(missing)==report90["remaining_no_complete_draft"]
    assert len([r for r in reviews if r["source_edition"]=="8.9_or_earlier" and r["qaroshi_candidate"]])==190
    write(OUT/"formal_review_500.csv",reviews)
    write(OUT/"blind_qaroshi_only.csv",blind)
    write(OUT/"private_english_answer_key.csv",key)
    write(OUT/"unresolved_cases.csv",missing)
    result={
      "all_stimuli_preserved":500,
      "inherited_editorial_candidates_formally_reviewed":190,
      "all_current_candidate_prompts_blinded":len(blind),
      "still_no_full_draft":len(missing),
      "formal_check_counts":dict(sorted(Counter(r["formal_check_not_human"] for r in reviews).items())),
      "human_backtranslations_collected":0,
      "independent_comprehension_trials":0,
      "independent_semantic_equivalence_decisions":0,
      "blind_key_separated":True,
      "speaker_comprehension_claimed":False,
      "no_content_invented_for_unresolved":True
    }
    (OUT/"audit_summary.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    return result

if __name__=="__main__":
    print(json.dumps(run(),indent=2,ensure_ascii=False))
