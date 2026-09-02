#!/usr/bin/env python3
"""geo_probe — "이런 거 하고 싶은데 뭐 쓰지?"에 우리 제품이 후보로 뽑히는지 재는 자.

왜 (2026-09-02 대표): "각 서비스가, 원하는 사람이 뭔가 하려고 할 때 추천이 되고 싶어."
  기록은 목적이 아니라 **할 일 생성기**다. 결과 한 줄에서 세 목록이 나온다 —
  인용 출처 = 우리가 실려야 할 자리 / 추천 기준 = 우리 페이지에 있어야 할 문장 /
  질문 표현 = 우리가 써야 할 글 제목.

무엇이 결정론이고 무엇이 LLM인가 (slack-bot CLAUDE.md 룰 #1)
  결정론: 질문 던지기, 응답·인용 URL 저장, 별칭 substring 원신호, 도메인 집계, 주간 diff.
  LLM   : "추천됐나 / 몇 번째냐 / 어떤 기준으로 골랐나 / 우리 설명이 맞나" — 자연어 의미.
          코드는 LLM 판정값을 원문 id 와 대조해 *있는 항목만* 받는다(지어낸 항목 폐기).

엔진
  claude    : `claude -p --allowedTools WebSearch WebFetch` (구독 자원. 질문당 60~120초)
  chatgpt   : OpenAI Responses API + web_search (OPENAI_API_KEY. 질문당 몇 원)
  naver_web : search.naver.com 웹 탭 1페이지 외부 링크 (HTML. API 는 앱 scope 없음 → 401)
  naver_blog: 같은 페이지의 블로그 탭

재개 가능 (룰 #12): 회차 파일은 (q_id, engine) 키로 쌓이고, 다시 돌리면 빈 칸만 채운다.
  죽은 회차가 남긴 파일을 "끝난 것"으로 오인하지 않게 `complete` 플래그를 따로 둔다.

사용
  python3 scripts/geo_probe.py run    [--engines claude,chatgpt,naver_web,naver_blog] [--products heyreci,cue] [--limit N]
  python3 scripts/geo_probe.py judge  [--date YYYY-MM-DD]
  python3 scripts/geo_probe.py report [--date YYYY-MM-DD] [--slack]      # 표준출력
  python3 scripts/geo_probe.py weekly [--engines ...]                      # run→judge→report→원장
"""
from __future__ import annotations

import argparse
import html as _html
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, OrderedDict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
GEO_DIR = ROOT / "docs" / "geo"
RUNS_DIR = GEO_DIR / "runs"
QUESTIONS = GEO_DIR / "questions.json"
LEDGER = GEO_DIR / "GEO_LEDGER.md"
SOURCES = GEO_DIR / "sources.json"
STATUS = GEO_DIR / "status.json"

KST = timezone(timedelta(hours=9))
ENGINES = ("claude", "chatgpt", "naver_web", "naver_blog")
LLM_ENGINES = ("claude", "chatgpt")
OUR_DOMAINS = ("the-moment.us", "heyreci.com")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

CLAUDE_PROBE_TIMEOUT = 300
CLAUDE_JUDGE_TIMEOUT = 240
OPENAI_TIMEOUT = 150
NAVER_TIMEOUT = 40
PAUSE_BETWEEN = 2.0          # 엔진 한도 보호 — 직렬 + 간격
JUDGE_MODEL = "sonnet"
JUDGE_SYSTEM = ("너는 채점·집계 전용 판정기다. 입력으로 받은 자료를 읽고 요청된 JSON 한 덩어리만 출력한다. "
                "설명·인사·되묻기 없이 JSON 만. 자료에 없는 것은 지어내지 않는다.")


def _neutral_cwd() -> str:
    """claude -p 를 *이 저장소 밖*에서 돌린다. momentus 의 CLAUDE.md·훅·메모리가 답변에 섞이면
    '우리 제품이 추천됐다'는 측정이 오염된다(자기 자료를 읽고 자기를 추천하는 꼴)."""
    import tempfile
    d = Path(tempfile.gettempdir()) / "geo_probe_neutral"
    d.mkdir(parents=True, exist_ok=True)
    return str(d)


