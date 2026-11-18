#!/usr/bin/env python3
"""Bounded Qaroshi 9.3 typed-grammar CLI.

Examples:
  python -m tools.grammar93.cli parse 'sen mi mara-m tika-te.'
  python -m tools.grammar93.cli render '{"proposition":{"type":"atom","actor":"mi","verb":"tika","patient":"mara","tense":"te"}}'

This command reports precise structural semantics, not reliable free-form
English translation. It refuses unlicensed noun senses, verbs and passives.
"""
from __future__ import annotations
import argparse
import json
import sys
from dataclasses import asdict
from tools.grammar93.engine import Atom,Link,Sentence,Grammar,GrammarError
from tools.grammar93.source_exemplars import SourceExemplarGrammar


def atom_or_link(obj:dict):
    if not isinstance(obj,dict):
        raise GrammarError("Proposition must be a JSON object")
    tag=obj.get("type")
    if tag=="atom":
        fields={name:value for name,value in obj.items() if name!="type"}
        try:
            return Atom(**fields)
        except TypeError as err:
            raise GrammarError("Malformed atom JSON: "+str(err)) from err
    if tag=="link":
        try:
            first=atom_or_link(obj["first"])
            second=atom_or_link(obj["second"])
            if not isinstance(first,Atom) or not isinstance(second,Atom):
                raise GrammarError("Nested link AST is outside the bounded 9.3 parser")
            return Link(obj["relation"],first,second)
        except (KeyError,TypeError) as err:
            raise GrammarError("Malformed link JSON: "+str(err)) from err
    raise GrammarError("Proposition must have explicit type atom or link")


def from_dict(obj:dict)->Sentence:
    if not isinstance(obj,dict):
        raise GrammarError("Sentence must be JSON object")
    try:
        return Sentence(
            proposition=atom_or_link(obj["proposition"]),
            resonance=obj.get("resonance","sen"),
            mood=obj.get("mood","statement"),
            attribution=obj.get("attribution",""),
            evidential=obj.get("evidential",""))
    except (KeyError,TypeError) as err:
        raise GrammarError("Malformed sentence: "+str(err)) from err


def to_dict(s:Sentence)->dict:
    out=asdict(s)
    p=s.proposition
    out["proposition"]={"type":"atom",**asdict(p)} if isinstance(p,Atom) else {
        "type":"link","relation":p.relation,
        "first":{"type":"atom",**asdict(p.first)},
        "second":{"type":"atom",**asdict(p.second)}}
    return out


def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Parse/render restricted typed Qaroshi 9.3 grammar")
    parser.add_argument("action",choices=("parse","render"))
    parser.add_argument("content",help="Qaroshi sentence (parse) or JSON AST (render)")
    parser.add_argument("--source-exemplars",action="store_true",
        help="Opt in to 97 narrow, source-recorded verb/object pairs; not general reviewed frames")
    args=parser.parse_args(argv)
    g=SourceExemplarGrammar() if args.source_exemplars else Grammar()
    scope=("25 reviewed plus 97 exact 8.7 source pairings; editorial morphology, no human meaning validation"
           if args.source_exemplars else "25-reviewed-frame typed sublanguage, not general translation")
    try:
        if args.action=="parse":
            s=g.parse(args.content)
            result={"accepted":True,"ast":to_dict(s),
                    "structural_semantics":g.semantic_view(s),
                    "scope":scope}
        else:
            s=from_dict(json.loads(args.content))
            result={"accepted":True,"qaroshi":g.render(s),
                    "structural_semantics":g.semantic_view(s),
                    "scope":"25-reviewed-frame typed sublanguage, not general translation"}
    except (GrammarError,ValueError,TypeError) as err:
        print(json.dumps({"accepted":False,"reason":str(err)},ensure_ascii=False))
        return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    sys.exit(main())
