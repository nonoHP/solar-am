---
name: add-note
description: >-
  Solar AM Notes に新しい実務学習ノート（HTMLページ）を追加し、
  assets/js/main.js のナビゲーション配列へ登録・整合性検証・デプロイを行うスキル。
  ユーザーが「新しいノートを追加して」「新しいテーマのページを作成して」と指示した際に使用する。
---

# 新規学習ノート追加スキル

本スキルは、`notes/` 配下に新しいテーマの学習ノートを作成し、サイト全体のナビゲーション（`main.js`）および目次と完全に同期させて公開する手順を定義します。

## 実行手順

### 1. 既存ノートをテンプレートとして複製
既存のページ（例: `notes/om.html`）を参考に、新規ノートHTMLを `notes/<page_id>.html` として作成します。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>【テーマ名】Solar AM Notes</title>
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body data-page="<page_id>">
  <!-- ナビゲーションやヘッダー -->
  <main>
    <section id="section1">
      <h2>1. 大見出し</h2>
      <p>解説テキスト...</p>
    </section>
  </main>
  <script src="../assets/js/main.js"></script>
</body>
</html>
```

### 2. `assets/js/main.js` の `PAGES` 配列への追加
`assets/js/main.js` の冒頭にある `PAGES` 配列に、新規ページのメタデータを追加します。
これにより、ドロップダウンメニュー、トピック別一覧、前後のページ送りリンクが自動生成されます。

### 3. デプロイと動作検証
```powershell
git add .
git status
git commit -m "Add: New study note <page_id>"
git push origin main
```