def log(msg: str) -> None:
    print(f"[geo {datetime.now(KST).strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


# ── 환경 ─────────────────────────────────────────────────────────────────

def _load_env_fallback() -> None:
    """slack-bot/.env 의 키를 빌린다 (이 저장소엔 비밀이 없다). 이미 있으면 안 건드린다."""
    if os.environ.get("OPENAI_API_KEY"):
        return
    for cand in (Path.home() / "slack-bot" / ".env",):
        if not cand.exists():
            continue
        for line in cand.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and v and k not in os.environ:
                os.environ[k] = v


def load_questions() -> dict:
    return json.loads(QUESTIONS.read_text(encoding="utf-8"))


def flat_questions(cfg: dict, products: Optional[List[str]] = None) -> List[dict]:
    out = []
    for p in cfg["products"]:
        if products and p["key"] not in products:
            continue
        for q in p["questions"]:
            out.append({"id": q["id"], "q": q["q"], "product": p["key"],
                        "brands": p["brands"], "domains": p["domains"]})
    return out


# ── 회차 파일 ─────────────────────────────────────────────────────────────

def run_path(date: str) -> Path:
    return RUNS_DIR / f"{date}.json"


def today() -> str:
    return datetime.now(KST).strftime("%Y-%m-%d")


def load_run(date: str) -> dict:
    p = run_path(date)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"date": date, "complete": False, "entries": {}, "judged": False, "actions": None}


def save_run(run: dict) -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = run_path(run["date"]).with_suffix(".json.tmp")
    tmp.write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(run_path(run["date"]))


def previous_run_date(date: str) -> Optional[str]:
    if not RUNS_DIR.exists():
        return None
    dates = sorted(p.stem for p in RUNS_DIR.glob("*.json") if p.stem < date)
    for d in reversed(dates):
        try:
            if load_run(d).get("judged"):
                return d
        except Exception:
            continue
    return None


def entry_key(q_id: str, engine: str) -> str:
    return f"{q_id}|{engine}"


# ── 결정론 원신호 ─────────────────────────────────────────────────────────

def brand_hit(text: str, brands: List[str]) -> bool:
    t = (text or "").lower()
    return any(b.lower() in t for b in brands)


def domain_of(url: str) -> str:
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
    except Exception:
        return ""
    return host[4:] if host.startswith("www.") else host


def is_ours(url: str) -> bool:
    d = domain_of(url)
    return any(d == od or d.endswith("." + od) for od in OUR_DOMAINS)


# ── 엔진: claude ──────────────────────────────────────────────────────────

_URL_RE = re.compile(r"https?://[^\s)\]>\"'）]+")


def probe_claude(question: str) -> dict:
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)            # 중첩 세션 차단 해제
    cmd = ["claude", "-p", question, "--allowedTools", "WebSearch", "WebFetch",
           "--output-format", "json", "--no-session-persistence"]
    t0 = time.time()
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=CLAUDE_PROBE_TIMEOUT,
                            env=env, cwd=_neutral_cwd())
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout {CLAUDE_PROBE_TIMEOUT}s", "elapsed": time.time() - t0}
    if cp.returncode != 0:
        return {"ok": False, "error": (cp.stderr or cp.stdout or "")[-400:], "elapsed": time.time() - t0}
    try:
        d = json.loads(cp.stdout)
        text = d.get("result") or ""
        meta = {"turns": d.get("num_turns"), "cost_nominal": d.get("total_cost_usd")}
    except Exception:
        text, meta = cp.stdout, {}
    urls = list(OrderedDict.fromkeys(u.rstrip(".,") for u in _URL_RE.findall(text)))
    return {"ok": bool(text.strip()), "text": text, "citations": urls, "meta": meta,
            "elapsed": round(time.time() - t0, 1)}


# ── 엔진: chatgpt (OpenAI Responses + web_search) ─────────────────────────

def probe_chatgpt(question: str, model: str = "gpt-5-mini") -> dict:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return {"ok": False, "error": "OPENAI_API_KEY 없음"}
    body = {"model": model, "tools": [{"type": "web_search"}], "input": question}
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=OPENAI_TIMEOUT))
    except Exception as e:  # noqa: BLE001
        detail = ""
        try:
            detail = e.read().decode("utf-8", "ignore")[:300]  # type: ignore[attr-defined]
        except Exception:
            pass
        return {"ok": False, "error": f"{e} {detail}", "elapsed": time.time() - t0}
    texts, cites = [], []
    for it in r.get("output", []) or []:
        for c in it.get("content", []) or []:
            if c.get("type") == "output_text":
                texts.append(c.get("text") or "")
                for a in c.get("annotations", []) or []:
                    if a.get("type") == "url_citation" and a.get("url"):
                        cites.append(a["url"])
    text = "\n".join(texts)
    urls = list(OrderedDict.fromkeys(cites + [u.rstrip(".,") for u in _URL_RE.findall(text)]))
    usage = r.get("usage") or {}
    return {"ok": bool(text.strip()), "text": text, "citations": urls,
            "meta": {"model": model, "tokens": usage.get("total_tokens")},
            "elapsed": round(time.time() - t0, 1)}


