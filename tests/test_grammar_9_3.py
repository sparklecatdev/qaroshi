"""9.3 reusable syntax tests: full 25-curated-frame roundtrips and rejection.

These validate only the specifically licensed subset of Qaroshi; they never
claim general parsing of 30k headwords or human semantic equivalence.
"""
from __future__ import annotations
import unittest
from dataclasses import replace

from tools.grammar93.engine import Grammar,GrammarError,Atom,Link,Sentence

class TypedGrammar93(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=Grammar()

    def example(self,verb):
        g=self.g
        rule=g.license[verb]
        def choose(role):
            allowed=rule.get(role,[])
            for item in g.lex.values():
                if item["class"] in allowed:
                    return item["form"]
            return None
        return Atom(actor=choose("subject"),verb=verb,
                    patient=choose("patient"),recipient=choose("recipient"),
                    tense="te")

    def test_all_25_curated_verbs_have_real_structural_licenses(self):
        self.assertEqual(len(self.g.curated),25)
        self.assertEqual(set(self.g.curated),set(self.g.license))
        for verb in self.g.curated:
            with self.subTest(verb=verb):
                atom=self.example(verb)
                q=self.g.render(Sentence(atom))
                self.assertEqual(self.g.parse(q),Sentence(atom))
                sem=self.g.semantic_view(Sentence(atom))
                self.assertEqual(sem["roles"][0]["verb"],verb)
                self.assertEqual(sem["matrix_event_asserted"],True)
                self.assertEqual(sem["source_boundary"],"exact 9.3 lexical license; no independent speaker verification")

    def test_tense_aspect_modality_and_negation_combine_in_order(self):
        source=self.example("tika")
        for tense in ("","te","yu"):
            for aspect in ("","se","mo","në"):
                for modal in ("","ki","ho","du"):
                    for neg in (False,True):
                        atom=replace(source,tense=tense,aspect=aspect,modal=modal,negated=neg)
                        s=Sentence(atom)
                        self.assertEqual(self.g.parse(self.g.render(s)),s)
                        sem=self.g.semantic_view(s)
                        self.assertEqual(sem["roles"][0]["modal"],modal)
                        self.assertEqual(sem["roles"][0]["negated"],neg)

    def test_person_and_patient_cross_combination_without_case_templates(self):
        for actor in ("mi","ti","mara","sa","qaro"):
            for patient in ("ti","mara","qaro","mi","sa","shima"):
                atom=Atom(actor=actor,patient=patient,verb="tika",tense="yu")
                s=Sentence(atom)
                q=self.g.render(s)
                self.assertEqual(self.g.parse(q),s)
        self.assertEqual(self.g.parse("sen mi mara-m tika-te.").proposition,
                         Atom("mi","tika","mara",tense="te"))

    def test_transfer_distinguishes_patient_from_recipient(self):
        a=Atom("mi","pëli",patient="kima",recipient="mara",tense="te")
        self.assertEqual(self.g.render(Sentence(a)),"sen mi mara-tu kima-m pëli-te.")
        self.assertEqual(self.g.parse("sen mi mara-tu kima-m pëli-te.").proposition,a)
        with self.assertRaises(GrammarError):
            self.g.render(Sentence(replace(a,patient="mara",recipient="kima")))
        with self.assertRaises(GrammarError):
            self.g.render(Sentence(replace(a,recipient=None)))
        with self.assertRaises(GrammarError):
            self.g.render(Sentence(replace(a,patient=None)))

    def test_embedding_report_ignorance_vs_direct_assertion_and_question(self):
        atom=Atom("mi","tika",patient="mara",tense="te")
        assertive=Sentence(atom)
        reported=Sentence(atom,attribution="reported_to_speaker")
        unknown=Sentence(atom,attribution="unknown_whether")
        polar=Sentence(atom,resonance="hë",mood="polar")
        witnessed=Sentence(atom,evidential="si")
        inferred=Sentence(atom,evidential="ye")
        for sentence in (assertive,reported,unknown,polar,witnessed,inferred):
            q=self.g.render(sentence)
            self.assertEqual(self.g.parse(q),sentence)
        self.assertTrue(self.g.semantic_view(assertive)["matrix_event_asserted"])
        for sentence in (reported,unknown,polar):
            self.assertFalse(self.g.semantic_view(sentence)["matrix_event_asserted"])
        self.assertEqual(self.g.semantic_view(reported)["report_source"],"indefinite_person")
        self.assertEqual(self.g.semantic_view(unknown)["speech_act"],"ignorance_of_whether")
        self.assertEqual(self.g.semantic_view(inferred)["evidential"],"ye")
        self.assertNotEqual(self.g.render(reported),self.g.render(assertive))

    def test_unseen_clausal_event_compositions_without_fixed_family_ids(self):
        a=Atom("mi","tika",patient="mara",tense="te")
        b=Atom("ti","këmë",patient="kima",tense="te")
        for relation in ("after","before","when","if","counterfactual"):
            p=Link(relation,a,b)
            for scope in ("","reported_to_speaker","unknown_whether"):
                s=Sentence(p,attribution=scope)
                q=self.g.render(s)
                self.assertEqual(self.g.parse(q),s)
                sem=self.g.semantic_view(s)
                self.assertEqual(sem["relation"],relation)
                self.assertFalse(sem["conditional_antecedent_asserted"]) if relation in ("if","counterfactual") else None
                if scope:
                    self.assertFalse(sem["matrix_event_asserted"])
                if relation=="counterfactual":
                    self.assertTrue(q.endswith(" qinë.")) if not scope else self.assertIn(" qinë",q)

    def test_invalid_grammatical_forms_and_roles_abstain(self):
        bad=[
            "sen mi kima-m shëma-te.",
            "sen kima ti-m tika-te.",
            "sen mi kima-m pëli-te.",
            "sen mi mara-tu kima-m goro-te.",
            "sen mi kima-m nu mara-tu pëli-te.",
            "sen mi mara-m tika-ki-te.",
            "sen mi mara-m tika-te-te.",
            "sen mi mara-m tika-yu-te.",
            "sen mi mara-m tika-te-ki-du.",
            "sen mi mara-m mara-m tika-te.",
            "sen mi mara-m tika-ru-te.",
            "sen mi mara-m xyz-te.",
            "mi mara-m tika-te.",
            "sen mi mara-m tika-te he?",
            "hë mi mara-m tika-te.",
            "sen mi mara-m tika-te-do.",
            "sen mi mara-m tika-te hu ye.",
            "sen mi mara-m tika-te do yano mi-tu shiri-te si.",
        ]
        for q in bad:
            with self.subTest(q=q),self.assertRaises(GrammarError):
                self.g.parse(q)

    def test_unlicensed_voice_and_semantic_category_swaps_rejected(self):
        with self.assertRaises(GrammarError):
            self.g.parse("sen mi mara-m tika-li-te.")
        for candidate in (
            Atom("mi","këmë",patient="shima"),
            Atom("mi","mali",patient="kima"),
            Atom("mi","goro",patient="mara"),
            Atom("mi","rawo",patient="nëpoqo"),
            Atom("mi","shëma",patient="kima"),
            Atom("mi","shëliro",patient="nëpoqo"),
        ):
            with self.assertRaises(GrammarError):
                self.g.render(Sentence(candidate))

    def test_can_parse_licensed_case_order_but_refuses_noncanonical_written_order(self):
        s="sen mi mara-tu kima-m pëli-te."
        self.assertEqual(self.g.parse(s).proposition.recipient,"mara")
        self.assertEqual(self.g.parse(s).proposition.patient,"kima")
        with self.assertRaises(GrammarError):
            self.g.parse("sen mi kima-m mara-tu pëli-te.")

if __name__=="__main__":unittest.main()
