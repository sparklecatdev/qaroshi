"""Standard 9.3: typed, compositional Qaroshi syntax engine.

This module consumes 25 reviewed V0/V1/V2 valency frames (not a sentence
inventory), validates lexical selectional roles, builds ASTs and parses surface
Qaroshi back into the same AST. The syntax parser has *no original English
challenge strings* and does not import stress81–92 composition templates.

Honest scope: the noun sets are specifically declared test licenses. Passive,
arbitrary relativization, unrestricted noun classes and arbitrary V2 transfer
are NOT automatically licensed by a dictionary word's English gloss.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union

ROOT=Path(__file__).resolve().parents[2]
SPEC=ROOT/"data/standard_9_3/grammar_licenses.json"
FRAMES=ROOT/"data/semantics/valency_frames.json"

class GrammarError(ValueError):
    """Input is not licensed by this finite 9.3 grammatical sublanguage."""

@dataclass(frozen=True)
class Atom:
    actor:str
    verb:str
    patient:str|None=None
    recipient:str|None=None
    goal:str|None=None
    location:str|None=None
    source:str|None=None
    comitative:str|None=None
    tense:str=""
    aspect:str=""
    modal:str=""
    negated:bool=False

@dataclass(frozen=True)
class Link:
    relation:str  # after | before | when | if | counterfactual
    first:Atom
    second:Atom

Proposition=Union[Atom,Link]

@dataclass(frozen=True)
class Sentence:
    proposition:Proposition
    resonance:str="sen"
    mood:str="statement"  # statement | polar
    attribution:str=""    # bare | reported_to_speaker | unknown_whether
    evidential:str=""     # si | hu | ye | empty


class Grammar:
    CASES={"recipient":"tu","patient":"m","goal":"gu","source":"de",
           "location":"lo","comitative":"wa"}
    # Order is conventional; syntactically marked input may be permuted.
    RENDER_ORDER=("recipient","patient","goal","source","location","comitative")
    TEMPO={"after":"ana","before":"ëna","when":"yaro",
           "if":"wë","counterfactual":"wënu"}
    REVERSE_TEMPO={value:key for key,value in TEMPO.items()}

    def __init__(self):
        spec=json.loads(SPEC.read_text(encoding="utf8"))
        curated=json.loads(FRAMES.read_text(encoding="utf8"))
        if len(curated)!=25:
            raise GrammarError("Expected exactly 25 inherited reviewed frames")
        self.spec=spec
        self.lex={x["form"]:x for x in spec["nouns"]}
        self.curated={f["lemma"]:f for f in curated}
        self.license=spec["verb_overrides"]
        if set(self.curated)!=set(self.license) or len(self.lex)!=len(spec["nouns"]):
            raise GrammarError("Lexical inventory/frame mismatch or duplicate noun")
        for verb,rule in self.license.items():
            frame=self.curated[verb]
            if frame["frame"] not in ("V0","V1","V2"):
                raise GrammarError("Unknown canonical frame")
            if "subject" not in rule or "patient" not in rule:
                raise GrammarError("Missing required selectional role classes")
            required_object="object:-m" in frame["required_roles"]
            if frame["frame"]=="V0" and rule["patient"]:
                raise GrammarError("V0 may not accept object")
            if required_object and not rule["patient"]:
                raise GrammarError("Missing required V1/V2 object-license class")
            if frame["frame"]=="V2" and "recipient" not in rule:
                raise GrammarError("V2 cannot omit recipient selection")
        self.resonances=set(spec["allowed_resonances"])

    def noun(self,form:str,role:str,verb:str)->None:
        entry=self.lex.get(form)
        if entry is None:
            raise GrammarError(f"Unlicensed noun head: {form}")
        allowed=self.license[verb].get(role)
        if not allowed:
            raise GrammarError(f"Verb {verb} does not license role {role}")
        if entry["class"] not in allowed:
            raise GrammarError(f"Verb {verb} disallows {role} type {entry['class']}")

    def validate_atom(self,a:Atom)->None:
        if a.verb not in self.license:
            raise GrammarError("Unknown or unreviewed verb/sense")
        frame=self.curated[a.verb]["frame"]
        self.noun(a.actor,"subject",a.verb)
        if "object:-m" in self.curated[a.verb]["required_roles"] and not a.patient:
            raise GrammarError("Missing required patient")
        if frame=="V0" and a.patient:
            raise GrammarError("Intransitive verb given an object")
        if frame=="V2" and not a.recipient:
            raise GrammarError("Missing V2 recipient")
        if a.patient:self.noun(a.patient,"patient",a.verb)
        for role in ("recipient","goal","source","location","comitative"):
            item=getattr(a,role)
            if item:self.noun(item,role,a.verb)
        if a.tense not in self.spec["tense_suffixes"]:
            raise GrammarError("Unknown or stacked tense")
        if a.aspect not in self.spec["aspect_suffixes"]:
            raise GrammarError("Unknown or stacked aspect")
        if a.modal not in self.spec["modal_suffixes"]:
            raise GrammarError("Unknown or stacked modality")
        # A verb frame's English gloss does not allow an arbitrary passive;
        # passives must use separately recorded exact 8.8 licenses.

    def validate(self,s:Sentence)->None:
        if s.resonance not in self.resonances:
            raise GrammarError("Independent sentence lacks known resonance")
        if s.mood not in ("statement","polar"):
            raise GrammarError("Unlicensed mood")
        if s.mood=="polar" and s.resonance!="hë":
            raise GrammarError("9.3 limits polar utterances to documented hë")
        if s.attribution not in ("","reported_to_speaker","unknown_whether"):
            raise GrammarError("Unlicensed embedding")
        if s.evidential not in self.spec["evidentials"]:
            raise GrammarError("Unsupported source status")
        if s.mood=="polar" and s.attribution:
            raise GrammarError("Nested polar attitude plus direct question needs further license")
        if s.attribution and s.evidential:
            raise GrammarError("One source status per embedded assertion")
        if s.mood=="polar" and s.evidential:
            raise GrammarError("Question evidentials outside bounded scope")
        p=s.proposition
        if isinstance(p,Atom):
            self.validate_atom(p)
        elif isinstance(p,Link):
            if p.relation not in self.TEMPO:
                raise GrammarError("Invalid clausal connective")
            self.validate_atom(p.first)
            self.validate_atom(p.second)
            if p.relation=="counterfactual" and p.first.tense!="te":
                raise GrammarError("Past counterfactual requires explicit past antecedent")
        else:
            raise GrammarError("Unknown AST node")

    @staticmethod
    def _finite(a:Atom)->str:
        return a.verb+("".join("-"+v for v in (a.tense,a.aspect,a.modal) if v))

    def atom_text(self,a:Atom)->str:
        self.validate_atom(a)
        result=[a.actor]
        for role in self.RENDER_ORDER:
            form=getattr(a,role)
            if form: result.append(form+"-"+self.CASES[role])
        if a.negated:result.append("nu")
        result.append(self._finite(a))
        return " ".join(result)

    def proposition_text(self,p:Proposition)->str:
        if isinstance(p,Atom):
            return self.atom_text(p)
        if isinstance(p,Link):
            left=self.atom_text(p.first)
            right=self.atom_text(p.second)
            s=self.TEMPO[p.relation]+" "+left+", "+right
            if p.relation=="counterfactual":
                s+=" qinë"
            return s
        raise GrammarError("Not an AST proposition")

    def render(self,s:Sentence)->str:
        self.validate(s)
        body=self.proposition_text(s.proposition)
        if s.attribution=="reported_to_speaker":
            body+=" do yano mi-tu shiri-te"
        elif s.attribution=="unknown_whether":
            body+=" he do mi nu sëmi"
        if s.evidential:
            body+=" "+s.evidential
        if s.mood=="polar":
            return s.resonance+" "+body+" he?"
        return s.resonance+" "+body+"."

    @staticmethod
    def _parse_finite(token:str)->tuple[str,str,str,str]:
        # Exact known-root-first strategy. Strip from the RIGHT by grammar
        # slots, never by "English suffix-looking" substrings.
        pieces=token.split("-")
        if len(pieces)>4 or not pieces or any(not p for p in pieces):
            raise GrammarError("Malformed finite verbal token")
        verb=pieces[0]
        rest=pieces[1:]
        slots=({"te","yu"},{"se","mo","në"},{"ki","ho","du"})
        tense=aspect=modal=""
        index=0
        for pos,allowed in enumerate(slots):
            if index<len(rest) and rest[index] in allowed:
                if pos==0:tense=rest[index]
                if pos==1:aspect=rest[index]
                if pos==2:modal=rest[index]
                index+=1
        if index!=len(rest):
            raise GrammarError("Noncanonical voice/tense/aspect/modal order or repetition")
        return verb,tense,aspect,modal

    def parse_atom(self,text:str)->Atom:
        if not text or "  " in text or "," in text or any(c in text for c in ".?!«»"):
            raise GrammarError("Not a single finite clause")
        tokens=text.split(" ")
        if len(tokens)<2:
            raise GrammarError("No actor/predicate")
        verb,tense,aspect,modal=self._parse_finite(tokens[-1])
        if verb not in self.license:
            raise GrammarError("Verb sense not in reviewed inventory")
        if tokens[0] not in self.lex:
            raise GrammarError("Missing/unknown subject")
        tokens=tokens[:-1]
        actor=tokens.pop(0)
        negated=False
        if tokens and tokens[-1]=="nu":
            tokens.pop()
            negated=True
        elif "nu" in tokens:
            raise GrammarError("Negation must immediately precede predicate")
        roles={}
        bycase={suffix:role for role,suffix in self.CASES.items()}
        for token in tokens:
            if "-" not in token:
                raise GrammarError("Unmarked or extraneous argument")
            stem,sep,case=token.rpartition("-")
            if not sep or not stem or case not in bycase:
                raise GrammarError("Invalid case marker")
            role=bycase[case]
            if role in roles:
                raise GrammarError("Duplicate argument case")
            roles[role]=stem
        a=Atom(actor=actor,verb=verb,tense=tense,aspect=aspect,modal=modal,
               negated=negated,**roles)
        self.validate_atom(a)
        return a

    def parse_proposition(self,text:str)->Proposition:
        head,space,tail=text.partition(" ")
        if head in self.REVERSE_TEMPO:
            if not space or tail.count(", ")!=1:
                raise GrammarError("Clausal link requires two explicit bounded clauses")
            a,b=tail.split(", ",1)
            relation=self.REVERSE_TEMPO[head]
            if relation=="counterfactual":
                if not b.endswith(" qinë"):
                    raise GrammarError("Past unreal consequent requires explicit qinë")
                b=b[:-len(" qinë")]
            p=Link(relation,self.parse_atom(a),self.parse_atom(b))
            if relation=="counterfactual" and p.first.tense!="te":
                raise GrammarError("Past counterfactual antecedent lacks past tense")
            return p
        return self.parse_atom(text)

    def parse(self,text:str)->Sentence:
        if not text or text!=text.strip() or "\n" in text or "  " in text:
            raise GrammarError("Sentence whitespace is noncanonical")
        resonance,sep,body=text.partition(" ")
        if not sep or resonance not in self.resonances:
            raise GrammarError("No required opening resonance")
        question=text.endswith(" he?")
        if question:
            body=body[:-len(" he?")]
        elif text.endswith("."):
            body=body[:-1]
        else:
            raise GrammarError("Must terminate with period or polar he?")
        attribution=""
        evidential=""
        if body.endswith(" do yano mi-tu shiri-te"):
            attribution="reported_to_speaker"
            body=body[:-len(" do yano mi-tu shiri-te")]
        elif body.endswith(" he do mi nu sëmi"):
            attribution="unknown_whether"
            body=body[:-len(" he do mi nu sëmi")]
        else:
            for x in ("si","hu","ye"):
                if body.endswith(" "+x):
                    evidential=x
                    body=body[:-len(x)-1]
                    break
        proposition=self.parse_proposition(body)
        result=Sentence(proposition,resonance,
                        "polar" if question else "statement",attribution,evidential)
        self.validate(result)
        # Enforce a single canonical written surface. This prevents an
        # accidental parse of a partially legitimate but misordered phrase.
        if self.render(result)!=text:
            raise GrammarError("Noncanonical argument sequence or conflicting scope")
        return result

    def semantic_view(self,s:Sentence)->dict:
        """Recover scope commitments, NOT free-form English meaning."""
        self.validate(s)
        p=s.proposition
        atoms=[p] if isinstance(p,Atom) else [p.first,p.second]
        is_question=s.mood=="polar"
        is_report=s.attribution=="reported_to_speaker"
        is_unknown=s.attribution=="unknown_whether"
        counter=isinstance(p,Link) and p.relation=="counterfactual"
        hypothetical=isinstance(p,Link) and p.relation in ("if","counterfactual")
        return {
           "roles":[{"actor":a.actor,"patient":a.patient,"recipient":a.recipient,
                     "goal":a.goal,"source":a.source,"location":a.location,
                     "comitative":a.comitative,"verb":a.verb,
                     "negated":a.negated,"tense":a.tense,"aspect":a.aspect,
                     "modal":a.modal} for a in atoms],
           "relation":p.relation if isinstance(p,Link) else "single",
           "speech_act":"question" if is_question else "report" if is_report
                        else "ignorance_of_whether" if is_unknown else "assertion",
           "matrix_event_asserted":not (is_question or is_report or is_unknown or hypothetical),
           "conditional_antecedent_asserted":False if hypothetical else None,
           "counterfactual":counter,
           "report_source":"indefinite_person" if is_report else None,
           "evidential":s.evidential or None,
           "permissive_is_not_completed_action":any(a.modal=="ho" for a in atoms),
           "obligation_does_not_entail_completion":any(a.modal=="du" for a in atoms),
           "source_boundary":"exact 9.3 lexical license; no independent speaker verification",
        }