# ── 엔진: naver (HTML) ────────────────────────────────────────────────────

_NAVER_SKIP = ("naver.com", "naver.me", "navercorp.com")
_A_RE = re.compile(r'<a\s+([^>]*?)href="(https?://[^"]+)"([^>]*)>(.*?)</a>', re.S)


def _naver_html(query: str, where: str) -> str:
    url = (f"https://search.naver.com/search.naver?where={where}&sm=tab_jum&query="
           + urllib.parse.quote(query))
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ko-KR,ko;q=0.9"})
    return urllib.request.urlopen(req, timeout=NAVER_TIMEOUT).read().decode("utf-8", "ignore")


def parse_naver_links(html_text: str, where: str, cap: int = 15) -> List[dict]:
    """검색 결과 페이지에서 결과 링크를 문서 순서대로 뽑는다(광고·네이버 내부 링크 제외).

    web  : 외부 도메인 링크(naver.com 계열 제외).
    blog : blog.naver.com/<id>/<post> 형태만.
    형식 파싱이라 자연어 판단이 아니다(룰 #1 무관). 못 잡으면 빈 목록 — 판정을 막지 않는다.
    """
    out: List[dict] = []
    seen = set()
    for m in _A_RE.finditer(html_text):
        href = _html.unescape(m.group(2))
        cls = (re.search(r'class="([^"]*)"', m.group(1) + m.group(3)) or [None, ""])[1] or ""
        if "ader.naver.com" in href or "ad.search.naver.com" in href or "tab" == cls.strip():
            continue
        d = domain_of(href)
        if where == "blog":
            if not re.match(r"^https?://(m\.)?blog\.naver\.com/[^/?#]+/\d+", href):
                continue
        else:
            if any(d == s or d.endswith("." + s) for s in _NAVER_SKIP):
                continue
            if any(x in cls for x in ("btn_", "favicon", "thumb", "lnk_thumb")):
                continue
        key = href.split("?utm")[0]
        if key in seen:
            continue
        seen.add(key)
        title = re.sub(r"<[^>]+>", "", _html.unescape(m.group(4))).strip()
        out.append({"url": href, "title": title[:120], "domain": d})
        if len(out) >= cap:
            break
    return out


def probe_naver(question: str, where: str) -> dict:
    t0 = time.time()
    try:
        page = _naver_html(question, where)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e), "elapsed": time.time() - t0}
    links = parse_naver_links(page, where)
    return {"ok": True, "text": "\n".join(f"{i+1}. {l['title']} — {l['url']}" for i, l in enumerate(links)),
            "citations": [l["url"] for l in links], "links": links,
            "elapsed": round(time.time() - t0, 1)}


PROBES = {
    "claude": lambda q: probe_claude(q),
    "chatgpt": lambda q: probe_chatgpt(q),
    "naver_web": lambda q: probe_naver(q, "web"),
    "naver_blog": lambda q: probe_naver(q, "blog"),
}


# ── run ───────────────────────────────────────────────────────────────────

def cmd_run(date: str, engines: List[str], products: Optional[List[str]], limit: Optional[int],
            retry_failed: bool = True) -> dict:
    _load_env_fallback()
    cfg = load_questions()
    qs = flat_questions(cfg, products)
    if limit:
        qs = qs[:limit]
    run = load_run(date)
    run["complete"] = False
    _write_status({"phase": "run", "date": date, "started": _now_iso(), "finished": None})
    save_run(run)
    todo = []
    for q in qs:
        for e in engines:
            ent = run["entries"].get(entry_key(q["id"], e))
            if ent and ent.get("ok"):
                continue
            if ent and not retry_failed:
                continue
            todo.append((q, e))
    log(f"run {date}: {len(todo)} 칸 채움 (전체 {len(qs)}문항 × {len(engines)}엔진)")
    for i, (q, e) in enumerate(todo, 1):
        log(f"  [{i}/{len(todo)}] {e} ← {q['id']}")
        res = PROBES[e](q["q"])
        res.update({"q_id": q["id"], "engine": e, "product": q["product"], "question": q["q"],
                    "at": _now_iso()})
        if res.get("ok"):
            res["brand_hit"] = brand_hit(res.get("text", ""), q["brands"])
            res["ours_cited"] = [u for u in res.get("citations", []) if is_ours(u)]
        run["entries"][entry_key(q["id"], e)] = res
        save_run(run)
        time.sleep(PAUSE_BETWEEN)
    expected = {entry_key(q["id"], e) for q in qs for e in engines}
    done = {k for k, v in run["entries"].items() if v.get("ok")}
    run["complete"] = expected <= done
    run["engines"] = sorted(set(run.get("engines", [])) | set(engines))
    save_run(run)
    _write_status({"phase": "run", "date": date, "finished": _now_iso(), "complete": run["complete"],
                   "failed": sorted(expected - done)})
    log(f"run {date}: complete={run['complete']} 실패 {len(expected - done)}")
    return run


