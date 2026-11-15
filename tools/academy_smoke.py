"""Browser smoke run on the self-contained HTML, no server needed."""
from __future__ import annotations
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]

async def main():
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1440,'height':900}, device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda err: errors.append(str(err)))
        html=(ROOT/'Qaroshi_Academy.html').read_text(encoding='utf-8')
        data=json.loads(html.split('<script type="application/json" id="academy-data">')[1].split('</script>')[0])
        phrase_by={row[1]:row[2] for row in data['sentences']}
        await page.set_content(html,wait_until='domcontentloaded')
        tests=0
        async def check(cond,msg):
            nonlocal tests
            assert cond,msg
            tests+=1
        await check('Learn Qaroshi' in await page.locator('h1').first.inner_text(),'home headline')
        await page.screenshot(path=str(ROOT/'previews/academy_desktop.png'),full_page=True)
        await page.locator('.sidebar [data-go="course"]').click()
        await check(await page.locator('[data-lesson]').count()==16,'all lessons present')
        await page.locator('[data-lesson="1"]').click()
        await check(await page.locator('.example-row').count()==10,'ten original examples')
        await check(await page.locator('details.read-more').count()==1,'full teacher key')
        await page.screenshot(path=str(ROOT/'previews/academy_lesson.png'),full_page=True)
        await page.locator('[data-lesson-play="1"]').first.click()
        for i in range(5):
            sent=await page.locator('.question-title').inner_text()
            meaning=phrase_by[sent]
            options=await page.locator('.answer').all_inner_texts()
            await check(meaning in options,f'lesson answer present: {sent}')
            await page.locator('.answer').nth(options.index(meaning)).click()
            await check('Correct!' in await page.locator('.feedback').inner_text(),f'lesson answer correct {i}')
            await page.locator('[data-action="next-question"]').click()
        await check('Lesson marked complete' in await page.locator('main').inner_text(),'lesson completion')
        await check('1/16' in await page.locator('#side-progress').inner_text(),'lesson progress')
        await page.locator('[data-go="practice"]').last.click()
        await check(await page.locator('[data-mode]').count()==8,'8 practice modes')
        await page.screenshot(path=str(ROOT/'previews/academy_practice.png'),full_page=True)
        for mode in ['vocab','reverse','sentence','affix','resonance','glyph','sound','forge']:
            await page.locator(f'[data-mode="{mode}"]').click()
            if mode=='glyph':await check(await page.locator('.native img').count()>0,'native script images')
            if mode=='forge':
                await check(await page.locator('[data-tile]').count()>=4,'word tiles')
                # Toggle every tile and submit the sentence. Even a mistake must provide feedback.
                tiles=await page.locator('[data-tile]').count()
                for i in range(tiles):await page.locator(f'[data-tile="{i}"]').click()
                await page.locator('[data-action="check-forge"]').click()
            else:await page.locator('.answer').first.click()
            await check(await page.locator('.feedback').count()==1,f'{mode} feedback')
            await check(await page.locator('.feedback .reading').count()==1,f'{mode} IPA / sound-out')
            await page.locator('.sidebar [data-go="practice"]').click()
        await page.locator('.sidebar [data-go="dictionary"]').click()
        await page.locator('#word-search').fill('gëro')
        await check(await page.locator('.wordrow').count()>0,'dictionary search')
        await page.locator('.wordrow').filter(has_text='gëro').first.click()
        await check('GUH-roh' in await page.locator('.word-detail').inner_text(),'pronunciation word page')
        await check(await page.locator('.native img').count()>0,'native glyph spelling on word page')
        await page.screenshot(path=str(ROOT/'previews/academy_dictionary.png'),full_page=True)
        await page.locator('.sidebar [data-go="guides"]').click()
        await check(await page.locator('[data-guide]').count()==16,'guide count')
        await page.locator('[data-guide="4"]').click()
        await check(await page.locator('article.markdown').count()==1,'guide article')
        await page.locator('.sidebar [data-go="flight"]').click()
        await page.locator('[data-mode="flight"]').click()
        await check('skyflight route' in (await page.locator('main').inner_text()).lower(),'skyflight started')
        await page.locator('#theme-btn').select_option('dark')
        await check(await page.locator('html').get_attribute('data-theme')=='dark','dark theme')
        await page.screenshot(path=str(ROOT/'previews/academy_skyflight_dark.png'),full_page=True)
        await check(not errors,'no JavaScript errors: '+str(errors))
        m=await browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
        errors2=[];m.on('pageerror',lambda err: errors2.append(str(err)))
        await m.set_content(html,wait_until='domcontentloaded')
        await m.locator('#menu-btn').click()
        await check('menu-open' in (await m.locator('#app').get_attribute('class') or ''),'mobile sidebar open')
        await m.locator('.sidebar [data-go="practice"]').click()
        await check('Practice games' in await m.locator('h1').first.inner_text(),'mobile sidebar navigation')
        await m.wait_for_timeout(350)
        await check('menu-open' not in (await m.locator('#app').get_attribute('class') or ''),'mobile menu closes after navigation')
        await m.screenshot(path=str(ROOT/'previews/academy_mobile.png'),full_page=True)
        await check(not errors2,'no mobile JS errors: '+str(errors2))
        print('PASS',tests,'interactive browser checks')
        await browser.close()

if __name__=='__main__':
    asyncio.run(main())
