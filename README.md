# Batch Renamer

> Cross-platform batch file renaming tool with support for text conversion, replacement, symbol removal, and prefix/suffix operations.

![Version](https://img.shields.io/badge/version-1.4-blue)
![Python](https://img.shields.io/badge/python-3.10+-brightgreen)
![Framework](https://img.shields.io/badge/framework-Flet-2dd4bf)
![License](https://img.shields.io/badge/license-MIT-green)

[中文版本](#chinese-version) | [English](#english-version)

---

## Core Features

- **Simplified to Traditional Chinese**: Automatically convert Simplified Chinese to Traditional Chinese in filenames (OpenCC or fallback dictionary)
- **Text Replacement**: Batch replace specified text in filenames
- **Symbol Removal**: Remove specific symbols from filenames
- **Prefix & Suffix**: Add prefix and suffix to filenames
- **Live Preview**: View all renaming results before execution
- **Smart Filtering**: Filter by file extension
- **Multi-language Support**: English and Traditional Chinese
- **Detailed Logging**: Track the renaming process for each file

## System Requirements

- **Python**: 3.10 or higher
- **Operating System**: macOS 10.14+, Windows 10+, Linux
- **GUI Framework**: Flet (>=0.20.0)

## Quick Start

### Run from Source

**macOS/Linux:**
```bash
# Clone repository
git clone https://github.com/eden0118/batch-files.git
cd batch-files

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flet

# Run the application
python3 main.py
```

**Windows (PowerShell/CMD):**
```cmd
# Clone repository
git clone https://github.com/eden0118/batch-files.git
cd batch-files

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install flet

# Run the application
python main.py
```

## Usage Guide

### Basic Steps

1. **Select Folder**: Enter or browse the directory path to rename
2. **Set Filter** (Optional):
   - **Filter Type**: All files or specific extensions
   - **Extensions**: Input extensions (e.g., `txt,pdf,mp3`)
3. **Set Operation**:
   - **Conversion Mode**: None, Simplified to Traditional, Text Replace
   - **Formatting**: Remove symbols, add prefix/suffix
4. **Preview Results**: View live preview or full preview
5. **Execute**: Click "Execute Rename" and confirm

### Operation Modes

#### No Operation
Only apply formatting operations (prefix, suffix, symbol removal)

#### Simplified to Traditional
Convert Simplified Chinese to Traditional Chinese
- Prioritize OpenCC (more accurate)
- Use fallback dictionary if OpenCC unavailable

#### Text Replace
Directly replace specified text in filenames

## Project Structure

```
batch-files/
├── src/batch_renamer/
│   ├── __init__.py
│   ├── main.py                   # Module entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── renamer.py           # File renaming engine (business logic)
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py               # Flet GUI main application
│   │   ├── components.py        # Reusable UI components
│   │   └── events.py            # Event handlers
│   └── utils/
│       ├── __init__.py
│       ├── constants.py         # Constants definition (dicts, colors)
│       ├── converter.py         # Simplified/Traditional conversion tools
│       └── strings.py           # Multi-language strings
├── tests/
│   ├── __init__.py
│   └── test_renamer.py          # Unit tests
├── main.py                       # Application entry point
├── pyproject.toml               # Project configuration
├── requirements.txt             # Runtime dependencies
├── requirements-build.txt       # Build dependencies
├── build_mac.sh                 # macOS build script
├── build_win.bat                # Windows build script
├── build_spec.py                # PyInstaller configuration
└── README.md                    # This file
```

## Architecture Design

### Layered Structure

- **Core Layer** (`src/batch_renamer/core/`): Pure business logic, no UI dependencies, independently testable
- **UI Layer** (`src/batch_renamer/ui/`): Flet GUI, handles user interaction
- **Utils Layer** (`src/batch_renamer/utils/`): Shared tools and constants

### Main Classes

**FileRenamer**: Core renaming engine
- `scan_directory()`: Recursively scan directory
- `apply_conversion()`: Apply text conversion
- `apply_formatting()`: Apply formatting
- `execute_rename()`: Execute actual renaming

## Dependency Management

### Runtime Dependencies

```
flet>=0.20.0                 # GUI framework
```

### Optional Dependencies

```
opencc>=1.1.0                # Simplified/Traditional conversion (high precision)
```

### Development Dependencies

```
pytest>=7.0                  # Unit testing
pytest-cov>=4.0              # Test coverage
```

## Development

### Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install flet pytest
```

### Run Development Version

```bash
source venv/bin/activate
python3 main.py
```

### Code Standards

- **Naming**: snake_case (functions/variables), CamelCase (classes)
- **Type Hints**: Use `typing` module
- **Documentation**: Docstrings explaining function purpose

## Building

### macOS

```bash
source venv/bin/activate
pip install pyinstaller
chmod +x build_mac.sh
./build_mac.sh
```

**Output:**
- `dist/Batch Renamer.app` - Application bundle
- `dist/Batch Renamer.dmg` - DMG installer

**Status:** ✅ Tested and working

### Windows

```cmd
venv\Scripts\activate
pip install pyinstaller
build_win.bat
```

**Output:**
- `dist/Batch Renamer.exe` - Single executable file

**Status:** ⚠️ **Not yet tested** - Build script is configured but executable has not been tested on Windows systems. Please report any issues encountered during building or running on Windows.

## FAQ

**Q: Poor conversion quality for Simplified to Traditional?**
A: Install OpenCC for better accuracy:
```bash
pip install opencc
```

**Q: How to restore renamed files?**
A: Renaming operations cannot be undone. Back up important files in advance.

**Q: Permission issues on macOS?**
A: Remove the quarantine attribute:
``✅ Restructured project, separated business logic from UI
- ✅ Created modular architecture (Core/UI/Utils)
- ✅ Simplified app.py, improved maintainability
- ✅ Optimized constants.py, removed redundant dicts
- ✅ Integrated execute_rename() logic
- ✅ macOS build verified and working
- ⚠️ Windows build script added but not yet tested

### v1.4 (2026-01-19)
- Restructured project, separated business logic from UI
- Created modular architecture (Core/UI/Utils)
- Simplified app.py, improved maintainability
- Optimized constants.py, removed redundant dicts
- Integrated execute_rename() logic

### v1.0 (2026-01-18)
- Initial release
- Flet cross-platform GUI
- Core features: Simplified to Traditional, text replacement
- macOS and Windows build support

## License

MIT License - See LICENSE file for details

## Contributing

Issues and Pull Requests are welcome!

---

Last Updated: 2026-01-19

<a id="chinese-version"></a>

# 批次檔案重新命名工具

> 支援繁簡轉換、文本替換、符號移除、前綴後綴等功能的跨平台檔案批次重新命名工具

## 核心功能

- **簡體轉繁體**: 自動轉換檔案名稱中的簡體字為繁體字（OpenCC 或備用字典）
- **文本替換**: 批次替換檔案名稱中的指定文本
- **符號移除**: 移除檔案名稱中的特定符號字元
- **前綴後綴**: 為檔案名稱添加前綴和後綴
- **實時預覽**: 執行前查看所有重新命名結果
- **智能篩選**: 按副檔名進行篩選
- **多語言支援**: 中文 (繁體) 和英文
- **詳細日誌**: 記錄每個檔案的重新命名過程

## 系統需求

- **Python**: 3.10 或更高版本
- **作業系統**: macOS 10.14+, Windows 10+, Linux
- **GUI 框架**: Flet (>=0.20.0)

## 快速開始

### 從原始碼執行

```bash
git clone https://github.com/eden0118/batch-files.git
cd batch-files
python3 -m venv venv
source venv/bin/activate
pip install flet
python3 main.py
```

## 使用指南

### 基本步驟

1. **選擇資料夾**: 貼入或選擇要重新命名的目錄路徑
2. **設定篩選** (可選): 選擇全部檔案或特定副檔名
3. **設定操作**: 無、簡轉繁、文本替換
4. **設定格式**: 移除符號、添加前綴/後綴
5. **預覽結果**: 查看即時預覽或完整預覽
6. **執行**: 點選「執行重新命名」並確認

### 操作模式

#### 無操作
僅應用格式化操作（前綴、後綴、符號移除）

#### 簡轉繁
將簡體字轉換為繁體字
- 優先使用 OpenCC（更準確）
- 無 OpenCC 時使用備用字典

#### 文本替換
直接替換檔案名稱中的指定文本

## 變更日誌

### v1.4 (2026-01-19)
- 重構專案結構，分離業務邏輯與 UI
- 創建模組化架構 (Core/UI/Utils)
- 簡化 app.py，改善可維護性
- 優化 constants.py，移除冗餘字典
- 整合 execute_rename() 邏輯

### v1.0 (2026-01-18)
- 首個發行版本
- Flet 跨平台 GUI
- 簡轉繁、文本替換等核心功能
- macOS 和 Windows 編譯支援
