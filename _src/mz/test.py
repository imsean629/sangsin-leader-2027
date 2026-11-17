import asyncio
from playwright.async_api import async_playwright
URL="file:///home/claude/xb/mz/out/index.html"
async def run(pg, ncorrect):
    await pg.goto(URL); await pg.fill('#nick','김상신'); await pg.click('#btn-start')
    for i in range(15):
        sel = '#q-opts .opt[data-ok="1"]' if i < ncorrect else '#q-opts .opt[data-ok="0"]'
        await pg.click(sel); await pg.click('#btn-next')
    await pg.wait_for_selector('#s-result.on')
    return await pg.evaluate("[document.getElementById('r-level').textContent, +document.getElementById('app').dataset.score, document.querySelectorAll('#r-notes div').length]")
async def main():
    ok=True; log=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        ctx=await b.new_context(viewport={"width":390,"height":844}, accept_downloads=True); pg=await ctx.new_page()
        exp={0:"삐삐 호출 대기자",2:"삐삐 호출 대기자",3:"싸이월드 도토리 부자",5:"싸이월드 도토리 부자",6:"카톡 이모티콘 장인",9:"알잘딱깔센 통역사",11:"알잘딱깔센 통역사",12:"MZ 명예 원어민",14:"MZ 명예 원어민",15:"영크크 만렙"}
        for n,lv in exp.items():
            r=await run(pg,n); good=r[0]==lv and r[1]==n and r[2]==(15-n if n<15 else 1)
            ok&=good; log.append(f"[{n}개] {'OK' if good else 'FAIL'} → {r[0]}, 오답노트 {r[2]}")
        # 문제 화면 캡처 + 결과 이미지 저장
        await pg.goto(URL); await pg.fill('#nick','김상신'); await pg.click('#btn-start'); await pg.click('#q-opts .opt[data-ok="0"]'); await pg.screenshot(path='shot_q.png')
        for i in range(14):
            await pg.click('#btn-next'); await pg.click('#q-opts .opt[data-ok="1"]' if i%3 else '#q-opts .opt[data-ok="0"]')
        await pg.click('#btn-next'); await pg.wait_for_selector('#s-result.on'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='shot_result.png', full_page=True)
        async with pg.expect_download(timeout=6000) as dl: await pg.click('#btn-save')
        d=await dl.value; from PIL import Image; im=Image.open(await d.path())
        good=im.size[0]>900; ok&=good; log.append(f"[이미지 저장] {'OK' if good else 'FAIL'} {d.suggested_filename} {im.size}")
        # 모든 단어가 정확히 1번씩 출제되는지
        uniq=await pg.evaluate("new Set(window.__MZ.order()).size"); ok&=uniq==15; log.append(f"[출제] 15문항 중복 없음: {uniq==15}")
        await b.close()
    print("\n".join(log)); print("ALL PASS" if ok else "FAIL")
asyncio.run(main())
