#!/usr/bin/env python3
"""Sync the editor defaults from the checked-in sheet, without changing icon cells."""
import json
from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def main():
    manifest = json.loads((ROOT / 'iconsheet.json').read_text())
    sheet = Image.open(ROOT / manifest['sheet']).convert('L')
    size, step = manifest['tileSize'], manifest['tileSize'] + manifest['spacing']
    if size != 32:
        raise ValueError('Editor defaults must be 32x32')
    defaults = {}
    cells = set()
    for icon in manifest['icons']:
        name = icon['name']
        cell = (icon['row'], icon['col'])
        if name in defaults or cell in cells:
            raise ValueError(f'Duplicate name/cell: {name}')
        cells.add(cell)
        x, y = icon['col'] * step, icon['row'] * step
        if x < 0 or y < 0 or x + size > sheet.width or y + size > sheet.height:
            raise ValueError(f'Out-of-bounds tile: {name}')
        bitmap = []
        for yy in range(32):
            for xx in range(0, 32, 8):
                bitmap.append(sum((1 << bit) for bit in range(8)
                                  if sheet.getpixel((x + xx + bit, y + yy)) > manifest['threshold']))
        if not any(bitmap):
            raise ValueError(f'Blank default: {name}')
        defaults[name] = bytes(bitmap).hex().upper()
    page = ROOT / 'index.html'
    source, count = re.subn(r'const STANDARD_ICONS_HEX = \{[^\n]+\};',
                           lambda _: 'const STANDARD_ICONS_HEX = ' + json.dumps(defaults, separators=(',', ':')) + ';',
                           page.read_text())
    if count != 1:
        raise ValueError('Expected one defaults declaration')
    page.write_text(source)
    print(f'Synchronized {len(defaults)} browser defaults')


if __name__ == '__main__':
    main()
