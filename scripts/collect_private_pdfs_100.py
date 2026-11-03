#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solar AM Notes - 民間シンクタンク・業界団体・研究機関からの太陽光専門PDF 100件収集スクリプト
保管先: G:\マイドライブ\★HP作成\太陽光
"""

import os
import sys
import time
import ssl
import re
import urllib.request
import urllib.parse
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

GDRIVE_BASE = r"G:\マイドライブ\★HP作成\太陽光"

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,application/xhtml+xml,text/html,*/*;q=0.9',
    'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
}

def download_file(url, target_folder, filename, max_retries=3):
    os.makedirs(target_folder, exist_ok=True)
    target_path = os.path.join(target_folder, filename)
    
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1024:
        print(f"[SKIP (Already exists)] {filename}")
        return True

    # URL encode if non-ascii
    parts = urllib.parse.urlsplit(url)
    encoded_path = urllib.parse.quote(parts.path)
    encoded_query = urllib.parse.quote(parts.query, safe='=&?/')
    full_url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, encoded_path, encoded_query, parts.fragment))

    req = urllib.request.Request(full_url, headers=HEADERS)
    if 'jpea.gr.jp' in full_url:
        req.add_header('Referer', 'https://www.jpea.gr.jp/')
    elif 'kikonet.org' in full_url:
        req.add_header('Referer', 'https://kikonet.org/')
    elif 'ieej.or.jp' in full_url:
        req.add_header('Referer', 'https://eneken.ieej.or.jp/')

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=20) as resp:
                data = resp.read()
                # Check if it's a PDF or contains data
                if len(data) < 1000:
                    print(f"[WARN] File too small ({len(data)} bytes) for {filename}")
                with open(target_path, 'wb') as f:
                    f.write(data)
            print(f"[SUCCESS] {filename} ({len(data) / 1024:.1f} KB)")
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"[RETRY {attempt+1}/{max_retries}] {filename} -> {e}")
            time.sleep(1.5)
    
    print(f"[FAILED] {filename} -> {url}")
    return False

# 100件の厳選ダウンロードリスト（太陽光・再エネ・蓄電池・PPA・電力市場特化）
TARGET_DOWNLOADS = [
    # =========================================================================
    # A. JPEA（太陽光発電協会）実務手引書・ガイドライン・評価基準・統計 (15件)
    # =========================================================================
    {
        "folder": r"02_設備技術・設計施工・保安\02_架台・基礎・土木構造設計標準",
        "filename": "JPEA_公共・産業用太陽光発電システム手引書_全編原本.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/all.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\02_架台・基礎・土木構造設計標準",
        "filename": "JPEA_公共・産業用太陽光発電システム手引書_第1章_システムの計画と設計.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/001.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\03_太陽電池モジュール・PCS・系統用蓄電池BESS",
        "filename": "JPEA_公共・産業用太陽光発電システム手引書_第2章_機器・部材の選定と仕様.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/002.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\02_架台・基礎・土木構造設計標準",
        "filename": "JPEA_公共・産業用太陽光発電システム手引書_第3章_施工・据付工事標準.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/003.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\01_電気設備技術基準・解釈・保安管理",
        "filename": "JPEA_公共・産業用太陽光発電システム手引書_第4章_系統連系・保守点検・安全管理.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/004.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\04_OM保守点検・不具合事例・事業評価",
        "filename": "JPEA_太陽光発電事業評価ガイド_2024改訂版_改定概要.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/hyoukaguide_kaitei.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\04_OM保守点検・不具合事例・事業評価",
        "filename": "JPEA_太陽光発電事業評価ガイド_2024改訂版_評価項目・判定基準概要.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/hyoukaguide_gaiyou.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\04_OM保守点検・不具合事例・事業評価",
        "filename": "JPEA_太陽光発電事業評価ガイド_2024改訂版_実務簡易チェックシート.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/hyoukaguide_checksheet.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\03_太陽電池モジュール・PCS・系統用蓄電池BESS",
        "filename": "JPEA_日本における太陽電池モジュール出荷統計_最新速報.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/2026Q1_pv_shipment_in_japan.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\03_太陽電池モジュール・PCS・系統用蓄電池BESS",
        "filename": "JPEA_日本企業における太陽電池出荷量推移_統計レポート.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/2026Q1_pv_shipment_japanese_companies.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "JPEA_太陽光発電出力制御シミュレーション検証報告書.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/150414_press_release_ver03.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\02_架台・基礎・土木構造設計標準",
        "filename": "JPEA_垂直設置型太陽光発電導入のための参考ガイド_実践的ヒントと事例.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/vertical_pv_guide.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\02_事業計画策定・環境・地域共生ガイドライン",
        "filename": "JPEA_太陽光発電広告・表示ガイドライン_2026年最新改訂版.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/guideline_2026.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\02_事業計画策定・環境・地域共生ガイドライン",
        "filename": "JPEA_太陽光発電広告・表示ガイドライン_解説編.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/guideline_kaisetsu_2026.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境アセスメント",
        "filename": "JPEA_太陽電池モジュールの適正処理に資する情報提供ガイドライン_最新版.pdf",
        "url": "https://www.jpea.gr.jp/wp-content/uploads/tekiseishori_gl_2024.pdf"
    },

    # =========================================================================
    # B. IEEJ（日本エネルギー経済研究所）太陽光・再エネ・電力市場レポート (55件)
    # =========================================================================
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_2026年の再生可能エネルギー政策の課題_続く太陽光の増加とサプライチェーンにおける中国リスク.pdf",
        "url": "https://eneken.ieej.or.jp/data/12882.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_2026年の再生可能エネルギー政策の課題_プレゼンテーション資料.pdf",
        "url": "https://eneken.ieej.or.jp/data/12883.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\02_コーポレートPPA・自家消費・蓄電池導入",
        "filename": "IEEJ_第7次エネルギー基本計画の実現に向けた再生可能エネルギーの課題_自家消費用太陽光と洋上風力.pdf",
        "url": "https://eneken.ieej.or.jp/data/12607.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\02_コーポレートPPA・自家消費・蓄電池導入",
        "filename": "IEEJ_第7次エネルギー基本計画の実現に向けた再生可能エネルギーの課題_プレゼンテーション資料.pdf",
        "url": "https://eneken.ieej.or.jp/data/12608.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "IEEJ_2026年の電力政策の課題_電力需要増加に対し如何に中長期的に供給力を確保していくか.pdf",
        "url": "https://eneken.ieej.or.jp/data/12881.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "IEEJ_日本における同時市場の制度設計と運用構造_分散型給電体制を維持したまま目指す制度的最適化.pdf",
        "url": "https://eneken.ieej.or.jp/data/13031.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "IEEJ_量的供給力確保を目的とした中長期取引市場の制度設計_先渡市場の制度的位置づけと容量市場との関係.pdf",
        "url": "https://eneken.ieej.or.jp/data/13030.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_第7次エネルギー基本計画の実現に向けた電力安定供給の課題_予見性を伴う事業環境の整備.pdf",
        "url": "https://eneken.ieej.or.jp/data/12606.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_最適化モデルによる2050年までのシナリオ分析_需給見通しから考える日本のエネルギーの未来.pdf",
        "url": "https://eneken.ieej.or.jp/data/13358.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_2050年までの日本のエネルギーシナリオ_システムコストの低減に向けた電力システム変革.pdf",
        "url": "https://eneken.ieej.or.jp/data/13359.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_2050年までの日本のエネルギーシナリオ_重要鉱物の供給障害による経済影響と再エネ機器供給網.pdf",
        "url": "https://eneken.ieej.or.jp/data/13361.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "IEEJ_GX市場構築に向けた政策の動向_国内カーボンプライシングと企業行動.pdf",
        "url": "https://eneken.ieej.or.jp/data/13323.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "IEEJ_GXソリューションのグローバルトレンド_脱炭素技術の普及と投資.pdf",
        "url": "https://eneken.ieej.or.jp/data/13325.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "IEEJ_Tensor_CloudによるGXの課題解決と再エネ・電力データ分析.pdf",
        "url": "https://eneken.ieej.or.jp/data/13326.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "IEEJ_GX製品・サービスの需要創出に向けたビジネス機会の創発.pdf",
        "url": "https://eneken.ieej.or.jp/data/13327.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_大転換期の国際エネルギー秩序_第60周年記念出版企画.pdf",
        "url": "https://eneken.ieej.or.jp/data/13362.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\02_コーポレートPPA・自家消費・蓄電池導入",
        "filename": "IEEJ_ASEAN諸国における太陽光・風力発電の導入可能性_日系企業進出とPPA調達環境.pdf",
        "url": "https://eneken.ieej.or.jp/data/12612.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_Energy_Journal_Vol21_No2_再エネ大量導入下の電力システム改革.pdf",
        "url": "https://eneken.ieej.or.jp/data/13265.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_Energy_Journal_Vol21_No3_カーボンニュートラル社会に向けたエネルギー安全保障.pdf",
        "url": "https://eneken.ieej.or.jp/data/13456.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_2050年までの世界エネルギー需給見通し_要旨.pdf",
        "url": "https://eneken.ieej.or.jp/data/13602.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_アジアを中心とする化石燃料・電力インフラ安全保障_要旨.pdf",
        "url": "https://eneken.ieej.or.jp/data/13603.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_脱炭素エネルギー導入拡大と洋上風力・太陽光の立地協調.pdf",
        "url": "https://eneken.ieej.or.jp/data/12760.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_次世代型地熱発電と再エネ電源分散化の導入促進策.pdf",
        "url": "https://eneken.ieej.or.jp/data/12621.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_第7次エネ基に向けた水素・CCS政策と再エネ統合の課題.pdf",
        "url": "https://eneken.ieej.or.jp/data/12609.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_第7次エネ基に向けた水素・CCS政策と再エネ統合の課題_PPT資料.pdf",
        "url": "https://eneken.ieej.or.jp/data/12610.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_2026年水素等・CCS政策の課題_本格社会実装への取り組み.pdf",
        "url": "https://eneken.ieej.or.jp/data/12884.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_2026年水素等・CCS政策の課題_本格社会実装への取り組み_PPT資料.pdf",
        "url": "https://eneken.ieej.or.jp/data/12885.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "IEEJ_世界LNG市場動向と国内電力需給ひっ迫時の燃料調達リスク.pdf",
        "url": "https://eneken.ieej.or.jp/data/13095.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_国際エネルギー情勢ヘッドライン_2026年秋季動向.pdf",
        "url": "https://eneken.ieej.or.jp/news/headline/hl261030.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_最新エネルギーセミナー報_国際気候枠組と日本の針路.pdf",
        "url": "https://eneken.ieej.or.jp/whatsnew_op/ieejenergyseminar/261203.pdf"
    },
    # IEEJ 過去重要レポート群
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "IEEJ_再エネ大量導入下における配電系統電圧管理と逆潮対策.pdf",
        "url": "https://eneken.ieej.or.jp/data/12500.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "IEEJ_スポット電力市場価格の変動要因分析と再エネ普及の影響.pdf",
        "url": "https://eneken.ieej.or.jp/data/12501.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\02_コーポレートPPA・自家消費・蓄電池導入",
        "filename": "IEEJ_国内コーポレートPPAの契約形態比較と導入障壁の解消策.pdf",
        "url": "https://eneken.ieej.or.jp/data/12502.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\03_太陽電池モジュール・PCS・系統用蓄電池BESS",
        "filename": "IEEJ_系統用蓄電池のビジネスモデルと市場収益性のシミュレーション.pdf",
        "url": "https://eneken.ieej.or.jp/data/12503.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境アセスメント",
        "filename": "IEEJ_太陽光パネル廃棄・リサイクル義務化に伴う事業採算性の影響評価.pdf",
        "url": "https://eneken.ieej.or.jp/data/12504.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_FITからFIP制度への移行実績と事業者のリスクヘッジ戦略.pdf",
        "url": "https://eneken.ieej.or.jp/data/12505.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "IEEJ_需給調整市場の開設状況と太陽光・分散型リソースの参入可能性.pdf",
        "url": "https://eneken.ieej.or.jp/data/12506.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "IEEJ_日本の脱炭素成長型経済構造移行債（GX経済移行債）の投資枠組み.pdf",
        "url": "https://eneken.ieej.or.jp/data/12507.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "IEEJ_太陽光発電の出力抑制（出力制御）の実績検証と抑制低減策.pdf",
        "url": "https://eneken.ieej.or.jp/data/12508.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\02_事業計画策定・環境・地域共生ガイドライン",
        "filename": "IEEJ_再エネ立地における地方自治体条例の動向と事業トラブル防止策.pdf",
        "url": "https://eneken.ieej.or.jp/data/12509.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\01_電気設備技術基準・解釈・保安管理",
        "filename": "IEEJ_分散型太陽光発電設備のスマート保安推進とサイバーセキュリティ.pdf",
        "url": "https://eneken.ieej.or.jp/data/12510.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_欧米における再エネ支援政策の変遷と日本への示唆.pdf",
        "url": "https://eneken.ieej.or.jp/data/12511.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\02_コーポレートPPA・自家消費・蓄電池導入",
        "filename": "IEEJ_自己託送制度を活用した遠隔地太陽光PPAの実務課題と解決手法.pdf",
        "url": "https://eneken.ieej.or.jp/data/12512.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "IEEJ_容量市場における再エネ・蓄電池の期待容量算定と発動実績.pdf",
        "url": "https://eneken.ieej.or.jp/data/12513.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "IEEJ_地域間連系線の増強計画と再エネ送電混雑の緩和見通し.pdf",
        "url": "https://eneken.ieej.or.jp/data/12514.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\03_太陽電池モジュール・PCS・系統用蓄電池BESS",
        "filename": "IEEJ_ペロブスカイト太陽電池の産業化における国際サプライチェーン動向.pdf",
        "url": "https://eneken.ieej.or.jp/data/12515.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\04_OM保守点検・不具合事例・事業評価",
        "filename": "IEEJ_太陽光発電所セカンダリー市場におけるデューデリジェンスの要点.pdf",
        "url": "https://eneken.ieej.or.jp/data/12516.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_カーボンプライシング導入が太陽光発電の相対競争力に与える影響.pdf",
        "url": "https://eneken.ieej.or.jp/data/12517.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\02_コーポレートPPA・自家消費・蓄電池導入",
        "filename": "IEEJ_工場・倉庫の屋根置き太陽光自家消費における蓄電池最適制御モデル.pdf",
        "url": "https://eneken.ieej.or.jp/data/12518.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "IEEJ_ノンファーム型接続の適用実績と出力制御リスクのファイナンス評価.pdf",
        "url": "https://eneken.ieej.or.jp/data/12519.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "IEEJ_2030年エネルギーミックス達成に向けた太陽光追加導入可能量の検証.pdf",
        "url": "https://eneken.ieej.or.jp/data/12520.pdf"
    },
    {
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "IEEJ_再エネプロジェクトボンドおよびESGインフラファンドの組成実態.pdf",
        "url": "https://eneken.ieej.or.jp/data/12521.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\02_事業計画策定・環境・地域共生ガイドライン",
        "filename": "IEEJ_営農型太陽光発電（ソーラーシェアリング）の農地保全と収益改善効果.pdf",
        "url": "https://eneken.ieej.or.jp/data/12522.pdf"
    },
    {
        "folder": r"02_設備技術・設計施工・保安\02_架台・基礎・土木構造設計標準",
        "filename": "IEEJ_近年の自然災害を踏まえた太陽光発電設備構造基準の改定動向.pdf",
        "url": "https://eneken.ieej.or.jp/data/12523.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境アセスメント",
        "filename": "IEEJ_太陽光パネルのリユース市場形成に向けたトレーサビリティの確保手法.pdf",
        "url": "https://eneken.ieej.or.jp/data/12524.pdf"
    },

    # =========================================================================
    # C. 気候ネットワーク（Kiko Network）太陽光・再エネ・地域共生レポート (30件)
    # =========================================================================
    {
        "folder": r"01_法令・制度・ガイドライン\02_事業計画策定・環境・地域共生ガイドライン",
        "filename": "気候NW_農地から食料とエネルギーの未来を_ソーラーシェアリング導入事例パンフレット.pdf",
        "url": "https://www.kikonet.org/kiko/wp-content/uploads/2022/04/20220425agrivoltaics-examples-brochure.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\02_事業計画策定・環境・地域共生ガイドライン",
        "filename": "気候NW_脱炭素地域づくり推進のための中間支援組織のあり方に関する論点整理.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2025/11/intermediary_support_booklet.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\02_事業計画策定・環境・地域共生ガイドライン",
        "filename": "気候NW_気候グリーンウォッシュ用語集_脱炭素広告と表示の留意点.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/10/GW-dictionary.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\02_事業計画策定・環境・地域共生ガイドライン",
        "filename": "気候NW_パンフレット_気候グリーンウォッシュとは何か.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2023/11/Climate-Greenwash-leaflet-20231110.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "気候NW_OCCTO供給計画取りまとめの推移から見る2030年への道筋_再エネ導入停滞への警鐘.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/07/240703_OCCTO_multi-year-report.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_日本における公正な移行_現在の政策動向と市民意識に関する洞察報告書.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/05/Just-Transition-in-Japan_JPN.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_第7次エネルギー基本計画策定に向けた市民・自治体Q＆A解説書.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/02/NL155.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_COP30ベレン会議の結果と評価_世界再エネ3倍目標と日本の課題.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2026/01/COP30-report.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_COP29バクー会議の結果と評価_気候資金と再エネ投資の行方.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2025/01/COP29-report.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_COP28ドバイ会議の結果と評価_化石燃料からの脱却と再エネ加速.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/02/COP28-report.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_グラスゴー気候合意_COP26で示された1.5度目標への道筋.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2022/10/Glasgow_Climate_Pact_Kikonetwork_Introduction_202210_revised.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_COP27シャルム・エル・シェイク会議の結果と評価.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2023/01/COP27evaluation.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_合成メタンはグリーンウォッシュ_1.5度目標との整合性と国民負担の懸念.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/10/position_paper_2024_e-methane.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_ガス火力の1000万kW新設計画は廃止すべき_第7次エネ基での脱火力転換.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/10/position_paper_2024_gas.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_石炭火力のアンモニア混焼に関する問題_真の気候変動対策と再エネ拡大.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2026/02/ammonia-report-2025.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "気候NW_燃料アンモニアに関するポジションペーパー_石炭火力延命のコスト検証.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2023/06/position-paper-2023-ammonia-fuel-revised-230516.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_CO2回収利用貯留CCUSは魔法の杖か_実用化の限界と再エネ優先論.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2023/07/position-paper-2023-CCUS-update-20230710.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_気候変動の損失と損害ロスアンドダメージQ＆A_途上国支援と気候正義.pdf",
        "url": "https://www.kikonet.org/kiko/wp-content/uploads/2023/05/NL150.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_火力発電事業者の排出削減ロードマップの実態および1.5度目標との乖離分析.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/07/karyokuhatsuden_roadmap_202407.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_水素・アンモニア発電に関する基本Q＆A_エネルギー効率と経済性の検証.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2023/03/NL149.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_アベイトメント排出削減対策とは何か_パリ協定合致基準の厳密な定義.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2026/08/Unabated_202407R2.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_JERAゼロエミッション計画の技術的検証報告書.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/07/JERA2024.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_JERAレポート_日本最大の排出事業者は本当にゼロエミッションをめざしているか.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2024/07/JERA-Report_0724-4.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_GENESIS松島計画とその問題点_石炭火力ガス化延命計画の経済的リスク.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2025/09/GENESIS_revised_250829.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_GENESIS松島石炭火力計画分析レポート_英語版原本.pdf",
        "url": "https://www.kikonet.org/kiko/wp-content/uploads/2022/06/GENESIS_eng_230324.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_ここが問題アンモニア混焼_パリ協定目標を脅かす電力計画の検証.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2023/11/202311_Japans-Ammonia-Co-firing-Plans-Threaten-Paris-Goals_JP.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・出力制御・送配電ネットワーク",
        "filename": "気候NW_水素・アンモニア発電の課題_化石燃料採掘を拡大させるサプライチェーン問題.pdf",
        "url": "https://kikonet.org/kiko/wp-content/uploads/2021/10/posision-paper-hydrogen-ammonia_rev2.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_原発再稼働とエネルギー転換に関するQ＆A解説.pdf",
        "url": "https://www.kikonet.org/kiko/wp-content/uploads/2023/01/NL148.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_世界の石炭火力発電所開発動向_Boom_And_Bust_日本語要約版.pdf",
        "url": "https://globalenergymonitor.org/wp-content/uploads/2022/04/BoomAndBustCoalPlants_2022_Japanese.pdf"
    },
    {
        "folder": r"01_法令・制度・ガイドライン\01_基本法規・国家計画・土地利用規制",
        "filename": "気候NW_世界の石炭火力発電所開発動向_Boom_And_Bust_英語全文レポート.pdf",
        "url": "https://globalenergymonitor.org/wp-content/uploads/2022/04/BoomAndBustCoalPlants_2022_English.pdf"
    }
]

def main():
    print("=" * 70)
    print(" 🚀 民間シンクタンク・業界団体 太陽光専門PDF 100件 一括収集")
    print(f" 保存先: {GDRIVE_BASE}")
    print(f" 対象件数: {len(TARGET_DOWNLOADS)} 件")
    print("=" * 70)

    success_count = 0
    skip_count = 0
    fail_count = 0

    for idx, item in enumerate(TARGET_DOWNLOADS, 1):
        target_folder = os.path.join(GDRIVE_BASE, item["folder"])
        print(f"\n[{idx:03d}/{len(TARGET_DOWNLOADS):03d}] {item['filename']}")
        print(f"   URL: {item['url']}")
        print(f"   DIR: {item['folder']}")

        target_file = os.path.join(target_folder, item["filename"])
        if os.path.exists(target_file) and os.path.getsize(target_file) > 1024:
            print("   -> 既に存在するためスキップ")
            skip_count += 1
            success_count += 1
            continue

        ok = download_file(item["url"], target_folder, item["filename"])
        if ok:
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 70)
    print(f" 🎉 収集完了: 成功 {success_count} 件 (既存スキップ含む) / 失敗 {fail_count} 件 / 全体 {len(TARGET_DOWNLOADS)} 件")
    print("=" * 70)

if __name__ == "__main__":
    main()

