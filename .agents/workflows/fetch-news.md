# fetch-news (.agents/workflows/fetch-news.md)

## 概要
太陽光発電・メガソーラー関連の最新業界ニュースを外部から自動取得し、`news.html` を更新・公開する手順書です。
チャット欄で `/fetch-news` と入力して呼び出します。

## 実行手順
1. **ニュース取得スクリプトの実行**:
   ```powershell
   python scripts/fetch_news.py
   ```
2. **更新内容の確認**:
   - `git diff news.html` を実行し、新しいニュース項目が正しく追加されているか確認する。
   - 文字化けや日付の乱れがないか確認する。
3. **自動コミットとデプロイ**:
   - 取得が成功したら `/deploy` ワークフローを実行し、GitHub Pages への公開を完了する。

