# Hardwareone Icon Tool

Create and manage 32x32 monochrome icons for ESP32 HardwareOne devices.

## Web Tool (Recommended)

**[Github Pages: Icon Tool](https://cadengithubb.github.io/HardwareOne_Icon_Tool/)**

Draw, edit, and export icons entirely in your browser — no dependencies required.

Click **Defaults** to load the expanded set of 162 icons (75 additions and two revisions to the original 87). The checked-in iconsheet and C++ exports contain the same artwork, including centered warning and refresh symbols, smooth arrow tips, the JSON semicolon, and the two-dot image icon.

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
Rebuilds `assets/iconsheet.png` from the browser’s current standard icon bitmaps, using `iconsheet.json` for the layout (requires Pillow).

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

## Expanded artwork and regeneration

The 162-icon sheet includes every name in [the request list](docs/ICON_REQUESTS.md), including all 23 planned symbols. Existing 87 cells and names are retained; additions follow them. `memory` is a RAM module and `notify_cli` has a notification badge. All icons are pure black/white 32×32 tiles.

- `assets/iconsheet.png` + `iconsheet.json` are the editable artwork and layout.
- `python3 scripts/sync_defaults.py` synchronizes browser Defaults from that sheet.
- `python3 scripts/draw_iconsheet_png.py` rebuilds the same sheet from browser Defaults.
- `python3 scripts/export_icons_embedded_cpp.py` writes the generic C++ export **inside this repository**.
- `scripts/icon-designs.mjs` contains the repaired expansion’s deterministic pixel definitions and explicit symmetry rules.
- `python3 scripts/test_icons.py` checks defaults, tiles, both export formats and regeneration (requires Pillow).

The editor releases obsolete thumbnail and export canvases to support the larger set.

## HardwareOne firmware integration

Use the firmware-aware installer rather than copying the generic `icons_embedded.cpp` over a newer `System_Icons.cpp`:

```sh
python3 scripts/integrate_firmware_icons.py "/path/to/HardwareOne" --check
python3 scripts/integrate_firmware_icons.py "/path/to/HardwareOne"
```

It updates matching artwork and adds missing registry entries while retaining existing build guards, lookup functions, extra icons and aliases. `bond` artwork maps to the firmware’s existing `pair_*` identifiers; `battery_full` follows `battery_100`. New feature guards are in `firmware-icons.json`. The 23 unused backlog icons are opt-in with `HW1_ICON_INCLUDE_PLANNED=1`; they remain available in the editor regardless.

If `components/hardwareone/icons/iconsheet.json` exists, the installer merges artwork into that generator’s existing cells, fills retained reserved names, removes the eight rejected names, compacts cells, and preserves unknown artwork and metadata, and updates its `scripts/generate_icons.py` entry point. Timestamped backups are written beside changed files. The installed generator reads its sheet and preserves firmware lookup/build policy. Requires Pillow when synchronizing a nested generator. Run it normally after editing the nested sheet:

```sh
python3 components/hardwareone/icons/scripts/generate_icons.py
```

Menu wiring and extension mappings are deliberately outside this asset update. New icons are registered for callers to use, subject to their feature guard. No full ESP-IDF build or physical-device test was performed.

## Pixel-style rebuild

The expansion now uses square-ended 2px pixel strokes, half-pixel-centered circular masks, simpler symbols, and explicit mirror/rotation constraints (`docs/icon-geometry.json`). Expected symmetric shapes are checked directly against their exported pixels. The chart has no marker dots or rounded endcaps.

Every file-format icon and the generic file share a 24×28 page frame at (4,2), expanded by two pixels on each side of the original frame, inside the unchanged 32×32 tile. file_video contains a larger side-profile video camera. The JSON semicolon and both image dots are retained. The original 77 icons outside the file family, memory and notify_cli remain pixel-identical.

This repair was constructed in the pixel definitions, imported into the editor for visual review, and verified against its PNG export. It has not been committed or pushed.
