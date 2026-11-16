#!/usr/bin/env python3
"""Exercise the curated web entry point and its links at desktop/mobile widths."""
from __future__ import annotations
import http.server
import json
import socketserver
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/'_site'

from build_pages import stage
stage(SITE)
checks=[]
def require(assertion, name):
    if not assertion:raise AssertionError(name)
    checks.append(name)

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for name,viewport in [('desktop',{'width':1440,'height':920}),('mobile',{'width':390,'height':844})]:
        page=browser.new_page(viewport=viewport)
        errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        page.set_content((SITE/'explore.html').read_text(encoding='utf-8'),wait_until='domcontentloaded')
        require('Qaroshi' in page.title(),name+' portal title')
        require(page.locator('#featured a.app').count()==5,name+' five recommended tools')
        require(page.locator('#archived a.app').count()==5,name+' five archived/reference tools')
        require(not page.locator('#older').evaluate('(node)=>node.open'),name+' older tools collapsed')
        page.locator('#search').fill('pronunciation')
        require(page.locator('#featured a.app').count()==1,name+' pronunciation search')
        require(page.locator('#featured a.app').first.get_attribute('href')=='Qaroshi_20_Speech_Studio.html',name+' relevant result')
        page.locator('#search').fill('')
        page.locator('[data-filter="Learn"]').click()
        require(page.locator('#featured a.app').count()==3,name+' learner filter')
        require(page.locator('[data-filter="Learn"]').get_attribute('aria-pressed')=='true',name+' filter selected state')
        page.locator('[data-filter="All"]').click()
        page.locator('#search').press('Control+k')
        require(page.locator('#search').evaluate('(el)=>document.activeElement===el'),name+' keyboard find')
        page.locator('#search').fill('translation')
        page.locator('#search').press('Escape')
        require(page.locator('#search').input_value()=='',name+' escape clears search')
        page.locator('#theme').click()
        require(page.locator('body').get_attribute('data-theme')=='light',name+' appearance toggle')
        page.locator('#older summary').click()
        require(page.locator('#older').evaluate('(node)=>node.open'),name+' older tool disclosure')
        require(page.locator('#archived a.app').count()==5,name+' archive remains accessible')
        for a in page.locator('a.app').all():
            path=a.get_attribute('href');file=SITE/path
            require(file.is_file() and file.read_bytes()[:150].lower().lstrip().startswith(b'<!doctype html'),name+' working href '+path)
        require(page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+2'),name+' no horizontal overflow')
        require(not errors,name+' no JS exceptions: '+str(errors[:3]))
        page.set_content((SITE/'Qaroshi_21_23_Translation_Immersion_Academy.html').read_text(encoding='utf8'),wait_until='domcontentloaded')
        require('Qaroshi' in page.title(),name+' latest academy is staged')
        page.set_content((SITE/'index.html').read_text(encoding='utf8'),wait_until='domcontentloaded')
        require(page.locator('#wiki-data').count()==1,name+' Wiki index source preserved')
        require(not errors,name+' no page JS exceptions after navigation')
        page.set_content((SITE/'explore.html').read_text(encoding='utf-8'),wait_until='domcontentloaded')
        page.screenshot(path=str(ROOT/f'Qaroshi_Quality_Explore_{name}.png'),full_page=True)
        page.close()
    browser.close()
result={'passed':True,'checks':len(checks),'descriptions':checks,'scope':'Public portal, direct URLs, desktop/mobile links, interactive search and appearance'}
(ROOT/'data/quality_browser_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASSED',len(checks),'browser checks')
