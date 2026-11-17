#!/usr/bin/env python3
"""Qaroshi 9.1: editorially complete 500-case challenge composition.

This is additive to Standard 9.0 and preserves all 318 earlier source forms
in the historical ledger. Eight noncanonical past+ability forms are explicitly
repaired in this versioned view, with their prior forms retained. Semantic signatures are editorial claims, NOT independent reader
judgments. Each newly added challenge retains explicit participants, content,
tense, polarity, source evidence, and limitation notes.
"""
from __future__ import annotations
import csv,json,sys,re
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.stress90.compose import build as build90,rows
from tools.stress89.compose import evidence as evidence89,consent_action
from tools.stress90.consent import compose as consent90, semantic_record as consent_semantics90
from tools.stress90.relatives import compose as relative90, semantics as relative_semantics90
from tools.stress90.modals import compose as modal90, semantics as modal_semantics90
from tools.stress90.literary import compose as literary90, semantics as literary_semantics90
from tools.stress90.technical import compose as technical90, semantics as technical_semantics90

STD=ROOT/"data/standard_8"
OUT=ROOT/"data/stress91"
BASES={"daily":0,"time_motion":50,"social_consent":100,"evidentiality":200,
       "embedding_reference":250,"counterfactual_modal":300,"voice_valency":350,
       "narrative_figures":400,"technical_precision":450}
EXPECTED={"daily":16,"time_motion":41,"social_consent":10,"evidentiality":23,
          "embedding_reference":28,"counterfactual_modal":35,"voice_valency":5,
          "narrative_figures":18,"technical_precision":6}

def read(name):
    return json.loads((STD/name).read_text(encoding="utf-8"))

def write_csv(path,items):
    assert items
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(items[0]),lineterminator="\n")
        w.writeheader();w.writerows(items)

def challenge_id(domain,family,variant):
    assert domain in BASES and 1<=family<=10 and 1<=variant<=5
    return f"QS81-{BASES[domain]+(family-1)*5+variant:04d}"

def predicate_negative(p):
    """Strict SOV: retain roles, negate only the final finite event."""
    tokens=p.split()
    assert tokens[-1].endswith("-te") and "-te" in tokens[-1], p
    return " ".join(tokens[:-1]+["nu",tokens[-1]])

def everyday(f,v):
    subject,patient,verb=f["actor"],f["patient"],f["verb"]
    p=f"{subject} {patient} {verb}-te"
    if v==1:return f"sen {p}."
    if v==2:return f"sen {predicate_negative(p)}."
    if v==3:return f"hë {p} he?"
    if v==4:return f"sen {p} do yano mi-tu shiri-te."
    if v==5:return f"sen wënu {p}, {f['consequence']} qinë."
    raise ValueError(v)

def motion(f,v):
    p=f["main"];q=f["after"];b=f["before"]
    if v==1:return f"sen ana {p}, {q}."
    if v==2:return f"sen ëna {b}, {p}."
    if v==3:return f"sen yaro {q}, {p}."
    if v==4:
        # English 'not until' commits to a later instance of the action.
        # torëne licenses the negative phase; a second full clause asserts
        # actual crossing/boarding/etc after the SAME endpoint.
        return f"sen torëne {b}, {predicate_negative(p)}. sen ana {b}, {p}."
    if v==5:return f"hë ëna {q}, {p} he?"
    raise ValueError(v)

def evidential(f,v):
    return evidence89(f,v)

def negated_matrix_claim(f):
    return f"sen {f['event_clause']} do mi nu shërawëhu."

def instrument(f):
    return f"sen {f['actor']} {f['patient']}-m {f['instrument']}-shi {f['verb']}-te."

