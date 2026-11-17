#!/usr/bin/env python3
"""Qaroshi 8.8: full-item adversarial semantic bookkeeping and narrow amendments.

Only *full candidate strings* for specifically licensed senses can increase the
proposal count. Nothing here demonstrates independent speaker comprehension.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/stress88"
sys.path.insert(0, str(ROOT / "tools/stress83"))
from complete import build as build83, rows

DOMAIN_REQUIREMENTS = {
    "daily": {
        1: "agent, physical patient, completed-in-past event assertion",
        2: "agent, physical patient, negated past event; no success inference",
        3: "yes/no scope over one past action, with agent and patient",
        4: "source conveyed an embedded P to speaker; P not asserted true",
        5: "counterfactual antecedent, contrary-to-fact status, distinct past consequent, reference tracking",
    },
    "time_motion": {
        1: "two separately licensed events; later-than ordering of main event",
        2: "two events; before relation and source actor identity",
        3: "two overlapping event intervals, no spurious causal claim",
        4: "negative until boundary and post-boundary occurrence presupposition",
        5: "polar question over order of two events",
    },
    "social_consent": {
        1: "asker, addressee, action actor, patient, permission polarity",
        2: "refusal by addressee and original permission request",
        3: "offer versus rejection, separate agent and patient roles",
        4: "silence/departure not equated with permission",
        5: "prior permission, explicit revocation, temporal priority before action",
    },
    "quantifier_logic": {
        1: "universal scope over domain and adjective",
        2: "not-all scope, without asserting that some do P",
        3: "no member satisfies predicate",
        4: "existential some, no universal inference",
        5: "exclusive focus of demonstrative NP, not predicate/time",
    },
    "evidentiality": {
        1: "witness source is first-person direct observation",
        2: "person spoke to speaker, event is unasserted",
        3: "inference from evidence, not direct witness and not guaranteed truth",
        4: "unknown whether P, not unknown whether not-P by scope inversion",
        5: "explicitly refrain from asserting alternative, not assert its negation",
    },
    "embedding_reference": {
        1: "head identifies same participant in relative clause and matrix clause",
        2: "matrix think attitude embeds relative proposition, not asserted as fact",
        3: "matrix knowledge negation scopes over polar question about relative proposition",
        4: "conditional antecedent includes relative referent; distinct consequent",
        5: "causal relation between relative-headed main assertion and reason",
    },
    "counterfactual_modal": {
        1: "past counterfactual antecedent and unreal consequent",
        2: "ability assertion contrasted with barrier, no permission inference",
        3: "permission assertion contrasted with barrier, no ability inference",
        4: "obligation assertion despite barrier, no claim action occurred",
        5: "projected conditional with altered barrier, no actual-world result",
    },
    "voice_valency": {
        1: "active transitive actor-patient mapping",
        2: "passive patient and overt actor -za, no instrument interpretation",
        3: "active actor, patient and true instrument -shi",
        4: "negative active scope over whole event",
        5: "passive patient and overt agent inside question scope",
    },
    "narrative_figures": {
        1: "fictional metaphor, not literal-world assertion",
        2: "quoted lexical identity and narrator attribution",
        3: "the poet's intended indirect reading, not literal event",
        4: "negated literal entailment, preserve exact quoted source proposition",
        5: "initial mistaken literal interpretation, later correction and actor tracking",
    },
    "technical_precision": {
        1: "reporting source and scientific proposition; report does not prove truth",
        2: "second observer is independently distinct; reported proposition",
        3: "possibility plus explicit lack of independent verification",
        4: "conditional trigger and recommendation modality, not realized action",
        5: "unsupported consequence explicitly not entailed, not asserting its falsehood",
    },
}

def write_csv(path:Path, things):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf8", newline="") as fp:
        out=csv.DictWriter(fp,fieldnames=list(things[0]),lineterminator="\n")
        out.writeheader()
        out.writerows(things)

def verb_sentence(actor,patient,verb,variant):
    """Only 8.8 licensed V1 active senses, no passive/causative inference."""
    if variant == 1:
        return f"sen {actor} {patient}-m {verb}-te."
    if variant == 2:
        return f"sen {actor} {patient}-m nu {verb}-te."
    if variant == 3:
        return f"hë {actor} {patient}-m {verb}-te he?"
    if variant == 4:
        return f"sen {actor} {patient}-m {verb}-te do yano mi-tu shiri-te."
    raise ValueError("Unsupported daily variant")

def valency_sentence(f,variant):
    subject=f["actor"]; obj=f["patient"]; v=f["root"]
    if variant == 1:return f"sen {subject} {obj}-m {v}-te."
    if variant == 2:return f"sen {obj} {subject}-za {v}-li-te."
    if variant == 3:
        if not f["tool"]:return None
        return f"sen {subject} {obj}-m {f['tool']}-shi {v}-te."
    if variant == 4:return f"sen {subject} {obj}-m nu {v}-te."
    if variant == 5:return f"hë {obj} {subject}-za {v}-li-te he?"
    raise ValueError("Unknown valency variant")

def run():
    build83()
    original=rows(ROOT/"data/stress83/translation_proposals_500.csv")
    challenges=rows(ROOT/"data/stress81/challenges_500.csv")
    frames=json.loads((ROOT/"data/standard_8/valency_overlay_8_8.json").read_text(encoding="utf8"))
    senses=json.loads((ROOT/"data/standard_8/sense_extension_8_8.json").read_text(encoding="utf8"))
    old={x["id"]:x for x in original}
    assert len(original)==500 and len(challenges)==500 and len(old)==500
    assert len(frames)==5 and len(senses)==3
    families={x["family"]:x for x in frames}
    extension={x["family"]:x for x in senses}
    old_yes=sum(bool(x["qaroshi_draft"]) for x in original)
    assert old_yes==96, f"Unexpected earlier score: {old_yes}"
    queue=[]
    for item in challenges:
        id_=item["id"]; domain=item["domain"];variant=int(item["variant"])
        fam=int(item["scenario_family"].split("-")[-1])
        source=old[id_]
        proposal=source["qaroshi_draft"] or ""
        method="inherited_unverified_editorial_draft" if proposal else "no_full_candidate"
        witness=""
        caveat=source.get("editorial_warning","")
        competing=""
        # A truly new, fully realized *editorial* proposal is permitted only
        # with explicitly licensed fixed participant/object senses.
        if domain=="daily" and fam in extension and variant<=4:
            f=extension[fam]
            candidate=verb_sentence(f["actor"],f["patient"],f["verb"],variant)
            if fam==10:
                # "transport ticket" narrows unspecified English "ticket".
                # Preserve the mismatch, do not fill a supposedly solved cell.
                competing=candidate
                caveat="Contextual travel-ticket paraphrase ONLY; adds ticket-type entailment absent in English."
            else:
                proposal=candidate
                method="new_8_8_editorial_full_composition_not_independently_validated"
                witness=" | ".join([f["actor_id"],f["verb_id"],f["patient_id"],f["id"]])
                caveat=f["boundary"]
        if domain=="quantifier_logic" and fam==1 and variant==5:
            assert not proposal
            proposal="sen dëna qaro ngëshi nëna haro."
            method="new_8_8_editorial_full_composition_not_independently_validated"
            witness="qaro (noun) | haro (adjective) | dëna (demonstrative) | ngëshi (focus) | nëna (present-time adverb)"
            caveat="Restricts the Nardoragon NP, not the well-being property or time."
        if domain=="daily" and variant==4 and fam in (1,2,7):
            # Repair source attribution: use an indefinite person explicitly
            # speaking to the first-person recipient, not arbitrary 'they'.
            base={1:("nënugo","gëla","shëmiroli"),2:("shuna","tëzhoza","shëliroa"),7:("rezhago","relanga","ngëmiro")}[fam]
            proposal=verb_sentence(*base,4)
            method="revised_inherited_source_reporting_editorial_draft"
            witness="yano (an unspecified person) | mi-tu (recipient) | do (content) | shiri-te (said)"
            caveat="Embedded action is reported but not asserted by the outer speaker."
        if domain=="voice_valency" and fam in families:
            f=families[fam]
            expected=valency_sentence(f,variant)
            if expected:
                proposal=expected
                method="8_8_specific_actor_patient_voice_license_unverified"
                witness=" | ".join([f["root_id"],f["actor_id"],f["patient_id"],f["id"]]+([f["tool_id"]] if variant==3 else []))
                caveat=f["boundary"]
        if not proposal and not competing: caveat="No full licensed composition documented; do not fill by dropping semantic roles."
        queue.append({"id":id_,"domain":domain,"family":fam,"variant":variant,
                      "english":item["english"],"required_semantic_factors":DOMAIN_REQUIREMENTS[domain][variant],
                      "qaroshi_full_candidate":proposal,"candidate_status":method,
                      "witness_ids":witness,"editorial_scope_warning":caveat or "Requires item-level meaning review.",
                      "contextual_partial_paraphrase_not_counted":competing,
                      "known_english_role_loss":"not independently assessed",
                      "human_backtranslation":"not performed",
                      "external_comprehension":"not performed",
                      "proven_language_impossibility":"no"})
    assert len(queue)==500 and len({x["id"] for x in queue})==500
    n=sum(bool(x["qaroshi_full_candidate"]) for x in queue)
    assert n>=96
    counts=Counter(x["candidate_status"] for x in queue)
    report={
        "edition":"8.8 selective semantic/productive proposals",
        "challenge_count":500,
        "prior_editorial_candidates":old_yes,
        "editorial_candidates_now":n,
        "net_new_complete_candidate_strings":n-old_yes,
        "still_without_full_candidate":500-n,
        "human_verified":0,
        "source_preservation":"all frozen earlier files unchanged",
        "new_voice_frame_licenses":len(frames),
        "narrow_new_everyday_senses":2,
        "contextual_travel_ticket_paraphrase_not_promoted":4,
        "source_report_templates_narrowed":3,
        "candidate_status_counts":dict(sorted(counts.items())),
        "language_complete":False,
        "translation_certified":False,
    }
    write_csv(OUT/"case_evidence_500.csv",queue)
    (OUT/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return report

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,indent=2))
