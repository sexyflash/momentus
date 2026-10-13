/* 인스타 인기순 정렬 — 읽기용 원본. 배포본은 python3 scripts/build_bookmarklet.py insta-rank
   2026-10-13 조회수 정렬 추가:
   - 프로필 그리드의 릴스 링크는 /p/ 가 아니라 /reel/ 이다. 예전엔 /p/ 만 모아 릴스가 통째로 빠졌다.
   - 조회수는 릴스 탭(/<계정>/reels/)에만 찍힌다. 메인 그리드엔 조회수가 아예 없다(실측).
   - 릴스 탭 썸네일은 <img> 가 아니라 배경 이미지(div style) 라 거기서 주소를 꺼낸다.
   - 칸 구조: 좋아요·댓글 = 호버 오버레이의 li 안 / 조회수 = li 밖의 숫자 span. */
(function () {
  var LINK = 'a[href*="/p/"],a[href*="/reel/"]';
  if (document.getElementById("ig-sort-float")) document.getElementById("ig-sort-float").remove();
  if (document.getElementById("ig-sort-style")) document.getElementById("ig-sort-style").remove();
  if (window.__igSortBackup) {
    try {
      var p0 = window.__igSortBackup;
      if (p0.newContainer && p0.newContainer.parentElement) p0.newContainer.parentElement.removeChild(p0.newContainer);
      if (p0.scroller) p0.scroller.style.display = p0.scrollerOrigDisplay || "";
    } catch (e) {}
    window.__igSortBackup = null;
  }
  var styleEl = document.createElement("style");
  styleEl.id = "ig-sort-style";
  styleEl.textContent =
    '.ig-sorted-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;width:100%;max-width:963px;margin:0 auto;}.ig-sorted-cell{position:relative;aspect-ratio:1;overflow:hidden;cursor:pointer;background:#000;display:block;text-decoration:none;}.ig-sorted-cell img{width:100%;height:100%;object-fit:cover;display:block;transition:transform 0.25s;}.ig-sorted-cell:hover img{transform:scale(1.05);}.ig-sorted-cell::after{content:"";position:absolute;inset:0;background:rgba(0,0,0,0);transition:background 0.15s;pointer-events:none;}.ig-sorted-cell:hover::after{background:rgba(0,0,0,0.25);}.ig-rank-badge{position:absolute;top:12px;left:12px;background:rgba(0,0,0,0.85);color:#fff;font-size:13px;font-weight:700;padding:0 12px;border-radius:20px;height:24px;display:inline-flex;align-items:center;gap:8px;z-index:2;font-family:-apple-system,sans-serif;pointer-events:none;line-height:1;white-space:nowrap;max-width:calc(100% - 24px);overflow:hidden;}.ig-type-icon{position:absolute;top:12px;right:12px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,0.7);z-index:2;pointer-events:none;font-size:18px;line-height:1;}';
  document.head.appendChild(styleEl);
  var MAX_SECONDS = 180;
  var METRICS = {
    views: { icon: "▶", label: "조회수" },
    likes: { icon: "❤️", label: "좋아요" },
    comments: { icon: "💬", label: "댓글" }
  };
  function parseNum(t) {
    if (!t) return 0;
    t = t.trim().replace(/,/g, "");
    var n = parseFloat(t);
    if (isNaN(n)) return 0;
    if (/억/.test(t)) return Math.round(n * 100000000);
    if (/만/.test(t)) return Math.round(n * 10000);
    if (/천/.test(t)) return Math.round(n * 1000);
    if (/[bB]/.test(t)) return Math.round(n * 1000000000);
    if (/[mM]/.test(t)) return Math.round(n * 1000000);
    if (/[kK]/.test(t)) return Math.round(n * 1000);
    return Math.round(n);
  }
  function digitSpan(root) {
    var t = [].slice.call(root.querySelectorAll("span")).map(function (s) {
      return s.textContent.trim();
    }).find(function (s) {
      return /\d/.test(s);
    });
    return parseNum(t);
  }
  function readNums(el) {
    return [].slice.call(el.querySelectorAll("li")).map(digitSpan).filter(function (n) {
      return n > 0;
    });
  }
  function readViews(el) {
    var spans = [].slice.call(el.querySelectorAll("span")).filter(function (s) {
      return !s.closest("li") && !s.querySelector("span") && /\d/.test(s.textContent);
    });
    return spans.length ? parseNum(spans[0].textContent) : 0;
  }
  function thumbOf(aTag) {
    var img = aTag.querySelector("img");
    if (img && img.src) return { src: img.src, srcset: img.srcset || "", alt: img.alt || "" };
    var bg = [].slice.call(aTag.querySelectorAll("div")).map(function (d) {
      return d.style.backgroundImage || "";
    }).find(function (s) {
      return /url\(/.test(s);
    });
    var m = bg && bg.match(/url\(["']?(.*?)["']?\)$/);
    return { src: m ? m[1] : "", srcset: "", alt: "" };
  }
  function findCommonParent(els) {
    if (els.length === 0) return null;
    var ancestors = [];
    var p = els[0].parentElement;
    while (p) {
      ancestors.push(p);
      p = p.parentElement;
    }
    for (var i = 1; i < Math.min(els.length, 15); i++) {
      var c = els[i].parentElement;
      var found = null;
      while (c) {
        if (ancestors.indexOf(c) !== -1) {
          found = c;
          break;
        }
        c = c.parentElement;
      }
      if (found) ancestors = ancestors.slice(ancestors.indexOf(found));
    }
    return ancestors[0];
  }
  function findContainer() {
    var grid = document.querySelector('div[style*="gridTemplateColumns"]');
    if (grid) {
      var p = grid.parentElement;
      while (p) {
        var st = p.getAttribute("style") || "";
        if ((/flex-direction:\s*column/.test(st) || /padding-(top|bottom):\s*[\d.]+/.test(st)) && p.querySelectorAll('div[style*="gridTemplateColumns"]').length >= 3) return p;
        if (p.tagName === "SECTION") break;
        p = p.parentElement;
      }
      return grid.parentElement;
    }
    var main = document.querySelector("main") || document.body;
    var allLinks = [].slice.call(main.querySelectorAll(LINK));
    if (allLinks.length === 0) return null;
    var common = findCommonParent(allLinks);
    if (!common) return null;
    var c = common;
    while (c) {
      if (c.tagName === "MAIN" || c.tagName === "SECTION") break;
      var rect = c.getBoundingClientRect();
      if (rect.width >= 600 && rect.width <= 1200 && c.parentElement && c.parentElement.getBoundingClientRect().width > rect.width + 50) return c;
      c = c.parentElement;
    }
    return common;
  }
  function fireOnAnchor(aTag, events, coords) {
    if (!aTag) return;
    var rect = aTag.getBoundingClientRect();
    var cx = coords ? coords.x : rect.left + rect.width / 2;
    var cy = coords ? coords.y : rect.top + rect.height / 2;
    var ev = { bubbles: true, cancelable: true, clientX: cx, clientY: cy, view: window, composed: true };
    [aTag.parentElement && aTag.parentElement.parentElement, aTag.parentElement, aTag].concat([].slice.call(aTag.querySelectorAll("div"))).forEach(function (t) {
      if (!t) return;
      events.forEach(function (e) {
        t.dispatchEvent(new MouseEvent(e, ev));
      });
    });
  }
  function captureMetadata(aTag) {
    var th = thumbOf(aTag);
    return {
      href: aTag.getAttribute("href"),
      src: th.src,
      srcset: th.srcset,
      alt: th.alt,
      carousel: !!aTag.querySelector('svg[aria-label="슬라이드"],svg[aria-label="Carousel"]'),
      reel: /\/reel\//.test(aTag.getAttribute("href")) || !!aTag.querySelector('svg[aria-label="릴스"],svg[aria-label="Reel"],svg[aria-label="Clip"],svg[aria-label="클립"]'),
      video: !!aTag.querySelector('svg[aria-label="동영상"],svg[aria-label="Video"]')
    };
  }
  var allCells = {};
  var containerRef = null;
  function batchScanVisible() {
    return new Promise(function (resolve) {
      var container = containerRef || document.body;
      var anchors = [].slice.call(container.querySelectorAll(LINK));
      var pending = [];
      anchors.forEach(function (a) {
        if (a.dataset.igProcessed === "1") return;
        var href = a.getAttribute("href");
        if (allCells[href]) {
          a.dataset.igProcessed = "1";
          return;
        }
        pending.push({ aTag: a, href: href });
      });
      if (pending.length === 0) {
        resolve(0);
        return;
      }
      pending.forEach(function (p) {
        fireOnAnchor(p.aTag, ["pointerover", "pointerenter", "mouseover", "mouseenter"]);
      });
      setTimeout(function () {
        pending.forEach(function (p) {
          p.aTag.dataset.igProcessed = "1";
          var meta = captureMetadata(p.aTag);
          var nums = readNums(p.aTag);
          meta.likes = nums[0] || 0;
          meta.comments = nums[1] || 0;
          meta.views = readViews(p.aTag);
          allCells[p.href] = meta;
        });
        pending.forEach(function (p) {
          fireOnAnchor(p.aTag, ["pointerout", "pointerleave", "mouseout", "mouseleave"], { x: -9999, y: -9999 });
        });
        setTimeout(function () {
          resolve(pending.length);
        }, 30);
      }, 220);
    });
  }
  var onReelsTab = /\/reels\/?$/.test(location.pathname);
  var account = (location.pathname.split("/").filter(Boolean)[0] || "");
  var float = document.createElement("div");
  float.id = "ig-sort-float";
  float.style.cssText = "position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:99999;display:flex;flex-direction:column;align-items:center;gap:8px;font-family:-apple-system,sans-serif;";
  var ctl = "background:#262626;color:#fff;font-size:14px;font-weight:700;padding:8px 10px;border:1px solid #444;border-radius:20px;outline:none;";
  float.innerHTML =
    '<div class="ig-msg" style="background:rgba(0,0,0,0.85);color:#fff;font-size:13px;font-weight:600;padding:10px 20px;border-radius:24px;box-shadow:0 4px 20px rgba(0,0,0,0.3);white-space:nowrap;max-width:80vw;text-align:center;overflow:hidden;text-overflow:ellipsis;"></div>' +
    '<a class="ig-reels-link" style="display:none;background:#0095f6;color:#fff;font-size:13px;font-weight:700;padding:8px 16px;border-radius:20px;text-decoration:none;">릴스 탭으로 이동 →</a>' +
    '<div style="display:flex;gap:6px;align-items:center;background:rgba(0,0,0,0.85);padding:6px;border-radius:28px;box-shadow:0 4px 16px rgba(0,0,0,0.3);">' +
    '<select class="ig-metric" style="' + ctl + 'cursor:pointer;">' +
    '<option value="views">▶ 조회수</option><option value="likes">❤️ 좋아요</option><option value="comments">💬 댓글</option></select>' +
    '<input class="ig-input" type="number" value="100" min="10" max="2000" step="10" style="' + ctl + 'width:70px;text-align:center;"/>' +
    '<button class="ig-btn-sort" style="background:#0095f6;color:#fff;font-size:14px;font-weight:700;padding:9px 20px;border:none;border-radius:22px;cursor:pointer;white-space:nowrap;">정렬</button>' +
    '<button class="ig-btn-restore" style="background:#262626;color:#fff;font-size:14px;font-weight:700;padding:9px 16px;border:1px solid #444;border-radius:22px;cursor:pointer;display:none;white-space:nowrap;">↩️ 원복</button></div>';
  document.body.appendChild(float);
  var msg = float.querySelector(".ig-msg");
  var reelsLink = float.querySelector(".ig-reels-link");
  var metricSel = float.querySelector(".ig-metric");
  var input = float.querySelector(".ig-input");
  var btnSort = float.querySelector(".ig-btn-sort");
  var btnRestore = float.querySelector(".ig-btn-restore");
  metricSel.value = onReelsTab ? "views" : "likes";
  if (account) reelsLink.href = "/" + account + "/reels/";
  function setMsg(t) {
    msg.textContent = t;
  }
  function needReelsTab() {
    return metricSel.value === "views" && !onReelsTab;
  }
  function hint() {
    reelsLink.style.display = needReelsTab() && account ? "inline-block" : "none";
    if (needReelsTab()) setMsg("조회수는 릴스 탭에만 표시됩니다 — 릴스 탭에서 다시 눌러 주세요");
    else setMsg("기준·최대 갯수 정하고 정렬");
  }
  hint();
  function phase1Scan(maxPosts) {
    return new Promise(function (resolve) {
      setMsg("상단으로 이동...");
      containerRef = findContainer();
      window.scrollTo(0, 0);
      var startTime = Date.now();
      setTimeout(function () {
        var noNewCount = 0;
        function loop() {
          batchScanVisible().then(function () {
            var curCount = Object.keys(allCells).length;
            setMsg("수집중 " + curCount + "/" + maxPosts);
            if (curCount >= maxPosts) return finish(maxPosts + "개 도달");
            var elapsed = (Date.now() - startTime) / 1000;
            if (elapsed > MAX_SECONDS) return finish("시간한도");
            var beforeCount = curCount;
            window.scrollBy(0, window.innerHeight * 0.7);
            setTimeout(function () {
              batchScanVisible().then(function () {
                var newCount = Object.keys(allCells).length;
                var atBottom = window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 200;
                if (newCount === beforeCount) noNewCount++;
                else noNewCount = 0;
                setMsg(newCount + "/" + maxPosts + " | " + Math.round(elapsed) + "s | " + (atBottom ? "바닥" : "스크롤"));
                if (noNewCount >= 8) return finish("새 게시물 없음");
                setTimeout(loop, atBottom ? 1500 : 400);
              });
            }, 400);
          });
        }
        function finish(reason) {
          setMsg("수집 완료(" + reason + "). " + Object.keys(allCells).length + "개");
          resolve();
        }
        loop();
      }, 600);
    });
  }
  function unmountGrid() {
    var p = window.__igSortBackup;
    if (!p) return;
    try {
      if (p.newContainer && p.newContainer.parentElement) p.newContainer.parentElement.removeChild(p.newContainer);
      if (p.scroller) p.scroller.style.display = p.scrollerOrigDisplay || "";
    } catch (e) {
      console.error(e);
    }
    window.__igSortBackup = null;
  }
  function fmt(n) {
    if (!(n > 0)) return "—";
    if (n >= 100000000) return +(n / 100000000).toFixed(1) + "억";
    if (n >= 10000) return +(n / 10000).toFixed(1) + "만";
    return n.toLocaleString();
  }
  function buildSortedGrid() {
    var key = metricSel.value;
    var container = containerRef || findContainer();
    if (!container) {
      setMsg("❌ 게시물 목록을 못 찾았습니다");
      return;
    }
    var list = Object.keys(allCells).map(function (k) {
      return allCells[k];
    }).filter(function (d) {
      return d.src && d.href;
    });
    if (list.length === 0) {
      setMsg("❌ 정렬할 데이터 없음");
      return;
    }
    if (key === "views" && !list.some(function (d) { return d.views > 0; })) {
      reelsLink.style.display = account ? "inline-block" : "none";
      setMsg("이 화면엔 조회수가 없습니다 — 릴스 탭에서 다시 눌러 주세요");
      return;
    }
    var order = [key].concat(["views", "likes", "comments"].filter(function (k) { return k !== key; }));
    var sorted = list.slice().sort(function (a, b) {
      return (b[key] || 0) - (a[key] || 0);
    });
    unmountGrid();
    var newContainer = document.createElement("div");
    newContainer.id = "ig-sort-container";
    newContainer.className = "ig-sorted-grid";
    sorted.forEach(function (d, idx) {
      var cell = document.createElement("a");
      cell.className = "ig-sorted-cell";
      cell.href = d.href;
      cell.target = "_blank";
      cell.rel = "noopener";
      var img = document.createElement("img");
      img.src = d.src;
      if (d.srcset) img.srcset = d.srcset;
      img.alt = d.alt || "";
      img.referrerPolicy = "no-referrer";
      cell.appendChild(img);
      if (d.carousel || d.reel || d.video) {
        var icon = document.createElement("div");
        icon.className = "ig-type-icon";
        icon.textContent = d.reel ? "⏵" : d.video ? "▶" : "⊟";
        cell.appendChild(icon);
      }
      var badge = document.createElement("div");
      badge.className = "ig-rank-badge";
      var parts = order.filter(function (k) {
        return k === key || d[k] > 0;
      }).map(function (k, i) {
        return '<span style="' + (i === 0 ? "" : "opacity:0.75;") + '">' + METRICS[k].icon + " " + fmt(d[k]) + "</span>";
      });
      badge.innerHTML = '<span style="font-weight:800;">' + String.fromCharCode(35) + (idx + 1) + '</span><span style="opacity:0.4;">|</span>' + parts.join('<span style="opacity:0.4;">·</span>');
      cell.appendChild(badge);
      newContainer.appendChild(cell);
    });
    window.__igSortBackup = { scroller: container, scrollerOrigDisplay: container.style.display || "", newContainer: newContainer };
    container.style.display = "none";
    container.parentElement.insertBefore(newContainer, container);
    window.scrollTo(0, 0);
    reelsLink.style.display = "none";
    setMsg("✅ " + sorted.length + "개 · " + METRICS[key].label + "순 정렬 완료");
    btnRestore.style.display = "inline-block";
    btnSort.textContent = "다시 모으기";
  }
  function restore() {
    if (!window.__igSortBackup) return;
    unmountGrid();
    btnRestore.style.display = "none";
    btnSort.textContent = "정렬";
    setMsg("원래대로 복구됨");
  }
  function run() {
    if (needReelsTab()) {
      hint();
      return;
    }
    var maxPosts = parseInt(input.value) || 100;
    if (maxPosts < 10) maxPosts = 10;
    if (window.__igSortBackup) restore();
    allCells = {};
    [].slice.call(document.querySelectorAll("[data-ig-processed]")).forEach(function (a) {
      delete a.dataset.igProcessed;
    });
    btnSort.disabled = true;
    btnSort.textContent = "실행중...";
    phase1Scan(maxPosts).then(function () {
      buildSortedGrid();
      btnSort.disabled = false;
      if (!window.__igSortBackup) btnSort.textContent = "정렬";
    });
  }
  metricSel.onchange = function () {
    if (Object.keys(allCells).length && !btnSort.disabled && !needReelsTab()) buildSortedGrid();
    else hint();
  };
  btnSort.onclick = run;
  btnRestore.onclick = restore;
})()
