#!/usr/bin/env python3
"""
Icon Template Generator
Creates a 512x512px canvas with a grid for drawing 32x32 icons
Outputs to icons/assets/ by default.
"""

from pathlib import Path
from PIL import Image, ImageDraw
import sys

# Paths relative to this script
SCRIPT_DIR = Path(__file__).parent
ICONS_DIR = SCRIPT_DIR.parent
ASSETS_DIR = ICONS_DIR / "assets"

def create_icon_template(output_path=None, show_grid=True, show_markers=False, tile_size=32, spacing=1):
    """
    Create a 512x512px template for drawing 32x32 icons.
    Outputs to icons/assets/iconsheet.png by default.
    """
    # Default output to assets folder
    if output_path is None:
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = ASSETS_DIR / "iconsheet.png"
    
    # Create white canvas
    img = Image.new('RGB', (512, 512), 'white')
    draw = ImageDraw.Draw(img)
    
    if show_grid:
        # Draw grid lines to show icon boundaries
        icon_size = int(tile_size)
        spacing = int(spacing)
        step = icon_size + spacing
        
        # Calculate how many icons fit (start at 0, not 1)
        icons_per_row = 512 // step
        
        print(f"Template: 512x512px")
        print(f"Icon size: {icon_size}x{icon_size}px")
        print(f"Spacing: {spacing}px")
        print(f"Icons per row/column: {icons_per_row}")
        print(f"Total icon slots: {icons_per_row * icons_per_row}")
        
        # Draw vertical lines (grid boundaries)
        for i in range(icons_per_row + 1):
            x = i * step
            if x <= 512:
                draw.line([(x, 0), (x, 512)], fill=(200, 200, 200), width=1)
        
        # Draw horizontal lines (grid boundaries)
        for i in range(icons_per_row + 1):
            y = i * step
            if y <= 512:
                draw.line([(0, y), (512, y)], fill=(200, 200, 200), width=1)
        
        # Optionally draw red markers at first few icon positions for reference
        if show_markers:
            reference_positions = [
                (0, 0, "0,0"),
                (17, 0, "17,0"),
                (0, 17, "0,17"),
                (34, 0, "34,0"),
                (0, 34, "0,34"),
            ]
            
            for x, y, label in reference_positions:
                # Draw small red corner marker
                draw.rectangle([x, y, x+2, y+2], fill=(255, 0, 0))
    
    # Save template
    img.save(output_path)
    print(f"\nSaved: {output_path}")
    print("\nNext steps:")
    print(f"  1) Open {output_path} in your pixel art editor")
    print(f"  2) Draw {int(tile_size)}x{int(tile_size)} icons in the grid squares (leave {int(spacing)}px gaps)")
    print("  3) Save/export when done")
    print("  4) Optional: extract tiles to separate PNGs:")
    print(f"     python3 icons/scripts/extract_icons.py {output_path} --tile-size {int(tile_size)} --spacing {int(spacing)}")
    print("  5) Preferred: update icons/iconsheet.json then generate embedded icons:")
    print("     python3 icons/scripts/generate_icons.py")

def create_blank_template(output_path="icon_template_blank.png"):
    """Create a blank white 512x512px canvas without grid"""
    img = Image.new('RGB', (512, 512), 'white')
    img.save(output_path)
    print(f"Saved blank template: {output_path}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Create icon template canvas')
    parser.add_argument('--blank', action='store_true', help='Create blank template without grid')
    parser.add_argument('--markers', action='store_true', help='Show red reference markers')
    parser.add_argument('--tile-size', type=int, default=32, help='Icon tile size in pixels (default: 32)')
    parser.add_argument('--spacing', type=int, default=1, help='Spacing between tiles in pixels (default: 1)')
    parser.add_argument('--output', '-o', default=None, help='Output filename (default: assets/iconsheet.png)')
    
    args = parser.parse_args()
    
    if args.blank:
        out = args.output or str(ASSETS_DIR / "iconsheet_blank.png")
        create_blank_template(out)
    else:
        create_icon_template(args.output, show_grid=True, show_markers=args.markers, tile_size=args.tile_size, spacing=args.spacing)
