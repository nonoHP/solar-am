# -*- coding: utf-8 -*-
import sys
import json
import re

# Windows環境における文字エンコーディングのUTF-8強制
if sys.platform.startswith("win"):
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            print(json.dumps({"decision": "allow"}))
            return
        
        data = json.loads(raw_input)
        tool_call = data.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})
        
        if tool_name == "run_command":
            cmd = args.get("CommandLine", "")
            
            # 1. UTF-16LE 文字化け禁止パターン検知
            mojibake_patterns = [
                r"\bSet-Content\b",
                r"\bOut-File\b",
                r">\s*[\w\./\\]+\.(html|htm|js|css|json|txt|md)\b",
                r">>\s*[\w\./\\]+\.(html|htm|js|css|json|txt|md)\b"
            ]
            for pat in mojibake_patterns:
                if re.search(pat, cmd, re.IGNORECASE):
                    res = {
                        "decision": "deny",
                        "reason": (
                            "【Antigravity Guardrail】PowerShellのSet-Contentやリダイレクト(>, >>)は"
                            "UTF-16LE文字化けを引き起こすため禁止されています。"
                            "Python (open(..., encoding='utf-8')) または AI編集ツールを使用してください。"
                        )
                    }
                    print(json.dumps(res, ensure_ascii=False))
                    return

            # 2. プロジェクト直下への tmp_* ファイル生成の検知
            tmp_root_patterns = [
                r">\s*tmp_[^\s/\\|&;]+",
                r"New-Item\s+.*-Path\s+['\"]?tmp_",
                r"touch\s+tmp_"
            ]
            for pat in tmp_root_patterns:
                if re.search(pat, cmd, re.IGNORECASE):
                    res = {
                        "decision": "deny",
                        "reason": (
                            "【Antigravity Guardrail】プロジェクト直下に一時ファイルを作成することは"
                            "共通ルールで禁止されています。"
                        )
                    }
                    print(json.dumps(res, ensure_ascii=False))
                    return

        # 安全な場合は実行を許可
        print(json.dumps({"decision": "allow"}))

    except Exception as e:
        print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()

