#!/usr/bin/env python3
"""Qaroshi 8.2: source-honest expressive-completeness review.

Produces per-item adjudication of all 500 stress challenges, structured
reviews for every non-general verb frame, lexical rulings/risk rankings,
grammar minimal pairs and authored connected prose. It does not manufacture
English/Qaroshi equivalences or independent learner responses.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import csv
import json
import re
import sys
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/stress82"
sys.path.insert(0, str(ROOT / "tools/stress81"))
sys.path.insert(0, str(ROOT / "tools/v28_34"))
sys.path.insert(0, str(ROOT / "tools/standard_8"))
from embedded_question import analyze as embedded_analyze
from reform_core import analyze_quantifier
from scope import analyze as double_scope

DOMAIN_RISK = {
    "daily": ("actor/patient selection, tense, and unknown lexical meanings",
              "Check exact subject, direct-object -m, verb sense, past -te and reported/conditional clauses."),
    "time_motion": ("two-event temporal order and aspect",
                    "Specify event order, before/after/while/until boundary and local negation."),
    "social_consent": ("permission, refusal, and participant scope",
                       "Keep asking separate from allowing; silence never entails consent."),
    "quantifier_logic": ("nonuniversal, negative, and scalar focus",
                         "Distinguish not-all from none and identify focus comparison class."),
    "evidentiality": ("reported vs witnessed vs inferred content",
                      "Never strengthen hearsay into direct observation or infer an unsupported claim."),
    "embedding_reference": ("relative-clause attachment and embedded polar scope",
                            "Resolve which noun is modified, whether vs that, and matrix negation."),
    "counterfactual_modal": ("irrealis tense and ability/permission/obligation",
                             "Disambiguate counterfactual, possible, allowed, necessary and actual."),
    "voice_valency": ("actor vs instrument, passive voice and patient licensing",
                      "Use passive actor -za, instrumental -shi and a reviewed verb frame."),
    "narrative_figures": ("literal quote, editorial metaphor and interpretation",
                          "Do not assert that a metaphor is a literal event or community-attested idiom."),
    "technical_precision": ("domain lexical sense, evidence and causal implication",
                            "Distinguish reported observation, recommendation, possibility and proof."),
}

# Each new editorial decision is a *restriction on an existing canonical gloss*,
# not a proposal to rename the word, infer natural use or promote an unreviewed compound.
NARROW_SENSES = {
    "balëwimorushi": "A percussive recording captures or documents percussion; not every preserved speech item is percussive.",
    "banoyinohowa": "Preventive safety describes protective practices or risk reduction; it does not guarantee danger is absent.",
    "banoyiwërawi": "A preventive plan is an intended prevention sequence, not a claim the outcome was achieved.",
    "banurëliro": "Wing practice is training involving wing movement; not automatically a religious practice or a performance.",
    "banurëmawo": "Wing ceremony denotes a ceremonial event concerning wings; this does not prove a traditional custom exists.",
    "banushërawërao": "Wing root is the anatomical attachment/base of a wing, not a root of the lexicon.",
    "banushëru": "Wing rhythm concerns patterned wing motion; it need not be musical rhythm.",
    "bayimokhimërawa": "Knitted garment is a piece of clothing made by knitting; not every piece of knitted fabric is clothing.",
    "bayimokhizhëmo": "Knitted fabric denotes textile material, not necessarily a finished garment.",
    "bedubopënawë": "Motor service denotes maintenance or assistance regarding a motor, not a motor serving someone socially.",
    "bepëqonoha": "Repair boundary is a limit or authorized scope of a repair, not automatically a physical wall.",
    "bepëqonohowa": "Repair safety concerns controls and hazards during repairs, not a guarantee of no injury.",
    "bepëqorënaro": "Repair task is a defined repair action, not evidence that the repair succeeded.",
    "bepëqorërawëho": "Repair schedule is a planned repair timeline, not proof that repairs happened.",
    "betashesinohowa": "Rescue safety refers to risk management during rescue; it is not a promise of success.",
    "bewahanohowa": "Maintenance safety is protection against maintenance hazards, not absence of every possible danger.",
    "bewahapënawë": "Maintenance service means maintenance work provided, not general social assistance.",
    "bewaharënaro": "Maintenance task is an assigned maintenance action, not evidence of its completion.",
    "bihuzugongërawëra": "Thermal pattern concerns structured temperature variation, not necessarily periodic recurrence.",
    "bihuzugonohowa": "Thermal safety means reducing risk from heat/cold, not proof of a risk-free environment.",
    "bihuzugorëmëra": "Thermal measurement is a measured physical thermal quantity, not subjective comfort.",
    "bihuzugoshënaroa": "Thermal signal conveys thermal information; it does not automatically imply a warning.",
    "bikhimirëlawë": "Session risk is risk relating to a session, not automatically physical injury.",
    "biwëpinohowa": "High-speed safety describes risk controls at speed, not an unconditional safety guarantee.",
    "bodedemërawi": "An interlinear example has aligned linguistic annotation lines; not every example is interlinear.",
    "budopengëmarawo": "Magnetic storage refers to storage using magnetic phenomena; stored data and energy are different contexts.",
}

# New original teaching texts use *existing documented grammar and lexemes*.
# They are deliberately assembled in short independent clauses. No one has
# independently verified naturalness or conversational social register.
PASSAGES = [
    ("Home and care", [
        ("sen mi naro-gu gura.", "I go home.", "direction -gu; basic travel frame"),
        ("sen mi naro-lo nëra.", "I remain at home.", "location -lo and stay"),
        ("sen mi kima-m këmë.", "I drink water.", "liquid patient -m"),
        ("sen sa haro he do mi nu sëmi.", "I do not know whether they are well.", "8.1 embedded whether; matrix negation"),
        ("sen mi mara-tu kima-m pëli.", "I offer/give water to a friend.", "theme -m and recipient -tu"),
        ("sen mi ti-m nashi.", "I deeply cherish you.", "cherishing need not be romantic"),
        ("sen sa haro he do mi sëmi.", "I know whether they are well.", "knowledge of answer, not truth of positive alternative"),
        ("sen mi naro-lo nëra.", "I remain at home.", "return to the location frame"),
    ]),
    ("When everyone is not the same", [
        ("sen ngënao qaro goro.", "Every Nardoragon flies.", "universal scope"),
        ("sen nëgëra qaro goro.", "Not every Nardoragon flies.", "counterexample; does not entail some fly"),
        ("sen shërano qaro goro.", "At least one Nardoragon flies.", "existential scope"),
        ("sen ngënao qaro nu goro.", "No Nardoragon flies.", "predicate negative under universal"),
        ("sen mi nu goro.", "I do not fly.", "simple preverbal negation"),
        ("sen mi naro-gu gura.", "I go home.", "travel not entailed to be flight"),
        ("sen mi naro-lo nëra.", "I stay at home.", "locative continuation"),
        ("sen mi nu shiri.", "I do not speak.", "absence of speech is not assent"),
    ]),
    ("Who protected the home?", [
        ("sen mi naro-m daru-te.", "I protected the home.", "active past, direct object -m"),
        ("sen naro mara-za daru-li-te.", "The home was protected by a friend.", "passive actor -za"),
        ("sen naro banu-shi daru-li-te.", "The home was protected using wings.", "instrument -shi, agent unexpressed"),
        ("sen sa haro do mi sëmi.", "I know that they are well.", "that-complement, factual knowledge"),
        ("sen sa haro he do mi sëmi.", "I know whether they are well.", "whether-complement does not entail they are well"),
        ("sen sa nu haro do mi sëmi.", "I know that they are not well.", "embedded negative, not matrix negative"),
        ("sen sa haro do mi nu sëmi.", "I do not know that they are well.", "matrix negative, not embedded negative"),
        ("sen mi ti-m nashi.", "I deeply cherish you.", "care independent of proof about third-party condition"),
    ]),
    ("Two ways of talking about friends", [
        ("sen shërano qaro ngënao mara-m tika.", "Some Nardoragon sees every friend.", "8.0 two-quantifier: some > every"),
        ("sen ngënao mara-m shërano qaro tika.", "Every friend is seen by some Nardoragon.", "8.0 two-quantifier: every > some"),
        ("sen mi mara-tu kima-m pëli.", "I give a friend water.", "theme -m and recipient -tu"),
        ("sen mi kima-m nu këmë.", "I do not drink water.", "does not imply I drink something else"),
        ("sen mi ti-m nashi.", "I cherish you deeply.", "not equivalent to romance"),
        ("sen mi naro-gu gura.", "I travel home.", "goal -gu"),
        ("sen mi naro-lo nëra.", "I stay at home.", "location -lo"),
        ("sen mi kima-m këmë.", "I drink water.", "liquid object"),
    ]),
]

def csvread(path):
    with Path(path).open(encoding="utf8", newline="") as f:
        return list(csv.DictReader(f))

def csvwrite(path, items):
    if not items: raise AssertionError("Empty output: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(items[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(items)

def jsonwrite(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf8")

def ensure_standard():
    p = ROOT / "data/standard_8/verb_audit_400.csv"
    if not p.exists():
        subprocess.run([sys.executable, str(ROOT / "tools/standard_8/build_standard.py")],
                       check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    return p

def build(output=OUT):
    ensure_standard()
    challenges = csvread(ROOT / "data/stress81/challenges_500.csv")
    previous = csvread(ROOT / "data/stress81/audit_results_500.csv")
    assert len(challenges) == len(previous) == 500
    by_id = {r["id"]: r for r in previous}
    assert len(by_id) == 500
    corpus = {r["id"]: r for r in csvread(ROOT / "corpus/parallel_sentences.csv")}
    words = {r["qaroshi"]: r for r in csvread(ROOT / "data/lexicon.csv")}
    frame = csvread(ROOT / "data/standard_8/verb_audit_400.csv")
    restricted = [r for r in frame if not r["general_frame_review"].startswith("yes")]
    assert len(frame) == 400 and len(restricted) == 375
    risk = csvread(ROOT / "data/standard_8/compound_risk_register.csv")
    decisions = csvread(ROOT / "data/standard_8/lexical_decisions.csv")
    assert len(risk) == 3108
    adopted = {r["canonical_word"]: r["adopted_sense_constraint"] for r in decisions
               if not r["decision"].startswith("retain canonical")}

    # 500 item-level adjudications: exact meaning-target, semantic operation,
    # currently licensed QR evidence and exactly which review remains open.
    review = []
    for c in challenges:
        old = by_id[c["id"]]
        assert c["english"] == old["english"] and c["feature"] == old["feature"]
        domain_risk, required = DOMAIN_RISK[c["domain"]]
        draft = old["normative_compositional_draft"]
        parsed = analyze_quantifier(draft) if draft else None
        if draft and not (draft.startswith("sen dëna ") or parsed.get("interpretable")):
            raise AssertionError("Unexpected unverified structural draft " + c["id"])
        coverage = ("limited_normative_composition_unratified" if draft
                    else "no_complete_Qaroshi_translation_yet")
        review.append({
            "id": c["id"], "domain": c["domain"], "family": c["scenario_family"],
            "variant": c["variant"], "feature": c["feature"],
            "english_target": c["english"],
            "source_artifact": "stress81/audit_results_500.csv",
            "source_grammar_feature": domain_risk,
            "target_semantic_structure": required,
            "qaroshi_draft": draft,
            "draft_lexical_witness": old["draft_basis"],
            "restricted_structural_readback": (parsed.get("logical_form") if parsed and parsed.get("interpretable") else ""),
            "complete_backtranslation_independently_checked": "no",
            "coverage": coverage,
            "word_selection_review": "required" if not draft else "source lexemes selected; new sentence unratified",
            "verb_frame_review": "required" if c["domain"] in {"daily","time_motion","counterfactual_modal","voice_valency","technical_precision"} else "as required by its predicate",
            "human_comprehension": "not administered",
            "new_language_gap_proven": "no",
            "required_next_adjudication": ("Blindly compare intended meaning with reconstruction" if draft
                                          else "Resolve lexical selection, argument structure and clause scope; create a sourced QR draft"),
            "review_status": "pending_human_semantics_and_context",
        })
    csvwrite(output / "case_adjudications_500.csv", review)

    # Every restricted verb gets its OWN source and three distinct decisions,
    # not a generic blanket permission to use passive/causative freely.
    verb_rows, verb_probes = [], []
    for r in restricted:
        sid = r["example_source_id"]
        e = corpus.get(sid)
        if sid:
            assert e is not None and e["qaroshi"] == r["example_qaroshi"]
        verb_rows.append({
            "lemma": r["lemma"], "dictionary_id": r["dictionary_id"],
            "reference_gloss": r["reference_gloss"],
            "prior_linguistic_license": r["decision"],
            "source_id": sid,
            "source_qaroshi": r["example_qaroshi"],
            "source_english": r["example_english"],
            "exact_object_lemma": r["exact_documented_object_root"],
            "general_object_class": "unadjudicated",
            "general_passive": "unadjudicated",
            "general_causative": "unadjudicated",
            "authority": "recorded example only; not a full argument frame",
            "individual_review_result": "retain exact source license; withhold generalization",
            "full_general_frame_approved_by_8_2": "no",
            "human_comprehension": "not conducted",
        })
        for mode in ("different patient class", "passive agent -za", "causative actor -ru"):
            verb_probes.append({
                "lemma": r["lemma"], "source_id": sid,
                "review_probe": mode,
                "source_qaroshi": r["example_qaroshi"],
                "new_candidate_qaroshi": "",
                "proposed_test": "Construct a contrasting novel clause with the same sense and test interpretation.",
                "adopted_construction": "none without separate valency adjudication",
                "status": "open; no invented translation",
            })
    assert len(verb_rows) == 375 and len(verb_probes) == 1125
    csvwrite(output / "verb_reviews_375.csv", verb_rows)
    csvwrite(output / "verb_contrast_trials_1125.csv", verb_probes)

    # Exact new editorial sense constraints. Never change a frozen spelling.
    for w in NARROW_SENSES:
        if w not in words:
            raise AssertionError("Narrow sense word not in canonical dictionary: " + w)
    newdec = []
    for w, definition in sorted(NARROW_SENSES.items()):
        if w in adopted:
            continue  # preserve older approved constraints rather than overwriting
        newdec.append({"lemma": w, "canonical_id": words[w]["id"],
                       "canonical_gloss": words[w]["english"],
                       "approved_editorial_sense_boundary": definition,
                       "editorial_status": "8.2 new narrow lexical interpretation",
                       "historical_spelling_changed": "no",
                       "independent_speaker_attestation": "none claimed"})
    csvwrite(output / "new_lexical_boundaries.csv", newdec)
    prioritized = []
    for r in risk:
        word = r["word"]
        state = ("already_adopted_standard_8" if word in adopted else
                 "adopted_new_narrow_8_2" if word in NARROW_SENSES else
                 "unresolved_component_polysemy")
        rule = adopted[word] if word in adopted else NARROW_SENSES.get(word, "")
        prioritized.append({
            "word": word, "canonical_id": r["canonical_id"],
            "current_meaning": r["meaning"], "risk": r["risk"],
            "decision_status": state, "sense_boundary": rule,
            "needs_speaker_judgment": "yes",
            "preserve_spelling": "yes",
            "false_friend_warning": "Component English glosses are not interchangeable across domains.",
        })
    assert len(prioritized) == 3108
    csvwrite(output / "compound_review_3108.csv", prioritized)

    # 8.1 embedded-question recognizer generates real paired QR strings,
    # parses BOTH forms, and checks the semantic interpretation changed.
    pairs = []
    def pair(category, a, b, gloss_a, gloss_b, witness):
        if a == b or gloss_a == gloss_b:
            raise AssertionError("Non-contrastive pair " + category)
        pairs.append({
            "id": "MP82-%04d" % (len(pairs) + 1), "category": category,
            "qaroshi_A": a, "qaroshi_B": b,
            "meaning_A": gloss_a, "meaning_B": gloss_b,
            "normative_witness": witness, "status": "source-rule-derived; not independent speaker attestation",
        })
    pronouns = ["mi", "ti", "sa", "naru", "muru", "tiri", "sari"]
    predicates = ["haro", "goro"]
    def embed(sub, pred, inneg=False, matrixneg=False, innerhe=False, finalhe=False):
        return ("sen " + sub + (" nu" if inneg else "") + " " + pred
                + (" he" if innerhe else "") + " do mi"
                + (" nu" if matrixneg else "") + " sëmi"
                + (" he?" if finalhe else "."))
    witness = "8.1 adopted he/do embedded-polar clause boundary and clause-local nu"
    for sub, pred, inneg, matrixneg, matrixq in product(pronouns, predicates, (False,True), (False,True), (False,True)):
        a = embed(sub,pred,inneg,matrixneg,False,matrixq)
        b = embed(sub,pred,inneg,matrixneg,True,matrixq)
        pa,pb=embedded_analyze(a),embedded_analyze(b)
        if not pa["supported"] or not pb["supported"]:raise AssertionError((a,b,pa,pb))
        pair("embedded that / whether", a,b,pa["meaning_gloss"],pb["meaning_gloss"],witness)
    for sub,pred,question,polar in product(pronouns,predicates,(False,True),(False,True)):
        a=embed(sub,pred,True,False,polar,question)
        b=embed(sub,pred,False,True,polar,question)
        pa,pb=embedded_analyze(a),embedded_analyze(b)
        if not pa["supported"] or not pb["supported"]:raise AssertionError((a,b))
        pair("matrix vs subordinate negation",a,b,pa["meaning_gloss"],pb["meaning_gloss"],witness)
    for sub,pred,innerneg,matrixneg,polar in product(pronouns,predicates,(False,True),(False,True),(False,True)):
        a=embed(sub,pred,innerneg,matrixneg,polar,False)
        b=embed(sub,pred,innerneg,matrixneg,polar,True)
        pa,pb=embedded_analyze(a),embedded_analyze(b)
        if not pa["supported"] or not pb["supported"]:raise AssertionError((a,b))
        pair("matrix statement vs question",a,b,pa["meaning_gloss"],pb["meaning_gloss"],witness)
    # Existing 49 licensed quantifier compositions give 96 more genuine
    # Qaroshi contrasting sentence pairs, not merely English prompts.
    by_family = defaultdict(list)
    for r in review:
        if r["domain"] == "quantifier_logic" and r["qaroshi_draft"]:
            by_family[r["family"]].append(r)
    for family, items in sorted(by_family.items()):
        for a,b in combinations(items,2):
            pair("quantifier and focus",a["qaroshi_draft"],b["qaroshi_draft"],
                 a["english_target"],b["english_target"],
                 "8.0/28-34 quantified NP rules, 8.1 individually composed editorial draft")
    if len(pairs) < 350:raise AssertionError("Insufficient verified contrastive Qaroshi pairs: "+str(len(pairs)))
    csvwrite(output / "qaroshi_minimal_pairs.csv",pairs)

    # Connected passages are original EDITORIAL training texts with linewise
    # target English and named grammar license. No fabricated observed dialogue.
    lines=[]; passage_meta=[]
    for no,(title,utterances) in enumerate(PASSAGES,1):
        passage_meta.append({"passage_id":f"P82-{no:02d}", "title":title,
                             "line_count":len(utterances),
                             "status":"editorial controlled composition; independent comprehension not tested"})
        for i,(qr,en,why) in enumerate(utterances,1):
            if not qr.startswith("sen "):raise AssertionError("Unexpected unmarked complete sentence")
            # Parsing is only claimed when an 8.1 embedded or 28-34 quantifier
            # rule has actually recognized the input.
            parsed = embedded_analyze(qr) if " do " in qr else analyze_quantifier(qr)
            support = ("embedded_polar_recognized" if parsed.get("supported") and " do " in qr
                       else "simple_quantifier_recognized" if parsed.get("interpretable") else
                       "editorially analyzed by listed grammar rule; not independently parser-certified")
            lines.append({"passage_id":f"P82-{no:02d}","title":title,
                          "line":i,"qaroshi":qr,"english_target":en,
                          "grammar_annotation":why,"verification_scope":support,
                          "source_type":"new authored practice composition",
                          "speaker_attested":"no"})
    csvwrite(output / "connected_passages.csv",lines)
    jsonwrite(output / "passage_catalog.json",passage_meta)

    manifest={
        "edition":"Qaroshi 8.2 candidate: expressive testing and evidence-limited semantic repairs",
        "challenges_reviewed":len(review),
        "complete_unratified_rule_based_drafts":sum(bool(r["qaroshi_draft"]) for r in review),
        "remaining_without_complete_Qaroshi_draft":sum(not bool(r["qaroshi_draft"]) for r in review),
        "independent_semantic_backtranslations":0,
        "human_comprehension_test_participants":0,
        "fully_general_verb_frames_newly_approved":0,
        "verb_restriction_rows":len(verb_rows),
        "verb_unvalidated_contrast_trials":len(verb_probes),
        "new_lexical_sense_constraints":len(newdec),
        "compound_risk_reviews":len(prioritized),
        "unresolved_compound_risks":sum(r["decision_status"]=="unresolved_component_polysemy" for r in prioritized),
        "normative_structural_minimal_pairs":len(pairs),
        "editorial_passage_lines":len(lines),
        "frozen_standard_modified":False,
        "limits":"Not all 500 translated; verb generalizations, speaker judgments and blind comprehension remain open.",
        "generated_sha256": {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(output.iterdir()) if p.is_file() and p.name!="manifest.json"},
    }
    jsonwrite(output / "manifest.json",manifest)
    return manifest

if __name__ == "__main__":
    print(json.dumps(build(),ensure_ascii=False,indent=2))
