#!/usr/bin/env node
// 관측소 — **48시간 뒤 판정기.** 2026-09-14 BWT 설치 직후 심어둔 장치.
//
// ## 왜 있나
// BWT 는 "데이터 반영에 최대 48시간" 을 고지한다. 그래서 설치 당일 숫자는 전부 0이다.
// 이틀 뒤에 0을 보고 "GEO 안 되네" 라고 읽으면 **계정이 새것이라 0인지, 진짜 안 보여서 0인지**
// 구분을 못 한다. 그 구분을 사람 기억에 맡기지 않으려고 판정 규칙을 코드로 박아 둔다.
//
// ## 판정 원리 — 대조군(control)이 있다
// GA4 28일 실측에서 **빙에서 사람이 실제로 클릭해 들어온 사이트**가 있었다:
//   teamai 1 · 빈방 2 · 북마크릿(the-moment.us/tools/) 1   ← 빙 노출이 확실히 존재
//   cue 0                                                  ← 빙 리퍼러 없음
// 그리고 **AI 답변에서 클릭이 들어온 사이트**도 하나 있었다:
//   the-moment.us ← chatgpt.com 1건.  cue 0
// → 대조군에 숫자가 뜨는데 cue 가 0이면 **계기는 멀쩡하고 cue 가 진짜 안 보이는 것**이다.
// → 대조군도 0이면 계기(계정·파이프)를 의심한다.
//
// 사용법: node observatory/recheck.mjs      (2026-09-16 이후)
import fs from 'node:fs';
import path from 'node:path';

const KEYFILE = path.join(process.env.HOME, '.config/observatory/bing.json');
const BASE = 'https://ssl.bing.com/webmaster/api.svc/json/';
const BASELINE = path.join(path.dirname(new URL(import.meta.url).pathname), 'data/baseline-2026-09-14.json');

// 대조군 = 빙에서 실제 클릭이 있었던 사이트(검증됨). 처리군 = 우리가 궁금한 사이트.
const CONTROL = ['https://teamai.the-moment.us/', 'https://the-moment.us/'];
const TREATMENT = 'https://cue.the-moment.us/';

const key = JSON.parse(fs.readFileSync(KEYFILE, 'utf8')).apikey;
const get = async (ep, q = {}) => {
  const u = BASE + ep + '?apikey=' + key + Object.entries(q).map(([k, v]) => `&${k}=${v}`).join('');
  try { return await (await fetch(u)).json(); } catch (e) { return { error: String(e).slice(0, 80) }; }
};

const base = JSON.parse(fs.readFileSync(BASELINE, 'utf8'));
const sites = (await get('GetUserSites')).d || [];
const now = {};

console.log(`\n관측소 재판정 — 기준선 ${base.taken_at}\n`);
console.log('  사이트                                   검증  노출  클릭  질의  사이트맵');
for (const s of sites) {
  const url = s.Url;
  const rt = (await get('GetRankAndTrafficStats', { siteUrl: url })).d || [];
  const qs = (await get('GetQueryStats', { siteUrl: url })).d || [];
  const fd = (await get('GetFeeds', { siteUrl: url })).d || [];
  const imp = rt.reduce((a, r) => a + (r.Impressions || 0), 0);
  const clk = rt.reduce((a, r) => a + (r.Clicks || 0), 0);
  now[url] = { verified: !!s.IsVerified, imp, clk, q: qs.length, feeds: fd.length };
  const b = base.sites[url] || {};
  const d = (a, bb) => { const x = (a || 0) - (bb || 0); return x > 0 ? `+${x}` : String(x); };
  console.log(`  ${url.padEnd(40)} ${s.IsVerified ? '✅' : '🟡'}  ${String(imp).padStart(4)}(${d(imp, b.impressions_sum)}) ${String(clk).padStart(3)} ${String(qs.length).padStart(4)}  ${fd.length}`);
}

// ── 판정 ────────────────────────────────────────────────────────────
const ctlImp = CONTROL.reduce((a, u) => a + (now[u]?.imp || 0), 0);
const trtImp = now[TREATMENT]?.imp || 0;

console.log('\n── 판정 (규칙은 2026-09-14 에 미리 정했다. 결과를 보고 고치지 마라)\n');
if (ctlImp === 0 && trtImp === 0) {
  console.log('  🟡 대조군도 0 · cue 도 0');
  console.log('     → 계기(계정·데이터 파이프)를 의심한다. 아직 반영 안 됐거나 API 가 이 계정에');
  console.log('       데이터를 안 채우는 것이다. **"GEO 안 된다"고 결론내지 마라.**');
  console.log('     → 할 일: 하루 더 기다린다. 그래도 0이면 BWT UI 를 눈으로 확인(API 만의 문제일 수 있다).');
} else if (ctlImp > 0 && trtImp === 0) {
  console.log(`  🔴 대조군 노출 ${ctlImp} · cue 0`);
  console.log('     → **계기는 멀쩡하다. cue 가 빙에서 진짜 안 보이는 것이다.**');
  console.log('     → 할 일: cue 의 색인 자체를 의심한다. URL Inspection 으로 실제 색인 여부 확인 →');
  console.log('       색인은 됐는데 노출 0이면 "걸릴 검색어가 없는 것"(수요 문제) 이다.');
} else if (trtImp > 0) {
  console.log(`  🟢 cue 노출 ${trtImp} · 질의 ${now[TREATMENT]?.q || 0}건`);
  console.log('     → **빙에서 보이고 있다.** 이제 질의어를 봐라 — 어떤 말로 걸리는지가 다음 편성의 재료다.');
  console.log('     → 할 일: GetQueryStats 상위 질의어를 뽑아 콘텐츠 편성에 반영.');
}

// AI Performance 는 API 미확인 — 사람이 봐야 하는 자리
console.log('\n── 손으로 볼 것 (API 미확인)');
console.log('  AI Performance: https://www.bing.com/webmasters/aiperformance?siteUrl=https://cue.the-moment.us/');
console.log('    · the-moment.us 에 citation 이 뜨는데 cue 가 0 → cue 만 AI 에 안 잡히는 것');
console.log('    · 둘 다 0 → 이 계기가 Copilot 만 재고 ChatGPT 를 못 재는 것일 수 있다.');
console.log('      그때만 geo_probe.py 를 **1회** 돌려 교차 확인한다(상시 금지).');
console.log('\n── 같이 볼 것: node ~/Projects/cue/scripts/ga.mjs --source --days 7');
console.log('    기준선(9/14, 28일): cue AI 리퍼러 0 · the-moment.us chatgpt.com 1 · bing 리퍼러 팀AI 1·빈방 2·북마크릿 1\n');
