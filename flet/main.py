"""
Batch Renamer v4.4 - GUI File Renaming Application
支持繁簡轉換、文本替換、前綴後綴、符號移除等功能
"""

import flet as ft
import os
from pathlib import Path
from typing import List, Tuple

# ============================================================================
# GLOBAL CONFIGURATION & INITIALIZATION
# ============================================================================

# 簡體轉繁體微型字典 (OpenCC 備用方案)
SIMPLIFIED_TO_TRADITIONAL = str.maketrans({
    '国': '國', '爱': '愛', '华': '華', '宝': '寶', '电': '電', '开': '開', '关': '關',
    '医': '醫', '车': '車', '书': '書', '听': '聽', '发': '發', '门': '門', '专': '專',
    '难': '難', '业': '業', '东': '東', '画': '畫', '写': '寫', '马': '馬', '鸟': '鳥',
    '儿': '兒', '语': '語', '头': '頭', '见': '見', '气': '氣', '长': '長', '实': '實',
    '后': '後', '机': '機', '权': '權', '变': '變', '现': '現', '务': '務', '际': '際'
})

# 初始化 OpenCC (簡轉繁工具)
HAS_OPENCC = False
OPENCC_CONVERTER = None
OPENCC_STATUS = "Init..."

try:
    from opencc import OpenCC
    for config in ['s2t', 's2t.json', 't2s', 't2s.json']:
        try:
            temp_cc = OpenCC(config)
            if temp_cc.convert('国') == '國':
                OPENCC_CONVERTER = temp_cc
                HAS_OPENCC = True
                OPENCC_STATUS = f"Active ({config})"
                break
        except:
            continue
    if not HAS_OPENCC:
        OPENCC_STATUS = "Missing (Fallback Active)"
except ImportError:
    OPENCC_STATUS = "Module Missing"



# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main(page: ft.Page):
    """主應用入口點"""

    # ===== PAGE SETUP =====
    page.title = "Renamer v1.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # ===== COLOR PALETTE =====
    COLORS = {
        "bg": "#111827",
        "sidebar": "#0f172a",
        "accent": "#2dd4bf",
        "card": "#1e293b",
        "text_dim": "#94a3b8",
        "red": "#ef4444",
    }

    # ===== UI COMPONENT REFERENCES =====
    selected_path = ft.Ref[ft.TextField]()
    rename_mode = ft.Ref[ft.RadioGroup]()
    filter_type = ft.Ref[ft.RadioGroup]()
    filter_ext = ft.Ref[ft.TextField]()
    op_mode = ft.Ref[ft.Dropdown]()
    replace_from = ft.Ref[ft.TextField]()
    replace_to = ft.Ref[ft.TextField]()
    remove_sym_input = ft.Ref[ft.TextField]()
    prefix_input = ft.Ref[ft.TextField]()
    suffix_input = ft.Ref[ft.TextField]()
    preview_log = ft.Ref[ft.Column]()
    live_preview_container = ft.Ref[ft.Column]()
    status_banner = ft.Ref[ft.Container]()
    btn_execute = ft.Ref[ft.ElevatedButton]()

    # ===== APPLICATION STATE =====
    app_state = {
        "confirming": False,  # 執行確認狀態
        "targets": [],  # 待處理文件清單
        "is_executing": False  # 正在執行重命名
    }

    # ========================================================================
    # CORE LOGIC FUNCTIONS
    # ========================================================================

    def _apply_conversion(name: str, operation: str) -> str:
        """
        應用文字轉換操作

        Args:
            name: 原始名稱
            operation: 操作類型 ("s2t" = 簡轉繁, "replace" = 替換, "none" = 無)

        Returns:
            轉換後的名稱
        """
        if operation == "s2t":
            # 優先使用 OpenCC，失敗則用微型字典
            if HAS_OPENCC and OPENCC_CONVERTER:
                converted = OPENCC_CONVERTER.convert(name)
                if converted != name:
                    return converted
            return name.translate(SIMPLIFIED_TO_TRADITIONAL)

        elif operation == "replace":
            find_text = replace_from.current.value
            replace_text = replace_to.current.value
            if find_text:
                return name.replace(find_text, replace_text)

        return name

    def _apply_formatting(item: Path, name: str) -> str:
        """
        應用文件名格式化 (移除符號、添加前綴後綴)

        Args:
            item: 路徑對象
            name: 名稱

        Returns:
            格式化後的名稱
        """
        # 移除指定符號
        symbols_to_remove = remove_sym_input.current.value
        if symbols_to_remove:
            for char in symbols_to_remove:
                name = name.replace(char, "")

        # 添加前綴後綴
        prefix = prefix_input.current.value or ""
        suffix = suffix_input.current.value or ""

        if item.is_file():
            # 文件：保持副檔名
            stem = Path(name).stem
            ext = Path(name).suffix
            return f"{prefix}{stem}{suffix}{ext}"
        else:
            # 資料夾：直接添加
            return f"{prefix}{name}{suffix}"

    def _update_live_preview(targets: List[Tuple[Path, str]]) -> None:
        """更新即時預覽 (顯示前3個)"""
        controls = []
        for item, new_name in targets[:1]:
            color = COLORS["accent"] if item.name != new_name else "grey"
            controls.append(
                ft.Text(f"{item.name}  →  {new_name}", color=color, font_family="monospace")
            )

        if not targets:
            controls.append(ft.Text("沒有符合條件的文件", color="orange"))

        live_preview_container.current.controls = controls
        live_preview_container.current.update()

    def _update_status_banner(targets: List[Tuple[Path, str]]) -> None:
        """更新狀態橫幅"""
        changed_count = sum(1 for t in targets if t[0].name != t[1])
        total_count = len(targets)

        # 檢查文件數量是否超過 300
        if total_count > 300:
            status_msg = f"找到 {total_count} 個文件| 變更: {changed_count} 個"
            _set_status_banner("warning", status_msg)
        elif changed_count > 0:
            status_msg = f"準備就緒: {changed_count} 個文件將被重命名"
            _set_status_banner("ready", status_msg)
        else:
            _set_status_banner("idle", f"無變化偵測 ({OPENCC_STATUS})")

    def _update_input_states() -> None:
        """根據選項動態啟用/禁用輸入欄"""
        # 替換模式的輸入欄
        is_replace = op_mode.current.value == "replace"
        replace_from.current.disabled = not is_replace
        replace_to.current.disabled = not is_replace

        # 副檔名篩選輸入欄
        is_ext = filter_type.current.value == "ext"
        filter_ext.current.disabled = not is_ext

    def update_ui(e=None) -> None:
        """
        主要 UI 更新函數 (事件處理器)
        - 獲取目標文件
        - 更新預覽
        - 更新狀態橫幅
        - 更新輸入欄狀態
        """
        _reset_execute_button()
        targets = get_targets()
        app_state["targets"] = targets

        _update_live_preview(targets)
        _update_status_banner(targets)
        _update_input_states()

        page.update()

    def _set_status_banner(status_type: str, message: str) -> None:
        """設置狀態橫幅顏色和圖示"""
        status_config = {
            "idle": {"color": "grey700", "icon": ft.Icons.INFO_OUTLINE},
            "ready": {"color": "green700", "icon": ft.Icons.CHECK_CIRCLE_OUTLINE},
            "warning": {"color": "orange700", "icon": ft.Icons.WARNING_AMBER_ROUNDED},
            "error": {"color": "red700", "icon": ft.Icons.ERROR_OUTLINE}
        }

        config = status_config.get(status_type, status_config["idle"])
        status_banner.current.content = ft.Row([
            ft.Icon(config["icon"], color="white"),
            ft.Text(message, color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER)
        status_banner.current.bgcolor = config["color"]
        status_banner.current.update()

    def _reset_execute_button() -> None:
        """將執行按鈕重置為初始狀態"""
        app_state["confirming"] = False
        btn_execute.current.text = "Execute Rename"
        btn_execute.current.bgcolor = COLORS["accent"]
        btn_execute.current.color = "black"
        btn_execute.current.icon = ft.Icons.ROCKET_LAUNCH
        btn_execute.current.update()

    def on_execute_click(e) -> None:
        """
        執行按鈕點擊事件
        - 首次點擊：顯示確認狀態
        - 二次點擊：執行重命名
        """
        # 防止重複點擊
        if app_state["is_executing"]:
            return

        targets = app_state["targets"]
        changed = [t for t in targets if t[0].name != t[1]]

        if not changed:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("沒有變化可應用!"),
                bgcolor="orange"
            )
            page.snack_bar.open = True
            page.update()
            return

        # 首次點擊 - 顯示確認狀態
        if not app_state["confirming"]:
            app_state["confirming"] = True
            btn_execute.current.text = f"確認重新命名"
            btn_execute.current.bgcolor = COLORS["red"]
            btn_execute.current.color = "white"
            btn_execute.current.icon = ft.Icons.WARNING
            btn_execute.current.update()

        # 二次點擊 - 執行重命名
        else:
            # 進入 loading 狀態
            app_state["is_executing"] = True
            btn_execute.current.disabled = True
            btn_execute.current.text = "正在重新命名..."
            btn_execute.current.bgcolor = "grey700"
            btn_execute.current.update()
            page.update()

            success = 0
            log_lines = [ft.Text("--- 執行開始 ---", color=COLORS["accent"])]

            try:
                for old, new in targets:
                    if old.name == new:
                        continue
                    try:
                        os.rename(old, old.parent / new)
                        success += 1
                        log_lines.append(
                            ft.Text(f"[OK] {old.name} -> {new}", color="green", font_family="monospace")
                        )
                    except Exception as ex:
                        log_lines.append(
                            ft.Text(f"[ERR] {old.name}: {ex}", color="red", font_family="monospace")
                        )

                log_lines.append(
                    ft.Text(f"--- 完成: {success} 個文件已重命名 ---", weight="bold")
                )

            finally:
                # 恢復狀態
                app_state["is_executing"] = False
                _reset_execute_button()
                update_ui()
                preview_log.current.controls = log_lines
                preview_log.current.update()

                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"成功! {success} 個文件已重命名"),
                    bgcolor="green"
                )
                page.snack_bar.open = True
                page.update()

    def on_show_full_preview(e) -> None:
        """顯示完整預覽"""
        targets = get_targets()
        log_lines = [ft.Text("--- 預覽模式 ---", color="yellow")]

        for item, new_name in targets:
            if item.name != new_name:
                log_lines.append(ft.Row([
                    ft.Text(item.name, color="grey"),
                    ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=COLORS["accent"]),
                    ft.Text(new_name, color="white", weight="bold")
                ]))

        preview_log.current.controls = log_lines
        preview_log.current.update()

    # ========================================================================
    # FILE PICKER SETUP
    # ========================================================================

    def on_folder_picker_result(e: ft.FilePickerResultEvent) -> None:
        """資料夾選擇器回調"""
        if e.path:
            selected_path.current.value = e.path
            selected_path.current.update()
            update_ui()

    file_picker = ft.FilePicker(on_result=on_folder_picker_result)
    page.overlay.append(file_picker)

    # ========================================================================
    # HELPER: GET TARGETS
    # ========================================================================

    def get_targets() -> List[Tuple[Path, str]]:
        """
        遞歸掃描目標資料夾及其子資料夾，生成重命名配對

        Returns:
            [(原始路徑, 新名稱), ...] 列表（包含所有層級）
        """
        raw_path = selected_path.current.value
        if not raw_path:
            return []

        p = Path(raw_path.strip())
        if not p.exists():
            return []

        targets = []
        mode = rename_mode.current.value
        f_type = filter_type.current.value

        # 解析副檔名過濾器
        valid_exts = []
        if filter_ext.current.value:
            valid_exts = [e.strip().lower() for e in filter_ext.current.value.split(',')]

        def _scan_recursive(directory: Path) -> None:
            """遞歸掃描資料夾及其所有子資料夾"""
            try:
                for item in directory.iterdir():
                    # 跳過隱藏文件和資料夾
                    if item.name.startswith('.'):
                        continue

                    # 如果是資料夾，遞歸進入
                    if item.is_dir():
                        if mode != "files":
                            # 如果需要重命名資料夾，則處理
                            new_name = item.name

                            # 1. 應用文字轉換
                            operation = op_mode.current.value
                            new_name = _apply_conversion(new_name, operation)

                            # 2. 應用格式化
                            new_name = _apply_formatting(item, new_name)

                            targets.append((item, new_name))

                        # 遞歸掃描子資料夾
                        _scan_recursive(item)

                    # 如果是文件
                    else:
                        # 副檔名篩選
                        if f_type == "ext" and valid_exts:
                            if item.suffix.lower() not in valid_exts:
                                continue

                        new_name = item.name

                        # 1. 應用文字轉換
                        operation = op_mode.current.value
                        new_name = _apply_conversion(new_name, operation)

                        # 2. 應用格式化
                        new_name = _apply_formatting(item, new_name)

                        targets.append((item, new_name))

            except Exception as e:
                print(f"掃描錯誤 ({directory}): {e}")

        # 開始遞歸掃描
        _scan_recursive(p)

        return targets

    # ========================================================================
    # UI COMPONENTS ASSEMBLY
    # ========================================================================

    # --- STEP 1: SOURCE FOLDER ---
    step1 = ft.Container(
        content=ft.Column([
            ft.Text("Step 1: Source Folder", size=18, weight=ft.FontWeight.BOLD),
            ft.TextField(
                ref=selected_path,
                label="Paste Path Here",
                expand=True, dense=True,
                border_color=COLORS["accent"], bgcolor="black",
                on_submit=update_ui
            ),
            ft.Row([
                ft.ElevatedButton(
                    "Load Folder",
                    icon=ft.Icons.REFRESH,
                    bgcolor=COLORS["accent"], color="black",
                    on_click=update_ui,
                    height=40, expand=True
                )
            ]),
            ft.RadioGroup(
                ref=rename_mode,
                value="files",
                content=ft.Row([
                    ft.Radio(value="files", label="Files Only", fill_color=COLORS["accent"]),
                    ft.Radio(value="both", label="Files & Folders", fill_color=COLORS["accent"])
                ]),
                on_change=update_ui
            )
        ], spacing=15),
        padding=15, bgcolor=COLORS["card"], border_radius=10
    )

    # --- STEP 2: FILTER ---
    step2 = ft.Container(
        content=ft.Column([
            ft.Text("Step 2: Filter", size=18, weight=ft.FontWeight.BOLD),
            ft.RadioGroup(
                ref=filter_type,
                value="all",
                content=ft.Row([
                    ft.Radio(value="all", label="All Files", fill_color=COLORS["accent"]),
                    ft.Radio(value="ext", label="Specific Ext", fill_color=COLORS["accent"])
                ]),
                on_change=update_ui
            ),
            ft.TextField(
                ref=filter_ext,
                hint_text="jpg, png, txt",
                disabled=True,
                dense=True,
                on_change=update_ui
            )
        ], spacing=10),
        padding=15, bgcolor=COLORS["card"], border_radius=10
    )

    # --- STEP 3: OPERATION ---
    step3 = ft.Container(
        content=ft.Column([
            ft.Text("Step 3: Operation", size=18, weight=ft.FontWeight.BOLD),
            ft.Dropdown(
                ref=op_mode,
                value="s2t",
                options=[
                    ft.dropdown.Option("none", "No Operation"),
                    ft.dropdown.Option("replace", "Replace Text"),
                    ft.dropdown.Option("s2t", "Simplified -> Traditional")
                ],
                border_color=COLORS["accent"],
                dense=True, expand=True,
                on_change=update_ui
            ),
            ft.Row([
                ft.TextField(
                    ref=replace_from,
                    label="Find",
                    expand=True, disabled=True,
                    dense=True,
                    on_change=update_ui
                ),
                ft.TextField(
                    ref=replace_to,
                    label="Replace",
                    expand=True, disabled=True,
                    dense=True,
                    on_change=update_ui
                )
            ])
        ], spacing=10),
        padding=15, bgcolor=COLORS["card"], border_radius=10
    )

    # --- STEP 4: FORMATTING ---
    step4 = ft.Container(
        content=ft.Column([
            ft.Text("Step 4: Formatting", size=18, weight=ft.FontWeight.BOLD),
            ft.TextField(
                ref=remove_sym_input,
                label="Remove Symbols",
                value="",
                hint_text="!@#$%",
                dense=True,
                on_change=update_ui
            ),
            ft.Row([
                ft.TextField(
                    ref=prefix_input,
                    label="Prefix",
                    expand=True, dense=True,
                    on_change=update_ui
                ),
                ft.TextField(
                    ref=suffix_input,
                    label="Suffix",
                    expand=True, dense=True,
                    on_change=update_ui
                )
            ]),
            ft.Divider(),
            ft.Text("Live Preview :", color=COLORS["text_dim"]),
            ft.Column(ref=live_preview_container)
        ], spacing=10),
        padding=15, bgcolor=COLORS["card"], border_radius=10
    )

    # --- RIGHT COLUMN: EXECUTION & LOG ---
    status_display = ft.Container(
        ref=status_banner,
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_OUTLINE, color="white"),
            ft.Text("Waiting...", color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor="grey700", padding=10, border_radius=8
    )

    action_buttons = ft.Row([
        ft.Container(
            content=ft.ElevatedButton(
                "Show Full Preview",
                icon=ft.Icons.VISIBILITY,
                on_click=on_show_full_preview,
                style=ft.ButtonStyle(color=COLORS["accent"], bgcolor=COLORS["card"])
            ),
            height=50, expand=True
        ),
        ft.Container(
            content=ft.ElevatedButton(
                ref=btn_execute,
                text="Execute Rename",
                icon=ft.Icons.ROCKET_LAUNCH,
                on_click=on_execute_click,
                style=ft.ButtonStyle(color="black", bgcolor=COLORS["accent"])
            ),
            height=50, expand=True
        )
    ], spacing=10)

    log_area = ft.Container(
        content=ft.Column(ref=preview_log, scroll=ft.ScrollMode.AUTO),
        bgcolor="black",
        border=ft.border.all(1, "grey"),
        border_radius=5,
        padding=10,
        expand=True
    )

    right_column = ft.Column([
        ft.Text("Execution & Log", size=18, weight=ft.FontWeight.BOLD),
        status_display,
        action_buttons,
        log_area
    ], spacing=15, expand=True)

    step_actions = ft.Container(
        content=right_column,
        padding=15, bgcolor=COLORS["card"], border_radius=10,
        expand=True
    )

    # --- MAIN LAYOUT ---
    main_content = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE, color=COLORS["accent"], size=32),
            ft.Column([
                ft.Text("Renamer", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("v1.0 • Batch File Renaming Tool", size=11, color=COLORS["text_dim"])
            ], spacing=2)
        ], spacing=15, alignment=ft.MainAxisAlignment.START),
        ft.Container(height=25),
        ft.Row([
            ft.Column(
                [step1, step2, step3, step4],
                expand=6, spacing=15,
                scroll=ft.ScrollMode.AUTO
            ),
            ft.Column([step_actions], expand=6)
        ], vertical_alignment=ft.CrossAxisAlignment.STRETCH, spacing=20, expand=True)
    ], expand=True)

    content = ft.Container(
        expand=True,
        bgcolor=COLORS["bg"],
        padding=30,
        content=main_content
    )

    # --- RENDER PAGE ---
    page.add(content)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
