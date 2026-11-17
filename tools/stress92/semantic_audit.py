#!/usr/bin/env python3
"""Independent *structural* audit of all 500 existing 9.1 editorial proposals.

No English-to-Qaroshi string from the generator is used as the gold answer.
Each separate case is checked against its own speech-act feature, tense/voice
morphology, role preservation, and evidence source. A pass is NOT evidence that
unrelated humans recover that English meaning or find it idiomatic.
"""
from __future__ import annotations
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.stress91.compose import build as build91,rows
from tools.stress92.heldout import write,OUT

CORE=ROOT/"data/stress81/challenges_500.csv"
PRIOR=ROOT/"data/stress91/case_evidence_500.csv"
OVERLAY=ROOT/"data/standard_8/editorial_lexicon_9_1.json"
CANON=ROOT/"data/lexicon.csv"

# The required meanings come from original independent English feature
# annotations, not from the edition-specific composition functions.
FEATURES={
"daily":["assert_past","negative_past","direct_question","someone_reported_to_me","past_counterfactual"],
"time_motion":["after","before","overlap","negative_until_and_later_real","before_question"],
"social_consent":["permission_question","actual_refusal","declined_offer","silence_not_permission","withdrawal_before_action"],
"quantifier_logic":["every","not_every","none","some","exclusive_only"],
"evidentiality":["speaker_witnessed","someone_told_speaker","speaker_inferred","speaker_ignorant_whether","speaker_does_not_claim_other"],
"embedding_reference":["relative_head","speaker_thinks","speaker_ignorant_whether","conditional_on_relative","because_relative"],
"counterfactual_modal":["counterfactual_not_actual","able_despite_barrier","allowed_despite_barrier","required_despite_barrier","conditional_on_barrier_change"],
"voice_valency":["active_agent_patient","passive_with_agent","tool_instrument","negated_active","passive_question"],
"narrative_figures":["fictional_metaphor","literal_quote","poetic_suggestion","deny_literal_claim","mistaken_then_corrected"],
"technical_precision":["report_says_p","second_observer_recorded_p","possibly_unverified","if_p_then_should","p_not_sufficient_proof_of_q"],
}
assert len(FEATURES)==10
OPEN_RESONANCE={"sen","hë","qor","më","zha","rak","wen","zher","rëm","hol","nëm","dal","sur","khar","lën","yë"}
CASE_MORPH=re.compile(r"-(?:ki|ho|du)-te\b")
REPEATED_CASE=re.compile(r"-(?:m|tu|za|shi|lo|gu|de)-(?:m|tu|za|shi|lo|gu|de)\b")

