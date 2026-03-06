#!/usr/bin/env python3
"""
Create basic example icons using PIL (no external dependencies).
Outputs to icons/assets/ directory.

This is an optional step for users who want pre-made basic icons
instead of drawing their own in the iconsheet.
"""

from pathlib import Path
from PIL import Image, ImageDraw

# Paths relative to this script
SCRIPT_DIR = Path(__file__).parent
ICONS_DIR = SCRIPT_DIR.parent
ASSETS_DIR = ICONS_DIR / "assets"

# Icon size (32x32 to match iconsheet tiles)
ICON_SIZE = 32

def create_folder_icon():
    """Create a folder icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    # Folder body
    draw.rectangle([4, 10, 28, 26], fill=0)
    # Folder tab
    draw.rectangle([4, 8, 12, 12], fill=0)
    return img

def create_file_icon():
    """Create a file icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    # File body
    draw.rectangle([8, 4, 24, 28], fill=0)
    # Corner fold
    draw.polygon([(24, 4), (24, 10), (18, 4)], fill=255)
    return img

def create_gear_icon():
    """Create a gear/settings icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    # Center circle
    draw.ellipse([10, 10, 22, 22], fill=0)
    # Inner circle (hole)
    draw.ellipse([13, 13, 19, 19], fill=255)
    # Teeth (simplified as rectangles)
    for angle in range(0, 360, 45):
        import math
        rad = math.radians(angle)
        x = 16 + int(10 * math.cos(rad))
        y = 16 + int(10 * math.sin(rad))
        draw.rectangle([x-2, y-2, x+2, y+2], fill=0)
    return img

def create_wifi_icon():
    """Create a wifi icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    # Arcs (simplified as lines)
    draw.arc([4, 8, 28, 32], 200, 340, fill=0, width=2)
    draw.arc([8, 12, 24, 28], 200, 340, fill=0, width=2)
    draw.arc([12, 16, 20, 24], 200, 340, fill=0, width=2)
    # Dot at bottom
    draw.ellipse([14, 22, 18, 26], fill=0)
    return img

def create_home_icon():
    """Create a home icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    # Roof
    draw.polygon([(16, 4), (4, 14), (28, 14)], fill=0)
    # House body
    draw.rectangle([8, 14, 24, 28], fill=0)
    # Door
    draw.rectangle([13, 18, 19, 28], fill=255)
    return img

def create_arrow_up_icon():
    """Create an up arrow icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    draw.polygon([(16, 4), (6, 18), (12, 18), (12, 28), (20, 28), (20, 18), (26, 18)], fill=0)
    return img

def create_arrow_down_icon():
    """Create a down arrow icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    draw.polygon([(16, 28), (6, 14), (12, 14), (12, 4), (20, 4), (20, 14), (26, 14)], fill=0)
    return img

def create_check_icon():
    """Create a checkmark icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    draw.line([(6, 16), (12, 24), (26, 8)], fill=0, width=3)
    return img

def create_x_icon():
    """Create an X icon."""
    img = Image.new('L', (ICON_SIZE, ICON_SIZE), 255)
    draw = ImageDraw.Draw(img)
    draw.line([(8, 8), (24, 24)], fill=0, width=3)
    draw.line([(24, 8), (8, 24)], fill=0, width=3)
    return img

def main():
    print("Creating example icons using PIL...")
    
    # Ensure assets directory exists
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Define icons to create
    icons = {
        "folder": create_folder_icon,
        "file": create_file_icon,
        "gear": create_gear_icon,
        "wifi": create_wifi_icon,
        "home": create_home_icon,
        "arrow_up": create_arrow_up_icon,
        "arrow_down": create_arrow_down_icon,
        "check": create_check_icon,
        "x_close": create_x_icon,
    }
    
    created = 0
    for name, create_func in icons.items():
        try:
            img = create_func()
            output_path = ASSETS_DIR / f"{name}.png"
            img.save(output_path)
            print(f"  Created: {name}.png")
            created += 1
        except Exception as e:
            print(f"  Error creating {name}.png: {e}")
    
    print(f"\nCreated {created}/{len(icons)} icons in: {ASSETS_DIR}")
    print("\nThese are individual icon files. To use them:")
    print("  1. Place them in the iconsheet.png at the desired grid positions")
    print("  2. Update iconsheet.json with the name and row/col")
    print("  3. Run: python3 scripts/generate_icons.py")

if __name__ == "__main__":
    main()
