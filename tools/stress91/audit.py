#!/usr/bin/env python3
"""Produce the COMPLETE original 500-item blinded comprehension/review packet.

Machine-checking grammar can catch some violations; it cannot establish an
accurate English translation or independent usage. Scores remain blank until
real respondents who have not seen the English originals are recruited.
"""
from __future__ import annotations
import csv,hashlib,json,re,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.stress91.compose import build,rows,OUT,STD
from tools.stress90.audit import run as audit90

def write(path,lines):
    assert lines
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf8") as fp:
        writer=csv.DictWriter(fp,fieldnames=list(lines[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(lines)

def flags(row,source_lex,overlay_lex):
    q=row["qaroshi_full_candidate"]
    issues=[]
    if not q:issues.append("no whole-proposition editorial draft")
    if not q.startswith(("sen ","hë ","qor ","më ","zha ","rak ","wen ","zher ","rëm ","hol ","nëm ","dal ","sur ","khar ","lën ","yë ")):
        issues.append("independent sentence lacks opening resonance")
    if "«" in q and "»" not in q:issues.append("unclosed quotation")
    if "toru «" in q and "toru «sen " not in q and "toru «nu.»" not in q:
        issues.append("verbatim full-sentence quote may lack its own resonance")
    for witness in row["edition_9_1_source_ids"].split(" | "):
        if witness.startswith("Q") and witness not in source_lex:
            issues.append("unknown canonical source "+witness)
        if witness.startswith("X91-") and (witness not in overlay_lex or
                overlay_lex[witness].get("status")=="not_adopted"):
            issues.append("invalid 9.1 lexical overlay source "+witness)
    # Explicitly flag an inherited editorial morphology that puts a modal
    # before tense. Preserve inherited strings for traceability, and do not
    # mistake 'no basic flag' for independent semantic correctness.
    if re.search(r"-(?:ki|ho|du)-te\b",q):
        issues.append("Modal precedes tense; authoritative order is root-voice-tense-aspect-modal")
    d=row["domain"];v=int(row["variant"])
    if d=="time_motion" and v==4:
        if not (q.startswith("sen torëne ") and ". sen ana " in q and " nu " in q):
            issues.append("not-until lacks negative interval plus real later event")
    if d=="social_consent" and v==5 and not ("maho-m hëzhohe-te." in q and
                                               "maho-m keleyu-te." in q):
        issues.append("earlier grant and explicit revocation not separately expressed")
    if d=="evidentiality":
        if v==2 and " do yano mi-tu shiri-te." not in q:
            issues.append("reported source and speaker-recipient insufficiently explicit")
        if v==4 and not q.endswith(" he do mi nu sëmi."):
            issues.append("embedded whether-unknown scope incomplete")
        if v==5 and not q.endswith(" do mi nu shërawëhu."):
            issues.append("nonassertion matrix predicate missing")
    if d=="voice_valency" and v==3:
        if "-shi" not in q:issues.append("physical tool case -shi missing")
        if "-za" in q:issues.append("instrument confused with agent -za")
    if d=="technical_precision" and v==5 and " do zotenga nu eri." not in q:
        issues.append("blocked inference not expressed")
    if d=="embedding_reference" and " sha" not in q:
        issues.append("head-gap boundary absent")
    return issues

def run():
    audit90()
    coverage=build()
    data=rows(OUT/"case_evidence_500.csv")
    with (ROOT/"data/lexicon.csv").open(encoding="utf8",newline="") as fp:
        canonical={r["id"]:r for r in csv.DictReader(fp)}
    lex=json.loads((STD/"editorial_lexicon_9_1.json").read_text(encoding="utf8"))
    overlay={r["id"]:r for r in lex["entries"]}
    assert len(data)==500 and all(x["qaroshi_full_candidate"] for x in data)
    review=[];blind=[];key=[]
    for row in data:
        id_=row["id"]
        issues=flags(row,canonical,overlay)
        signature=row["edition_9_1_semantic_signature_json"] or row["edition_9_0_semantic_signature_json"]
        # An older candidate can precede these overlays, with meaning
        # constraints captured in older status and warning columns.
        review.append({
            "case_id":id_,"domain":row["domain"],"variant":row["variant"],
            "original_english":row["english"],"editorial_qaroshi":row["qaroshi_full_candidate"],
            "draft_origin":"9.1" if row["edition_9_1_source_ids"] else "9.0_or_earlier",
            "source_ids":row["edition_9_1_source_ids"] or row["witness_ids"],
            "semantic_source_signature":signature,
            "required_semantic_factors":row["required_semantic_factors"],
            "editorial_limits":row["editorial_scope_warning"],
            "automatic_form_flags":json.dumps(issues,ensure_ascii=False),
            "automated_check_result":"form_flagged" if issues else "no_basic_form_flag_NOT_certified",
            "independent_semantic_equivalence":"not_tested",
            "human_backtranslation":"not_collected",
            "independent_reader_count":"0",
            "researcher_decision":"","researcher_notes":"",
            "human_readers_claimed":"no"
        })
        packet="ABC"[hashlib.sha256(("qaroshi-91-blind/"+id_).encode()).digest()[0]%3]
        blind.append({
            "case_id":id_,"packet":packet,
            "qaroshi_only":row["qaroshi_full_candidate"],
            "instructions":"Without viewing the English key: write a literal English interpretation; identify who did what, temporal sequence, negation scope, evidence source, objects and uncertainty. Record anything you cannot resolve.",
            "participant_id":"","consent_to_test":"","reader_english":"","uncertain_elements":"","reader_confidence":""
        })
        key.append({
            "case_id":id_,"packet":packet,
            "target_english":row["english"],
            "required_semantic_components":row["required_semantic_factors"],
            "prior_context":"none",
            "role_reference_rubric":"Actor/patient/reference identities must agree",
            "time_rubric":"Event order, past time, relative time, counterfactual must agree",
            "polarity_rubric":"Affirmed/negated/question/reported/unknown/hypothetical must agree",
            "source_rubric":"Who knows, saw, inferred, reported or merely considered must agree",
            "nonentailment_rubric":"No new cause, guilt, actual consent, physical literal miracle or factual Q",
            "rater_id":"","rater_score":"","rater_notes":""
        })
    assert len(review)==len(blind)==len(key)==500
    assert {x["case_id"] for x in blind}=={x["case_id"] for x in key}
    write(OUT/"formal_review_500.csv",review)
    write(OUT/"blind_qaroshi_500.csv",blind)
    write(OUT/"private_reviewer_english_key_500.csv",key)
    new=[x for x in review if x["draft_origin"]=="9.1"]
    flagged=[x for x in review if x["automated_check_result"]=="form_flagged"]
    summary={
        "frozen_original_items":500,
        "all_have_full_editorial_candidates":True,
        "original_9_0_or_earlier_candidates_preserved":318,
        "new_9_1_editorial_candidates":len(new),
        "untranslated_items_at_editorial_draft_stage":0,
        "cases_with_basic_form_flags":len(flagged),
        "flagged_case_ids":[x["case_id"] for x in flagged],
        "automated_checks_are_not_semantic_certification":True,
        "independent_human_backtranslations":0,
        "independent_comprehension_trials":0,
        "independent_english_equivalence_decisions":0,
        "has_blind_reading_material_for_all_500":True,
        "private_english_key_separate_from_blind_packet":True,
        "remaining_obligation":"Every candidate requires independent meaning/comprehension validation, including 318 inherited drafts"
    }
    (OUT/"review_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    return summary

if __name__=="__main__":
    print(json.dumps(run(),indent=2,ensure_ascii=False))
