#!/usr/bin/env python3
"""Standard 9.4: complete independent-*source* semantic requirements for 500.

190 earlier proposals lack comparably structured contemporary annotations.
We backfill these from the ORIGINAL author-controlled English scenario tuples
and explicit features, not by copying or reverse engineering the Qaroshi
candidate. This is source-intent annotation, NOT independent validation of
what Qaroshi readers will interpret.

Canonical 8.0–9.2 sources and previous proposed sentences remain untouched.
"""
from __future__ import annotations
import csv,json,sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.stress81 import scenarios
from tools.stress91.compose import rows
from tools.stress92.semantic_audit import run as run92, FEATURES
from tools.stress92.heldout import write

OUT=ROOT/"data/stress94"
FORMAL=ROOT/"data/stress92/semantic_review_500.csv"
CURRENT=ROOT/"data/stress92/corrected_editorial_500.csv"

TUPLES={
 "daily":scenarios.DAILY,"time_motion":scenarios.MOTION,
 "social_consent":scenarios.SOCIAL,"quantifier_logic":scenarios.LOGIC,
 "evidentiality":scenarios.EVIDENCE,"embedding_reference":scenarios.EMBED,
 "counterfactual_modal":scenarios.COUNTER,"voice_valency":scenarios.VALENCY,
 "narrative_figures":scenarios.NARRATIVE,"technical_precision":scenarios.TECH,
}
assert all(len(v)==10 for v in TUPLES.values())

def source_components(domain:str,raw:tuple)->dict:
    # These roles are copied from ORIGINAL SOURCE STRUCTURED SCENARIOS.
    # They are not assumed present in the draft, and no dictionary gloss
    # or English NLP is used to infer missing argument structure.
    if domain=="daily":
        a,past,bare,part,consequence=raw
        return {"actor":a,"main_action_past":past,"main_action_bare":bare,
                "antecedent_participle":part,"counterfactual_consequence":consequence}
    if domain=="time_motion":
        a,past,bare,other,endpoint=raw
        return {"main_actor":a,"main_event_past":past,
                "main_event_bare":bare,"secondary_event":other,"boundary_event":endpoint}
    if domain=="social_consent":
        a,b,action=raw
        return {"asker_or_action_actor":a,"permission_addressee":b,"proposed_action":action}
    if domain=="quantifier_logic":
        one,many,quality=raw
        return {"singular_domain":one,"plural_domain":many,"tested_property":quality}
    if domain=="evidentiality":
        claim,other=raw
        return {"main_embedded_proposition":claim,"alternative_claim_not_endorsed":other}
    if domain=="embedding_reference":
        head,event,effect,reason=raw
        return {"relative_head_description":head,"matrix_predication":event,
                "conditional_consequence":effect,"causal_explanation":reason}
    if domain=="counterfactual_modal":
        a,base,part,barrier,effect=raw
        return {"modal_actor":a,"uninflected_action":base,
                "past_participle_action":part,"obstacle_proposition":barrier,
                "counterfactual_consequence":effect}
    if domain=="voice_valency":
        a,patient,past,base,part,tool=raw
        return {"agent":a,"patient":patient,"action_past":past,
                "action_bare":base,"passive_participle":part,
                "physical_instrument":tool}
    if domain=="narrative_figures":
        metaphor,interpretation,literal=raw
        return {"quoted_image":metaphor,"literary_suggested_meaning":interpretation,
                "denied_literal_implication":literal}
    if domain=="technical_precision":
        p,recommendation,q=raw
        return {"proposition_p":p,"conditional_recommendation":recommendation,
                "unsupported_conclusion_q":q}
    raise ValueError(domain)

SCOPE={
"daily":[("assert_positive_past",True),("assert_negative_past",False),("ask_direct_polar",None),
         ("attribute_to_unspecified_reporter",None),("past_counterfactual",False)],
"time_motion":[("after_both_actual",True),("before_both_actual",True),("overlap_both_actual",True),
               ("not_until_with_positive_later_event",True),("question_event_order",None)],
"social_consent":[("request_permission_not_grant",None),("explicit_refusal",False),
                  ("offer_and_declined",False),("silence_not_consent",False),
                  ("withdraw_action_specific_past_consent",False)],
"quantifier_logic":[("universal",True),("not_all",True),("none",True),
                    ("existential",True),("exclusive_subject_focus",True)],
"evidentiality":[("speaker_witnessed",True),("someone_told_speaker",None),
                 ("speaker_inferred_not_necessarily_true",None),("speaker_does_not_know_whether",None),
                 ("speaker_explicitly_does_not_claim_alternative",None)],
"embedding_reference":[("assert_relative_head_proposition",True),
                       ("speaker_thinks_p_not_asserted",None),
                       ("speaker_does_not_know_whether_relative_p",None),
                       ("conditional_relative_p_not_asserted",None),
                       ("because_relative_p_and_reason_asserted",True)],
"counterfactual_modal":[("past_counterfactual_no_actual_result",False),
                        ("ability_not_completion",None),("permission_not_ability_or_completion",None),
                        ("obligation_not_completion",None),("barrier_change_conditional_not_fact",None)],
"voice_valency":[("active_patient_asserted",True),("passive_agent_explicit_asserted",True),
                 ("instrument_not_agent",True),("negated_active_event",False),
                 ("passive_agent_polar_question",None)],
"narrative_figures":[("fictional_not_real",False),("narrator_exact_written_quote",None),
                     ("poet_suggested_metaphorical_reading",None),
                     ("deny_literal_entailment",False),("reader_initial_then_corrected",None)],
"technical_precision":[("report_says_p_not_fact",None),("second_observer_recorded_p_not_fact",None),
                       ("possibly_p_without_independent_verification",None),
                       ("conditional_normative_recommendation",None),
                       ("assert_p_but_p_not_proof_of_q",True)],
}

