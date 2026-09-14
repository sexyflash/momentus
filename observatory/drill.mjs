#!/usr/bin/env node
/**
 * 경보 드릴 — **🔴 가 실제로 우는지 눈으로 보고 되돌린다.** (docs/OBSERVATORY.md 자[尺] 5번)
 *
 * 왜 필요한가: 안 울리는 경보는 장식이다. 이 저장소는 "도입 후 3개월간 한 번도 발동 안 한
 * 안전망"을 실제로 겪었다(slack-bot 룰 #14). 그래서 **경보는 만들 때 한 번 울려보고 끝낸다.**
 *
 * 하는 일
 *   ① 원장을 백업한다
 *   ② **가짜 전주(W-1) 행**을 붙여 이번 주 실측값이 나쁘게 보이게 만든다 (값을 지어내는 건
 *      드릴 안에서만이고, 끝나면 원본으로 되돌린다)
 *   ③ 진짜 판정기(judge)를 진짜 렌더러로 통과시켜 🔴 가 뜨는지 확인한다
 *   ④ 원장을 복원하고 🔴 가 사라지는 것까지 확인한다
 *
 * 🚫 "돌려봤더니 되더라"로 끝내지 마라 — 이 스크립트는 **기대한 경보가 안 뜨면 실패(rc=1)** 한다.
 *
 *   node observatory/drill.mjs            # 드릴 실행(끝나면 원장 원상복구)
 *   node observatory/drill.mjs --keep     # 복원하지 않고 남긴다(수동 확인용)
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { readLedger, collapse, prevWeekKey, weekKey, table } from './collect.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const LEDGER = path.join(HERE, 'data', 'ledger.jsonl');
const BAK = `${LEDGER}.drill-bak`;

const wk = process.argv.includes('--week') ? process.argv[process.argv.indexOf('--week') + 1] : weekKey();
const pw = prevWeekKey(wk);

const cur = [...collapse(readLedger()).values()].filter((r) => r.week === wk);
if (!cur.length) { console.error(`🔴 원장에 ${wk} 행이 없다 — 먼저 collect.mjs 를 한 번 돌려라`); process.exit(1); }
const by = (id) => cur.find((r) => r.site === id);

// ── 가짜 전주 행. **이번 주 실측값 기준으로** 경보 조건을 넘게 만든다.
const fakes = [];
const expect = [];

const cue = by('cue');
if (cue && typeof cue.crawl?.total === 'number') {
  // 크롤 −50%: 전주를 이번 주의 3배로 두면 이번 주가 절반 밑으로 떨어진다
  fakes.push({ at: 'DRILL', week: pw, site: 'cue', label: cue.label, domain: cue.domain,
    crawl: { total: cue.crawl.total * 3, bots: {}, days: 7 }, index: null, gsc: null, bing: null, ga: null });
  expect.push(['크롤 급감', cue.label]);
}

const team = by('teamai');
if (team && typeof team.index?.orphanPct === 'number' && team.index.orphanPct >= 16) {
  // 고아율 급증: 전주를 15pp 이상 낮게 둔다
  fakes.push({ at: 'DRILL', week: pw, site: 'teamai', label: team.label, domain: team.domain,
    crawl: null, index: { ...team.index, orphans: 1, orphanPct: 1 }, gsc: null, bing: null, ga: null });
  expect.push(['고아율 급증', team.label]);
}

const zero = cur.find((r) => r.ga?.week?.sessions === 0);
if (zero) {
  // GA 세션 0: 전주엔 있었던 것으로 둔다
  fakes.push({ at: 'DRILL', week: pw, site: zero.site, label: zero.label, domain: zero.domain,
    crawl: null, index: null, gsc: null, bing: null, ga: { week: { users: 40, sessions: 40, views: 40, sources: [] }, wide: { sources: [] } } });
  expect.push(['GA 세션 0', zero.label]);
}

// FAIL 신규: 전주 FAIL 0 → 이번 주 실측 FAIL>0 인 사이트
const failing = cur.find((r) => typeof r.index?.fail === 'number' && r.index.fail > 0 && !fakes.some((f) => f.site === r.site));
if (failing) {
  fakes.push({ at: 'DRILL', week: pw, site: failing.site, label: failing.label, domain: failing.domain,
    crawl: null, index: { ...failing.index, fail: 0 }, gsc: null, bing: null, ga: null });
  expect.push(['FAIL', failing.label]);
}

if (!fakes.length) { console.error('🔴 드릴을 걸 자리가 없다 — 이번 주 실측이 전부 비어 있나?'); process.exit(1); }

// 드릴 **전**의 경보 집합을 먼저 잡아둔다. 복원 확인은 "패턴이 사라졌나"가 아니라
// **"드릴 전과 똑같아졌나"** 로 해야 한다 — 첫 회 기준선 경보처럼 원래 있던 🔴 는 남는 게 맞다.
const baseline = new Set(table(cur, readLedger()).alerts.filter((a) => a.lv === 'bad').map((a) => a.t));

fs.copyFileSync(LEDGER, BAK);
let rc = 0;
try {
  fs.appendFileSync(LEDGER, fakes.map((f) => JSON.stringify(f)).join('\n') + '\n');
  const { alerts } = table(cur, readLedger());
  const bad = alerts.filter((a) => a.lv === 'bad').map((a) => a.t);
  console.log(`\n── 드릴: 가짜 전주(${pw}) ${fakes.length}행을 넣고 ${wk} 실측을 다시 판정한다\n`);
  for (const t of bad) console.log('  ' + t);
  console.log();
  for (const [kind, label] of expect) {
    const hit = bad.some((t) => t.includes(label) && t.includes(kind));
    console.log(`  ${hit ? '✅' : '🔴 안 울렸다'}  ${label} — ${kind}`);
    if (!hit) rc = 1;
  }
} finally {
  if (process.argv.includes('--keep')) {
    console.log(`\n⚠️ --keep: 원장에 가짜 행이 남아 있다. 되돌리려면: mv ${BAK} ${LEDGER}`);
  } else {
    fs.copyFileSync(BAK, LEDGER);
    fs.unlinkSync(BAK);
    const after = new Set(table(cur, readLedger()).alerts.filter((a) => a.lv === 'bad').map((a) => a.t));
    const extra = [...after].filter((t) => !baseline.has(t));
    const lost = [...baseline].filter((t) => !after.has(t));
    console.log(`\n── 복원 완료 (${fs.readFileSync(LEDGER, 'utf8').trim().split('\n').length}행)`);
    if (!extra.length && !lost.length) console.log('  ✅ 경보 집합이 드릴 전과 똑같다 — 원장이 온전히 복원됐다');
    else {
      for (const t of extra) console.log(`  🔴 드릴 뒤에 남은 경보: ${t}`);
      for (const t of lost) console.log(`  🔴 드릴 뒤에 사라진 경보: ${t}`);
      rc = 1;
    }
  }
}
process.exit(rc);
