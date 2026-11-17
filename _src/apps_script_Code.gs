/**
 * 26/27년 경영검토회 쉬어가는 코너 — 응답 수집용 Google Apps Script (일곱 콘텐츠 공용)
 *  1) 리더십 테스트      https://imsean629.github.io/sangsin-leader-2027/         → '응답' 탭
 *  2) 브레이크 챌린지    https://imsean629.github.io/sangsin-leader-2027/brake/   → '브레이크' 탭
 *  3) MZ어 능력시험      https://imsean629.github.io/sangsin-leader-2027/mz/      → 'MZ퀴즈' 탭
 *  4) 2027 다짐 월       https://imsean629.github.io/sangsin-leader-2027/wall/    → '다짐' 탭
 *     '다짐' 탭의 hide 칸에 아무 글자(예: x)나 넣으면 그 다짐은 월 화면에서 바로 빠집니다.
 *  5) 2026 상식 레이스   https://imsean629.github.io/sangsin-leader-2027/quiz/    → '상식퀴즈' 탭
 *  6) 속마음 타이머      https://imsean629.github.io/sangsin-leader-2027/count/   → '타이머' 탭 (재도전 가능, 이름별 최고 기록)
 *  7) AI 운전면허 시험    https://imsean629.github.io/sangsin-leader-2027/ai/      → 'AI활용' 탭 (익명 가능, 집계 화면용)
 *     └ 이어지는 2부 AI에 대한 나의 생각(익명, 9유형 카드)                                              → 'AI관점' 탭 (한마디 의견은 시트에만 저장, 화면 공개 안 함)
 *     1인 1회: 같은 이름의 두 번째 기록은 받지 않습니다. 관리자가 '상식퀴즈' 탭의 행(또는 탭 전체)을 지우면
 *     그 사람은 다시 참여할 수 있습니다(휴대폰의 참여 잠금도 자동으로 풀림).
 * script.google.com 에서 새 프로젝트를 만들고 이 코드를 붙여넣어 웹앱으로 배포합니다(회사망에서는 차단될 수 있음).
 * 배포 후 받은 웹앱 URL 하나를 일곱 페이지의 CONFIG.SHEET_URL 에 똑같이 넣습니다.
 */
const SHEET_ID = '1XPvG7d9ymy7R2F2Mv3rD-q8vqY7kguHBZddQOnQcwaI'; // 「26/27 경영검토회 리더십테스트 응답」 시트

const TABS = {
  leader: { name: '응답', cols: ['ts', 'nickname', 'result', 'resultName', 'rule',
    'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8',
    't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8',
    'score_N', 'score_B', 'score_S', 'score_R', 'score_W', 'sid', 'v'] },
  brake: { name: '브레이크', cols: ['ts', 'nickname', 'team', 'best', 'avg', 'r1', 'r2', 'r3', 'fouls', 'grade', 'sid'] },
  mz: { name: 'MZ퀴즈', cols: ['ts', 'nickname', 'score', 'level', 'answers', 'wrong', 'sid'] },
  wall: { name: '다짐', cols: ['ts', 'nickname', 'text', 'hide', 'sid'] },
  aiview: { name: 'AI관점', cols: ['ts', 'role', 'horizon', 'outlook', 'hopes', 'worries', 'scope', 'purpose', 'first', 'type', 'usage', 'comment', 'sid'] },
  ai: { name: 'AI활용', cols: ['ts', 'nickname', 'score', 'level', 'a_freq', 'a_range', 'a_skill', 'a_resp', 'answers', 'uses', 'tools', 'sid'] },
  count: { name: '타이머', cols: ['ts', 'nickname', 'total_ms', 'r1', 'r2', 'r3', 'grade', 'sid'] },
  quiz: { name: '상식퀴즈', cols: ['ts', 'nickname', 'score', 'level', 'time_ms', 'f_econ', 'f_soc', 'f_intl', 'f_work', 'f_sci', 'answers', 'note', 'sid'] },
};

function sheet_(kind) {
  const t = TABS[kind];
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sh = ss.getSheetByName(t.name);
  if (!sh) { sh = ss.insertSheet(t.name); sh.appendRow(t.cols); sh.setFrozenRows(1); }
  return sh;
}

function clean_(v) {
  if (v === null || v === undefined) return '';
  if (typeof v === 'number') return v;
  let s = String(v).slice(0, 300);
  if (/^[=+\-@]/.test(s)) s = "'" + s; // 수식 주입 방지
  return s;
}

