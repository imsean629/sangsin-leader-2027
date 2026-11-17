import asyncio, itertools, json, sys
from playwright.async_api import async_playwright
URL="file:///home/claude/xb/lt/out/leadership_test.html"
async def answer(pg, types, nick="테스트선장"):
    await pg.click('#btn-start'); await pg.fill('#nick', nick); await pg.click('#btn-nick-go')
    for t in types:
        await pg.click(f'#q-opts .opt[data-type="{t}"]'); await pg.wait_for_timeout(260)
async def result(pg):
    return await pg.evaluate("[document.getElementById('app').dataset.result, document.getElementById('app').dataset.rule, document.getElementById('r-name').textContent + '|' + document.getElementById('r-nick').textContent, document.getElementById('r-grow').textContent, !!(document.querySelector('#r-art img') && document.querySelector('#r-art img').naturalWidth>0)]")
async def main():
    ok=True; log=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":390,"height":844})
        await pg.goto(URL)
        D=await pg.evaluate("window.__LT.data")
        Q=D["questions"]
        # 1) 다섯 결과 모두: 가능한 한 그 유형을 고르기
        for k in D["order"]:
            picks=[]
            for q in Q:
                ts=[o["t"] for o in q["options"]]
                picks.append(k if k in ts else ts[0])
            await pg.goto(URL); await answer(pg, picks)
            r=await result(pg)
            exp_name=D["types"][k]["short"]; exp_grow=D["types"][k]["grow"]
            good = r[0]==k and exp_name in r[2] and '테스트선장 님의' in r[2] and r[3]==exp_grow and r[4]
            ok&=good; log.append(f"[결과 {k}] {'OK' if good else 'FAIL'} → {r}")
        # 2) 되돌아가 답 바꾸면 재계산
        await pg.goto(URL)
        picks=["N","N","N","B","B","N","W","N"]
        await answer(pg,picks); r1=await result(pg)
        await pg.click('#btn-back-result')           # Q8
        for _ in range(7): await pg.click('#btn-prev')  # → Q1
        cnt=await pg.evaluate("document.getElementById('q-count').textContent")
        sel=await pg.evaluate("document.querySelector('#q-opts .opt.sel').dataset.type")
        newp=["B","R","S","B","B","R","B","B"]
        for t in newp:
            await pg.click(f'#q-opts .opt[data-type="{t}"]'); await pg.wait_for_timeout(260)
        r2=await result(pg)
        good = r1[0]=="N" and cnt.startswith("1") and sel=="N" and r2[0]=="B"
        ok&=good; log.append(f"[되돌리기] {'OK' if good else 'FAIL'} 처음 {r1[0]} → Q1 복귀 시 이전 선택 {sel} 표시 → 변경 후 {r2[0]}")
        # 3) 동점 규칙 (compute 직접 + 전수)
        comp=lambda a: pg.evaluate("a=>window.__LT.compute(a)", a)
        t1=await comp(["N","R","S","R","S","N","W","R"])   # 동점 N,R,S(2/4) → 8번 R
        t2=await comp(["N","R","S","R","S","N","W","B"])   # 8번 B(동점 아님) → 가장 최근 동점 유형 (7번 W 아님 → 6번 N)
        good = t1["type"]=="R" and t1["rule"]=="q8" and t2["type"] in t2["ties"] and t2["rule"]=="draw"
        ok&=good; log.append(f"[동점] {'OK' if good else 'FAIL'} 8번 우선:{t1['type']}/{t1['rule']} ties={t1['ties']}, 공평 추첨:{t2['type']}/{t2['rule']} ties={t2['ties']}")
        # 4) 전체 응답 조합 전수 → 결과 분포
        combos=list(itertools.product(*[[o["t"] for o in q["options"]] for q in Q]))
        dist=await pg.evaluate("""cs=>{var d={};cs.forEach(c=>{var r=window.__LT.compute(c);d[r.type]=(d[r.type]||0)+1});return d}""", [list(c) for c in combos])
        good=len(dist)==5
        ok&=good; log.append(f"[전수 {len(combos)}가지 응답] 결과 분포 {dist}")
        log.append(f"[노출 횟수] {D['expo']}")
        # 5) 닉네임 필수·카드 이미지 생성·기록 행
        await pg.goto(URL); await pg.click('#btn-start')
        dis=await pg.evaluate("document.getElementById('btn-nick-go').disabled")
        await pg.fill('#nick','   '); dis2=await pg.evaluate("document.getElementById('btn-nick-go').disabled")
        await pg.fill('#nick','등대지기'); dis3=await pg.evaluate("document.getElementById('btn-nick-go').disabled")
        await pg.click('#btn-nick-go')
        for t in ["S","W","S","B","S","S","W","S"]:
            await pg.click(f'#q-opts .opt[data-type="{t}"]'); await pg.wait_for_timeout(260)
        dims=await pg.evaluate("window.__LT.capture().then(p=>new Promise(r=>{var i=new Image();i.onload=()=>r([i.naturalWidth,i.naturalHeight]);i.src=p.url}))")
        row=await pg.evaluate("window.__LT.record()")
        good = dis and dis2 and not dis3 and dims[0]>800 and row['nickname']=='등대지기' and row['result']=='S' and row['q1'] in 'ABC'
        ok&=good; log.append(f"[닉네임·저장] {'OK' if good else 'FAIL'} 빈칸 차단 {dis}/{dis2}, 카드 PNG {dims[0]}x{dims[1]}, 기록 행 {dict((k,row[k]) for k in ['nickname','result','rule','q1','q8','t1'])}")
        await b.close()
    print("\n".join(log)); print("ALL PASS" if ok else "SOME FAILED")
if __name__ == "__main__": asyncio.run(main())

async def crew():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":390,"height":844})
        await pg.goto(URL); await answer(pg, ["N","N","N","R","B","N","R","N"], nick="대구의 등대")
        out=[]
        for x in ["W","B","N"]:
            await pg.click(f'#r-dex .dex-btn[data-type="{x}"]'); await pg.wait_for_selector('#m-crew.on')
            t=await pg.evaluate("document.querySelector('#m-crew-card .pk-name').textContent + ' | ' + document.getElementById('m-crew-note').textContent")
            out.append(t)
            if x=="B": await pg.wait_for_timeout(800); await pg.screenshot(path="shot_crew.png")
            await pg.click('#m-crew-close')
        await pg.click('#r-dex .dex-btn[data-type="S"]'); await pg.click('#m-crew-next')
        nxt=await pg.evaluate("document.querySelector('#m-crew-card .pk-name b').textContent")
        await pg.click('#m-crew-close')
        # 메인 카드 저장이 여전히 내 카드인지
        main=await pg.evaluate("document.querySelector('#pk .pk-name').textContent")
        ids=await pg.evaluate("document.querySelectorAll('#pk').length")
        await b.close()
        ok = "동주공제 크루" in out[0] and "콤보 파트너" in out[1] and "대구의 등대 님의" in out[2] and nxt=="수리장" and "대구의 등대" in main and ids==1
        print("[크루 도감]", "OK" if ok else "FAIL", out, "다음▶:", nxt, "| 저장 카드:", main)
if __name__ == "__main__": asyncio.run(crew())
