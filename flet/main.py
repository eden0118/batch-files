import flet as ft
import os
from pathlib import Path

# --- 1. 內建微型字典 (Fallback) ---
MINI_DICT = str.maketrans({
    '国': '國', '爱': '愛', '华': '華', '宝': '寶', '电': '電', '开': '開', '关': '關',
    '医': '醫', '车': '車', '书': '書', '听': '聽', '发': '發', '门': '門', '专': '專',
    '难': '難', '业': '業', '东': '東', '画': '畫', '写': '寫', '马': '馬', '鸟': '鳥',
    '儿': '兒', '语': '語', '头': '頭', '见': '見', '气': '氣', '长': '長', '实': '實',
    '后': '後', '机': '機', '权': '權', '变': '變', '现': '現', '务': '務', '际': '際'
})

# --- OpenCC ---
HAS_OPENCC = False
cc = None
OPENCC_MSG = "Init..."
try:
    from opencc import OpenCC
    for config in ['s2t', 's2t.json', 't2s', 't2s.json']:
        try:
            temp_cc = OpenCC(config)
            if temp_cc.convert('国') == '國':
                cc = temp_cc
                HAS_OPENCC = True
                OPENCC_MSG = f"Active ({config})"
                break
        except: continue
    if not HAS_OPENCC: OPENCC_MSG = "Missing (Mini-Dict Active)"
except ImportError: OPENCC_MSG = "Module Missing"