def _now_iso() -> str:
    return datetime.now(KST).isoformat(timespec="seconds")


def _write_status(d: dict) -> None:
    GEO_DIR.mkdir(parents=True, exist_ok=True)
    cur = {}
    if STATUS.exists():
        try:
            cur = json.loads(STATUS.read_text(encoding="utf-8"))
        except Exception:
            cur = {}
    cur.update(d)
    STATUS.write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding="utf-8")


# ── judge (LLM) ───────────────────────────────────────────────────────────

def _claude_json(prompt: str, timeout: int = CLAUDE_JUDGE_TIMEOUT, model: str = JUDGE_MODEL) -> Optional[Any]:
    """판정용 claude -p — 도구 0, JSON 만. 실패는 None (fail-open: 판정 없음으로 표시)."""
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)
    cmd = ["claude", "-p", "--output-format", "json", "--model", model,
           "--system-prompt", JUDGE_SYSTEM,
           "--disallowedTools", "Bash", "Edit", "Write", "WebSearch", "WebFetch", "Agent",
           "--no-session-persistence"]
    try:
        cp = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout,
                            env=env, cwd=_neutral_cwd())
    except subprocess.TimeoutExpired:
        log(f"judge timeout {timeout}s")
        return None
    if cp.returncode != 0:
        log(f"judge rc={cp.returncode}: {(cp.stderr or '')[-300:]}")
        return None
    try:
        body = json.loads(cp.stdout).get("result") or ""
    except Exception:
        body = cp.stdout
    parsed = extract_json(body)
    if parsed is None:
        log(f"judge: JSON 추출 실패 — stdout[:300]={cp.stdout[:300]!r} stderr[:200]={(cp.stderr or '')[:200]!r}")
    return parsed


def extract_json(body: str) -> Optional[Any]:
    """응답 본문에서 첫 JSON 객체/배열을 꺼낸다 (```json 펜스 포함)."""
    if not body:
        return None
    m = re.search(r"```(?:json)?\s*([\[{].*?[\]}])\s*```", body, re.S)
    cand = m.group(1) if m else None
    if cand is None:
        s = body.find("{")
        a = body.find("[")
        starts = [x for x in (s, a) if x >= 0]
        if not starts:
            return None
        cand = body[min(starts):]
    for end in range(len(cand), 0, -1):
        try:
            return json.loads(cand[:end])
        except Exception:
            continue
    return None


JUDGE_SCHEMA = (
    '{"judgments":[{"key":"<q_id>|<engine>","mentioned":true|false,"recommended":true|false,'
    '"rank":<int|null>,"competitors":["<서비스명>",...],"criteria":["<추천 기준 한 구절>",...],'
    '"our_description":"correct|wrong|absent","quote":"<우리를 언급한 원문 한 문장 또는 빈 문자열>"}]}'
)


def build_judge_prompt(product: dict, entries: List[dict]) -> str:
    L = [
        "너는 AI 검색 답변을 채점하는 판정기다. 아래는 손님이 AI에게 던진 질문과 그 답변이다.",
        f"우리 제품: {product['name']} ({product['url']}). 별칭: {', '.join(product['brands'])}.",
        "",
        "각 답변마다 판정하라:",
        "- mentioned: 우리 제품이 답변에 등장하는가 (별칭·도메인 포함)",
        "- recommended: 손님에게 '써볼 만한 후보'로 제시됐는가 (부정적·주의 언급이면 false)",
        "- rank: 후보 목록 중 몇 번째인가 (없으면 null)",
        "- competitors: 답변이 후보로 제시한 다른 서비스 이름 전부 (원문 표기 그대로)",
        "- criteria: 답변이 후보를 고르거나 설명할 때 쓴 기준 구절 (예: '무료 체험', '한국어 지원', '촬영 없이')",
        "- our_description: 우리 설명이 맞으면 correct, 틀리면 wrong, 언급 없으면 absent",
        "- quote: 우리를 언급한 원문 한 문장 (없으면 빈 문자열). 지어내지 마라.",
        "",
        "🚫 답변에 없는 서비스·기준을 지어내지 마라. 원문에 있는 것만 적어라.",
        "JSON 한 덩어리로만 답하라. 형식:",
        JUDGE_SCHEMA,
        "",
    ]
    for e in entries:
        L.append(f"━━━ key: {entry_key(e['q_id'], e['engine'])} ━━━")
        L.append(f"[질문] {e['question']}")
        L.append(f"[엔진] {e['engine']}")
        L.append("[답변]")
        L.append((e.get("text") or "")[:6000])
        if e.get("citations"):
            L.append("[인용 URL] " + " · ".join(e["citations"][:15]))
        L.append("")
    return "\n".join(L)


