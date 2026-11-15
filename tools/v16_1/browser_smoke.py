#!/usr/bin/env python3
"""Offline desktop/mobile functional checks. Chromium URL navigation is policy-blocked;
load the actual packaged HTML with set_content and a temporary localStorage shim.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'Qaroshi_16_1_Root_Reform_Studio.html').read_text(encoding='utf8')
count=0

def check(x,msg):
 global count
 assert x,msg;count+=1

def run():
 from playwright.sync_api import sync_playwright
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for dims,mobile in [({'width':1365,'height':930},False),({'width':390,'height':844},True)]:
   context=browser.new_context(viewport=dims,accept_downloads=True,is_mobile=mobile,has_touch=mobile)
   page=context.new_page();errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
   page.evaluate('''() => {const local={};Object.defineProperty(window,"localStorage",{configurable:true,value:{getItem:k=>local[k]||null,setItem:(k,v)=>local[k]=v,removeItem:k=>delete local[k]}})}''')
   page.set_content(HTML,wait_until='domcontentloaded',timeout=65000)
   check(page.locator('h1').inner_text()=='Learn roots, not random strings','overview')
   check(page.evaluate('D.lex.length')==30000,'30k lexicon')
   check(page.evaluate('D.audit.length')==16525,'16.5k headword audit')
   check(page.evaluate('D.roots.length')==1200,'1200 ranked roots')
   check(page.evaluate('D.gaps.length')>2500,'gap priorities')
   def nav(name):
    if mobile:page.locator('#hamburger').click()
    page.get_by_role('button',name=name,exact=True).click()
   nav('Headword explorer');page.locator('#search').fill('banuaro')
   check(page.locator('.entry').count()>=1,'headword search')
   page.locator('button[data-action^="view-"]').first.click()
   check('banuqamago' in page.locator('#app').inner_text(),'component preview')
   check('not prove' in page.locator('#app').inner_text().lower(),'disclaimer visible')
   page.locator('#revDecision').select_option('candidate')
   page.locator('#revNote').fill('Needs independent semantic example and consent of language editors')
   page.get_by_role('button',name='Save review locally').click();page.once('dialog',lambda dialog:dialog.accept()) if False else None
   # Alert may be auto-dismissed, depending on Playwright handler.
   check(page.evaluate('Object.keys(memory.decisions).length')==1,'local review saved')
   nav('Transparent alternatives');page.locator('#search').fill('wing joint')
   check(page.locator('.entry').count()>=1,'proposals filter')
   nav('Missing building blocks');page.locator('#search').fill('membrane')
   check(page.locator('.entry').count()>=1,'root gap keyword')
   nav('Root learning path')
   check(page.locator('#studySlider').count()==1,'study controls')
   page.get_by_role('button',name='Reveal meaning').click()
   check(page.locator('button[data-action="learn-study"]').count()==1,'revealed meaning')
   page.get_by_role('button',name='Mark learned').click()
   check(page.evaluate('Object.keys(memory.seen).length')==1,'root learned')
   nav('Grammar builder');check('goro-ki' in page.locator('#app').inner_text(),'ability')
   page.get_by_role('button',name='Permission').click()
   check('goro-ho' in page.locator('#app').inner_text(),'permission')
   nav('Review workspace');check(page.locator('.entry').count()==1,'review queue persisted')
   with page.expect_download() as dl:page.locator('button[data-action="export-data"]').click()
   payload=json.loads(Path(dl.value.path()).read_text(encoding='utf8'))
   check(payload['format']=='Qaroshi16ReviewV1','backup format')
   check(len(payload['decisions'])==1,'backup review')
   page.locator('#theme').click();check('dark' in (page.locator('body').get_attribute('class') or ''),'dark mode')
   nav('Overview')
   check(not errs,'Javascript runtime errors: '+repr(errs))
   page.screenshot(path=str(ROOT/('Qaroshi_16_1_Mobile.png' if mobile else 'Qaroshi_16_1_Desktop.png')),full_page=False)
   context.close()
  browser.close()
 (ROOT/'data/v16_1/browser_results.json').write_text(json.dumps({'checks':count,'errors':0,'desktop_mobile':True,'method':'Playwright chromium page.set_content with temporary localStorage shim, because URL navigation is policy restricted'},indent=2),encoding='utf8')
 print('Passed',count,'desktop/mobile checks')
if __name__=='__main__':run()
