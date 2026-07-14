#!/usr/bin/env python3
"""
Draw first-pass placeholder glyphs into seeded (blank) icon slots.

Run AFTER reorganize_iconsheet.py (which lays out the grid + blank seeds).
Reads iconsheet.json for each icon's cell, draws a white-on-black 32x32 glyph
into that cell of assets/iconsheet.png. Only touches the names listed here;
everything else is left untouched. Re-runnable.

  python3 scripts/reorganize_iconsheet.py      # layout + blank seeds
  python3 scripts/draw_placeholder_glyphs.py   # fill some blanks with art
"""
import json, os
from PIL import Image, ImageDraw

TOOL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TILE, STEP = 32, 33
W, B = (255, 255, 255), (0, 0, 0)

# ---- 32x32 glyphs (white on black). Bold strokes so they read when scaled. ---
def g_logo(d):        # "H1" monogram — HardwareOne brand-mark placeholder
    d.rectangle([6, 7, 9, 25], fill=W)          # H left
    d.rectangle([14, 7, 17, 25], fill=W)        # H right
    d.rectangle([9, 14, 14, 17], fill=W)        # H bar
    d.rectangle([22, 7, 25, 25], fill=W)        # 1 stem
    d.rectangle([18, 23, 28, 25], fill=W)       # 1 base
    d.polygon([(22, 7), (22, 11), (18, 11)], fill=W)  # 1 flag

def g_password(d):    # key
    d.ellipse([3, 4, 18, 19], fill=W)
    d.ellipse([7, 8, 14, 15], fill=B)           # ring hole
    d.rectangle([15, 10, 28, 13], fill=W)       # shaft
    d.rectangle([22, 13, 24, 20], fill=W)       # tooth
    d.rectangle([26, 13, 28, 18], fill=W)       # tooth

def g_gps(d):         # crosshair / position-fix target
    d.ellipse([7, 7, 25, 25], fill=W)
    d.ellipse([11, 11, 21, 21], fill=B)         # ring
    d.ellipse([14, 14, 18, 18], fill=W)         # center dot
    d.rectangle([15, 1, 17, 8], fill=W)         # ticks N/S/E/W
    d.rectangle([15, 24, 17, 31], fill=W)
    d.rectangle([1, 15, 8, 17], fill=W)
    d.rectangle([24, 15, 31, 17], fill=W)

def g_map(d):         # folded map with a marker
    d.rectangle([3, 7, 28, 25], outline=W, width=2)
    d.line([11, 7, 11, 25], fill=W, width=1)    # fold creases
    d.line([20, 7, 20, 25], fill=W, width=1)
    d.ellipse([15, 10, 21, 16], fill=W)         # pin head
    d.polygon([(15, 14), (21, 14), (18, 21)], fill=W)  # pin point
    d.ellipse([17, 12, 19, 14], fill=B)         # pin hole

def g_bond(d):        # two devices with a bidirectional link (master/worker)
    d.rectangle([2, 9, 11, 23], outline=W, width=2)
    d.rectangle([21, 9, 30, 23], outline=W, width=2)
    d.rectangle([14, 15, 18, 17], fill=W)       # link shaft
    d.polygon([(11, 16), (15, 12), (15, 20)], fill=W)   # arrow -> left device
    d.polygon([(21, 16), (17, 12), (17, 20)], fill=W)   # arrow -> right device

def g_llm(d):         # chat bubble + AI sparkle
    d.rectangle([4, 4, 28, 21], outline=W, width=2)
    d.polygon([(9, 21), (9, 28), (16, 21)], fill=W)     # tail
    d.polygon([(16, 6), (18, 11), (24, 13), (18, 15),
               (16, 20), (14, 15), (8, 13), (14, 11)], fill=W)  # 4-point sparkle

def g_bolt(d):        # lightning bolt — event trigger
    d.polygon([(19, 2), (8, 17), (15, 17), (13, 30), (24, 12), (17, 12)], fill=W)

GLYPHS = {
    "logo": g_logo, "password": g_password, "gps": g_gps, "map": g_map,
    "bond": g_bond, "llm": g_llm, "bolt": g_bolt,
}

def main():
    manifest = json.load(open(os.path.join(TOOL, "iconsheet.json")))
    pos = {ic["name"]: (ic["row"], ic["col"]) for ic in manifest["icons"]}
    sheet = Image.open(os.path.join(TOOL, "assets", "iconsheet.png")).convert("RGB")

    done = []
    for name, fn in GLYPHS.items():
        if name not in pos:
            print(f"  ! {name}: no slot in manifest, skipped"); continue
        r, c = pos[name]
        tile = Image.new("RGB", (TILE, TILE), B)
        fn(ImageDraw.Draw(tile))
        sheet.paste(tile, (c * STEP, r * STEP))     # tiles flush at offset 0
        done.append(f"{name}@{r},{c}")
    sheet.save(os.path.join(TOOL, "assets", "iconsheet.png"))
    print("drew " + str(len(done)) + " placeholder glyphs: " + ", ".join(done))

if __name__ == "__main__":
    main()
