import segno, io, base64, html
B="https://imsean629.github.io/sangsin-leader-2027/"
F="file:///home/claude/xb/fonts/node_modules/@fontsource/"
FONTS="".join(f'<link rel="stylesheet" href="{F}{x}.css">' for x in ["noto-sans-kr/400","noto-sans-kr/500","noto-sans-kr/700","noto-sans-kr/900","jetbrains-mono/700","jua/400"])
LOGO="file:///home/claude/xb/assets/logo_en.png"; LOGOW="file:///home/claude/xb/assets/logo_en_white.png"
def qr(url, dark="#0B1B36"):
    b=io.BytesIO(); segno.make(url, error='q').save(b, kind='png', scale=12, border=2, dark=dark, light='#FFFFFF'); return "data:image/png;base64,"+base64.b64encode(b.getvalue()).decode()
SHEETS={
 "1":dict(kick="FULL THROTTLE", title="기록에 도전하세요", sub="내 기록이 행사장 대형 화면에 실시간으로 올라갑니다", acc="#E60013", acc2="#FF5A66", note="랭킹 화면은 행사장 스크린에서 확인하세요",
  items=[("🛑","브레이크 반응속도 챌린지","빨간불이 켜지는 순간 브레이크!<br>0.001초까지 겨루는 반응속도","랭킹","30초",B+"brake/"),
         ("🏁","2026 상식 레이스","시사와 상식 25문항.<br>1인 1회, 단 한 번의 기회","랭킹","5분",B+"quiz/"),
         ("🤫","속마음 타이머","5·10·15초를 속으로 세어 딱 멈추기.<br>누구의 체내 시계가 정확할까?","랭킹","1분",B+"count/"),
         ("🚗","AI 운전면허 시험","20문항으로 받는<br>9가지 AI 드라이버 카드","집계 공개","3분",B+"ai/")]),
 "2":dict(kick="PIT STOP", title="잠깐 쉬어가세요", sub="가볍게 즐기고, 결과 카드는 저장·공유하세요", acc="#004098", acc2="#2BB8E6", note="모든 결과는 이미지 저장·카카오톡 공유 가능",
  items=[("🧭","리더 유형 테스트","함께 일할 때 나는 어떤 리더일까?<br>나의 동주공제 리더 카드","카드","2분",B),
         ("💬","MZ어 능력시험","신조어 15문항,<br>나의 MZ어 레벨은?","레벨","2분",B+"mz/"),
         ("✍️","2027 다짐 한 줄","한 줄 다짐을 띄우면<br>대형 화면 다짐 월에 등장","다짐 월","1분",B+"wall/"),
         ("🥠","2027 포춘쿠키","쿠키를 톡 깨서 꺼내는<br>2027 정미년 운세 (1인 3개)","운세","30초",B+"fortune/")]),
}
HEAD=f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>@page{{size:1123px 1587px;margin:0}}html,body{{margin:0}}*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}.e{{font-family:"Noto Color Emoji"}}.m{{font-family:"JetBrains Mono"}}</style></head><body>'
def A(s):  # 다크 계기판 + 2x2 카드
    cards=""
    for i,(em,t,d,tag,tm,u) in enumerate(s["items"]):
        cards+=f'''<div style="background:#fff;border-radius:28px;padding:30px 30px 28px;position:relative;overflow:hidden;box-shadow:0 18px 40px rgba(0,0,0,.28)">
<div style="position:absolute;left:0;top:0;right:0;height:10px;background:{s["acc"]}"></div>
<div style="display:flex;align-items:center;gap:14px"><span class="m" style="font-size:22px;font-weight:700;color:{s["acc"]}">0{i+1}</span><span style="font-size:15px;font-weight:700;color:#5B6576;background:#EEF1F5;border-radius:99px;padding:5px 13px">{tag} · {tm}</span><span class="e" style="margin-left:auto;font-size:42px">{em}</span></div>
<div style="margin-top:12px;font-size:31px;font-weight:900;color:#0B1B36;letter-spacing:-.5px;white-space:nowrap">{t}</div>
<div style="margin-top:8px;font-size:18.5px;line-height:1.55;color:#4A5465;height:58px">{d}</div>
<div style="margin-top:18px;display:flex;justify-content:center"><img src="{qr(u)}" style="width:250px;height:250px;border-radius:12px;border:2px solid #E3E7EE"></div></div>'''
    return HEAD+f'''<div style="width:1123px;height:1587px;position:relative;overflow:hidden;background:radial-gradient(1200px 700px at 85% 0%,#123a73 0%,#0B1B36 55%,#08142a 100%);font-family:'Noto Sans KR';color:#fff">
<div style="position:absolute;left:0;top:0;width:1123px;height:16px;display:flex"><div style="width:786px;background:#E60013"></div><div style="width:337px;background:#004098"></div></div>
<svg style="position:absolute;right:-120px;top:40px;opacity:.13" width="560" height="560" viewBox="0 0 200 200"><circle cx="100" cy="100" r="92" fill="none" stroke="#fff" stroke-width="6"/><circle cx="100" cy="100" r="62" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="4 8"/>{"".join(f'<circle cx="{100+77*__import__("math").cos(k*0.785)}" cy="{100+77*__import__("math").sin(k*0.785)}" r="9" fill="#fff"/>' for k in range(8))}<circle cx="100" cy="100" r="22" fill="#fff"/></svg>
<img src="{LOGOW}" style="position:absolute;left:80px;top:66px;height:34px">
<div style="position:absolute;right:80px;top:68px;font-size:20px;font-weight:700;color:#9FB0C8">26/27년 경영검토회</div>
<div class="m" style="position:absolute;left:80px;top:160px;font-size:26px;font-weight:700;letter-spacing:8px;color:{s["acc2"]}">{s["kick"]}</div>
<div style="position:absolute;left:76px;top:196px;font-size:96px;font-weight:900;letter-spacing:-3px;line-height:1.1">{s["title"]}</div>
<div style="position:absolute;left:80px;top:318px;font-size:26px;font-weight:500;color:#C9D2E0">{s["sub"]}</div>
<div style="position:absolute;left:80px;top:372px;width:120px;height:8px;border-radius:4px;background:{s["acc"]}"></div>
<div style="position:absolute;left:70px;right:70px;top:420px;display:grid;grid-template-columns:1fr 1fr;gap:34px">{cards}</div>
<div style="position:absolute;left:80px;right:80px;bottom:52px;display:flex;justify-content:space-between;align-items:center;font-size:19px;color:#9FB0C8"><span>휴대폰 카메라로 QR을 비추면 바로 시작돼요</span><span>{s["note"]}</span></div>
</div></body></html>'''
def Bd(s):  # 라이트 레이싱 티켓 + 세로 리스트
    rows=""
    for i,(em,t,d,tag,tm,u) in enumerate(s["items"]):
        rows+=f'''<div style="height:236px;display:flex;align-items:center;background:#fff;border-radius:26px;box-shadow:0 10px 30px rgba(11,27,54,.10);overflow:hidden;position:relative">
<div style="width:150px;align-self:stretch;background:{s["acc"] if i%2==0 else "#0B1B36"};display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff"><span class="m" style="font-size:64px;font-weight:700;line-height:1">0{i+1}</span><span class="e" style="font-size:46px;margin-top:14px">{em}</span></div>
<div style="flex:1;padding:0 34px"><div style="display:flex;gap:10px"><span style="font-size:16px;font-weight:700;color:{s["acc"]};border:2px solid {s["acc"]};border-radius:99px;padding:3px 13px">{tag}</span><span style="font-size:16px;font-weight:700;color:#5B6576;background:#EEF1F5;border-radius:99px;padding:5px 13px">{tm}</span></div>
<div style="margin-top:12px;font-size:37px;font-weight:900;color:#0B1B36;letter-spacing:-1px">{t}</div><div style="margin-top:8px;font-size:21px;line-height:1.55;color:#4A5465">{d}</div></div>
<div style="width:2px;align-self:stretch;margin:22px 0;background:repeating-linear-gradient(#CBD3DF 0 10px,transparent 10px 20px)"></div>
<div style="width:250px;display:flex;align-items:center;justify-content:center"><img src="{qr(u)}" style="width:212px;height:212px"></div></div>'''
    chk="".join(f'<div style="width:28px;height:28px;background:{"#0B1B36" if (r+c)%2==0 else "transparent"}"></div>' for r in range(2) for c in range(40))
    return HEAD+f'''<div style="width:1123px;height:1587px;position:relative;overflow:hidden;background:#F2F4F8;font-family:'Noto Sans KR';color:#0B1B36">
<div style="position:absolute;left:-200px;top:-80px;width:1600px;height:500px;background:{s["acc"]};transform:rotate(-3deg);transform-origin:left top"></div>
<div style="position:absolute;left:-200px;top:410px;width:1600px;height:22px;background:#0B1B36;transform:rotate(-3deg);transform-origin:left top"></div>
<img src="{LOGOW}" style="position:absolute;left:80px;top:60px;height:34px">
<div style="position:absolute;right:80px;top:62px;font-size:20px;font-weight:700;color:rgba(255,255,255,.85)">26/27년 경영검토회</div>
<div style="position:absolute;left:80px;top:140px;color:#fff"><span style="font-family:Jua;font-size:30px;letter-spacing:2px;background:#0B1B36;padding:6px 18px;border-radius:10px">{s["kick"]}</span></div>
<div style="position:absolute;left:76px;top:196px;font-family:Jua;font-size:104px;line-height:1.05;color:#fff;letter-spacing:-1px">{s["title"]}</div>
<div style="position:absolute;left:80px;top:316px;font-size:25px;font-weight:700;color:rgba(255,255,255,.92)">{s["sub"]}</div>
<div style="position:absolute;left:70px;right:70px;top:470px;display:flex;flex-direction:column;gap:20px">{rows}</div>
<div style="position:absolute;left:0;bottom:0;width:1123px;height:56px;display:flex;flex-wrap:wrap;opacity:.9">{chk}</div>
<div style="position:absolute;left:80px;right:80px;bottom:76px;display:flex;justify-content:space-between;font-size:19px;color:#5B6576"><span>QR을 휴대폰 카메라로 비추면 바로 시작</span><span>{s["note"]}</span></div>
</div></body></html>'''
for k,s in SHEETS.items():
    open(f'z{k}A.html','w').write(A(s)); open(f'z{k}B.html','w').write(Bd(s))
