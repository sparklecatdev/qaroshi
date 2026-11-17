#!/usr/bin/env python3
"""Trace exact lexicon index witnesses for original adversarial scenario seeds.

This is a *diagnostic*, not an assertion of grammatical/semantic validity.
"""
import json
import sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/stress81"))
sys.path.insert(0,str(ROOT/"tools/stress83"))
from complete import Glosses, rows, build
import scenarios

def exact(lex,s,pos):
    root,ident,note=lex.choose(s,pos)
    return {"en":s,"qr":root,"id":ident,"kind":note}

def main():
    build()
    lex=Glosses()
    inv={"daily":[],"valency":[],"motion":[],"social":[],"counter":[]}
    for i,(who,past,bare,part,consequence) in enumerate(scenarios.DAILY,1):
        seg=bare.split(" the ",1)
        inv["daily"].append({"i":i,"agent":exact(lex,who.replace("the ",""),"n"),
          "verb":exact(lex,seg[0],"v"),"patient":exact(lex,seg[1] if len(seg)==2 else "","n")})
    for i,(a,o,past,bare,part,tool) in enumerate(scenarios.VALENCY,1):
        inv["valency"].append({"i":i,"agent":exact(lex,a,"n"),"verb":exact(lex,bare,"v"),
                             "patient":exact(lex,o,"n"),"tool":exact(lex,tool.replace("a ",""),"n")})
    for i,(who,past,bare,after,before) in enumerate(scenarios.MOTION,1):
        inv["motion"].append({"i":i,"actor":exact(lex,who.replace("the ",""),"n"),
                           "verb":exact(lex,bare.split(" the ")[0].split(" to ")[0].split(" at ")[0],"v")})
    proposals=rows(ROOT/"data/stress83/translation_proposals_500.csv")
    print("ORIGINAL_8_3_DRAFT_COUNT",sum(bool(r["qaroshi_draft"]) for r in proposals))
    for domain,items in inv.items():
        print(domain.upper(),json.dumps(items,ensure_ascii=False))
    by=Counter((r["domain"],bool(r["qaroshi_draft"])) for r in proposals)
    print("BASELINE_BY_DOMAIN",json.dumps({f"{a}:{b}":n for (a,b),n in by.items()},sort_keys=True))

if __name__=="__main__": main()
