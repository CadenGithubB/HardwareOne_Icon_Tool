#!/usr/bin/env python3
"""
Generate initial iconsheet.json from existing icon PNGs in assets folder,
or create a starter template if no icons exist.

Run this once when setting up your iconsheet for the first time.
"""

import json
from pathlib import Path

# Paths relative to this script
SCRIPT_DIR = Path(__file__).parent
ICONS_DIR = SCRIPT_DIR.parent
ASSETS_DIR = ICONS_DIR / "assets"
JSON_PATH = ICONS_DIR / "iconsheet.json"

def main():
    # Check for existing individual icon PNGs in assets
    icon_files = sorted(ASSETS_DIR.glob("*.png")) if ASSETS_DIR.exists() else []
    
    # Filter out iconsheet.png itself
    icon_files = [f for f in icon_files if f.name != "iconsheet.png"]
    
    if JSON_PATH.exists():
        print(f"iconsheet.json already exists at: {JSON_PATH}")
        print("Delete it first if you want to regenerate.")
        return
    
    manifest = {
        "tile_size": 32,
        "spacing": 1,
        "threshold": 128,
        "icons": []
    }
    
    if icon_files:
        # Generate entries from existing icon files
        print(f"Found {len(icon_files)} icon PNGs in assets/")
        print("Assigning grid positions row by row...")
        
        cols_per_row = 15  # 512px / (32+1) = ~15 icons per row
        
        for idx, icon_file in enumerate(icon_files):
            name = icon_file.stem  # filename without extension
            row = idx // cols_per_row
            col = idx % cols_per_row
            
            manifest["icons"].append({
                "name": name,
                "row": row,
                "col": col
            })
            print(f"  {name}: row={row}, col={col}")
    else:
        # Create starter template with example entries
        print("No icon PNGs found in assets/. Creating starter template...")
        manifest["icons"] = [
            {"name": "folder", "row": 0, "col": 0},
            {"name": "file", "row": 0, "col": 1},
            {"name": "gear", "row": 0, "col": 2},
            {"name": "wifi", "row": 0, "col": 3},
            {"name": "home", "row": 0, "col": 4},
        ]
        print("  Added example entries (folder, file, gear, wifi, home)")
        print("  Edit these to match your actual icons in iconsheet.png")
    
    # Write JSON
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nCreated: {JSON_PATH}")
    print("\nNext steps:")
    print("  1. Draw icons in assets/iconsheet.png at the specified row/col positions")
    print("  2. Edit iconsheet.json to add/update icon names and positions")
    print("  3. Run: python3 scripts/generate_icons.py")

if __name__ == "__main__":
    main()
