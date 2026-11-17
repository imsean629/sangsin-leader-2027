import asyncio, json
from playwright.async_api import async_playwright
U="file:///home/claude/xb/ai/out/index_mock.html"; DB=[]; VB=[]
async def h(route, req):
    if req.method=="POST":
        d=json.loads(req.post_data); (VB if d.get('kind')=='aiview' else DB).append(d); return await route.fulfill(status=200, body="ok")
    if 'type=aiview' in req.url:
        out={"count":len(VB)}
        for k in ['role','horizon','outlook','hopes','worries','scope','purpose','first','type','usage']:
            c={}
            for d in VB:
                for x in str(d.get(k,'')).split('|'):
                    if x: c[x]=c.get(x,0)+1
            out[k]=c
        return await route.fulfill(status=200, content_type="application/json", headers={"Access-Control-Allow-Origin":"*"}, body=json.dumps(out, ensure_ascii=False))
    n=len(DB); av=lambda k: round(sum(d[k] for d in DB)/n) if n else 0
    tal=lambda k: {x:sum(1 for d in DB if x in d[k].split('|')) for d in DB for x in d[k].split('|') if x}
    lv={}
    for d in DB: lv[d['level']]=lv.get(d['level'],0)+1
    body={"count":n,"avg":av('score'),"axes":{"freq":av('a_freq'),"range":av('a_range'),"skill":av('a_skill'),"resp":av('a_resp')},"levels":lv,"uses":tal('uses'),"tools":tal('tools')}
    await route.fulfill(status=200, content_type="application/json", headers={"Access-Control-Allow-Origin":"*"}, body=json.dumps(body, ensure_ascii=False))
async def wq(pg, k): await pg.wait_for_function(f"(document.querySelector('.screen.on #q-count, .screen.on #v-count')||{{}}).textContent && document.querySelector('.screen.on #q-count, .screen.on #v-count').textContent.startsWith('{k} /')", timeout=8000)
async def play(pg, picks, uses, tools, view, name=None, comment=''):
    await pg.goto(U)
    if name: await pg.fill('#nick', name)
    await pg.click('#btn-start')
    for i in range(10):
        await wq(pg, i+1)
        if i==2:
            for u in uses: await pg.click(f'#q-opts .opt:nth-child({u+1})')
            await pg.click('#btn-next')
        else: await pg.click(f'#q-opts .opt:nth-child({picks[i]+1})')
    await wq(pg, 11)
    for t in tools: await pg.click(f'#q-opts .opt:nth-child({t+1})')
    await pg.click('#btn-next'); await pg.wait_for_selector('#s-mid.on')
    for j,pk in enumerate(view):  # 직책 + 7문항
        await wq(pg, 12+j)
        if isinstance(pk,list):
            for x in pk: await pg.click(f'#v-opts .opt:nth-child({x+1})')
            await pg.click('#v-next')
        else: await pg.click(f'#v-opts .opt:nth-child({pk+1})')
    await wq(pg, 20)
    if comment: await pg.fill('#v-comment', comment)
    await pg.click('#v-next'); await pg.wait_for_selector('#s-result.on')
