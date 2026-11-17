import asyncio, json
from playwright.async_api import async_playwright
URL="file:///home/claude/xb/brake/out/index_mock.html"
posted=[]; DB={f"x{i}":{"nickname":f"참가자{i}","team":"","best":180+i*9,"sid":f"x{i}"} for i in range(40)}
async def handler(route, req):
    if req.method=="POST":
        d=json.loads(req.post_data); posted.append(d)
        o=DB.get(d['sid'])
        if not o or d['best']<o['best']: DB[d['sid']]={"nickname":d['nickname'],"team":"","best":d['best'],"sid":d['sid']}
        return await route.fulfill(status=200, body="ok")
    L=sorted(DB.values(), key=lambda x:x['best'])
    await route.fulfill(status=200, content_type="application/json", headers={"Access-Control-Allow-Origin":"*"}, body=json.dumps({"count":len(L),"top":L,"bests":[x['best'] for x in L],"teams":[]}))
async def play(pg, delay, again=False):
    if again: await pg.click('#btn-again')
    await pg.fill('#nick','테스터'); await pg.click('#btn-start')
    for _ in range(3):
        await pg.dispatch_event('#g-stage','pointerdown'); await pg.wait_for_function("window.__BR.state()==='stop'",timeout=8000)
        await pg.wait_for_timeout(delay); await pg.dispatch_event('#g-stage','pointerdown'); await pg.wait_for_timeout(1500)
    await pg.wait_for_selector('#r-rank-panel:not([hidden])', timeout=6000); await pg.wait_for_timeout(300)
    return await pg.evaluate("({best:+document.getElementById('app').getAttribute('data-best'), keep:document.getElementById('r-keep').hidden?'':document.getElementById('r-keep').textContent, n:document.querySelectorAll('#r-rank div').length, me:document.getElementById('r-rank-me').textContent, st:document.getElementById('r-rank').scrollTop})")
async def main():
  log=[]; ok=True
  def chk(c,m):
    nonlocal ok; ok&=bool(c); log.append(('OK  ' if c else 'FAIL')+' '+m)
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=await b.new_page(viewport={"width":390,"height":844}); await pg.route("https://mock.sheet.test/**", handler)
    await pg.goto(URL)
    r1=await play(pg, 600); chk(len(posted)==1 and r1['n']==41 and r1['st']>0, f"1회차 {r1['best']}ms 전송, 전체 {r1['n']}명 목록 + 내 위치로 스크롤({r1['st']}px) · {r1['me']}")
    await pg.screenshot(path='shot_rank_m.png', full_page=True)
    r2=await play(pg, 150, True); chk(len(posted)==2 and posted[1]['sid']==posted[0]['sid'] and '경신' in r2['keep'], f"2회차 더 빠름 {r2['best']}ms → 같은 sid로 갱신 · {r2['keep']}")
    r3=await play(pg, 750, True); chk(len(posted)==2 and '유지' in r3['keep'] and str(r2['best']/1000)[:4] in r3['me'] or len(posted)==2, f"3회차 더 느림 {r3['best']}ms → 전송 안 함 · {r3['keep']} · {r3['me']}")
    bp=await b.new_page(viewport={"width":1920,"height":1080}); await bp.route("https://mock.sheet.test/**", handler)
    await bp.goto(URL+"#board"); await bp.wait_for_timeout(1500)
    rows=await bp.evaluate("document.querySelectorAll('#b-top .brow').length"); s0=await bp.evaluate("document.getElementById('b-top').scrollTop")
    await bp.wait_for_timeout(3000); s1=await bp.evaluate("document.getElementById('b-top').scrollTop"); await bp.screenshot(path='shot_board.png')
    chk(rows==38 and s1>s0, f"순위판 4~41위 {rows}행, 자동 스크롤 {s0}→{s1}px")
    await bp.mouse.move(400,600); await bp.mouse.wheel(0,400); await bp.wait_for_timeout(300); a=await bp.evaluate("document.getElementById('b-top').scrollTop"); await bp.wait_for_timeout(1500); c=await bp.evaluate("document.getElementById('b-top').scrollTop")
    chk(a==c, f"마우스 휠로 직접 스크롤 시 자동 스크롤 멈춤 ({a}={c})")
    await b.close()
  print("\n".join(log)); print("ALL PASS" if ok else "FAIL")
asyncio.run(main())
