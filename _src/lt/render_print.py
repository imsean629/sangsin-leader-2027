import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg=await b.new_page(viewport={"width":1123,"height":1587})
        await pg.goto("file:///home/claude/xb/lt/out/poster.html"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        await pg.screenshot(path="out/poster.png")
        await pg.pdf(path="out/A3_poster.pdf", width="297mm", height="420mm", print_background=True, scale=297/ (1123*25.4/96))
        pg2=await b.new_page()
        await pg2.goto("file:///home/claude/xb/lt/out/scoring.html"); await pg2.evaluate("document.fonts.ready"); await pg2.wait_for_timeout(500)
        await pg2.pdf(path="out/scoring.pdf", format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
