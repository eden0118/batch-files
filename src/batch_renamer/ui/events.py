"""Event handlers for the Batch Renamer application"""

import flet as ft
from pathlib import Path
from typing import List, Tuple, Callable
from ..core.renamer import FileRenamer
from ..utils.constants import COLORS
from ..utils.strings import get_string


def create_event_handlers(
    page: ft.Page,
    renamer: FileRenamer,
    current_language: list,
    app_state: dict,
    refs: dict,
    get_targets: Callable,
    update_ui: Callable,
    reset_execute_button: Callable,
    set_status_banner: Callable,
    hide_step3_loading: Callable
):
    """建立所有事件處理函數"""

    def _get_text(key: str, *args, **kwargs) -> str:
        """簡化獲取字符串的方法"""
        return get_string(key, current_language[0], *args, **kwargs)

    def on_folder_picker_result(e: ft.FilePickerResultEvent) -> None:
        """資料夾選擇器回調"""
        if e.path:
            refs["selected_path"].value = e.path
            refs["selected_path"].update()
            update_ui()

    def on_reset_click(e=None) -> None:
        """重設按鈕"""
        if app_state["is_executing"]:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(_get_text("alert_cant_reset")),
                bgcolor="orange"
            )
            page.snack_bar.open = True
            page.update()
            return

        refs["selected_path"].value = ""
        refs["rename_mode"].value = "files"
        refs["filter_type"].value = "all"
        refs["filter_ext"].value = ""
        refs["op_mode"].value = "s2t"
        refs["replace_from"].value = ""
        refs["replace_to"].value = ""
        refs["remove_sym_input"].value = ""
        refs["prefix_input"].value = ""
        refs["suffix_input"].value = ""
        refs["preview_log"].controls = []
        refs["live_preview_container"].controls = []

        reset_execute_button()
        set_status_banner("idle", _get_text("status_reset"))

        page.update()

    def on_execute_click(e=None) -> None:
        """執行按鈕點擊事件"""
        if app_state["is_executing"]:
            return

        targets = app_state["targets"]
        changed = [t for t in targets if t[0].name != t[1]]

        if not changed:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(_get_text("alert_no_changes")),
                bgcolor="orange"
            )
            page.snack_bar.open = True
            page.update()
            return

        if not app_state["confirming"]:
            app_state["confirming"] = True
            refs["btn_execute"].text = _get_text("exec_btn_confirm")
            refs["btn_execute"].bgcolor = COLORS["red"]
            refs["btn_execute"].color = "white"
            refs["btn_execute"].icon = ft.Icons.WARNING
            refs["btn_execute"].update()
        else:
            app_state["is_executing"] = True
            refs["btn_execute"].disabled = True
            refs["btn_execute"].text = _get_text("exec_btn_renaming")
            refs["btn_execute"].bgcolor = "grey700"
            refs["btn_execute"].update()

            log_lines = [ft.Text(_get_text("execution_start"), color=COLORS["accent"])]
            refs["preview_log"].controls = log_lines
            refs["preview_log"].update()
            page.update()

            try:
                success, failed = renamer.execute_rename(targets)

                log_lines = [
                    ft.Text(_get_text("execution_start"), color=COLORS["accent"]),
                    ft.Text(_get_text("execution_progress", success, 0), color=COLORS["text_dim"], size=13),
                    ft.Text(_get_text("execution_complete", success), weight="bold", color="green")
                ]

            finally:
                app_state["is_executing"] = False
                reset_execute_button()
                update_ui()
                refs["preview_log"].controls = log_lines
                refs["preview_log"].update()

                page.snack_bar = ft.SnackBar(
                    content=ft.Text(_get_text("alert_success", success)),
                    bgcolor="green"
                )
                page.snack_bar.open = True
                page.update()

    def on_show_full_preview(e=None) -> None:
        """顯示完整預覽"""
        targets = get_targets()
        log_lines = [ft.Text(_get_text("preview_mode"), color="yellow")]

        for item, new_name in targets:
            if item.name != new_name:
                log_lines.append(ft.Row([
                    ft.Text(item.name, color="grey", selectable=True, expand=True),
                    ft.Text(" → ", color=COLORS["accent"], size=12, weight="bold"),
                    ft.Text(new_name, color=COLORS["accent"], weight="bold", selectable=True, expand=True)
                ], spacing=8))

        refs["preview_log"].controls = log_lines
        refs["preview_log"].update()

    def on_language_change(e=None) -> None:
        """語言切換"""
        lang = "zh" if current_language[0] == "en" else "en"
        current_language[0] = lang
        page.clean()
        # 觸發重建（會在 main 中呼叫）
        page.session.set("rebuild_ui", True)
        page.update()

    return {
        "on_folder_picker_result": on_folder_picker_result,
        "on_reset_click": on_reset_click,
        "on_execute_click": on_execute_click,
        "on_show_full_preview": on_show_full_preview,
        "on_language_change": on_language_change
    }
