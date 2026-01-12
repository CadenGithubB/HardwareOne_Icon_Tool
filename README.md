# This is a set of Python scripts that is used to generate the icons for the Hardware One project.

## Usage Guide:

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
