---
name: fetch-news
description: >-
  メガソーラー・再生可能エネルギーに関する最新ニュースや政策動向をスクリプトで自動収集し、
  news.json および news.html を更新して GitHub Pages へデプロイするスキル。
  ユーザーが「ニュースを更新して」「最新政策動向を取得して」と指示した際に使用する。
---

# 太陽光・再エネ最新ニュース更新スキル

本スキルは、`scripts/fetch_news.py` を実行して再エネ・電力市場・FIT/FIP関連の最新動向を収集し、サイトのニュースセクションを更新します。

## 実行手順

1. **ニュース収集スクリプトの実行**:
   ```powershell
   python scripts/fetch_news.py
   ```

2. **インデックスカタログの更新**:
   ```powershell
   python scripts/update_index_catalog.py
   ```

3. **Git コミット＆自動プッシュ**:
   ```powershell
   git add data/news.json assets/js/news_data.js news.html
   git status
   git commit -m "Update: Solar energy latest news and policies"
   git push origin main
   ```
