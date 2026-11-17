#!/usr/bin/env python3
"""Restricted semantic scope interpreter for explicitly adopted 8.8 examples.

Do not use this to validate a general Qaroshi sentence. It maps *only exact*
licensed case/role forms onto typed scopes and does not test human naturalness.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def source(name):
    return json.loads((ROOT/"data/standard_8"/name).read_text(encoding="utf8"))

def scope(text):
    from .compose import verb_sentence, valency_sentence
    for record in source("sense_extension_8_8.json"):
        for variant in range(1,5):
            expected=verb_sentence(record["actor"],record["patient"],record["verb"],variant,
                                   patient_surface=record.get("patient_surface"),
                                   theme=record.get("theme"))
            if text!=expected: continue
            return {"status":"licensed_8_8_restricted",
                "family":"daily", "scenario_family":record["family"],
                "sense_id":record["id"],"actor":record["actor"],
                "patient":record["patient"],"theme":record.get("theme"),
                "predicate":record["verb"],"recipient":record["patient"] if record.get("theme") else None,
                "voice":"active",
                "speech_act":"polar_question" if variant==3 else "declarative",
                "event_polarity":"negative" if variant==2 else "positive",
                "embedded_event_asserted":False if variant==4 else None,
                "outer_speech_event_asserted":True if variant==4 else None,
                "reported_by":"yano" if variant==4 else None,
                "reported_to":"mi" if variant==4 else None,
                "event_is_asserted":variant==1,
                "source_role_status":"editioned editorial choice, not human validation"}
    for record in source("valency_overlay_8_8.json"):
        for variant in range(1,6):
            expected=valency_sentence(record,variant)
            if expected is None or text!=expected: continue
            return {"status":"licensed_8_8_restricted",
                "family":"voice_valency","scenario_family":record["family"],
                "sense_id":record["id"],"actor":record["actor"],
                "patient":record["patient"],"instrument":record["tool"] if variant==3 else None,
                "predicate":record["root"],"voice":"passive" if variant in (2,5) else "active",
                "passive_agent_case":"-za" if variant in (2,5) else None,
                "instrument_case":"-shi" if variant==3 else None,
                "speech_act":"polar_question" if variant==5 else "declarative",
                "event_polarity":"negative" if variant==4 else "positive",
                "event_is_asserted":variant in (1,2,3),
                "source_role_status":"editioned editorial choice, not human validation"}
    if text=="sen dëna qaro ngëshi nëna haro.":
        return {"status":"licensed_8_8_restricted",
                "family":"quantifier_logic","scenario_family":1,
                "sense_id":"Q88-0155",
                "focus":{"constituent":"dëna qaro","kind":"exclusive-NP"},
                "time_reference":"nëna (now)","predicate":"haro",
                "speech_act":"declarative","event_is_asserted":True,
                "exclusive_time_focus":False,
                "source_role_status":"editioned editorial choice, not human validation"}
    return {"status":"outside_restricted_8_8_scope","meaning_verified":False}

if __name__=="__main__":
    import argparse
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("sentence")
    args=a.parse_args()
    print(json.dumps(scope(args.sentence),ensure_ascii=False,indent=2))
