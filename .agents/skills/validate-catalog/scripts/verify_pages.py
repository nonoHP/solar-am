# -*- coding: utf-8 -*-
"""
太陽光AMノート ページ・メニュー整合性検証スクリプト (verify_pages.py)
notes/ 配下の HTML と assets/js/main.js の PAGES 配列の整合性を突合します。
"""

import os
import sys
import re

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

def verify():
    notes_dir = os.path.join(ROOT_DIR, "notes")
    main_js = os.path.join(ROOT_DIR, "assets", "js", "main.js")

    print("=== 太陽光AMノート 整合性検証 ===")
    if not os.path.exists(notes_dir) or not os.path.exists(main_js):
        print("❌ エラー: notes/ または main.js が見つかりません。")
        return False

    # 1. notes/ の HTML 一覧取得
    note_files = {f for f in os.listdir(notes_dir) if f.endswith(".html")}
    print(f"📄 notes/ 内のノート数: {len(note_files)}件")

    # 2. main.js の PAGES 配列からファイル名を抽出
    with open(main_js, "r", encoding="utf-8", errors="ignore") as f:
        js_content = f.read()

    # extract url: "notes/xxx.html"
    registered_notes = set(re.findall(r"notes/([a-zA-Z0-9_\-]+\.html)", js_content))
    print(f"📑 main.js に登録済みのノート数: {len(registered_notes)}件")

    missing_in_js = note_files - registered_notes
    missing_in_files = registered_notes - note_files

    has_error = False
    if missing_in_js:
        has_error = True
        print(f"\n⚠️ main.js に未登録のノートファイル ({len(missing_in_js)}件):")
        for m in sorted(missing_in_js):
            print(f"  - notes/{m}")

    if missing_in_files:
        has_error = True
        print(f"\n❌ main.js に登録されているが実ファイルが存在しない ({len(missing_in_files)}件):")
        for m in sorted(missing_in_files):
            print(f"  - notes/{m}")

    if not has_error:
        print("\n✅ 完全一致: すべてのノートが main.js のメニューと完全に同期しています！")
        return True
    return False

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