def signature(domain,f,v,generated):
    base={
        "domain":domain,"family":f["family"],"variant":v,
        "new_source_licensed_editorial_frame":f.get("id"),
        "status":"editorial, not independently attested",
        "independent_reader_count":0
    }
    if domain=="daily":
        base.update({"actor":f["actor"],"patient":f["patient"],
                     "actual_positive_event_asserted":v==1,
                     "negated_event_asserted":v==2,
                     "polar_question":v==3,
                     "third_party_report_not_narrator_verified":v==4,
                     "counterfactual_not_actual_outcome":v==5})
    elif domain=="time_motion":
        base.update({"main":f["main"],"after_event":f["after"],"endpoint":f["before"],
                     "ordering":"after" if v==1 else "before" if v in (2,5) else "while" if v==3 else "not_until_with_later_positive_event",
                     "same_endpoint_repeated_once_in_same_discourse":v==4,
                     "positive_main_event_asserted":v!=5,
                     "matrix_question":v==5,
                     "unasserted_causation":True})
    elif domain=="social_consent":
        base.update({"actor":f["actor"],"addressee":f["other"],"proposed_action":f["action"],
                     "permission_not_inferred_from_silence":True,
                     "action_occurred_asserted":False,
                     "frame_scope":{1:"asked",2:"explicit_refusal",3:"offer_declined",
                                    4:"silent_departure_not_permission",5:"prior_permission_withdrawn"}[v]})
    elif domain=="evidentiality":
        base.update({"embedded_proposition":f.get("clause") or f.get("event_clause"),
                     "reported_claim_not_fact":v in (2,5),
                     "speaker_evidence_type":{1:"direct",2:"named_indefinite_source",3:"inferential",4:"unknown_polar",5:"nonassertion"}[v],
                     "alternative_explicitly_negated":False})
    elif domain=="embedding_reference":
        base.update(relative_semantics90(f,v))
    elif domain=="counterfactual_modal":
        base.update(modal_semantics90(f,v))
    elif domain=="voice_valency":
        base.update({"actor":f["actor"],"patient":f["patient"],
                     "instrument":f["instrument"],
                     "instrument_is_agent":False,"instrument_case":"-shi",
                     "patient_case":"-m","positive_event_asserted":True})
    elif domain=="narrative_figures":
        base.update(literary_semantics90(f,v))
    elif domain=="technical_precision":
        base.update(technical_semantics90(f,v))
    return base

def collect_ids(f,variant):
    ids=[]
    for key in ("ids","source_ids","action_ids","barrier_ids","consequent_ids","recommendation_ids",
                "unsupported_ids","interpretation_ids","literal_ids"):
        if key in f:
            if key=="consequent_ids" and variant!=1:continue
            if key=="recommendation_ids" and variant!=4:continue
            if key=="unsupported_ids" and variant!=5:continue
            if key=="interpretation_ids" and variant!=3:continue
            if key=="literal_ids" and variant!=4:continue
            ids.extend(f[key])
    for key in ("actor_id","other_id","head_id","verb_id","patient_id"):
        if f.get(key):ids.append(f[key])
    return [i for i in dict.fromkeys(ids) if i]

def overlay_witnesses(candidate, lexemes):
    """Include actual 9.1 word uses in the evidence trail, not just frame metadata.

    A surface token may carry a case ending (-m/-shi/-lo), or a finite
    inflection. A rejected proposal never contributes a lexical witness.
    """
    tokens=re.findall(r"[^\s,.;?!«»]+",candidate)
    return [entry["id"] for entry in lexemes
            if entry.get("status")!="not_adopted"
            and any(token==entry["form"] or token.startswith(entry["form"]+"-")
                    for token in tokens)]

