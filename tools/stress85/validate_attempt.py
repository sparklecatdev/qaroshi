"""Recognize a small overt-pronoun subset of the 8.5 attempt frame."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "stress84"))
from validate_core import analyze, RESONANCES, SUBJECTS


def analyze_attempt(sentence):
    result = {"status": "outside_restricted_checker", "semantic_validation": "not performed"}
    parts = sentence.strip().rstrip(".!?").split()
    if len(parts) < 6 or parts[0] not in RESONANCES or parts.count("do") != 1:
        return result
    boundary = parts.index("do")
    embedded, matrix = parts[1:boundary], parts[boundary + 1:]
    if not embedded or not matrix or embedded[0] not in SUBJECTS or matrix[0] != embedded[0]:
        return result
    if matrix[-1].split("-")[0] != "kërawë":
        return result
    inner = analyze(" ".join([parts[0]] + embedded))
    outer = analyze(" ".join([parts[0]] + matrix))
    if inner["status"] == outer["status"] == "structural_model_match":
        result["status"] = "structural_model_match"
    return result