def build()->dict:
    formal_summary=run92()
    original=rows(ROOT/"data/stress81/challenges_500.csv")
    current=rows(CURRENT)
    audit=rows(FORMAL)
    assert len(original)==len(current)==len(audit)==500
    assert set(TUPLES)==set(SCOPE)==set(FEATURES)
    c={r["id"]:r for r in current}
    f={r["case_id"]:r for r in audit}
    structured=[]
    backfilled=[]
    for base in original:
        id_=base["id"]
        domain=base["domain"]
        v=int(base["variant"])
        family=int(base["scenario_family"].split("-")[-1])
        src=TUPLES[domain][family-1]
        row=c[id_]
        review=f[id_]
        assert row["english"]==base["english"]
        assert review["english_target"]==base["english"]
        expect=FEATURES[domain][v-1]
        assert review["source_feature"]==expect
        prior=row.get("edition_9_1_semantic_signature_json") or row.get("edition_9_0_semantic_signature_json")
        earlier=bool(prior)
        source_semantics,real_world_event=SCOPE[domain][v-1]
        source_intent={
           "id":id_,"domain":domain,"family":family,"variant":v,
           "source_feature":base["feature"],"source_operator":expect,
           "source_semantic_scope":source_semantics,
           "proposition_event_assertion":real_world_event,
           "original_english_exact":base["english"],
           "original_role_or_event_components":source_components(domain,src),
           "semantic_roles_are_from_original_english_scenario":True,
           "source_assertion_derived_not_backward_parsed":True,
           "speaker_human_attestation":False,
           "english_to_qaroshi_equivalence":"not verified",
        }
        if domain=="social_consent":
            source_intent.update({
               "implied_permission_from_silence":False,
               "requested_action_occurrence_entailed":False,
               "earlier_specific_grant_and_later_revocation_asserted":v==5,
            })
        if domain=="technical_precision":
            source_intent["unsupported_q_asserted_false"]=False
            source_intent["unsupported_q_proved_by_p"]=False
        if domain=="evidentiality":
            source_intent["embedded_event_negated_by_matrix"]=False
        if domain=="counterfactual_modal":
            source_intent["hypothetical_result_occurred_asserted"]=False
        if domain=="narrative_figures":
            source_intent["literal_metaphor_occurred_in_actual_world"]=False
        if domain=="voice_valency":
            source_intent["instrument_is_agent"]=False
            source_intent["overt_passive_agent_required"]=v in (2,5)
        if domain=="time_motion":
            source_intent["both_events_asserted"]=v in (1,2,3,4)
            source_intent["later_event_asserted_despite_negated_preboundary"]=v==4
        content=json.dumps(source_intent,ensure_ascii=False,sort_keys=True)
        if not earlier:backfilled.append(id_)
        structured.append({
           "id":id_,"domain":domain,"variant":v,"family":family,
           "original_english":base["english"],
           "current_9_2_qaroshi_candidate":row["qaroshi_full_candidate"],
           "source_semantic_intent_json":content,
           "prior_editorial_signature_json":prior or "",
           "signature_source":"9_4_source_backfill" if not earlier else "9_0_or_9_1_plus_9_4_source",
           "scope_operator_9_2_audit":review["structural_status"],
           "scope_issue_json":review["blocking_form_issues"],
           "prior_9_1_original":row["prior_9_1_editorial_candidate"],
           "9_2_versioned_correction_reason":row.get("9_2_correction_reason",""),
           "external_human_paraphrase":"",
           "external_reviewer_id":"",
           "independent_semantic_equivalence":"unadjudicated",
           "authoritative_native_grammar_attestation":"no",
        })
    assert len(structured)==len({r["id"] for r in structured})==500
    assert len(backfilled)==190,("Unexpected prior-modern signature count",len(backfilled))
    assert all(r["scope_operator_9_2_audit"]=="bounded_form_checks_passed" for r in structured), formal_summary
    OUT.mkdir(parents=True,exist_ok=True)
    write(OUT/"source_semantic_requirements_500.csv",structured)
    write(OUT/"legacy_190_backfilled.csv",[r for r in structured if r["signature_source"]=="9_4_source_backfill"])
    write(OUT/"independent_comprehension_review_queue.csv",[{
       "id":r["id"],"domain":r["domain"],"original_english":r["original_english"],
       "qaroshi_candidate":r["current_9_2_qaroshi_candidate"],
       "source_semantic_requirements_json":r["source_semantic_intent_json"],
       "without_english_reader_paraphrase":"","reader_id":"","reviewer_score":"","reviewer_notes":""
    } for r in structured])
    summary={
       "edition":"9.4 source-intent semantic requirements, not independent Qaroshi comprehension",
       "all_frozen_original_challenges_annotated":len(structured),
       "new_source_grounded_missing_signature_backfills":len(backfilled),
       "inherited_9_0_or_9_1_structured_signatures_retained":len(structured)-len(backfilled),
       "all_original_english_strings_preserved":True,
       "all_9_2_editorial_corrections_preserved":formal_summary["versioned_9_2_grammatical_corrections"],
       "source_intent_features":len(SCOPE)*5,
       "frozen_baselines_modified":False,
       "missing_source_intent_records":0,
       "independent_human_paraphrases":0,
       "independently_confirmed_english_qaroshi_equivalences":0,
       "known_9_2_form_blockers":formal_summary["structural_blockers"],
       "language_independent_of_english_proven":False,
       "critical_distinction":"These 190 new structures describe what the original English means. They do not prove that the old Qaroshi sentence encodes that English; blind readers must still validate."
    }
    (OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return summary

if __name__=="__main__":
    print(json.dumps(build(),ensure_ascii=False,indent=2))
