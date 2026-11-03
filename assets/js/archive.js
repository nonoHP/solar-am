/* ==========================================================
   Solar AM Notes - 原本資料アーカイブ (archive.html) 専用スクリプト
   ・全598件の原本PDF・資料の分類・検索・アコーディオン表示
   ・大分類・発行機関・キーワードリアルタイム高速絞り込み
   ・Google Drive原本連携
   ========================================================== */
(function () {
  "use strict";

  var data = window.SOLAR_ARCHIVE_DATA;
  if (!data || !data.items) {
    var c = document.getElementById("archive-container");
    if (c) c.innerHTML = '<p style="color:var(--text-sub);padding:30px;text-align:center;">原本アーカイブデータが見つかりませんでした。</p>';
    return;
  }

  var rawItems = data.items || [];
  var searchInput = document.getElementById("archive-search");
  var catChips = document.querySelectorAll("#cat-chips .chip");
  var orgChips = document.querySelectorAll("#org-chips .chip");
  var countEl = document.getElementById("archive-count");
  var container = document.getElementById("archive-container");
  var emptyEl = document.getElementById("archive-empty");
  var btnExpandAll = document.getElementById("btn-expand-all");
  var btnCollapseAll = document.getElementById("btn-collapse-all");

  var currentCat = "all";
  var currentOrg = "all";
  var currentQuery = "";

  // URLパラメータから初期フィルタを取得
  var urlParams = new URLSearchParams(window.location.search);
  var initCat = urlParams.get("cat");
  var initOrg = urlParams.get("org");
  var initQ = urlParams.get("q");

  if (initCat) {
    currentCat = initCat;
    catChips.forEach(function (b) {
      if (b.getAttribute("data-cat") === initCat) b.classList.add("active");
      else b.classList.remove("active");
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

  function render() {
    var q = currentQuery.trim().toLowerCase();

    // フィルタリング
    var filtered = rawItems.filter(function (it) {
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
        if (!matchTitle && !matchOrg && !matchFolder) return false;
      }
      return true;
    });

    // 件数表示
    if (countEl) {
      countEl.textContent = "表示中: " + filtered.length + "件 （全" + rawItems.length + "件中）";
    }

    if (!filtered.length) {
      container.innerHTML = "";
      if (emptyEl) emptyEl.style.display = "block";
      return;
    }
    if (emptyEl) emptyEl.style.display = "none";

    // フォルダごとにグループ化
    var groups = {};
    var groupOrder = [];

    filtered.forEach(function (it) {
      var folderKey = it.folder;
      if (!groups[folderKey]) {
        groups[folderKey] = {
          catCode: it.cat_code,
          catName: it.cat_name,
          subcat: it.subcat,
          folder: folderKey,
          items: []
        };
        groupOrder.push(folderKey);
      }
      groups[folderKey].items.push(it);
    });

    var shouldExpand = q.length > 0 || groupOrder.length <= 4;
    var html = "";

    groupOrder.forEach(function (folderKey) {
      var grp = groups[folderKey];
      var openClass = shouldExpand ? " open" : "";

      html += '<div class="archive-folder-group' + openClass + '" data-folder="' + escapeHtml(folderKey) + '">';
      html += '  <div class="archive-folder-header">';
      html += '    <div class="archive-folder-title-wrap">';
      html += '      <span class="archive-folder-icon">📂</span>';
      html += '      <span class="archive-folder-name">' + escapeHtml(grp.subcat) + '</span>';
      html += '      <span class="archive-folder-count">' + grp.items.length + '件</span>';
      html += '    </div>';
      html += '    <svg class="archive-folder-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>';
      html += '  </div>';

      html += '  <div class="archive-file-list" style="' + (shouldExpand ? "" : "display:none;") + '">';

      grp.items.forEach(function (it) {
        var typeClass = "pdf";
        if (it.type === "音声") typeClass = "audio";
        else if (it.type === "PPT" || it.type === "スライド") typeClass = "slide";

        // Google Drive 検索URL（該当ファイル名でDrive内を即座に開く）
        var driveSearchUrl = "https://drive.google.com/drive/search?q=" + encodeURIComponent('"' + it.title + '"');

        html += '<a class="archive-file-card" href="' + escapeHtml(driveSearchUrl) + '" target="_blank" rel="noopener noreferrer">';
        html += '  <div>';
        html += '    <div class="archive-file-top">';
        html += '      <span class="archive-file-type-badge ' + typeClass + '">' + escapeHtml(it.type) + '</span>';
        html += '      <span class="archive-file-org-badge" title="' + escapeHtml(it.org) + '">' + escapeHtml(it.org) + '</span>';
        html += '      <span class="archive-file-size">' + escapeHtml(it.size) + '</span>';
        html += '    </div>';
        html += '    <h3 class="archive-file-title" title="' + escapeHtml(it.title) + '">' + escapeHtml(it.title) + '</h3>';
        html += '  </div>';
        html += '  <div class="archive-file-foot">';
        html += '    <span>' + escapeHtml(it.subcat.substring(0, 24)) + '</span>';
        html += '    <span class="archive-file-action">Drive原本で開く <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg></span>';
        html += '  </div>';
        html += '</a>';
      });

      html += '  </div>';
      html += '</div>';
    });

    container.innerHTML = html;

    // アコーディオンの開閉クリックイベントを付与
    var folderHeaders = container.querySelectorAll(".archive-folder-header");
    folderHeaders.forEach(function (hdr) {
      hdr.addEventListener("click", function () {
        var parent = hdr.parentElement;
        var list = parent.querySelector(".archive-file-list");
        if (parent.classList.contains("open")) {
          parent.classList.remove("open");
          if (list) list.style.display = "none";
        } else {
          parent.classList.add("open");
          if (list) list.style.display = "grid";
        }
      });
    });
  }

  // 大分類チップ
  catChips.forEach(function (btn) {
    btn.addEventListener("click", function () {
      catChips.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      currentCat = btn.getAttribute("data-cat");
      render();
    });
  });

  // 発行機関チップ
  orgChips.forEach(function (btn) {
    btn.addEventListener("click", function () {
      orgChips.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      currentOrg = btn.getAttribute("data-org");
      render();
    });
  });

  // 検索入力（ディバウンス）
  var debounceTimer = null;
  if (searchInput) {
    searchInput.addEventListener("input", function (e) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () {
        currentQuery = e.target.value;
        render();
      }, 150);
    });
  }

  // すべて展開 / 折りたたみ
  if (btnExpandAll) {
    btnExpandAll.addEventListener("click", function () {
      var groups = container.querySelectorAll(".archive-folder-group");
      groups.forEach(function (g) {
        g.classList.add("open");
        var list = g.querySelector(".archive-file-list");
        if (list) list.style.display = "grid";
      });
    });
  }
  if (btnCollapseAll) {
    btnCollapseAll.addEventListener("click", function () {
      var groups = container.querySelectorAll(".archive-folder-group");
      groups.forEach(function (g) {
        g.classList.remove("open");
        var list = g.querySelector(".archive-file-list");
        if (list) list.style.display = "none";
      });
    });
  }

  // 初回描画
  render();
})();
