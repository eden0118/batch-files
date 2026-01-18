#!/usr/bin/env python3
"""
Batch File Renaming Tool - Compact Style Configuration
Optimized for 1080p Screens (Lower vertical footprint)
"""

# Color Palette (Unchanged)
COLORS = {
    "bg": "#121212",
    "fg": "#00DD00",
    "text_normal": "#E0E0E0",
    "secondary": "#16a34a",
    "input_bg": "#2D2D2D",
    "input_fg": "#FFFFFF",
    "btn_bg": "#FFFFFF",
    "btn_fg": "#006400",
    "disabled_fg": "#555555",
}

# Fonts - Slightly reduced for compactness
FONTS = {
    "title": ("Helvetica Neue", 18, "bold"),      # Was 22
    "header": ("Helvetica Neue", 13, "bold"),     # Was 15
    "normal": ("Helvetica Neue", 11),             # Was 12
    "small": ("Helvetica Neue", 10),              # Was 11
    "tiny": ("Helvetica Neue", 9),
}

# Button Configuration (Compact)
BUTTON_STYLE = {
    "font": ("Helvetica Neue", 11, "bold"),
    "bg": COLORS["btn_bg"],
    "fg": COLORS["btn_fg"],
    "activebackground": "#dddddd",
    "activeforeground": COLORS["btn_fg"],
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "padx": 16,                     # Reduced from 24
    "pady": 5,                      # Reduced from 8
    "cursor": "hand2"
}

# Input/Entry Configuration
ENTRY_STYLE = {
    "font": FONTS["normal"],
    "bg": COLORS["input_bg"],
    "fg": COLORS["input_fg"],
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "insertbackground": COLORS["fg"],
    "width": 10
}

# Window Configuration - Much smaller default
WINDOW_CONFIG = {
    "width": 960,                   # Fits nicely in half-1080p width
    "height": 680,                  # Safe height for all screens
    "resizable": (True, True),
}

# Spacing Configuration - TIGHTENED
SPACING = {
    "section_pady": 10,             # Was 20
    "section_padx_bottom": 4,
    "element_pady": 8,              # Was 14 (Major vertical saver)
    "element_padx": 16,             # Was 24
    "widget_padx": 10,
    "widget_padx_nested": 20,
    "widget_pady": 6,
    "widget_pady_small": 2,
    "widget_pady_tiny": 1,          # Minimal gap between label and input
    "widget_pady_input": 4,
    "widget_pady_input_between": (0, 4),
    "button_pady": 10,
    "button_padx_tight": 8,
    "panel_padx_right": (0, 16),
    "panel_padx_inner": 1,
    "panel_pady_inner": 1,
    "label_padx": 0,
    "label_pady": (4, 4),
    "status_padx": 8,
    "status_pady": 4,
}