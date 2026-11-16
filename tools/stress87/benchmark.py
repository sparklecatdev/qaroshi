#!/usr/bin/env python3
"""Report performance on transparent synthetic form checks, not language ability."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.stress87.validate import analyze  # noqa: E402


def cases():
    frames = json.loads((ROOT / "data/standard_8/valency_overlay_8_7.json").read_text(encoding="utf-8"))
    for frame in frames:
        yield "source", frame["source_sentence"], True
        obj, verb = frame["attested_object"], frame["lemma"]
        # Generated from the same examples; these are not an independent test set.
        for suffix in ("", "-te", "-yu-se", "-te-mo-ki-la"):
            yield "generated positive", f"sen ti {obj}-ri-m nu {verb}{suffix} he?", True
        for predicate in (verb + "-te-yu", verb + "-la-la", verb + "-ki-te", verb + "-xyz"):
            yield "generated negative", f"sen mi {obj}-m {predicate}.", False
        for obj_form in ("-m", obj, obj + "-m-m", "notaword-m"):
            yield "generated negative", f"sen mi {obj_form} {verb}.", False


def main():
    counts = {}
    failures = []
    for group, sentence, expected in cases():
        actual = analyze(sentence)["status"] == "structural_model_match"
        count = counts.setdefault(group, [0, 0])
        count[1] += 1
        count[0] += actual == expected
        if actual != expected:
            failures.append(sentence)
    for group, (passed, total) in counts.items():
        print(f"{group}: {passed}/{total}")
    print("Synthetic forms derived from the source examples; no semantic or human comprehension score.")
    if failures:
        print("Unexpected results:", *failures, sep="\n")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
