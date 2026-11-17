import asyncio, json
from playwright.async_api import async_playwright
U="file:///home/claude/xb/quiz/out/index_mock.html"; UF="file:///home/claude/xb/quiz/out/index_fast.html"
DB=[]  # 모의 Apps Script
async def h(route, req):
    if req.method=="POST":
        d=json.loads(req.post_data)
        if any(r['nickname']==d['nickname'] and r['sid']!=d['sid'] for r in DB): return await route.fulfill(status=200, body="duplicate")
        for r in DB:
            if r['sid']==d['sid']: r.update(d); break
        else: DB.append(d)
        return await route.fulfill(status=200, body="ok")
    from urllib.parse import urlparse, parse_qs
    p={k:v[0] for k,v in parse_qs(urlparse(req.url).query).items()}
    if 'name' in p: body={"exists": any(r['nickname']==p['name'] for r in DB)}
    elif 'sid' in p: body={"exists": any(r['sid']==p['sid'] for r in DB)}
    else:
        L=sorted(DB, key=lambda r:(-r['score'], r['time_ms'])); body={"count":len(L),"avg":round(sum(r['score'] for r in L)/len(L)) if L else 0,"top":[{"nickname":r['nickname'],"score":r['score'],"time":r['time_ms']} for r in L[:10]],"list":[[r['score'],r['time_ms']] for r in L]}
    await route.fulfill(status=200, content_type="application/json", headers={"Access-Control-Allow-Origin":"*"}, body=json.dumps(body, ensure_ascii=False))

async def play(pg, name, wrong=(), stop_at=None, url=U, skip=()):
    await pg.goto(url); await pg.fill('#nick', name); await pg.click('#btn-start')
    for i in range(25):
        if stop_at is not None and i==stop_at: return
        await pg.wait_for_selector('#s-q.on', timeout=8000)
        await pg.wait_for_function(f"window.__QZ.state().i==={i} && document.querySelectorAll('#q-opts .opt:not([disabled])').length>0", timeout=8000)
        if i in skip:
            await pg.wait_for_function(f"window.__QZ.state().i==={i+1}", timeout=8000); continue
        ans=await pg.evaluate("(()=>{const s=window.__QZ.state();return window.__QZ.qById(s.order[s.i])[5]})()")
        n=await pg.evaluate("document.querySelectorAll('#q-opts .opt').length")
        pick = ans if i not in wrong else (ans+1)%n
        await pg.click(f'#q-opts .opt[data-i="{pick}"]')
    await pg.wait_for_selector('#s-result.on', timeout=8000)

async def main():
    ok=True; log=[]
    def chk(c, m): 
        nonlocal ok; ok &= bool(c); log.append(('OK  ' if c else 'FAIL')+' '+m)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        A=await b.new_context(viewport={"width":390,"height":844}, accept_downloads=True); await A.route("https://mock.sheet.test/**", h); pa=await A.new_page()
        await pa.goto(U); await pa.screenshot(path='shot_start.png', full_page=True)
        # 1) 만점 완주
        await play(pa, '김상신'); await pa.wait_for_timeout(3500)
        st=await pa.evaluate("window.__QZ.state()")
        chk(st['score']==100 and DB and DB[0]['score']==100 and DB[0]['level']=='레드존 마스터', f"만점 완주 → {st['score']}점, 시트 {DB[0]['level'] if DB else '-'}")
        rk=await pa.text_content('#c-rank'); chk('1명 중 1위' in rk, f"순위 표시: {rk}")
        await pa.screenshot(path='shot_result.png', full_page=True)
        async with pa.expect_download(timeout=8000) as dl: await pa.click('#btn-save')
        d=await dl.value; chk(d.suggested_filename.endswith('.png'), f"이미지 저장: {d.suggested_filename}")
        # 2) 새로고침해도 결과 화면(잠금)
        await pa.reload(); await pa.wait_for_selector('#s-result.on', timeout=8000); chk(True, "재접속 시 결과 화면 고정(재참여 불가)")
        # 3) 다른 기기에서 같은 이름 → 차단
        B=await b.new_context(viewport={"width":390,"height":844}); await B.route("https://mock.sheet.test/**", h); pb=await B.new_page()
        await pb.goto(U); await pb.fill('#nick','김상신'); await pb.click('#btn-start'); await pb.wait_for_timeout(800)
        msg=await pb.text_content('#start-msg'); chk('이미 같은 이름' in msg and await pb.is_visible('#s-start'), "다른 기기 같은 이름 차단")
        # 4) 점수 계산(일부 오답) + 중도 이탈
        await play(pb, '박안전', wrong={0,7,18}); st=await pb.evaluate("window.__QZ.state()")
        exp=100-2-4-6; chk(st['score']==exp, f"오답 3개(하·중·상) → {st['score']}점 (기대 {exp})")
        C=await b.new_context(viewport={"width":390,"height":844}); await C.route("https://mock.sheet.test/**", h); pc=await C.new_page()
        await play(pc, '이브레이크', stop_at=5); await pc.reload(); await pc.wait_for_selector('#s-result.on', timeout=8000); await pc.wait_for_timeout(1500)
        r=[x for x in DB if x['nickname']=='이브레이크']; chk(r and r[0]['note']=='중도 이탈' and r[0]['score']==10, f"중도 이탈 → 그때까지 기록 확정 ({r[0]['score'] if r else '-'}점, {r[0]['note'] if r else ''})")
        # 5) 관리자 리셋 → 다시 참여 가능
        DB[:] = [x for x in DB if x['nickname']!='김상신']
        await pa.reload(); await pa.wait_for_timeout(1500)
        chk(await pa.is_visible('#s-start') and await pa.evaluate("localStorage.getItem('sangsin_quiz_2026')===null"), "관리자 리셋 후 같은 기기 재참여 가능")
        # 6) 시간 초과
        D=await b.new_context(viewport={"width":390,"height":844}); await D.route("https://mock.sheet.test/**", h); pd=await D.new_page()
        await play(pd, '최디스크', url=UF, skip={2}); st=await pd.evaluate("window.__QZ.state()"); q2=st['order'][2]
        chk(st['ans'][str(q2)]==-1 and st['score']==98, f"시간 초과 처리 → 해당 문항 오답, {st['score']}점")
        # 화면 캡처: 문제, 순위판
        E=await b.new_context(viewport={"width":390,"height":844}); await E.route("https://mock.sheet.test/**", h); pe=await E.new_page()
        await play(pe, '정패드', stop_at=19); await pe.wait_for_selector('#s-q.on'); await pe.wait_for_timeout(600); await pe.screenshot(path='shot_q.png')
        for i,(n,s_,t) in enumerate([("한캘리퍼",92,210000),("오반응",88,190000),("윤제동",80,230000),("강로터",76,250000),("조패드",70,200000),("임라이닝",64,260000),("서드럼",60,240000)]): DB.append({"nickname":n,"score":s_,"time_ms":t,"sid":f"m{i}"})
        W=await b.new_page(viewport={"width":1920,"height":1080}); await W.route("https://mock.sheet.test/**", h)
        await W.goto(U+"#board"); await W.wait_for_timeout(1500); await W.screenshot(path='shot_board.png')
        rows=await W.evaluate("document.querySelectorAll('#b-top .brow').length"); chk(rows==7, "순위판 표시")
        await b.close()
    print("\n".join(log)); print("ALL PASS" if ok else "FAIL")
asyncio.run(main())
