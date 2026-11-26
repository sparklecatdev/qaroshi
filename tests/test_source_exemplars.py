"""Opt-in 8.7 exemplar grammar: positive/negative, exact source, AST scope."""
import json
import subprocess
import sys
import unittest
from dataclasses import replace
from tools.grammar93.engine import Atom, Link, Sentence, Grammar, GrammarError
from tools.grammar93.source_exemplars import SourceExemplarGrammar, rows, CORPUS


class ExemplarGrammarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = SourceExemplarGrammar()
        cls.source = {p["id"]: p for p in rows(CORPUS)}

    def test_97_exact_source_examples_and_frozen_reviewed_baseline(self):
        self.assertEqual(len(self.g.source_frames),97)
        self.assertEqual(len(self.g.evidence_rows()),97)
        self.assertEqual(len(Grammar().license),25)
        self.assertEqual(len(self.g.license),122)
        for r in self.g.evidence_rows():
            with self.subTest(verb=r["lemma"]):
                self.assertEqual(self.source[r["source_example_id"]]["qaroshi"],
                                 r["source_sentence"])
                a=self.g.parse(r["source_sentence"])
                self.assertEqual(a.proposition.actor,"mi")
                self.assertEqual(a.proposition.patient,r["patient"])
                self.assertFalse(r["human_attested"])
                self.assertEqual(self.g.render(a),r["source_sentence"])
                with self.assertRaises(GrammarError):
                    Grammar().parse(r["source_sentence"])

    def test_all_exemplars_compose_in_restricted_tense_polarity_and_questions(self):
        count=0
        for r in self.g.evidence_rows():
            for tense in ("","te","yu"):
                for negative in (False,True):
                    for mood in ("statement","polar"):
                        s=Sentence(Atom("mi",r["lemma"],patient=r["patient"],
                                        tense=tense,negated=negative),
                                   mood=mood,resonance="hë" if mood=="polar" else "sen")
                        result=self.g.parse(self.g.render(s))
                        self.assertEqual(result,s)
                        evidence=self.g.semantic_view(result)["lexical_evidence"][0]
                        self.assertEqual(evidence["source_example_id"],r["source_example_id"])
                        self.assertEqual(evidence["kind"],"source_exemplar_not_general_frame")
                        count+=1
        self.assertEqual(count,1164)

    def test_reject_patient_actor_roles_voice_modal_aspect(self):
        a=Atom("mi","khukhiri",patient="shiwaro")
        bad=[
            replace(a,actor="ti"), replace(a,patient="kima"),
            replace(a,patient=None),replace(a,recipient="mara"),
            replace(a,source="naro"),replace(a,modal="du"),
            replace(a,modal="ho"),replace(a,modal="ki"),
            replace(a,aspect="se"),
        ]
        for candidate in bad:
            with self.subTest(candidate=candidate),self.assertRaises(GrammarError):
                self.g.render(Sentence(candidate))
        for text in (
            "sen mi shiwaro-m khukhiri-li.",
            "sen mi shiwaro-m khukhiri-te-ki.",
            "sen mi kima-m khukhiri.",
            "sen ti shiwaro-m khukhiri.",
            "sen mi shiwaro-tu shiwaro-m khukhiri.",
            "sen mi shiwaro-m khukhiri-ki-te.",
            "mi shiwaro-m khukhiri.",
        ):
            with self.subTest(text=text),self.assertRaises(GrammarError):
                self.g.parse(text)

    def test_cross_source_link_and_reporting_scope(self):
        src=Atom("mi","khukhiri",patient="shiwaro",tense="te")
        other=Atom("mi","khuwohu",patient="shërawëlon",tense="yu")
        for relation in ("after","before","when","if","counterfactual"):
            link=Link(relation,src,other)
            for attribution in ("","reported_to_speaker","unknown_whether"):
                s=Sentence(link,attribution=attribution)
                q=self.g.render(s)
                self.assertEqual(self.g.parse(q),s)
                semantic=self.g.semantic_view(s)
                self.assertEqual(len(semantic["lexical_evidence"]),2)
                if relation in ("if","counterfactual"):
                    self.assertFalse(semantic["matrix_event_asserted"])
                if attribution:
                    self.assertFalse(semantic["matrix_event_asserted"])

    def test_default_cli_stays_strict_while_opt_in_is_bounded(self):
        from tools.grammar93.cli import from_dict, to_dict
        s=Sentence(Atom("mi","khukhiri",patient="shiwaro",tense="te"))
        self.assertEqual(from_dict(to_dict(s)),s)
        with self.assertRaises(GrammarError):
            Grammar().render(s)
        self.assertEqual(self.g.parse(self.g.render(s)),s)
        for action, content in (("render", json.dumps(to_dict(s))),
                                ("parse", self.g.render(s))):
            with self.subTest(action=action):
                result = subprocess.run(
                    [sys.executable, "-m", "tools.grammar93.cli", "--source-exemplars", action, content],
                    capture_output=True, text=True, check=True,
                )
                self.assertIn("97 exact 8.7 source pairings", json.loads(result.stdout)["scope"])


if __name__=="__main__":
    unittest.main()
