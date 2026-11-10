---
name: validate-catalog
description: >-
  Verifies that all HTML files in notes/ are properly registered in the PAGES array
  of assets/js/main.js to avoid broken links and orphan pages in the Solar AM project.
  Use this skill whenever adding, deleting, or renaming notes in the Solar AM project.
---

# Validate Catalog Skill (太陽光ノート・メニュー同期検証)

本スキルは、`notes/` 配下の学習ノートが `assets/js/main.js` のナビゲーションメニュー（`PAGES` 配列）と完全に一致しているかを自動検査するための手順書です。

## 実行手順
1. 以下の検査スクリプトを実行する：
   ```powershell
   python .agents/skills/validate-catalog/scripts/verify_pages.py
   ```
2. 出力結果を確認する：
   - 「完全一致」と出ればOK。
   - 「未登録のノートファイル」が表示された場合は、指示に従って `main.js` の `PAGES` 配列にタイトル、トピック、URLを追加する。
3. 整合性が確認できたら `/deploy` で公開する。

