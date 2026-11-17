import asyncio, json
from playwright.async_api import async_playwright
U="file:///home/claude/xb/wall/out/index_mock.html"
TX=["2027년엔 먼저 묻고, 함께 노 젓겠습니다","야근보다 칼퇴! 대신 낮에 몰입","우리 팀에게: 올해 진짜 고마웠어요","안전은 타협하지 않기","한 달에 한 번 동료에게 커피 사기","나 자신에게: 조급해하지 말자","불량 제로, 이번엔 진짜로","회의는 짧게, 실행은 빠르게","모르면 모른다고 말하기","2027년엔 꼭 영어 공부","건강검진 미루지 않기","같은 배, 같은 방향으로","후배 이야기 끝까지 듣기","품질은 현장에서 시작된다","주 3회 운동, 계단 이용하기","아이디어는 일단 말해 보기","고객 클레임 0건 도전","메일 대신 먼저 전화 한 통","올해보다 한 뼘 더 성장","가족과 저녁 먹는 날 늘리기","새로운 업무도 겁내지 않기","칭찬은 크게, 피드백은 정확하게"]
NM=["김상신","익명","박안전","이브레이크","최디스크","정패드","한캘리퍼","오반응"]
items=[{"id":f"r{i}","name":NM[i%8],"text":TX[i%len(TX)]} for i in range(60)]
posted=[]
async def h(route,req):
    if req.method=="POST": posted.append(json.loads(req.post_data)); await route.fulfill(status=200,body="ok")
    else: await route.fulfill(status=200,content_type="application/json",headers={"Access-Control-Allow-Origin":"*"},body=json.dumps({"count":len(items),"items":items}))
async def main():
  ok=True
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--allow-file-access-from-files"])
    pg=await b.new_page(viewport={"width":390,"height":844}); await pg.route("https://mock.sheet.test/**",h)
    await pg.goto(U); await pg.fill('#nm','김상신'); await pg.click('#chips button:nth-child(2)'); await pg.type('#tx','같이 노 저어요!'); await pg.wait_for_timeout(500)
    await pg.screenshot(path='m_form.png',full_page=True)
    await pg.fill('#tx','시발 장난'); await pg.click('#send'); bad=await pg.text_content('#msg'); ok&=('다른 표현' in bad) and not posted
    await pg.fill('#tx','우리 팀에게: 같이 노 저어요!'); await pg.click('#send'); await pg.wait_for_selector('#done:not([hidden])')
    await pg.screenshot(path='m_done.png',full_page=True)
    ok&= posted and posted[0]['kind']=='wall' and posted[0]['text']=='우리 팀에게: 같이 노 저어요!'
    print('[작성·전송]', 'OK' if ok else 'FAIL', posted[:1])
    for w,hh in [(1920,1080),(1280,720)]:
      wp=await b.new_page(viewport={"width":w,"height":hh}); await wp.route("https://mock.sheet.test/**",h)
      await wp.goto(U+"#wall"); await wp.wait_for_timeout(4500)
      n=await wp.evaluate("document.querySelectorAll('#field .note').length")
      ov=await wp.evaluate("""(()=>{const r=[...document.querySelectorAll('#field .note')].map(e=>e.getBoundingClientRect());let o=0;for(let i=0;i<r.length;i++)for(let j=i+1;j<r.length;j++){const a=r[i],b=r[j];const x=Math.min(a.right,b.right)-Math.max(a.left,b.left),y=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);if(x>0&&y>0)o+=x*y;}const tot=r.reduce((s,a)=>s+a.width*a.height,0);return Math.round(o/tot*100)})()""")
      await wp.screenshot(path=f'wall_{hh}.png'); print(f'[월 {w}x{hh}] 쪽지 {n}개, 겹침 {ov}%')
      if hh==1080:
        items.append({"id":"new1","name":"김상신","text":"새로 온 다짐: 2027 같이 가요!"}); items.insert(3, None); items.remove(None)
        hidden=items.pop(0)  # 시트에서 숨김 처리 시뮬레이션
        await wp.wait_for_timeout(9500); print(await wp.evaluate('Object.keys(window.__WALL.shown()).join(",")')); has=await wp.evaluate("[!!window.__WALL.shown()['new1'], !!window.__WALL.shown()['r0']]")
        g=has==[True,False]; ok&=g; print('[실시간 추가·숨김 반영]', 'OK' if g else 'FAIL', has); await wp.screenshot(path='wall_new.png')
    await b.close()
  print('ALL PASS' if ok else 'FAIL')
asyncio.run(main())
