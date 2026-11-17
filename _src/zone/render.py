import asyncio
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
    for n in ['z1A','z1B','z2A','z2B']:
      pg=await b.new_page(viewport={'width':1123,'height':1587}); await pg.goto(f'file:///home/claude/xb/zone/{n}.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(600)
      await pg.screenshot(path=f'{n}.png'); await pg.pdf(path=f'{n}.pdf', width='297mm', height='420mm', print_background=True, scale=297/(1123*25.4/96))
    await b.close()
asyncio.run(m())
