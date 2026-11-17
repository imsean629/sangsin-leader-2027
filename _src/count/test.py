import asyncio, json
from playwright.async_api import async_playwright
U="file:///home/claude/xb/count/out/index_mock.html"; DB=[]
async def h(route, req):
    if req.method=="POST": DB.append(json.loads(req.post_data)); return await route.fulfill(status=200, body="ok")
    best={}
    for r in DB:
        if r['nickname'] not in best or r['total_ms']<best[r['nickname']]: best[r['nickname']]=r['total_ms']
    L=sorted([{"nickname":n,"total":t} for n,t in best.items()], key=lambda x:x['total'])
    await route.fulfill(status=200, content_type="application/json", headers={"Access-Control-Allow-Origin":"*"}, body=json.dumps({"count":len(L),"top":L[:10],"list":[x['total'] for x in L]}, ensure_ascii=False))
async def play(pg, waits):
    for w in waits:
        await pg.wait_for_selector('#g-pad.ready', timeout=8000)
        await pg.dispatch_event('#g-pad','pointerdown'); await pg.wait_for_timeout(w); await pg.dispatch_event('#g-pad','pointerdown')
    await pg.wait_for_selector('#s-result.on', timeout=8000)
async def main():
  ok=True; log=[]
  def chk(c,m):
    nonlocal ok; ok&=bool(c); log.append(('OK  ' if c else 'FAIL')+' '+m)
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    ctx=await b.new_context(viewport={"width":390,"height":844}, accept_downloads=True); await ctx.route("https://mock.sheet.test/**", h); pg=await ctx.new_page()
    await pg.goto(U); await pg.screenshot(path='shot_start.png', full_page=True); await pg.fill('#nick','김상신'); await pg.click('#btn-start')
    await pg.wait_for_selector('#g-pad.ready'); await pg.dispatch_event('#g-pad','pointerdown'); await pg.wait_for_timeout(1200); await pg.screenshot(path='shot_run.png')
    await pg.dispatch_event('#g-pad','pointerdown'); await pg.wait_for_timeout(400); await pg.screenshot(path='shot_after.png')
    # 나머지 2라운드
    for w in [9700, 15400]:
        await pg.wait_for_selector('#g-pad.ready', timeout=8000); await pg.dispatch_event('#g-pad','pointerdown'); await pg.wait_for_timeout(w); await pg.dispatch_event('#g-pad','pointerdown')
    await pg.wait_for_selector('#s-result.on', timeout=8000); await pg.wait_for_timeout(3500)
    laps=await pg.evaluate("window.__CT.laps()"); tot=abs(laps[0]-5000)+abs(laps[1]-10000)+abs(laps[2]-15000)
    chk(DB and DB[-1]['total_ms']==tot and DB[-1]['kind']=='count', f"3라운드 측정·전송 {laps} → 오차 {tot/1000:.2f}초 ({DB[-1]['grade'] if DB else ''})")
    rk=await pg.text_content('#c-rank'); chk('1명 중 1위' in rk, f"순위 표시: {rk}")
    await pg.screenshot(path='shot_result.png', full_page=True)
    async with pg.expect_download(timeout=8000) as dl: await pg.click('#btn-save')
    chk((await dl.value).suggested_filename.endswith('.png'), "이미지 저장")
    # 재도전: 더 나쁜 기록 → 최고 기록 유지
    await pg.click('#btn-again'); await play(pg, [3000, 7000, 12000]); await pg.wait_for_timeout(3500)
    rk2=await pg.text_content('#c-rank'); chk('(최고 기록)' in rk2 and '1명 중 1위' in rk2, f"재도전(나쁜 기록) → {rk2}")
    # 두 번 누름 방지
    await pg.click('#btn-again'); await pg.wait_for_selector('#g-pad.ready'); await pg.dispatch_event('#g-pad','pointerdown'); await pg.dispatch_event('#g-pad','pointerdown')
    chk(await pg.evaluate("window.__CT.state()")=='run', "시작 직후 연타는 무시")
    for i,(n,t) in enumerate([("한캘리퍼",420),("오반응",510),("윤제동",880),("강로터",1200),("조패드",1650),("임라이닝",2300),("서드럼",3400),("이브레이크",4100)]): DB.append({"nickname":n,"total_ms":t})
    W=await b.new_page(viewport={"width":1920,"height":1080}); await W.route("https://mock.sheet.test/**", h)
    await W.goto(U+"#board"); await W.wait_for_timeout(1500); await W.screenshot(path='shot_board.png')
    chk(await W.evaluate("document.querySelectorAll('#b-top .brow').length")==7, "순위판 표시")
    await b.close()
  print("\n".join(log)); print("ALL PASS" if ok else "FAIL")
asyncio.run(main())
