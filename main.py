import flet as ft
import os
import shutil
from pathlib import Path
from collections import Counter

# --- 嘗試導入 OpenCC (簡繁轉換) ---
try:
    from opencc import OpenCC
    HAS_OPENCC = True
    cc = OpenCC('s2t')
except ImportError:
    HAS_OPENCC = False
    cc = None

def main(page: ft.Page):
    # --- 1. APP CONFIGURATION ---
    page.title = "Pro Renamer v2.5 (Stable)"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 850

    # Custom Colors (使用 Hex 字串最安全)
    COLOR_BG = "#111827"
    COLOR_SIDEBAR = "#0f172a"
    COLOR_ACCENT = "#2dd4bf"
    COLOR_CARD = "#1e293b"
    COLOR_TEXT_DIM = "#94a3b8"

    # --- 2. STATE VARIABLES ---
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

    # --- 3. LOGIC FUNCTIONS ---

    def update_status_banner(status_type, message):
        # 定義狀態樣式 (使用字串顏色與 ft.Icons)
        colors = {
            "idle": "grey700",
            "ready": "green700",
            "warning": "orange700",
            "error": "red700",
        }
        icons = {
            "idle": ft.Icons.INFO_OUTLINE,
            "ready": ft.Icons.CHECK_CIRCLE_OUTLINE,
            "warning": ft.Icons.WARNING_AMBER_ROUNDED,
            "error": ft.Icons.ERROR_OUTLINE,
        }

        banner_content = ft.Row([
            ft.Icon(icons.get(status_type, ft.Icons.INFO), color="white"),
            ft.Text(message, color="white", weight=ft.FontWeight.BOLD, size=14)
        ], alignment=ft.MainAxisAlignment.CENTER)

        status_banner.current.content = banner_content
        status_banner.current.bgcolor = colors.get(status_type, "grey700")
        status_banner.current.update()

    def get_target_files():
        if not selected_path.current.value:
            return []
        path = Path(selected_path.current.value)
        if not path.exists():
            return []

        targets = []
        mode = rename_mode.current.value
        f_type = filter_type.current.value
        valid_exts = [e.strip().lower() for e in filter_ext.current.value.split(',')] if filter_ext.current.value else []

        try:
            items = list(path.iterdir())
        except Exception:
            return []

        for item in items:
            if item.is_dir() and mode == "files":
                continue
            if item.is_file() and f_type == "ext" and valid_exts:
                if item.suffix.lower() not in valid_exts:
                    continue
            new_name = transform_name(item.name, item.is_file())
            targets.append((item, new_name))
        return targets

    def transform_name(original_name, is_file):
        stem = Path(original_name).stem if is_file else original_name
        suffix = Path(original_name).suffix if is_file else ""

        operation = op_mode.current.value
        if operation == "s2t" and HAS_OPENCC:
            stem = cc.convert(stem)
        elif operation == "replace":
            r_from = replace_from.current.value
            r_to = replace_to.current.value
            if r_from:
                stem = stem.replace(r_from, r_to)

        symbols = remove_sym_input.current.value
        if symbols:
            for char in symbols:
                stem = stem.replace(char, "")

        pre = prefix_input.current.value or ""
        suf = suffix_input.current.value or ""
        return f"{pre}{stem}{suf}{suffix}"

    def update_live_sample(e=None):
        targets = get_target_files()

        controls = []
        for item, new_name in targets[:3]:
            controls.append(
                ft.Text(f"{item.name}  →  {new_name}", color=COLOR_ACCENT, font_family="monospace")
            )
        if not targets:
             controls.append(ft.Text("No files match filters.", color="grey"))
        live_preview_container.current.controls = controls
        live_preview_container.current.update()

        if not targets:
            update_status_banner("idle", "Status: No files selected or matching filters.")
            return

        new_names = [t[1] for t in targets]
        name_counts = Counter(new_names)
        conflicts = [name for name, count in name_counts.items() if count > 1]
        empty_names = any(not name.strip() for name in new_names)

        if conflicts:
             update_status_banner("warning", f"Warning: {len(conflicts)} naming conflicts detected!")
        elif empty_names:
             update_status_banner("warning", "Warning: Resulting filename is empty!")
        else:
             update_status_banner("ready", f"Status: Ready to process {len(targets)} items.")

    def generate_preview_log(e=None):
        targets = get_target_files()
        log_lines = []
        log_lines.append(ft.Text("========================================", font_family="monospace"))
        log_lines.append(ft.Text(f"Found {len(targets)} items", color=COLOR_ACCENT, weight=ft.FontWeight.BOLD))
        log_lines.append(ft.Container(height=10))

        for item, new_name in targets:
            color = "white"
            if item.name == new_name:
                color = "grey"

            log_lines.append(
                ft.Row([
                    ft.Text(item.name, color="grey", font_family="monospace"),
                    ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=COLOR_ACCENT),
                    ft.Text(new_name, color=color, weight=ft.FontWeight.BOLD, font_family="monospace")
                ], spacing=10)
            )

        log_lines.append(ft.Container(height=10))
        log_lines.append(ft.Text("(Preview Mode - Not Yet Executed)", color="yellow", italic=True))
        preview_log.current.controls = log_lines
        preview_log.current.update()

    def confirm_execution(e):
        targets = get_target_files()
        if not targets:
            page.snack_bar = ft.SnackBar(ft.Text("No files to rename!"))
            page.snack_bar.open = True
            page.update()
            return

        def proceed_rename(e):
            page.dialog.open = False
            execute_renaming(targets)
            page.update()

        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Rename"),
            content=ft.Text(f"Rename {len(targets)} items?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(page.dialog, 'open', False) or page.update()),
                ft.ElevatedButton("Yes, Proceed", bgcolor=COLOR_ACCENT, color="black", on_click=proceed_rename),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    def execute_renaming(targets):
        success = 0
        fail = 0
        preview_log.current.controls = [ft.Text("Executing...", color=COLOR_ACCENT)]

        update_status_banner("idle", "Status: Renaming in progress...")

        for item, new_name in targets:
            if item.name == new_name: continue
            try:
                new_path = item.parent / new_name
                if new_path.exists() and new_path != item:
                     raise FileExistsError("Target file already exists.")
                os.rename(item, new_path)
                preview_log.current.controls.append(ft.Text(f"[OK] {item.name}", color="green", font_family="monospace"))
                success += 1
            except Exception as ex:
                preview_log.current.controls.append(ft.Text(f"[ERR] {item.name}: {ex}", color="red", font_family="monospace"))
                fail += 1

        preview_log.current.controls.append(ft.Divider())
        preview_log.current.controls.append(ft.Text(f"Finished. Success: {success}, Failed: {fail}", weight=ft.FontWeight.BOLD))
        preview_log.current.update()
        update_live_sample()

    # --- 4. UI EVENT HANDLERS & FILE PICKER ---

    def on_folder_result(e: ft.FilePickerResultEvent):
        if e.path:
            selected_path.current.value = e.path
            selected_path.current.update()
            update_live_sample()

    file_picker = ft.FilePicker(on_result=on_folder_result)
    page.overlay.append(file_picker)
    page.update()

    def on_option_change(e):
        is_replace = op_mode.current.value == "replace"
        replace_from.current.disabled = not is_replace
        replace_to.current.disabled = not is_replace

        is_ext = filter_type.current.value == "ext"
        filter_ext.current.disabled = not is_ext

        page.update()
        update_live_sample()

    # --- 5. UI COMPONENTS ---

    # Step 1
    step1 = ft.Container(
        content=ft.Column([
            ft.Text("Step 1: Source", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.TextField(
                    ref=selected_path,
                    label="Folder Path",
                    read_only=True,
                    expand=True,
                    dense=True,
                    border_color=COLOR_ACCENT
                ),
                ft.IconButton(
                    icon=ft.Icons.FOLDER_OPEN,
                    icon_color=COLOR_ACCENT,
                    tooltip="Select Folder",
                    on_click=lambda _: file_picker.get_directory_path()
                )
            ]),
            ft.RadioGroup(
                ref=rename_mode,
                value="files",
                content=ft.Row([
                    ft.Radio(value="files", label="Files Only", fill_color=COLOR_ACCENT),
                    ft.Radio(value="both", label="Files & Folders", fill_color=COLOR_ACCENT),
                ]),
                on_change=on_option_change
            )
        ]),
        padding=15, bgcolor=COLOR_CARD, border_radius=10
    )

    # Step 2
    step2 = ft.Container(
        content=ft.Column([
            ft.Text("Step 2: Filter", size=18, weight=ft.FontWeight.BOLD),
            ft.RadioGroup(
                ref=filter_type,
                value="all",
                content=ft.Row([
                    ft.Radio(value="all", label="All Files", fill_color=COLOR_ACCENT),
                    ft.Radio(value="ext", label="Specific Ext", fill_color=COLOR_ACCENT),
                ]),
                on_change=on_option_change
            ),
            ft.TextField(ref=filter_ext, hint_text="jpg, png", disabled=True, dense=True, on_change=on_option_change)
        ]),
        padding=15, bgcolor=COLOR_CARD, border_radius=10
    )

    # Step 3
    op_opts = [
        ft.dropdown.Option("none", "No Operation"),
        ft.dropdown.Option("replace", "Replace Text"),
    ]
    if HAS_OPENCC:
        op_opts.insert(1, ft.dropdown.Option("s2t", "Simplified -> Traditional"))

    step3 = ft.Container(
        content=ft.Column([
            ft.Text("Step 3: Operation", size=18, weight=ft.FontWeight.BOLD),
            ft.Dropdown(
                ref=op_mode,
                value="none",
                options=op_opts,
                border_color=COLOR_ACCENT,
                dense=True,
                on_change=on_option_change
            ),
            ft.Row([
                ft.TextField(ref=replace_from, label="Find", expand=True, disabled=True, dense=True, on_change=on_option_change),
                ft.TextField(ref=replace_to, label="Replace", expand=True, disabled=True, dense=True, on_change=on_option_change),
            ])
        ]),
        padding=15, bgcolor=COLOR_CARD, border_radius=10
    )

    # Step 4
    step4 = ft.Container(
        content=ft.Column([
            ft.Text("Step 4: Formatting", size=18, weight=ft.FontWeight.BOLD),
            ft.TextField(ref=remove_sym_input, label="Remove Symbols", value="!@#", dense=True, on_change=on_option_change),
            ft.Row([
                ft.TextField(ref=prefix_input, label="Prefix", expand=True, dense=True, on_change=on_option_change),
                ft.TextField(ref=suffix_input, label="Suffix", expand=True, dense=True, on_change=on_option_change),
            ]),
            ft.Divider(),
            ft.Text("Live Preview (Top 3):", color=COLOR_TEXT_DIM),
            ft.Column(ref=live_preview_container)
        ]),
        padding=15, bgcolor=COLOR_CARD, border_radius=10
    )

    # Actions Area

    status_display = ft.Container(
        ref=status_banner,
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_OUTLINE, color="white"),
            ft.Text("Status: Waiting for input...", color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor="grey700", # 安全起見使用字串
        padding=10,
        border_radius=8,
        alignment=ft.alignment.center,
        # [FIX] 這裡修正了：使用 ft.Animation
        animate=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT)
    )

    btn_preview = ft.Container(
        content=ft.ElevatedButton(
            "Preview Logs",
            icon=ft.Icons.VISIBILITY,
            on_click=generate_preview_log,
            style=ft.ButtonStyle(color=COLOR_ACCENT, bgcolor=COLOR_CARD)
        ),
        height=50, expand=True
    )

    btn_run = ft.Container(
        content=ft.ElevatedButton(
            "Execute Rename",
            icon=ft.Icons.ROCKET_LAUNCH,
            on_click=confirm_execution,
            style=ft.ButtonStyle(color="black", bgcolor=COLOR_ACCENT)
        ),
        height=50, expand=True
    )

    step_actions = ft.Container(
        content=ft.Column([
            ft.Text("Execution & Status", size=18, weight=ft.FontWeight.BOLD),
            status_display,
            ft.Row([btn_preview, btn_run]),
            ft.Container(
                content=ft.Column(ref=preview_log, scroll=ft.ScrollMode.AUTO),
                bgcolor="black",
                border=ft.border.all(1, "grey"),
                border_radius=5,
                padding=10,
                height=250,
            )
        ], spacing=15),
        padding=15, bgcolor=COLOR_CARD, border_radius=10
    )

    # --- 6. LAYOUT ---

    sidebar = ft.Container(
        width=250,
        bgcolor=COLOR_SIDEBAR,
        padding=20,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE, color=COLOR_ACCENT, size=30),
                ft.Text("Renamer", size=20, weight=ft.FontWeight.BOLD)
            ]),
            ft.Divider(),
            ft.Text("v2.5 Stable", color=COLOR_TEXT_DIM)
        ])
    )

    content = ft.Container(
        expand=True,
        bgcolor=COLOR_BG,
        padding=30,
        content=ft.Column([
            ft.Text("Batch Renamer Configuration", size=28, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Row([
                ft.Column([step1, step2, step3, step4], expand=6, spacing=20),
                ft.Column([step_actions], expand=6)
            ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=20)
        ], scroll=ft.ScrollMode.AUTO)
    )

    page.add(ft.Row([sidebar, content], expand=True, spacing=0))

if __name__ == "__main__":
    ft.app(target=main)