#!/usr/bin/env python3
"""Discover source index senses for original stress families. No sense adoption."""
import csv
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/stress83"))
from complete import Glosses

TERMS = {
"actors":"courier|passenger|climber|ambulance|bicycle|pilot|tourist|hiker|train|rescue team|captain|neighbor|scientist|witness|parcel|comet|telescope|dancer|conductor|animal|sensor|student|mechanic|librarian|volunteer|gardener|musician|recipient|person|teacher|moderator",
"event_nouns":"river|bridge|storm|fog|ferry|summit|guide|route|cliff|tide|sun|fire|market|railway|station|platform|streetlight|runway|aircraft|museum|exhibition|rain|camp|alarm|radio|signal|message|meeting|window|room|voice|face|measurement|hypothesis|address|boundary|backup|server|key|register",
"event_verbs":"cross|board|arrive|reach|depart|leave|pass|land|enter|return|stop|approach|inspect|end|clear|check|sound|ring|narrow|appear|begin|grow|set|light|warn|transmit|detect|recognize|repeat|change|cancel|repair|crack|fail|restart|open|be|tell|ask|say|infer|believe|claim|know|witness|report",
"evidence_extra":"record|copy|deliver|write|receive|see|observe|witness|hear|reveal|change their story|disappear|cloud|overnight|recognize|cancel|move|return|different|read|identify|question|true|false|proof|verify|possible",
"adjectives":"broken|failed|open|closed|damaged|strong|clear|heavy|early|late|busy|accurate|missing|available|right|wrong|wet|green|cold",
"case_nouns":"home|field|gate|book|shelter|engine|flight|ticket|wheel|table|document|law|road|test|answer|wound|clock|flame|forest|sky|light|winter|town|memory|silence"
}
lex=Glosses()
print("LEX_HEADERS",list(lex.lex[0]))
for cat,terms in TERMS.items():
    for term in terms.split("|"):
        literal=re.compile(r"\b"+re.escape(term)+r"\b",re.I)
        hits=[r for r in lex.lex if literal.search(r["english"])]
        hits=sorted(hits,key=lambda r:(r.get("type")!="headword",len(r["english"]),r["id"]))
        # Curb noisy matches and avoid false semantic parity.
        picks=[{"id":r["id"],"q":r["qaroshi"],"pos":r["pos"],"en":r["english"][:95]} for r in hits[:4]]
        print("TERM",cat,term,json.dumps(picks,ensure_ascii=False))
