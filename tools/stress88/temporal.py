"""A deliberately restricted two-clause temporal scope recognizer.

Recognizes documented subject-pronoun finite clause patterns and reports
ordering/overlap. Cannot judge unrestricted language or human naturalness.
"""
from __future__ import annotations
import re

VERBS={"goro":"fly","nëru":"rest","shërami":"sleep"}
SUBJECTS={"mi":"speaker","ti":"listener","sa":"third party"}
CONNECTIVES={
    "ana":"matrix_after_subordinate",
    "ëna":"matrix_before_subordinate",
    "yaro":"overlap",
    "torëne":"matrix_holds_until_subordinate_boundary",
}
CLAUSE=re.compile(
    r"^(mi|ti|sa) (nu )?(goro|nëru|shërami)-(te|yu)(?:-(se|mo|në))?$"
)

def parse_clause(text:str)->dict|None:
    x=CLAUSE.fullmatch(text)
    if not x:return None
    subject,negative,verb,tense,aspect=x.groups()
    return {"subject":subject,"verb":verb,"verb_sense":VERBS[verb],
            "past_or_future":"past" if tense=="te" else "future",
            "aspect":aspect or "neutral","negative":bool(negative)}

def analyze(text:str)->dict:
    r={"status":"outside_temporal_88_restricted_checker",
       "speaker_comprehension":"not tested"}
    if not (text.endswith(".") and text.startswith("sen ") and text.count(",")==1):
        return r
    body=text[4:-1]
    head,main=body.split(", ",1) if ", " in body else ("","")
    if " " not in head:return r
    marker,subordinate=head.split(" ",1)
    if marker not in CONNECTIVES:return r
    a=parse_clause(subordinate)
    b=parse_clause(main)
    if a is None or b is None:return r
    if marker=="yaro" and (a["aspect"]!="se" or b["aspect"]!="se"):
        return r
    r.update({"status":"licensed_temporal_88_restricted",
        "connective":marker,"relation":CONNECTIVES[marker],
        "subordinate":a,"matrix":b,
        "subordinate_actually_asserted":False if marker=="torëne" else None,
        "matrix_after_boundary_asserted":False if marker=="torëne" else None,
        "implicature_limit":"A negative until clause does not by itself assert a later positive occurrence."
            if marker=="torëne" else "Temporal order does not establish causation.",
        "semantic_validation":"restricted editorial scope only"})
    return r

if __name__=="__main__":
    import argparse,json
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("sentence")
    args=p.parse_args()
    print(json.dumps(analyze(args.sentence),ensure_ascii=False,indent=2))
