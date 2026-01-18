# Batch File Renaming Tool

🎨 **Hacker Terminal Green Theme** GUI application for powerful batch file renaming with a beautiful, modern interface.

## ✨ Features

### Core Features
- **🟢 Terminal Aesthetic** - Green-on-black hacker terminal style interface with neon green text (#00DD00) on pure black (#000000)
- **📝 Flexible Renaming Operations**
  - Add prefix/suffix to filenames
  - Remove unwanted symbols
  - Find and replace text patterns
  - Simplified to Traditional Chinese conversion (with OpenCC)
- **📁 Dual Rename Mode** - Choose between renaming files only or files + folders together
- **🔍 Smart File Filtering** - Process all files or filter by specific file extensions
- **👀 Live Preview** - Real-time preview of renaming changes before execution
- **📋 Detailed Logging** - Live terminal-style log display with color-coded output
- **⚙️ Modular Architecture** - Clean separation of concerns (UI, themes, translations, logic)
- **📐 Unified Styling System** - Centralized style configuration for consistent UI
- **🎛️ Smart Spacing Management** - Responsive layout with carefully tuned spacing constants

### User Experience Features
- **One-Click Directory Selection** - Browse and select folders with native file dialog
- **Real-Time Format Preview** - See how your settings affect filenames as you change them
- **Safe Execution** - Always preview before renaming, with confirmation dialog
- **Smart Error Handling** - Gracefully handles duplicate names and errors
- **Status Indicator** - Clear indication of application state (Awaiting, Preview Ready, Executing, Completed)
- **Responsive Two-Column Layout** - Split view with controls on left, live output on right
- **Scrollable Interface** - Works on smaller screens with automatic scrollbars
- **Window Size Constraints** - Optimized minimum window size (900x600) for usability
- **English Interface** - Clean, single-language interface for focused workflow

### Technical Highlights
- **Pure Python** - No heavy frameworks, built with standard Tkinter
- **Standalone** - No complex dependencies, only OpenCC for optional S2T feature
- **Cross-Platform** - Works on macOS, Windows, and Linux
- **Terminal-Style Logging** - Monaco monospace font with green-on-black theme
- **Type Safety** - Full type hints for better code maintainability
- **i18n Ready** - Modular translation system (currently English) with easy extensibility

## 📋 Requirements

- **Python**: 3.10+
- **Tkinter**: Included in Python standard library
- **OpenCC** (optional): For Simplified→Traditional Chinese conversion
  ```bash
  pip install opencc
  ```

## 🚀 Installation

### Option 1: Using startup script (Recommended)
```bash
cd batch-files
pip install -r requirements.txt
chmod +x run.sh
./run.sh
```

### Option 2: Direct Python execution
```bash
cd batch-files
pip install -r requirements.txt
python3 batch_rename_gui.py
```

### Option 3: With specific Python version (macOS with Homebrew)
```bash
/opt/homebrew/opt/python@3.12/bin/python3.12 batch_rename_gui.py
```

## 📁 Project Structure

```
batch-files/
├── batch_rename_gui.py       # Main application (UI + business logic)
├── styles.py                 # Theme & styling configuration
├── i18n.py                   # Internationalization (EN/ZH translations)
├── requirements.txt          # Python dependencies
├── run.sh                     # Launcher script
└── README.md                  # This documentation
```

## 🏗️ Architecture & Design

### Core Components

#### `batch_rename_gui.py` - Main Application
The heart of the application, containing:
- **UI Layout**: Responsive two-column design (controls left, output right)
- **Batch Renaming Logic**: 4-step validation pipeline for safe file processing
- **Event Handling**: Directory selection, operation switching, mode changes
- **Error Management**: Graceful error handling with detailed logging
- **State Management**: Tracks current language, theme, and renaming plan

**Key Classes/Methods:**
- `BatchRenameApp`: Main application controller
- `setup_ui()`: Builds complete UI with all controls
- `_get_rename_plan()`: Generates safe rename operations before execution
- `_display_preview()`: Shows preview of rename changes in terminal log
- `_on_mode_changed()`: Handles rename mode selection changes

#### `styles.py` - Unified Styling System
Centralized configuration for visual consistency:

**THEMES Dictionary**
- Color palette: Backgrounds, buttons, text, borders
- Typography: Font families, sizes, weights
- Widget-specific styling: Colors, relief, borders

**SPACING Dictionary** (26 configuration values)
- Section-level: `section_pady`, `section_padx_bottom`
- Element-level: `element_padx`, `element_pady`
- Widget-level: `widget_padx`, `widget_pady`, variations
- Button-specific: `button_padx`, `button_pady`, `button_group_padx`
- Panel/Layout: `panel_padx_right`, `panel_padx_inner`, `panel_pady_inner`
- Label styling: `label_padx`, `label_pady`, title variants
- Status bar: `status_padx`, `status_pady`

**BUTTON_STYLES Dictionary**
- Preset configurations for primary, secondary, and compact buttons
- Centralized button styling for consistency

**Utility Functions**
- `get_widget_config(theme, widget_type)`: Returns style dict for any widget

#### `i18n.py` - Internationalization Engine
Modular translation system with 52+ translation keys:

**LANGUAGES Dictionary**
- English (`en`): Full American English translations (currently active)
- Traditional Chinese (`zh`): Available for future use
- Easily extensible for additional languages

**Coverage Areas**
- Application titles and headers
- Step-by-step workflow labels (6 steps)
- Form labels and placeholders
- Operation descriptions and examples
- Dialog messages and confirmations
- Log messages with formatting placeholders
- Status indicators

**Key Features**
- All text centralized (no hardcoding in UI)
- Simple key-based access: `self.lang["key"]`
- Easy to extend with new languages

### Design Patterns

#### Two-Column Responsive Layout
```
┌─────────────────────────────────┐
│ 📌 BATCH RENAME  [中文/English] │  Header
├──────────────┬──────────────────┤
│ Left Panel   │ Right Panel      │
│ (50% width)  │ (50% width)      │
│              │                  │
│ Steps 01-04  │ Live Terminal    │
│ Settings     │ Output Log       │
│              │                  │
│ Preview      │ Status + Buttons │
│ Output       │                  │
│              │                  │
└──────────────┴──────────────────┘
```

#### Safe Renaming Pipeline
```
Step 1: Validate Input
  ├─ Directory exists
  ├─ Files match filter
  └─ Required fields filled

Step 2: Generate Plan
  ├─ Text transformation (S2T/Replace)
  ├─ Symbol removal
  ├─ Prefix/suffix addition
  ├─ Index numbering
  └─ Check for conflicts

Step 3: User Preview
  └─ Review all changes before execution

Step 4: Execute Safely
  ├─ Process each file individually
  ├─ Log all operations
  ├─ Handle errors gracefully
  └─ Provide detailed summary
```

## 📖 Complete Workflow Reference

### 6-Step Workflow

#### Step 01: Choose Folder & Rename Mode
**Purpose**: Select the directory containing files to rename and choose rename mode.

**Directory Selection:**
- Click "Select Folder" button to open file browser
- Chosen directory path displays in the panel
- **Output**: Selected directory path stored for processing
- **Example**: `/Users/john/Documents/Photos`

**Rename Mode:**
- **Files Only** (default) - Rename only files, ignore folders
- **Files & Folders** - Rename both files and folders together
- **Behavior**: Affects which items are shown in preview and processed

---

#### Step 02: File Filter
**Purpose**: Define which files to process (folders use rename mode setting).

**Options:**
- **All Files** (default)
  - Process every file in the directory
  - Ignores file extensions

- **Specific Type**
  - Process only files matching specified extensions
  - Enter extensions separated by commas
  - Format: `.jpg, .png, .txt` or `jpg, png, txt`
  - Extensions are case-insensitive
  - **Example**: `.jpg, .png` → processes only JPG and PNG files

**Behavior**: Entry field enables/disables based on selection

---

#### Step 03: Choose Operation
**Purpose**: Select the renaming operation to apply.

**Available Operations:**

1. **Simplified to Traditional Chinese (S2T)**
   - Converts simplified Chinese characters to traditional
   - Requires OpenCC library installed
   - Operates on filename stem (not extension)
   - **Example**: `简体字.txt` → `繁體字.txt`
   - **Status**: Disabled if OpenCC not available

2. **Replace Text**
   - Find and replace text in filenames
   - **From**: Text pattern to find
   - **To**: Text to replace with
   - Operates on filename stem
   - **Example**:
     - From: `old`
     - To: `new`
     - Result: `old_file.txt` → `new_file.txt`

**Behavior**: Replace input fields enable only when "Replace Text" selected

---

#### Step 04: Format Settings
**Purpose**: Apply additional formatting transformations.

**Available Settings:**

1. **Remove Symbols**
   - Delete specific characters from filenames
   - Default: `!@#$%^&*()`
   - Customizable list
   - **Example**:
     - Input: `file@2024!.txt`
     - Symbols: `@!`
     - Result: `file2024.txt`

2. **Add Prefix**
   - Insert text at the beginning of filename (before extension)
   - **Example**:
     - Prefix: `[NEW]`
     - Input: `document.pdf`
     - Result: `[NEW]document.pdf`

3. **Add Suffix**
   - Insert text at the end of filename (before extension)
   - **Example**:
     - Suffix: `_backup`
     - Input: `data.xlsx`
     - Result: `data_backup.xlsx`

**Live Preview**
- Shows format preview as you modify settings
- Displays up to 3 sample files from directory
- Format: `original_name.ext → preview_name.ext`
- Updates in real-time as settings change

**Processing Order**
1. Apply S2T/Replace
2. Remove symbols
3. Add prefix
4. Add suffix
---

#### Step 05: Preview Changes
**Purpose**: Review all changes before execution.

**Using Preview:**
1. Click "Show Changes" button
2. Log displays all planned renames
3. Shows: `original_name.ext → new_name.ext` for each file
4. Counts total items to be processed
5. **No files/folders are modified** at this stage

**Log Display:**
- Separator line: `============...`
- Message: "Processing started..."
- Item count: "Found X files" or "Found X items"
- Each rename pair
- Message: "(Preview Mode - Not Yet Executed)"

**Example Log Output:**
```
============================================================
Processing started...
Found 3 files

photo_old.jpg → photo_new.jpg
document.txt → [NEW]document_001.txt
image_2024!.png → image_2024.png

============================================================
(Preview Mode - Not Yet Executed)
```

---

#### Step 06: Confirm & Execute
**Purpose**: Execute the actual file renaming.

**Workflow:**
1. Click "Confirm & Rename" button
2. Confirmation dialog appears with file count
3. **Two options:**
   - **Yes**: Proceed with renaming
   - **No**: Cancel operation (logged as "Execution cancelled")

4. **Execution Progress:**
   - Log clears and shows execution details
   - Processes files one by one
   - Shows success count and failures
   - Displays detailed error messages if any

**Log Display (After Execution):**
```
============================================================
Processing started...
Found 3 files

photo.jpg → photo_001.jpg
document.txt → document_001.txt
image.png → image_001.png

Completed
Success: 3
Failed: 0
```

**Error Handling:**
- Skips files that already exist with new name
- Continues processing even if one file fails
- Logs error message for failed renames
- Shows summary with success/failed counts

**Final Confirmation:**
- Dialog shows final results: `Renamed: X, Failed: Y`
- Files are now renamed in the directory

---

### Processing Order Summary

When you execute a rename:

1. **Input**: Original filename
2. **Text Transformation**: S2T or Replace operation
3. **Symbol Removal**: Delete specified characters
4. **Prefix Addition**: Add text at start
5. **Suffix Addition**: Add text at end
6. **Indexing**: Add sequence number if enabled
7. **Output**: Final renamed filename (with original extension preserved)

**Example Chain:**
```
Input:           file@old!.txt
↓ (Replace old→new)
Output:          file@new!.txt
↓ (Remove @!)
Output:          filenew.txt
↓ (Prefix [2024])
Output:          [2024]filenew.txt
↓ (Suffix _backup)
Output:          [2024]filenew_backup.txt
↓ (Add index)
Output:          [2024]filenew_backup_001.txt
```

## 🎯 Quick Start Guide

### Scenario 1: Simple Prefix Addition
**Goal**: Add date prefix to all photos

1. Click "Select Folder" → Choose folder with photos
2. Step 02: Select "All Files" (or choose "Specific Type" → ".jpg, .png")
3. Step 03: Choose "Replace Text" (or leave S2T if not needed)
4. Step 04:
   - Add Prefix: `2024-01-18_`
   - Check format preview
5. Click "Show Changes" → Review in log
6. Click "Confirm & Rename" → Done!

### Scenario 2: Clean Filenames
**Goal**: Remove special characters from document names

1. Select folder with documents
2. Step 02: Choose "Specific Type" → ".txt, .pdf, .doc"
3. Step 03: Keep "Replace Text" or "S2T"
4. Step 04:
   - Remove Symbols: `!@#$%&*()`
   - Check preview
5. Preview and confirm

### Scenario 3: Rename & Index Files
**Goal**: Sequential numbering for batch processing

1. Select folder
2. Step 02: Filter by type if needed
3. Step 03: Choose operation
4. Step 04:
   - Add Prefix: `batch_`
   - Add Index: ✓ (checked)
5. Preview shows: `batch_001.ext`, `batch_002.ext`, etc.

## 🛠️ Configuration & Customization

### Customizing Theme Colors

Edit `styles.py` to change the appearance:

```python
THEMES = {
    "dark": {
        # Color palette
        "bg_primary": "#000000",        # Window background
        "fg_primary": "#00DD00",        # Text color (bright green)
        "bg_button": "#00DD00",         # Button background
        "border": "#00DD00",            # Border color

        # Typography
        "font_title": ("Monaco", 20, "bold"),
        "font_header": ("Monaco", 16, "bold"),
        "font_normal": ("Monaco", 13),
        "font_small": ("Monaco", 11),
    }
}
```

### Customizing Spacing & Layout

The `SPACING` dictionary controls all padding and margins:

```python
SPACING = {
    "element_padx": 20,              # Main container padding
    "element_pady": 16,              # Section spacing
    "widget_padx": 12,               # Widget padding
    "widget_pady_small": 6,          # Small gaps
    "button_pady": 12,               # Button padding
    # ... 26 total spacing values
}
```

**To adjust overall spacing**, update these key values:
- `element_padx`: Main container horizontal margin
- `element_pady`: Space between major sections
- `widget_padx`: Standard horizontal padding
- `widget_pady`: Standard vertical padding

### Adding a New Language

1. Open `i18n.py`
2. Add new language dictionary:

```python
LANGUAGES = {
    "en": { ... },
    "zh": { ... },
    "ja": {  # Japanese example
        "app_title": "バッチファイル名変更",
        "step_01": "ステップ 01: フォルダを選択",
        "select_dir": "フォルダを選択",
        # ... add all 52+ keys
    }
}
```

4. Test new language by updating `self.lang = LANGUAGES["ja"]` in `batch_rename_gui.py`

### Modifying Button Styles

Edit `BUTTON_STYLES` in `styles.py`:

```python
BUTTON_STYLES = {
    "primary": {
        "padx": SPACING["button_padx"],
        "pady": SPACING["button_pady"],
        "width": None,
    },
    "compact": {
        "padx": SPACING["button_padx_tight"],
        "pady": SPACING["button_pady_tight"],
        "width": 15,  # Fixed width
    }
}
```

## 📋 Complete Configuration

## 💡 Best Practices

### Before Renaming
- ✅ **Always preview first** - Click "Show Changes" to review all modifications
- ✅ **Backup important files** - Create copies before running batch operations
- ✅ **Test with sample files** - Use a test folder first to verify behavior
- ✅ **Check filter settings** - Ensure you're targeting the right file types
- ✅ **Review format preview** - Verify format looks correct on sample names

### During Renaming
- ✅ **Read the confirmation dialog** - Know how many files will be affected
- ✅ **Monitor the log** - Watch for errors during processing
- ✅ **Keep the window open** - Don't close until operation completes

### Common Patterns
```
📸 Photos:
  Filter: .jpg, .png, .heic
  Operation: Add Prefix + Index
  Result: Photo_001.jpg, Photo_002.jpg, ...

📄 Documents:
  Filter: .pdf, .doc, .docx, .txt
  Operation: Remove Symbols + Add Suffix
  Result: document_clean_v2.pdf

🎵 Music:
  Filter: .mp3, .flac, .wav
  Operation: S2T (Chinese) + Remove Symbols
  Result: Clean filename without special characters

📁 Archives:
  Filter: .zip, .rar, .7z
  Operation: Replace + Add Date Prefix
  Result: 2024-01-18_archive_v2.zip
```

## ⚠️ Troubleshooting

### Issue: "macOS version required" Error
**Solution**: This is a Python version issue, not the app. Use appropriate Python:
```bash
# Check Python version
python3 --version  # Should be 3.10+

# If needed, install via Homebrew
brew install python@3.12
/opt/homebrew/opt/python@3.12/bin/python3.12 batch_rename_gui.py
```

### Issue: OpenCC Not Available
**Problem**: S2T (Simplified→Traditional) option is disabled
**Solution**:
```bash
# Install OpenCC
pip install opencc

# Or via Homebrew (macOS)
brew install opencc
```

### Issue: Files Not Renaming
**Checklist**:
- ✓ Directory selected correctly
- ✓ Files match filter criteria and rename mode
- ✓ No files/folders with target names already exist
- ✓ Write permissions for the directory
- ✓ Proper confirmation in dialog

### Issue: UI Spacing Looks Off
**Check**:
1. Window size at least 900x600 (minimum)
2. Update SPACING values in styles.py
3. Clear Python cache: `rm -rf __pycache__ *.pyc`

## 🤝 Contributing

### Reporting Issues
Include:
- Python version: `python3 --version`
- macOS/Windows/Linux version
- Steps to reproduce
- Error messages from terminal

### Improvement Ideas
- Additional renaming operations
- More language support
- Dark/light theme toggle
- Undo/redo functionality

## 📝 Notes & Limitations

### File Processing
- Files sorted alphabetically before renaming
- Existing target files are **skipped** (not overwritten)
- Extension always preserved
- Processing continues even if some files fail

### Character Support
- Supports all Unicode characters in filenames
- Chinese text requires OpenCC for S2T conversion
- Special characters can be removed via "Remove Symbols"

### Performance
- Handles hundreds of files efficiently
- Large operation completes in seconds
- Preview generation instant for small folders
- Log display optimized for terminal output
