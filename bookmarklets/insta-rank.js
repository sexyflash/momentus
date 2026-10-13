/* 인스타 인기순 정렬 — 읽기용 원본. 배포본은 python3 scripts/build_bookmarklet.py insta-rank
   2026-10-13 조회수 정렬 추가:
   - 프로필 그리드의 릴스 링크는 /p/ 가 아니라 /reel/ 이다. 예전엔 /p/ 만 모아 릴스가 통째로 빠졌다.
   - 조회수는 릴스 탭(/<계정>/reels/)에만 찍힌다. 메인 그리드엔 조회수가 아예 없다(실측).
   - 릴스 탭 썸네일은 <img> 가 아니라 배경 이미지(div style) 라 거기서 주소를 꺼낸다.
   - 칸 구조: 좋아요·댓글 = 호버 오버레이의 li 안 / 조회수 = li 밖의 숫자 span.
   2026-10-13 둘째 판 — 탐색(/explore/) 화면:
   - 칸에 숫자가 하나도 안 찍히고 호버해도 안 뜬다 → 화면을 긁는 방식으로는 전부 「—」였다.
   - 대신 인스타가 페이지에 심어 둔 데이터(script application/json, 문자열 안에 또 JSON)와
     스크롤할 때 받아오는 응답(fetch·XHR)에 게시물마다 like_count·comment_count·play_count 가 있다.
     그걸 게시물 코드(/p/<코드>/)로 맞춰 쓰고, 없을 때만 화면 숫자로 돌아간다.
   - 셋째 판: 다른 화면에서 탐색으로 넘어오면 첫 묶음 데이터가 북마크 실행 전에 이미 지나가
     심긴 데이터에도 응답 가로채기에도 안 잡힌다(대표 화면에서 조회수 0건). 빈 칸만
     게시물 정보(/api/v1/media/<id>/info/)를 3개씩 천천히 물어 채운다. 429 면 즉시 멈춘다.
   - 탐색 화면의 릴스 칸은 <img> 없이 <video> 라 썸네일도 데이터(image_versions2)에서 꺼낸다. */