def merge_judgments(run: dict, parsed: Any, allowed_keys: set) -> int:
    """LLM 판정을 회차에 합친다. 원문에 없는 key 는 버린다(지어낸 항목 차단). 반환: 반영 건수."""
    if not isinstance(parsed, dict):
        return 0
    items = parsed.get("judgments")
    if not isinstance(items, list):
        return 0
    n = 0
    for j in items:
        if not isinstance(j, dict):
            continue
        k = j.get("key")
        if k not in allowed_keys or k not in run["entries"]:
            continue
        ent = run["entries"][k]
        ent["judgment"] = {
            "mentioned": bool(j.get("mentioned")),
            "recommended": bool(j.get("recommended")),
            "rank": j.get("rank") if isinstance(j.get("rank"), int) else None,
            "competitors": [str(x)[:60] for x in (j.get("competitors") or []) if x][:15],
            "criteria": [str(x)[:80] for x in (j.get("criteria") or []) if x][:12],
            "our_description": j.get("our_description") if j.get("our_description") in ("correct", "wrong", "absent") else "absent",
            "quote": str(j.get("quote") or "")[:300],
        }
        n += 1
    return n


def cmd_judge(date: str) -> dict:
    run = load_run(date)
    cfg = load_questions()
    by_product: Dict[str, List[dict]] = {}
    for k, ent in run["entries"].items():
        if not ent.get("ok") or ent.get("engine") not in LLM_ENGINES or ent.get("judgment"):
            continue
        by_product.setdefault(ent["product"], []).append(ent)
    prods = {p["key"]: p for p in cfg["products"]}
    _write_status({"phase": "judge", "date": date, "judge_started": _now_iso()})
    for pkey, ents in by_product.items():
        p = prods.get(pkey)
        if not p:
            continue
        for i in range(0, len(ents), 6):          # 프롬프트 예산 — 6답변씩
            chunk = ents[i:i + 6]
            keys = {entry_key(e["q_id"], e["engine"]) for e in chunk}
            log(f"judge {pkey}: {len(chunk)}건")
            parsed = _claude_json(build_judge_prompt(p, chunk))
            n = merge_judgments(run, parsed, keys)
            if n < len(chunk):
                log(f"  ⚠️ {pkey}: {len(chunk) - n}건 판정 누락 (미판정으로 남김)")
            save_run(run)
    # naver 는 LLM 판정 없이 결정론(우리 도메인 등장 여부)만
    for k, ent in run["entries"].items():
        if ent.get("ok") and ent.get("engine") in ("naver_web", "naver_blog") and not ent.get("judgment"):
            ours = [u for u in ent.get("citations", []) if is_ours(u)]
            rank = None
            for i, u in enumerate(ent.get("citations", []), 1):
                if is_ours(u):
                    rank = i
                    break
            ent["judgment"] = {"mentioned": bool(ours), "recommended": bool(ours), "rank": rank,
                               "competitors": [], "criteria": [], "our_description": "absent",
                               "quote": "", "deterministic": True}
    run["judged"] = True
    save_run(run)
    return run


# ── 집계 (결정론) ─────────────────────────────────────────────────────────

