#!/usr/bin/env python3
"""
Batch File Renaming Tool - Style Configuration
Hacker Terminal Green theme design
"""
from typing import Tuple
from i18n import DEFAULT_LANGUAGE

THEMES = {
    "dark": {
        # Background Colors (Hacker Terminal Style)
        "bg_primary": "#000000",              # Primary background (pure black)
        "bg_secondary": "#0A0A0A",            # Secondary background (very dark)
        "bg_tertiary": "#0D0D0D",             # Tertiary background (card)
        "bg_input": "#000000",                # Input field background (black)

        # Button Colors (Green Neon)
        "bg_button": "#00DD00",               # Primary action button (bright green)
        "bg_button_hover": "#166534",         # Brighter green on hover
        "fg_button": "#000000",               # Black text on buttons

        # Secondary Button
        "bg_button_secondary": "#1A3A1A",     # Dark green secondary button
        "fg_button_secondary": "#00DD00",     # Green text

        # Text Colors
        "fg_primary": "#00DD00",              # Primary text (bright green)
        "fg_secondary": "#16a34a",            # Secondary text (darker green)
        "fg_tertiary": "#006600",             # Tertiary text (even darker green)

        # Border & Separator
        "border": "#00DD00",                  # Green separator color

        # Typography (Monospace - Terminal Style)
        "font_title": ("Monaco", 20, "bold"),
        "font_header": ("Monaco", 16, "bold"),
        "font_normal": ("Monaco", 13),
        "font_small": ("Monaco", 11),
        "font_log": ("Monaco", 11),
    }
}

# Widget Style Presets
def get_widget_config(theme: dict, widget_type: str) -> dict:
    """Get style configuration for widget type"""
    configs = {
        "label": {
            "bg": theme["bg_primary"],
            "fg": theme["fg_primary"]
        },
        "label_secondary": {
            "bg": theme["bg_primary"],
            "fg": theme["fg_secondary"]
        },
        "frame": {
            "bg": theme["bg_primary"]
        },
        "entry": {
            "bg": theme["bg_input"],
            "fg": theme["fg_primary"],
            "insertbackground": theme["fg_primary"],
            "relief": "solid",
            "bd": 1,
            "borderwidth": 1
        },
        "button": {
            "bg": theme["bg_button"],
            "fg": theme["fg_button"],
            "activebackground": theme["bg_button_hover"],
            "activeforeground": theme["fg_button"],
            "relief": "solid",
            "bd": 1,
            "padx": 20,
            "pady": 10,
            "highlightthickness": 0,
            "font": ("Monaco", 12, "bold")
        },
        "button_secondary": {
            "bg": theme["bg_button_secondary"],
            "fg": theme["fg_button_secondary"],
            "activebackground": theme["border"],
            "activeforeground": theme["fg_primary"],
            "relief": "solid",
            "bd": 1,
            "padx": 12,
            "pady": 8,
            "highlightthickness": 0
        },
        "checkbox": {
            "bg": theme["bg_primary"],
            "fg": theme["fg_primary"],
            "selectcolor": theme["bg_input"],
            "activebackground": theme["bg_primary"],
            "activeforeground": theme["fg_primary"]
        },
        "radio": {
            "bg": theme["bg_primary"],
            "fg": theme["fg_primary"],
            "selectcolor": theme["bg_input"],
            "activebackground": theme["bg_primary"],
            "activeforeground": theme["fg_primary"]
        },
        "text": {
            "bg": theme["bg_input"],
            "fg": theme["fg_primary"],
            "insertbackground": theme["fg_primary"],
            "relief": "solid",
            "bd": 1
        }
    }
    return configs.get(widget_type, {})

WINDOW_CONFIG = {
    "width": 700,
    "height": 800,
    "resizable": (True, True),
}

SPACING = {
    # Section-level spacing
    "section_pady": 24,         # Section spacing (more generous)
    "section_padx_bottom": 12,  # Section bottom padding alternative

    # Element-level spacing
    "element_pady": 16,         # Element vertical spacing
    "element_padx": 20,         # Element horizontal spacing (card inset)

    # Widget-level spacing (internal padding within containers)
    "widget_padx": 12,          # Standard widget horizontal padding
    "widget_padx_nested": 24,   # Nested widget horizontal padding
    "widget_pady": 12,          # Standard widget vertical padding
    "widget_pady_small": 6,     # Small widget padding
    "widget_pady_tiny": 3,      # Tiny widget padding
    "widget_pady_input": 8,     # Input field vertical padding
    "widget_pady_input_between": (0, 8),  # Space between input label and field
    "widget_pady_between": (0, 12),  # Space between sections

    # Button spacing
    "button_pady": 12,          # Button padding
    "button_padx": 20,          # Button padding
    "button_pady_tight": 8,     # Tight button padding
    "button_padx_tight": 6,     # Tight button padding
    "button_group_padx": (0, 6), # Button group spacing

    # Panel/Column spacing
    "panel_padx_right": (0, 12),    # Right column gap between panels
    "panel_padx_inner": 1,          # Inner border padding
    "panel_pady_inner": 1,          # Inner border padding

    # Label spacing
    "label_padx": 12,           # Label horizontal padding
    "label_pady": (12, 8),      # Label vertical padding
    "label_title_padx": 12,     # Title label padding
    "label_title_pady": (12, 8), # Title label padding

    # Status bar spacing
    "status_padx": 12,          # Status bar padding
    "status_pady": 8,           # Status bar padding
}

# Button Style Presets (commonly used button configurations)
BUTTON_STYLES = {
    "primary": {
        # Main action button (Confirm & Rename)
        "padx": SPACING["button_padx"],
        "pady": SPACING["button_pady"],
        "width": None,
    },
    "secondary": {
        # Secondary action button (Show Changes)
        "padx": SPACING["button_padx"],
        "pady": SPACING["button_pady"],
        "width": None,
    },
    "compact": {
        # Compact/tight button
        "padx": SPACING["button_padx_tight"],
        "pady": SPACING["button_pady_tight"],
        "width": 15,  # Fixed width for folder select button
    },
}

DEFAULT_THEME = "dark"