def proposals():
    entries={}
    overlay=read("editorial_lexicon_9_1.json")["entries"]
    old_relative={f["family"]:f for f in read("relative_frames_9_0.json")}
    old_literary={f["family"]:f for f in read("literary_frames_9_0.json")}
    old_technical={f["family"]:f for f in read("technical_propositions_9_0.json")}
    event_data=read("evidential_frames_9_1.json")
    bydomain={
        "daily":read("daily_frames_9_1.json"),
        "time_motion":read("motion_frames_9_1.json"),
        "social_consent":read("consent_frames_9_1.json"),
        "evidentiality":event_data["events"]+event_data["nonassertions"],
        "embedding_reference":read("relative_frames_9_1.json"),
        "counterfactual_modal":read("modal_frames_9_1.json"),
        "voice_valency":read("instrument_frames_9_1.json"),
        "narrative_figures":read("literary_frames_9_1.json"),
        "technical_precision":read("technical_completion_9_1.json")
    }
    for domain,frames in bydomain.items():
        for draft in frames:
            frame=draft
            if draft.get("use_existing_9_0_frame"):
                base=old_relative if domain=="embedding_reference" else old_literary
                frame={**base[draft["family"]],**draft}
                # Never mutate source 9.0 dictionary objects.
                assert frame["family"]==draft["family"]
            if domain=="technical_precision":
                frame={**old_technical[draft["family"]],**draft}
            # A short editorial family identifier is distinct from canonical
            # lexicon IDs and remains stable if source frames lack a row ID.
            frame={**frame,"id":frame.get("id") or
                   ("ED91-"+domain.upper()+"-"+str(frame["family"]).zfill(2))}
            for variant in draft["variants"]:
                id_=challenge_id(domain,frame["family"],variant)
                assert id_ not in entries,("Duplicate 9.1 proposal",id_)
                if domain=="daily":candidate=everyday(frame,variant)
                elif domain=="time_motion":candidate=motion(frame,variant)
                elif domain=="social_consent":
                    candidate=consent_action(frame,variant) if variant in (1,2,3) else consent90(frame,variant)
                    if variant==5:
                        # In the authoritative 8.0 morphology tense precedes
                        # modality: ROOT-te-ki, never ROOT-ki-te. Earlier
                        # editorial drafts are retained for separate review.
                        wrong=f"{frame['action']}-ki-te"
                        right=f"{frame['action']}-te-ki"
                        assert wrong in candidate
                        candidate=candidate.replace(wrong,right)
                elif domain=="evidentiality":
                    candidate=evidential(frame,variant) if variant in (1,2,3,4) else negated_matrix_claim(frame)
                elif domain=="embedding_reference":candidate=relative90(frame,variant)
                elif domain=="counterfactual_modal":candidate=modal90(frame,variant)
                elif domain=="voice_valency":
                    assert variant==3
                    candidate=instrument(frame)
                elif domain=="narrative_figures":candidate=literary90(frame,variant)
                elif domain=="technical_precision":candidate=technical90(frame,variant)
                else:raise AssertionError(domain)
                assert candidate and candidate.startswith(("sen ","hë ")),(id_,candidate)
                entries[id_]={
                    "candidate":candidate,
                    "domain":domain,"variant":variant,
                    "frame":frame,
                    "semantic_signature_json":json.dumps(signature(domain,frame,variant,candidate),
                                                          ensure_ascii=False,sort_keys=True),
                    "source_ids":list(dict.fromkeys(
                        collect_ids(draft,variant)+overlay_witnesses(candidate,overlay))),
                    "scope_warning":str(draft.get("note") or draft.get("boundary") or
                                       draft.get("editorial_sense") or draft.get("decision") or
                                       draft.get("semantic") or "Explicit source-specific editorial roles")
                }
    totals=dict(Counter(x["domain"] for x in entries.values()))
    assert totals==EXPECTED,(totals,EXPECTED)
    assert len(entries)==182
    return entries

