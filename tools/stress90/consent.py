"""9.0 scope-typed refusal to infer permission and revocation before an action.

This grammar explicitly distinguishes an actual silent departure from an inference
about permission, and distinguishes past consent, later revocation, and a merely
possible action. It is an editorial proposal and requires independent reading.
"""
from __future__ import annotations

def nonconsent(frame: dict) -> str:
    actor, other, action = frame["actor"], frame["other"], frame["action"]
    # The first sentence asserts the departure. The second specifically
    # denies the actor's acceptance of a conditional *permission* proposition.
    return (f"sen {other} shëlahe dëru-te. "
            f"sen wë {other} shëlahe dëru-te, {actor} {action}-ho do "
            f"{actor} nu shërawë-te.")

def revocation(frame: dict) -> str:
    actor, other, action = frame["actor"],frame["other"],frame["action"]
    # Content identity repeats verbatim in the potential-event boundary.
    # The first clause records the formerly granted, action-specific consent.
    # The second withdraws THAT consent, prior to the action opportunity.
    return (f"sen {actor} {action}-ho do {other} terawo "
            f"{actor}-tu maho-m hëzhohe-te. "
            f"sen ëna {actor} {action}-ki-te, "
            f"{other} dëna maho-m keleyu-te.")

def semantic_record(frame:dict, variant:int) -> dict:
    if variant not in (4,5):raise ValueError("Only consent variants 4 and 5")
    return {
      "actor":frame["actor"],"other":frame["other"],"proposed_action":frame["action"],
      "speech_act":"reject_silent_permission_inference" if variant==4 else "withdraw_action_specific_consent",
      "silent_departure_asserted":variant==4,
      "grant_earlier_asserted":variant==5,
      "withdrawal_asserted":variant==5,
      "opportunity_boundary_not_act_assertion":variant==5,
      "target_action_occurred_asserted":False,
      "permission_granted_by_silence":False,
      "underlying_permission_automatically_retained":False,
      "independent_human_comprehension":"not measured"
    }

def compose(frame:dict,variant:int) -> str:
    if variant==4:return nonconsent(frame)
    if variant==5:return revocation(frame)
    raise ValueError("No other variants licensed here")
