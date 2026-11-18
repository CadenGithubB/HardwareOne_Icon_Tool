#!/usr/bin/env python3
"""Verify source/export agreement and portable firmware integration behavior."""
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    merge = load('integrate_firmware_icons')
    artwork = merge.read_artwork()
    manifest = json.loads((ROOT / 'iconsheet.json').read_text())
    page = (ROOT / 'index.html').read_text()
    defaults = json.loads(re.search(r'const STANDARD_ICONS_HEX = (\{[^\n]+\});', page)[1])
    sheet = Image.open(ROOT / manifest['sheet']).convert('RGB')
    assert len(artwork) == len(manifest['icons']) == len(defaults) == 162
    assert list(defaults) == [i['name'] for i in manifest['icons']]
    assert not set(defaults) & merge.REMOVED
    assert [(i['row'], i['col']) for i in manifest['icons']] == [divmod(i, 15) for i in range(162)]
    geometry = json.loads((ROOT / 'docs/icon-geometry.json').read_text())
    tiles = {}
    cells = set()
    for icon in manifest['icons']:
        name = icon['name']; cell = (icon['row'], icon['col'])
        assert cell not in cells; cells.add(cell)
        x, y = icon['col'] * 33, icon['row'] * 33
        tile = sheet.crop((x, y, x+32, y+32))
        bits = [int(v[0] > 128) for v in tile.get_flattened_data()]
        tiles[name] = [bits[y*32:(y+1)*32] for y in range(32)]
        if name == 'file' or name.startswith('file_'):
            assert tile.convert('L').getbbox() == (4, 2, 28, 30), name
        assert any(bits), name
        assert bytes.fromhex(defaults[name]) == artwork[name]['bitmap'], name
        assert bits == [(b >> k) & 1 for b in artwork[name]['bitmap'] for k in range(8)], name
        assert Image.open(io.BytesIO(artwork[name]['png'])).convert('RGB').tobytes() == tile.tobytes(), name
    for name, axes in geometry['symmetry'].items():
        pixels = tiles[name]
        if 'x' in axes: assert pixels == [row[::-1] for row in pixels], name
        if 'y' in axes: assert pixels == pixels[::-1], name
        if axes == 'rot90': assert pixels == [list(row) for row in zip(*pixels[::-1])], name
    for name in ['file_csv', 'file_model']:
        assert tiles[name][12:28] == [row[::-1] for row in tiles[name][12:28]], name
    for a, b in [('memory', 'notify_system'), ('notify_cli', 'terminal')]:
        diff = sum((x ^ y).bit_count() for x, y in zip(artwork[a]['bitmap'], artwork[b]['bitmap']))
        assert diff > 60, (a, b, diff)
    assert artwork['file_json']['bitmap'] != artwork['file_code']['bitmap']
    with tempfile.TemporaryDirectory(prefix='hw1-icons-') as tmp:
        tmp = Path(tmp)
        # Exercise both supported regeneration directions on a disposable copy.
        (tmp / 'assets').mkdir()
        shutil.copy2(ROOT / 'iconsheet.json', tmp / 'iconsheet.json')
        shutil.copy2(ROOT / 'index.html', tmp / 'index.html')
        generator = load('draw_iconsheet_png'); generator.ROOT = tmp; generator.main()
        assert Image.open(tmp / 'assets/iconsheet.png').convert('RGB').tobytes() == sheet.tobytes()
        sync = load('sync_defaults'); sync.ROOT = tmp; sync.main()
        assert (tmp / 'index.html').read_text() == page
    print('PASS: 162 defaults, sheet tiles, PNGs and bitmaps agree; both regeneration directions match.')
    print('PASS: declared mirror/rotation constraints and 14 enlarged page bounds.')
    print('PASS: memory/system and CLI/terminal pairs have distinct artwork.')


if __name__ == '__main__':
    main()
