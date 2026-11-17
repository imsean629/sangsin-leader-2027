import asyncio
from playwright.async_api import async_playwright
from test_app import URL, answer
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        ctx=await b.new_context(viewport={"width":390,"height":844}, accept_downloads=True)
        pg=await ctx.new_page(); await pg.goto(URL)
        await answer(pg, ["N","W","N","R","B","N","W","N"], nick="바로저장")
        await pg.wait_for_timeout(2500)   # 미리 굽기 완료 대기
        ready=await pg.evaluate("!!document.getElementById('pk')")
        async with pg.expect_download(timeout=5000) as dl:
            await pg.click('#btn-save')
        d=await dl.value; path=await d.path()
        from PIL import Image; im=Image.open(path)
        modal=await pg.evaluate("document.getElementById('m-save').classList.contains('on')")
        toast=await pg.evaluate("document.getElementById('r-saved').textContent")
        # 답 바꾸고 다시 결과 → 새 카드로 저장되는지
        await pg.click('#btn-back-result')
        for _ in range(7): await pg.click('#btn-prev')
        for t in ["B","R","S","B","B","R","B","B"]:
            await pg.click(f'#q-opts .opt[data-type="{t}"]'); await pg.wait_for_timeout(260)
        await pg.wait_for_timeout(2500)
        async with pg.expect_download(timeout=5000) as dl2:
            await pg.click('#btn-save')
        d2=await dl2.value
        print("1차:", d.suggested_filename, im.size, "모달 표시:", modal, "|", toast)
        print("2차:", d2.suggested_filename)
        ok = im.size[0]>900 and not modal and "항해장" in d.suggested_filename and "갑판장" in d2.suggested_filename
        print("[바로 저장]", "OK" if ok else "FAIL")
        await b.close()
asyncio.run(main())