def summarize(run: dict, cfg: dict) -> dict:
    prods = {p["key"]: p for p in cfg["products"]}
    engines = run.get("engines") or sorted({e.get("engine") for e in run["entries"].values() if e.get("engine")})
    per: Dict[str, dict] = {}
    cited_domains: Counter = Counter()
    competitors: Dict[str, Counter] = {}
    criteria: Dict[str, Counter] = {}
    wrong_desc: List[str] = []
    unjudged = 0
    for k, ent in run["entries"].items():
        pk = ent.get("product")
        if pk not in prods:
            continue
        row = per.setdefault(pk, {"name": prods[pk]["name"], "asked": 0, "answered": 0,
                                  "mentioned": 0, "recommended": 0, "by_engine": {}})
        eng = ent.get("engine")
        be = row["by_engine"].setdefault(eng, {"asked": 0, "answered": 0, "recommended": 0})
        row["asked"] += 1
        be["asked"] += 1
        if not ent.get("ok"):
            continue
        row["answered"] += 1
        be["answered"] += 1
        for u in ent.get("citations", []):
            d = domain_of(u)
            if d and not is_ours(u):
                cited_domains[d] += 1
        j = ent.get("judgment")
        if not j:
            unjudged += 1
            continue
        if j.get("mentioned"):
            row["mentioned"] += 1
        if j.get("recommended"):
            row["recommended"] += 1
            be["recommended"] += 1
        if j.get("our_description") == "wrong":
            wrong_desc.append(f"{k}: {j.get('quote', '')[:120]}")
        for c in j.get("competitors", []):
            competitors.setdefault(pk, Counter())[c] += 1
        for c in j.get("criteria", []):
            criteria.setdefault(pk, Counter())[c] += 1
    return {
        "date": run["date"], "engines": engines, "complete": run.get("complete", False),
        "products": per, "unjudged": unjudged,
        "cited_domains": cited_domains.most_common(25),
        "competitors": {k: v.most_common(8) for k, v in competitors.items()},
        "criteria": {k: v.most_common(8) for k, v in criteria.items()},
        "wrong_descriptions": wrong_desc,
    }


def diff_summary(cur: dict, prev: Optional[dict]) -> dict:
    """지난 회차 대비 변화 — 새로 추천된 곳 / 사라진 곳 / 새 인용 도메인 / 새 경쟁자."""
    if not prev:
        return {"first": True}
    out: dict = {"first": False, "recommended_delta": {}, "new_domains": [], "gone_domains": [],
                 "new_competitors": {}}
    for pk, row in cur["products"].items():
        pr = prev["products"].get(pk)
        if pr:
            out["recommended_delta"][pk] = row["recommended"] - pr["recommended"]
    cd, pd = {d for d, _ in cur["cited_domains"]}, {d for d, _ in prev["cited_domains"]}
    out["new_domains"] = sorted(cd - pd)
    out["gone_domains"] = sorted(pd - cd)
    for pk, lst in cur["competitors"].items():
        prevset = {c for c, _ in prev["competitors"].get(pk, [])}
        new = [c for c, _ in lst if c not in prevset]
        if new:
            out["new_competitors"][pk] = new
    return out


# ── actions (LLM) ─────────────────────────────────────────────────────────

ACTIONS_SCHEMA = (
    '{"headline":"<한 줄 요약>","bot_actions":[{"title":"<무엇을>","why":"<결과의 어느 줄 때문에>",'
    '"target":"<제품 key 또는 apex>"}],"human_actions":[{"title":"<무엇을>","why":"<왜 사람이 해야 하나>",'
    '"target":"<제품 key>"}]}'
)


def build_actions_prompt(summary: dict, diff: dict, cfg: dict) -> str:
    L = [
        "너는 모멘터스(1인 AI 스튜디오)의 성장 데스크다. 아래는 이번 주 GEO 측정 집계다 —",
        "손님이 AI·검색에 '이런 거 하고 싶은데 뭐 쓰지?'라고 물었을 때 우리 제품이 후보로 뽑혔는지.",
        "",
        "결과를 **할 일**로 바꿔라. 세 가지 읽는 법:",
        "① 인용된 출처 도메인 = 우리가 실려야 할 자리 (디렉터리 등록·비교글 기고·커뮤니티)",
        "② 추천 기준 구절 = 우리 페이지에 문장으로 있어야 할 것 (FAQ·첫 문단·llms.txt)",
        "③ 질문 표현 = 우리가 써야 할 글 제목 (손님 말 그대로)",
        "",
        "bot_actions = 코드·페이지 수정·초안 작성처럼 봇이 혼자 끝낼 수 있는 일.",
        "human_actions = 계정 로그인·외부 제출·발행 승인·촬영처럼 사람이 해야 하는 일. 새로 생긴 것만.",
        "각 항목은 한 줄, 근거(why)는 집계의 어느 숫자·도메인·구절 때문인지 구체적으로.",
        "제품당 최대 2개, 전체 8개 이내. 근거 없는 일반론('SEO를 강화하세요')은 쓰지 마라.",
        "🚫 집계에 없는 서비스·도메인·숫자를 지어내지 마라.",
        "JSON 한 덩어리로만. 형식:", ACTIONS_SCHEMA, "",
        "─── 이번 주 집계 ───",
        json.dumps(summary, ensure_ascii=False, indent=1)[:12000],
        "",
        "─── 지난 회차 대비 ───",
        json.dumps(diff, ensure_ascii=False, indent=1)[:3000],
        "",
        "─── 제품 목록 ───",
    ]
    for p in cfg["products"]:
        L.append(f"- {p['key']}: {p['name']} {p['url']}")
    return "\n".join(L)


