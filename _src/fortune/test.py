import asyncio
from playwright.async_api import async_playwright
U="file:///home/claude/xb/fortune/out/index_local.html"
async def main():
  ok=True; log=[]
  def chk(c,m):
    nonlocal ok; ok&=bool(c); log.append(('OK  ' if c else 'FAIL')+' '+m)
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    ctx=await b.new_context(viewport={"width":390,"height":844}, accept_downloads=True); pg=await ctx.new_page()
    await pg.goto(U); await pg.wait_for_timeout(600); await pg.screenshot(path='s0.png')
    await pg.dispatch_event('#cookie','pointerdown'); await pg.wait_for_timeout(250); await pg.screenshot(path='s1.png')
    await pg.dispatch_event('#cookie','pointerdown'); await pg.wait_for_timeout(250); await pg.screenshot(path='s2.png')
    await pg.dispatch_event('#cookie','pointerdown'); await pg.wait_for_timeout(700); await pg.screenshot(path='s3.png')
    await pg.wait_for_selector('#result:not([hidden])'); await pg.wait_for_timeout(900); await pg.screenshot(path='s4.png', full_page=True)
    chk(len((await pg.evaluate("window.__FC.state()"))['got'])==1, "3번 두드리면 쿠키 1개 획득")
    async with pg.expect_download(timeout=8000) as dl: await pg.click('#btn-save')
    chk((await dl.value).suggested_filename.endswith('.png'), "카드 이미지 저장")
    for k in range(2):
      await pg.click('#btn-next'); await pg.wait_for_timeout(500)
      for _ in range(3): await pg.dispatch_event('#cookie','pointerdown'); await pg.wait_for_timeout(200)
      await pg.wait_for_selector('#result:not([hidden])', timeout=5000); await pg.wait_for_timeout(300)
    st=await pg.evaluate("window.__FC.state()"); fs=[g['f'] for g in st['got']]
    chk(len(fs)==3 and len(set(fs))==3, f"3개 모두 서로 다른 운세 {fs}")
    await pg.click('#btn-next'); await pg.wait_for_selector('#all:not([hidden])'); await pg.wait_for_timeout(1500); await pg.screenshot(path='s5.png', full_page=True)
    async with pg.expect_download(timeout=8000) as dl: await pg.click('#btn-save-all')
    chk((await dl.value).suggested_filename=='2027포춘쿠키_3장.png', "3장 모음 이미지 저장")
    await pg.reload(); await pg.wait_for_timeout(800)
    chk(await pg.is_visible('#all') and not await pg.is_visible('#stage'), "다시 접속하면 더 못 깸(모음 화면 고정)")
    await pg.evaluate("window.__FC.tap()"); chk(len((await pg.evaluate("window.__FC.state()"))['got'])==3, "4번째 쿠키 차단")
    await b.close()
  print("\n".join(log)); print("ALL PASS" if ok else "FAIL")
asyncio.run(main())
