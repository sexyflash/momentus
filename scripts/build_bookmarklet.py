# -*- coding: utf-8 -*-
"""북마크릿 빌더 — bookmarklets/<이름>.js(읽기용 원본) → assets/bookmarklets/<이름>.txt(배포본).

왜 필요한가: .txt 는 퍼센트 인코딩된 한 줄이라 손으로 못 고친다. 실제로 README 는
"원본 .js 가 여기 있다"고 적어놨는데 그 파일이 없어서, 그동안 인코딩된 덩어리를
직접 건드려야 했다(#·% 금지 같은 함정이 전부 거기서 나왔다).

보존 규칙 — **꼬리를 건드리지 않는다.**
  .txt = <인코딩된 본체> + <날것 그대로의 공용 꼬리 2개>
  꼬리 = 귀환 갈고리(다른 무료 도구 보기) + GA 픽셀. 도구 4종이 공유하고,
  인코딩되지 않은 채로 붙어 있다. 여기서는 기존 .txt 에서 잘라내 그대로 다시 붙인다.
  (README "계측" 절 참조 — 이 두 줄이 사라지면 설치·실행 지표가 죽는다.)

실행: python3 scripts/build_bookmarklet.py pinterest-grab
"""
import os
import re
import subprocess
import sys
import urllib.parse

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

TAIL_MARK = ";(function(){var IDS="   # 공용 꼬리 시작점(날것)


def strip_comments(src: str) -> str:
    """/* 블록 주석 */ 만 제거하고 줄 앞 들여쓰기를 턴다.
    // 줄 주석은 건드리지 않는다 — 문자열 안의 '//'(URL 경로)와 구분할 안전한 방법이 없다."""
    out = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    lines = [ln.strip() for ln in out.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def node_check(body: str, label: str) -> None:
    p = subprocess.run(["node", "--check", "-"], input=body, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"❌ {label} 문법 오류\n{p.stderr}")


def build(name: str) -> None:
    src_path = f"bookmarklets/{name}.js"
    out_path = f"assets/bookmarklets/{name}.txt"
    with open(src_path, encoding="utf-8") as f:
        src = f.read().strip()
    node_check(src, "원본")

    body = strip_comments(src)
    node_check(body, "주석 제거본")

    with open(out_path, encoding="utf-8") as f:
        old = f.read().strip()
    i = old.find(TAIL_MARK)
    if i < 0:
        sys.exit(f"❌ {out_path} 에서 공용 꼬리({TAIL_MARK})를 못 찾았다 — 손으로 확인해라")
    tail = old[i:]

    # encodeURIComponent 와 같은 규칙(원본 파일이 그렇게 만들어져 있다)
    enc = urllib.parse.quote(body, safe="!*'()")
    new = "javascript:" + enc + tail

    # 되돌려서 한 번 더 검증 — 배포되는 바로 그 문자열을 검사한다
    decoded = urllib.parse.unquote(new[len("javascript:"):])
    node_check(decoded, "배포본(디코드)")
    if "#" in enc:
        sys.exit("❌ 인코딩 결과에 날 # 이 있다 — javascript: URL 에서 잘린다")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(new + "\n")
    print(f"✅ {out_path}  ({len(old)} → {len(new)} bytes, 꼬리 {len(tail)} bytes 보존)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("사용법: python3 scripts/build_bookmarklet.py <이름>  (예: pinterest-grab)")
    for n in sys.argv[1:]:
        build(n)