(function () {
  var LINK = 'a[href*="/p/"],a[href*="/reel/"]';
  var DATA = window.__igSortData = window.__igSortData || {};
  function num(v) {
    return typeof v === "number" && v > 0 ? v : 0;
  }
  function pickThumb(o) {
    var c = o.image_versions2 && o.image_versions2.candidates;
    if (!c || !c.length) {
      var cm = o.carousel_media && o.carousel_media[0];
      c = cm && cm.image_versions2 && cm.image_versions2.candidates;
    }
    if (c && c.length) {
      var best = c[0];
      c.forEach(function (x) {
        if (x.width >= 320 && x.width < best.width) best = x;
      });
      return best.url || "";
    }
    return o.display_uri || o.thumbnail_src || o.display_url || "";
  }
  function walk(o, depth) {
    if (!o || depth > 60) return;
    if (typeof o === "string") {
      if (o.length > 50 && (o.charAt(0) === "{" || o.charAt(0) === "[") && o.indexOf("like_count") >= 0) {
        try {
          walk(JSON.parse(o), depth + 1);
        } catch (e) {}
      }
      return;
    }
    if (typeof o !== "object") return;
    if (Array.isArray(o)) {
      for (var i = 0; i < o.length; i++) walk(o[i], depth + 1);
      return;
    }
    var code = o.code || o.shortcode;
    if (typeof code === "string" && ("like_count" in o || "play_count" in o || "comment_count" in o || "edge_liked_by" in o)) {
      var prev = DATA[code] || {};
      var likes = num(o.like_count) || num(o.edge_liked_by && o.edge_liked_by.count) || num(o.edge_media_preview_like && o.edge_media_preview_like.count);
      var comments = num(o.comment_count) || num(o.edge_media_to_comment && o.edge_media_to_comment.count);
      var views = num(o.play_count) || num(o.ig_play_count) || num(o.view_count) || num(o.video_play_count) || num(o.video_view_count);
      DATA[code] = {
        likes: likes || prev.likes || 0,
        comments: comments || prev.comments || 0,
        views: views || prev.views || 0,
        thumb: prev.thumb || pickThumb(o)
      };
    }
    for (var k in o) {
      if (Object.prototype.hasOwnProperty.call(o, k)) walk(o[k], depth + 1);
    }
  }
  function ingestText(t) {
    if (!t || t.indexOf("like_count") < 0 && t.indexOf("play_count") < 0) return;
    t = t.replace(/^for \(;;\);/, "");
    try {
      walk(JSON.parse(t), 0);
      return;
    } catch (e) {}
    t.split("\n").forEach(function (line) {
      try {
        walk(JSON.parse(line), 0);
      } catch (e) {}
    });
  }
  function ingestPage() {
    [].slice.call(document.querySelectorAll('script[type="application/json"]')).forEach(function (sc) {
      if (sc.dataset.igIngested === "1") return;
      sc.dataset.igIngested = "1";
      ingestText(sc.textContent);
    });
  }
  if (!window.__igSortHooked) {
    window.__igSortHooked = true;
    try {
      var of = window.fetch;
      window.fetch = function () {
        var pr = of.apply(this, arguments);
        pr.then(function (r) {
          try {
            r.clone().text().then(ingestText, function () {});
          } catch (e) {}
        }, function () {});
        return pr;
      };
    } catch (e) {}
    try {
      var os = XMLHttpRequest.prototype.send;
      XMLHttpRequest.prototype.send = function () {
        this.addEventListener("load", function () {
          try {
            if (!this.responseType || this.responseType === "text") ingestText(this.responseText);
          } catch (e) {}
        });
        return os.apply(this, arguments);
      };
    } catch (e) {}
  }
  function codeOf(href) {
    var m = (href || "").match(/\/(?:p|reel)\/([^\/?]+)/);
    return m ? m[1] : "";
  }
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
    var v = aTag.querySelector("video");
    return {
      href: aTag.getAttribute("href"),
      code: codeOf(aTag.getAttribute("href")),
      src: th.src || (v && v.poster) || "",
      video_src: v ? v.currentSrc || v.src || "" : "",
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
  var segs = location.pathname.split("/").filter(Boolean);
  var NOT_PROFILE = ["explore", "reels", "reel", "p", "tags", "locations", "stories", "direct", "accounts", "search"];
  var account = segs.length && NOT_PROFILE.indexOf(segs[0]) < 0 ? segs[0] : "";
  var onReelsTab = !!account && segs[1] === "reels";
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
  metricSel.value = account && !onReelsTab ? "likes" : "views";
  if (account) reelsLink.href = "/" + account + "/reels/";
  function setMsg(t) {
    msg.textContent = t;
  }
  function needReelsTab() {
    return metricSel.value === "views" && !!account && !onReelsTab;
  }
  function hint() {
    reelsLink.style.display = needReelsTab() ? "inline-block" : "none";
    if (needReelsTab()) setMsg("프로필 첫 화면엔 조회수가 없습니다 — 릴스 탭에서 다시 눌러 주세요");
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
  var B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
  function pkOf(code) {
    var n = BigInt(0);
    var c = code.slice(0, 11);
    for (var i = 0; i < c.length; i++) n = n * BigInt(64) + BigInt(B64.indexOf(c.charAt(i)));
    return n.toString();
  }
  function fillMissing() {
    ingestPage();
    var todo = Object.keys(allCells).map(function (k) {
      return allCells[k];
    }).filter(function (d) {
      if (!d.code) return false;
      var x = DATA[d.code];
      if (!x) return true;
      return (d.reel || d.video || d.video_src) && !x.views;
    }).map(function (d) {
      return d.code;
    });
    if (!todo.length) return Promise.resolve();
    var done = 0;
    var stopped = false;
    function one(code) {
      return fetch("/api/v1/media/" + pkOf(code) + "/info/", { headers: { "X-IG-App-ID": "936619743392459" }, credentials: "include" }).then(function (r) {
        if (r.status === 429) stopped = true;
        return r.ok ? r.text() : "";
      }).then(function (t) {
        ingestText(t);
      }, function () {}).then(function () {
        done++;
        setMsg("숫자 확인중 " + done + "/" + todo.length);
      });
    }
    return new Promise(function (resolve) {
      var i = 0;
      var active = 0;
      function next() {
        if (stopped || i >= todo.length) {
          if (active === 0) resolve();
          return;
        }
        var code = todo[i++];
        active++;
        one(code).then(function () {
          active--;
          setTimeout(next, 150);
        });
      }
      for (var k = 0; k < 3; k++) next();
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
    ingestPage();
    var list = Object.keys(allCells).map(function (k) {
      var d = allCells[k];
      var x = DATA[d.code];
      if (x) {
        d.likes = x.likes || d.likes;
        d.comments = x.comments || d.comments;
        d.views = x.views || d.views;
        if (!d.src) d.src = x.thumb || "";
      }
      return d;
    }).filter(function (d) {
      return d.href && (d.src || d.video_src);
    });
    if (list.length === 0) {
      setMsg("❌ 정렬할 데이터 없음");
      return;
    }
    if (key === "views" && !list.some(function (d) { return d.views > 0; })) {
      reelsLink.style.display = account && !onReelsTab ? "inline-block" : "none";
      setMsg(account && !onReelsTab ? "프로필 첫 화면엔 조회수가 없습니다 — 릴스 탭에서 다시 눌러 주세요" : "모은 게시물에 조회수 정보가 없습니다(사진만 있으면 조회수가 없습니다)");
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
      var img;
      if (d.src) {
        img = document.createElement("img");
        img.src = d.src;
        if (d.srcset) img.srcset = d.srcset;
        img.alt = d.alt || "";
        img.referrerPolicy = "no-referrer";
      } else {
        img = document.createElement("video");
        img.src = d.video_src;
        img.muted = true;
        img.preload = "metadata";
        img.style.cssText = "width:100%;height:100%;object-fit:cover;display:block;";
      }
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
    ingestPage();
    [].slice.call(document.querySelectorAll("[data-ig-processed]")).forEach(function (a) {
      delete a.dataset.igProcessed;
    });
    btnSort.disabled = true;
    btnSort.textContent = "실행중...";
    phase1Scan(maxPosts).then(fillMissing).then(function () {
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
