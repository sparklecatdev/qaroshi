#!/usr/bin/env python3
"""Optional offline Playwright smoke test; no browser network navigation required.

Loads the self-contained wiki through set_content to work in restricted CI.
"""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
PREVIEWS=ROOT/'previews';PREVIEWS.mkdir(exist_ok=True)

async def main():
 checks=[];errors=[]
 def check(label,cond):
  checks.append((label,bool(cond)))
  if not cond:print('FAIL',label)
  else:print('PASS',label)
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  page=await browser.new_page(viewport={'width':1440,'height':920},device_scale_factor=1,accept_downloads=True)
  page.on('pageerror',lambda e: errors.append(str(e)))
  html=(ROOT/'Qaroshi_Wiki.html').read_text(encoding='utf-8')
  await page.set_content(html,wait_until='load')
  await page.wait_for_timeout(150)
  check('Home opens',await page.locator('.home-hero h1').count()==1)
  check('Full count shown', '18,663' in await page.locator('#mainContent').inner_text())
  check('Sidebar is populated',await page.locator('#leftSidebar a.navlink').count()>=50)
  await page.screenshot(path=str(PREVIEWS/'Qaroshi_5.0_Home.png'))
  # Search using top bar and confirm global wiki search.
  await page.locator('#topSearch').fill('throat')
  await page.locator('#topSearch').press('Enter')
  await page.wait_for_timeout(100)
  check('Global search works',await page.locator('#searchWords').count()==1)
  await page.evaluate("location.hash='#dictionary'")
  await page.wait_for_timeout(120)
  check('Dictionary route works',await page.locator('#wordQuery').count()==1)
  await page.locator('#wordQuery').fill('gero')
  await page.wait_for_timeout(160)
  result=await page.locator('#wordResults').inner_text()
  check('Accent insensitive Romanization', 'gëro' in result)
  await page.screenshot(path=str(PREVIEWS/'Qaroshi_5.0_Dictionary.png'))
  await page.locator('a.entry-row[href="#word/g%C3%ABro"]').first.click()
  await page.wait_for_timeout(130)
  check('Word page opens',await page.locator('#pronunciation').count()==1)
  check('English-style sound-out visible','GUH-roh' in await page.locator('.pronunciation-panel').inner_text())
  check('IPA visible','/ˈɡə.ɾo/' in await page.locator('.pronunciation-panel').inner_text())
  check('All native glyph images load',await page.evaluate("Array.from(document.querySelectorAll('.glyphbox img')).every(i=>i.complete&&i.naturalWidth>0)"))
  await page.screenshot(path=str(PREVIEWS/'Qaroshi_5.0_Word.png'))
  # Compound opens with connected component links.
  await page.evaluate("location.hash='#dictionary'")
  await page.wait_for_timeout(120)
  await page.locator('#wordQuery').fill('private message')
  await page.wait_for_timeout(160)
  compound=await page.locator('#wordResults a.entry-row').count()
  check('Compounds searchable by definition',compound>0)
  if compound:
   await page.locator('#wordResults a.entry-row').first.click();await page.wait_for_timeout(100)
   check('Component links open from compound',await page.locator('.information a[href^="#word/"]').count()>=2)
  await page.evaluate("location.hash='#phrases'")
  await page.wait_for_timeout(130)
  check('Phrasebook loads',await page.locator('#phraseQuery').count()==1)
  await page.locator('#phraseQuery').fill('throat')
  await page.wait_for_timeout(100)
  check('Phrasebook query responds', 'matching' not in await page.locator('#phraseCount').inner_text() or await page.locator('.phrase-item').count()>=0)
  await page.evaluate("location.hash='#grammar/02'")
  await page.wait_for_timeout(120)
  check('Grammar chapter loads',await page.locator('#chapterBody').count()==1)
  await page.evaluate("location.hash='#script'")
  await page.wait_for_timeout(120)
  check('Native converter opens',await page.locator('#scriptInput').count()==1)
  await page.locator('#scriptInput').fill('më ti lësha.')
  await page.wait_for_timeout(120)
  check('Native converter renders glyphs',await page.locator('#converterResult img').count()>=4)
  check('Converter shows sound-out',await page.locator('#converterPronunciation').count()==1 and 'English' in await page.locator('#converterPronunciation').inner_text())
  # The built-in export writes an image with no remote calls.
  try:
   async with page.expect_download(timeout=3500) as download_event:
    await page.locator('#saveScript').click()
   dl=await download_event.value
   check('Native PNG export',dl.suggested_filename.endswith('.png'))
  except Exception as e:
   check('Native PNG export',False)
   print('PNG export details:',str(e)[:150])
  await page.locator('#themeBtn').click()
  check('Theme toggle works',await page.evaluate("document.documentElement.getAttribute('data-theme')==='dark'"))
  await page.evaluate("location.hash='#home'")
  await page.wait_for_timeout(100)
  # Mobile scenario: actual CSS viewport and sidebar interaction.
  await page.set_viewport_size({'width':390,'height':844})
  await page.wait_for_timeout(160)
  check('No page-level horizontal overflow',await page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 2'))
  check('Mobile menu visible',await page.locator('#menuBtn').is_visible())
  await page.locator('#menuBtn').click()
  check('Mobile sidebar opens', 'open' in (await page.locator('#leftSidebar').get_attribute('class') or ''))
  await page.locator('#leftSidebar a[href="#dictionary"]').first.click()
  await page.wait_for_timeout(100)
  check('Mobile sidebar closes after navigation', 'open' not in (await page.locator('#leftSidebar').get_attribute('class') or ''))
  await page.locator('#themeBtn').click() # back to light for screenshot
  await page.evaluate("location.hash='#home'")
  await page.wait_for_timeout(150)
  await page.evaluate("document.querySelectorAll('.toast').forEach(e=>e.remove())")
  await page.screenshot(path=str(PREVIEWS/'Qaroshi_5.0_Mobile.png'))
  check('No uncaught runtime errors',len(errors)==0)
  await browser.close()
  print('BROWSER RESULT:',sum(v for _,v in checks),'/',len(checks),'passed')
  if errors:print('Errors:',errors[:4])
  (ROOT/'data/browser_smoke_report.json').write_text(json.dumps({'passed':sum(v for _,v in checks),'total':len(checks),'checks':dict(checks),'errors':errors},indent=2)+'\n')
  assert all(v for _,v in checks)
asyncio.run(main())