V_OPT=lambda role,outlook: [role,2,outlook,[0,1],[1,0],1,1,2]
async def main():
  ok=True; log=[]
  def chk(c,m):
    nonlocal ok; ok&=bool(c); log.append(('OK  ' if c else 'FAIL')+' '+m)
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    ctx=await b.new_context(viewport={"width":390,"height":844}, accept_downloads=True); await ctx.route("https://mock.sheet.test/**", h); pg=await ctx.new_page()
    await pg.goto(U); await pg.screenshot(path='shot_start.png', full_page=True)
    await play(pg, [3]*10, list(range(8)), [0,1], V_OPT(0,4), '김상신', '사람을 키우는 도구로'); r=await pg.evaluate("window.__AI.res()")
    chk(r['score']==100 and r['type']=='자율주행 선구자' and r['verdict']=='유토피아 드리머', f"활용 100 × 매우 기대 → {r['type']} / {r['verdict']}")
    chk(DB[-1]['nickname']=='김상신' and 'type' not in DB[-1] and VB[-1]['type']=='자율주행 선구자' and 'nickname' not in VB[-1] and VB[-1]['role']=='임원' and VB[-1]['comment']=='사람을 키우는 도구로', "1부(이름)·2부(익명, 유형) 분리 전송")
    await pg.wait_for_timeout(3500); await pg.screenshot(path='shot_result.png', full_page=True)
    same=await pg.text_content('#vr-list .vr .same'); chk('%' in same, f"같은 선택 비교: {same}")
    async with pg.expect_download(timeout=8000) as dl: await pg.click('#btn-save')
    fn=(await dl.value).suggested_filename; chk(fn.startswith('AI드라이버카드_자율주행선구자'), f"카드 이미지 저장: {fn}")
    await play(pg, [0]*10, [8], [8], V_OPT(3,0)); r=await pg.evaluate("window.__AI.res()")
    chk(r['score']==0 and r['type']=='신중한 관찰자' and r['verdict']=='디스토피아 경계경보', f"활용 0 × 매우 걱정 → {r['type']} / {r['verdict']}")
    await play(pg, [2,1,0,2,1,2,2,1,2,3], [0,1,2], [0,3], V_OPT(1,2), '박안전'); r=await pg.evaluate("window.__AI.res()")
    chk(r['score']==60 and r['type']=='실용주의 운전자' and r['verdict']=='균형 잡힌 중도', f"활용 60 × 반반 → {r['type']} / {r['verdict']}")
    await play(pg, [3,3,0,3,3,3,3,3,3,3], [0,1,2,3,4], [1], V_OPT(2,1)); r=await pg.evaluate("window.__AI.res()")
    chk(r['type']=='안전벨트 전문가' and r['verdict']=='신중한 현실주의', f"활용 {r['score']} × 걱정 더 → {r['type']} / {r['verdict']}")
    # 2부 첫 문항에서 이전 → 1부 마지막 문항으로
    await pg.goto(U); await pg.click('#btn-start')
    for i in range(10):
        await wq(pg, i+1)
        if i==2: await pg.click('#q-opts .opt:nth-child(1)'); await pg.click('#btn-next')
        else: await pg.click('#q-opts .opt:nth-child(2)')
    await wq(pg, 11); await pg.click('#q-opts .opt:nth-child(1)'); await pg.click('#btn-next'); await wq(pg, 12)
    await pg.click('#v-prev'); await wq(pg, 11); chk(True, "2부 첫 문항에서 이전 → 1부 11번으로 복귀")
    await pg.click('#btn-next'); await wq(pg, 12); chk(True, "다시 다음 → 2부로 바로 이어짐(전환 화면 생략)")
    await pg.screenshot(path='shot_q.png')
    for i in range(6):
        VB.append({"role":"팀장","horizon":"대부분 직무가 다시 짜임","outlook":["반반이다","기대가 더 크다","걱정이 더 크다"][i%3],"hopes":"생산성 향상|반복 업무에서 해방","worries":"정보 유출·보안|일자리 감소","scope":"부서별 시범 적용","purpose":["같은 인원으로 더 큰 성과","사람은 더 가치 있는 일로 이동"][i%2],"first":"직원 교육","type":["실용주의 운전자","가속 페달 개척자","브레이크 담당 실무가"][i%3]})
    W2=await b.new_page(viewport={"width":1920,"height":1080}); await W2.route("https://mock.sheet.test/**", h)
    await W2.goto(U+"#view"); await W2.wait_for_timeout(1800); await W2.screenshot(path='shot_viewboard.png')
    chk('응답' in (await W2.text_content('#vb-msg')) and (await W2.evaluate("document.querySelectorAll('#vb-type .ag-bar').length"))==3, "관점 집계판 + 유형 TOP 3")
    W=await b.new_page(viewport={"width":1920,"height":1080}); await W.route("https://mock.sheet.test/**", h)
    await W.goto(U+"#board"); await W.wait_for_timeout(1800); await W.screenshot(path='shot_board.png')
    chk('응시자' in (await W.text_content('#ag-n')), "활용 지수 집계판")
    await b.close()
  print("\n".join(log)); print("ALL PASS" if ok else "FAIL")
asyncio.run(main())
