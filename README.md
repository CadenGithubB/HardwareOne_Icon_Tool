# HardwareOne Icon Generator

Create and manage 32x32 monochrome icons for ESP32 HardwareOne devices.

## Web Tool (Recommended)

**[Open Icon Generator](https://cadengithubb.github.io/HardwareOne_Icon_Generator/)**

Draw, edit, and export icons entirely in your browser — no dependencies required.

### Features
- **Pixel Drawing** — 32x32 grid canvas with pen, eraser, fill, and line tools
- **Icon Management** — Add, rename, delete, and browse icons in a visual list
- **Import** — Load an existing `iconsheet.png` + `iconsheet.json` to continue editing
- **Export C++** — Download `icons_embedded.cpp` with PROGMEM arrays ready for firmware
- **Export PNG/JSON** — Download `iconsheet.png` and `iconsheet.json` for the Python workflow
- **Keyboard Shortcuts** — P/E/F/L for tools, Ctrl+Z undo, Ctrl+Shift+Z redo

---

## Python Scripts (Legacy)

These scripts still work if you prefer a local workflow.

### 1. Create or Edit the Iconsheet
> No iconsheet? Run `python3 scripts/icon_template_generator.py` first.

**Edit `assets/iconsheet.png`** - Draw within the 32x32 tiles (don't edit the 1px spacing lines)
- **Optional**: Run `python3 scripts/create_icons.py` for basic example icons

### 2. Update the Icon Registry
> No iconsheet.json? Run `python3 scripts/generate_iconsheet_json.py` first.

**Add/update entries in `iconsheet.json`** - Format: `{"name": "icon_name", "row": X, "col": Y}`

### 3. Export Icons
**Run `python3 scripts/generate_icons.py`**
- Reads `iconsheet.json` + `assets/iconsheet.png` -> generates `icons_embedded.cpp`
- **Warning:** This completely regenerates the file and erases previous content

### Great Success. You now have 32x32 icons for your project in a format that requires no heap allocation.