def build():
    build90()
    parent=rows(ROOT/"data/stress90/case_evidence_500.csv")
    source=rows(ROOT/"data/stress81/challenges_500.csv")
    assert len(parent)==len(source)==500
    assert sum(bool(x["qaroshi_full_candidate"]) for x in parent)==318
    english={r["id"]:r["english"] for r in source}
    entries=proposals()
    correction=read("consent_morphology_corrections_9_1.json")
    repairs=set(correction["case_ids"])
    assert len(repairs)==8 and not repairs.intersection(entries)
    out=[]
    for record in parent:
        id_=record["id"]
        assert record["english"]==english[id_]
        row=dict(record)
        row["prior_9_0_candidate"]=record["qaroshi_full_candidate"]
        row["edition_9_1_semantic_signature_json"]=""
        row["edition_9_1_source_ids"]=""
        row["edition_9_1_editorial_scope_warning"]=""
        row["edition_9_1_inherited_morphology_repair_reason"]=""
        if id_ in repairs:
            old=row["qaroshi_full_candidate"]
            source_form=correction["original_bad_sequence"]
            new_form=correction["corrected_sequence"]
            assert old and old.count(source_form)==1,(id_,old)
            row["qaroshi_full_candidate"]=old.replace(source_form,new_form,1)
            row["edition_9_1_inherited_morphology_repair_reason"]=correction["reason"]
            row["editorial_scope_warning"]=str(row["editorial_scope_warning"])+(
                " | Corrected noncanonical past-ability suffix order; original 9.0 form preserved in prior_9_0_candidate.")
        if id_ in entries:
            assert not row["qaroshi_full_candidate"],("Historical draft collision",id_)
            item=entries[id_]
            row["qaroshi_full_candidate"]=item["candidate"]
            row["candidate_status"]="9_1_full_editorial_licensed_composition_pending_human_review"
            row["edition_9_1_semantic_signature_json"]=item["semantic_signature_json"]
            row["edition_9_1_source_ids"]=" | ".join(item["source_ids"]+[item["frame"]["id"]])
            row["witness_ids"]=row["edition_9_1_source_ids"]
            row["edition_9_1_editorial_scope_warning"]=item["scope_warning"]
            row["editorial_scope_warning"]=item["scope_warning"]
        row["human_backtranslation"]="not performed"
        row["external_comprehension"]="not performed"
        row["independently_semantically_verified"]="no"
        out.append(row)
    assert len(out)==len({r["id"] for r in out})==500
    assert len(entries)==182
    assert sum(bool(x["qaroshi_full_candidate"]) for x in out)==500
    assert {x["id"] for x in out if x["edition_9_1_source_ids"]}==set(entries)
    assert all(x["prior_9_0_candidate"]==p["qaroshi_full_candidate"] for x,p in zip(out,parent))
    assert {x["id"] for x in out if x["edition_9_1_inherited_morphology_repair_reason"]}==repairs
    OUT.mkdir(parents=True,exist_ok=True)
    write_csv(OUT/"case_evidence_500.csv",out)
    report={
        "edition":"9.1 source-linked FULL editorial drafts, NOT certified natural-language comprehension",
        "frozen_english_challenges":500,
        "inherited_9_0_draft_count":318,
        "new_9_1_draft_count":182,
        "inherited_drafts_preserved_verbatim_in_current_9_1_view":310,
        "inherited_9_0_drafts_explicitly_morphologically_repaired":len(repairs),
        "inherited_repair_ids":sorted(repairs),
        "all_318_previous_forms_preserved_in_prior_9_0_candidate":True,
        "all_full_editorial_candidate_strings":500,
        "no_complete_editorial_draft":0,
        "new_editorial_drafts_by_domain":dict(sorted(Counter(x["domain"] for x in entries.values()).items())),
        "new_candidate_ids":sorted(entries),
        "independent_backtranslations":0,
        "independent_comprehension_trials":0,
        "certified_english_qaroshi_equivalence_count":0,
        "full_natural_language_functionality_established":False,
        "frozen_reference_files_modified":False,
        "warning":"A full editorial draft is a proposal with documented sense decisions. No human meanings were elicited. An automated lexical or structural pass is NOT a semantic proof."
    }
    (OUT/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report

if __name__=="__main__":
    print(json.dumps(build(),ensure_ascii=False,indent=2))