def sanitize_actions(parsed: Any, cfg: dict) -> Optional[dict]:
    if not isinstance(parsed, dict):
        return None
    keys = {p["key"] for p in cfg["products"]} | {"apex", "all"}

    def _clean(lst: Any) -> List[dict]:
        out = []
        for a in (lst or [])[:8]:
            if not isinstance(a, dict) or not a.get("title"):
                continue
            tgt = str(a.get("target") or "all")
            out.append({"title": str(a["title"])[:140], "why": str(a.get("why") or "")[:200],
                        "target": tgt if tgt in keys else "all"})
        return out

    return {"headline": str(parsed.get("headline") or "")[:200],
            "bot_actions": _clean(parsed.get("bot_actions")),
            "human_actions": _clean(parsed.get("human_actions"))}


def cmd_actions(date: str) -> dict:
    run = load_run(date)
    cfg = load_questions()
    summ = summarize(run, cfg)
    prev_date = previous_run_date(date)
    prev = summarize(load_run(prev_date), cfg) if prev_date else None
    diff = diff_summary(summ, prev)
    parsed = _claude_json(build_actions_prompt(summ, diff, cfg), timeout=300)
    acts = sanitize_actions(parsed, cfg)
    run["actions"] = acts
    run["summary"] = summ
    run["diff"] = diff
    run["prev_date"] = prev_date
    save_run(run)
    if acts is None:
        log("⚠️ actions 판정 실패 — 표만 보고한다")
    return run


# ── report / ledger ───────────────────────────────────────────────────────

def render_report(run: dict, cfg: dict, slack: bool = False) -> str:
    summ = run.get("summary") or summarize(run, cfg)
    diff = run.get("diff") or {"first": True}
    acts = run.get("actions")
    b = "*" if slack else "**"
    L = [f"{b}GEO 주간 측정 {summ['date']}{b} — 엔진: {', '.join(summ['engines'])}"
         + ("" if summ["complete"] else " (⚠️ 일부 칸 실패)")]
    if acts and acts.get("headline"):
        L.append(acts["headline"])
    L.append("")
    L.append(f"{b}제품별 추천됨 / 질문수{b}")
    for pk, row in summ["products"].items():
        parts = []
        for eng, be in row["by_engine"].items():
            parts.append(f"{eng} {be['recommended']}/{be['asked']}")
        delta = ""
        if not diff.get("first"):
            d = diff.get("recommended_delta", {}).get(pk)
            if isinstance(d, int) and d != 0:
                delta = f"  ({'+' if d > 0 else ''}{d})"
        L.append(f"• {row['name']}: 추천 {row['recommended']}/{row['asked']} · 언급 {row['mentioned']}"
                 f"{delta}  [{' · '.join(parts)}]")
    if summ.get("unjudged"):
        L.append(f"  미판정 {summ['unjudged']}건")
    L.append("")
    L.append(f"{b}대신 추천된 곳 (상위){b}")
    for pk, lst in summ["competitors"].items():
        if lst:
            L.append(f"• {summ['products'][pk]['name']}: " + ", ".join(f"{c}({n})" for c, n in lst[:5]))
    L.append("")
    L.append(f"{b}인용된 출처 도메인 = 우리가 실려야 할 자리{b}")
    L.append(", ".join(f"{d}({n})" for d, n in summ["cited_domains"][:12]) or "(없음)")
    if not diff.get("first") and diff.get("new_domains"):
        L.append("새로 등장: " + ", ".join(diff["new_domains"][:10]))
    if summ.get("wrong_descriptions"):
        L.append("")
        L.append(f"{b}우리 설명이 틀리게 나온 곳{b}")
        L += [f"• {w}" for w in summ["wrong_descriptions"][:5]]
    if acts:
        if acts.get("bot_actions"):
            L.append("")
            L.append(f"{b}봇이 이어서 할 일{b}")
            L += [f"• [{a['target']}] {a['title']} — {a['why']}" for a in acts["bot_actions"]]
        if acts.get("human_actions"):
            L.append("")
            L.append(f"{b}대표님 몫 (새로 생긴 것만){b}")
            L += [f"• [{a['target']}] {a['title']} — {a['why']}" for a in acts["human_actions"]]
    else:
        L.append("")
        L.append("(할 일 판정이 실패해 표만 올립니다 — 다음 회차에 다시 시도)")
    return "\n".join(L)


