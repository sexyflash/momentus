#!/usr/bin/env node
/**
 * 빙 계기 — Bing Webmaster Tools API (무료).
 *
 * ── 왜 있나 (2026-09-14, docs/OBSERVATORY.md §지표 4)
 * **ChatGPT 웹검색·코파일럿이 타는 인덱스가 빙이다.** 구글은 cue 601장을 미색인으로 묶어놨는데
 * 빙에는 이미 들어가 있다(DuckDuckGo `site:` 실측). 구글을 GSC 로 보듯 빙을 봐야 하는데
 * 지금까지 보는 수단이 아예 없었다. 빙에서 안 보이면 ChatGPT 가 우리를 못 찾는다.
 *
 * ── 키 (2026-09-14 Cue 세션이 발급·등록 완료)
 * 정본 위치 **`~/.config/observatory/bing.json`** (chmod 600, 필드 `apikey`).
 * 🚫 저장소에 넣지 마라 — keyguard 가 커밋을 막는다. env `BING_API_KEY` 도 받는다.
 * 키가 없으면 이 모듈은 **조용히 죽지 않고** `{ unavailable: <사유> }` 를 돌려준다 —
 * 표에서 빙 칸이 "키 없음" 으로 보이고, 그게 곧 해야 할 일이다(🚫 0 으로 채워 지어내지 마라).
 *
 * ── 등록 현황 (2026-09-14)
 * GSC 임포트로 8개 사이트 `IsVerified: true`. notes.the-moment.us 만 미검증(개별 GSC 속성이
 * 아니었다 — DNS CNAME 이나 파일 배포가 필요한데 notes 저장소에 남의 미커밋 변경이 있어 보류).
 *
 * ── ⚠️ 지표 엔드포인트는 등록 직후 **빈 배열**이다
 * GetRankAndTrafficStats·GetQueryStats·GetCrawlStats 가 2026-09-14 현재 `{"d":[]}` 다.
 * BWT 가 "최대 48시간" 을 고지했다. **빈 배열은 0 이 아니라 '아직 모름'**이다 —
 * 그래서 이 모듈은 행이 하나도 없으면 0 이 아니라 `unavailable` 을 돌려준다.
 * 🚫 2026-09-16 전에 "빙은 안 된다"고 결론내지 마라.
 *
 * ── 🔴 AI Performance(BETA)는 **공개 API 가 없다** (2026-09-14 실측)
 * BWT UI 에 Total Citations·Avg. Cited Pages·Grounding Queries 가 있지만,
 * `api.svc/json` 에는 대응 메서드가 없다 — GetAIPerformanceStats·GetCitationStats·
 * GetGroundingQueries·GetCopilotStats 등 9종을 찔러 **전부 404**. UI 경로
 * `www.bing.com/webmasters/api/aiperformance` 는 쿠키 인증 SPA 껍데기(HTML)를 준다.
 * → 지금 붙일 수 있는 길은 ① UI 의 Download 버튼 ② 브라우저 자동화 둘뿐이다.
 *   `aiPerformance()` 는 그 사실을 담아 `unavailable` 을 돌려준다(지어내지 않는다).
 *
 * 쓰는 법
 *   node observatory/bing.mjs                      # 등록된 사이트 목록 + 키 상태
 *   node observatory/bing.mjs --site heyreci.com   # 한 사이트 지표
 *   node observatory/bing.mjs --json
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
// 🚫 저장소 안에 키를 두지 마라. 정본은 홈 밑이다.
const KEY_FILE = process.env.BING_KEY_FILE || path.join(process.env.HOME || '', '.config', 'observatory', 'bing.json');
const API = 'https://ssl.bing.com/webmaster/api.svc/json';

export function apiKey() {
  if (process.env.BING_API_KEY) return process.env.BING_API_KEY.trim();
  try {
    const raw = fs.readFileSync(KEY_FILE, 'utf8').trim();
    if (!raw) return null;
    if (raw.startsWith('{')) return (JSON.parse(raw).apikey || '').trim() || null;
    return raw;                                  // 한 줄짜리 키 파일도 받는다
  } catch { return null; }
}

export const NO_KEY = '빙 API 키 없음 — ~/.config/observatory/bing.json 의 apikey 를 확인해라 (bing.com/webmasters → 설정 → API 액세스)';
export const NO_DATA = 'BWT 데이터 아직 없음 — 사이트 등록 후 최대 48시간(2026-09-14 등록). 빈 배열은 0 이 아니라 모름이다';
export const NO_AI_API = 'AI Performance(BETA)는 공개 API 없음 — api.svc/json 메서드 9종 전부 404, UI 는 쿠키 인증 SPA. Download 버튼 또는 브라우저 자동화가 유일한 길 (2026-09-14 실측)';

async function call(method, params) {
  const key = apiKey();
  if (!key) return { err: NO_KEY };
  const qs = new URLSearchParams({ ...params, apikey: key });
  try {
    const r = await fetch(`${API}/${method}?${qs}`, { headers: { 'user-agent': 'momentus-observatory/1.0' } });
    const txt = await r.text();
    if (!r.ok) return { err: `${method} ${r.status}: ${txt.slice(0, 200)}` };
    // BWT 는 성공 응답도 { "d": ... } 로 감싼다.
    try { return { d: JSON.parse(txt).d }; } catch { return { err: `${method} 응답 파싱 실패: ${txt.slice(0, 200)}` }; }
  } catch (e) {
    return { err: `${method} 호출 실패: ${String(e.message).slice(0, 200)}` };
  }
}

/** BWT 날짜는 `/Date(1757808000000)/` 형태다. 못 읽으면 null — 🚫 오늘로 때우지 마라. */
const bingDate = (v) => {
  const m = /\/Date\((\d+)/.exec(String(v || ''));
  return m ? new Date(Number(m[1])).toISOString().slice(0, 10) : null;
};

/** 등록된 사이트 목록. 키 상태를 보는 가장 싼 호출이다. */
export async function userSites() {
  const { d, err } = await call('GetUserSites', {});
  if (err) return { err };
  return { sites: (d || []).map((s) => String(s.Url || '').replace(/^https?:\/\//, '').replace(/\/$/, '')) };
}

/**
 * 한 사이트의 빙 지표. 반환은 **항상 같은 모양**이다 —
 * 값을 못 구했으면 null 로 두고 `unavailable` 에 사유를 담는다(모름을 0 으로 바꾸지 않는다).
 */
export async function siteStats(domain, days = 7) {
  const out = { domain, days, inIndex: null, crawled: null, impressions: null, clicks: null, topQueries: [], unavailable: null };
  const key = apiKey();
  if (!key) { out.unavailable = NO_KEY; return out; }
  const siteUrl = `https://${domain}`;
  const cutoff = new Date(Date.now() - days * 86400000).toISOString().slice(0, 10);

  const traffic = await call('GetRankAndTrafficStats', { siteUrl });
  if (traffic.err) { out.unavailable = traffic.err; return out; }
  const all = (traffic.d || []).map((r) => ({ day: bingDate(r.Date), imp: Number(r.Impressions || 0), clk: Number(r.Clicks || 0) }))
    .filter((r) => r.day);
  // ⚠️ **행이 하나도 없는 것**과 **그 창에 0 인 것**은 다르다. 앞은 모름, 뒤는 0.
  //    둘을 한 갈래로 묶으면 원장이 거짓말을 하고, 에러가 안 나서 아무도 모른다(룰 #13).
  if (!all.length) { out.unavailable = NO_DATA; return out; }
  const rows = all.filter((r) => r.day >= cutoff);
  out.impressions = rows.reduce((a, r) => a + r.imp, 0);
  out.clicks = rows.reduce((a, r) => a + r.clk, 0);

  const crawl = await call('GetCrawlStats', { siteUrl });
  if (!crawl.err) {
    const cr = (crawl.d || []).map((r) => ({ day: bingDate(r.Date), idx: Number(r.InIndex || 0), cw: Number(r.CrawledPages || 0) }))
      .filter((r) => r.day).sort((a, b) => a.day.localeCompare(b.day));
    const recent = cr.filter((r) => r.day >= cutoff);
    // 색인 수는 **누적 스냅샷**이라 합치면 안 된다 — 가장 최근 값을 쓴다.
    out.inIndex = cr.length ? cr[cr.length - 1].idx : null;
    out.crawled = recent.reduce((a, r) => a + r.cw, 0);
  }

  const q = await call('GetQueryStats', { siteUrl });
  if (!q.err) {
    out.topQueries = (q.d || [])
      .map((r) => ({ q: r.Query, imp: Number(r.Impressions || 0), clk: Number(r.Clicks || 0) }))
      .sort((a, b) => b.imp - a.imp).slice(0, 5);
  }
  return out;
}

/**
 * AI 인용 성적표(Total Citations · Grounding Queries). **지금은 못 가져온다** —
 * 공개 API 가 없다는 사실 자체를 값으로 돌려준다. 엔드포인트가 열리면 여기만 고치면 된다.
 */
export async function aiPerformance(domain) {
  return { domain, citations: null, citedPages: null, groundingQueries: [], unavailable: NO_AI_API };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const site = args.includes('--site') ? args[args.indexOf('--site') + 1] : null;
  const asJson = args.includes('--json');
  const res = site ? await siteStats(site) : await userSites();
  if (asJson) { console.log(JSON.stringify(res, null, 2)); }
  else if (res.err || res.unavailable) { console.log('🔴 ' + (res.err || res.unavailable)); }
  else if (site) {
    console.log(`\n── 빙: ${site}`);
    console.log(`  색인 ${res.inIndex ?? '—'}장 · 최근 ${res.days}일 크롤 ${res.crawled ?? '—'}장`);
    console.log(`  노출 ${res.impressions ?? '—'} · 클릭 ${res.clicks ?? '—'}`);
    for (const t of res.topQueries) console.log(`    ${String(t.imp).padStart(5)} 노출 · ${String(t.clk).padStart(3)} 클릭  ${t.q}`);
    console.log();
  } else {
    console.log(`\n── 빙에 등록된 사이트 ${res.sites.length}개`);
    for (const s of res.sites) console.log(`  ${s}`);
    console.log();
  }
}
