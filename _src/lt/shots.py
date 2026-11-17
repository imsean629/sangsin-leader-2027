import asyncio
from playwright.async_api import async_playwright
URL="file:///home/claude/xb/lt/out/leadership_test.html"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":390,"height":844}, device_scale_factor=1)
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.click('#btn-start'); await pg.fill('#nick','대구의 등대'); await pg.wait_for_timeout(100)
        await pg.screenshot(path="shot_nick.png")
        await pg.click('#btn-nick-go')
        for t in ["N","N","N","R","B","N","R","N"]:
            await pg.click(f'#q-opts .opt[data-type="{t}"]'); await pg.wait_for_timeout(260)
        await pg.wait_for_timeout(900)
        await pg.screenshot(path="shot_result.png", full_page=True)
        await pg.click('#btn-save'); await pg.wait_for_selector('#m-save.on')
        src=await pg.evaluate("document.getElementById('m-img').src")
        await pg.goto(src); await pg.screenshot(path="shot_png.png", full_page=True)
        await b.close()
asyncio.run(main())