def append_ledger(run: dict, cfg: dict) -> None:
    summ = run.get("summary") or summarize(run, cfg)
    text = render_report(run, cfg, slack=False)
    head = ""
    if not LEDGER.exists():
        head = (
            "# GEO 원장 — '뭐 쓰지?'에 우리가 후보로 뽑히는가\n\n"
            "> 매주 `scripts/geo_probe.py weekly` 가 아래에 한 회차씩 쌓는다. 원본은 `runs/<날짜>.json`.\n"
            "> 읽는 법: **인용 도메인 = 실려야 할 자리 · 추천 기준 = 페이지에 있어야 할 문장 · 질문 표현 = 글 제목.**\n"
            "> 🚫 회차를 지우지 마라. 안 움직인 기록이 제일 값나간다(SEO_EXPERIMENTS.md 원칙).\n\n"
        )
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(head)
        f.write(f"\n---\n\n## {summ['date']}\n\n{text}\n")
    # 누적 출처 도메인 — 실려야 할 자리 목록
    cur: Dict[str, dict] = {}
    if SOURCES.exists():
        try:
            cur = json.loads(SOURCES.read_text(encoding="utf-8"))
        except Exception:
            cur = {}
    for d, n in summ["cited_domains"]:
        row = cur.setdefault(d, {"count": 0, "first": summ["date"], "last": summ["date"], "listed": False})
        row["count"] += n
        row["last"] = summ["date"]
    SOURCES.write_text(json.dumps(cur, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def git_commit_ledger(date: str) -> bool:
    try:
        subprocess.run(["git", "add", "docs/geo"], cwd=ROOT, check=True, capture_output=True)
        cp = subprocess.run(["git", "commit", "-q", "-m", f"chore(geo): 주간 측정 {date}",
                             "docs/geo"], cwd=ROOT, capture_output=True, text=True)
        return cp.returncode == 0
    except Exception as e:  # noqa: BLE001
        log(f"git commit 실패(무시): {e}")
        return False


def cmd_weekly(engines: List[str], products: Optional[List[str]], limit: Optional[int],
               date: Optional[str] = None, commit: bool = True) -> dict:
    date = date or today()
    cmd_run(date, engines, products, limit)
    cmd_judge(date)
    run = cmd_actions(date)
    cfg = load_questions()
    append_ledger(run, cfg)
    run["reported"] = run.get("reported", False)
    save_run(run)
    _write_status({"phase": "done", "date": date, "finished": _now_iso(), "complete": run["complete"]})
    if commit:
        git_commit_ledger(date)
    return run


# ── CLI ───────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("run", "weekly"):
        s = sub.add_parser(name)
        s.add_argument("--engines", default=",".join(ENGINES))
        s.add_argument("--products", default="")
        s.add_argument("--limit", type=int, default=None)
        s.add_argument("--date", default=None)
        if name == "weekly":
            s.add_argument("--no-commit", action="store_true")
    for name in ("judge", "actions", "report"):
        s = sub.add_parser(name)
        s.add_argument("--date", default=None)
        if name == "report":
            s.add_argument("--slack", action="store_true")
    a = ap.parse_args(argv)
    date = getattr(a, "date", None) or today()
    if a.cmd in ("run", "weekly"):
        engines = [e for e in a.engines.split(",") if e]
        bad = [e for e in engines if e not in ENGINES]
        if bad:
            ap.error(f"모르는 엔진 {bad} (가능: {ENGINES})")
        products = [p for p in a.products.split(",") if p] or None
        if a.cmd == "run":
            cmd_run(date, engines, products, a.limit)
        else:
            run = cmd_weekly(engines, products, a.limit, date, commit=not a.no_commit)
            print(render_report(run, load_questions()))
        return 0
    if a.cmd == "judge":
        cmd_judge(date)
        return 0
    if a.cmd == "actions":
        run = cmd_actions(date)
        print(json.dumps(run.get("actions"), ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "report":
        print(render_report(load_run(date), load_questions(), slack=a.slack))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
