#!/usr/bin/env python3
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'Qaroshi_16_2_Root_Standardization_Studio.html').read_text(encoding='utf8')
report=[]
def check(x,msg):
 if not x:raise AssertionError(msg)
 report.append(msg)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu'])
 for viewport in ({'width':1400,'height':900},{'width':390,'height':844}):
  page=browser.new_page(viewport=viewport)
  errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  # In-memory HTML avoids the managed browser's file URL-navigation restriction.
  page.set_content(HTML,wait_until='domcontentloaded',timeout=90000)
  mode='mobile' if viewport['width']<600 else 'desktop'
  check(page.locator('#stats .stat').count()==4,mode+' overview metrics')
  check(page.locator('text=More meaning.').count()>=1,mode+' hero')
  page.locator('[data-nav="review"]').click()
  check(page.locator('#reviewCards .item').count()==30,mode+' review paging')
  page.locator('#reviewFilter').select_option('manual_reject')
  check(page.locator('#reviewCards .item').count()==12,mode+' explicit semantic rejections')
  page.locator('#reviewSearch').fill('water meter')
  check(page.locator('#reviewCards .item').count()>=1,mode+' false-friend search')
  page.locator('#reviewSearch').fill('')
  page.locator('#reviewFilter').select_option('manual_trial')
  check(page.locator('#reviewCards .item').count()==30,mode+' curated trial list')
  page.locator('#reviewCards select').first.select_option('test in context')
  check(page.locator('#reviewCards select').first.input_value()=='test in context',mode+' local decision binding')
  page.locator('#moreReview').click()
  check(page.locator('#reviewCards .item').count()==44,mode+' expandable results')
  page.locator('[data-nav="roots"]').click()
  check(page.locator('#rootCards .root').count()==8,mode+' eight root dossiers')
  check(page.locator('#reuseCards .root').count()==8,mode+' reuse-before-coinage')
  check(page.locator('#derivativeCards .item').count()==26,mode+' narrow experimental derivatives')
  page.locator('[data-nav="learn"]').click()
  check(page.locator('#lessonRows .lesson').count()==16,mode+' grammar contrasts')
  page.locator('[data-nav="dictionary"]').click()
  page.locator('#dictionarySearch').fill('banu')
  check(page.locator('#dictionaryCards .item').count()>=1,mode+' canonical dictionary search')
  page.locator('#dictionarySearch').fill('kima')
  check(page.locator('#dictionaryCards .item').count()>=1,mode+' bilingual root search')
  page.locator('[data-nav="method"]').click()
  check(page.locator('#method').is_visible(),mode+' explicit limitations')
  check(not errs,mode+' no JavaScript errors '+str(errs[:3]))
  page.locator('[data-nav="overview"]').click()
  check(page.locator('#overview').is_visible(),mode+' overview return navigation')
  if mode=='desktop':page.screenshot(path=str(ROOT/'Qaroshi_16_2_Desktop_Preview.png'),full_page=True)
  else:page.screenshot(path=str(ROOT/'Qaroshi_16_2_Mobile_Preview.png'),full_page=True)
  page.close()
 browser.close()
(ROOT/'data/v16_2/browser_results.json').write_text(json.dumps({'checks':len(report),'passed':True,'items':report},indent=2),encoding='utf8')
print('PASSED',len(report),'browser checks')
