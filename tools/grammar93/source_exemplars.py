"""Evidence-gated extension of the original, untouched Standard 9.3 grammar.

Exactly 97 prior Standard 8.7 V1 source examples are accepted as exact
actor=mi, patient=one recorded canonical word, verb=one recorded verb.
Only basic morphosyntactic operators compose on top of that exemplar.
No arbitrary verb-object substitutions, extended valency, voices, modals,
independently reviewed meanings, or fluent-speaker acceptance are implied.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from tools.grammar93.engine import Atom, Grammar, GrammarError, Link, Sentence

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "data/standard_8/valency_overlay_8_7.json"
CORPUS = "corpus/parallel_sentences.csv"
LEXICON = "data/lexicon.csv"


def rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


class SourceExemplarGrammar(Grammar):
    """Opt-in subset: 25 reviewed verbs plus 97 exact recorded V1 pairings."""

    def __init__(self):
        super().__init__()  # validates the preserved 25-verb subset first
        src = json.loads((ROOT / SOURCE).read_text(encoding="utf-8"))
        lex = {w["qaroshi"]: w for w in rows(LEXICON)}
        by_id = {w["id"]: w for w in lex.values()}
        phrases = {p["id"]: p for p in rows(CORPUS)}
        if len(src) != 97 or len(lex) != 30000 or len(phrases) != 4383:
            raise GrammarError("Historical source counts changed; refuse exemplar expansion")
        if len(by_id) != len(lex):
            raise GrammarError("Duplicate canonical IDs")
        self.source_frames: dict[str, dict] = {}
        seen_ids: set[str] = set()
        for r in src:
            verb, patient, id_ = r["lemma"], r["attested_object"], r["id"]
            source = phrases.get(r["source_example_id"])
            if (verb in self.license or verb in self.source_frames or id_ in seen_ids
                or r["frame"] != "V1" or r["human_observed"] is not False
                or not r["semantic_boundary"].strip()
                or verb not in lex or patient not in lex
                or lex[verb]["id"] != r["dictionary_id"]
                or lex[patient]["id"] != r["attested_object_dictionary_id"]
                or not source
                or source["qaroshi"] != r["source_sentence"]
                or source["qaroshi"] != f"sen mi {patient}-m {verb}."):
                raise GrammarError("Source exemplar must match exact canonical verb, object, and corpus line: " + id_)
            seen_ids.add(id_)
            self.source_frames[verb] = r
            # Narrow synthetic selection classes do not license substitutions:
            # noun() below checks the *exact* actor and object for this verb.
            self.license[verb] = {
                "subject": ["source_actor_only_mi"],
                "patient": ["source_patient_only_" + verb],
                "sense": r["dictionary_gloss"],
                "note": "8.7 exact source exemplar; not a fully reviewed general verb frame",
            }
            self.curated[verb] = {
                "lemma": verb, "frame": "V1",
                "required_roles": ["subject:documented_actor", "object:-m"],
                "source_id": id_,
            }
            if patient not in self.lex:
                self.lex[patient] = {
                    "form": patient, "class": "source_object_only",
                    "gloss": lex[patient]["english"],
                }
        if len(self.source_frames) != 97:
            raise GrammarError("Incomplete source-exemplar inventory")

    def noun(self, form: str, role: str, verb: str) -> None:
        source = self.source_frames.get(verb)
        if source:
            if role == "subject" and form == "mi":
                return
            if role == "patient" and form == source["attested_object"]:
                return
            raise GrammarError(
                "8.7 verb is licensed only with exact source actor mi "
                "and source patient " + source["attested_object"])
        return super().noun(form, role, verb)

    def validate_atom(self, a: Atom) -> None:
        super().validate_atom(a)
        if a.verb in self.source_frames:
            if a.aspect or a.modal:
                raise GrammarError(
                    "8.7 exemplar does not license extra aspect/modality; "
                    "only unmarked, past or future plus negation and speech-act scope")
            if a.tense not in ("", "te", "yu"):
                raise GrammarError("Unlicensed exemplar tense")
            if (a.recipient or a.goal or a.location or a.source or a.comitative):
                raise GrammarError("8.7 exemplar has no additional valency slot")

    def evidence_rows(self) -> list[dict]:
        """Small verified read-only public records for the Wiki learning tool."""
        return [{
            "source_id": r["id"],
            "lemma": r["lemma"],
            "dictionary_id": r["dictionary_id"],
            "gloss": r["dictionary_gloss"],
            "domain": r["domain"],
            "patient": r["attested_object"],
            "patient_id": r["attested_object_dictionary_id"],
            "source_example_id": r["source_example_id"],
            "source_sentence": r["source_sentence"],
            "source_english": r["source_translation"],
            "semantic_boundary": r["semantic_boundary"],
            "review_status": "bounded_source_exemplar_not_general_frame",
            "human_attested": False,
        } for r in self.source_frames.values()]

    def semantic_view(self, s: Sentence) -> dict:
        out = super().semantic_view(s)
        atoms = ([s.proposition] if isinstance(s.proposition, Atom)
                 else [s.proposition.first, s.proposition.second])
        out["lexical_evidence"] = [{
            "verb": a.verb,
            "kind": "source_exemplar_not_general_frame" if a.verb in self.source_frames
                    else "fully_reviewed_9_3_frame",
            "source_id": self.source_frames[a.verb]["id"] if a.verb in self.source_frames else None,
            "source_example_id": (self.source_frames[a.verb]["source_example_id"]
                                  if a.verb in self.source_frames else None),
        } for a in atoms]
        out["independent_speaker_meaning_attestations"] = 0
        out["source_boundary"] = (
            "25 fully reviewed 9.3 verbs plus 97 exact source-bound 8.7 verb-object pairs; "
            "additional morphology is formal composition, not independently approved usage"
        )
        return out


if __name__ == "__main__":
    g = SourceExemplarGrammar()
    print(json.dumps({
        "original_reviewed_verb_frames": 25,
        "additional_exact_source_pairings": len(g.source_frames),
        "independent_speaker_meaning_attestations": 0,
        "example": g.render(Sentence(Atom("mi", "khukhiri", patient="shiwaro", tense="te"))),
    }, indent=2, ensure_ascii=False))
