# Hardwareone Icon Tool

Create and manage 32x32 monochrome icons for ESP32 HardwareOne devices.

## Web Tool (Recommended)

**[Github Pages: Icon Tool](https://cadengithubb.github.io/HardwareOne_Icon_Generator/)**

Draw, edit, and export icons entirely in your browser — no dependencies required.

### Features
- **Pixel Drawing** — 32x32 grid canvas with pen, eraser, fill, and line tools
- **Icon Management** — Add, rename, delete, and browse icons in a visual list
- **Import** — Load an existing `iconsheet.png` + `iconsheet.json` to continue editing
- **Export C++** — Download `icons_embedded.cpp` with PROGMEM arrays ready for use in a HardwareOne system
- **Export PNG/JSON** — Download `iconsheet.png` and `iconsheet.json` for the Python workflow
- **Keyboard Shortcuts** — P/E/F/L for tools, Ctrl+Z undo, Ctrl+Shift+Z redo

---

## Python Scripts (Legacy)

These scripts still work if you prefer a local workflow.

### 1. Create or Edit the Iconsheet

**Option A — Regenerate from code:**
```
python3 scripts/draw_iconsheet_png.py
```
Programmatically draws all 87 standard icons to `assets/iconsheet.png`.

**Option B — Start from a blank template:**
```
python3 scripts/create_blank_iconsheet_png.py
```
Creates a blank 512×512 grid PNG for drawing icons manually in an image editor.

**Option C — Generate basic example icons:**
```
python3 scripts/draw_example_icons_to_assets.py
```
Outputs a small set of simple example icons as individual PNGs into `assets/`.

### 2. Update the Icon Registry
> No `iconsheet.json`? Run `python3 scripts/create_iconsheet_json.py` first.

**Edit `iconsheet.json`** — Format: `{"name": "icon_name", "row": X, "col": Y}`

### 3. Export to a .cpp file
```
python3 scripts/export_icons_embedded_cpp.py
```
Reads `iconsheet.json` + `assets/iconsheet.png` → generates `icons_embedded.cpp`
> **Warning:** Completely regenerates the file and erases previous content.

### Utilities
- **`extract_individual_icon_pngs.py`** — Extracts each tile from `iconsheet.png` as a separate PNG file

### Great Success. You now have 32×32 icons for your project in a format that requires no heap allocation.
