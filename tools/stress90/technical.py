"""Compositional epistemic and technical-report scope.

A report of P or a conditional on P is not an assertion of P. A statement
that P does not PROVE Q may presuppose P but does not assert not-Q. These are
new editorial constructions with exact licensed source predicates, not
independently validated usage or universal verb valency licenses.
"""
from __future__ import annotations

def compose(frame:dict,variant:int)->str|None:
    p=frame["p"]
    if variant==1:
        return f"sen {p} do zhikasasho shërawëhu-te."
    if variant==2:
        return f"sen {p} do larëno subali-mi khunikhu-te."
    if variant==3:
        return f"sen {p} do këraro nao {p} do tequyu nu shërawëhe-li-te."
    if variant==4:
        q=frame.get("recommendation")
        return f"sen wë {p}, {q}." if q else None
    if variant==5:
        q=frame.get("unsupported")
        if not q:return None
        return (f"sen {p}. "
                f"sen {p} do ngëshi zhëwëra, {q} do zotenga nu eri.")
    raise ValueError("Only original five technical variants are defined")

def semantics(frame:dict,variant:int)->dict:
    return {
       "technical_proposition":frame["p"],
       "reporting_source":"impersonal_report" if variant==1 else
                           ("second_independent_observer" if variant==2 else None),
       "proposition_asserted_by_main_speaker":variant==5,
       "embedded_p_is_possible_not_asserted":variant==3,
       "lack_of_independent_verification_asserted":variant==3,
       "observational_record_is_not_truth_proof":variant in (1,2),
       "condition_is_hypothetical":variant==4,
       "recommendation_asserted_normatively":variant==4,
       "recommendation_act_occurred":False if variant==4 else None,
       "only_p_as_premise":variant==5,
       "unsupported_q_does_not_follow_from_p":variant==5,
       "unsupported_q_asserted_false":False,
       "source_edition":"9.0 editorial; no independent respondent"
    }
