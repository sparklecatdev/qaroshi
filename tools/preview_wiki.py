import asyncio
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading
from functools import partial
from playwright.async_api import async_playwright
async def main():
 p=Path(__file__).resolve().parents[1]
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(p)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  page=await browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.set_content((p/'Qaroshi_Wiki.html').read_text(encoding='utf-8'),wait_until='load')
  await page.wait_for_timeout(500)
  print('PAGE TITLE',await page.title());print('URL',page.url)
  print('HEAD', (await page.locator('#mainContent').inner_text())[:600])
  await page.screenshot(path=str(p/'preview_before.png'),full_page=False)
  print('errors',errors)
  await browser.close()
 server.shutdown()
asyncio.run(main())
