"""UI Strings Management - 中英文字符串管理"""

# 語言代碼
LANGUAGES = {
    "en": "English",
    "zh": "繁體中文"
}

# 所有 UI 字符串
STRINGS = {
    "en": {
        # 應用標題
        "app_title": "Renamer v1.4",
        "app_subtitle": "Batch File Renaming Tool",

        # Step 1: Source Folder
        "step1_title": "Step 1: Source Folder",
        "step1_input_label": "Paste Path Here",
        "step1_btn_load": "Load Folder",
        "step1_radio_files": "Files Only",
        "step1_radio_both": "Files & Folders",

        # Step 2: Filter
        "step2_title": "Step 2: Filter",
        "step2_radio_all": "All Files",
        "step2_radio_ext": "Specific Ext",
        "step2_filter_hint": "jpg, png, txt, flac, mp4",

        # Step 3: Operation
        "step3_title": "Step 3: Operation",
        "step3_option_none": "No Operation",
        "step3_option_replace": "Replace Text",
        "step3_option_s2t": "Simplified -> Traditional",
        "step3_find_label": "Find",
        "step3_replace_label": "Replace",
        "step3_loading": "Loading...",
        "step3_refresh_btn": "Refresh",
        "step3_refresh_hint": "Click Refresh after changing operation mode",

        # Step 4: Formatting
        "step4_title": "Step 4: Formatting",
        "step4_remove_symbols": "Remove Symbols",
        "step4_remove_hint": "!@#$%",
        "step4_prefix": "Prefix",
        "step4_suffix": "Suffix",
        "step4_preview": "Live Preview :",

        # Right Column: Execution & Log
        "exec_title": "Execution & Log",
        "exec_status_waiting": "Waiting...",
        "exec_btn_preview": "Show Full Preview",
        "exec_btn_execute": "Execute Rename",
        "exec_btn_confirm": "Confirm Rename",
        "exec_btn_renaming": "Renaming...",

        # Status Messages
        "status_idle": "No changes detected",
        "status_ready": "Ready: {} file(s) will be renamed",
        "status_warning": "Found {} files | Changes: {} file(s)",
        "status_reset": "All settings have been reset",
        "status_executing": "Executing",

        # Alerts
        "alert_no_changes": "No changes to apply!",
        "alert_success": "Success! {} file(s) renamed",
        "alert_cant_reset": "Cannot reset while renaming!",
        "alert_no_files": "No matching files found",

        # Preview Mode
        "preview_mode": "--- Preview Mode ---",
        "execution_start": "--- Execution Started ---",
        "execution_complete": "--- Completed: {} file(s) renamed ---",
        "execution_progress": "Successfully renamed: {} | Remaining: {} ",
        "execution_error": "[ERR] {}: {}",

        # Buttons & Actions
        "btn_reset": "Reset all settings",
        "btn_language": "Language",
    },

    "zh": {
        # 應用標題
        "app_title": "Renamer v1.4",
        "app_subtitle": "批次檔案重新命名工具",

        # Step 1: Source Folder
        "step1_title": "步驟 1: 選擇資料夾",
        "step1_input_label": "粘貼路徑在此",
        "step1_btn_load": "載入資料夾",
        "step1_radio_files": "僅檔案",
        "step1_radio_both": "檔案及資料夾",

        # Step 2: Filter
        "step2_title": "步驟 2: 篩選",
        "step2_radio_all": "全部檔案",
        "step2_radio_ext": "特定副檔名",
        "step2_filter_hint": "jpg, png, txt, flac, mp4",

        # Step 3: Operation
        "step3_title": "步驟 3: 操作",
        "step3_option_none": "無操作",
        "step3_option_replace": "文本替換",
        "step3_option_s2t": "簡體轉繁體",
        "step3_find_label": "目標",
        "step3_replace_label": "替換成",
        "step3_loading": "加載中...",
        "step3_refresh_btn": "重新整理",
        "step3_refresh_hint": "切換操作模式後請點擊重新整理",

        # Step 4: Formatting
        "step4_title": "步驟 4: 格式化",
        "step4_remove_symbols": "移除符號",
        "step4_remove_hint": "!@#$%^&*()_+-=[]|;:',.<>/?",
        "step4_prefix": "前綴",
        "step4_suffix": "後綴",
        "step4_preview": "即時預覽 :",

        # Right Column: Execution & Log
        "exec_title": "執行日誌",
        "exec_status_waiting": "等候中...",
        "exec_btn_preview": "顯示完整預覽",
        "exec_btn_execute": "執行重新命名",
        "exec_btn_confirm": "確認重新命名",
        "exec_btn_renaming": "正在重新命名...",

        # Status Messages
        "status_idle": "未偵測到變化",
        "status_ready": "準備就緒: {} 個檔案將被重命名",
        "status_warning": "找到 {} 個檔案 | 變更: {} 個",
        "status_reset": "已重設所有設定",
        "status_executing": "正在執行",

        # Alerts
        "alert_no_changes": "沒有變化可應用!",
        "alert_success": "成功! {} 個檔案已重命名",
        "alert_cant_reset": "正在轉換中，無法重設!",
        "alert_no_files": "未找到符合條件的檔案",

        # Preview Mode
        "preview_mode": "--- 預覽模式 ---",
        "execution_start": "--- 執行開始 ---",
        "execution_complete": "--- 完成: {} 個檔案已重命名 ---",
        "execution_progress": "已轉換成功 {} 個，剩餘 {} 個",
        "execution_error": "[ERR] {}: {}",

        # Buttons & Actions
        "btn_reset": "重設所有設定",
        "btn_language": "語言",
    }
}


def get_string(key: str, language: str = "en", *args, **kwargs) -> str:
    """
    獲取指定語言的字符串

    Args:
        key: 字符串鍵名
        language: 語言代碼 ("en" 或 "zh")
        *args: 用於字符串位置格式化的參數
        **kwargs: 用於字符串關鍵字格式化的參數

    Returns:
        格式化後的字符串

    Examples:
        get_string("status_ready", "en", 5)  # 位置參數
        get_string("status_ready", "en", changed_count=5)  # 關鍵字參數
    """
    if language not in STRINGS:
        language = "en"

    string = STRINGS[language].get(key, key)

    # 支持字符串格式化
    if args or kwargs:
        try:
            if args:
                return string.format(*args, **kwargs)
            else:
                return string.format(**kwargs)
        except (KeyError, ValueError, IndexError):
            return string

    return string


def get_all_strings(language: str = "en") -> dict:
    """獲取指定語言的所有字符串"""
    if language not in STRINGS:
        language = "en"
    return STRINGS[language]
