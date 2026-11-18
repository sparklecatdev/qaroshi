"""Evidence-checked source assembly for the Qaroshi 11.0 editorial learning pilot."""
from pathlib import Path
import csv
import json

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
    pairs = readcsv("data/v28_34/meaning_boundaries.csv")
    rules = readjson("data/v28_34/conversational_usage_rules.json")
    guides = readjson("data/standard_11/contrast_guides.json")
    tasks = readjson("data/standard_11/dialogue_challenges.json")
    if len(pairs) != 30 or len(rules) != 20 or len(guides) != 30 or len(tasks) != 12:
        raise ValueError("Missing standard source or editorial exercises")
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
                        "source_conversational_rules": 20, "new_situational_challenges": 12,
                        "independent_reader_results": 0, "new_canonical_words": 0,
                        "new_normative_senses": 0, "new_normative_grammar": 0}}

if __name__ == "__main__":
    print(json.dumps(assemble()["metrics"], ensure_ascii=False, indent=2))
