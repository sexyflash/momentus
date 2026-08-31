#!/usr/bin/env node
/**
 * 무료 도구 계측 확인 — 가져감(tool_install) · 실행(tool_run) 을 도구별로 본다
 *
 * 창업자 지시(2026-08-30): "쿠팡 북마크릿도 하는데 왜 핀터레스트·유튜브·인스타는 왜 안해?"
 *
 * ★ 도구는 **이벤트 이름**으로 갈린다 — `<도구>_run` · `<도구>_install`
 *   (`quickpang_run`, `youtube_rank_install` …). 그래서 이 스크립트는 이름을 쪼개 집계한다.
 *
 * ★ 왜 매개변수가 아니라 이름인가 (2026-08-31 실측)
 *   `tool_run` + 매개변수 `tool` 로 갈랐더니 **실시간에서 도구를 못 봤다.**
 *   GA4 실시간 API 는 이벤트 범위 맞춤 측정기준을 아예 안 받는다
 *   (`customEvent:tool` → "not a valid dimension"). 표준 보고서를 몇 시간 기다려야 갈렸다.
 *   이름에 박으니 기본 화면에서 즉시 갈린다. 창업자: "그 툴이 뭐냐고."
 *   맞춤 측정기준 `도구`(tool)·`설치 방식`(method)도 등록돼 있다 — 표준 보고서의 교차 분석용.
 *
 * 사용법:
 *   node scripts/ga_tools_report.mjs            # 최근 28일
 *   node scripts/ga_tools_report.mjs --realtime # 최근 29분 (즉시 확인)
 */
import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'
import crypto from 'node:crypto'

const RT = process.argv.includes('--realtime')
const PROPERTY = process.env.GA_PROPERTY || '460766131'   // 무료 도구 (북마크릿)
const KEY = process.env.GINDEX_KEY_FILE
  || [path.join(os.homedir(), 'Projects/momentus/.gindex-sa.json'),
      path.join(os.homedir(), 'Projects/heyreci/.gindex-sa.json')].find(fs.existsSync)

const b64 = (b) => Buffer.from(b).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')

async function token() {
  const sa = JSON.parse(fs.readFileSync(KEY, 'utf8'))
  const now = Math.floor(Date.now() / 1000)
  const head = b64(JSON.stringify({ alg: 'RS256', typ: 'JWT' }))
  const claim = b64(JSON.stringify({
    iss: sa.client_email, scope: 'https://www.googleapis.com/auth/analytics.readonly',
    aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600,
  }))
  const sig = crypto.createSign('RSA-SHA256').update(`${head}.${claim}`).sign(sa.private_key)
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion: `${head}.${claim}.${b64(sig)}` }),
  })
  const j = await r.json()
  if (!j.access_token) throw new Error('토큰 실패')
  return j.access_token
}

async function main() {
  const H = { Authorization: `Bearer ${await token()}`, 'content-type': 'application/json' }
  const url = `https://analyticsdata.googleapis.com/v1beta/properties/${PROPERTY}:` +
    (RT ? 'runRealtimeReport' : 'runReport')
  const range = RT
    ? { minuteRanges: [{ startMinutesAgo: 29, endMinutesAgo: 0 }] }
    : { dateRanges: [{ startDate: '28daysAgo', endDate: 'today' }] }

  const ask = (body) => fetch(url, { method: 'POST', headers: H, body: JSON.stringify({ ...range, ...body }) }).then((r) => r.json())

  console.log(`=== 무료 도구 계측 · ${RT ? '최근 29분' : '최근 28일'} ===\n`)

  const ev = await ask({ dimensions: [{ name: 'eventName' }], metrics: [{ name: 'eventCount' }], limit: 50 })
  if (ev.error) throw new Error(ev.error.message)

  /*
    이벤트 이름 자체가 `<도구>_run` · `<도구>_install` 이다 (2026-08-31).
    GA4 실시간이 맞춤 측정기준을 안 받아서, 이름에 도구를 박아야 즉시 갈린다.
    그래서 여기서도 이름을 쪼개 도구별로 모은다 — 실시간·표준 둘 다 같은 방식으로 읽힌다.
  */
  const rows = (ev.rows || [])
    .map((r) => ({ name: r.dimensionValues[0].value, n: Number(r.metricValues[0].value) }))
    .filter((r) => /_(run|install)$/.test(r.name))
  const tools = {}
  for (const r of rows) {
    const m = /^(.+)_(run|install)$/.exec(r.name)
    const tool = m[1] === 'tool' ? '(옛 집계)' : m[1]
    tools[tool] = tools[tool] || { run: 0, install: 0 }
    tools[tool][m[2]] += r.n
  }
  console.log('[도구별]  가져감(install) → 실행(run)\n')
  const names = Object.keys(tools).sort()
  if (!names.length) console.log('  (아직 데이터 없음)')
  for (const t of names) {
    const { install, run } = tools[t]
    const rate = install ? ` · 전환 ${Math.round((run / install) * 100)}%` : ''
    console.log(`  ${t.padEnd(18)} 가져감 ${String(install).padStart(4)}   실행 ${String(run).padStart(4)}${rate}`)
  }
  return
}
main().catch((e) => { console.error('실패:', e.message); process.exit(1) })
