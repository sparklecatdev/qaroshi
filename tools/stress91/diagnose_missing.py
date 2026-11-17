#!/usr/bin/env python3
"""Transient editorial diagnostics for precise unsolved challenge language."""
from pathlib import Path
from collections import Counter,defaultdict
import sys, re, json, csv
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/"tools/stress83")]
from tools.stress90.compose import build,rows,OUT
from complete import Glosses
from tools.stress81 import scenarios as sc
build()
missing=[r for r in rows(OUT/"case_evidence_500.csv") if not r["qaroshi_full_candidate"]]
print("REMAINING_COUNTS",json.dumps(dict(sorted(Counter(r["domain"] for r in missing).items()))))
for r in missing:
    print("MISSING",r["id"],r["domain"],r["variant"],r["english"])
print("LEXHEADERS",list(Glosses().lex[0]))
lex=Glosses().lex
for domain,series in [
    ("daily",sc.DAILY),("time_motion",sc.MOTION),("social_consent",sc.SOCIAL),
    ("quantifier_logic",sc.LOGIC),("evidentiality",sc.EVIDENCE),
    ("embedding_reference",sc.EMBED),("counterfactual_modal",sc.COUNTER),
    ("voice_valency",sc.VALENCY),("narrative_figures",sc.NARRATIVE),("technical_precision",sc.TECH)]:
    ids=sorted({int(r["scenario_family"].split("-")[-1]) for r in missing if r["domain"]==domain})
    print("REMAINING_FAMILIES",domain,ids)
