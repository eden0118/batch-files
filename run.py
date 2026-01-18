#!/usr/bin/env python3
"""
跨平台運行腳本 (Windows & macOS & Linux)
批次檔案重新命名工具啟動器
"""

import sys
import os
import platform
import subprocess
from pathlib import Path


def get_python_executable() -> str:
    """取得當前 Python 可執行檔路徑"""
    return sys.executable


def check_dependencies() -> bool:
    """檢查必需的依賴是否已安裝"""
    required_modules = ['flet']
    optional_modules = ['opencc', 'opencc_python_reimplemented']

    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        print(f"❌ 缺少必需的模組: {', '.join(missing)}")
        print(f"\n💡 請執行以下命令安裝依賴：")
        print(f"   pip install {' '.join(missing)}")
        return False

    # 檢查可選模組
    opencc_available = False
    for module in optional_modules:
        try:
            __import__(module)
            opencc_available = True
            break
        except ImportError:
            pass

    if not opencc_available:
        print(f"⚠️  未安裝 OpenCC（簡繁轉換功能將不可用）")
        print(f"   可選安裝：pip install opencc-python-reimplemented")

    return True


def get_script_dir() -> Path:
    """取得腳本所在目錄"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包的應用
        script_dir = Path(sys.executable).parent
    else:
        # 一般 Python 腳本
        script_dir = Path(__file__).parent.absolute()
    return script_dir


def main():
    """主函數"""
    system = platform.system()
    script_dir = get_script_dir()
    main_script = script_dir / "main.py"

    print(f"🖥️  運行平台: {system}")
    print(f"📁 應用目錄: {script_dir}")
    print(f"🐍 Python 版本: {sys.version.split()[0]}")

    # 檢查 main.py 是否存在
    if not main_script.exists():
        print(f"\n❌ 錯誤：找不到 main.py")
        print(f"   預期位置: {main_script}")
        sys.exit(1)

    # 檢查依賴
    print("\n🔍 檢查依賴...")
    if not check_dependencies():
        sys.exit(1)

    print("\n✅ 依賴檢查完成\n")
    print("=" * 60)
    print("🚀 啟動批次檔案重新命名工具...")
    print("=" * 60 + "\n")

    # 運行應用
    python_exe = get_python_executable()

    try:
        # 在當前進程運行（不使用 subprocess，以便應用能訪問終端）
        if system in ["Windows", "Darwin", "Linux"]:
            # 使用 subprocess 以保持終端輸出
            result = subprocess.run(
                [python_exe, str(main_script)],
                cwd=str(script_dir),
            )
            sys.exit(result.returncode)
        else:
            print(f"❌ 不支持的平台: {system}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⛔ 應用已中止")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 運行時出錯: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