def main(page: ft.Page):
    # --- APP CONFIGURATION ---
    page.title = "Pro Renamer v4.4 (Browse Fixed)"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 850

    # Colors
    C_BG = "#111827"
    C_SIDEBAR = "#0f172a"
    C_ACCENT = "#2dd4bf"
    C_CARD = "#1e293b"
    C_TEXT_DIM = "#94a3b8"
    C_RED = "#ef4444"

    # --- STATE REFS ---
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

    # Global State
    state = {"confirming": False, "targets": []}

    # --- LOGIC ---

    def get_targets():
        raw = selected_path.current.value
        if not raw: return []
        p = Path(raw.strip())
        if not p.exists(): return []

        targets = []
        mode = rename_mode.current.value
        f_type = filter_type.current.value
        valid_exts = [e.strip().lower() for e in filter_ext.current.value.split(',')] if filter_ext.current.value else []

        try:
            for item in p.iterdir():
                if item.name.startswith('.'): continue
                if item.is_dir() and mode == "files": continue
                if item.is_file() and f_type == "ext" and valid_exts:
                    if item.suffix.lower() not in valid_exts: continue

                new_name = item.name

                # 1. Operation
                op = op_mode.current.value
                if op == "s2t":
                    if HAS_OPENCC and cc: new_name = cc.convert(new_name)
                    if new_name == item.name: new_name = item.name.translate(MINI_DICT)
                elif op == "replace":
                    f = replace_from.current.value
                    t = replace_to.current.value
                    if f: new_name = new_name.replace(f, t)

                # 2. Formatting
                syms = remove_sym_input.current.value
                if syms:
                    for char in syms: new_name = new_name.replace(char, "")

                pre = prefix_input.current.value or ""
                suf = suffix_input.current.value or ""

                if item.is_file():
                    stem = Path(new_name).stem
                    suffix = Path(new_name).suffix
                    new_name = f"{pre}{stem}{suf}{suffix}"
                else:
                    new_name = f"{pre}{new_name}{suf}"

                targets.append((item, new_name))
        except Exception as e:
            print(f"Scan Error: {e}")

        return targets

    def update_ui(e=None):
        reset_execute_button()
        targets = get_targets()
        state["targets"] = targets

        # Live Preview (Top 3)
        controls = []
        for item, new_name in targets[:3]:
            color = C_ACCENT if item.name != new_name else "grey"
            controls.append(ft.Text(f"{item.name}  →  {new_name}", color=color, font_family="monospace"))

        if not targets:
            controls.append(ft.Text("No files match current filters.", color="orange"))

        live_preview_container.current.controls = controls
        live_preview_container.current.update()

        # Banner
        changed_count = sum(1 for t in targets if t[0].name != t[1])
        if changed_count > 0:
            update_status_banner("ready", f"Ready: {changed_count} files will change.")
        else:
            update_status_banner("idle", f"No changes detected. ({OPENCC_MSG})")

        # Inputs
        is_replace = op_mode.current.value == "replace"
        replace_from.current.disabled = not is_replace
        replace_to.current.disabled = not is_replace
        is_ext = filter_type.current.value == "ext"
        filter_ext.current.disabled = not is_ext
        page.update()

    def update_status_banner(status_type, message):
        colors = {"idle": "grey700", "ready": "green700", "warning": "orange700", "error": "red700"}
        icons = {"idle": ft.Icons.INFO_OUTLINE, "ready": ft.Icons.CHECK_CIRCLE_OUTLINE, "warning": ft.Icons.WARNING_AMBER_ROUNDED, "error": ft.Icons.ERROR_OUTLINE}
        status_banner.current.content = ft.Row([
            ft.Icon(icons.get(status_type, ft.Icons.INFO), color="white"),
            ft.Text(message, color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER)
        status_banner.current.bgcolor = colors.get(status_type, "grey700")
        status_banner.current.update()

    def reset_execute_button():
        state["confirming"] = False
        btn_execute.current.text = "Execute Rename"
        btn_execute.current.bgcolor = C_ACCENT
        btn_execute.current.color = "black"
        btn_execute.current.icon = ft.Icons.ROCKET_LAUNCH
        btn_execute.current.update()

    def on_execute_click(e):
        targets = state["targets"]
        changed = [t for t in targets if t[0].name != t[1]]

        if not changed:
            page.snack_bar = ft.SnackBar(content=ft.Text("No changes to apply!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return

        if not state["confirming"]:
            state["confirming"] = True
            btn_execute.current.text = f"CONFIRM ({len(changed)})?"
            btn_execute.current.bgcolor = C_RED
            btn_execute.current.color = "white"
            btn_execute.current.icon = ft.Icons.WARNING
            btn_execute.current.update()
        else:
            success = 0
            log_lines = [ft.Text("--- Execution Started ---", color=C_ACCENT)]
            for old, new in targets:
                if old.name == new: continue
                try:
                    os.rename(old, old.parent / new)
                    success += 1
                    log_lines.append(ft.Text(f"[OK] {old.name} -> {new}", color="green", font_family="monospace"))
                except Exception as ex:
                    log_lines.append(ft.Text(f"[ERR] {old.name}: {ex}", color="red", font_family="monospace"))

            reset_execute_button()
            update_ui()
            log_lines.append(ft.Text(f"--- Completed: {success} files renamed ---", weight="bold"))
            preview_log.current.controls = log_lines
            preview_log.current.update()
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Success! {success} files renamed."), bgcolor="green")
            page.snack_bar.open = True
            page.update()

    def generate_full_preview(e):
        targets = get_targets()
        log_lines = [ft.Text("--- Preview Mode ---", color="yellow")]
        for item, new_name in targets:
            if item.name != new_name:
                log_lines.append(ft.Row([
                    ft.Text(item.name, color="grey"),
                    ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=C_ACCENT),
                    ft.Text(new_name, color="white", weight="bold")
                ]))
        preview_log.current.controls = log_lines
        preview_log.current.update()

    # --- FILE PICKER LOGIC (RE-ENABLED) ---
    def on_folder_picker_result(e: ft.FilePickerResultEvent):
        # 這是關鍵：如果使用者真的選了資料夾，e.path 會有值
        if e.path:
            selected_path.current.value = e.path
            selected_path.current.update()
            update_ui()
        else:
            print("Picker cancelled or no path selected.")

    # [FIX] 1. 定義 Picker
    file_picker = ft.FilePicker(on_result=on_folder_picker_result)
    # [FIX] 2. 加入 Overlay (這步最重要)
    page.overlay.append(file_picker)
    page.update()

    # --- UI COMPONENTS ---

    # Step 1
    step1 = ft.Container(
        content=ft.Column([
            ft.Text("Step 1: Source Folder", size=18, weight=ft.FontWeight.BOLD),
            ft.TextField(
                ref=selected_path,
                label="Paste Path Here",
                expand=True, dense=True, border_color=C_ACCENT, bgcolor="black",
                on_submit=update_ui
            ),
            ft.Row([
                ft.ElevatedButton("Load Folder", icon=ft.Icons.REFRESH, bgcolor=C_ACCENT, color="black", on_click=update_ui, height=40, expand=True),
                # [FIX] 3. 綁定按鈕事件
                ft.OutlinedButton(
                    "Browse...",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=lambda _: file_picker.get_directory_path(), # 呼叫原生資料夾選擇器
                    height=40
                )
            ]),
            ft.RadioGroup(ref=rename_mode, value="files", content=ft.Row([ft.Radio(value="files", label="Files Only", fill_color=C_ACCENT), ft.Radio(value="both", label="Files & Folders", fill_color=C_ACCENT)]), on_change=update_ui)
        ]), padding=15, bgcolor=C_CARD, border_radius=10
    )

    # Step 2
    step2 = ft.Container(content=ft.Column([
        ft.Text("Step 2: Filter", size=18, weight=ft.FontWeight.BOLD),
        ft.RadioGroup(ref=filter_type, value="all", content=ft.Row([ft.Radio(value="all", label="All Files", fill_color=C_ACCENT), ft.Radio(value="ext", label="Specific Ext", fill_color=C_ACCENT)]), on_change=update_ui),
        ft.TextField(ref=filter_ext, hint_text="jpg, png", disabled=True, dense=True, on_change=update_ui)
    ]), padding=15, bgcolor=C_CARD, border_radius=10)

    # Step 3
    op_opts = [
        ft.dropdown.Option("none", "No Operation"),
        ft.dropdown.Option("replace", "Replace Text"),
        ft.dropdown.Option("s2t", "Simplified -> Traditional")
    ]
    step3 = ft.Container(content=ft.Column([
        ft.Text("Step 3: Operation", size=18, weight=ft.FontWeight.BOLD),
        ft.Dropdown(
            ref=op_mode,
            value="s2t",
            options=op_opts,
            border_color=C_ACCENT,
            dense=True,
            expand=True,
            on_change=update_ui
        ),
        ft.Row([ft.TextField(ref=replace_from, label="Find", expand=True, disabled=True, dense=True, on_change=update_ui), ft.TextField(ref=replace_to, label="Replace", expand=True, disabled=True, dense=True, on_change=update_ui)])
    ]), padding=15, bgcolor=C_CARD, border_radius=10)

    # Step 4
    step4 = ft.Container(content=ft.Column([
        ft.Text("Step 4: Formatting", size=18, weight=ft.FontWeight.BOLD),
        ft.TextField(
            ref=remove_sym_input,
            label="Remove Symbols",
            value="",
            hint_text="!@#",
            dense=True, on_change=update_ui
        ),
        ft.Row([ft.TextField(ref=prefix_input, label="Prefix", expand=True, dense=True, on_change=update_ui), ft.TextField(ref=suffix_input, label="Suffix", expand=True, dense=True, on_change=update_ui)]),
        ft.Divider(), ft.Text("Live Preview:", color=C_TEXT_DIM), ft.Column(ref=live_preview_container)
    ]), padding=15, bgcolor=C_CARD, border_radius=10)

    # Actions Area
    status_display = ft.Container(ref=status_banner, content=ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE, color="white"), ft.Text("Waiting...", color="white", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER), bgcolor="grey700", padding=10, border_radius=8)

    right_column_content = ft.Column([
        ft.Text("Execution & Log", size=18, weight=ft.FontWeight.BOLD),
        status_display,
        ft.Row([
            ft.Container(content=ft.ElevatedButton("Show Full Preview", icon=ft.Icons.VISIBILITY, on_click=generate_full_preview, style=ft.ButtonStyle(color=C_ACCENT, bgcolor=C_CARD)), height=50, expand=True),
            ft.Container(content=ft.ElevatedButton(
                ref=btn_execute,
                text="Execute Rename",
                icon=ft.Icons.ROCKET_LAUNCH,
                on_click=on_execute_click,
                style=ft.ButtonStyle(color="black", bgcolor=C_ACCENT)
            ), height=50, expand=True)
        ]),
        ft.Container(
            content=ft.Column(ref=preview_log, scroll=ft.ScrollMode.AUTO),
            bgcolor="black",
            border=ft.border.all(1, "grey"),
            border_radius=5,
            padding=10,
            expand=True
        )
    ], spacing=15, expand=True)

    step_actions = ft.Container(
        content=right_column_content,
        padding=15, bgcolor=C_CARD, border_radius=10,
        expand=True
    )

    # Main Layout
    sidebar = ft.Container(width=250, bgcolor=C_SIDEBAR, padding=20, content=ft.Column([ft.Row([ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE, color=C_ACCENT, size=30), ft.Text("Renamer", size=20, weight=ft.FontWeight.BOLD)]), ft.Divider(), ft.Text("v4.4 Browse Fix", color=C_TEXT_DIM)]))

    main_content = ft.Column(
        [
            ft.Text("Batch Renamer Config", size=28, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Row(
                [
                    ft.Column(
                        [step1, step2, step3, step4],
                        expand=6,
                        spacing=20,
                        scroll=ft.ScrollMode.HIDDEN
                    ),
                    ft.Column(
                        [step_actions],
                        expand=6,
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=20,
                expand=True
            )
        ],
        expand=True
    )

    content = ft.Container(
        expand=True,
        bgcolor=C_BG,
        padding=30,
        content=main_content
    )

    page.add(ft.Row([sidebar, content], expand=True, spacing=0))

if __name__ == "__main__":
    ft.app(target=main)