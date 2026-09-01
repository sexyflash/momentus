(function () {
  /* MOMENTUS 이미지 수집기 (pinterest-grab)
   * ────────────────────────────────────────────────────────────────
   * 이 파일이 읽기용 원본이다. 배포본은 scripts/build_bookmarklet.py 가
   * 이걸 퍼센트 인코딩해 assets/bookmarklets/pinterest-grab.txt 에 넣는다.
   * .txt 를 손으로 고치지 마라 — 여기 고치고 빌드해라.
   *
   * v2 (2026-09-01)
   *  1) 패널을 Shadow DOM 안으로  — 남의 사이트 CSS 가 우리 그리드를 못 건드린다.
   *     (v1 은 리스트가 겹치고 안에서 스크롤이 안 먹던 문제가 있었다)
   *  2) 접기/펴기 + 헤더 드래그 이동 — 패널이 가린 뒤쪽 이미지를 고를 수 있다.
   *  3) 아무 사이트에서나 동작 — 핀터레스트 전용 처리(originals 승격)는
   *     핀터레스트에서만 켜지고, 그 밖에서는 일반 <img>/배경이미지를 고른다.
   *  4) ZIP 로 한 번에 내려받기 — 라이브러리 없이 클라이언트에서 압축(STORE).
   *
   * ⚠️ 호스트 엘리먼트 id 는 __loud-pc-sidebar 그대로 둔다.
   *    공용 "귀환 갈고리" 꼬리가 이 id 를 찾아 링크를 붙인다. shadow 안에
   *    <slot> 을 둬서 그 링크가 패널 하단에 그대로 렌더된다.
   */
  if (window.__loudPinCollector) { window.__loudPinCollector.destroy(); return; }

  var HOST_ID = '__loud-pc-sidebar';
  var PIN_SEL = '[data-test-id="pin"]';
  var IS_PIN = /(^|\.)pinterest\.[a-z]{2,4}(\.[a-z]{2,3})?$/i.test(location.hostname);
  var POS_KEY = '__loud_pc_pos';
  var SELECTED = new Map();   /* 정규화 URL -> {url, thumb, link, alt, el} */
  var MAX_ITEMS = 300;
  var busy = false;

  /* ───────────── URL 유틸 ───────────── */
  function abs(u) { try { return new URL(u, location.href).href; } catch (e) { return ''; } }
  function originalsUrl(s) { return s.replace(/\/\d+x(?:\d+)?(?:_[A-Za-z]{1,4})?\//, '/originals/'); }
  function cleanUrl(u) { return u.replace(/\/(?:control\d*|v\d*|[0-9a-z]+)\/originals\//, '/originals/'); }
  function normalize(u) {
    if (!u) return '';
    if (IS_PIN && /(^|\.)pinimg\.com\//.test(u)) return cleanUrl(originalsUrl(u));
    return u;
  }
  function bestUrl(img) {
    var ss = img.getAttribute('srcset') || img.getAttribute('data-srcset') || '';
    var best = '', bw = -1;
    ss.split(',').forEach(function (part) {
      var bits = part.trim().split(/\s+/);
      if (!bits[0]) return;
      var d = bits[1] || '';
      var w = /x$/.test(d) ? parseFloat(d) * 2000 : parseFloat(d) || 0;
      if (w >= bw) { bw = w; best = bits[0]; }
    });
    var u = best || img.currentSrc || img.getAttribute('src') ||
            img.getAttribute('data-src') || img.getAttribute('data-original') || '';
    if (/^data:/.test(u)) u = img.currentSrc || img.getAttribute('data-src') || u;
    return abs(u);
  }
  function bgUrl(el) {
    var bg = '';
    try { bg = getComputedStyle(el).backgroundImage || ''; } catch (e) { return ''; }
    var m = bg.match(/url\((['"]?)(.+?)\1\)/);
    if (!m || /^data:/.test(m[2])) return '';
    return abs(m[2]);
  }
  function linkOf(el) {
    var a = el.closest ? el.closest('a[href]') : null;
    return a ? abs(a.getAttribute('href')) : location.href;
  }
  function pinImg(p) { return p.querySelector('img[src*="pinimg.com"]'); }
  function pinLink(p) {
    var a = p.querySelector('a[href^="/pin/"]');
    return a ? abs(a.getAttribute('href')) : location.href;
  }

  /* 클릭 지점에서 "무엇을 담을지" 판정. 못 고르면 null → 페이지 클릭을 안 막는다. */
  function pick(t) {
    if (!t || !t.closest) return null;
    if (IS_PIN) {
      var pin = t.closest(PIN_SEL);
      if (pin) {
        var pi = pinImg(pin);
        if (pi) return { el: pin, url: normalize(pi.src), thumb: pi.src, link: pinLink(pin), alt: pi.alt || '' };
      }
    }
    var img = t.closest('img');
    if (!img) {
      var pic = t.closest('picture');
      if (pic) img = pic.querySelector('img');
    }
    if (img) {
      var u = normalize(bestUrl(img));
      if (u) return { el: img, url: u, thumb: img.currentSrc || img.src || u, link: linkOf(img), alt: img.alt || '' };
    }
    var e = t, n = 0;
    while (e && n < 4) {
      var bu = bgUrl(e);
      if (bu) return { el: e, url: normalize(bu), thumb: bu, link: linkOf(e), alt: '' };
      e = e.parentElement; n++;
    }
    return null;
  }

  /* ───────────── 대상 표시(호스트 문서 스타일 — 최소한만) ───────────── */
  var docStyle = document.createElement('style');
  docStyle.setAttribute('data-loud-pc', '1');
  docStyle.textContent = [
    '.__loud-selected{outline:4px solid #FF0066 !important;outline-offset:-4px !important}',
    '.__loud-hover{outline:3px dashed rgba(255,0,102,.9) !important;outline-offset:-3px !important;cursor:copy !important}',
    PIN_SEL + '.__loud-selected::after{content:"\\2713";position:absolute;top:8px;right:8px;',
    'width:28px;height:28px;background:#FF0066;color:#fff;font-weight:900;font-size:16px;',
    'display:flex;align-items:center;justify-content:center;border-radius:50%;z-index:10;pointer-events:none}'
  ].join('\n');
  (document.head || document.documentElement).appendChild(docStyle);

  /* ───────────── 패널(Shadow DOM) ───────────── */
  var host = document.createElement('div');
  host.id = HOST_ID;
  [['position', 'fixed'], ['top', '16px'], ['right', '16px'], ['left', 'auto'], ['bottom', 'auto'],
   ['z-index', '2147483647'], ['width', 'auto'], ['height', 'auto'], ['margin', '0'], ['padding', '0'],
   ['border', '0'], ['display', 'block'], ['opacity', '1'], ['visibility', 'visible'],
   ['transform', 'none'], ['filter', 'none'], ['float', 'none'], ['overflow', 'visible'],
   ['max-width', 'none'], ['max-height', 'none'], ['min-width', '0'], ['min-height', '0'],
   ['pointer-events', 'auto'], ['background', 'transparent'], ['box-shadow', 'none'],
   ['font-size', '16px'], ['line-height', 'normal'], ['isolation', 'isolate']
  ].forEach(function (kv) { host.style.setProperty(kv[0], kv[1], 'important'); });
  document.body.appendChild(host);
  var root = host.attachShadow({ mode: 'open' });

  var css = [
    '*,*::before,*::after{box-sizing:border-box}',
    '.pnl{width:320px;max-height:calc(100vh - 40px);display:flex;flex-direction:column;',
    ' background:#fff;color:#111;border-radius:14px;overflow:hidden;',
    ' box-shadow:0 16px 48px rgba(0,0,0,.28);',
    ' font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}',
    '.pnl.min{width:auto}',
    '.pnl.min .bd{display:none}',
    '.hd{display:flex;align-items:center;gap:8px;padding:11px 12px;border-bottom:1px solid #eee;',
    ' cursor:grab;user-select:none}',
    '.hd.grab{cursor:grabbing}',
    '.ttl{font-weight:700;font-size:13px;white-space:nowrap}',
    '.cnt{color:#888;font-size:12px;flex:1;white-space:nowrap}',
    '.ic{flex:0 0 26px;width:26px;height:26px;border:0;border-radius:8px;background:#f1f1f1;',
    ' color:#333;font:600 15px/1 inherit;font-family:inherit;cursor:pointer;padding:0}',
    '.ic:hover{background:#e3e3e3}',
    '.bd{display:flex;flex-direction:column;flex:1 1 auto;min-height:0}',
    '.list{flex:1 1 auto;min-height:64px;max-height:44vh;overflow-y:auto;overflow-x:hidden;',
    ' padding:10px;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;align-content:start}',
    '.list.empty{display:block;text-align:center;color:#aaa;font-size:12px;padding:24px 12px;line-height:1.6}',
    '.th{position:relative;aspect-ratio:1;background:#f4f4f4;border-radius:8px;overflow:hidden}',
    '.th img{width:100%;height:100%;object-fit:cover;display:block}',
    '.rm{position:absolute;top:3px;right:3px;width:20px;height:20px;border:0;border-radius:50%;',
    ' background:rgba(0,0,0,.72);color:#fff;font:400 13px/1 inherit;font-family:inherit;cursor:pointer;padding:0}',
    '.ft{display:flex;gap:6px;padding:8px 10px 0}',
    '.ft.last{padding-bottom:10px;border-bottom:1px solid #f0f0f0}',
    '.btn{flex:1;padding:9px 8px;border:0;border-radius:9px;background:#f1f1f1;color:#333;',
    ' font:700 12px/1.2 inherit;font-family:inherit;cursor:pointer;white-space:nowrap}',
    '.btn:hover{background:#e3e3e3}',
    '.btn.pri{background:#FF0066;color:#fff}',
    '.btn.pri:hover{background:#e2005b}',
    '.btn:disabled{background:#f3f3f3;color:#c2c2c2;cursor:not-allowed}',
    '.msg{padding:8px 12px 0;font-size:11px;color:#8a8a8a;line-height:1.5}',
    '.hook{padding:0 12px 10px}',
    '.toast{position:fixed;bottom:32px;left:50%;transform:translateX(-50%);background:#111;color:#fff;',
    ' padding:10px 20px;border-radius:24px;font:13px/1.4 -apple-system,system-ui,sans-serif;',
    ' opacity:0;transition:opacity .2s;pointer-events:none;white-space:nowrap}',
    '.toast.on{opacity:1}'
  ].join('\n');

  root.innerHTML =
    '<style>' + css + '</style>' +
    '<div class="pnl">' +
      '<div class="hd">' +
        '<span class="ttl">📌 라우드 수집기</span>' +
        '<span class="cnt">0개</span>' +
        '<button class="ic mini" title="접기/펼기">–</button>' +
        '<button class="ic cls" title="닫기">×</button>' +
      '</div>' +
      '<div class="bd">' +
        '<div class="list empty"></div>' +
        '<div class="msg"></div>' +
        '<div class="ft">' +
          '<button class="btn all">전부 담기</button>' +
          '<button class="btn clr">비우기</button>' +
        '</div>' +
        '<div class="ft last">' +
          '<button class="btn pri copy">URL 복사</button>' +
          '<button class="btn zip">ZIP 받기</button>' +
        '</div>' +
        '<div class="hook"><slot></slot></div>' +
      '</div>' +
    '</div>' +
    '<div class="toast"></div>';

  var $ = function (s) { return root.querySelector(s); };
  var pnl = $('.pnl'), hd = $('.hd'), list = $('.list'), cnt = $('.cnt'), msg = $('.msg'), toastEl = $('.toast');
  var btnCopy = $('.copy'), btnZip = $('.zip'), btnAll = $('.all'), btnClr = $('.clr');

  function toast(m) {
    toastEl.textContent = m;
    toastEl.classList.add('on');
    clearTimeout(toastEl.__t);
    toastEl.__t = setTimeout(function () { toastEl.classList.remove('on'); }, 1900);
  }
  function say(m) { msg.textContent = m || ''; }

  /* ───────────── 선택 표시 다시 칠하기 ───────────── */
  var paintReq = 0;
  function paint() {
    clearTimeout(paintReq);
    paintReq = setTimeout(applyOverlay, 120);
  }
  function applyOverlay() {
    document.querySelectorAll('.__loud-selected').forEach(function (el) { el.classList.remove('__loud-selected'); });
    if (!SELECTED.size) return;
    SELECTED.forEach(function (it) { if (it.el && it.el.isConnected) it.el.classList.add('__loud-selected'); });
    if (IS_PIN) {
      document.querySelectorAll(PIN_SEL).forEach(function (p) {
        var im = pinImg(p);
        if (im && SELECTED.has(normalize(im.src))) p.classList.add('__loud-selected');
      });
    }
    document.querySelectorAll('img').forEach(function (im) {
      if (IS_PIN && im.closest(PIN_SEL)) return;
      var u = normalize(bestUrl(im));
      if (u && SELECTED.has(u)) im.classList.add('__loud-selected');
    });
  }

  function render() {
    cnt.textContent = SELECTED.size + '개';
    btnCopy.disabled = btnZip.disabled = btnClr.disabled = (SELECTED.size === 0 || busy);
    list.innerHTML = '';
    if (!SELECTED.size) {
      list.classList.add('empty');
      list.textContent = IS_PIN
        ? '핀을 클릭해서 고르세요.'
        : '이미지를 클릭해서 고르세요.';
      return;
    }
    list.classList.remove('empty');
    SELECTED.forEach(function (d, key) {
      var box = document.createElement('div');
      box.className = 'th';
      var im = document.createElement('img');
      im.src = d.thumb || d.url;
      im.alt = '';
      im.referrerPolicy = 'no-referrer';
      box.appendChild(im);
      var rm = document.createElement('button');
      rm.className = 'rm';
      rm.textContent = '×';
      rm.addEventListener('click', function (ev) {
        ev.stopPropagation();
        SELECTED.delete(key);
        applyOverlay(); render();
      });
      box.appendChild(rm);
      list.appendChild(box);
    });
  }

  function add(it) {
    if (!it || !it.url) return false;
    if (SELECTED.has(it.url)) { SELECTED.delete(it.url); return true; }
    if (SELECTED.size >= MAX_ITEMS) { toast('한 번에 ' + MAX_ITEMS + '장까지만 담깁니다.'); return false; }
    SELECTED.set(it.url, it);
    return true;
  }

  /* ───────────── 페이지 클릭 가로채기 ───────────── */
  function inPanel(t) { return t === host || (t && t.getRootNode && t.getRootNode() === root); }

  function onClick(e) {
    if (inPanel(e.target) || e.altKey || e.metaKey || e.ctrlKey) return;
    var it = pick(e.target);
    if (!it) return;               /* 이미지가 아니면 페이지 동작을 막지 않는다 */
    e.preventDefault();
    e.stopPropagation();
    if (e.stopImmediatePropagation) e.stopImmediatePropagation();
    if (add(it)) { applyOverlay(); render(); }
  }
  function onDown(e) {
    if (inPanel(e.target) || e.altKey || e.metaKey || e.ctrlKey) return;
    if (pick(e.target) && e.stopImmediatePropagation) e.stopImmediatePropagation();
  }
  var hoverEl = null, hoverRaf = 0;
  function onMove(e) {
    if (hoverRaf) return;
    hoverRaf = requestAnimationFrame(function () {
      hoverRaf = 0;
      if (inPanel(e.target)) return;
      var it = pick(e.target);
      var el = it ? it.el : null;
      if (el === hoverEl) return;
      if (hoverEl) hoverEl.classList.remove('__loud-hover');
      hoverEl = el;
      if (hoverEl && !hoverEl.classList.contains('__loud-selected')) hoverEl.classList.add('__loud-hover');
    });
  }
  function onKey(e) {
    if (e.key !== 'Escape') return;
    var a = document.activeElement;
    if (a && /^(INPUT|TEXTAREA)$/.test(a.tagName)) return;
    window.__loudPinCollector.destroy();
  }
  document.addEventListener('click', onClick, true);
  document.addEventListener('mousedown', onDown, true);
  document.addEventListener('mousemove', onMove, true);
  document.addEventListener('keydown', onKey, true);

  var mo = new MutationObserver(paint);
  mo.observe(document.body, { childList: true, subtree: true });

  /* ───────────── 화면 속 이미지 전부 담기 ───────────── */
  btnAll.addEventListener('click', function () {
    var before = SELECTED.size, n = 0;
    if (IS_PIN) {
      document.querySelectorAll(PIN_SEL).forEach(function (p) {
        var im = pinImg(p);
        if (!im) return;
        var u = normalize(im.src);
        if (u && !SELECTED.has(u) && SELECTED.size < MAX_ITEMS) {
          SELECTED.set(u, { el: p, url: u, thumb: im.src, link: pinLink(p), alt: im.alt || '' }); n++;
        }
      });
    }
    document.querySelectorAll('img').forEach(function (im) {
      if (IS_PIN && im.closest(PIN_SEL)) return;
      /* 아이콘·픽셀·로고를 거르는 기준은 "실제로 받게 될 크기"(naturalWidth)다.
         화면에 작게 깔린 썸네일 그리드도 원본은 크다 — 표시 크기만 보면 다 떨어진다. */
      var r = im.getBoundingClientRect();
      if (r.width < 80 || r.height < 80) return;
      if ((im.naturalWidth || 0) < 200 && r.width < 200) return;
      var u = normalize(bestUrl(im));
      if (u && !SELECTED.has(u) && SELECTED.size < MAX_ITEMS) {
        SELECTED.set(u, { el: im, url: u, thumb: im.currentSrc || im.src || u, link: linkOf(im), alt: im.alt || '' }); n++;
      }
    });
    applyOverlay(); render();
    say(n ? (n + '장 추가했습니다. (스크롤 후 다시 누르면 더 담깁니다)')
             : '추가할 새 이미지가 없습니다.');
    if (before === SELECTED.size && !n) toast('새로 담을 게 없습니다.');
  });

  btnClr.addEventListener('click', function () {
    SELECTED.clear(); applyOverlay(); render(); say('');
  });

  /* ───────────── URL 복사 ───────────── */
  btnCopy.addEventListener('click', function () {
    var urls = [];
    SELECTED.forEach(function (d) { urls.push(d.url); });
    if (!urls.length) return;
    var text = urls.join('\n');
    navigator.clipboard.writeText(text).then(function () {
      toast(urls.length + '개 URL 복사됨');
    }, function () {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) {}
      ta.remove();
      toast(ok ? (urls.length + '개 URL 복사됨') : '복사 실패');
    });
  });

  /* ───────────── ZIP (라이브러리 없이 STORE 압축) ───────────── */
  var CRCT = null;
  function crc32(b) {
    if (!CRCT) {
      CRCT = new Uint32Array(256);
      for (var n = 0; n < 256; n++) {
        var c = n;
        for (var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
        CRCT[n] = c >>> 0;
      }
    }
    var crc = 0xFFFFFFFF;
    for (var i = 0; i < b.length; i++) crc = (crc >>> 8) ^ CRCT[(crc ^ b[i]) & 0xFF];
    return (crc ^ 0xFFFFFFFF) >>> 0;
  }
  function zipStore(files) {
    var parts = [], central = [], off = 0, d = new Date();
    var dt = (((d.getFullYear() - 1980) & 0x7F) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    var tm = (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1);
    var enc = new TextEncoder();
    files.forEach(function (f) {
      var name = enc.encode(f.name), data = f.data, crc = crc32(data);
      var lh = new DataView(new ArrayBuffer(30));
      lh.setUint32(0, 0x04034B50, true); lh.setUint16(4, 20, true); lh.setUint16(6, 0, true);
      lh.setUint16(8, 0, true); lh.setUint16(10, tm, true); lh.setUint16(12, dt, true);
      lh.setUint32(14, crc, true); lh.setUint32(18, data.length, true); lh.setUint32(22, data.length, true);
      lh.setUint16(26, name.length, true); lh.setUint16(28, 0, true);
      parts.push(new Uint8Array(lh.buffer), name, data);
      var ch = new DataView(new ArrayBuffer(46));
      ch.setUint32(0, 0x02014B50, true); ch.setUint16(4, 20, true); ch.setUint16(6, 20, true);
      ch.setUint16(8, 0, true); ch.setUint16(10, 0, true); ch.setUint16(12, tm, true);
      ch.setUint16(14, dt, true); ch.setUint32(16, crc, true); ch.setUint32(20, data.length, true);
      ch.setUint32(24, data.length, true); ch.setUint16(28, name.length, true);
      ch.setUint16(30, 0, true); ch.setUint16(32, 0, true); ch.setUint16(34, 0, true);
      ch.setUint16(36, 0, true); ch.setUint32(38, 0, true); ch.setUint32(42, off, true);
      central.push(new Uint8Array(ch.buffer), name);
      off += 30 + name.length + data.length;
    });
    var csize = central.reduce(function (a, u) { return a + u.length; }, 0);
    var eo = new DataView(new ArrayBuffer(22));
    eo.setUint32(0, 0x06054B50, true); eo.setUint16(4, 0, true); eo.setUint16(6, 0, true);
    eo.setUint16(8, files.length, true); eo.setUint16(10, files.length, true);
    eo.setUint32(12, csize, true); eo.setUint32(16, off, true); eo.setUint16(20, 0, true);
    return new Blob(parts.concat(central, [new Uint8Array(eo.buffer)]), { type: 'application/zip' });
  }
  function extOf(url, type) {
    if (/png/.test(type)) return 'png';
    if (/webp/.test(type)) return 'webp';
    if (/gif/.test(type)) return 'gif';
    if (/jpe?g/.test(type)) return 'jpg';
    var m = url.split('?')[0].match(/\.([a-zA-Z0-9]{2,4})$/);
    return m ? m[1].toLowerCase() : 'jpg';
  }
  function viaCanvas(url) {
    return new Promise(function (res, rej) {
      var im = new Image();
      im.crossOrigin = 'anonymous';
      im.referrerPolicy = 'no-referrer';
      im.onload = function () {
        try {
          var c = document.createElement('canvas');
          c.width = im.naturalWidth; c.height = im.naturalHeight;
          c.getContext('2d').drawImage(im, 0, 0);
          c.toBlob(function (b) {
            if (!b) { rej(0); return; }
            b.arrayBuffer().then(function (ab) { res({ bytes: new Uint8Array(ab), type: 'image/png' }); }, rej);
          }, 'image/png');
        } catch (e) { rej(e); }
      };
      im.onerror = function () { rej(0); };
      im.src = url;
    });
  }
  function grab(url) {
    return fetch(url, { mode: 'cors', credentials: 'omit', referrerPolicy: 'no-referrer' })
      .then(function (r) {
        if (!r.ok) throw 0;
        return r.arrayBuffer().then(function (ab) {
          if (!ab.byteLength) throw 0;
          return { bytes: new Uint8Array(ab), type: r.headers.get('content-type') || '' };
        });
      })
      .catch(function () { return viaCanvas(url); })
      .catch(function () { return null; });
  }

  btnZip.addEventListener('click', function () {
    if (busy || !SELECTED.size) return;
    busy = true; render();
    var items = [];
    SELECTED.forEach(function (d) { items.push(d); });
    var files = [], done = 0, fail = 0, idx = 0;
    var lines = items.map(function (d, i) { return (i + 1) + '\t' + d.url + '\t' + (d.link || ''); });

    function tick() { say('받는 중 ' + done + ' / ' + items.length + (fail ? ('  (실패 ' + fail + ')') : '')); }
    tick();

    function next() {
      if (idx >= items.length) return Promise.resolve();
      var i = idx++, d = items[i];
      /* originals 승격이 항상 되는 건 아니다 — 핀에 따라 403 이 온다(실측).
         그때 손을 놓으면 그 장은 통째로 못 받는다. 큰 것 → 중간 → 화면에 보이던 것 순으로
         내려가며 받는다. 주소를 복사하는 쪽은 v1 그대로 originals 를 준다. */
      var cand = [d.url];
      if (d.thumb && d.thumb !== d.url) {
        var mid = d.thumb.replace(/\/\d+x(?:\d+)?(?:_[A-Za-z]{1,4})?\//, '/736x/');
        if (cand.indexOf(mid) < 0) cand.push(mid);
        if (cand.indexOf(d.thumb) < 0) cand.push(d.thumb);
      }
      return cand.reduce(function (chain, u) {
        return chain.then(function (got) { return got || grab(u); });
      }, Promise.resolve(null)).then(function (r) {
        done++;
        if (r) {
          var base = (d.url.split('?')[0].split('/').pop() || 'image').replace(/[^A-Za-z0-9._-]/g, '');
          base = base.replace(/\.[A-Za-z0-9]{2,4}$/, '').slice(0, 40) || 'image';
          files.push({ name: String(i + 1).padStart(3, '0') + '_' + base + '.' + extOf(d.url, r.type), data: r.bytes });
        } else { fail++; }
        tick();
        return next();
      });
    }

    var lanes = [];
    for (var l = 0; l < 4; l++) lanes.push(next());
    Promise.all(lanes).then(function () {
      files.push({ name: 'urls.txt', data: new TextEncoder().encode(lines.join('\n') + '\n') });
      var blob = zipStore(files);
      var u = URL.createObjectURL(blob);
      var a = document.createElement('a');
      var s = new Date(), p = function (x) { return String(x).padStart(2, '0'); };
      a.href = u;
      a.download = 'moment-images-' + s.getFullYear() + p(s.getMonth() + 1) + p(s.getDate()) + '-' + p(s.getHours()) + p(s.getMinutes()) + '.zip';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(u); }, 60000);
      busy = false; render();
      var okn = files.length - 1;
      say(fail
        ? (okn + '장 받았습니다. ' + fail + '장은 사이트가 막아 못 받았고, 그 주소는 urls.txt 에 들어 있습니다.')
        : (okn + '장 받았습니다. (urls.txt 포함)'));
      toast('ZIP 다운로드 시작');
    }, function () {
      busy = false; render();
      say('ZIP 생성에 실패했습니다. URL 복사는 그대로 됩니다.');
    });
  });

  /* ───────────── 접기 / 드래그 / 닫기 ───────────── */
  function savePos() {
    try {
      localStorage.setItem(POS_KEY, JSON.stringify({
        l: host.style.left, t: host.style.top, r: host.style.right, m: pnl.classList.contains('min') ? 1 : 0
      }));
    } catch (e) {}
  }
  function loadPos() {
    var v = null;
    try { v = JSON.parse(localStorage.getItem(POS_KEY) || 'null'); } catch (e) {}
    if (!v) return;
    if (v.l && v.l !== 'auto') {
      host.style.setProperty('left', v.l, 'important');
      host.style.setProperty('right', 'auto', 'important');
    }
    if (v.t) host.style.setProperty('top', v.t, 'important');
    if (v.m) pnl.classList.add('min');
  }

  $('.mini').addEventListener('click', function () { pnl.classList.toggle('min'); savePos(); });
  $('.cls').addEventListener('click', function () { window.__loudPinCollector.destroy(); });

  var drag = null;
  hd.addEventListener('mousedown', function (e) {
    if (e.target.closest('.ic')) return;
    var r = host.getBoundingClientRect();
    drag = { dx: e.clientX - r.left, dy: e.clientY - r.top, w: r.width, h: r.height };
    hd.classList.add('grab');
    e.preventDefault();
  });
  function dragMove(e) {
    if (!drag) return;
    var x = Math.max(4, Math.min(window.innerWidth - drag.w - 4, e.clientX - drag.dx));
    var y = Math.max(4, Math.min(window.innerHeight - 40, e.clientY - drag.dy));
    host.style.setProperty('left', x + 'px', 'important');
    host.style.setProperty('top', y + 'px', 'important');
    host.style.setProperty('right', 'auto', 'important');
  }
  function dragUp() {
    if (!drag) return;
    drag = null; hd.classList.remove('grab'); savePos();
  }
  window.addEventListener('mousemove', dragMove, true);
  window.addEventListener('mouseup', dragUp, true);

  loadPos();
  applyOverlay();
  render();
  say(IS_PIN
    ? '핀을 클릭해 담으세요. 패널은 제목줄을 잡고 옮길 수 있습니다.'
    : '이 페이지의 아무 이미지나 클릭하세요. Alt+클릭은 원래 동작입니다.');
  toast('수집기 활성화');

  window.__loudPinCollector = {
    destroy: function () {
      try { mo.disconnect(); } catch (e) {}
      clearTimeout(paintReq);
      document.removeEventListener('click', onClick, true);
      document.removeEventListener('mousedown', onDown, true);
      document.removeEventListener('mousemove', onMove, true);
      document.removeEventListener('keydown', onKey, true);
      window.removeEventListener('mousemove', dragMove, true);
      window.removeEventListener('mouseup', dragUp, true);
      document.querySelectorAll('.__loud-selected,.__loud-hover').forEach(function (el) {
        el.classList.remove('__loud-selected'); el.classList.remove('__loud-hover');
      });
      host.remove();
      docStyle.remove();
      delete window.__loudPinCollector;
    }
  };
})();
