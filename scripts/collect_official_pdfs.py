#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solar AM Notes - 公的実務原本PDF 自動収集・体系化スクリプト
環境省、OCCTO（電力広域的運営推進機関）、JPEA（太陽光発電協会）、TDGC等から
太陽光・再エネ・蓄電池・市場実務に関わる一次原本PDFを収集し、
Google Drive（マイドライブ/太陽光/）の体系別フォルダに格納します。
"""

import os
import sys
import time
import ssl
import urllib.request
import urllib.error

# 出力文字コード
sys.stdout.reconfigure(encoding='utf-8')

# Google Drive ベースディレクトリ
GDRIVE_BASE = r"G:\マイドライブ\太陽光"

# SSLコンテキスト
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# 収集ターゲット定義
TARGET_DOWNLOADS = [
    # =========================================================================
    # 1. 01_法令・制度・ガイドライン \ 04_廃棄・リサイクル・環境GL
    # =========================================================================
    {
        "url": "https://www.env.go.jp/content/000302385.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_太陽光発電設備のリサイクル制度のあり方について_報告書.pdf"
    },
    {
        "url": "https://www.env.go.jp/content/000302386.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_太陽光発電設備のリサイクル制度のあり方について_参考資料.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000433712.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第11回_資料1_太陽電池廃棄物の再資源化等の推進に関する法律について.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000433713.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第11回_資料2_下位法令の検討体制等について.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000433714.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第11回_資料3_基本方針について.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000433716.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第11回_参考資料2_下位法令策定等に係る検討会の創設について.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000371843.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第10回_資料1_太陽光パネルのリサイクル制度について.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000300368.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第9回_資料1_太陽光発電設備のリサイクル制度のあり方について（案）.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000300463.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第9回_資料2_パブリックコメント結果及び考え方（案）.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000300371.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第9回_参考資料2_リサイクル制度検討参考資料.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000272490.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第8回_資料1_太陽光発電設備のリサイクル制度のあり方について（案）.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000272494.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第8回_参考資料2_参考資料.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000269504.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第7回_資料1_太陽光発電設備の廃棄・リサイクル制度構築に向けた論点整理.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000266953.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第6回_参考資料2_池田委員提出資料_リサイクル技術動向.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000261701.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第5回_資料2_PV_CYCLE_JAPAN説明用資料.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000261702.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第5回_資料3_再生可能エネルギー長期安定電源推進協会説明資料.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000261703.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第5回_資料4_太陽光発電協会_説明資料.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000261507.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第4回_資料1_これまでの議論について.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000261516.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第4回_資料2_全国解体工事業団体連合会説明資料.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000261509.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第4回_資料3_太陽光パネルリユース・リサイクル協会説明資料.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000261510.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第4回_資料4_AGC株式会社説明資料_カバーガラス再資源化.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000258349.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第3回_資料1_太陽光発電設備の廃棄・リサイクル制度の論点について.pdf"
    },
    {
        "url": "https://www.env.go.jp/council/content/03recycle03/000252102.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "環境省_第1回_資料3_太陽光発電設備の廃棄・リサイクルをめぐる状況及び論点について.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/uploads/260423_JPEA「太陽電池廃棄物の再資源化等の推進に関する法律案」について.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "JPEA_太陽電池廃棄物の再資源化等の推進に関する法律案に関する意見書.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/t171211.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "JPEA_使用済太陽電池モジュールの適正処理に資する情報提供のガイドライン_第1版.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/t161019.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "JPEA_太陽電池モジュールの環境配慮設計アセスメントガイドライン_第1版.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/uploads/20260608_recycle_contr_list_v1.9.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "JPEA_太陽電池モジュール適正処理リサイクル中間処理業者名簿_最新版.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/handout_qa.pdf",
        "folder": r"01_法令・制度・ガイドライン\04_廃棄・リサイクル・環境GL",
        "filename": "JPEA_使用済み太陽電池モジュールの適正処理・リサイクルQA集.pdf"
    },

    # =========================================================================
    # 2. 02_設備技術・設計施工・保安 \ 04_OM・保守点検・不具合事例・評価
    # =========================================================================
    {
        "url": "https://www.jpea.gr.jp/wp-content/uploads/jpea_hyouji_guideline_kaisetsu2026.pdf",
        "folder": r"02_設備技術・設計施工・保安\04_OM・保守点検・不具合事例・評価",
        "filename": "JPEA_太陽光発電協会_表示ガイドライン解説編_2026年版.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/t140925.pdf",
        "folder": r"02_設備技術・設計施工・保安\04_OM・保守点検・不具合事例・評価",
        "filename": "JPEA_公共産業用太陽光発電設備のレイアウト・表示自主ルール.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/revention_reflection.pdf",
        "folder": r"02_設備技術・設計施工・保安\04_OM・保守点検・不具合事例・評価",
        "filename": "JPEA_太陽光発電システムの反射光トラブル防止対策報告書.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/t151009.pdf",
        "folder": r"02_設備技術・設計施工・保安\04_OM・保守点検・不具合事例・評価",
        "filename": "JPEA_太陽光発電システム被災時の点検・撤去手順および留意点_水害編.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/t160428.pdf",
        "folder": r"02_設備技術・設計施工・保安\04_OM・保守点検・不具合事例・評価",
        "filename": "JPEA_太陽光発電システム被災時の点検・復旧・撤去手順および留意点_震災編.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/98/seibi_98_02_01.pdf",
        "folder": r"02_設備技術・設計施工・保安\04_OM・保守点検・不具合事例・評価",
        "filename": "OCCTO_高経年化設備更新ガイドラインの改定について_第98回広域系統整備委.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/150529_JPEA_checklist.pdf",
        "folder": r"02_設備技術・設計施工・保安\04_OM・保守点検・不具合事例・評価",
        "filename": "JPEA_太陽光発電システムの基礎・架台の設計・施工チェックリストと留意点.pdf"
    },

    # =========================================================================
    # 3. 02_設備技術・設計施工・保安 \ 03_太陽電池・PCS・系統用蓄電池BESS
    # =========================================================================
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/rikiritsu_qa.pdf",
        "folder": r"02_設備技術・設計施工・保安\03_太陽電池・PCS・系統用蓄電池BESS",
        "filename": "JPEA_PCS力率一定制御についてのQA集.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/guideline_sticker.pdf",
        "folder": r"02_設備技術・設計施工・保安\03_太陽電池・PCS・系統用蓄電池BESS",
        "filename": "JPEA_自立運転機能の操作方法表示シール等作成ガイドライン_第1版.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/97/seibi_97_02_01.pdf",
        "folder": r"02_設備技術・設計施工・保安\03_太陽電池・PCS・系統用蓄電池BESS",
        "filename": "OCCTO_系統用蓄電池の新規連系における課題と対応_第97回広域系統整備委.pdf"
    },

    # =========================================================================
    # 4. 02_設備技術・設計施工・保安 \ 01_電気設備技術基準・解釈・保安
    # =========================================================================
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/report_prevention.pdf",
        "folder": r"02_設備技術・設計施工・保安\01_電気設備技術基準・解釈・保安",
        "filename": "JPEA_屋根・建物からの墜落防止のための検討委員会報告書.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/121/chousei_121_03.pdf",
        "folder": r"02_設備技術・設計施工・保安\01_電気設備技術基準・解釈・保安",
        "filename": "OCCTO_イベリア半島大規模停電を踏まえた日本の電力系統での技術的対応.pdf"
    },

    # =========================================================================
    # 5. 03_金融・PPA・電力市場・契約 \ 01_AMガイドライン・グリーンファイナンス
    # =========================================================================
    {
        "url": "https://www.jpea.gr.jp/wp-content/uploads/hyoukaguide_kaitei.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "JPEA_太陽光発電事業の評価ガイド改訂概要_2024年改訂版.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/uploads/hyoukaguide_checksheet.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "JPEA_太陽光発電事業の評価ガイド簡易チェックシート.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/2025/files/seibi_94_01_02.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\01_AMガイドライン・グリーンファイナンス",
        "filename": "OCCTO_北海道本州間連系設備に係るプロジェクトファイナンス上の課題について.pdf"
    },

    # =========================================================================
    # 6. 01_法令・制度・ガイドライン \ 01_関係法令・基本計画
    # =========================================================================
    {
        "url": "https://www.jpea.gr.jp/wp-content/uploads/pv_outlook2050_2024ver.1.pdf",
        "folder": r"01_法令・制度・ガイドライン\01_関係法令・基本計画",
        "filename": "JPEA_PV_OUTLOOK_2050_2024年度改訂版.pdf"
    },
    {
        "url": "https://www.tdgc.jp/compliance/docs/一般送配電事業者の行為規制等に関する行動指針.pdf",
        "folder": r"01_法令・制度・ガイドライン\01_関係法令・基本計画",
        "filename": "TDGC_一般送配電事業者の行為規制等に関する行動指針_公表原本.pdf"
    },

    # =========================================================================
    # 7. 01_法令・制度・ガイドライン \ 03_系統連系・電力市場・送配電
    # =========================================================================
    {
        "url": "https://www.occto.or.jp/assets/houkokusho/2026/denryokujukyukensho_20261028/261028_denryokujukyukensho.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_電力需給検証報告書_2026年10月28日公表最新原本.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/houkokusho/2026/2026_nenjihoukokusho/nenjihoukokusho_2026_kyoukyuukeikaku_260330.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_2026年度供給計画の取りまとめ_年次報告書版.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/houkokusho/2026/2026_nenjihoukokusho/260710_access_toukei_01.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_発電設備等系統アクセス業務情報公表_2025年度受付回答統計.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/houkokusho/2026/files/denryokujukyuu_2025_260909.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_電力需給及び電力系統に関する概況_2025年度実績_2026年9月公表.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/121/chousei_121_01.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_中長期の需給見通しを踏まえた供給力確保策について_第121回.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/120/chousei_120_03.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_地内系統混雑を考慮した供給信頼度評価の課題整理_第120回.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/117/chousei_117_03.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_再エネ主力電源化に向けた技術的課題及びその対応策の検討状況_第117回.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/116/chousei_116_03.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_再エネ予測精度向上に向けた取り組みについて_第116回.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/98/seibi_98_01_01.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_広域系統整備計画のコスト検証等に関するガイドラインについて_第98回.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/98/seibi_98_01_02.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_広域系統整備計画コスト検証ガイドライン素案_第98回.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/98/seibi_98_03_01.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_広域系統整備計画の進捗状況について_2025年度第3四半期_第98回.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/2025/files/seibi_92_02_01.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_2030年度の系統混雑に関する中長期見通し_第92回.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/2025/files/seibi_92_06_01.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_系統混雑に関する中長期見通しの算出結果_東京電力パワーグリッド.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/2025/files/seibi_92_10_01.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_系統混雑に関する中長期見通しの算出結果_九州電力送配電.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/kouikikeitouseibi/2025/files/seibi_92_07_01.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "OCCTO_系統混雑に関する中長期見通しの算出結果_関西電力送配電.pdf"
    },
    {
        "url": "https://www.jpea.gr.jp/wp-content/themes/jpea/pdf/t140829.pdf",
        "folder": r"01_法令・制度・ガイドライン\03_系統連系・電力市場・送配電",
        "filename": "JPEA_電力協議様式記載要領_高圧連系太陽光発電.pdf"
    },

    # =========================================================================
    # 8. 03_金融・PPA・電力市場・契約 \ 03_電力市場取引・容量市場・需給調整
    # =========================================================================
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/117/chousei_117_04.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "OCCTO_需給調整市場検討小委員会における検討状況_2025年度報告.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/houkokusho/2026/2026_nenjihoukokusho/20260514_chouseiryokukakuho_fy2026.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "OCCTO_2026年度調整力の確保に関する計画の取りまとめについて_報告.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/houkokusho/2026/260624_2027chouseiryokukoubo/20260624_chouseiryokukoubo_fy2027.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "OCCTO_2027年度向け調整力の公募にかかる必要量等の考え方について.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/various/capacity-market/houkatsutekikensyo/report/youryou_2025_houkatsutekikensyo_report.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "OCCTO_容量市場2025年度包括的検証_検証報告書_公表版.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/122/chousei_122_01.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "OCCTO_補完オークションについて_第122回調整力等委.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/122/chousei_122_02.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "OCCTO_需給状況を表す新たなシグナルの検討状況について_第122回調整力等委.pdf"
    },
    {
        "url": "https://www.occto.or.jp/assets/iinkai/chousei_jukyu/120/chousei_120_02.pdf",
        "folder": r"03_金融・PPA・電力市場・契約\03_電力市場取引・容量市場・需給調整",
        "filename": "OCCTO_中長期の調整力確保状況の確認結果_2035年度まで_第120回.pdf"
    }
]

def download_file(url, dest_path):
    """URLからファイルをダウンロードしてdest_pathに保存"""
    # 日本語など非ASCII文字が含まれる場合はURLエンコード
    parsed = urllib.parse.urlsplit(url)
    encoded_path = urllib.parse.quote(parsed.path, safe='/:@&=+$,?%#')
    encoded_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, encoded_path, parsed.query, parsed.fragment))

    req = urllib.request.Request(
        encoded_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
        }
    )
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as resp:
        content = resp.read()
    with open(dest_path, "wb") as f:
        f.write(content)
    return len(content)

def main():
    print("=" * 70)
    print(" ☀️ Solar AM Notes - 公的原本PDF 収集・拡充バッチ")
    print(f" 格納先ルート: {GDRIVE_BASE}")
    print(f" 対象件数: {len(TARGET_DOWNLOADS)} 件")
    print("=" * 70)

    if not os.path.exists(GDRIVE_BASE):
        print(f"[ERROR] Google Driveパスが存在しません: {GDRIVE_BASE}")
        sys.exit(1)

    success_count = 0
    skip_count = 0
    fail_count = 0

    for idx, item in enumerate(TARGET_DOWNLOADS, 1):
        target_dir = os.path.join(GDRIVE_BASE, item["folder"])
        os.makedirs(target_dir, exist_ok=True)
        dest_file = os.path.join(target_dir, item["filename"])

        if os.path.exists(dest_file) and os.path.getsize(dest_file) > 1000:
            print(f"[{idx:02d}/{len(TARGET_DOWNLOADS)}] [SKIP (既存)] {item['filename']} ({os.path.getsize(dest_file):,} bytes)")
            skip_count += 1
            continue

        print(f"[{idx:02d}/{len(TARGET_DOWNLOADS)}] [DL開始] {item['filename']}")
        print(f"       URL: {item['url']}")

        try:
            size = download_file(item["url"], dest_file)
            print(f"       -> [SUCCESS] 保存完了: {size:,} bytes")
            success_count += 1
            time.sleep(1.0)  # サーバー負荷軽減ウェイト
        except Exception as e:
            print(f"       -> [FAIL] ダウンロード失敗: {e}")
            fail_count += 1
            time.sleep(1.0)

    print("\n" + "=" * 70)
    print(f" 実行結果サマリー: 成功 {success_count} 件 / スキップ {skip_count} 件 / 失敗 {fail_count} 件")
    print("=" * 70)

if __name__ == "__main__":
    main()

