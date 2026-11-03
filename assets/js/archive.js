/* ==========================================================
   Solar AM Notes - 官公庁原本・専門PDFナレッジライブラリ (archive.html)
   ・全598件の原本PDF・資料の分類・高速検索・モーダル詳細閲覧
   ・「開けない」を解消：確実なWeb共有URL＋公式PDF直接URL＋サイト内解説
   ・Notion/Stripe風の洗練されたデジタルライブラリUI
   ========================================================== */
(function () {
  "use strict";

  var data = window.SOLAR_ARCHIVE_DATA;
  if (!data || !data.items) {
    console.error("Archive data not loaded.");
    return;
  }

  var rawItems = data.items || [];
  var searchInput = document.getElementById("archive-search");
  var catCards = document.querySelectorAll(".archive-cat-card");
  var orgChips = document.querySelectorAll("#org-chips .chip");
  var countEl = document.getElementById("archive-count");
  var container = document.getElementById("archive-container");
  var emptyEl = document.getElementById("archive-empty");
  var loadMoreContainer = document.getElementById("archive-load-more-wrap");
  var btnLoadMore = document.getElementById("btn-load-more");
  var modalOverlay = document.getElementById("doc-modal-overlay");
  var modalClose = document.getElementById("doc-modal-close");
  var viewButtons = document.querySelectorAll(".archive-view-btn");

  var currentCat = "all";
  var currentOrg = "all";
  var currentQuery = "";
  var currentView = "cards"; // "cards" or "folders"
  var displayedCount = 24;
  var PAGE_STEP = 24;

  // URLパラメータの反映
  var urlParams = new URLSearchParams(window.location.search);
  var initCat = urlParams.get("cat");
  var initOrg = urlParams.get("org");
  var initQ = urlParams.get("q");

  if (initCat) {
    currentCat = initCat;
    catCards.forEach(function (c) {
      if (c.getAttribute("data-cat") === initCat) c.classList.add("active");
      else c.classList.remove("active");
    });
  }
  if (initOrg) {
    currentOrg = initOrg;
    orgChips.forEach(function (b) {
      if (b.getAttribute("data-org") === initOrg) b.classList.add("active");
      else b.classList.remove("active");
    });
  }
  if (initQ) {
    currentQuery = initQ;
    if (searchInput) searchInput.value = initQ;
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function getOrgClass(org) {
    if (!org) return "";
    if (org.indexOf("OCCTO") !== -1) return "occto";
    if (org.indexOf("TDGC") !== -1) return "tdgc";
    if (org.indexOf("環境省") !== -1) return "env";
    if (org.indexOf("JPEA") !== -1) return "jpea";
    if (org.indexOf("IEEJ") !== -1) return "ieej";
    if (org.indexOf("気候ネットワーク") !== -1) return "kiko";
    if (org.indexOf("経産省") !== -1) return "meti";
    return "";
  }

  // フィルタリング処理
  function getFilteredItems() {
    var q = currentQuery.trim().toLowerCase();
    return rawItems.filter(function (it) {
      if (currentCat !== "all" && it.cat_code !== currentCat) {
        return false;
      }
      if (currentOrg !== "all" && it.org !== currentOrg) {
        return false;
      }
      if (q) {
        var matchTitle = it.title.toLowerCase().indexOf(q) !== -1;
        var matchOrg = it.org.toLowerCase().indexOf(q) !== -1;
        var matchFolder = it.folder.toLowerCase().indexOf(q) !== -1;
        var matchSummary = it.summary && it.summary.toLowerCase().indexOf(q) !== -1;
        var matchTags = it.tags && it.tags.some(function (t) { return t.toLowerCase().indexOf(q) !== -1; });
        if (!matchTitle && !matchOrg && !matchFolder && !matchSummary && !matchTags) return false;
      }
      return true;
    });
  }

  // モーダルを開く
  function openModal(item) {
    if (!modalOverlay) return;
    var orgClass = getOrgClass(item.org);

    document.getElementById("modal-org").className = "doc-org-tag " + orgClass;
    document.getElementById("modal-org").textContent = item.org;
    document.getElementById("modal-type").textContent = item.type;
    document.getElementById("modal-size").textContent = item.size;
    document.getElementById("modal-title").textContent = item.title;
    document.getElementById("modal-summary").textContent = item.summary || "アセットマネジメント実務における公式一次情報原本です。";
    document.getElementById("modal-folder").textContent = item.folder;

    // タグ
    var tagsHtml = "";
    (item.tags || []).forEach(function (t) {
      tagsHtml += '<span class="doc-tag-pill">' + escapeHtml(t) + '</span>';
    });
    document.getElementById("modal-tags").innerHTML = tagsHtml;

    // ボタン設定
    var btnDirect = document.getElementById("modal-btn-direct");
    if (item.direct_url) {
      btnDirect.style.display = "flex";
      btnDirect.href = item.direct_url;
      btnDirect.innerHTML = '📄 公式配信元で原本PDFを開く ↗ <small style="opacity:0.8;font-size:11px;font-weight:normal;">(公的直接リンク)</small>';
    } else {
      btnDirect.style.display = "none";
    }

    var btnDrive = document.getElementById("modal-btn-drive");
    btnDrive.href = item.drive_url || "https://drive.google.com/drive/folders/1DrJ6fb1ogmJ0mTASIJPvzN9IL0IlwR_Z?usp=sharing";

    var btnNote = document.getElementById("modal-btn-note");
    if (item.related_note) {
      btnNote.style.display = "inline-flex";
      btnNote.href = item.related_note;
    } else {
      btnNote.style.display = "none";
    }

    modalOverlay.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  // モーダルを閉じる
  function closeModal() {
    if (!modalOverlay) return;
    modalOverlay.classList.remove("active");
    document.body.style.overflow = "";
  }

  if (modalClose) modalClose.addEventListener("click", closeModal);
  if (modalOverlay) {
    modalOverlay.addEventListener("click", function (e) {
      if (e.target === modalOverlay) closeModal();
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && modalOverlay && modalOverlay.classList.contains("active")) {
      closeModal();
    }
  });

  // レンダリング
  function render() {
    var filtered = getFilteredItems();

    // 件数更新
    if (countEl) {
      countEl.innerHTML = '表示中: <strong>' + Math.min(displayedCount, filtered.length) + '件</strong> <span style="color:var(--text-mute);font-weight:normal;">/ 該当 ' + filtered.length + '件（全' + rawItems.length + '件）</span>';
    }

    if (!filtered.length) {
      container.innerHTML = "";
      if (emptyEl) emptyEl.style.display = "block";
      if (loadMoreContainer) loadMoreContainer.style.display = "none";
      return;
    }
    if (emptyEl) emptyEl.style.display = "none";

    if (currentView === "cards") {
      // ===== 1. カードグリッド表示（モダン） =====
      var sliceItems = filtered.slice(0, displayedCount);
      var html = '<div class="doc-cards-grid">';

      sliceItems.forEach(function (it) {
        var orgClass = getOrgClass(it.org);
        var typeClass = it.type === "PDF" ? "pdf" : (it.type === "音声" ? "audio" : "slide");

        html += '<div class="doc-item-card" data-id="' + it.id + '">';
        html += '  <div>';
        html += '    <div class="doc-card-meta">';
        html += '      <span class="doc-org-tag ' + orgClass + '">' + escapeHtml(it.org) + '</span>';
        html += '      <span class="archive-file-size">' + escapeHtml(it.size) + '</span>';
        html += '    </div>';
        html += '    <h3 class="doc-card-title">' + escapeHtml(it.title) + '</h3>';
        html += '    <p class="doc-card-summary">' + escapeHtml(it.summary) + '</p>';
        html += '    <div class="doc-card-tags">';
        (it.tags || []).forEach(function (t) {
          html += '    <span class="doc-tag-pill">' + escapeHtml(t) + '</span>';
        });
        html += '    </div>';
        html += '  </div>';
        html += '  <div class="doc-card-foot">';
        html += '    <span class="archive-file-type-badge ' + typeClass + '">' + escapeHtml(it.type) + '</span>';
        html += '    <span class="doc-view-btn">詳細・原本を開く ↗</span>';
        html += '  </div>';
        html += '</div>';
      });
      html += '</div>';

      container.innerHTML = html;

      // 「もっと読み込む」ボタンの制御
      if (loadMoreContainer) {
        if (displayedCount < filtered.length) {
          loadMoreContainer.style.display = "block";
          if (btnLoadMore) {
            btnLoadMore.textContent = "さらに資料を読み込む（残り " + (filtered.length - displayedCount) + " 件）↓";
          }
        } else {
          loadMoreContainer.style.display = "none";
        }
      }

      // カードクリックでモーダル
      var cards = container.querySelectorAll(".doc-item-card");
      cards.forEach(function (card) {
        card.addEventListener("click", function () {
          var id = parseInt(card.getAttribute("data-id"), 10);
          var it = rawItems.find(function (x) { return x.id === id; });
          if (it) openModal(it);
        });
      });

    } else {
      // ===== 2. フォルダ階層アコーディオン表示 =====
      if (loadMoreContainer) loadMoreContainer.style.display = "none";

      var groups = {};
      var groupOrder = [];

      filtered.forEach(function (it) {
        var folderKey = it.folder;
        if (!groups[folderKey]) {
          groups[folderKey] = {
            subcat: it.subcat,
            folder: folderKey,
            items: []
          };
          groupOrder.push(folderKey);
        }
        groups[folderKey].items.push(it);
      });

      var html = "";
      groupOrder.forEach(function (folderKey) {
        var grp = groups[folderKey];
        html += '<div class="archive-folder-group open">';
        html += '  <div class="archive-folder-header">';
        html += '    <div class="archive-folder-title-wrap">';
        html += '      <span class="archive-folder-icon">📂</span>';
        html += '      <span class="archive-folder-name">' + escapeHtml(grp.subcat) + '</span>';
        html += '      <span class="archive-folder-count">' + grp.items.length + '件</span>';
        html += '    </div>';
        html += '    <svg class="archive-folder-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>';
        html += '  </div>';
        html += '  <div class="archive-file-list">';

        grp.items.forEach(function (it) {
          var orgClass = getOrgClass(it.org);
          var typeClass = it.type === "PDF" ? "pdf" : (it.type === "音声" ? "audio" : "slide");

          html += '<div class="archive-file-card" data-id="' + it.id + '" style="cursor:pointer;">';
          html += '  <div>';
          html += '    <div class="archive-file-top">';
          html += '      <span class="archive-file-type-badge ' + typeClass + '">' + escapeHtml(it.type) + '</span>';
          html += '      <span class="doc-org-tag ' + orgClass + '">' + escapeHtml(it.org) + '</span>';
          html += '      <span class="archive-file-size">' + escapeHtml(it.size) + '</span>';
          html += '    </div>';
          html += '    <h3 class="archive-file-title">' + escapeHtml(it.title) + '</h3>';
          html += '    <p style="font-size:11.5px;color:var(--text-sub);margin:0 0 6px;line-height:1.4;">' + escapeHtml(it.summary) + '</p>';
          html += '  </div>';
          html += '  <div class="archive-file-foot">';
          html += '    <span>' + escapeHtml(it.size) + '</span>';
          html += '    <span class="archive-file-action">詳細・原本 ↗</span>';
          html += '  </div>';
          html += '</div>';
        });

        html += '  </div>';
        html += '</div>';
      });

      container.innerHTML = html;

      // フォルダ開閉
      var headers = container.querySelectorAll(".archive-folder-header");
      headers.forEach(function (hdr) {
        hdr.addEventListener("click", function () {
          var p = hdr.parentElement;
          var l = p.querySelector(".archive-file-list");
          if (p.classList.contains("open")) {
            p.classList.remove("open");
            if (l) l.style.display = "none";
          } else {
            p.classList.add("open");
            if (l) l.style.display = "grid";
          }
        });
      });

      // アコーディオンカードクリックでモーダル
      var fCards = container.querySelectorAll(".archive-file-card");
      fCards.forEach(function (card) {
        card.addEventListener("click", function () {
          var id = parseInt(card.getAttribute("data-id"), 10);
          var it = rawItems.find(function (x) { return x.id === id; });
          if (it) openModal(it);
        });
      });
    }
  }

  // 大分類カードクリック
  catCards.forEach(function (card) {
    card.addEventListener("click", function () {
      var cat = card.getAttribute("data-cat");
      if (currentCat === cat) {
        currentCat = "all";
        catCards.forEach(function (c) { c.classList.remove("active"); });
      } else {
        currentCat = cat;
        catCards.forEach(function (c) { c.classList.remove("active"); });
        card.classList.add("active");
      }
      displayedCount = PAGE_STEP;
      render();
    });
  });

  // 発行機関チップ
  orgChips.forEach(function (btn) {
    btn.addEventListener("click", function () {
      orgChips.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      currentOrg = btn.getAttribute("data-org");
      displayedCount = PAGE_STEP;
      render();
    });
  });

  // 検索入力
  var debounceTimer = null;
  if (searchInput) {
    searchInput.addEventListener("input", function (e) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () {
        currentQuery = e.target.value;
        displayedCount = PAGE_STEP;
        render();
      }, 150);
    });
  }

  // 表示切替スイッチ
  viewButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      viewButtons.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      currentView = btn.getAttribute("data-view");
      render();
    });
  });

  // もっと読み込むボタン
  if (btnLoadMore) {
    btnLoadMore.addEventListener("click", function () {
      displayedCount += PAGE_STEP;
      render();
    });
  }

  // ピックアップカードのクリックイベント
  var featCards = document.querySelectorAll(".featured-doc-card");
  featCards.forEach(function (fc) {
    fc.addEventListener("click", function () {
      var id = parseInt(fc.getAttribute("data-id"), 10);
      var it = rawItems.find(function (x) { return x.id === id; });
      if (it) openModal(it);
    });
  });

  // 初回描画
  render();
})();
