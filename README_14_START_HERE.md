# Qaroshi 14.0: Start here

This release is an editorial-language QA update to Qaroshi 12.0–13.0, with unchanged source dictionary and writing system.

**Fastest path:** open `Qaroshi_14_Semantic_Workbench.html` in a browser. It works without an account or network connection, and you can mark entries for revision and export your private review notes. The app never silently changes canonical dictionary entries.

**For the deeper audit:** read `docs/v14/AUDIT_FINDINGS.md`, followed by `docs/v14/FORMAL_DECISIONS.md`. The full CSV review registers are under `data/v14/`.

**For reproducibility:** run `python -m unittest discover -s tests -q` and `python tools/v14/test_browser.py` after extracting the package. The compiler of the optional glyph font depends on external local font libraries; no font binary is included.

**Caution:** The 103 original translation flags, 1,000 figurative candidates, and 5,000 sense cards remain subject to semantic and cultural review. Structural testing cannot stand in for human linguistic judgement or speaker evidence.
