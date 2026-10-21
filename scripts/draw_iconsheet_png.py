#!/usr/bin/env python3
"""Rebuild the sheet from the same approved defaults used by the web editor."""
import json
from pathlib import Path
import re

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    source = (ROOT / "index.html").read_text()
    match = re.search(r"const STANDARD_ICONS_HEX = (\{[^\n]+\});", source)
    if match is None:
        raise ValueError("Standard icon bitmaps not found in index.html")
    defaults = json.loads(match.group(1))
    manifest = json.loads((ROOT / "iconsheet.json").read_text())
    size = manifest["tileSize"]
    spacing = manifest["spacing"]
    step = size + spacing
    sheet = Image.new("RGB", (manifest["cols"] * step + spacing,
                              manifest["rows"] * step + spacing), "black")
    draw = ImageDraw.Draw(sheet)
    for col in range(manifest["cols"]):
        x = col * step + size
        draw.line((x, 0, x, sheet.height - 1), fill="#333333", width=spacing)
    for row in range(manifest["rows"]):
        y = row * step + size
        draw.line((0, y, sheet.width - 1, y), fill="#333333", width=spacing)
    for icon in manifest["icons"]:
        bitmap = bytes.fromhex(defaults[icon["name"]])
        if len(bitmap) * 8 != size * size:
            raise ValueError(f"Invalid bitmap size: {icon['name']}")
        tile = Image.new("RGB", (size, size))
        tile.putdata([(255, 255, 255) if byte & (1 << bit) else (0, 0, 0)
                      for byte in bitmap for bit in range(8)])
        sheet.paste(tile, (icon["col"] * step, icon["row"] * step))
    output = ROOT / manifest["sheet"]
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    print(f"Wrote {output} ({len(manifest['icons'])} icons)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
