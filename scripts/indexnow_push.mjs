#!/usr/bin/env node
/**
 * IndexNow 다중 사이트 푸시 — **바뀐 URL만** 참여 검색엔진에 통지한다.
 *
 * 🔴 왜 (2026-08-31):
 *   네이버 서치어드바이저 콘솔은 도구 제한으로 자동 조작이 안 된다(4회 확인).
 *   그런데 **네이버는 IndexNow 참여사**다 — 콘솔 없이 URL 을 밀 수 있다.
 *   (구글은 IndexNow 를 안 받는다. 구글은 sitemap lastmod + 색인 API 로 간다.)
 *
 *   8/30 에 6개 사이트 1,606장을 한 번 밀었는데 **그게 전부였다.**
 *   사이트마다 배포 방식이 달라(워커·Pages·Vercel·launchd) 각각 붙이면 또 갈라진다.
 *   → 하나로 묶고, apex 재빌드(매일 05:45)에 태운다.
 *
 * 🚫 매일 전량을 밀지 마라. IndexNow 는 "바뀐 것"을 알리는 규격이다.
 *    안 바뀐 1,600장을 매일 밀면 스팸이고, 무시당하기 시작하면 되돌리기 어렵다.
 *    → sitemap 의 lastmod 를 기억해 두고 **새 URL + lastmod 가 바뀐 URL만** 민다.
 *    lastmod 가 없는 사이트(heyreci·kontext)는 **새 URL만** 민다.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATE = path.join(__dirname, '..', 'data', 'indexnow_state.json');
const SHARED = 'd6e7f8cba7e39c9ddaf16baf456279a6';
const MAX_PER_RUN = 500;   // 예의 상한. 첫 실행이나 대량 변경 시 나눠 나간다.

const SITES = {
  'cue.the-moment.us': { map: '/sitemap.xml', key: SHARED },
  'the-moment.us': { map: '/sitemap.xml', key: SHARED },
  'mark.the-moment.us': { map: '/sitemap-index.xml', key: SHARED },
  'notes.the-moment.us': { map: '/sitemap.xml', key: SHARED },
  'heyreci.com': { map: '/sitemap.xml', key: SHARED },
  'kontext.the-moment.us': { map: '/sitemap.xml', key: SHARED },
};

const get = async (u) => (await fetch(u, { headers: { 'user-agent': 'momentus-indexnow/2' } })).text();

// url → lastmod('' 가능). 사이트맵 인덱스는 자식을 펼친다.
async function entries(host, map) {
  const walk = async (u) => {
    const xml = await get(u);
    if (/<sitemapindex/i.test(xml)) {
      const kids = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
      const out = [];
      for (const k of kids) out.push(...(await walk(k)));
      return out;
    }
    return [...xml.matchAll(/<url>([\s\S]*?)<\/url>/g)].map((m) => {
      const loc = (/<loc>([^<]+)<\/loc>/.exec(m[1]) || [])[1] || '';
      const lm = (/<lastmod>([^<]+)<\/lastmod>/.exec(m[1]) || [])[1] || '';
      return [loc, lm.slice(0, 10)];
    }).filter(([l]) => l);
  };
  const all = await walk(`https://${host}${map}`);
  return all.filter(([u]) => u.startsWith(`https://${host}/`) || u === `https://${host}`);
}

let state = {};
try { state = JSON.parse(fs.readFileSync(STATE, 'utf8')); } catch { /* 첫 실행 */ }

const only = process.argv.slice(2).filter((a) => !a.startsWith('-'));
const all = process.argv.includes('--all');   // 상태 무시하고 전량(첫 세팅·복구용)
const hosts = only.length ? only : Object.keys(SITES);
let grand = 0;

for (const host of hosts) {
  const cfg = SITES[host];
  if (!cfg) { console.log(`  ⏭  ${host} — 목록에 없다`); continue; }
  try {
    const kr = await fetch(`https://${host}/${cfg.key}.txt`);
    if (!kr.ok || (await kr.text()).trim() !== cfg.key) { console.log(`  🔴 ${host} — 키 파일 없음/불일치 (${kr.status})`); continue; }

    const list = await entries(host, cfg.map);
    const prev = state[host] || {};
    const now = {};
    const push = [];
    for (const [u, lm] of list) {
      now[u] = lm;
      if (all) { push.push(u); continue; }
      if (!(u in prev)) push.push(u);                          // 새 URL
      else if (lm && lm !== prev[u]) push.push(u);             // 내용이 바뀐 날짜
    }
    const gone = Object.keys(prev).filter((u) => !(u in now)).length;

    if (!push.length) {
      console.log(`  ✅ ${host.padEnd(24)} 변화 없음 (${list.length}장 유지${gone ? ` · ${gone}장 사라짐` : ''})`);
      state[host] = now;
      continue;
    }
    const send = push.slice(0, MAX_PER_RUN);
    const res = await fetch('https://www.bing.com/indexnow', {
      method: 'POST',
      headers: { 'content-type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ host, key: cfg.key, keyLocation: `https://${host}/${cfg.key}.txt`, urlList: send }),
    });
    const ok = res.status === 200 || res.status === 202;
    console.log(`  ${ok ? '✅' : '🔴'} ${host.padEnd(24)} ${String(send.length).padStart(4)}장 통지`
      + (push.length > send.length ? ` (남은 ${push.length - send.length}장은 다음 실행)` : '')
      + (ok ? '' : ` — HTTP ${res.status}`));
    if (ok) {
      grand += send.length;
      // 보낸 것만 상태에 반영한다 — 상한에 걸려 못 보낸 건 다음에 다시 잡히게.
      const sent = new Set(send);
      state[host] = { ...prev };
      for (const [u, lm] of Object.entries(now)) if (sent.has(u) || u in prev) state[host][u] = lm;
      for (const u of Object.keys(state[host])) if (!(u in now)) delete state[host][u];
    }
  } catch (e) {
    console.log(`  🔴 ${host} — ${String(e.message).slice(0, 60)}`);
  }
}
try {
  fs.mkdirSync(path.dirname(STATE), { recursive: true });
  fs.writeFileSync(STATE, JSON.stringify(state, null, 0));
} catch (e) { console.log('  🟠 상태 저장 실패: ' + e.message); }
console.log(`  ── 이번 실행 합계 ${grand}장`);