// 응답 기록: 같은 sid(같은 참여)면 그 행을 갱신, 아니면 새 행
function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const d = JSON.parse(e.postData.contents);
    if (!d || !d.sid) return ContentService.createTextOutput('ignored');
    const kind = TABS[d.kind] ? d.kind : 'leader';
    if (kind === 'brake' && !(d.best >= 100 && d.best < 5000)) return ContentService.createTextOutput('ignored');
    if (kind === 'wall') { d.text = String(d.text || '').replace(/\s+/g, ' ').trim().slice(0, 60); d.nickname = String(d.nickname || '').trim().slice(0, 10); d.hide = BLOCK_.test(d.text + d.nickname) ? 'auto' : ''; if (!d.text) return ContentService.createTextOutput('ignored'); }
    if (kind === 'quiz' && !(d.score >= 0 && d.score <= 100)) return ContentService.createTextOutput('ignored');
    if (kind === 'ai' && !(d.score >= 0 && d.score <= 100)) return ContentService.createTextOutput('ignored');
    if (kind === 'count' && !(d.total_ms >= 0 && d.total_ms < 120000 && d.r1 > 300 && d.r2 > 300 && d.r3 > 300)) return ContentService.createTextOutput('ignored');
    const t = TABS[kind], sh = sheet_(kind);
    if (kind === 'quiz') { // 1인 1회: 다른 참여(sid)로 같은 이름이 이미 있으면 무시
      const cols = t.cols, last0 = sh.getLastRow();
      if (last0 > 1) {
        const rs = sh.getRange(2, 1, last0 - 1, cols.length).getValues();
        const nm = String(d.nickname || '').trim();
        if (rs.some(r => String(r[cols.indexOf('nickname')]).replace(/^'/, '').trim() === nm && String(r[cols.indexOf('sid')]) !== String(d.sid))) return ContentService.createTextOutput('duplicate');
      }
    }
    if (kind === 'brake') { // 같은 기기(sid)는 더 빠른 기록일 때만 갱신
      const cols = t.cols, last0 = sh.getLastRow();
      if (last0 > 1) {
        const rs = sh.getRange(2, 1, last0 - 1, cols.length).getValues();
        const old = rs.find(r => String(r[cols.indexOf('sid')]) === String(d.sid));
        if (old && Number(old[cols.indexOf('best')]) > 0 && Number(old[cols.indexOf('best')]) <= Number(d.best)) return ContentService.createTextOutput('kept');
      }
    }
    const row = t.cols.map(c => clean_(d[c]));
    const sidCol = t.cols.indexOf('sid') + 1, last = sh.getLastRow();
    if (last > 1) {
      const ids = sh.getRange(2, sidCol, last - 1, 1).getValues().map(r => r[0]);
      const i = ids.indexOf(d.sid);
      if (i >= 0) { sh.getRange(i + 2, 1, 1, t.cols.length).setValues([row]); return ContentService.createTextOutput('updated'); }
    }
    sh.appendRow(row);
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}

// 브레이크 챌린지 순위 조회: ?type=brake
//  - top: 기기(sid)별 최고 기록 전체 순위(최대 300)
//  - teams: 소속별 평균(3명 이상), bests: 사람별 최고 기록 목록(내 순위 계산용)
function doGet(e) {
  if (e && e.parameter && e.parameter.type === 'wall') return wall_();
  if (e && e.parameter && e.parameter.type === 'quiz') return quiz_(e.parameter);
  if (e && e.parameter && e.parameter.type === 'count') return count_();
  if (e && e.parameter && e.parameter.type === 'ai') return ai_();
  if (e && e.parameter && e.parameter.type === 'aiview') return aiview_();
  if (!e || !e.parameter || e.parameter.type !== 'brake') return json_({ ok: true });
  const sh = sheet_('brake'), cols = TABS.brake.cols, last = sh.getLastRow();
  const rows = last > 1 ? sh.getRange(2, 1, last - 1, cols.length).getValues() : [];
  const ix = c => cols.indexOf(c);
  const people = {};
  rows.forEach(r => {
    const best = Number(r[ix('best')]); if (!(best > 0)) return;
    const key = String(r[ix('sid')]) || (String(r[ix('nickname')]) + '|' + String(r[ix('team')])); // 기기(sid)별 1명
    if (!people[key] || best < people[key].best) people[key] = { nickname: String(r[ix('nickname')]), team: String(r[ix('team')]), best: best, sid: String(r[ix('sid')]) };
  });
  const list = Object.keys(people).map(k => people[k]).sort((a, b) => a.best - b.best);
  const teams = {};
  list.forEach(p => { if (!p.team) return; (teams[p.team] = teams[p.team] || []).push(p.best); });
  const teamList = Object.keys(teams).filter(t => teams[t].length >= 3)
    .map(t => ({ team: t, n: teams[t].length, avg: Math.round(teams[t].reduce((a, b) => a + b, 0) / teams[t].length) }))
    .sort((a, b) => a.avg - b.avg);
  return json_({ count: list.length, top: list.slice(0, 300), bests: list.map(p => p.best), teams: teamList });
}

// 다짐 월 조회: ?type=wall — 숨김(hide) 표시가 없는 최근 120개
const BLOCK_ = /(시발|씨발|ㅅㅂ|ㅆㅂ|병신|ㅂㅅ|개새|좆|존나|ㅈㄴ|닥쳐|꺼져|미친놈|미친년|fuck|shit)/i;
function wall_() {
  const sh = sheet_('wall'), cols = TABS.wall.cols, last = sh.getLastRow();
  const rows = last > 1 ? sh.getRange(2, 1, last - 1, cols.length).getValues() : [];
  const ix = c => cols.indexOf(c);
  const items = rows.filter(r => !String(r[ix('hide')]).trim() && String(r[ix('text')]).trim())
    .map(r => ({ id: String(r[ix('sid')]), name: String(r[ix('nickname')]).replace(/^'/, ''), text: String(r[ix('text')]).replace(/^'/, '') }));
  return json_({ count: items.length, items: items.slice(-120) });
}

// 상식 레이스: ?type=quiz            → 순위판 {count, avg, top(10), list[[점수,시간]]}
//              ?type=quiz&name=이름  → {exists} 같은 이름 참여 여부
//              ?type=quiz&sid=참여ID → {exists} 내 기록이 남아 있는지(관리자 리셋 확인)
function quiz_(p) {
  const sh = sheet_('quiz'), cols = TABS.quiz.cols, last = sh.getLastRow();
  const rows = last > 1 ? sh.getRange(2, 1, last - 1, cols.length).getValues() : [];
  const ix = c => cols.indexOf(c), str = v => String(v).replace(/^'/, '').trim();
  if (p.name) return json_({ exists: rows.some(r => str(r[ix('nickname')]) === String(p.name).trim()) });
  if (p.sid) return json_({ exists: rows.some(r => str(r[ix('sid')]) === String(p.sid)) });
  const list = rows.filter(r => str(r[ix('nickname')]) !== '' && r[ix('score')] !== '')
    .map(r => ({ nickname: str(r[ix('nickname')]), score: Number(r[ix('score')]), time: Number(r[ix('time_ms')]) || 0 }))
    .sort((a, b) => b.score - a.score || a.time - b.time);
  const avg = list.length ? Math.round(list.reduce((s, x) => s + x.score, 0) / list.length) : 0;
  return json_({ count: list.length, avg: avg, top: list.slice(0, 10), list: list.map(x => [x.score, x.time]) });
}

// 속마음 타이머: ?type=count → {count, top(10), list[이름별 최고 오차]}
function count_() {
  const sh = sheet_('count'), cols = TABS.count.cols, last = sh.getLastRow();
  const rows = last > 1 ? sh.getRange(2, 1, last - 1, cols.length).getValues() : [];
  const ix = c => cols.indexOf(c), best = {};
  rows.forEach(r => {
    const n = String(r[ix('nickname')]).replace(/^'/, '').trim(), t = Number(r[ix('total_ms')]);
    if (!n || !(t >= 0)) return;
    if (!(n in best) || t < best[n]) best[n] = t;
  });
  const list = Object.keys(best).map(n => ({ nickname: n, total: best[n] })).sort((a, b) => a.total - b.total);
  return json_({ count: list.length, top: list.slice(0, 10), list: list.map(x => x.total) });
}

// AI 운전면허: ?type=ai → 집계 {count, avg, axes{freq,range,skill,resp}, levels{}, uses{}, tools{}}
function ai_() {
  const sh = sheet_('ai'), cols = TABS.ai.cols, last = sh.getLastRow();
  const rows = last > 1 ? sh.getRange(2, 1, last - 1, cols.length).getValues() : [];
  const ix = c => cols.indexOf(c), str = v => String(v).replace(/^'/, '').trim();
  const ok = rows.filter(r => r[ix('score')] !== '' && !isNaN(Number(r[ix('score')])));
  const n = ok.length, avg = k => n ? Math.round(ok.reduce((s, r) => s + Number(r[ix(k)] || 0), 0) / n) : 0;
  const tally = k => { const o = {}; ok.forEach(r => str(r[ix(k)]).split('|').filter(x => x).forEach(x => { o[x] = (o[x] || 0) + 1; })); return o; };
  const levels = {}; ok.forEach(r => { const l = str(r[ix('level')]); if (l) levels[l] = (levels[l] || 0) + 1; });
  return json_({ count: n, avg: avg('score'), axes: { freq: avg('a_freq'), range: avg('a_range'), skill: avg('a_skill'), resp: avg('a_resp') }, levels: levels, uses: tally('uses'), tools: tally('tools') });
}

// AI 관점(2부): ?type=aiview → 문항별 선택 수 {count, role{}, horizon{}, outlook{}, hopes{}, worries{}, scope{}, purpose{}, first{}} (의견 원문은 반환 안 함)
function aiview_() {
  const sh = sheet_('aiview'), cols = TABS.aiview.cols, last = sh.getLastRow();
  const rows = last > 1 ? sh.getRange(2, 1, last - 1, cols.length).getValues() : [];
  const keys = ['role', 'horizon', 'outlook', 'hopes', 'worries', 'scope', 'purpose', 'first', 'type', 'usage'], out = { count: 0 };
  keys.forEach(k => out[k] = {});
  rows.forEach(r => {
    if (!String(r[cols.indexOf('outlook')]).trim()) return;
    out.count++;
    keys.forEach(k => String(r[cols.indexOf(k)]).replace(/^'/, '').split('|').map(x => x.trim()).filter(x => x).forEach(x => { out[k][x] = (out[k][x] || 0) + 1; }));
  });
  return json_(out);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
