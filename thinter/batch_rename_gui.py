#!/usr/bin/env python3
"""
Batch File Renaming Tool
Layout Fix: Matching Screenshot Structure
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

from styles import WINDOW_CONFIG, SPACING, FONTS, COLORS, BUTTON_STYLE, ENTRY_STYLE
from i18n import LANGUAGES

try:
    from opencc import OpenCC
    OPENCC_AVAILABLE = True
except (ImportError, RuntimeError, Exception):
    OPENCC_AVAILABLE = False


class BatchRenameApp:
    """Main batch file renaming application"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.lang = LANGUAGES["en"]
        self.root.title(self.lang["app_title"])
        self.root.geometry(f"{WINDOW_CONFIG['width']}x{WINDOW_CONFIG['height']}")
        self.root.resizable(*WINDOW_CONFIG["resizable"])
        self.root.configure(bg=COLORS["bg"])

        # Initialize converter
        self.s2t_converter: Optional[OpenCC] = None
        if OPENCC_AVAILABLE:
            try:
                self.s2t_converter = OpenCC('s2t')
            except:
                pass

        # State variables
        self.selected_directory: Optional[Path] = None
        self.current_plan: List[tuple] = []
        self.rename_mode: str = "files"

        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup UI with left control panel and right terminal log"""

        # Header Title
        header = tk.Frame(self.root, bg=COLORS["bg"])
        header.pack(fill=tk.X, padx=SPACING["element_padx"], pady=(SPACING["section_pady"], 10))
        title = tk.Label(header, text=self.lang["app_title"], font=FONTS["title"], fg=COLORS["fg"], bg=COLORS["bg"])
        title.pack(expand=True) # Center Title

        # Main container
        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=SPACING["element_padx"], pady=(0, SPACING["section_pady"]))
        main.grid_columnconfigure(0, weight=4) # Left panel 40%
        main.grid_columnconfigure(1, weight=6) # Right panel 60%
        main.grid_rowconfigure(0, weight=1)

        # Left panel - controls
        left = tk.Frame(main, bg=COLORS["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=SPACING["panel_padx_right"])

        # --- Step 01: Choose Folder ---
        step01 = self._step_frame(left, "step_01")

        # Container for Path text + Button
        path_frame = tk.Frame(left, bg=COLORS["bg"])
        path_frame.pack(fill=tk.X, padx=SPACING["widget_padx"], pady=(0, SPACING["element_pady"]))

        # Button Right
        self.select_btn = tk.Button(
            path_frame,
            text=self.lang["select_dir"],
            command=self.select_directory,
            **BUTTON_STYLE
        )
        self.select_btn.pack(side=tk.RIGHT)

        # Label Left
        self.dir_label = tk.Label(path_frame, text=self.lang["selected_dir"], font=FONTS["normal"], fg=COLORS["secondary"], bg=COLORS["bg"])
        self.dir_label.pack(side=tk.LEFT, expand=True, fill=tk.X, anchor=tk.W)

        # --- Rename Mode ---
        mode_frame = tk.Frame(left, bg=COLORS["bg"])
        mode_frame.pack(fill=tk.X, padx=SPACING["widget_padx"], pady=(0, SPACING["element_pady"]))

        tk.Label(mode_frame, text=self.lang["rename_mode"], font=FONTS["small"], fg=COLORS["text_normal"], bg=COLORS["bg"]).pack(side=tk.LEFT, padx=(0, 10))

        self.mode_var = tk.StringVar(value="files")
        rb_style = {"fg": COLORS["text_normal"], "bg": COLORS["bg"], "selectcolor": COLORS["input_bg"], "activebackground": COLORS["bg"], "activeforeground": COLORS["fg"], "font": FONTS["small"]}

        tk.Radiobutton(mode_frame, text=self.lang["mode_files"], variable=self.mode_var, value="files", command=self._on_mode_changed, **rb_style).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text=self.lang["mode_both"], variable=self.mode_var, value="both", command=self._on_mode_changed, **rb_style).pack(side=tk.LEFT, padx=5)

        # --- Step 02: File Filter ---
        step02 = self._step_frame(left, "step_02")
        self.filter_var = tk.StringVar(value="all")
        tk.Radiobutton(left, text=self.lang["all_files"], variable=self.filter_var, value="all", command=self._on_filter_changed, **rb_style).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 4))
        tk.Radiobutton(left, text=self.lang["specific_type"], variable=self.filter_var, value="specific", command=self._on_filter_changed, **rb_style).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 4))

        self.ext_entry_frame, self.ext_entry = self._create_styled_entry(left)
        self.ext_entry.insert(0, self.lang["default_extensions"])
        self._toggle_input_state(self.ext_entry_frame, self.ext_entry, False)
        self.ext_entry_frame.pack(fill=tk.X, padx=SPACING["widget_padx_nested"], pady=(4, 0))

        tk.Label(left, text=self.lang["example_ext"], font=FONTS["tiny"], fg=COLORS["secondary"], bg=COLORS["bg"]).pack(anchor=tk.W, padx=SPACING["widget_padx_nested"], pady=(2, SPACING["element_pady"]))

        # --- Step 03: Operation ---
        step03 = self._step_frame(left, "step_03")
        self.operation_var = tk.StringVar(value="s2t")
        tk.Radiobutton(left, text=self.lang["s2t_convert"], variable=self.operation_var, value="s2t", state=tk.NORMAL if OPENCC_AVAILABLE else tk.DISABLED, command=self._on_operation_changed, **rb_style).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 4))
        tk.Radiobutton(left, text=self.lang["replace_text"], variable=self.operation_var, value="replace", command=self._on_operation_changed, **rb_style).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 4))

        # Replace Container
        replace_frame = tk.Frame(left, bg=COLORS["bg"])
        replace_frame.pack(fill=tk.X, padx=SPACING["widget_padx_nested"], pady=(4, SPACING["element_pady"]))

        tk.Label(replace_frame, text=self.lang["replace_from"], font=FONTS["small"], fg=COLORS["text_normal"], bg=COLORS["bg"]).pack(anchor=tk.W, pady=(0, 2))
        self.replace_from_frame, self.replace_from = self._create_styled_entry(replace_frame)
        self._toggle_input_state(self.replace_from_frame, self.replace_from, False)
        self.replace_from_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(replace_frame, text=self.lang["replace_to"], font=FONTS["small"], fg=COLORS["text_normal"], bg=COLORS["bg"]).pack(anchor=tk.W, pady=(0, 2))
        self.replace_to_frame, self.replace_to = self._create_styled_entry(replace_frame)
        self._toggle_input_state(self.replace_to_frame, self.replace_to, False)
        self.replace_to_frame.pack(fill=tk.X)

        # --- Step 04: Format Settings ---
        step04 = self._step_frame(left, "step_04")

        # Remove Symbols
        tk.Label(left, text=self.lang["remove_symbols"], font=FONTS["small"], fg=COLORS["text_normal"], bg=COLORS["bg"]).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 2))
        self.symbols_frame, self.symbols_entry = self._create_styled_entry(left)
        self.symbols_frame.pack(fill=tk.X, padx=SPACING["widget_padx"], pady=(0, 0))
        self.symbols_entry.bind("<KeyRelease>", lambda e: self._update_format_preview())
        tk.Label(left, text=f"Suggest: {self.lang['default_symbols']}", font=FONTS["tiny"], fg=COLORS["disabled_fg"], bg=COLORS["bg"]).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(2, 8))

        # Prefix
        tk.Label(left, text=self.lang["add_prefix"], font=FONTS["small"], fg=COLORS["text_normal"], bg=COLORS["bg"]).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 2))
        self.prefix_frame, self.prefix_entry = self._create_styled_entry(left)
        self.prefix_frame.pack(fill=tk.X, padx=SPACING["widget_padx"], pady=(0, 8))
        self.prefix_entry.bind("<KeyRelease>", lambda e: self._update_format_preview())

        # Suffix
        tk.Label(left, text=self.lang["add_suffix"], font=FONTS["small"], fg=COLORS["text_normal"], bg=COLORS["bg"]).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 2))
        self.suffix_frame, self.suffix_entry = self._create_styled_entry(left)
        self.suffix_frame.pack(fill=tk.X, padx=SPACING["widget_padx"], pady=(0, 8))
        self.suffix_entry.bind("<KeyRelease>", lambda e: self._update_format_preview())

        # Preview
        tk.Label(left, text=self.lang["preview_format"], font=FONTS["small"], fg=COLORS["text_normal"], bg=COLORS["bg"]).pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 2))
        self.format_preview = tk.Label(left, text=self.lang["format_preview"], font=FONTS["normal"], fg=COLORS["fg"], bg=COLORS["bg"], wraplength=350, justify=tk.LEFT)
        self.format_preview.pack(anchor=tk.W, padx=SPACING["widget_padx"], pady=(0, 0), fill=tk.X)


        # --- Right panel (Terminal) ---
        right = tk.Frame(main, bg=COLORS["bg"])
        right.grid(row=0, column=1, sticky="nsew", padx=(SPACING["element_padx"], 0))

        # Header Row: Title Left, Status Right
        term_header = tk.Frame(right, bg=COLORS["bg"])
        term_header.pack(fill=tk.X, pady=(0, SPACING["section_padx_bottom"]))

        tk.Label(term_header, text=self.lang["terminal_title"], font=FONTS["header"], fg=COLORS["fg"], bg=COLORS["bg"]).pack(side=tk.LEFT)

        # Status (Moved to Header as per screenshot)
        status_container = tk.Frame(term_header, bg=COLORS["bg"])
        status_container.pack(side=tk.RIGHT)
        tk.Label(status_container, text="STATUS", font=FONTS["tiny"], fg=COLORS["secondary"], bg=COLORS["bg"]).pack(side=tk.LEFT, padx=(0, 8))
        self.status_text = tk.Label(status_container, text="AWAITING EXECUTION", font=FONTS["small"], fg=COLORS["fg"], bg=COLORS["bg"])
        self.status_text.pack(side=tk.LEFT)

        # Log frame
        log_frame = tk.Frame(right, highlightthickness=1, highlightbackground=COLORS["secondary"], highlightcolor=COLORS["fg"], bg=COLORS["bg"])
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, SPACING["widget_pady"]))

        log_inner = tk.Frame(log_frame, bg=COLORS["bg"])
        log_inner.pack(fill=tk.BOTH, expand=True, padx=SPACING["panel_padx_inner"], pady=SPACING["panel_pady_inner"])

        self.log_text = scrolledtext.ScrolledText(log_inner, font=FONTS["small"], state=tk.DISABLED, wrap=tk.WORD, relief="flat", bg=COLORS["bg"], fg=COLORS["text_normal"], insertbackground=COLORS["fg"])
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Buttons (Bottom Right)
        btn_frame = tk.Frame(right, bg=COLORS["bg"])
        btn_frame.pack(fill=tk.X, pady=(SPACING["button_pady"], 0))

        self.execute_btn = tk.Button(
            btn_frame,
            text=self.lang["confirm_rename"],
            command=self.on_confirm_execute,
            **BUTTON_STYLE
        )
        self.execute_btn.pack(side=tk.RIGHT)

        self.preview_btn = tk.Button(
            btn_frame,
            text=self.lang["show_preview"],
            command=self.on_show_preview,
            **BUTTON_STYLE
        )
        self.preview_btn.pack(side=tk.RIGHT, padx=(0, SPACING["button_padx_tight"]))


    def _create_styled_entry(self, parent: tk.Widget) -> Tuple[tk.Frame, tk.Entry]:
        """Creates a 'modern' styled entry with fake padding."""
        container = tk.Frame(
            parent,
            highlightthickness=1,
            highlightbackground=COLORS["secondary"],
            highlightcolor=COLORS["fg"],
            bg=COLORS["input_bg"]
        )
        entry = tk.Entry(container, **ENTRY_STYLE)
        entry.pack(fill=tk.X, expand=True, padx=10, pady=8)

        def on_focus_in(e):
            if entry['state'] == tk.NORMAL:
                container.config(highlightbackground=COLORS["fg"])
        def on_focus_out(e):
            if entry['state'] == tk.NORMAL:
                container.config(highlightbackground=COLORS["secondary"])

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return container, entry

    def _toggle_input_state(self, frame: tk.Frame, entry: tk.Entry, enable: bool) -> None:
        """Toggles state and border visibility."""
        if enable:
            entry.config(state=tk.NORMAL)
            frame.config(highlightthickness=1, highlightbackground=COLORS["secondary"])
        else:
            entry.config(state=tk.DISABLED)
            frame.config(highlightthickness=0)

    def _step_frame(self, parent: tk.Frame, step_key: str) -> tk.Frame:
        """Creates a label strictly; returns current parent for packing widgets below it"""
        tk.Label(parent, text=self.lang[step_key], font=FONTS["header"], fg=COLORS["fg"], bg=COLORS["bg"]).pack(anchor=tk.W, padx=SPACING["label_padx"], pady=SPACING["label_pady"])
        return parent # Return parent to pack items directly into the left column stream

    def _on_filter_changed(self) -> None:
        is_specific = self.filter_var.get() == "specific"
        self._toggle_input_state(self.ext_entry_frame, self.ext_entry, is_specific)

    def _on_mode_changed(self) -> None:
        self.rename_mode = self.mode_var.get()

    def _on_operation_changed(self) -> None:
        is_replace = self.operation_var.get() == "replace"
        self._toggle_input_state(self.replace_from_frame, self.replace_from, is_replace)
        self._toggle_input_state(self.replace_to_frame, self.replace_to, is_replace)

    def _update_format_preview(self) -> None:
        if not self.selected_directory:
            self.format_preview.config(text=self.lang["format_preview"])
            return
        try:
            items = list(self.selected_directory.glob("*"))[:3]
            if not items:
                self.format_preview.config(text=self.lang["format_preview"])
                return
            lines = []
            for item in items:
                if self.rename_mode == "files" and not item.is_file():
                    continue
                preview = self._apply_format(item.name, item.is_dir())
                lines.append(f"{item.name} → {preview}")
            self.format_preview.config(text="\n".join(lines) if lines else self.lang["format_preview"])
        except:
            self.format_preview.config(text=self.lang["format_preview"])

    def _apply_format(self, filename: str, is_dir: bool = False) -> str:
        if is_dir:
            stem, ext = filename, ""
        else:
            stem, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
            ext = f".{ext}" if ext else ""

        if self.operation_var.get() == "s2t" and self.s2t_converter:
            stem = self.s2t_converter.convert(stem)

        for s in self.symbols_entry.get():
            stem = stem.replace(s, "")

        prefix = self.prefix_entry.get().strip()
        if prefix: stem = prefix + stem

        suffix = self.suffix_entry.get().strip()
        if suffix: stem = stem + suffix

        return f"{stem}{ext}"

    def select_directory(self) -> None:
        d = filedialog.askdirectory()
        if d:
            self.selected_directory = Path(d)
            self.dir_label.config(text=str(self.selected_directory), fg=COLORS["fg"])
            self._update_format_preview()

    def log(self, msg: str) -> None:
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def on_show_preview(self) -> None:
        plan = self._get_rename_plan()
        if not plan: return
        self.current_plan = plan
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log("=" * 60)
        self.log(self.lang["log_started"])
        self.log(f"{self.lang['log_found_files'].format(len(plan))}\n")
        for old, new in plan:
            self.log(self.lang["log_success"].format(old.name, new.name))
        self.log("\n" + "=" * 60)
        self.log(self.lang["preview_mode"])
        self.status_text.config(text="PREVIEW READY")

    def on_confirm_execute(self) -> None:
        if not self.current_plan:
            messagebox.showinfo(self.lang["info"], self.lang["no_changes"])
            return
        if not messagebox.askyesno(self.lang["app_title"], self.lang["confirm_count"].format(len(self.current_plan))):
            self.log("\n" + self.lang["execution_cancelled"])
            self.status_text.config(text="CANCELLED")
            return
        self.status_text.config(text="EXECUTING...")
        success, failed = 0, 0
        for old, new in self.current_plan:
            try:
                old.rename(new)
                self.log(self.lang["log_success"].format(old.name, new.name))
                success += 1
            except Exception as e:
                self.log(f"ERROR: {str(e)}")
                failed += 1
        self.log(f"\n{self.lang['log_completed']}")
        self.log(f"{self.lang['log_success_count'].format(success)}")
        self.log(f"{self.lang['log_failed_count'].format(failed)}")
        self.status_text.config(text=f"COMPLETED: {success} SUCCESS, {failed} FAILED")
        messagebox.showinfo(self.lang["completed"], self.lang["completed_msg"].format(success, failed))

    def _get_rename_plan(self) -> Optional[List[tuple]]:
        if not self.selected_directory:
            messagebox.showerror(self.lang["error"], self.lang["no_dir_selected"])
            return None
        try:
            if self.rename_mode == "files":
                items = sorted([f for f in self.selected_directory.iterdir() if f.is_file()], key=lambda x: x.name.lower())
            else:
                items = sorted(self.selected_directory.iterdir(), key=lambda x: x.name.lower())
            if self.rename_mode == "files" and self.filter_var.get() == "specific":
                ext_str = self.ext_entry.get().strip()
                if not ext_str:
                    messagebox.showerror(self.lang["error"], self.lang["no_extension"])
                    return None
                exts = [e.strip().lower() if e.strip().startswith('.') else f'.{e.strip().lower()}' for e in ext_str.split(",")]
                items = [f for f in items if f.suffix.lower() in exts]
        except: return None
        if not items:
            messagebox.showinfo(self.lang["info"], self.lang["no_files"])
            return None
        plan = []
        for f in items:
            try:
                new_name = self._apply_format(f.name, f.is_dir())
                new_path = f.parent / new_name
                if new_path != f and not new_path.exists():
                    plan.append((f, new_path))
            except: pass
        return plan if plan else None


def main():
    root = tk.Tk()
    app = BatchRenameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()