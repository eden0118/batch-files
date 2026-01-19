"""Reusable UI components for the Batch Renamer application"""

import flet as ft
from typing import Callable, Optional, Dict, Any
from ..utils.constants import COLORS


class FilePathInput:
    """檔案路徑輸入組件"""

    def __init__(self, label: str, on_change: Callable, on_submit: Callable):
        self.field = ft.TextField(
            label=label,
            expand=True,
            dense=True,
            border_color=COLORS["accent"],
            bgcolor="black"
        )
        self.field.on_submit = on_submit
        self.field.on_change = on_change

    @property
    def value(self) -> str:
        return self.field.value

    @value.setter
    def value(self, val: str):
        self.field.value = val

    def update(self):
        self.field.update()


class RadioGroup:
    """單選組件"""

    def __init__(self, value: str, options: list, on_change: Callable):
        radio_items = [
            ft.Radio(value=opt["value"], label=opt["label"], fill_color=COLORS["accent"])
            for opt in options
        ]
        self.group = ft.RadioGroup(value=value, content=ft.Row(radio_items))
        self.group.on_change = on_change

    @property
    def value(self) -> str:
        return self.group.value

    @value.setter
    def value(self, val: str):
        self.group.value = val

    def update(self):
        self.group.update()


class StatusBanner:
    """狀態橫幅"""

    STATUS_CONFIG = {
        "idle": {"color": "grey700", "icon": ft.Icons.INFO_OUTLINE},
        "ready": {"color": "green700", "icon": ft.Icons.CHECK_CIRCLE_OUTLINE},
        "warning": {"color": "orange700", "icon": ft.Icons.WARNING_AMBER_ROUNDED},
        "error": {"color": "red700", "icon": ft.Icons.ERROR_OUTLINE}
    }

    def __init__(self):
        self.container = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, color="white"),
                ft.Text("", color="white", weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="grey700",
            padding=12,
            border_radius=8
        )

    def set_status(self, status_type: str, message: str):
        """設置狀態"""
        config = self.STATUS_CONFIG.get(status_type, self.STATUS_CONFIG["idle"])
        self.container.content = ft.Row([
            ft.Icon(config["icon"], color="white"),
            ft.Text(message, color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER)
        self.container.bgcolor = config["color"]
        self.container.update()


class LivePreviewLog:
    """即時預覽日誌"""

    def __init__(self):
        self.log_column = ft.Column(spacing=4, scroll="auto")

    def add_text(self, text: str, color: str = "white"):
        """添加文字"""
        self.log_column.controls.append(ft.Text(text, color=color))

    def clear(self):
        """清空"""
        self.log_column.controls.clear()

    def set_controls(self, controls: list):
        """設置控制項"""
        self.log_column.controls = controls

    def update(self):
        self.log_column.update()
