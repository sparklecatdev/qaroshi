#!/usr/bin/env python3
"""Small canonical lexical suggestion index for ten permission challenges."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/stress83"))
from complete import Glosses
from tools.stress81.scenarios import SOCIAL
lex=Glosses().lex
TERMS={
 "v":"borrow;share;read;change;record;display;enter;publish;use;keep;offer;decline;refuse;revoke;withdraw;leave;ask;consent;permit",
 "n":"host;visitor;bicycle;friend;neighbor;photograph;teacher;student;letter;dancer;partner;choreography;organizer;volunteer;conversation;artist;customer;portrait;medic;patient;room;moderator;member;message;traveler;companion;bed;researcher;participant;audio recording;permission;refusal",
 "adj":"private;spare;silent;audio;medical",
}
for pos,terms in TERMS.items():
    for term in terms.split(";"):
        hits=[x for x in lex if x["pos"]==pos and re.search(r"\b"+re.escape(term)+r"\b",x["english"],flags=re.I)]
        hits.sort(key=lambda x:(x["english"].casefold()!=term, x["english"].casefold().split(";")[0]!=term,len(x["english"]),x["id"]))
        print("SOCLEX",pos,term,json.dumps([{"q":x["qaroshi"],"id":x["id"],"gloss":x["english"]} for x in hits[:5]],ensure_ascii=False))
for i,(actor,other,action) in enumerate(SOCIAL,1):
    print("SOC",i,actor,other,action)
