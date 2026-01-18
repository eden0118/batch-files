#!/usr/bin/env python3
"""
Batch File Renaming Tool - Internationalization (i18n)
Multilingual language definitions and translations
"""
from typing import Dict

LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {
        # Window & Main
        "app_title": "Batch File Renaming",
        "toggle_language": "中文",

        # Step Headers
        "step_01": "Step 01: Choose Folder",
        "step_02": "Step 02: File Filter",
        "step_03": "Step 03: Operation",
        "step_04": "Step 04: Format Settings",
        "step_05": "Step 05: Preview Changes",
        "step_06": "Step 06: Confirm & Execute",

        # Step 01 - Choose Folder
        "select_dir": "Select Folder",
        "selected_dir": "No folder selected",
        "rename_mode": "Rename Mode:",
        "mode_files": "Files Only",
        "mode_folders": "Folders Only",
        "mode_both": "Files & Folders",

        # Step 02 - File Filter
        "all_files": "All Files",
        "specific_type": "Specific Type",
        "example_ext": "e.g., .jpg, .png, .txt, .flac",

        # Step 03 - Operation
        "s2t_convert": "Convert Zh-SC to Zh-TW",
        "replace_text": "Replace Text",
        "replace_from": "From:",
        "replace_to": "To:",

        # Step 04 - Format Settings
        "remove_symbols": "Remove Symbols:",
        "default_symbols": "!@#$%^&*()",
        "add_prefix": "Add Prefix:",
        "add_suffix": "Add Suffix:",
        "add_index": "Add Index (_001, _002...)",
        "preview_format": "Preview Format:",
        "format_preview": "No files selected",

        # Step 05 - Preview Changes
        "show_preview": "Show Changes",
        "no_changes": "No files to rename",

        # Preview Output Section
        "preview_output_title": "PREVIEW OUTPUT",

        # Terminal Section
        "terminal_title": "◇ LIVE_TERMINAL_FEED",

        # Step 06 - Confirm & Execute
        "confirm_rename": "Confirm & Rename",
        "processing_log": "Log:",

        # Defaults
        "default_extensions": ".jpg, .png, .pdf",

        # Log Messages
        "log_started": "Processing started...",
        "log_found_files": "Found {} files",
        "log_success": "{} → {}",
        "log_error": "Error: {}",
        "log_completed": "Completed",
        "log_success_count": "Success: {}",
        "log_failed_count": "Failed: {}",

        # Dialogs
        "error": "Error",
        "no_dir_selected": "Please select a directory",
        "no_extension": "Please enter file types",
        "info": "Information",
        "no_files": "No files found",
        "completed": "Done",
        "completed_msg": "Renamed: {}\nFailed: {}",

        # Confirmation Dialog
        "confirm_count": "Will rename {} files\n\nConfirm execution?",
        "execution_cancelled": "Execution cancelled",
        "preview_mode": "(Preview Mode - Not Yet Executed)",
    },

    "zh": {
        # Window & Main
        "app_title": "批次重新命名",
        "toggle_language": "English",

        # Step Headers
        "step_01": "步驟 01：選擇資料夾",
        "step_02": "步驟 02：檔案篩選",
        "step_03": "步驟 03：選擇操作",
        "step_04": "步驟 04：格式設定",
        "step_05": "步驟 05：預覽變更",
        "step_06": "步驟 06：確認並執行",

        # Step 01 - Choose Folder
        "select_dir": "選擇資料夾",
        "selected_dir": "未選擇資料夾",
        "rename_mode": "重新命名模式：",
        "mode_files": "只有檔案",
        "mode_folders": "只有資料夾",
        "mode_both": "檔案和資料夾",

        # Step 02 - File Filter
        "all_files": "全部檔案",
        "specific_type": "特定類型",
        "example_ext": "例：.jpg, .png, .txt, .flac",

        # Step 03 - Operation
        "s2t_convert": "簡轉繁",
        "replace_text": "替換文字",
        "replace_from": "從：",
        "replace_to": "到：",

        # Step 04 - Format Settings
        "remove_symbols": "移除符號：",
        "default_symbols": "!@#$%^&*()",
        "add_prefix": "添加前綴：",
        "add_suffix": "添加後綴：",
        "add_index": "添加序號 (_001, _002...)",
        "preview_format": "格式預覽：",
        "format_preview": "未選擇檔案",

        # Step 05 - Preview Changes
        "show_preview": "顯示變更",
        "no_changes": "沒有檔案需要重新命名",

        # Preview Output Section
        "preview_output_title": "預覽輸出",

        # Terminal Section
        "terminal_title": "◇ 即時終端",

        # Step 06 - Confirm & Execute
        "confirm_rename": "確認並重新命名",
        "processing_log": "日誌：",

        # Defaults
        "default_extensions": ".jpg, .png, .pdf",

        # Log Messages
        "log_started": "開始處理...",
        "log_found_files": "找到 {} 個檔案",
        "log_success": "{} → {}",
        "log_error": "錯誤：{}",
        "log_completed": "完成",
        "log_success_count": "成功：{}",
        "log_failed_count": "失敗：{}",

        # Dialogs
        "error": "錯誤",
        "no_dir_selected": "請選擇資料夾",
        "no_extension": "請輸入檔案類型",
        "info": "資訊",
        "no_files": "找不到檔案",
        "completed": "完成",
        "completed_msg": "已重新命名：{}\n失敗：{}",

        # Confirmation Dialog
        "confirm_count": "將重新命名 {} 個檔案\n\n確定要執行嗎？",
        "execution_cancelled": "已取消執行",
        "preview_mode": "（預覽模式 - 未執行）",
    }
}

DEFAULT_LANGUAGE = "en"
