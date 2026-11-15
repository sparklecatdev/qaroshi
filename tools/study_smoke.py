#!/usr/bin/env python3
"""Study library browser QA, including mobile and answer reveal."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parents[1];h=(root/'Qaroshi_Wiki.html').read_text(encoding='utf8');out=root/'previews';out.mkdir(exist_ok=True)
checks=[];errors=[]
def check(name,value):
    checks.append((name,bool(value)));print(('PASS' if value else 'FAIL'),name)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1440,'height':940})
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.set_content(h,wait_until='load');page.wait_for_timeout(200)
    check('Study link in sidebar',page.locator('#leftSidebar a[href="#learn"]').count()>=1)
    page.evaluate('location.hash="#learn"');page.wait_for_timeout(200)
    check('Study route loads',page.locator('.learning-grid').count()>=2)
    check('All 19 guides linked',page.locator('.learning-grid a.learning-card').count()==19)
    check('16-lesson course prominently listed',page.locator('a.learning-card[href="#guide/graded_course"]').count()==1)
    page.screenshot(path=str(out/'Qaroshi_5.1_Learning_Library.png'))
    page.locator('a.learning-card[href="#guide/getting_started"]').click();page.wait_for_timeout(100)
    check('Starter guide page has detailed sections',page.locator('#guideBody h2').count()>=8)
    check('Starter guide uses IPA', '/ˈ' in page.locator('#guideBody').inner_text())
    ans=page.locator('#guideBody details')
    check('Answer is an interactive disclosure',ans.count()>=1)
    if ans.count():
        check('Answers hidden initially',ans.first.get_attribute('open') is None)
        ans.first.locator('summary').click();check('Answers revealed',ans.first.get_attribute('open') is not None)
    page.evaluate('location.hash="#guide/graded_course"');page.wait_for_timeout(170)
    check('All 16 course lessons rendered',page.locator('#guideBody h2').count()==17)
    check('Course has 16 answer disclosures',page.locator('#guideBody details').count()==16)
    page.screenshot(path=str(out/'Qaroshi_5.1_Course.png'))
    page.evaluate('location.hash="#guide/sentence_atlas"');page.wait_for_timeout(150)
    check('Sentence atlas has 21 parses',page.locator('#guideBody h2').count()==22)
    page.evaluate('location.hash="#guide/workbook"');page.wait_for_timeout(150)
    check('Workbook opens and has answer key',page.locator('#guideBody details').count()==1)
    page.evaluate('location.hash="#grammar/06"');page.wait_for_timeout(120)
    check('Grammar links to deep guide',page.locator('.chapter-further a[href="#guide/verb_workshop"]').count()==1)
    check('Original grammar chapter body remains',page.locator('#chapterBody').count()==1)
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate('location.hash="#learn"');page.wait_for_timeout(150)
    check('Learning grid stacks on mobile',page.locator('.learning-grid').first.evaluate('(e)=>getComputedStyle(e).gridTemplateColumns.split(" ").length===1'))
    check('Learning library does not overflow viewport',page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+2'))
    page.screenshot(path=str(out/'Qaroshi_5.1_Learning_Mobile.png'))
    page.evaluate('location.hash="#guide/graded_course"');page.wait_for_timeout(220)
    check('Course mobile remains navigable',page.locator('#guideBody').count()==1)
    check('Course page-level horizontal overflow absent',page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+2'))
    page.screenshot(path=str(out/'Qaroshi_5.1_Course_Mobile.png'))
    check('No uncaught browser errors',not errors)
    browser.close()
results={'passed':sum(v for _,v in checks),'total':len(checks),'checks':dict(checks),'errors':errors}
(root/'data/study_browser_report.json').write_text(json.dumps(results,indent=2),encoding='utf8')
print('STUDY BROWSER RESULTS',results['passed'],'/',results['total']);assert all(v for _,v in checks),[k for k,v in checks if not v]
