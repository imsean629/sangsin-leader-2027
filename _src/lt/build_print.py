# -*- coding: utf-8 -*-
"""A3 포스터(1123x1587px = A3 @96dpi)와 질문·채점표(A4) 생성"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from data import TYPES, ORDER, QUESTIONS, STAT_LABELS, exposures
from build import LOCAL_FONTS, GF, selfclose

HERE = os.path.dirname(os.path.abspath(__file__))
RED, BLUE, NAVY, INK = "#E60013", "#004098", "#0B1B36", "#16191E"
SANS = "'Noto Sans KR', sans-serif"
LET = "ABCDE"


def poster(logo, qr=None):
    q, opts = QUESTIONS[0]
    rows = "".join(f'''
      <div style="display:flex;gap:18px;align-items:center;background:#FFFFFF;border:3px solid {INK};border-radius:18px;padding:15px 22px;">
        <span style="flex:0 0 52px;height:52px;border-radius:26px;background:{INK};color:#FFFFFF;font-family:{SANS};font-weight:900;font-size:28px;line-height:52px;text-align:center;">{LET[i]}</span>
        <span style="font-family:{SANS};font-weight:700;font-size:29px;line-height:1.4;color:{INK};word-break:keep-all;">{l}</span>
      </div>''' for i, (t, l) in enumerate(opts))
    backs = "".join(f'<div style="width:96px;height:136px;border-radius:12px;background:{NAVY};display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-family:{SANS};font-weight:900;font-size:44px;transform:rotate({r}deg);box-shadow:0 5px 0 rgba(0,0,0,0.18);outline:2px solid rgba(255,255,255,0.35);outline-offset:-10px;">?</div>'
                    for r in (-6, 4, -3, 5, -5))
    qr_box = (f'''<div style="width:270px;display:flex;flex-direction:column;align-items:center;gap:6px;">
          <div style="width:270px;height:270px;box-sizing:border-box;background:#FFFFFF;border:4px solid {INK};border-radius:14px;padding:8px;"><img src="{qr}" alt="테스트 접속 QR" style="display:block;width:246px;height:246px;"/></div>
          <span style="font-family:{SANS};font-weight:700;font-size:13px;color:#4A515C;white-space:nowrap;letter-spacing:-0.2px;">imsean629.github.io/sangsin-leader-2027</span>
        </div>''' if qr else
              f'''<div style="width:270px;height:270px;box-sizing:border-box;border:4px dashed {INK};border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;background:#FFFFFF;">
          <span style="font-family:{SANS};font-weight:900;font-size:34px;color:{INK};">QR 자리</span>
          <span style="font-family:{SANS};font-weight:500;font-size:19px;color:#4A515C;text-align:center;line-height:1.4;">최종 주소 확정 후<br/>삽입 (약 70×70mm)</span>
        </div>''')
    steps = "".join(f'''
        <div style="display:flex;gap:14px;align-items:flex-start;">
          <span style="flex:0 0 40px;height:40px;border-radius:20px;background:{RED};color:#FFFFFF;font-family:{SANS};font-weight:900;font-size:22px;line-height:40px;text-align:center;">{n}</span>
          <span style="font-family:{SANS};font-weight:700;font-size:25px;line-height:1.45;color:{INK};word-break:keep-all;">{t}</span>
        </div>''' for n, t in ((1, "휴대폰 카메라로 QR을 비춰 접속"), (2, "닉네임 정하고, 상황 8개에 답하기"), (3, "닉네임이 새겨진 리더 카드 공개 → 저장하고 동료와 비교")))
    return f'''
<div style="position:relative;width:1123px;height:1587px;overflow:hidden;background:#F4F2EE;font-family:{SANS};">
  <div style="position:absolute;top:0;left:0;width:1123px;height:16px;display:flex;"><div style="width:786px;height:16px;background:{RED};"></div><div style="width:337px;height:16px;background:{BLUE};"></div></div>
  <div style="position:absolute;top:74px;left:80px;width:963px;display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:{SANS};font-weight:900;font-size:30px;color:{INK};">26/27년 경영검토회</span>
    <span style="background:{INK};color:#FFFFFF;font-family:{SANS};font-weight:700;font-size:22px;line-height:1;padding:12px 18px;border-radius:999px;">쉬어가는 코너 · 약 2분</span>
  </div>
  <div style="position:absolute;top:140px;left:80px;width:963px;font-family:{SANS};font-weight:900;font-size:100px;line-height:1.18;color:{INK};letter-spacing:-4px;">함께 일할 때,<br/>나는 <span style="color:{RED};">어떤 리더</span>일까?</div>
  <div style="position:absolute;top:404px;left:80px;width:963px;font-family:{SANS};font-weight:500;font-size:30px;line-height:1.5;color:#2E333A;">팀이 난관을 만났을 때, 내가 <b style="font-weight:900;color:{INK};">실제로 가장 먼저 하는 행동</b>은?<br/>정답은 없습니다. 직급과도 상관없습니다.</div>
  <div style="position:absolute;top:528px;left:80px;width:963px;box-sizing:border-box;border-radius:26px;background:#FFE8E3;padding:30px 36px 34px;">
    <div style="font-family:{SANS};font-weight:900;font-size:24px;color:{RED};letter-spacing:1px;">첫 번째 질문 · 상황 01</div>
    <div style="margin-top:12px;font-family:{SANS};font-weight:900;font-size:44px;line-height:1.35;color:{INK};letter-spacing:-1px;word-break:keep-all;">회의가 길어지는데,<br/>무엇을 결정해야 할지 흐려졌다.</div>
    <div style="margin-top:12px;font-family:{SANS};font-weight:700;font-size:25px;color:#4A515C;">나라면 가장 먼저…</div>
    <div style="margin-top:18px;display:flex;flex-direction:column;gap:14px;">{rows}
    </div>
  </div>
  <div style="position:absolute;top:1150px;left:80px;width:963px;display:flex;gap:44px;align-items:center;">
    {qr_box}
    <div style="flex:1;display:flex;flex-direction:column;gap:18px;">
      <div style="font-family:{SANS};font-weight:900;font-size:34px;line-height:1.3;color:{INK};">답을 골랐다면,<br/>QR로 이어서 해 보세요</div>
      {steps}
    </div>
  </div>
  <div style="position:absolute;top:1464px;left:80px;width:963px;height:2px;background:#CFCBC2;"></div>
  <div style="position:absolute;top:1488px;left:80px;width:963px;display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:{SANS};font-weight:500;font-size:19px;color:#4A515C;">닉네임으로 참여합니다. 닉네임과 응답은 행사 통계용으로만 저장됩니다.</span>
    <img src="{logo}" alt="SANGSIN BRAKE" style="width:260px;height:26px;"/>
  </div>
</div>'''


def scoring():
    E = exposures()
    tn = lambda k: TYPES[k]["short"]
    qrows = ""
    for i, (q, opts) in enumerate(QUESTIONS, 1):
        tag = "동점 우선순위" if i == 8 else "채점"
        for j, (t, l) in enumerate(opts):
            qrows += (f'<tr>{"<td rowspan=%d class=qn><b>%d</b><br/><span>%s</span></td><td rowspan=%d class=qt>%s</td>" % (len(opts), i, tag, len(opts), q) if j == 0 else ""}'
                      f'<td class=c>{LET[j]}</td><td>{l}</td><td class=c><span class=tg style="background:{TYPES[t]["color"]}">{tn(t)}</span></td></tr>')
    erows = "".join(f'<tr><td>{TYPES[k]["name"]}</td><td class=c>{E[k]}</td><td>{", ".join(str(i) for i, (_, o) in enumerate(QUESTIONS[:7], 1) if k in [t for t, _ in o])}번</td></tr>' for k in ORDER)
    crows = "".join(f'<tr><td><b>{TYPES[k]["name"]}</b></td><td>{TYPES[k]["strength"]}</td><td><b>{TYPES[k]["skill"]}</b> · {TYPES[k]["skill_desc"]}</td><td>{TYPES[k]["grow"]}</td><td class=c>{" ".join(str(v) for v in TYPES[k]["stats"])}</td></tr>' for k in ORDER)
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>질문·채점표</title>{LOCAL_FONTS}
<style>
@page{{size:A4;margin:16mm 14mm}}
body{{font-family:{SANS};color:{INK};font-size:12.5px;line-height:1.55;word-break:keep-all}}
h1{{font-size:22px;margin:0}} h2{{font-size:16px;margin:22px 0 8px;padding-bottom:4px;border-bottom:2px solid {INK}}}
.sub{{color:#4A515C;margin-top:4px}}
table{{width:100%;border-collapse:collapse;margin-top:6px}}
th,td{{border:1px solid #9AA1AC;padding:5px 7px;vertical-align:top;text-align:left}}
th{{background:#EEF0F3;font-weight:700}}
td.c{{text-align:center;white-space:nowrap}} td.qn{{text-align:center;width:52px}} td.qn span{{font-size:10.5px;color:#4A515C}} td.qt{{width:170px;font-weight:700}}
.tg{{color:#FFFFFF;font-weight:700;padding:2px 7px;border-radius:9px;font-size:11.5px}}
ol{{margin:6px 0 0;padding-left:20px}} li{{margin:3px 0}}
.box{{background:#F4F2EE;padding:10px 12px;border-radius:6px;margin-top:8px}}
</style></head><body>
<h1>「함께 일할 때, 나는 어떤 리더일까?」 질문·채점표</h1>
<div class="sub">26/27년 경영검토회 쉬어가는 코너 · 동주공제(同舟共濟) 리더십 카드 · 검토용</div>

<h2>1. 결과 산정 규칙</h2>
<ol>
<li><b>채점 문항은 1~7번</b>입니다. 각 선택지는 다섯 유형 중 하나에 연결되어 있고, 고른 선택지의 유형에 1회씩 셉니다.</li>
<li>유형마다 선택지로 나온 횟수가 다르므로(아래 표), <b>유형 점수 = 그 유형을 고른 횟수 ÷ 그 유형이 선택지로 나온 횟수</b>로 보정합니다.</li>
<li>보정 점수가 가장 높은 유형이 결과입니다.</li>
<li>공동 1위가 생기면: <b>8번에서 고른 유형이 공동 1위 안에 있으면 그 유형</b>을 보여줍니다. 없으면 <b>공동 1위 유형 중 하나를 공평하게 추첨</b>합니다.</li>
<li>채점은 응답자의 휴대폰 화면 안에서 이루어지고, 결과가 공개될 때 닉네임과 응답(고른 보기, 결과 유형, 보정 점수)이 행사 통계용으로 기록됩니다. 기록 항목과 내려받는 방법은 「관리자 데이터 가이드」를 참고하세요.</li>
</ol>
<div class="box">검증: 1~8번 응답 조합 전체(10,935가지)를 계산했을 때 다섯 결과가 모두 나오며, 각 결과 비율은 약 18~23%입니다(무작위로 답했다고 가정한 분포이며, 실제 응답 분포와는 다를 수 있습니다).</div>

<h2>2. 유형별 선택지 노출 횟수 (1~7번)</h2>
<table><tr><th>유형</th><th class=c>노출 횟수</th><th>나오는 문항</th></tr>{erows}</table>

<h2>3. 문항과 선택지별 유형</h2>
<table><tr><th class=c>No</th><th>상황</th><th class=c>보기</th><th>선택지</th><th class=c>유형</th></tr>{qrows}</table>

<h2>4. 결과 카드 5종</h2>
<table><tr><th>유형</th><th>어려울 때 발휘하는 강점</th><th>고유 스킬</th><th>보완하면 좋을 점</th><th class=c>능력치<br/>({"·".join(STAT_LABELS)})</th></tr>{crows}</table>
<div class="sub" style="margin-top:6px">※ 능력치는 카드 캐릭터의 설정값이며, 결과 화면에 “개인의 역량 평가가 아님”을 표시합니다.</div>

<h2>5. 카드 삽화</h2>
<div>결과 카드에는 제공된 캐릭터 이미지 5종(항해장·갑판장·선발대장·수리장·파수장)을 사용합니다. 교체하려면 lt/src_img 폴더에 같은 유형 코드 이름(N·B·S·R·W)으로 넣고 다시 빌드합니다.</div>
</body></html>'''


def page(body, w, h):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>A3 포스터</title>{LOCAL_FONTS}'
            f'<style>@page{{size:{w}px {h}px;margin:0}}html,body{{margin:0;padding:0}}*{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}</style></head><body>{body}</body></html>')


def dc(body, title, w, h):
    body = selfclose(body).replace("<br/>", "<br>")
    body = re.sub(r'<img ([^>]*?)/>', r'<img \1>', body)
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="{GF}">
<style>
body{{margin:0}}
a{{color:#004098}}a:hover{{color:#E60013}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    local_logo = "file:///home/claude/xb/assets/logo_en.png"
    qr_local = "file:///home/claude/xb/lt/out/qr_leader_test.svg"
    open(os.path.join(HERE, "out", "poster.html"), "w").write(page(poster(local_logo, qr_local), 1123, 1587))
    open(os.path.join(HERE, "out", "scoring.html"), "w").write(scoring())
    if len(sys.argv) > 1:
        os.makedirs(os.path.join(HERE, "canvas", "project"), exist_ok=True)
        open(os.path.join(HERE, "canvas", "project", "Main.dc.html"), "w").write(dc(poster(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None), "A3 포스터 — 함께 일할 때, 나는 어떤 리더일까?", 1123, 1587))
    print("ok")
