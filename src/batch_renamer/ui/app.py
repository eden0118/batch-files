"""Flet GUI application - Main entry point and UI layout"""

import flet as ft
from flet import app as flet_app
from pathlib import Path
from typing import List, Tuple, Dict, Any
from ..core.renamer import FileRenamer
from ..utils.constants import COLORS
from ..utils.converter import get_opencc_status
from ..utils.strings import get_string, LANGUAGES


def create_app() -> None:
    """Create and run the Flet application"""

    renamer = FileRenamer()

    def main(page: ft.Page):
        """Main application entry point"""

        page.title = "Renamer v1.4"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0

        # Application state
        current_language = ["en"]
        app_state: Dict[str, Any] = {
            "confirming": False,
            "targets": [],
            "is_executing": False,
            "is_loading": False
        }
        refs = {}

        # =====================================================================
        # HELPER FUNCTIONS
        # =====================================================================

        def _get_text(key: str, *args, **kwargs) -> str:
            """Get localized text string"""
            return get_string(key, current_language[0], *args, **kwargs)

        def _update_live_preview(targets: List[Tuple[Path, str]]) -> None:
            """Update live preview with changes highlighted"""
            controls = []

            if not targets:
                controls.append(ft.Text(_get_text("alert_no_files"), color="orange"))
            else:
                item, new_name = targets[0]

                if item.name == new_name:
                    controls.append(
                        ft.Text(item.name, color="grey", font_family="monospace")
                    )
                else:
                    operation = refs["op_mode"].value
                    find_text = refs["replace_from"].value if operation == "replace" else ""

                    if operation == "replace" and find_text and find_text in item.name:
                        parts = item.name.split(find_text)
                        preview_parts = []

                        for i, part in enumerate(parts):
                            if part:
                                preview_parts.append(
                                    ft.Text(part, color="grey", font_family="monospace", size=11)
                                )
                            if i < len(parts) - 1:
                                preview_parts.append(
                                    ft.Text(find_text, color=COLORS["accent"], font_family="monospace", size=11, weight="bold")
                                )

                        controls.append(ft.Row(preview_parts, spacing=0))
                    else:
                        controls.append(
                            ft.Text(item.name, color="grey", font_family="monospace", size=11)
                        )

                    controls.append(
                        ft.Row([
                            ft.Text(" → ", color=COLORS["accent"], size=11),
                            ft.Text(new_name, color=COLORS["accent"], weight="bold", font_family="monospace", size=11)
                        ], spacing=0)
                    )

            refs["live_preview_container"].controls = controls
            refs["live_preview_container"].update()

        def _update_status_banner(targets: List[Tuple[Path, str]]) -> None:
            """Update status banner"""
            changed_count = sum(1 for t in targets if t[0].name != t[1])
            total_count = len(targets)

            if total_count > 300:
                status_msg = _get_text("status_warning", total_count, changed_count)
                _set_status_banner("warning", status_msg)
            elif changed_count > 0:
                status_msg = _get_text("status_ready", changed_count)
                _set_status_banner("ready", status_msg)
            else:
                opencc_status = get_opencc_status()
                status_msg = _get_text("status_idle") + f" ({opencc_status})"
                _set_status_banner("idle", status_msg)

        def _update_input_states() -> None:
            """Dynamically enable/disable input fields based on operation mode"""
            is_replace = refs["op_mode"].value == "replace"
            refs["replace_fields_row"].visible = is_replace
            refs["replace_from"].disabled = not is_replace
            refs["replace_to"].disabled = not is_replace

            is_ext = refs["filter_type"].value == "ext"
            refs["filter_ext"].disabled = not is_ext

        def _set_status_banner(status_type: str, message: str) -> None:
            """Set status banner"""
            status_config = {
                "idle": {"color": "grey700", "icon": ft.Icons.INFO_OUTLINE},
                "ready": {"color": "green700", "icon": ft.Icons.CHECK_CIRCLE_OUTLINE},
                "warning": {"color": "orange700", "icon": ft.Icons.WARNING_AMBER_ROUNDED},
                "error": {"color": "red700", "icon": ft.Icons.ERROR_OUTLINE}
            }

            config = status_config.get(status_type, status_config["idle"])
            refs["status_banner"].content = ft.Row([
                ft.Icon(config["icon"], color="white"),
                ft.Text(message, color="white", weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER)
            refs["status_banner"].bgcolor = config["color"]
            refs["status_banner"].update()

        def _reset_execute_button() -> None:
            """Reset execute button to initial state"""
            app_state["confirming"] = False
            refs["btn_execute"].text = _get_text("exec_btn_execute")
            refs["btn_execute"].bgcolor = COLORS["accent"]
            refs["btn_execute"].color = "black"
            refs["btn_execute"].icon = ft.Icons.ROCKET_LAUNCH
            refs["btn_execute"].disabled = False
            refs["btn_execute"].update()

        def _show_step3_loading() -> None:
            """Show loading indicator for Step 3"""
            if "step3_loading_indicator" in refs:
                indicator = refs["step3_loading_indicator"]
                indicator.controls[0].visible = True
                indicator.controls[1].value = _get_text("step3_loading")
                indicator.update()

        def _hide_step3_loading() -> None:
            """Hide loading indicator for Step 3"""
            if "step3_loading_indicator" in refs:
                indicator = refs["step3_loading_indicator"]
                indicator.controls[0].visible = False
                indicator.controls[1].value = ""
                indicator.update()

        def _get_targets() -> List[Tuple[Path, str]]:
            """Get target files list based on current settings"""
            raw_path = refs["selected_path"].value
            if not raw_path:
                return []

            p = Path(raw_path.strip())
            if not p.exists():
                return []

            valid_exts = []
            if refs["filter_ext"].value:
                valid_exts = [e.strip().lower() for e in refs["filter_ext"].value.split(',')]

            return renamer.scan_directory(
                root_path=p,
                rename_mode=refs["rename_mode"].value,
                filter_type=refs["filter_type"].value,
                valid_exts=valid_exts,
                operation=refs["op_mode"].value,
                find_text=refs["replace_from"].value,
                replace_text=refs["replace_to"].value,
                prefix=refs["prefix_input"].value or "",
                suffix=refs["suffix_input"].value or "",
                symbols=refs["remove_sym_input"].value
            )

        def update_ui(e=None) -> None:
            """Main UI update function"""
            _reset_execute_button()
            app_state["is_loading"] = True
            _show_step3_loading()

            targets = _get_targets()
            app_state["targets"] = targets

            _update_live_preview(targets)
            _update_status_banner(targets)
            _update_input_states()

            app_state["is_loading"] = False
            _hide_step3_loading()

            page.update()

        # =====================================================================
        # EVENT HANDLERS
        # =====================================================================

        def on_reset_click(e=None) -> None:
            """Reset button handler"""
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

            _reset_execute_button()
            _set_status_banner("idle", _get_text("status_reset"))

            page.update()

        def on_execute_click(e=None) -> None:
            """Execute button handler"""
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
                    _reset_execute_button()
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
            """Show full preview handler"""
            targets = _get_targets()
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
            """Language change handler"""
            lang = "zh" if current_language[0] == "en" else "en"
            current_language[0] = lang
            page.clean()
            _build_ui()
            page.update()

        # =====================================================================
        # UI BUILDING
        # =====================================================================

        def _build_ui():
            """Build all UI components"""

            # --- STEP 1: SOURCE FOLDER ---
            selected_path_field = ft.TextField(
                label=_get_text("step1_input_label"),
                expand=True, dense=True,
                border_color=COLORS["accent"], bgcolor="black"
            )
            selected_path_field.on_submit = update_ui
            refs["selected_path"] = selected_path_field

            load_folder_btn = ft.Button(
                _get_text("step1_btn_load"),
                icon=ft.Icons.REFRESH,
                bgcolor=COLORS["accent"], color="black",
                height=40, expand=True
            )
            load_folder_btn.on_click = update_ui
            refs["load_folder_btn"] = load_folder_btn

            rename_mode_group = ft.RadioGroup(
                value="files",
                content=ft.Row([
                    ft.Radio(value="files", label=_get_text("step1_radio_files"), fill_color=COLORS["accent"]),
                    ft.Radio(value="both", label=_get_text("step1_radio_both"), fill_color=COLORS["accent"])
                ])
            )
            rename_mode_group.on_change = update_ui
            refs["rename_mode"] = rename_mode_group

            step1 = ft.Container(
                content=ft.Column([
                    ft.Text(_get_text("step1_title"), size=18, weight=ft.FontWeight.BOLD),
                    selected_path_field,
                    ft.Row([load_folder_btn]),
                    rename_mode_group
                ], spacing=15),
                padding=15, bgcolor=COLORS["card"], border_radius=10
            )

            # --- STEP 2: FILTER ---
            filter_type_group = ft.RadioGroup(
                value="all",
                content=ft.Row([
                    ft.Radio(value="all", label=_get_text("step2_radio_all"), fill_color=COLORS["accent"]),
                    ft.Radio(value="ext", label=_get_text("step2_radio_ext"), fill_color=COLORS["accent"])
                ])
            )
            filter_type_group.on_change = update_ui
            refs["filter_type"] = filter_type_group

            filter_ext_field = ft.TextField(
                hint_text=_get_text("step2_filter_hint"),
                disabled=True,
                dense=True
            )
            filter_ext_field.on_change = update_ui
            refs["filter_ext"] = filter_ext_field

            step2 = ft.Container(
                content=ft.Column([
                    ft.Text(_get_text("step2_title"), size=18, weight=ft.FontWeight.BOLD),
                    filter_type_group,
                    filter_ext_field
                ], spacing=10),
                padding=12, bgcolor=COLORS["card"], border_radius=10
            )

            # --- STEP 3: OPERATION ---
            op_mode_dropdown = ft.Dropdown(
                value="s2t",
                options=[
                    ft.dropdown.Option("none", _get_text("step3_option_none")),
                    ft.dropdown.Option("replace", _get_text("step3_option_replace")),
                    ft.dropdown.Option("s2t", _get_text("step3_option_s2t"))
                ],
                border_color=COLORS["accent"],
                dense=True,
                expand=True
            )
            op_mode_dropdown.on_change = update_ui
            refs["op_mode"] = op_mode_dropdown

            loading_indicator = ft.Row([
                ft.ProgressRing(visible=False, width=20, height=20),
                ft.Text("", size=12, color=COLORS["text_dim"])
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
            refs["step3_loading_indicator"] = loading_indicator

            refresh_btn = ft.IconButton(
                ft.Icons.REFRESH,
                icon_size=20,
                tooltip=_get_text("step3_refresh_hint")
            )
            refresh_btn.on_click = update_ui
            refs["step3_refresh_btn"] = refresh_btn

            replace_from_field = ft.TextField(
                label=_get_text("step3_find_label"),
                expand=True, disabled=True,
                dense=True
            )
            replace_from_field.on_change = update_ui
            refs["replace_from"] = replace_from_field

            replace_to_field = ft.TextField(
                label=_get_text("step3_replace_label"),
                expand=True, disabled=True,
                dense=True
            )
            replace_to_field.on_change = update_ui
            refs["replace_to"] = replace_to_field

            replace_fields_row = ft.Row([replace_from_field, replace_to_field], visible=False)
            refs["replace_fields_row"] = replace_fields_row

            step3 = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(_get_text("step3_title"), size=18, weight=ft.FontWeight.BOLD, expand=True),
                        refresh_btn
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Text(_get_text("step3_refresh_hint"), size=11, color="orange", italic=True),
                    ft.Row([op_mode_dropdown, loading_indicator], expand=True),
                    replace_fields_row
                ], spacing=10),
                padding=15, bgcolor=COLORS["card"], border_radius=10
            )

            # --- STEP 4: FORMATTING ---
            remove_sym_field = ft.TextField(
                label=_get_text("step4_remove_symbols"),
                value="",
                hint_text=_get_text("step4_remove_hint"),
                dense=True
            )
            remove_sym_field.on_change = update_ui
            refs["remove_sym_input"] = remove_sym_field

            prefix_field = ft.TextField(
                label=_get_text("step4_prefix"),
                expand=True, dense=True
            )
            prefix_field.on_change = update_ui
            refs["prefix_input"] = prefix_field

            suffix_field = ft.TextField(
                label=_get_text("step4_suffix"),
                expand=True, dense=True
            )
            suffix_field.on_change = update_ui
            refs["suffix_input"] = suffix_field

            live_preview_col = ft.Column()
            refs["live_preview_container"] = live_preview_col

            step4 = ft.Container(
                content=ft.Column([
                    ft.Text(_get_text("step4_title"), size=18, weight=ft.FontWeight.BOLD),
                    remove_sym_field,
                    ft.Row([prefix_field, suffix_field]),
                    ft.Divider(),
                    ft.Text(_get_text("step4_preview"), color=COLORS["text_dim"]),
                    live_preview_col
                ], spacing=8),
                padding=16, bgcolor=COLORS["card"], border_radius=12
            )

            # --- RIGHT COLUMN: EXECUTION & LOG ---
            status_display = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, color="white"),
                    ft.Text(_get_text("exec_status_waiting"), color="white", weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor="grey700", padding=12, border_radius=8
            )
            refs["status_banner"] = status_display

            preview_btn = ft.Button(
                _get_text("exec_btn_preview"),
                icon=ft.Icons.VISIBILITY,
                style=ft.ButtonStyle(color=COLORS["accent"], bgcolor=COLORS["card"])
            )
            preview_btn.on_click = on_show_full_preview
            refs["preview_btn"] = preview_btn

            execute_btn = ft.Button(
                _get_text("exec_btn_execute"),
                icon=ft.Icons.ROCKET_LAUNCH,
                style=ft.ButtonStyle(color="black", bgcolor=COLORS["accent"])
            )
            execute_btn.on_click = on_execute_click
            refs["btn_execute"] = execute_btn

            action_buttons = ft.Row([
                ft.Container(content=preview_btn, height=50, expand=True),
                ft.Container(content=execute_btn, height=50, expand=True)
            ], spacing=8)

            preview_log = ft.Column(spacing=4, scroll="auto")
            refs["preview_log"] = preview_log

            log_area = ft.Container(
                content=preview_log,
                border_radius=4,
                padding=8,
                expand=True
            )

            right_column = ft.Column([
                ft.Text(_get_text("exec_title"), size=18, weight=ft.FontWeight.BOLD),
                status_display,
                action_buttons,
                log_area
            ], spacing=12, expand=True)

            step_actions = ft.Container(
                content=right_column,
                padding=12, bgcolor=COLORS["card"], border_radius=10,
                expand=True
            )

            # --- MAIN LAYOUT ---
            language_btn = ft.Button(
                "EN" if current_language[0] == "en" else "中文",
                icon=ft.Icons.LANGUAGE,
                height=36
            )
            language_btn.on_click = on_language_change
            refs["language_btn"] = language_btn

            reset_btn = ft.IconButton(
                ft.Icons.REFRESH,
                icon_size=24,
                tooltip=_get_text("btn_reset")
            )
            reset_btn.on_click = on_reset_click
            refs["reset_btn"] = reset_btn

            header_row = ft.Row([
                ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE, color=COLORS["accent"], size=32),
                        ft.Column([
                            ft.Text(_get_text("app_title"), size=24, weight=ft.FontWeight.BOLD),
                            ft.Text(_get_text("app_subtitle"), size=10, color=COLORS["text_dim"])
                        ], spacing=2)
                    ], spacing=12, alignment=ft.MainAxisAlignment.START)
                ], expand=True),
                ft.Row([language_btn, reset_btn], spacing=8)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

            main_content = ft.Column([
                header_row,
                ft.Container(height=12),
                ft.Row([
                    ft.Column(
                        [step1, step2, step3, step4],
                        expand=6, spacing=12,
                        scroll=ft.ScrollMode.AUTO
                    ),
                    ft.Column([step_actions], expand=6)
                ], vertical_alignment=ft.CrossAxisAlignment.STRETCH, spacing=16, expand=True)
            ], expand=True)

            content = ft.Container(
                expand=True,
                bgcolor=COLORS["bg"],
                padding=28,
                content=main_content
            )

            page.add(content)
            _update_input_states()

        _build_ui()
        page.update()

    flet_app(target=main)
