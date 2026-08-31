#!/usr/bin/env node
/**
 * 무료 도구 계측 확인 — 가져감(tool_install) · 실행(tool_run) 을 도구별로 본다
 *
 * 창업자 지시(2026-08-30): "쿠팡 북마크릿도 하는데 왜 핀터레스트·유튜브·인스타는 왜 안해?"
 *
 * ★ 맞춤 측정기준(2026-08-31 등록 완료)
 *   `도구`=tool · `설치 방식`=method, 둘 다 이벤트 범위. 이게 있어야 도구별로 쪼개진다.
 *   ⚠️ 등록 이전 데이터는 **소급 적용되지 않는다.**
 *
 * ★ 실시간 API 는 이벤트 범위 맞춤 측정기준을 **지원하지 않는다** (실측 확인).
 *   `customEvent:tool` 을 실시간에 넣으면 "not a valid dimension" 으로 죽는다 —
 *   미등록이 아니라 **API 제약**이다. 등록 여부는 metadata 로 확인해야 한다.
 *   그래서 --realtime 은 이벤트 합계만 보여주고, 도구별 내역은 표준 보고서로 본다.
 *   표준 보고서는 수집 후 반영까지 몇 시간 걸릴 수 있다.
 *
 * 사용법:
 *   node scripts/ga_tools_report.mjs            # 최근 28일 (도구별 포함)
 *   node scripts/ga_tools_report.mjs --realtime # 최근 29분 (이벤트 합계만)
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

  const ev = await ask({ dimensions: [{ name: 'eventName' }], metrics: [{ name: 'eventCount' }], limit: 20 })
  if (ev.error) throw new Error(ev.error.message)
  const want = ['tool_install', 'tool_run']
  console.log('[이벤트]')
  for (const n of want) {
    const row = (ev.rows || []).find((r) => r.dimensionValues[0].value === n)
    console.log(`  ${n.padEnd(14)} ${row ? row.metricValues[0].value : 0}`)
  }

  console.log('\n[도구별]')
  if (RT) {
    console.log('  (실시간 API 는 이벤트 범위 맞춤 측정기준을 지원하지 않는다 —')
    console.log('   도구별 내역은 --realtime 없이 표준 보고서로 봐라)')
    return
  }
  const byTool = await ask({
    dimensions: [{ name: 'customEvent:tool' }, { name: 'eventName' }],
    metrics: [{ name: 'eventCount' }], limit: 30,
  })
  if (byTool.error) {
    // 등록 여부는 metadata 가 진실이다 — 조회 실패만 보고 "미등록" 이라 단정하지 마라.
    console.log(`  ✗ 조회 실패 — ${byTool.error.message.slice(0, 90)}`)
    console.log('    등록 확인: properties/<id>/metadata 에 customEvent:tool 이 있는지 본다.')
    return
  }
  const rows = (byTool.rows || []).filter((r) => want.includes(r.dimensionValues[1].value))
  if (!rows.length) { console.log('  (아직 데이터 없음)'); return }
  for (const r of rows) {
    console.log(`  ${String(r.dimensionValues[0].value).padEnd(18)} ${r.dimensionValues[1].value.padEnd(14)} ${r.metricValues[0].value}`)
  }
}
main().catch((e) => { console.error('실패:', e.message); process.exit(1) })
