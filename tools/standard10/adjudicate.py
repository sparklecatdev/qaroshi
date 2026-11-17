#!/usr/bin/env python3
"""Join consented first-pass reader CSVs to a PRIVATE facilitator worksheet.

Never publish this output: it contains the editorial answer key and reader
responses. This tool DOES NOT auto-adjudicate or assert independence. Human
reviewers must fill semantic_rating and adjudicator_anonymous_code manually.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

READER_FIELDS = ("item_id", "reader_anonymous_code", "first_pass_english_paraphrase",
                 "actor_object_scope_notes", "uncertainty_0_to_3",
                 "reader_confirmed_no_key_access")
REQUIRED_KEY = ("item_id", "contextual_editorial_english", "literal_editorial_english")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def combine(response_files: list[Path], key_file: Path, output: Path) -> dict:
    if not response_files:
        raise ValueError("At least one private participant response file required")
    key_rows = rows(key_file)
    if len(key_rows) != 80 or len({x.get("item_id") for x in key_rows}) != 80:
        raise ValueError("Facilitator key must have exactly 80 distinct study items")
    if any(not all(k in x for k in REQUIRED_KEY) for x in key_rows):
        raise ValueError("Facilitator source-English key columns missing")
    key = {x["item_id"]: x for x in key_rows}
    joined, seen = [], set()
    for filename in response_files:
        records = rows(filename)
        if not records:
            raise ValueError("Empty participant responses: " + filename.name)
        if any(not all(k in record for k in READER_FIELDS) for record in records):
            raise ValueError("Participant export schema mismatch: " + filename.name)
        for response in records:
            item_id = response["item_id"]
            reader = response["reader_anonymous_code"].strip()
            paraphrase = response["first_pass_english_paraphrase"].strip()
            disclosure = response["reader_confirmed_no_key_access"]
            uncertainty = response["uncertainty_0_to_3"]
            if item_id not in key:
                raise ValueError("Unknown trial item " + item_id)
            if not reader or not paraphrase:
                raise ValueError("Missing anonymous code or interpretation")
            if disclosure not in {"yes", "no", "unsure"}:
                raise ValueError("Unrecognized answer-key exposure declaration")
            if uncertainty not in {"0", "1", "2", "3"}:
                raise ValueError("Invalid uncertainty rating")
            pair = (reader, item_id)
            if pair in seen:
                raise ValueError("Duplicate participant and trial item: " + repr(pair))
            seen.add(pair)
            source = key[item_id]
            joined.append({
                **{k: response[k] for k in READER_FIELDS},
                "adjudicator_anonymous_code": "",
                "semantic_rating": "",
                "adjudicator_notes": "",
                "facilitator_contextual_editorial_english": source["contextual_editorial_english"],
                "facilitator_literal_editorial_english": source["literal_editorial_english"],
                "source_scene_id": source.get("scene_id", ""),
                "status": "PRIVATE_UNRATED_HUMAN_ADJUDICATION_PENDING",
            })
    joined.sort(key=lambda x: (x["reader_anonymous_code"], x["item_id"]))
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(joined[0])
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(joined)
    return {
        "private_unrated_reader_responses": len(joined),
        "anonymous_reader_codes": len({x["reader_anonymous_code"] for x in joined}),
        "items_covered": len({x["item_id"] for x in joined}),
        "adjudications_supplied": 0,
        "output": str(output),
        "warning": "PRIVATE answer-bearing worksheet; do not upload to a public repository. Complete adjudicator fields by actual humans. A program cannot authenticate their independence.",
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--responses", nargs="+", type=Path, required=True)
    p.add_argument("--key", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(combine(args.responses, args.key, args.out), indent=2))
