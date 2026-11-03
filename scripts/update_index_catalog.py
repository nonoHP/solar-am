#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solar AM Notes - 資料体系インデックス (00_資料体系インデックス.md) 自動生成スクリプト
Google Drive（マイドライブ/太陽光/）の実ファイルを走査し、
最新のファイル数、カテゴリ別原本一覧テーブル、サイズを完全同期して出力します。
"""

import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

GDRIVE_BASE = r"G:\マイドライブ\太陽光"
OUTPUT_MD = r"c:\Users\user\Antigravity\太陽光\00_資料体系インデックス.md"

# 大分類カテゴリの順序と説明
TOP_CATEGORIES = [
    {
        "code": "01",
        "name": "01_法令・制度・ガイドライン",
        "desc": "エネ庁、環境省、農水省、林野庁、TDGC、送配電各社（特措法、事業計画策定GL、出力制御指針、営農型通知、廃棄・リサイクル新法・下位法令検討資料）"
    },
    {
        "code": "02",
        "name": "02_設備技術・設計施工・保安",
        "desc": "経産省保安、NEDO、JPEA、消防庁（電技解釈、架台基礎GL、水上・営農実験、事故不具合事例、保守点検GL、表示GL、力率一定制御QA）"
    },
    {
        "code": "03",
        "name": "03_金融・PPA・電力市場・契約",
        "desc": "OCCTO、環境省、JPEA（容量市場包括検証・補完オークション、コーポレートPPA事例、自家消費・蓄電池、AMガイドライン改訂版）"
    },
    {
        "code": "04",
        "name": "04_電験（電気主任技術者）",
        "desc": "電気技術者試験センター、実務テキスト（電験三種公式本試験問題・正解配点、理論・電力・機械・法規演習）"
    },
    {
        "code": "05",
        "name": "05_音声レクチャー・解説音源",
        "desc": "太陽光AM・制度・技術の要点を耳で学ぶオリジナル解説音声（14本）"
    },
    {
        "code": "06",
        "name": "06_独自リサーチ・スライド",
        "desc": "ディープリサーチ資料、プレゼンテーションスライド原本"
    }
]

def format_size(bytes_len):
    """ファイルサイズを可読形式（KB/MB）に変換"""
    if bytes_len >= 1024 * 1024:
        return f"{bytes_len / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_len / 1024:.0f} KB"

def get_file_type(ext):
    """拡張子から種別文字列を返す"""
    ext_lower = ext.lower().replace(".", "")
    if ext_lower == "pdf":
        return "PDF"
    elif ext_lower in ["m4a", "mp3"]:
        return ext_lower.upper()
    elif ext_lower in ["jpg", "jpeg", "png"]:
        return ext_lower.upper()
    elif ext_lower == "md":
        return "MD"
    elif ext_lower == "gdoc":
        return "GDOC"
    return ext_lower.upper()

def main():
    if not os.path.exists(GDRIVE_BASE):
        print(f"[ERROR] Path not found: {GDRIVE_BASE}")
        sys.exit(1)

    # 全ファイルスキャン
    all_files = []
    folder_files = {}

    for root, dirs, files in os.walk(GDRIVE_BASE):
        rel_dir = os.path.relpath(root, GDRIVE_BASE)
        if rel_dir == ".":
            # ルート直下の .md ファイル等はスキップまたは別枠
            continue
        
        # HPバックアップ等の管理用フォルダは除外
        if rel_dir.startswith("HPバックアップ") or ".git" in rel_dir:
            continue

        for f in sorted(files):
            full_p = os.path.join(root, f)
            size = os.path.getsize(full_p)
            ext = os.path.splitext(f)[1]
            item = {
                "rel_dir": rel_dir,
                "filename": f,
                "size": size,
                "ext": ext,
                "type": get_file_type(ext)
            }
            all_files.append(item)
            if rel_dir not in folder_files:
                folder_files[rel_dir] = []
            folder_files[rel_dir].append(item)

    total_files = len(all_files)
    pdf_files = [f for f in all_files if f["ext"].lower() == ".pdf"]
    total_pdfs = len(pdf_files)
    other_files = total_files - total_pdfs

    # 大分類別PDF集計
    cat_summary = []
    for cat in TOP_CATEGORIES:
        cat_prefix = cat["name"]
        cat_all = [f for f in all_files if f["rel_dir"].startswith(cat_prefix)]
        cat_pdf = [f for f in cat_all if f["ext"].lower() == ".pdf"]
        cat_summary.append({
            "code": cat["code"],
            "name": cat["name"],
            "pdf_count": len(cat_pdf),
            "total_count": len(cat_all),
            "desc": cat["desc"]
        })

    # Markdown構築
    now_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    lines = []
    lines.append("# 太陽光・再生可能エネルギー・電力システム実務 公的原本資料体系インデックス\n")
    lines.append("> [!IMPORTANT]")
    lines.append(f"> **原本アーカイブ総ファイル数: {total_files}件（PDF公的実務原本: {total_pdfs}件 / 電験・音声・スライド等: {other_files}件）**  ")
    lines.append(f"> **最終更新日時: {now_str}**  ")
    lines.append("> **Google Drive原本格納URL**: [https://drive.google.com/open?id=1DrJ6fb1ogmJ0mTASIJPvzN9IL0IlwR_Z&usp=drive_fs](https://drive.google.com/open?id=1DrJ6fb1ogmJ0mTASIJPvzN9IL0IlwR_Z&usp=drive_fs)\n")
    lines.append("本インデックスは、Google Drive（`マイドライブ/太陽光/`）に体系的に整理・保管された、経済産業省（エネ庁・保安院）、環境省、農林水産省、林野庁、消防庁、電力広域的運営推進機関（OCCTO）、送配電網協議会（TDGC）、一般送配電事業者10社、新エネルギー・産業技術総合開発機構（NEDO）、太陽光発電協会（JPEA）等の**公的一次原本資料（PDF）**を完全網羅した実務カタログです。\n")
    lines.append("---\n")
    lines.append("## 📁 大分類・体系構成サマリー\n")
    lines.append("| 分類コード | 大分類・カテゴリ名 | PDF原本数 | 主な公的発行機関・収録内容 |")
    lines.append("|:---|:---|:---:|:---|")

    for c in cat_summary:
        lines.append(f"| **{c['code']}** | **{c['name']}** | **{c['pdf_count']}件** (計{c['total_count']}件) | {c['desc']} |")

    lines.append("\n---\n")
    lines.append("## 📚 フォルダ別 詳細原本カタログ\n")

    # フォルダ順にソートして出力
    sorted_folders = sorted(folder_files.keys())
    for fld in sorted_folders:
        f_list = folder_files[fld]
        pdf_c = sum(1 for x in f_list if x["ext"].lower() == ".pdf")
        lines.append(f"### 📂 `{fld}` （計 {len(f_list)}件 / PDF {pdf_c}件）\n")
        lines.append("| No. | ファイル名（原本標題） | 種別 | サイズ |")
        lines.append("|:---:|:---|:---:|:---:|")
        for idx, item in enumerate(f_list, 1):
            lines.append(f"| {idx} | `{item['filename']}` | {item['type']} | {format_size(item['size'])} |")
        lines.append("")

    content = "\n".join(lines)
    with open(OUTPUT_MD, "w", encoding="utf-8") as out:
        out.write(content)

    # Google Drive側にも同期保存
    gdrive_md = os.path.join(GDRIVE_BASE, "00_資料体系インデックス.md")
    with open(gdrive_md, "w", encoding="utf-8") as out:
        out.write(content)

    print(f"[SUCCESS] {OUTPUT_MD} を更新しました（総ファイル数: {total_files}件, PDF: {total_pdfs}件）")
    print(f"[SUCCESS] Google Drive側（{gdrive_md}）も同期しました。")

if __name__ == "__main__":
    main()
