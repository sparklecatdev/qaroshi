"""Past counterfactual and ability/permission/obligation barrier contrast grammar.

No actual-world action is inferred from a modal or counterfactual. A generic
change in the barrier condition is not automatically its removal.
"""
def compose(frame:dict,variant:int)->str:
    action=frame["action"];barrier=frame["barrier"];consequent=frame["consequence"]
    if variant==1:
        return f"sen wënu {action}-te, {consequent}-te qinë."
    if variant==2:
        return f"sen {action}-te-ki nao {barrier}."
    if variant==3:
        return f"sen {action}-te-ho uro {barrier}."
    if variant==4:
        return f"sen {action}-te-du dëshu {barrier}."
    if variant==5:
        return f"sen wë {barrier} do shërawewa eri-yu, {action}-yu."
    raise ValueError("Only the five source barrier variants are licensed")

def semantics(frame:dict,variant:int)->dict:
    return {
       "actor":frame["who"],"action":frame["action"],"barrier":frame["barrier"],
       "modality":{1:"past_counterfactual",2:"past_dynamic_ability",3:"past_permission",
                   4:"past_obligation",5:"open_barrier_change_conditional"}[variant],
       "past_counterfactual":variant==1,
       "actual_action_asserted":False,
       "actual_consequent_asserted":False,
       "barrier_asserted_current_world":variant in (2,3,4),
       "barrier_change_asserted_current_world":False,
       "permission_from_ability":False,
       "ability_from_permission":False,
       "action_occurrence_from_obligation":False,
       "generic_barrier_change_not_necessarily_relief":variant==5,
       "human_meaning_verified":False
    }
