# 참여형 콘텐츠 제작 키트 (26/27년 경영검토회에서 사용)

이 폴더는 GitHub Pages에 공개되지 않습니다(밑줄로 시작하는 폴더는 Jekyll이 제외).
새 스레드/새 저장소에서 같은 형태의 콘텐츠를 만들 때 출발점으로 씁니다.

## 구조
| 폴더 | 콘텐츠 | 비고 |
|---|---|---|
| lt | 리더 유형 테스트 (루트 /) | build_app.py, data.py, app_template.html, build_print.py(포스터) |
| brake | 브레이크 반응속도 챌린지 | 순위판 #board CSS의 원본 (다른 콘텐츠가 재사용) |
| mz | MZ어 능력시험 | |
| wall | 2027 다짐 한 줄 월 | #wall 대형 화면, #walldemo |
| quiz | 2026 상식 레이스 | 1인 1회 + 관리자 리셋 |
| fortune | 2027 포춘쿠키 | 기기당 3개 |
| count | 속마음 타이머 | |
| ai | AI 운전면허 + AI 관점(9유형 카드) | #board, #view |
| zone | QR 4개 묶음 A3 포스터 A/B | |
| apps_script_Code.gs | 모든 콘텐츠 공용 Google Apps Script (kind별 탭 라우팅) | |

각 콘텐츠 = `data.py`(문항·문구) + `template.html`(단일 파일 앱) + `build.py`(데이터·로고·QR·html2canvas·SHEET_URL 주입 → out/index.html, out/index_mock.html) + `test.py`(Playwright, 시트는 https://mock.sheet.test/** 로 가짜 응답).

## 새 환경에서 복원
빌드 스크립트는 절대경로 `/home/claude/xb/...`를 씁니다. 그대로 맞추면 수정 없이 동작합니다.
```bash
mkdir -p /home/claude/xb && cp -r _src/* /home/claude/xb/
mkdir -p /home/claude/xb/lt/vendor/node_modules/html2canvas/dist && cp _src/vendor/html2canvas.min.js /home/claude/xb/lt/vendor/node_modules/html2canvas/dist/
cd /home/claude/xb/fonts && npm i @fontsource/noto-sans-kr @fontsource/noto-serif-kr @fontsource/jetbrains-mono @fontsource/jua @fontsource/gaegu @fontsource/nanum-pen-script @fontsource/gowun-batang
pip install segno playwright pillow opencv-python-headless pyzbar --break-system-packages   # 크롬: /usr/bin/google-chrome
```

## 공통 규칙
- 디자인: 상신 CI — 빨강 #E60013, 파랑 #004098, 네이비 #0B1B36, 골드 #E8C35A. 상단 빨강/파랑 띠, 영문 로고(assets/logo_en*.png). 폰트 Noto Sans KR.
- 결과 화면: 카드 이미지 저장(미리 캡처한 PNG, iOS는 navigator.share files) + 카카오톡 공유(Web Share API, 안 되면 링크 복사).
- 시트 전송: `fetch(SHEET_URL, {method:'POST', mode:'no-cors', headers:{'Content-Type':'text/plain;charset=utf-8'}, body: JSON.stringify({kind, sid, ...})})`. Apps Script가 TABS[kind] 탭에 sid 기준 upsert, =+-@ 로 시작하는 값은 ' 접두.
- 새 콘텐츠 추가 = TABS에 `{name, cols}` 추가 + (필요하면) doGet `?type=` 집계 함수 추가 → Apps Script **배포 관리 → 새 버전**(URL 유지). 기존 탭에 열을 추가하면 탭을 지우고 새로 만들게 해야 함(제목 줄은 탭 생성 시에만 기록).
- 대형 화면: 주소 뒤 해시(#board 등)로 같은 페이지가 집계판 모드로 전환.
- A3 포스터: 1123×1587px HTML → PDF 297×420mm (scale = 297/(1123*25.4/96)). QR은 segno error='q', 짙은색 #0B1B36. 인쇄 전 pyzbar로 QR 해독 확인.
- 배포: 저장소 폴더에 index.html(+og.png) 복사 → commit → push. 1~2분 뒤 Pages 반영.
