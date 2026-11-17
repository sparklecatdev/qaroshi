"""Narrow relative head-gap composition with explicit outer proposition scope.

Every relative frame names exactly the head and the missing argument role.
The embedded 'sha' has no independent resonance; 'do' and 'he do' scope over
the whole relative-headed proposition, not just the closest finite verb.
"""
def compose(frame:dict,variant:int)->str|None:
    proposition=frame["matrix_event"]
    if variant==1:
        return f"sen {proposition}."
    if variant==2:
        return f"sen {proposition} do mi tëmiro-te."
    if variant==3:
        return f"sen {proposition} he do mi nu sëmi."
    if variant==4:
        effect=frame.get("conditional_consequence")
        return f"sen wë {proposition}, {effect}." if effect else None
    if variant==5:
        cause=frame.get("reason")
        return f"sen {proposition} ro {cause}." if cause else None
    raise ValueError("Outside the five source challenge transformations")

def semantics(frame:dict,variant:int)->dict:
    return {
        "head":frame["head"],"head_gap_role":frame["head_gap_role"],
        "embedded_relative_predication":frame["relative_clause"],
        "matrix_event":frame["matrix_event"],
        "truth_of_matrix_event_asserted":variant in (1,5),
        "attitude_subject":"speaker" if variant in (2,3) else None,
        "scope":{1:"matrix-assertion",2:"speaker-thought",3:"negated-knowing-whether",
                 4:"real-conditional-antecedent",5:"causal-assertion"}[variant],
        "conditional_antecedent_asserted":False if variant==4 else None,
        "causal_reason_asserted":True if variant==5 else None,
        "relative_gap_belongs_to_head":True,
        "independent_backtranslation":"not performed"
    }