def outside_quote_segments(q:str)->list[str]:
    """Ignore punctuation and full sentences inside «quoted material»."""
    outer=[]
    depth=0
    for c in q:
        if c=="«":depth+=1;continue
        if c=="»":depth=max(0,depth-1);continue
        if depth==0:outer.append(c)
    return [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", "".join(outer)) if segment.strip()]

def check(row:dict,base:dict,canonical:dict,lexical_overlay:dict)->dict:
    q=row["qaroshi_full_candidate"]
    domain=row["domain"]
    variant=int(row["variant"])
    feature=FEATURES[domain][variant-1]
    blockers=[]
    warnings=[]
    if row["english"]!=base["english"]:
        blockers.append("Original English prompt changed")
    if base["feature"]!=row["feature"]:
        blockers.append("Original English transformation label changed")
    if not q:blockers.append("No complete proposed sentence")
    if CASE_MORPH.search(q):blockers.append("Reversed modal-before-tense suffix")
    if REPEATED_CASE.search(q):blockers.append("Repeated case slot")
    if q.count("«")!=q.count("»"):blockers.append("Unbalanced quotation")
    for segment in outside_quote_segments(q):
        if segment.split(" ")[0] not in OPEN_RESONANCE:
            blockers.append("Independent unquoted sentence lacks opening resonance")
    # Consistency of explicit semantic commitments. The operators are checked
    # independently of each original edition's composition implementation.
    must=[]
    if domain=="daily":
        must={1:[],2:[" nu "],3:[" he?"],4:["do yano mi-tu shiri-te"],5:["wënu "," qinë."]}[variant]
    elif domain=="time_motion":
        must={1:["ana "],2:["ëna "],3:["yaro "],4:["torëne "," nu ",". sen ana "],5:["hë ëna "," he?"]}[variant]
    elif domain=="social_consent":
        must={1:["-ho he do "],2:["«nu.»"],3:["noharo-te."],4:["nu shërawë-te."],5:["maho-m hëzhohe-te","maho-m keleyu-te"]}[variant]
    elif domain=="quantifier_logic":
        must={1:["ngënao"],2:["nëgëra"],3:[" nu "],4:[],5:["ngëshi"]}[variant]
    elif domain=="evidentiality":
        must={1:[" si."],2:["do yano mi-tu shiri-te"],3:[" ye."],4:[" he do mi nu sëmi."],5:["do mi nu shërawëhu."]}[variant]
    elif domain=="embedding_reference":
        must={1:[" sha"],2:[" sha"," do mi tëmiro-te."],3:[" sha"," he do mi nu sëmi."],4:["wë "," sha"],5:[" sha"," ro "]}[variant]
    elif domain=="counterfactual_modal":
        must={1:["wënu "," qinë."],2:["-te-ki"],3:["-te-ho"],4:["-te-du"],5:["wë ","-yu"]}[variant]
    elif domain=="voice_valency":
        must={1:["-m "],2:["-za","-li-"],3:["-shi "],4:[" nu "],5:["-za","-li-"," he?"]}[variant]
    elif domain=="narrative_figures":
        must={1:["gëmano"],2:["toru «"],3:["toru «","shërawiwo"],4:["toru «"," nu shërawëhu"],5:["toru «"," sen ana "]}[variant]
    elif domain=="technical_precision":
        must={1:["do zhikasasho shërawëhu-te"],2:["do larëno subali-mi khunikhu-te"],3:["do këraro","nu shërawëhe-li-te"],4:["wë ","-du."],5:["do zotenga nu eri."]}[variant]
    for token in must:
        if token not in q: blockers.append("Missing expected semantic operator: "+repr(token))
    if domain=="daily" and variant==3 and not q.startswith("hë "):
        blockers.append("Past polar question not in direct-question register")
    if domain=="voice_valency" and variant==3 and "-za" in q:
        blockers.append("Instrument confused with passive actor")
    if domain=="evidentiality" and variant==5 and "do mi nu shërawëhu." not in q:
        blockers.append("A negative claim must not be confused with not claiming")
    if domain=="technical_precision" and variant==5 and q.startswith("sen ") and q.count("sen ")<2:
        blockers.append("P-as-fact statement absent before nonentailment claim")
    if domain=="social_consent" and variant==5 and ("-te-ki" not in q):
        blockers.append("Potential event for consent withdrawal not tense-before-modality")
    if domain=="time_motion" and variant==4:
        if ". sen ana " in q:
            part1,part2=q.split(". sen ana ",1)
            # Do not infer later occurrence from negative until alone.
            if not part1.startswith("sen torëne ") or " nu " not in part1:
                blockers.append("Missing event-negation interval")
            if " nu " in part2:
                blockers.append("Positive later occurrence missing")
        else:blockers.append("Negative until requires separately asserted later event")
    if domain=="narrative_figures" and variant in (3,4,5) and "toru «" not in q:
        blockers.append("Literal/quoted proposition lost its attribution")
    # Independently check actual source citations, not merely that an ID is
    # syntactically well formed. An editorial overlay is never speaker proof.
    source_text=row["edition_9_1_source_ids"] or row["witness_ids"]
    witnesses=[s.strip() for s in source_text.split("|") if s.strip()]
    for id_ in witnesses:
        if id_.startswith("Q") and id_ not in canonical:
            blockers.append("Unknown canonical dictionary ID: "+id_)
        elif id_.startswith("X91-") and id_ not in lexical_overlay:
            blockers.append("Unknown 9.1 lexical ID: "+id_)
        elif id_.startswith("X91-") and lexical_overlay[id_].get("status")=="not_adopted":
            blockers.append("Rejected lexical sense used: "+id_)
    if row["edition_9_1_source_ids"]:
        # Detect actual mention of *new* lexical stems in the Qaroshi text,
        # regardless of what an editorial case-data row says it used.
        surface=re.findall(r"[^\s,.;?!«»]+",q)
        for item in lexical_overlay.values():
            if item.get("status")=="not_adopted":continue
            form=item["form"]
            if any(t==form or t.startswith(form+"-") for t in surface):
                if item["id"] not in witnesses:
                    blockers.append("Uncited actually used 9.1 word: "+item["id"])
    # Metadata-derived roles are *consistency tests*, not independently
    # validated English meaning. For inherited older frames the role field
    # may be missing, which itself is a documentation risk, not false meaning.
    signature=row["edition_9_1_semantic_signature_json"] or row["edition_9_0_semantic_signature_json"]
    parsed={}
    if signature:
        try:parsed=json.loads(signature)
        except json.JSONDecodeError:blockers.append("Malformed editorial semantic signature")
    else:
        warnings.append("No modern structured semantic signature: legacy editorial review needed")
    for role in ("actor","patient","instrument","head"):
        value=parsed.get(role)
        if isinstance(value,str) and value and role!="head":
            if value not in q and value+"-" not in q:
                warnings.append("Role "+role+" from editorial metadata not visibly recoverable")
    if row["edition_9_1_source_ids"]:
        warnings.append("New 9.1 editorial senses and case roles have zero independent attestation")
    if domain in ("narrative_figures","technical_precision","embedding_reference","counterfactual_modal"):
        warnings.append("High-scope complexity requires independent literal paraphrase and counterexample review")
    if domain=="social_consent":
        warnings.append("Actual permission and speech-act semantics cannot be certified by string checks")
    return {
        "case_id":row["id"],"domain":domain,"variant":variant,"source_feature":feature,
        "english_target":row["english"],"qaroshi_proposal":q,
        "editorial_origin":row["candidate_status"],
        "blocking_form_issues":json.dumps(sorted(set(blockers)),ensure_ascii=False),
        "nonblocking_review_risks":json.dumps(sorted(set(warnings)),ensure_ascii=False),
        "structural_status":"blocked_review" if blockers else "bounded_form_checks_passed",
        "source_ids":source_text,
        "speaker_comprehension":"not_tested",
        "human_editorial_equivalence":"unadjudicated",
        "independent_backtranslation":"",
        "reviewer_notes":"",
        "certified_translation":"no",
    }

def run()->dict:
    build91()
    original={r["id"]:r for r in rows(CORE)}
    current=rows(PRIOR)
    assert len(current)==len(original)==500
    with CANON.open(newline="",encoding="utf8") as file:
        canonical={r["id"]:r for r in csv.DictReader(file)}
    overlay={r["id"]:r for r in json.loads(OVERLAY.read_text(encoding="utf8"))["entries"]}
    report=[check(r,original[r["id"]],canonical,overlay) for r in current]
    blocked=[x for x in report if x["structural_status"]=="blocked_review"]
    bydomain=Counter(x["domain"] for x in blocked)
    by_risk=Counter()
    for x in report:
        for warning in json.loads(x["nonblocking_review_risks"]):
            by_risk[warning]+=1
    write(OUT/"semantic_review_500.csv",report)
    write(OUT/"editorial_action_queue.csv",[{
        "case_id":x["case_id"],"domain":x["domain"],
        "priority":"structural_blocker" if x["structural_status"]=="blocked_review" else "requires_external_comprehension",
        "issues":x["blocking_form_issues"],"risks":x["nonblocking_review_risks"],
        "editorial_decision":"","independent_reading":"","rater_id":""
    } for x in report])
    summary={
       "scope":"bounded independent structural audit; not independent human semantics",
       "original_cases":500,
       "full_existing_editorial_drafts":500,
       "checked_for_speech_act_by_domain":500,
       "structural_blockers":len(blocked),
       "structural_blocker_case_ids":[x["case_id"] for x in blocked],
       "blockers_by_domain":dict(sorted(bydomain.items())),
       "unresolved_editorial_equivalence":500,
       "human_backtranslations_collected":0,
       "independent_semantic_truth_condition_ratings":0,
       "humans_who_used_qaroshi_without_english":0,
       "risk_categories":dict(by_risk),
       "notes":"A structural pass cannot certify participant role, figurative meaning, selectional restrictions, or human comprehensibility. No failing item is automatically replaced by a guessed expression."
    }
    (OUT/"semantic_review_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return summary

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,indent=2))
