#!/usr/bin/env python3
"""NARROW syntactic checker for the eleven edition-8.4 active core frames.

This is NOT an open-domain parser or semantic acceptability judgment.
It only handles explicit pronoun-subject, single-clause model patterns.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRAMES = {r["lemma"]: r for r in json.loads(
    (ROOT / "data/standard_8/valency_overlay_8_4.json").read_text(encoding="utf8")
)}
RESONANCES = set("më zha qor sen hë lën sur rak khar yë nëm wen dal rëm hol zher".split())
SUBJECTS = set("mi ti sa naru muru tiri sari".split())
SUFFIXES = {"te", "yu", "se", "mo", "në", "ki", "ho", "du", "la"}
ORDER = {"te": 1, "yu": 1, "se": 2, "mo": 2, "në": 2,
         "ki": 3, "ho": 3, "du": 3, "la": 4}


def analyze(text: str) -> dict:
    """Return structural evidence only, never a claim of verified meaning."""
    original = text.strip()
    parts = original.rstrip(".!?").split()
    result = {"input": original, "status": "outside_narrow_checker",
              "reasons": [], "semantic_validation": "not performed"}
    if len(parts) < 3 or parts[0] not in RESONANCES:
        result["reasons"].append("Expected one resonance and a complete simple clause")
        return result
    if parts[1] not in SUBJECTS:
        result["reasons"].append("Only overt pronoun subjects are handled")
        return result
    pred = parts[-1]
    elements = pred.split("-")
    lemma, suffixes = elements[0], elements[1:]
    if lemma not in FRAMES:
        result["reasons"].append("Predicate has no new 8.4 overlay frame")
        return result
    frame = FRAMES[lemma]
    result["lemma"] = lemma
    result["frame_id"] = frame["id"]
    if any(x not in SUFFIXES for x in suffixes):
        result["reasons"].append("Unknown or unlicensed verbal affix; voice not permitted by this frame")
    if len({x for x in suffixes if x in {"te", "yu"}}) != len(
            [x for x in suffixes if x in {"te", "yu"}]) or sum(
            x in {"te", "yu"} for x in suffixes) > 1:
        result["reasons"].append("Multiple tense suffixes")
    if sum(x in {"se", "mo", "në"} for x in suffixes) > 1:
        result["reasons"].append("Multiple aspect suffixes")
    if sum(x in {"ki", "ho", "du"} for x in suffixes) > 1:
        result["reasons"].append("Multiple modality suffixes")
    if [ORDER[x] for x in suffixes if x in ORDER] != sorted(
            ORDER[x] for x in suffixes if x in ORDER):
        result["reasons"].append("Verbal suffixes out of order")
    middle = parts[2:-1]
    if middle and middle[-1] == "nu":
        middle = middle[:-1]
    if "nu" in middle:
        result["reasons"].append("Negation must immediately precede the predicate")
    objs = [x for x in middle if x.endswith("-m")]
    if frame["frame"] == "V1" and len(objs) != 1:
        result["reasons"].append("Exactly one overt -m object required for this V1 sense")
    if frame["frame"] == "V0" and objs:
        result["reasons"].append("This intransitive sense does not license an -m object")
    permitted = {r.split(":")[-1] for r in frame["licensed_optional_roles"]
                 if r.startswith(("recipient:", "instrument:", "location:"))}
    for x in middle:
        if x.endswith("-m"):
            continue
        if x.endswith(("-tu", "-shi", "-lo")):
            if "-" + x.rsplit("-", 1)[-1] not in permitted:
                result["reasons"].append("Unlicensed optional case on " + x)
        else:
            result["reasons"].append("Unparsed constituent: " + x)
    if not result["reasons"]:
        result["status"] = "structural_model_match"
        result["reasons"] = ["Compatible with the new restricted active frame; lexical object class and interpretation remain unverified"]
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sentence")
    args = ap.parse_args()
    print(json.dumps(analyze(args.sentence), ensure_ascii=False, indent=2))
