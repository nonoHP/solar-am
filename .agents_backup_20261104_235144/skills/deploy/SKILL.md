---
name: deploy
description: >-
  Solar AM Notes の変更内容を検証し、GitHub Pages (origin main) へ一括デプロイするスキル。
  ユーザーが「デプロイして」「変更を反映して」「サイトを公開して」と指示した際に使用する。
---

# Solar AM Notes デプロイスキル

本スキルは、サイトの変更内容をコミットし、GitHub Pages へ反映させる標準デプロイパイプラインです。

## 実行手順

1. **変更確認とクリーンアップ**:
   - 不要なキャッシュ（`__pycache__`）をクリーンアップします。
   ```powershell
   Get-ChildItem -Path "." -Filter "__pycache__" -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
   ```

2. **Git ステージング・コミット・プッシュ**:
   ```powershell
   git add .
   git status
   git commit -m "Update: Solar AM Notes content and enhancements"
   git push origin main
   ```

3. **デプロイ確認**:
   - `https://nonohp.github.io/solar-am/` を確認します。

