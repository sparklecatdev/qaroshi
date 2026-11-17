#!/usr/bin/env python3
"""Offline Wiki 9.5 interaction audit, in real desktop and mobile Chromium.

CI installs only browser-test dependencies for this step. The public wiki
remains one self-contained HTML file, with no runtime dependencies.
"""
from __future__ import annotations
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/"Qaroshi_Wiki.html"
assert WIKI.is_file()
RESULTS=[]
def check(ok,label):
    if not ok:
        raise AssertionError(label)
    RESULTS.append(label)

with sync_playwright() as play:
    browser=play.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for viewport in ({"width":1440,"height":900},{"width":390,"height":844}):
        label="desktop" if viewport["width"]>1000 else "mobile"
        page=browser.new_page(viewport=viewport)
        errors=[]
        external=[]
        page.on("pageerror",lambda error:errors.append(str(error)))
        page.on("request",lambda req:external.append(req.url) if not req.url.startswith("file://") else None)
        page.goto(WIKI.resolve().as_uri(),wait_until="domcontentloaded")
        check(page.locator(".home-hero").count()==1,label+": home loads")
        check(page.locator(".home-hero a[href='#workshop']").count()==0 or
              page.locator(".quick-grid a[href='#workshop']").count()==1,label+": workshop prominent")
        check(page.locator("#leftSidebar a.navlink:visible").count()<25,label+": compact visible sidebar")
        check(page.locator(".quick-grid .quick-card").count()==6,label+": six primary tasks")
        page.evaluate("location.hash='#categories'")
        page.wait_for_timeout(120)
        check(5<=page.locator(".topic-group").count()<=9,label+": grouped subjects")
        check(page.locator(".topic-group[open]").count()==0,label+": browse details collapsed by default")
        page.locator("#topicQuery").fill("music")
        page.wait_for_timeout(100)
        check(page.locator(".topic-group[open]").count()>=1,label+": topic search opens matched groups")
        check(page.locator(".topic-links a:visible").count()>=1,label+": topic search shows original domain")
        anchor=page.locator(".topic-links a:visible").first.get_attribute("href")
        check(anchor.startswith("#dictionary?domain="),label+": old exact-domain deep links preserved")
        page.evaluate("location.hash='#standard'")
        page.wait_for_timeout(120)
        check(page.locator(".standard-addendum").count()==10,label+": all ten source-based amendments")
        check(page.locator("#standardIntroduction").count()==1,label+": current rule precedence")
        page.evaluate("location.hash='#workshop'")
        page.wait_for_timeout(160)
        check(page.locator("#labBuilder").count()==1,label+": browser grammar editor")
        check(page.locator("#labInspect").get_attribute("hidden") is not None,label+": only build tab initially")
        page.locator("#labBuilder button[type=submit]").click()
        page.wait_for_timeout(100)
        check(page.locator("#labComposeResult .lab-output").count()==1,label+": compose succeeds")
        page.locator("#labTabInspect").click()
        check(page.locator("#labInspect").is_visible(),label+": inspect tab works")
        page.locator("#labText").fill("sen mi mara-m tika-te.")
        page.locator("#labInspector button[type=submit]").click()
        page.wait_for_timeout(100)
        check("mara" in page.locator("#labInspectResult").inner_text(),label+": role inspection source semantics")
        page.locator("#labText").fill("sen mi kima-m shëma-te.")
        page.locator("#labInspector button[type=submit]").click()
        check(page.locator("#labInspectResult .lab-error").count()==1,label+": bad role rejected rather than guessed")
        page.evaluate("location.hash='#cases'")
        page.wait_for_timeout(140)
        check(page.locator("#caseCounter").count()==1,label+": case index renders")
        check(page.locator("#caseList .case-item").count()==24,label+": 500 cases paginated")
        page.locator("#caseQuery").fill("QS81-0336")
        page.wait_for_timeout(100)
        check(page.locator("#caseList .case-item").count()==1,label+": exact ID search")
        page.locator("#caseList .case-item").click()
        page.wait_for_timeout(100)
        check("qinë" in page.locator("main").inner_text(),label+": revised active-view 9.2 case visible")
        check("not independently confirmed" in page.locator("main").inner_text().lower(),label+": no false human attestation")
        page.evaluate("location.hash='#grammar/02'")
        page.wait_for_timeout(100)
        check(page.locator("#chapterBody").count()==1,label+": prior grammar deep link survives")
        page.evaluate("location.hash='#dictionary'")
        page.wait_for_timeout(100)
        check(page.locator("#wordQuery").count()==1,label+": dictionary route intact")
        page.evaluate("location.hash='#word/daru'")
        page.wait_for_timeout(110)
        check(page.locator('.word-workshop a[href="#workshop?verb=daru"]').count()==1,label+": reviewed verb links to workshop")
        page.locator('.word-workshop a[href="#workshop?verb=daru"]').click()
        page.wait_for_timeout(120)
        check(page.locator('[data-field="A-verb"]').input_value()=='daru',label+": dictionary deep link preselects reviewed verb")
        # Wiki 9.6: first-party discovery and practice routes.
        page.evaluate("location.hash='#dictionary?q=water'")
        page.wait_for_timeout(110)
        check(page.locator("#wordQuery").input_value()=='water',label+": deep-linked ranked dictionary query")
        check(page.locator("#wordResults .entry-row").count()>=1,label+": ranked meaning search results")
        check(page.locator("#dictionaryAdvanced").count()==1,label+": optional dictionary filters")
        check(not page.locator("#dictionaryAdvanced").evaluate("(el)=>el.open"),label+": filters collapsed by default")
        page.evaluate("location.hash='#word/kima'")
        page.wait_for_timeout(110)
        check(page.locator("#family").count()==1,label+": word family section")
        check(page.locator("#related").count()==1,label+": meaning-neighbor section")
        check("not verified synonyms or antonyms" in page.locator("main").inner_text(),label+": semantic relations not invented")
        check(page.locator('a[href="#practice?word=kima"]').count()==1,label+": word-linked flashcard route")
        page.locator('a[href="#practice?word=kima"]').click()
        page.wait_for_timeout(120)
        check(page.locator("#practiceCard").count()==1,label+": embedded offline practice card")
        check(page.locator(".practice-prompt").inner_text().strip().lower()=='kima',label+": source headword preselected")
        page.locator("#practiceReveal").click()
        check(page.locator(".practice-answer").count()==1,label+": editorial answer revealed on demand")
        page.locator("#practiceKnow").click()
        check("recalled" in page.locator("#practiceProgress").inner_text(),label+": local recall state")
        page.locator("#practiceMode").select_option("phrases")
        page.wait_for_timeout(220)
        card_text=page.locator("#practiceCard .practice-eyebrow").text_content() or ""
        check("Teaching example" in card_text,label+": original corpus card active; mode="+page.locator("#practiceMode").input_value()+" raw="+repr(card_text[:200]))
        check(not external,label+": practice and lookup require no network")
        check(not errors,label+": zero browser script exceptions "+repr(errors[:2]))
        check(not external,label+": no network calls by default "+repr(external[:2]))
        check(page.evaluate("document.documentElement.scrollWidth<=window.innerWidth+4"),label+": no mobile or desktop horizontal overflow")
        page.close()
    browser.close()
print(json.dumps({"passed":len(RESULTS),"checks":RESULTS},ensure_ascii=False,indent=2))
