"""Evidence-checked source assembly for the Qaroshi 11.0 editorial learning pilot."""
from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[2]

def readcsv(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def readjson(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def assemble():
    words = readcsv("data/lexicon.csv")
    by_form = {word["qaroshi"]: word for word in words}
    assert len(words) == len(by_form) == 30000, "Historical dictionary has changed"
    # The one adopted post-7.0 determiner is intentionally not in the frozen 30k.
    overlays = readjson("data/v28_34/adopted_function_words.json")
    if len(overlays) != 1 or overlays[0]["lemma"] != "nëgëra" or overlays[0]["source_id"] != "Q28D001":
        raise ValueError("Unexpected post-7.0 lexicon overlay")
    if overlays[0]["lemma"] in by_form:
        raise ValueError("Overlay must not replace a historical dictionary word")
    by_form[overlays[0]["lemma"]] = {"id": overlays[0]["source_id"]}
    pairs = readcsv("data/v28_34/meaning_boundaries.csv")
    rules = readjson("data/v28_34/conversational_usage_rules.json")
    guides = readjson("data/standard_11/contrast_guides.json")
    tasks = readjson("data/standard_11/dialogue_challenges.json")
    if len(pairs) != 30 or len(rules) != 20 or len(guides) != 30 or len(tasks) != 20:
        raise ValueError("Missing standard source or editorial exercises")
    # Entire authentic *editorial teaching reference* examples, never new sentences.
    # Index exact canonical stems and only attested suffix chains; prefix
    # substrings and unrelated modifier-head compounds never count as a hit.
    phrases = readcsv("corpus/parallel_sentences.csv")
    if len(phrases) != 4383:
        raise ValueError("Historical phrasebook length changed")
    allowed = {"-" + affix["form"].lstrip("-") for affix in readjson("data/affixes.json")
               if affix["category"] in ("case", "nominal", "tense", "aspect", "modal",
                                        "modality", "manner", "voice", "discourse")}
    allowed.update(("-m", "-lo", "-na", "-gu", "-de", "-tu", "-wa", "-te", "-yu", "-ki", "-ho", "-du", "-za"))
    targets = {head for pair in pairs for head in (pair["left"], pair["right"])}
    examples = {}
    for phrase in phrases:
        for surface in re.findall(r"[a-zë]+(?:-[a-zë]+)*", phrase["qaroshi"].lower()):
            head = surface if surface in targets else None
            if head is None and "-" in surface:
                segments = surface.split("-")
                for i in range(len(segments)-1, 0, -1):
                    stem = "-".join(segments[:i])
                    if stem in targets and all("-" + tail in allowed for tail in segments[i:]):
                        head = stem
                        break
            if head in targets and head not in examples:
                examples[head] = {"source_id": phrase["id"], "qaroshi": phrase["qaroshi"],
                    "english": phrase["english"], "matched_form": surface,
                    "provenance": "corpus/parallel_sentences.csv",
                    "status": "historical controlled bilingual teaching reference, not speaker-attested"}
    guide_map = {item["source_id"]: item for item in guides}
    task_map = {item["source_id"]: item for item in tasks}
    if len(guide_map) != 30 or len(task_map) != 12:
        raise ValueError("Duplicate review item")
    if set(guide_map) != {p["id"] for p in pairs} or not set(task_map) <= {r["id"] for r in rules}:
        raise ValueError("Editorial item has no exact source ID")
    contrasts = []
    for pair in pairs:
        if pair["left"] not in by_form or pair["right"] not in by_form:
            raise ValueError("Semantic headword not in historical dictionary")
        note = guide_map[pair["id"]]
        if note["status"] != "editorial_explanation_not_independently_validated":
            raise ValueError("Improper semantic approval claim")
        if any(not note.get(field, "").strip() for field in ("explanation","learner_question","forbidden_inference")):
            raise ValueError("Missing explanation: " + pair["id"])
        contrasts.append({**pair, "source_status": pair["status"], "source": "data/v28_34/meaning_boundaries.csv",
            "left_dictionary_id": by_form[pair["left"]]["id"], "right_dictionary_id": by_form[pair["right"]]["id"],
            "left_example": examples.get(pair["left"]), "right_example": examples.get(pair["right"]),
            **{k:v for k,v in note.items() if k != "source_id"}})
    conversation_rules = []
    for rule in rules:
        exercise = task_map.get(rule["id"])
        if exercise and (exercise["status"] != "editorial_training_not_blind_validation" or
                         any(not exercise.get(k, "").strip() for k in ("scenario","question","editorial_answer"))):
            raise ValueError("Invalid conversational training task")
        conversation_rules.append({**rule, "source": "data/v28_34/conversational_usage_rules.json",
                                   "training": exercise})
    return {"edition": "11.0 editorial pilot", "contrasts": contrasts, "conversation_rules": conversation_rules,
            "metrics": {"source_contrasts": 30, "new_editorial_explanations": 30,
                        "distinct_exampled_headwords": len(examples),
                        "source_conversational_rules": 20, "new_situational_challenges": 20,
                        "independent_reader_results": 0, "new_canonical_words": 0,
                        "new_normative_senses": 0, "new_normative_grammar": 0}}

if __name__ == "__main__":
    print(json.dumps(assemble()["metrics"], ensure_ascii=False, indent=2))
