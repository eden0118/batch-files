#!/bin/bash
# 批次檔案重新命名工具啟動腳本

# 取得腳本所在目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 嘗試使用 Homebrew Python 3.12（推薦）
if [ -x "/opt/homebrew/opt/python@3.12/bin/python3.12" ]; then
    /opt/homebrew/opt/python@3.12/bin/python3.12 "${SCRIPT_DIR}/batch_rename_gui.py"
# 否則使用系統 Python 3
elif command -v python3 &> /dev/null; then
    python3 "${SCRIPT_DIR}/batch_rename_gui.py"
# 否則使用 Python（可能是 Python 2，但值得一試）
elif command -v python &> /dev/null; then
    python "${SCRIPT_DIR}/batch_rename_gui.py"
else
    echo "❌ 錯誤：找不到 Python。請確保已安裝 Python 3。"
    echo "💡 macOS 推薦使用：brew install python@3.12"
    exit 1
fi
