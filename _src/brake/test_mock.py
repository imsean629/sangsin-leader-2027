import asyncio, json
from playwright.async_api import async_playwright
URL="file:///home/claude/xb/brake/out/index_mock.html"
posted=[]
BOARD={"count":12,"top":[{"nickname":"번개손","team":"품질팀","best":187,"sid":"x"},{"nickname":"급정거장인","team":"기획팀","best":205,"sid":"y"}],"bests":[187,205,240,250,260,270,280,290,300,320,350,400],"teams":[{"team":"품질팀","n":4,"avg":231},{"team":"기획팀","n":3,"avg":252}]}
async def handler(route, req):
    if req.method=="POST": posted.append(json.loads(req.post_data)); await route.fulfill(status=200, body="ok")
    else: await route.fulfill(status=200, content_type="application/json", headers={"Access-Control-Allow-Origin":"*"}, body=json.dumps(BOARD))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":390,"height":844}); await pg.route("https://mock.sheet.test/**", handler)
        await pg.goto(URL); await pg.fill('#nick','테스터'); await pg.click('#btn-start')
        for d in [200,220,240]:
            await pg.dispatch_event('#g-stage','pointerdown'); await pg.wait_for_function("window.__BR.state()==='stop'",timeout=8000)
            await pg.wait_for_timeout(d); await pg.dispatch_event('#g-stage','pointerdown'); await pg.wait_for_timeout(1500)
        await pg.wait_for_selector('#r-rank-panel:not([hidden])', timeout=6000)
        me=await pg.evaluate("document.getElementById('r-rank-me').textContent"); n=await pg.evaluate("document.querySelectorAll('#r-rank div').length")
        bp=await b.new_page(viewport={"width":1280,"height":720}); await bp.route("https://mock.sheet.test/**", handler)
        await bp.goto(URL+"#board"); await bp.wait_for_timeout(1200); await bp.screenshot(path="shot_board.png")
        rows=await bp.evaluate("document.querySelectorAll('#b-top .brow').length")
        p0=posted[0]
        ok = p0["kind"]=="brake" and p0["nickname"]=="테스터" and len([p0["r1"],p0["r2"],p0["r3"]])==3 and n==2 and "명" in me and rows==7
        print("[시트 전송·순위]", "OK" if ok else "FAIL", {k:p0[k] for k in ["kind","nickname","best","avg","fouls","grade"]}, "|", me, "| 순위판 행:", rows)
        await b.close()
asyncio.run(main())
