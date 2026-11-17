#!/usr/bin/env python3
"""Build source-grounded Qaroshi Standard 10 learner data.

This combines existing sources without changing the frozen lexicon or corpus.
A semicolon-delimited English gloss does not establish a new sense; a proposed
example does not become speaker-attested because an editor wrote it. Nothing
in these outputs is an independently approved human comprehension result.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def load_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def assemble() -> dict[str, Any]:
    lexicon = load_csv("data/lexicon.csv")
    by_id = {w["id"]: w for w in lexicon}
    by_form = {w["qaroshi"]: w for w in lexicon}
    assert len(lexicon) == 30000 == len(by_id)
    accepted_editorial = collections.defaultdict(list)
    core_profiles = {}
    priority = {}
    unreviewed_drafts = {}
    rejected = collections.Counter()

    # Previously authored human-readable distinctions, restrictions, and
    # actual examples. Keep their published *editorial* approval status.
    for row in load_csv("data/v12_13/core_lexical_profiles.csv"):
        head = by_form.get(row["qaroshi"])
        if not head or head["id"] != row["source_id"]:
            rejected["core_profile_id_mismatch"] += 1
            continue
        core_profiles[head["qaroshi"]] = {
            "profile_id": row["id"],
            "definition": row["editorial_sense_definition"],
            "restriction": row["grammatical_or_semantic_restriction"],
            "contrast": row["contrast_or_false_friend"],
            "qaroshi_example": row["qaroshi_example"],
            "english_example": row["english_example_contextual"],
            "meaning_status": row["meaning_status"],
            "reviewer_status": row["reviewer_status"],
            "source": "data/v12_13/core_lexical_profiles.csv",
            "classification": "individually authored editorial clarification; no independent reader approval",
        }

    for row in load_json("data/semantics/curated_senses.json"):
        head = by_form.get(row["lemma"])
        if not head or head["id"] != row["dict_id"]:
            rejected["curated_sense_id_mismatch"] += 1
            continue
        accepted_editorial[row["lemma"]].append({
            "sense_id": row["id"],
            "label": row["sense"],
            "definition": row["definition"],
            "construction": row["construction"],
            "source_status": row["status"],
            "source": "data/semantics/curated_senses.json",
            "independent_human_attestation": False,
        })

    # The 800-word priority index is a *review inventory*. Its gloss is the
    # canonical English label, not a newly corroborated sense definition.
    for row in load_csv("data/v28_34/core_semantic_index_800.csv"):
        head = by_id.get(row["dictionary_id"])
        if not head or head["qaroshi"] != row["lemma"]:
            rejected["priority_id_mismatch"] += 1
            continue
        priority[head["qaroshi"]] = {
            "rank": int(row["priority_rank"]),
            "corpus_mentions": int(row["corpus_mentions"]),
            "source_reference_ids": row["source_reference_ids"],
            "curated_sense_ids": row["curated_sense_ids"],
            "lexical_treatment": row["lexical_treatment"],
            "gloss_interpretation": row["gloss_interpretation"],
            "speaker_attestation": row["speaker_attestation"],
            "source": "data/v28_34/core_semantic_index_800.csv",
        }

    # The existing set of 5,000 proposals selects one canonical English
    # gloss; it must NEVER be promoted into an independent polysemy assertion.
    # Candidate examples remain an explicitly unverified research queue.
    for row in load_csv("data/editorial/sense_cards_5000.csv"):
        head = by_form.get(row["qaroshi"])
        if not head or head["id"] != row["headword_id"]:
            rejected["draft_id_mismatch"] += 1
            continue
        segment = row["gloss"].strip()
        if segment.casefold() not in head["english"].casefold():
            rejected["draft_gloss_not_in_reference"] += 1
            continue
        unreviewed_drafts[head["qaroshi"]] = {
            "sense_id": row["sense_id"],
            "selected_reference_gloss": segment,
            "candidate_qaroshi": row["candidate_example"],
            "candidate_english": row["candidate_example_en"],
            "source": "data/editorial/sense_cards_5000.csv",
            "status": "UNREVIEWED: source-gloss selection and candidate example, not a new approved sense",
            "independent_human_attestation": False,
        }

    original11 = load_json("corpus/original11/dialogues.json")
    source18 = load_json("data/v18/source_linked_conversation_paths.json")
    dialogues = []
    for d in original11:
        turns = [{
            "speaker": t["speaker"], "qaroshi": t["qaroshi"],
            "english": t["english"],
            "literal_english": t.get("literal_translation", ""),
            "ipa": t.get("ipa", ""), "sound_out": t.get("sound_out", ""),
            "reference_id": "", "status": t["status"],
        } for t in d["turns"]]
        dialogues.append({
            "id": "original11/" + d["id"], "title": d["title"],
            "context": d["premise"], "domain": "original dialogues",
            "turns": turns, "source": "corpus/original11/dialogues.json",
            "status": "individually authored editorial conversation; no independent speaker ratification",
        })
    for d in source18:
        turns = [{
            "speaker": t["speaker"], "qaroshi": t["qaroshi"],
            "english": t["english"], "literal_english": "",
            "ipa": t.get("ipa", ""), "sound_out": t.get("sound_out", ""),
            "reference_id": t.get("reference_id", ""),
            "status": t["provenance"],
        } for t in d["turns"]]
        dialogues.append({
            "id": "source18/" + d["id"], "title": d["title"],
            "context": d["context"], "domain": d["domain"],
            "turns": turns, "source": "data/v18/source_linked_conversation_paths.json",
            "status": d["provenance"],
        })
    ids = {d["id"] for d in dialogues}
    assert len(ids) == len(dialogues)
    assert all(len(d["turns"]) >= 2 for d in dialogues)

    # The old offline translator's roundtripped corpus is useful for drill
    # variety only. These are NOT meaning-approved or native-attested lines.
    raw_drills = load_json("data/fluency11/translation_pairs.json")
    drills = []
    for i, pair in enumerate(raw_drills, 1):
        if not pair["en"] or not pair["qr"]:
            continue
        drills.append({
            "id": f"TR10-{i:04d}", "english": pair["en"],
            "qaroshi": pair["qr"],
            "backtranslated_english": pair.get("parsed_en", ""),
            "confidence": pair.get("confidence", ""),
            "warning": pair.get("note", ""),
            "status": "machine round-trip practice ONLY; editorial, not independent semantic equivalence",
            "source": "data/fluency11/translation_pairs.json",
        })

    manifest = {
        "canonical_words": len(lexicon),
        "core_individually_authored_profiles": len(core_profiles),
        "previous_editorial_sense_descriptions": sum(map(len, accepted_editorial.values())),
        "lemmas_with_curated_senses": len(accepted_editorial),
        "priority_lexical_review_inventory": len(priority),
        "unreviewed_gloss_selection_and_example_cards": len(unreviewed_drafts),
        "rejected_mismatched_source_rows": dict(sorted(rejected.items())),
        "editorial_conversations": len(dialogues),
        "conversation_turns": sum(len(d["turns"]) for d in dialogues),
        "source_dialogues_original11": len(original11),
        "source_dialogues_recombined18": len(source18),
        "machine_roundtrip_drills": len(drills),
        "independent_human_reader_trials": 0,
        "independent_human_attestations": 0,
        "independence_caveat": (
            "Software validation is not a human language-understanding experiment. "
            "The 5,000 legacy sense cards select canonical glosses; their examples are unreviewed."
        ),
    }
    return {
        "profiles": core_profiles, "senses": dict(accepted_editorial),
        "priorities": priority, "draft_cards": unreviewed_drafts,
        "dialogues": dialogues, "controlled_drills": drills,
        "manifest": manifest,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = assemble()
    if args.out:
        output = pathlib.Path(args.out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.summary or not args.out:
        print(json.dumps(result["manifest"], ensure_ascii=False, indent=2))
