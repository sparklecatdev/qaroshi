#!/usr/bin/env python3
"""Qaroshi 8.3: evidence-checked translation drafts and normative audit.

This edition is an editorial constructed-language development tool. It never
converts a lexical match into a claim of human validation. Every stress prompt
gets an explicit semantic/lexical/grammar coverage record and a reversible
translation *proposal* only where all claimed elements can be traced.
"""
from __future__ import annotations

import collections
import csv
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "stress83"
sys.path.insert(0, str(ROOT / "tools/stress82"))
sys.path.insert(0, str(ROOT / "tools/standard_8"))
sys.path.insert(0, str(ROOT / "tools/stress81"))
from build_review import build as build_82
from embedded_question import analyze as analyze_embedded
from scope import analyze as analyze_double

def rows(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def csvout(path, data):
    assert data
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, list(data[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(data)

def jsout(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 -]", "", s.casefold())).strip()

class Glosses:
    """Source-linked lexical suggestions, not indiscriminate English homonyms."""
    def __init__(self):
        self.lex = rows(ROOT / "data/lexicon.csv")
        self.by_qr = {r["qaroshi"]: r for r in self.lex}
        self.index = collections.defaultdict(list)
        for r in self.lex:
            for split in re.split(r";|\s+/\s+|,\s+(?=[a-z]{3})", r["english"]):
                split = re.sub(r"\([^)]*\)", "", split)
                key = norm(split)
                if not key or len(key) < 3 or key.startswith("see "):
                    continue
                self.index[key].append(r)
        self.verified = {
            # Existing source senses, NOT new invented spellings.
            ("noun","friend"):"mara",("noun","home"):"naro",
            ("noun","water"):"kima",("noun","nardoragon"):"qaro",
            ("verb","fly"):"goro",("verb","travel"):"gura",
            ("verb","drink"):"këmë",("verb","give"):"pëli",
            ("verb","say"):"shiri",("verb","speak"):"shiri",
            ("verb","know"):"sëmi",("verb","see"):"tika",
            ("verb","protect"):"daru",("verb","ask"):"sharoa",
            ("verb","stay"):"nëra",("verb","rest"):"nëru",
            ("adjective","well"):"haro",("adjective","good"):"haro",
        }
        for (pos,_),word in self.verified.items():
            assert word in self.by_qr,word
    def lookup(self, phrase, pos):
        phrase = norm(phrase)
        phrase = re.sub(r"^(the|a|an|this|that) ", "", phrase)
        if (pos,phrase) in self.verified:
            x=self.by_qr[self.verified[(pos,phrase)]]
            return x, "explicit previously documented form"
        trials=[phrase]
        if phrase.endswith("ies"):trials.append(phrase[:-3]+"y")
        if phrase.endswith("s") and not phrase.endswith("ss"):trials.append(phrase[:-1])
        if pos=="v":
            if phrase.endswith("ing"):trials.extend((phrase[:-3],phrase[:-3]+"e"))
            if phrase.endswith("ied"):trials.append(phrase[:-3]+"y")
            if phrase.endswith("ed"):trials.extend((phrase[:-2],phrase[:-1]))
        unique=[]
        for t in trials:
            if t and t not in unique:unique.append(t)
        candidates=[]
        for key in unique:
            for r in self.index.get(key,[]):
                if r["pos"] == pos:
                    candidates.append((int(r["type"]!="headword"),len(r["english"]),r))
        if candidates:
            r=min(candidates,key=lambda t:(t[0],t[1],t[2]["id"]))[2]
            return r, "exact source English indexing sense (not context certified)"
        return None,"no exact dictionary index sense"
    def choose(self,phrase,pos):
        x,note=self.lookup(phrase,pos)
        return (x["qaroshi"],x["id"],note) if x else (None,None,note)

def ingredient(qword,case,source_id):
    return qword+case if qword else None

def qr_sentence(lex,actor,verb,patient=None,tense="-te",negative=False,question=False,voice=False,agent=None,instrument=None):
    a=lex.choose(actor,"n") if actor else (None,None,"")
    v=lex.choose(verb,"v")
    b=lex.choose(patient,"n") if patient else (None,None,"")
    if not a[0] or not v[0] or (patient and not b[0]):
        return None,([("actor",actor,a),("verb",verb,v),("patient",patient,b)] if patient else
                      [("actor",actor,a),("verb",verb,v)])
    if voice:
        args=[b[0]]
        if agent:args.append(a[0]+"-za")
        if instrument:
            inst=lex.choose(instrument,"n")
            if inst[0]:args.append(inst[0]+"-shi")
            else:return None,[("instrument",instrument,inst)]
        pred=v[0]+"-li"+tense
    else:
        args=[a[0]]
        if patient:args.append(b[0]+"-m")
        if instrument:
            inst=lex.choose(instrument,"n")
            if inst[0]:args.append(inst[0]+"-shi")
            else:return None,[("instrument",instrument,inst)]
        pred=v[0]+tense
    q=("hë " if question else "sen ")+" ".join(args)+(" nu" if negative else "")+" "+pred+(" he?" if question else ".")
    return q,[("actor",actor,a),("verb",verb,v),("patient",patient,b)]

def parse_simple(raw):
    """Conservative closed-form extraction for English controlled assertions."""
    s=raw.strip(" .!?")
    patterns=[
        r"^(the|a) ([\w-]+) ([\w-]+) (?:the|a) ([\w-]+)$",
        r"^(the|a) ([\w-]+) ([\w-]+)$",
    ]
    for i,p in enumerate(patterns):
        m=re.match(p,s,re.I)
        if m:
            return {"actor":m.group(2).lower(),"verb":m.group(3).lower(),
                    "patient":m.group(4).lower() if i==0 else None}
    return None

def draft_for(case,lex):
    """Generate *editorial hypotheses* with explicit compatibility limits."""
    old=case["qaroshi_draft"]
    if old:
        return old,"8.1 adopted-rule composition retained","no source-independent semantic validation","",[]
    en=case["english_target"]
    family=case["family"]
    variant=int(case["variant"])
    domain=case["domain"]
    parts=family.split("-")
    idx=int(parts[-1])-1
    # Get the 100 controlling scenarios from the original source authoring code.
    import scenarios
    sem=None
    if domain=="daily":
        who,past,bare,part,consequence=scenarios.DAILY[idx]
        actor=who.removeprefix("the ").lower()
        # The 8.1 challenge scenarios explicitly supply one base action.
        a=re.fullmatch(r"([a-z]+) the (.+)",bare)
        if a:
            action,obj=a.groups()
            if variant in (1,2,3):
                q,ingredients=qr_sentence(lex,actor,action,obj,negative=variant==2,question=variant==3)
                if q:return q,"simple SOV with past -te, object -m and (nu/he)","verify predicate and patient sense", "",ingredients
            if variant==4:
                q,ingredients=qr_sentence(lex,actor,action,obj)
                if q:
                    embedded=q.removeprefix("sen ").removesuffix(".")
                    return "sen "+embedded+" do sa mi-tu shiri-te.", "content-clause do plus reported speech", "speaker and recipient attribution require individual semantic checking","",ingredients
        sem="daily action requires exact verb, agent and patient dictionary senses"
    elif domain=="voice_valency":
        who,patient,past,bare,part,tool=scenarios.VALENCY[idx]
        if variant in (1,2,3,4,5):
            passive=variant in (2,5)
            inst=tool.removeprefix("a ") if variant==3 else None
            q,ingredients=qr_sentence(lex,who,bare,patient,
                    negative=variant==4,question=variant==5,
                    voice=passive,agent=passive,instrument=inst)
            if q:
                license="source noun/verb roots and passive/agent case -za" if passive else "SOV transitive form and attested cases"
                caveat="new passive/causative for this exact sense must be editorially licensed" if passive else "check verb selectional restrictions"
                return q,license,caveat,"",ingredients
        sem="voice requires a precise patient, transitive verb, and source-licensed voice frame"
    elif domain=="evidentiality":
        claim,alt=scenarios.EVIDENCE[idx]
        basic=parse_simple(claim)
        if basic and variant in (1,2,3,4):
            q,ingredients=qr_sentence(lex,basic["actor"],basic["verb"],basic["patient"])
            if q:
                stem=q[4:-1]
                if variant in (1,2,3):
                    evid={1:"si",2:"hu",3:"ye"}[variant]
                    return "sen "+stem+" "+evid+".","existing source evidential "+evid,"confirm claim and event voice","",ingredients
                if variant==4:
                    return "sen "+stem+" he do mi nu sëmi.","8.1 embedded whether and matrix negation","check predicate selection","",ingredients
        sem="report, inference, or embedded question needs a source-grounded lexicalized proposition"
    elif domain=="time_motion":
        who,past,bare,after,before=scenarios.MOTION[idx]
        # Single-clause temporal assertions can be composed only when the
        # two event clauses have known exact verbal senses.
        sem="two-event temporal clauses require individually licensed predicates, aspect and event ordering"
    elif domain=="quantifier_logic":
        sem="8.1 restricted composition excludes extra temporal adverb scope"
    elif domain=="social_consent":
        sem="explicit permission and refusal require reviewed speaker/addressee and action complement frames"
    elif domain=="embedding_reference":
        sem="relative-clause attachment and complement scope require overt participant tracking"
    elif domain=="counterfactual_modal":
        sem="past counterfactual antecedent and consequent require independently reviewed verb arguments"
    elif domain=="narrative_figures":
        sem="source English metaphor has no established Qaroshi idiom or literal-equivalence evidence"
    elif domain=="technical_precision":
        sem="domain technical source, causal uncertainty, and predicate selection remain individually underdetermined"
    return "","no complete source-licensed composition",sem or "requires manual semantic adjudication","",[]

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    if not (ROOT/"data/stress82/case_adjudications_500.csv").exists():
        build_82()
    lex=Glosses()
    original=rows(ROOT/"data/stress82/case_adjudications_500.csv")
    assert len(original)==500
    cases=[]
    lookup_stats=collections.Counter()
    for c in original:
        candidate,basis,warning,extra,ingredients=draft_for(c,lex)
        words_used=[{"role":a,"english":b,"qr":c3[0],"id":c3[1],"qualification":c3[2]}
                    for a,b,c3 in ingredients if b]
        if candidate:
            status="compositional_editorial_draft_unverified"
            if c["qaroshi_draft"]:status="inherited_8_1_draft_unverified"
        else:status="unresolved_lexical_or_grammar"
        lookup_stats[status]+=1
        cases.append({
            "id":c["id"],"domain":c["domain"],"family":c["family"],
            "feature":c["feature"],"english_target":c["english_target"],
            "qaroshi_draft":candidate,
            "coverage_status":status,
            "editorial_rule_basis":basis,
            "dictionary_lexeme_witness_json":json.dumps(words_used,ensure_ascii=False,separators=(",",":")),
            "specific_blocker_or_warning":warning,
            "independent_reverse_translation":"not performed",
            "speaker_accepted":"not tested",
            "language_inexpressibility_proven":"no",
        })
    csvout(OUT/"translation_proposals_500.csv",cases)

    # Strict headword-and-sense audit for all flagged compounds. The original
    # canonical *whole-word* meaning is normative; an English component
    # semicolon does not license any alternate whole-compound interpretation.
    flagged=rows(ROOT/"data/stress82/compound_review_3108.csv")
    assert len(flagged)==3108
    lexical=[]
    for r in flagged:
        word=lex.by_qr[r["word"]]
        assert word["id"]==r["canonical_id"]
        lexical.append({
            "word":r["word"],"canonical_id":word["id"],
            "normative_whole_word_gloss":word["english"],
            "sense_boundary":r["sense_boundary"] or (
              "Read the whole canonical lexical entry, not unrelated senses of its English component glosses."),
            "has_individual_narrow_sense":("yes" if r["sense_boundary"] else "no"),
            "compound_status":"canonical whole-word meaning retained",
            "spelling_renamed":"no",
            "new_homonymous_sense_added":"no",
            "speaker_lexicalized_use_confirmed":"no",
            "future_interpretation_test":"Test context-inferred meaning independently of the English indexing gloss.",
        })
    csvout(OUT/"compound_sense_standard_3108.csv",lexical)

    # Deliberate valency decisions retain all 25 full reviewed frames.
    # For 375 others, each documented finite pattern is a typed exemplar,
    # not carte blanche to invent object classes or agentive passives.
    source=rows(ROOT/"data/stress82/verb_reviews_375.csv")
    assert len(source)==375
    frames=[]
    for r in source:
        has_object=bool(r["exact_object_lemma"])
        frames.append({
            "lemma":r["lemma"],"dictionary_id":r["dictionary_id"],
            "source_id":r["source_id"],"reference_gloss":r["reference_gloss"],
            "observed_syntax_class":("V1 documented exact patient" if has_object else "finite predicate; object class not established"),
            "subject_class":"referent licensing from documented sentence; not a semantic type inferred from English",
            "object_class":(r["exact_object_lemma"]+" (source instance only)" if has_object else "no general class inferred"),
            "licensed_passive":"no (needs independent editorial review)",
            "licensed_causative":"no (needs independent editorial review)",
            "lexical_role_override":"no",
            "adopted_precision_rule":"Only the cited finite construction; do not infer new voice or arguments",
            "review_completion":"source-level normative restriction recorded",
            "unrestricted_general_frame_completed":"no",
            "speaker_acceptability_measured":"no",
        })
    csvout(OUT/"restricted_valency_standard_375.csv",frames)

    # Scoreable independent comprehension exercises: participants cannot
    # invent data by merely running the generator.
    questions,answer=[]
    for c in cases:
        if not c["qaroshi_draft"]:continue
        idx=len(questions)+1
        # English target is *the editorial proposed answer*, not an
        # independently validated translation.
        distractors=[
            "The assertion is denied, rather than affirmed.",
            "The assertion says nothing about whether anybody was affected.",
        ]
        correct=c["english_target"]
        choices=[correct,*distractors]
        rotation=idx%3
        choices=choices[rotation:]+choices[:rotation]
        qid="B83-%04d"%idx
        questions.append({"id":qid,"qaroshi":c["qaroshi_draft"],
            "A":choices[0],"B":choices[1],"C":choices[2],
            "editorial_source_case":c["id"],
            "test_status":"unadministered, editor-authored meaning recognition item"})
        answer.append({"id":qid,"correct":"ABC"[choices.index(correct)],
            "editorial_english_target":correct,
            "warning":"not validated by blinded human respondents"})
    if questions:
        csvout(OUT/"blind_translation_questions.csv",questions)
        csvout(OUT/"separate_answer_key.csv",answer)

    manifest={
        "edition":"Qaroshi 8.3 candidate: completion-focused editorial evidence",
        "total_challenges":len(cases),
        "translation_status_counts":dict(lookup_stats),
        "all_challenges_human_validated":False,
        "source_limited_verb_cases":len(frames),
        "new_general_verb_frames_licensed":0,
        "canonical_compound_senses_locked":len(lexical),
        "individually_newly_semantically_reviewed_compounds":0,
        "human_comprehension_participants":0,
        "comprehension_instrument_questions":len(questions),
        "frozen_source_files_modified":False,
        "generated_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in sorted(OUT.iterdir()) if p.is_file() and p.name!="manifest.json"}
    }
    jsout(OUT/"manifest.json",manifest)
    return manifest

if __name__=="__main__":
    print(json.dumps(build(),ensure_ascii=False,indent=2))
