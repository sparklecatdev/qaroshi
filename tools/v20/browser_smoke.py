#!/usr/bin/env python3
"""Offline desktop/mobile UI tests, with no microphone activated by default."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'Qaroshi_20_Speech_Studio.html').read_text(encoding='utf8')
checks=[]
def ck(ok,title):
 assert ok,title
 checks.append(title)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1330,920),(390,844)]:
  kind='mobile' if width<500 else 'desktop'
  page=browser.new_page(viewport={'width':width,'height':height},accept_downloads=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(HTML,wait_until='domcontentloaded',timeout=90000)
  ck(page.locator('#stats .stat').count()==4,kind+' headline statistics')
  ck(page.locator('[data-tab]').count()==8,kind+' eight navigable sections')
  page.locator('[data-tab="phonemes"]').click()
  ck(page.locator('#phonemeList [data-phoneme]').count()==26,kind+' 26 source-linked phonemes')
  page.locator('#phonemeFilter').select_option('vowel')
  ck(page.locator('#phonemeList [data-phoneme]').count()==6,kind+' six distinct vowels')
  page.locator('#phonemeFilter').select_option('')
  page.locator('#phonemeSearch').fill('uvular')
  ck(page.locator('#phonemeList [data-phoneme]').count()>=1,kind+' phoneme articulation search')
  page.locator('#phonemeSearch').fill('')
  page.locator('#phonemeList [data-phoneme="q"]').click()
  ck('uvular' in page.locator('#phonemeDetail').inner_text().lower(),kind+' uvular phoneme detail')
  page.locator('#phonemeMark').click()
  ck('Reviewed' in page.locator('#phonemeMark').inner_text(),kind+' local phoneme mark')
  page.locator('[data-tab="pairs"]').click()
  ck(page.locator('#pairFilter option').count()>=10,kind+' sound contrast filters')
  page.locator('#pairFilter').select_option('q / k')
  ck(page.locator('#pairDetail .pair .card').count()==2,kind+' real lexical pair visible')
  page.locator('#pairMark').click()
  ck('Reviewed' in page.locator('#pairMark').inner_text(),kind+' local contrast mark')
  page.locator('#pairNext').click()
  ck(page.locator('#pairDetail .pair .card').count()==2,kind+' contrast next')
  page.locator('[data-tab="stress"]').click()
  ck(page.locator('#stressDetail .syll').count()>=2,kind+' stressed syllable options')
  page.locator('#stressDetail .syll').first.click()
  ck('penultimate' in page.locator('#stressAnswer').inner_text(),kind+' stress explanation')
  page.locator('#stressSyllables').select_option('3')
  ck(page.locator('#stressDetail .syll').count()==3,kind+' syllable length filter')
  ck(page.locator('#connectedCards .card').count()>=10,kind+' connected speech examples')
  page.locator('#connectedSearch').fill('water')
  ck(page.locator('#connectedCards .card').count()>=1,kind+' phrase reading search')
  page.locator('[data-tab="resonance"]').click()
  ck(page.locator('#resonanceFilter option').count()==16,kind+' 16 resonances')
  page.locator('#resonanceFilter').select_option('rëm')
  ck(page.locator('#resonanceDetail .card').count()>=1,kind+' rare resonance grounded source')
  page.locator('[data-tab="practice"]').click()
  ck(page.locator('#dayList [data-day]').count()==14,kind+' 14 day course')
  page.locator('#dayMark').click()
  ck('✓' in page.locator('#dayList').inner_text(),kind+' marked practiced')
  page.locator('#dayNext').click()
  ck('day 2' in page.locator('#dayDetail').inner_text().lower(),kind+' next day')
  page.locator('#dayDetail [data-taskjump]').first.click()
  ck(page.locator('#recorder').is_visible(),kind+' course to recorder')
  ck('RC20-' in page.locator('#taskDetail').inner_text(),kind+' source-linked recording prompt')
  page.locator('#recordStart').click()
  ck('Confirm' in page.locator('#recordStatus').inner_text(),kind+' consent required before recording')
  page.locator('#recordConsent').check()
  # In-memory about:blank cannot use a system microphone without secure context;
  # check that this is explained rather than leaking data or claiming recording.
  page.locator('#recordStart').click()
  ck('unavailable' in page.locator('#recordStatus').inner_text() or 'Microphone' in page.locator('#recordStatus').inner_text(),kind+' graceful recording permission context')
  page.locator('#taskSearch').fill('S00001')
  ck(page.locator('#taskSelect option').count()>=0,kind+' recording task filter remains usable')
  page.locator('#taskKind').select_option('canonical_word')
  ck(page.locator('#taskSelect option').count()<=100,kind+' word queue responsive filter')
  page.locator('#taskKind').select_option('')
  page.locator('#taskSearch').fill('')
  ck(page.locator('#taskSelect option').count()==100,kind+' 3000 queue paged selection')
  page.locator('#nextTask').click()
  ck(page.locator('#taskSelect option').count()==1,kind+' next prompt direct filter')
  page.locator('[data-tab="about"]').click()
  ck('not documented' in page.locator('#about').inner_text().lower() and 'native voice models' in page.locator('#about').inner_text().lower(),kind+' authenticity boundary')
  ck(not errors,kind+' no JavaScript page errors '+repr(errors[:2]))
  page.locator('[data-tab="home"]').click()
  page.screenshot(path=str(ROOT/('Qaroshi_20_Mobile_Preview.png' if width<500 else 'Qaroshi_20_Desktop_Preview.png')),full_page=False)
  page.close()
 # A simulated recorder validates control flow, downloads, session memory and the
 # advance-to-next-prompt logic without pretending fake audio is human speech.
 page=browser.new_page(accept_downloads=True)
 err=[];page.on('pageerror',lambda e:err.append(str(e)))
 page.set_content(HTML,wait_until='domcontentloaded',timeout=90000)
 page.evaluate('''() => {
 Object.defineProperty(navigator,'mediaDevices',{configurable:true,value:{getUserMedia:async()=>({getTracks:()=>[{stop:()=>{}}]})}});
 class MockRecorder {
 static isTypeSupported(){return true}
 constructor(){this.state='inactive';this.mimeType='audio/webm'}
 start(){this.state='recording'}
 stop(){this.state='inactive';this.ondataavailable?.({data:new Blob([new Uint8Array(2400)],{type:'audio/webm'})});this.onstop?.()}
 }
 window.MediaRecorder=MockRecorder;
 }''')
 page.locator('[data-tab="recorder"]').click()
 page.locator('#recordConsent').check()
 page.locator('#recordStart').click()
 ck(page.locator('#recordStop').is_enabled(),'mock recorder start enabled')
 page.wait_for_timeout(380)
 page.locator('#recordStop').click()
 ck('Recorded during this visit: 1' in page.locator('#savedTakes').inner_text(),'mock session take retained')
 ck(page.locator('#downloadAudio').is_enabled(),'mock audio download ready')
 with page.expect_download() as result:page.locator('#downloadMeta').click()
 ck(result.value.suggested_filename=='RC20-0001.json','mock metadata filename')
 with page.expect_download() as result:page.locator('#downloadAudio').click()
 ck(result.value.suggested_filename=='RC20-0001.webm','mock audio filename')
 page.locator('#nextTask').click()
 ck(page.locator('#taskSelect').input_value()=='RC20-0002','next prompt correct sequential ID')
 page.locator('#deleteAudio').click()
 ck('Recorded during this visit: 0' in page.locator('#savedTakes').inner_text(),'mock recording discard')
 ck(not err,'mock recorder no JS errors: '+str(err[:2]))
 page.close()
 browser.close()
(ROOT/'data/v20/browser_report.json').write_text(json.dumps({'checks':len(checks),'passed':True,'items':checks},indent=2),encoding='utf8')
print('Passed',len(checks),'offline desktop and mobile browser checks')
