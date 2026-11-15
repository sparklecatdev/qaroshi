#!/usr/bin/env python3
"""Browser UI checks using an in-memory HTML document (no network required).

Tests interactive behaviors, but does not claim speaker-level linguistic validation.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'Qaroshi_16_Semantic_Atlas.html').read_text(encoding='utf8')
checks=0

def check(statement,label):
 global checks
 assert statement,label
 checks+=1

def run():
 from playwright.sync_api import sync_playwright
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for size,mobile in [({'width':1380,'height':940},False),({'width':390,'height':820},True)]:
   context=browser.new_context(viewport=size,accept_downloads=True,is_mobile=mobile,has_touch=mobile)
   page=context.new_page();errs=[];page.on('pageerror',lambda err:errs.append(str(err)))
   # about:blank has restricted localStorage in some managed browser policies.
   # A small memory stub permits testing app state transitions without storage privileges.
   page.evaluate('''() => { const mem={};Object.defineProperty(window,"localStorage",{configurable:true,value:{getItem:k=>mem[k]||null,setItem:(k,v)=>{mem[k]=v},removeItem:k=>delete mem[k]}}) }''')
   page.set_content(HTML,wait_until='domcontentloaded',timeout=60000)
   check(page.locator('h1').inner_text()=='Meaning before volume','home heading')
   check(page.evaluate('DATA.lexicon.length')==30000,'30k data in app')
   check(page.evaluate('DATA.senses.length')==5000,'5k sense data in app')
   check(page.evaluate('DATA.idioms.length')==1000,'1k idiom data in app')
   check(page.evaluate('DATA.tasks.length')==240,'240 writing prompts')
   def nav(name):
    if mobile:
     page.locator('#navtoggle').click()
    page.get_by_role('button',name=name,exact=True).click()
   nav('Evidence dictionary')
   page.locator('#wordInput').fill('nashi')
   check(page.locator('.result').count()>0,'dictionary search matches')
   check(page.locator('.result .word').first.inner_text()=='nashi','exact headword ranks first')
   page.locator('button[data-word]').first.click()
   check(page.locator('details[open]').count()==1,'word evidence details expand')
   nav('Root Explorer & word builder')
   check(page.locator('#rootBreak').count()==1,'root breakdown input')
   check('bikhimi' in page.locator('#rootBreakResult').inner_text(),'compound head explained')
   check(page.locator('#rootsList .result').count()>0,'ranked root learning ladder')
   page.locator('#rootBreak').fill('goro-te')
   check('past tense' in page.locator('#rootBreakResult').inner_text(),'grammatical suffix explanation')
   page.locator('#rootsSearch').fill('assessment')
   check(page.locator('#rootsList .result').count()>0,'root search finds compound roots')
   nav('Meaning profiles')
   check(page.locator('.result').count()==118,'118 curated/profile cards')
   page.locator('#profileInput').fill('walking')
   check(page.locator('.result').count()>0,'profile search')
   nav('Semantic domains')
   check(page.locator('.barrow').count()>0,'domain coverage bars')
   nav('Gloss comparisons')
   check(page.locator('.result').count()==26,'gloss comparison groups')
   nav('40 literary metaphors')
   check(page.locator('.result').count()==40,'figurative cards')
   nav('5,000 sense cards')
   check(page.locator('.result').count()==40,'paginated sense list')
   page.locator('#sensePriority').select_option('P1')
   check('P1' in page.locator('.result').first.inner_text(),'priority filter')
   page.locator('textarea.reviewNotes').first.fill('Editorial review evidence placeholder')
   page.locator('textarea.reviewNotes').first.blur()
   check(page.evaluate('Object.keys(s.reviews).length')==1,'review note stored in app state')
   nav('1,000 idiom proposals')
   check(page.locator('.result').count()==40,'paginated idioms list')
   check('Exact occurrence in drafted corpus: 0' in page.locator('.result').first.inner_text(),'idiom evidence warning')
   nav('Translation variations')
   check(page.locator('.result').count()==50,'translation variation explorer')
   nav('240 writing assignments')
   check(page.locator('.result').count()==60,'domain writing brief listing')
   nav('Meaning contrasts')
   check(page.locator('button.quizans').count()==2,'two contrasting choices')
   page.locator('button.quizans').first.click()
   check(page.locator('.answer').count()==1,'answer reveals explanation')
   page.locator('[data-action="nextQuiz"]').click()
   check(page.locator('.answer').count()==0,'next question resets answer')
   nav('Decisions & backup')
   check(page.locator('#importFile').count()==1,'review import')
   with page.expect_download() as dl:
    page.locator('[data-action="export"]').click()
   obj=json.loads(dl.value.path().read_text(encoding='utf8'))
   check(obj['format']=='QaroshiSemanticAtlas16','review export valid JSON')
   check(len(obj['reviews'])>=1,'export includes local review')
   page.locator('#theme').click()
   check('dark' in page.locator('body').get_attribute('class'),'theme toggle')
   if mobile:
    check(page.locator('#navtoggle').is_visible(),'mobile nav toggle')
   check(not errs, 'no browser JavaScript errors: '+repr(errs))
   if mobile:
    page.locator('#navtoggle').click()
    page.get_by_role('button',name='Overview',exact=True).click()
    page.screenshot(path=str(ROOT/'Qaroshi_16_Mobile_Preview.png'),full_page=False)
   else:
    page.get_by_role('button',name='Overview',exact=True).click()
    page.screenshot(path=str(ROOT/'Qaroshi_16_Desktop_Preview.png'),full_page=False)
   context.close()
  browser.close()
 print('Passed',checks,'desktop/mobile interaction assertions')
 (ROOT/'data/v16/browser_report.json').write_text(json.dumps({'checks_passed':checks,'desktop_mobile':True,'managed_browser_mode':'set_content about:blank with localStorage memory shim','page_errors':0},indent=2),encoding='utf8')
if __name__=='__main__':run()
