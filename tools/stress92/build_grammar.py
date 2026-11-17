#!/usr/bin/env python3
"""Reproducibly consolidate frozen 90-chapter grammar and all later rules.

The 8.0 source and the 8.1–9.1 documents remain untouched. A current
editorial appendix is not external speaker attestation. Use --check in CI.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRONT = ROOT / "docs/standard_9_2/FRONT_MATTER.md"
REGISTRY = ROOT / "data/standard_9_2/amendment_registry.json"
OUTPUT = ROOT / "docs/standard_9_2/grammar.md"
CORE = ROOT / "docs/standard_8/grammar.md"


def render() -> str:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    source = CORE.read_text(encoding="utf-8").rstrip()
    sections = [int(n) for n in re.findall(r"^## ([0-9]+)\.", source, re.M)]
    assert sections == list(range(1, 91)), "Base grammar is not exactly 90 chapters"
    assert len(registry["source_paths"]) == 10
    assert registry["core_normative"] == str(CORE.relative_to(ROOT))
    parts = [FRONT.read_text(encoding="utf-8").rstrip(), "---", source]
    for item in registry["source_paths"]:
        path = ROOT / item["path"]
        assert path.is_file(), item["path"]
        doc = path.read_text(encoding="utf-8").rstrip()
        assert doc.startswith("# "), item["path"]
        parts.extend([
            "---",
            f"## Edition appendix {item['edition']} ({item['kind']})",
            f"Source: [{item['path']}](../../{item['path']}). "
            "Original archived wording is retained; the opening 9.2 conflict "
            "table takes precedence for new editorial writing.",
            doc,
        ])
    result = "\n\n".join(parts) + "\n"
    assert len(result) > 150_000 and "## 90. Genre conventions" in result
    assert result.count("## Edition appendix ") == 10
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(content, encoding="utf-8")
        print(f"Wrote unified 9.2 grammar: {len(content)} characters")
        return
    assert OUTPUT.is_file(), "Run python tools/stress92/build_grammar.py --write"
    actual = OUTPUT.read_text(encoding="utf-8")
    assert actual == content, "9.2 grammar is stale or manually altered; rebuild it"
    print("Unified Standard 9.2 grammar matches all editioned sources")


if __name__ == "__main__":
    main()
