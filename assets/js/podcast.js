/* ==========================================================
   Solar AM Notes - AI音声解説（ポッドキャスト）スタジオ用スクリプト
   ========================================================== */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var grid = document.getElementById("podcast-grid");
    var filterContainer = document.getElementById("podcast-filters");
    var searchInput = document.getElementById("podcast-search");
    var countBadge = document.getElementById("podcast-count");

    // 固定プレイヤー要素
    var stickyPlayer = document.getElementById("podcast-sticky-player");
    var playingTitle = document.getElementById("podcast-playing-title");
    var playerIframe = document.getElementById("podcast-player-iframe");
    var playerClose = document.getElementById("podcast-player-close");

    if (!grid || typeof PODCAST_DATA === "undefined") return;

    var currentCategory = "all";
    var currentKeyword = "";
    var currentPlayingId = null;

    // カテゴリ一覧
    var categories = ["all", "FIP・蓄電池・市場取引", "ファイナンス・契約", "法令・保安・地域共生", "廃棄・リサイクル・環境", "設備設計・LCOE", "実務全般"];

    // フィルターボタン描画
    if (filterContainer) {
      var filterHtml = categories.map(function (cat) {
        var label = cat === "all" ? "すべて (" + PODCAST_DATA.length + ")" : cat;
        return '<button class="chip' + (cat === "all" ? ' active' : '') + '" data-cat="' + cat + '">' + label + '</button>';
      }).join("");
      filterContainer.innerHTML = filterHtml;

      filterContainer.addEventListener("click", function (e) {
        var btn = e.target.closest(".chip");
        if (!btn) return;
        filterContainer.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("active"); });
        btn.classList.add("active");
        currentCategory = btn.getAttribute("data-cat");
        renderTracks();
      });
    }

    // 検索入力イベント
    if (searchInput) {
      searchInput.addEventListener("input", function (e) {
        currentKeyword = e.target.value.toLowerCase().trim();
        renderTracks();
      });
    }

    // カード描画関数
    function renderTracks() {
      var filtered = PODCAST_DATA.filter(function (t) {
        var matchCat = currentCategory === "all" || t.category === currentCategory;
        var matchKw = !currentKeyword ||
          t.title.toLowerCase().indexOf(currentKeyword) >= 0 ||
          t.summary.toLowerCase().indexOf(currentKeyword) >= 0 ||
          t.key_points.some(function (p) { return p.toLowerCase().indexOf(currentKeyword) >= 0; });
        return matchCat && matchKw;
      });

      if (countBadge) {
        countBadge.textContent = filtered.length + " 件";
      }

      if (filtered.length === 0) {
        grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:48px 20px;color:#94a3b8;">' +
          '<div style="font-size:32px;margin-bottom:12px;">🔍</div>' +
          '<p>条件に一致する音声講義が見つかりませんでした。</p>' +
          '</div>';
        return;
      }

      var html = filtered.map(function (t) {
        var isPlaying = t.id === currentPlayingId;
        var pointsList = t.key_points.map(function (p) {
          return '<li>' + escapeHtml(p) + '</li>';
        }).join("");

        return '<div class="podcast-card' + (isPlaying ? ' is-playing' : '') + '" id="track-' + t.id + '">' +
          '  <div class="podcast-card-top">' +
          '    <span class="podcast-category-badge">' + escapeHtml(t.category_badge || t.category) + '</span>' +
          '    <div class="podcast-meta-badge">' +
          '      <span>⏱️ ' + escapeHtml(t.duration) + '</span>' +
          '      <span>💾 ' + t.size_mb + 'MB</span>' +
          '    </div>' +
          '  </div>' +
          '  <h3 class="podcast-card-title">' + escapeHtml(t.title) + '</h3>' +
          '  <p class="podcast-card-desc">' + escapeHtml(t.summary) + '</p>' +
          '  <div class="podcast-points-box">' +
          '    <div class="podcast-points-head"><span>📌</span> 講義の重要アジェンダ</div>' +
          '    <ul class="podcast-points-list">' + pointsList + '</ul>' +
          '  </div>' +
          '  <div class="podcast-card-footer">' +
          '    <button class="btn-play-audio" data-id="' + t.id + '">' +
          '      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>' +
          '      ' + (isPlaying ? '再生中（プレイヤー起動中）' : '今すぐ音声を聴く') +
          '    </button>' +
          '    <a class="btn-audio-gdrive" href="' + t.gdrive_url + '" target="_blank" rel="noopener noreferrer">' +
          '      <span>Driveで開く</span>' +
          '      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>' +
          '    </a>' +
          '  </div>' +
          '</div>';
      }).join("");

      grid.innerHTML = html;

      // 再生ボタンイベント
      grid.querySelectorAll(".btn-play-audio").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var id = btn.getAttribute("data-id");
          playTrack(id);
        });
      });
    }

    // 再生処理
    function playTrack(id) {
      var track = PODCAST_DATA.find(function (t) { return t.id === id; });
      if (!track) return;

      currentPlayingId = id;
      if (stickyPlayer) {
        stickyPlayer.classList.add("is-active");
        if (playingTitle) {
          playingTitle.textContent = "🎙️ 再生中: " + track.title;
        }
        if (playerIframe) {
          playerIframe.src = track.preview_url;
        }
        // スムーズスクロール
        stickyPlayer.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }

      renderTracks();
    }

    // 閉じるボタン
    if (playerClose && stickyPlayer) {
      playerClose.addEventListener("click", function () {
        stickyPlayer.classList.remove("is-active");
        if (playerIframe) playerIframe.src = "";
        currentPlayingId = null;
        renderTracks();
      });
    }

    // FAQアコーディオン開閉
    document.querySelectorAll(".ai-faq-question").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var item = btn.closest(".ai-faq-item");
        if (item) {
          item.classList.toggle("is-open");
        }
      });
    });

    function escapeHtml(str) {
      if (!str) return "";
      return str.replace(/[&<>"']/g, function (m) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m];
      });
    }

    // 初回描画
    renderTracks();
  });
})();

