"""Explicit fictional scope, quotation, interpretation and reading repair.

Novel metaphor meanings are EDITORIAL, not historically traditional. Direct
quoted speech includes its own resonance. Describing a literal reading is not
asserting the literal-world event.
"""
def compose(frame:dict,variant:int)->str|None:
    p=frame["p"];quote=f"toru «sen {p}.»"
    if variant==1:
        return f"sen gëmano {p}."
    if variant==2:
        return f"sen shirimi {quote} shiroli-te."
    if variant==3:
        suggested=frame.get("interpretation")
        return f"sen deshemu-mi {quote} {suggested} do shërawiwo-te." if suggested else None
    if variant==4:
        literal=frame.get("literal")
        return f"sen shënaweho {quote} {literal} do nu shërawëhu-te." if literal else None
    if variant==5:
        return (f"sen pëyeno {quote} gëmodo shëliro-te. "
                f"sen ana pëyeno gëmodo shëliro-te, "
                f"pëyeno zhiqomo-m peziholë-te.")
    raise ValueError("Not an original narrative variant")

def semantics(frame:dict,variant:int)->dict:
    return {
        "quoted_full_sentence":"sen "+frame["p"]+".",
        "quote_present":variant in (2,3,4,5),
        "outer_fictional_scope":variant==1,
        "narrator_is_written_storyteller":variant==2,
        "writer_is_poet":variant==3,
        "interpretation_suggested_not_literal":variant==3,
        "literal_world_entailment_denied":variant==4,
        "reader_initially_treated_as_literal":variant==5,
        "reader_later_corrected_that_reading":variant==5,
        "metaphor_asserted_real_world":False,
        "source_not_a_traditional_idiom_claim":True,
        "human_understanding_measurement":"none"
    }
