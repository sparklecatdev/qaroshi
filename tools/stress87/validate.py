#!/usr/bin/env python3
"""Check a restricted 8.7 active-clause pattern, not meaning or general grammar."""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRAMES = {row["lemma"]: row for row in json.loads(
    (ROOT / "data/standard_8/valency_overlay_8_7.json").read_text(encoding="utf-8"))}
with (ROOT / "data/lexicon.csv").open(encoding="utf-8", newline="") as source:
    OBJECTS = {row["qaroshi"] for row in csv.DictReader(source)
               if row["pos"] in {"n", "pron"}}
RESONANCES = set("më zha qor sen hë lën sur rak khar yë nëm wen dal rëm hol zher".split())
SUBJECTS = set("mi ti sa naru muru tiri sari".split())
GROUPS = ({"te", "yu"}, {"se", "mo", "në"}, {"ki", "ho", "du"}, {"la"})


def analyze(sentence):
    """A match describes form alone; object selection and meaning are untested."""
    result = {"input": sentence, "status": "outside_restricted_checker",
              "semantic_validation": "not performed", "reasons": []}
    text = sentence.strip()
    if text and text[-1] in ".!?":
        text = text[:-1]
    parts = text.split()
    if parts and parts[-1] == "he":
        parts.pop()
    if len(parts) not in (4, 5) or parts[0] not in RESONANCES or parts[1] not in SUBJECTS:
        result["reasons"].append("Expected resonance, pronoun subject, object and predicate")
        return result
    if len(parts) == 5 and parts[3] != "nu":
        result["reasons"].append("Only immediate pre-predicate negation is handled")
        return result
    obj = parts[2].split("-")
    if len(obj) not in (2, 3) or obj[-1] != "m" or (len(obj) == 3 and obj[1] != "ri") or obj[0] not in OBJECTS:
        result["reasons"].append("Expected a dictionary noun or pronoun with optional plural and -m")
        return result
    lemma, *suffixes = parts[-1].split("-")
    if lemma not in FRAMES:
        result["reasons"].append("Predicate has no 8.7 frame")
        return result
    result.update(lemma=lemma, frame_id=FRAMES[lemma]["id"])
    positions = []
    for suffix in suffixes:
        match = next((i for i, group in enumerate(GROUPS) if suffix in group), None)
        if match is None:
            result["reasons"].append("Unknown or unhandled verbal suffix")
            return result
        positions.append(match)
    if positions != sorted(set(positions)):
        result["reasons"].append("Repeated or out-of-order verbal suffix category")
        return result
    result["status"] = "structural_model_match"
    result["reasons"].append("Form only; object suitability and interpretation are not checked")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sentence")
    print(json.dumps(analyze(parser.parse_args().sentence), ensure_ascii=False, indent=2))
