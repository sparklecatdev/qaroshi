#!/usr/bin/env python3
"""Edition 8.4 evidence ledger, restricted productive core and reviewer packets.

No synthetic human attestations, no automatic lexical ratification.
"""
from __future__ import annotations
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "stress84"
sys.path.insert(0, str(ROOT / "tools" / "stress83"))
sys.path.insert(0, str(ROOT / "tools" / "stress84"))
from complete import build as build_83
from validate_core import analyze

BLOCKERS = {
    "daily": "Select exact agent, object and verb sense; distinguish tense from completion and embedding",
    "time_motion": "Disambiguate before/after/while/until event order and local negation",
    "social_consent": "Disambiguate the asker, permitted action, explicit refusal and revocation",
    "quantifier_logic": "Distinguish all, none, not all, some, only and scope of tense/focus",
    "evidentiality": "Preserve direct observation, report, inference, knowledge and uncertainty",
    "embedding_reference": "License relative-head gaps and matrix versus subordinate reference/scope",
    "counterfactual_modal": "Distinguish ability, permission, necessity, unreal antecedents and actual outcomes",
    "voice_valency": "Check semantic patient classes, passive licenses, actors and instruments",
    "narrative_figures": "Paraphrase metaphor without changing literal truth conditions or fabricating idioms",
    "technical_precision": "Use specific domain senses and separate evidence, causes and recommendations",
}

# Distinct documented grammatical contrasts, not examples of independent
# recognition by learners. The answer-key file must be kept from test takers.
CONTRASTS = [
    ("negation", "sen mi kima-m këmë.", "I drink water.",
     "sen mi kima-m nu këmë.", "I do not drink water."),
    ("time", "sen mi kima-m këmë.", "I drink water.",
     "sen mi kima-m këmë-te.", "I drank water."),
    ("ability_permission", "sen sa goro-ki.", "They can fly.",
     "sen sa goro-ho.", "They may fly."),
    ("not_all_none", "sen nëgëra qaro goro.", "Not every Nardoragon flies.",
     "sen ngënao qaro nu goro.", "No Nardoragon flies."),
    ("that_whether", "sen sa haro do mi sëmi.", "I know that they are well.",
     "sen sa haro he do mi sëmi.", "I know whether they are well."),
    ("matrix_embedded_negation", "sen sa haro he do mi nu sëmi.", "I do not know whether they are well.",
     "sen sa nu haro he do mi sëmi.", "I know whether they are not well."),
    ("deep_care_romance", "më mi ti-m nashi.", "I deeply cherish you.",
     "më mi ti-m mali.", "I love you romantically."),
    ("travel_stay", "sen mi naro-gu gura.", "I travel toward home.",
     "sen mi naro-lo nëra.", "I remain at home."),
    ("passive_actor_instrument", "sen naro mara-za daru-li-te.", "The home was protected by a friend.",
     "sen naro banu-shi daru-li-te.", "The home was protected using wings."),
    ("inclusive_exclusive", "sen naru qaroshi-m shiri.", "We, including you, speak Qaroshi.",
     "sen muru qaroshi-m shiri.", "We, excluding you, speak Qaroshi."),
    ("witnessed_reported", "sen sa goro si.", "They fly, according to what I witnessed.",
     "sen sa goro hu.", "They fly, according to a report."),
    ("new_core_intention_result", "sen mi naro-m rëgë.", "I repair the home, without asserting success.",
     "sen mi naro-m rëgë-te-mo.", "I completed repairing the home (completion is not automatically restored function)."),
]

def readcsv(path):
    with path.open(encoding="utf8", newline="") as fp:
        return list(csv.DictReader(fp))

def savecsv(path, rows):
    if not rows:
        raise ValueError("Empty output: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def savejson(path, x):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(x, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf8")

