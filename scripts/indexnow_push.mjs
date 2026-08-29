#!/usr/bin/env node
/**
 * IndexNow 다중 사이트 푸시 — sitemap 전량을 참여 검색엔진에 통지한다.
 *
 * 🔴 왜 필요한가 (2026-08-29):
 *   네이버 서치어드바이저 콘솔은 도구 제한으로 자동 조작이 안 된다(4회 확인, ❌ 기록).
 *   그런데 **네이버는 IndexNow 참여사**다 — 콘솔 없이도 URL 을 밀 수 있다.
 *   구글은 IndexNow 를 안 받는다(2026-02 기준). 구글은 sitemap lastmod + 색인 API 로 간다.
 *
 * 키는 비밀이 아니다 — 규격상 `https://<host>/<key>.txt` 로 공개 서빙해야 검증된다.
 * 🚫 키 파일이 없는 호스트에 밀지 마라. 403 이 나고 그 호스트가 한동안 무시된다.
 *
 * 사용법: node scripts/indexnow_push.mjs [host ...]   (생략 시 전체)
 */
const KEY = process.env.INDEXNOW_KEY || 'd6e7f8cba7e39c9ddaf16baf456279a6';
const SITES = {
  'cue.the-moment.us': '/sitemap.xml',
  'the-moment.us': '/sitemap.xml',
  'mark.the-moment.us': '/sitemap-index.xml',
  'notes.the-moment.us': '/sitemap.xml',
  'heyreci.com': '/sitemap.xml',
  'kontext.the-moment.us': '/sitemap.xml',
};

const get = async (u) => (await fetch(u, { headers: { 'user-agent': 'momentus-indexnow/1' } })).text();

async function urlsOf(host, path) {
  const xml = await get(`https://${host}${path}`);
  let locs = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  // 사이트맵 인덱스면 자식을 펼친다 — 안 펼치면 URL 이 아니라 사이트맵 주소를 밀게 된다.
  if (/<sitemapindex/i.test(xml)) {
    const kids = locs;
    locs = [];
    for (const k of kids) {
      const cx = await get(k);
      locs.push(...[...cx.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]));
    }
  }
  return [...new Set(locs)].filter((u) => u.startsWith(`https://${host}/`) || u === `https://${host}`);
}

const targets = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(SITES);
for (const host of targets) {
  const path = SITES[host];
  if (!path) { console.log(`  ⏭  ${host} — 목록에 없다`); continue; }
  try {
    // 키 파일이 실제로 서빙되는지 먼저 본다. 없으면 밀지 않는다.
    const kr = await fetch(`https://${host}/${KEY}.txt`);
    if (!kr.ok || (await kr.text()).trim() !== KEY) { console.log(`  🔴 ${host} — 키 파일 없음/불일치 (${kr.status})`); continue; }
    const urls = await urlsOf(host, path);
    if (!urls.length) { console.log(`  🟠 ${host} — URL 0개`); continue; }
    let ok = true;
    for (let i = 0; i < urls.length; i += 10000) {
      const res = await fetch('https://www.bing.com/indexnow', {
        method: 'POST',
        headers: { 'content-type': 'application/json; charset=utf-8' },
        body: JSON.stringify({ host, key: KEY, keyLocation: `https://${host}/${KEY}.txt`, urlList: urls.slice(i, i + 10000) }),
      });
      if (!(res.status === 200 || res.status === 202)) { ok = false; console.log(`     ↳ HTTP ${res.status}`); }
    }
    console.log(`  ${ok ? '✅' : '🔴'} ${host.padEnd(24)} ${String(urls.length).padStart(4)}건 통지`);
  } catch (e) {
    console.log(`  🔴 ${host} — ${String(e.message).slice(0, 60)}`);
  }
}
