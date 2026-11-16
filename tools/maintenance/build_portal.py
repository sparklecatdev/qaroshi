#!/usr/bin/env python3
"""Build a self-contained, lightweight navigator without modifying canonical data."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT/'data/site_catalog.json'
TEMPLATE = ROOT/'web/portal/portal_template.html'
OUTPUT = ROOT/'explore.html'

def build():
    data = json.loads(CATALOG.read_text(encoding='utf-8'))
    items = data['apps']
    hrefs = [r['href'] for r in items]
    assert len(hrefs) == len(set(hrefs)), 'Duplicate app target'
    assert len({r['id'] for r in items}) == len(items), 'Duplicate app identifier'
    assert data['edition'] == '23'
    template = TEMPLATE.read_text(encoding='utf-8')
    assert template.count('__QAROSHI_SITE_CATALOG__') == 1
    safe = json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    OUTPUT.write_text(template.replace('__QAROSHI_SITE_CATALOG__',safe),encoding='utf-8')
    print(f'Portal created: {OUTPUT.name}, {len(items)} validated navigation targets')
    return OUTPUT
if __name__ == '__main__':build()