def build():
    build_83()
    OUT.mkdir(parents=True, exist_ok=True)
    original = readcsv(ROOT / "data/stress83/translation_proposals_500.csv")
    lex = {x["qaroshi"]: x for x in readcsv(ROOT / "data/lexicon.csv")}
    core = readcsv(ROOT / "data/v17/core_learning_120.csv")
    oldframes = json.loads((ROOT / "data/semantics/valency_frames.json").read_text(encoding="utf8"))
    newframes = json.loads((ROOT / "data/standard_8/valency_overlay_8_4.json").read_text(encoding="utf8"))
    priority = readcsv(ROOT / "data/v28_34/verb_frame_inventory_400.csv")
    assert len(original) == 500 and len(core) == 120 and len(oldframes) == 25
    assert len(newframes) == 11 and len(priority) == 400
    oldlemmata = {r["lemma"] for r in oldframes}
    newlemmata = {r["lemma"] for r in newframes}
    assert len(newlemmata) == 11 and not (newlemmata & oldlemmata)
    for frame in newframes:
        assert lex[frame["lemma"]]["pos"] == "v"
        assert analyze(frame["model_sentence"])["status"] == "structural_model_match", frame["lemma"]

    queued = []
    for c in original:
        witnesses = json.loads(c["dictionary_lexeme_witness_json"])
        vwords = sorted({w["qr"] for w in witnesses
                         if w["qr"] and w["qr"] in lex and lex[w["qr"]]["pos"] == "v"})
        newcore = [x for x in vwords if x in newlemmata]
        licensed_old = [x for x in vwords if x in oldlemmata]
        draft = bool(c["qaroshi_draft"])
        queued.append({
            "id": c["id"],
            "domain": c["domain"],
            "english_target": c["english_target"],
            "draft_8_3": c["qaroshi_draft"],
            "coverage_8_3": c["coverage_status"],
            "priority": "1" if c["domain"] in ("embedding_reference", "time_motion",
                                                   "social_consent", "technical_precision",
                                                   "counterfactual_modal") else "2",
            "review_blocker": BLOCKERS[c["domain"]],
            "documented_verb_lemmas": " | ".join(vwords),
            "prior_manual_frame_lemmas": " | ".join(licensed_old),
            "edition_8_4_core_lemmas": " | ".join(newcore),
            "audit_status": "candidate_needs_semantic_check" if draft else "needs_complete_original_composition",
            "human_backtranslation": "not performed",
            "reviewer_decision": "",
            "reviewer_reason": "",
            "false_completion_forbidden": "yes",
        })
    savecsv(OUT / "case_review_queue_500.csv", queued)

    byprior = {r["lemma"]: r for r in priority}
    cards = []
    for r in priority:
        if r["lemma"] in oldlemmata:
            status = "inherited_25_general_frame"
        elif r["lemma"] in newlemmata:
            status = "8_4_defined_active_frame_only"
        else:
            status = "source_limited_no_general_frame"
        cards.append({
            "lemma": r["lemma"], "dictionary_id": r["dictionary_id"],
            "reference_gloss": r["reference_gloss"],
            "original_review_status": r["review_status"],
            "8_4_frame_status": status,
            "source_count_controlled_editorial": r["source_count_controlled"],
            "source_example_ids": r["example_ids"],
            "documented_object_root": r["licensed_object_root"],
            "model": next((x["model_sentence"] for x in newframes
                           if x["lemma"] == r["lemma"]), ""),
            "review_agent_requirement": "",
            "review_patient_selection": "",
            "review_passive_licensed": "",
            "review_causative_licensed": "",
            "minimal_pair_counterexample": "",
            "independent_comprehension": "not performed",
        })
    savecsv(OUT / "verb_frame_cards_400.csv", cards)

    # Stable 120-core indexing, explicitly NOT 120 newly authored monolingual
    # definitions. Native explanations require distinct semantic work.
    corecards = []
    for r in core:
        term = lex[r["root"]]
        linked = [f for f in newframes if f["lemma"] == r["root"]]
        corecards.append({
            "root": r["root"], "dictionary_id": term["id"],
            "index_english": term["english"], "pos": term["pos"],
            "source_ipa": term["ipa"],
            "review_status": "8_4_individual_narrow_frame" if linked else
                ("earlier_reviewed_frame" if r["root"] in oldlemmata else
                 "source_gloss_only_not_individually_reviewed"),
            "productive_frame_id": linked[0]["id"] if linked else "",
            "native_definition_approved": "no",
            "native_definition_draft": "",
            "blind_context_understanding": "not performed",
        })
    savecsv(OUT / "core_semantic_cards_120.csv", corecards)

    prompts, key = [], []
    for idx, (topic, a, meaning_a, b, meaning_b) in enumerate(CONTRASTS, 1):
        k = "C84-%03d" % idx
        # Participants receive both Qaroshi alternatives and independently
        # choose which statement matches an English target, not a revealed key.
        target = meaning_a if idx % 2 else meaning_b
        correct = "A" if idx % 2 else "B"
        prompts.append({"id": k, "contrast": topic, "A_qaroshi": a,
                        "B_qaroshi": b, "english_target": target,
                        "response_A_or_B": "",
                        "source": "editorially constructed; no listener validation"})
        key.append({"id": k, "correct": correct, "A_meaning": meaning_a,
                    "B_meaning": meaning_b, "status": "unadministered"})
    savecsv(OUT / "blind_contrast_questions.csv", prompts)
    savecsv(OUT / "separate_blind_answer_key.csv", key)

    statuses = dict(Counter(r["audit_status"] for r in queued))
    manifest = {
        "edition": "8.4 active core and reproducible functional readiness ledger",
        "original_8_1_challenges": 500,
        "editorial_drafts_not_independently_validated": statuses.get("candidate_needs_semantic_check", 0),
        "challenges_without_complete_draft": statuses.get("needs_complete_original_composition", 0),
        "prior_reviewed_general_frames": len(oldframes),
        "new_narrow_active_frames_defined": len(newframes),
        "priority_verbs_still_without_general_frames": len(priority)-len(oldframes)-len(newframes),
        "core_lexemes_queued_for_individual_sense_definitions": len(core),
        "blind_grammar_minimal_pairs_prepared": len(prompts),
        "real_independent_test_participants": 0,
        "fully_general_translation_certified": False,
        "all_404_remaining_translated": False,
        "source_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(OUT.glob("*.csv"))},
    }
    savejson(OUT / "manifest.json", manifest)
    return manifest

if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
