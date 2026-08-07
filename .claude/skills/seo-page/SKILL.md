---
name: seo-page
description: momentus(the-moment.us) 페이지를 만들거나 <head>·JSON-LD·og:image·sitemap 을 건드릴 때 쓴다. 전역 seo-page 스킬의 momentus 전용 보충판. "페이지 추가", "제품 추가", "상세페이지 만들어", "SEO", "GEO", "구조화 데이터", "og 이미지" 라고 하면 발동.
---

# momentus 전용 — SEO/GEO 작업

**공통 규칙은 전역 스킬 `~/.claude/skills/seo-page/SKILL.md` 와
정본 문서 [docs/SEO_GEO.md](../../../docs/SEO_GEO.md) 에 있다. 여기 복붙하지 마라.**
이 문서는 **momentus 에서만 다른 것**만 적는다.

## momentus 는 대부분 이미 자동이다

`<head>` 9종·`canonical`·`og:image`·`twitter:card`·**페이지 유형별 JSON-LD** 가
전부 자동으로 붙는다. 새 페이지를 만들어도 빠뜨릴 수가 없는 구조다.

| 자동으로 붙는 것 | 어디서 |
|---|---|
| `<head>` 기본 9종 | `gen_site.py` 의 `page()` |
| `canonical`·`og:url`·`og:image`·`twitter:image` | `gen_site.py` 맨 끝 후처리 (경로에서 도출) |
| 페이지 유형별 JSON-LD | 같은 후처리의 `_schema_for()` (경로에서 유형 판별) |
| OG 이미지 PNG | `scripts/gen_og.py` (`products.json` 파생) |
| sitemap·robots.txt·llms.txt | `gen_site.py` |
| 빈 태그 페이지 `noindex` + sitemap 제외 | `gen_site.py` (글 0편이면 자동) |

## 그래서 실제로 할 일

**제품 추가** — `data/products.json` 에 한 줄. 끝이다.
카드·바·푸터·페이지·OG이미지·sitemap·llms.txt·JSON-LD 가 전부 따라온다.

**새 페이지 유형** — `gen_site.py` 에 빌더를 추가하고 **반드시 `page()` 를 통과시켜라.**
그다음 `_schema_for()` 에 그 경로의 `@type` 분기를 한 줄 추가한다.

**본문** — 이건 자동이 안 된다. 전역 스킬 §4 를 따라 직접 써라.

## 🚫 momentus 에서 하면 안 되는 것

- `index.html`·`products/*/index.html` 등 **생성물 직접 수정** → 매일 05:45 재빌드가 지운다
- `canonical`·`og:image`·`ld+json` 을 **손으로 박기** → 후처리가 덮어쓴다
- **손관리 HTML 주석에 `/assets/site.css?v=` 쓰기** → 생성물 판별이 단순 substring 이라
  주석에 있어도 생성물로 오인해 후처리가 그 파일을 덮어쓴다 (2026-08-07 사고)
- `robots.txt` 삭제 → Cloudflare 가 쓸모없는 자동 안내문을 주입한다
- `/l/*` 를 301 로 변경 → 302 + `no-store` 가 의도다

## 끝내기 전

```bash
python3 scripts/gen_site.py      # 생성 (og 이미지·스키마 포함)
python3 scripts/seo_check.py     # FAIL 0 이어야 한다
```

`.claude/settings.json` 의 PostToolUse 훅이 `*.html`·`gen_site.py`·`products.json` 을
고칠 때마다 점검기를 자동으로 돌린다(경고만, 작업은 안 막는다).
