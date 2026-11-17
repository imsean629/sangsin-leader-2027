import asyncio
from playwright.async_api import async_playwright
URL = "file:///home/claude/xb/brake/out/index.html"
async def tap(pg): await pg.dispatch_event('#g-stage', 'pointerdown')
async def wait_state(pg, s, t=8000):
    await pg.wait_for_function(f"window.__BR.state()==='{s}'", timeout=t)
async def main():
    log=[]; ok=True
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        ctx=await b.new_context(viewport={"width":390,"height":844}, accept_downloads=True)
        pg=await ctx.new_page(); await pg.goto(URL)
        dis=await pg.evaluate("document.getElementById('btn-start').disabled")
        await pg.screenshot(path="shot_start.png")
        await pg.fill('#nick','김상신'); await pg.click('#btn-start')
        # 1) 급발진: 초록불 중 누르기
        await tap(pg); await wait_state(pg,'wait'); await pg.wait_for_timeout(300); await tap(pg)
        foul1=await pg.evaluate("document.getElementById('g-foul').textContent")
        await wait_state(pg,'idle')
        # 2) 예측 출발: 빨간불 직후 50ms 안에 누르기
        await tap(pg); await wait_state(pg,'stop'); await tap(pg)
        foul2=await pg.evaluate("document.getElementById('g-foul').textContent")
        await wait_state(pg,'idle')
        # 3) 정상 3라운드
        for i,delay in enumerate([180, 240, 320]):
            await tap(pg); await wait_state(pg,'stop')
            if i==0: await pg.screenshot(path="shot_stop.png")
            await pg.wait_for_timeout(delay); await tap(pg)
            if i<2: await wait_state(pg,'idle')
        await pg.wait_for_selector('#s-result.on', timeout=5000); await pg.wait_for_timeout(1200)
        laps=await pg.evaluate("window.__BR.laps()"); r=await pg.evaluate("window.__BR.result()")
        nick=await pg.evaluate("document.getElementById('r-nick').textContent"); grade=await pg.evaluate("document.getElementById('r-grade').textContent")
        await pg.screenshot(path="shot_result.png", full_page=True)
        async with pg.expect_download(timeout=6000) as dl: await pg.click('#btn-save')
        d=await dl.value; from PIL import Image; im=Image.open(await d.path())
        good = dis and foul1=="1" and foul2=="2" and len(laps)==3 and all(170<=x<=420 for x in laps) and nick=="김상신" and r["best"]==min(laps) and im.size[0]>900
        ok&=good
        log.append(f"[게임] {'OK' if good else 'FAIL'} 닉네임 없으면 시작 불가:{dis}, 급발진 실격→{foul1}, 예측출발 실격→{foul2}, 기록 {laps}ms, 최고 {r['best']} 평균 {r['avg']} 등급 {grade}, 저장 PNG {im.size} {d.suggested_filename}")
        # 4) 순위판 화면 (시트 미연결 안내)
        await pg.goto(URL+"#board"); await pg.wait_for_timeout(500)
        msg=await pg.evaluate("document.getElementById('b-msg').textContent")
        log.append(f"[순위판] 시트 미연결 안내: {msg}")
        await b.close()
    print("\n".join(log)); print("ALL PASS" if ok else "FAIL")
asyncio.run(main())
