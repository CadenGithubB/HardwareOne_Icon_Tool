#!/usr/bin/env python3
"""Merge approved artwork into HardwareOne while preserving existing firmware policy."""
import argparse
import io
from datetime import datetime
import json
from pathlib import Path
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent.parent
ARRAY = re.compile(r'(static const uint8_t PROGMEM icon_(\w+)_(png|bitmap)\[\]\s*=\s*\{)(.*?)(\};)', re.S)
REGISTRY = re.compile(r'(const EmbeddedIcon EMBEDDED_ICONS\[\] PROGMEM\s*=\s*\{)(.*?)(\n\};)', re.S)
ALIASES = {'pair_link': 'bond', 'pair_link_off': 'bond_off', 'pair_sync': 'bond_sync',
           'pair_search': 'bond_search', 'battery_full': 'battery_100'}
REMOVED = {'fingerprint', 'guardrail', 'hourglass', 'bolt', 'calendar', 'stopwatch', 'branch', 'model'}
CANONICAL = {v: k for k, v in ALIASES.items() if k != 'battery_full'}


def read_artwork():
    # The installed firmware entry point regenerates from its synchronized sheet.
    if (ROOT / 'approved-generator.json').is_file():
        from PIL import Image
        manifest = json.loads((ROOT / 'iconsheet.json').read_text())
        size = manifest.get('tileSize', manifest.get('tile_size', 32))
        if size != 32:
            raise ValueError('Expected 32px source tiles')
        step = size + manifest.get('spacing', 1)
        sheet = Image.open(ROOT / manifest.get('sheet', 'assets/iconsheet.png')).convert('RGB')
        result = {}
        for item in manifest['icons']:
            x, y = item['col'] * step, item['row'] * step
            if x < 0 or y < 0 or x + 32 > sheet.width or y + 32 > sheet.height:
                raise ValueError(f"Invalid tile bounds: {item['name']}")
            tile = sheet.crop((x, y, x+32, y+32))
            gray = tile.convert('L')
            bits = bytes(sum(1 << bit for bit in range(8) if gray.getpixel((xx+bit, yy)) > manifest.get('threshold', 128)) for yy in range(32) for xx in range(0, 32, 8))
            if not any(bits):
                continue  # Unfilled historical slots do not become blank firmware icons.
            png = io.BytesIO(); tile.save(png, format='PNG', optimize=True)
            result[ALIASES.get(item['name'], item['name'])] = {'png': png.getvalue(), 'bitmap': bits}
        return result
    cpp = (ROOT / 'icons_embedded.cpp').read_text()
    result = {}
    for m in ARRAY.finditer(cpp):
        result.setdefault(m[2], {})[m[3]] = bytes.fromhex(''.join(re.findall(r'0x([0-9a-fA-F]{2})', m[4])))
    if not result or any(set(v) != {'png', 'bitmap'} or len(v['bitmap']) != 128 for v in result.values()):
        raise ValueError('Invalid or incomplete approved artwork')
    return result


def c_array(name, kind, data):
    rows = ['  ' + ', '.join(f'0x{x:02X}' for x in data[i:i+16]) + ',' for i in range(0, len(data), 16)]
    return f'static const uint8_t PROGMEM icon_{name}_{kind}[] = {{\n' + '\n'.join(rows) + '\n};'


def guarded(body, guard):
    return f'#if {guard}\n{body}\n#endif  // {guard}\n' if guard else body + '\n'


def merge(source, artwork, metadata):
    registry = REGISTRY.search(source)
    if registry is None or 'ICON_PNG_FIELDS' not in source or 'ICON_BITMAP_FIELD' not in source:
        raise ValueError('Expected the current guarded System_Icons.cpp format; no files changed')
    if 'sizeof(EMBEDDED_ICONS)' not in source:
        raise ValueError('Expected dynamically computed registry count; no files changed')
    seen = set()
    def replace(m):
        name, kind = m[2], m[3]
        if name in REMOVED:
            return ''
        origin = ALIASES.get(name, name)
        if origin not in artwork:
            return m[0]
        seen.add((name, kind))
        return c_array(name, kind, artwork[origin][kind])
    result = ARRAY.sub(replace, source)
    for name in REMOVED:
        result = re.sub(r'^\s*\{"' + name + r'",[^\n]+\},\n', '', result, flags=re.M)
    existing = set(re.findall(r'\{"([a-z0-9_]+)"\s*,', registry[2]))
    arrays = {m[2] for m in ARRAY.finditer(source)}
    added, declarations, entries = [], [], []
    for origin, data in artwork.items():
        name = CANONICAL.get(origin, origin)
        if name in existing:
            if (name, 'png') not in seen or (name, 'bitmap') not in seen:
                raise ValueError(f'Incomplete existing icon: {name}; no files changed')
            continue
        if name in arrays:
            raise ValueError(f'Array without registry entry: {name}; no files changed')
        guard = metadata.get(name, metadata.get(origin, ''))
        payload = guarded(c_array(name, 'png', data['png']), 'ENABLE_HTTP_SERVER')
        payload += guarded(c_array(name, 'bitmap', data['bitmap']), 'ENABLE_OLED_DISPLAY')
        declarations.append(guarded(payload, guard))
        entries.append(guarded(f'  {{"{name}", ICON_PNG_FIELDS({name}), ICON_BITMAP_FIELD({name}), 32, 32}},', guard))
        added.append(name)
    # Both insertions remain inside the original rendering-surface guard.
    if added:
        registry = REGISTRY.search(result)
        result = result[:registry.start()] + '\n'.join(declarations) + result[registry.start():]
        result = REGISTRY.sub(lambda m: m[1] + m[2] + '\n' + ''.join(entries) + m[3], result, count=1)
    for name, kind in seen:
        if kind == 'png':
            size = len(artwork[ALIASES.get(name, name)]['png'])
            result = re.sub(r'// ' + re.escape(name) + r' PNG data \(\d+ bytes\)',
                            f'// {name} PNG data ({size} bytes)', result)
    return result, sorted({name for name, _ in seen}), added


def sync_generator_assets(project, artwork):
    """Merge by name and cell, retaining unknown artwork and all existing metadata."""
    from PIL import Image
    base = project / 'components/hardwareone/icons'
    manifest_path = base / 'iconsheet.json'
    if not manifest_path.is_file():
        return []
    manifest = json.loads(manifest_path.read_text())
    size = manifest.get('tileSize', manifest.get('tile_size', 32))
    if size != 32:
        raise ValueError('Firmware generator sheet must use 32px tiles')
    step = size + manifest.get('spacing', 1)
    cols = manifest.get('cols', 15)
    path = base / manifest.get('sheet', 'assets/iconsheet.png')
    old = Image.open(path).convert('RGB')
    icons = [dict(icon) for icon in manifest['icons'] if icon['name'] not in REMOVED]
    manifest['icons'] = icons
    old_tiles = {i['name']: old.crop((i['col'] * step, i['row'] * step, i['col'] * step + size, i['row'] * step + size)) for i in icons}
    used = {(i['row'], i['col']) for i in icons}
    names = {i['name'] for i in icons}
    for origin in artwork:
        name = CANONICAL.get(origin, origin)
        if name in names:
            continue
        cell = 0
        while divmod(cell, cols) in used:
            cell += 1
        row, col = divmod(cell, cols)
        icons.append({'name': name, 'row': row, 'col': col})
        used.add((row, col)); names.add(name)
    for index, icon in enumerate(icons):
        icon['row'], icon['col'] = divmod(index, cols)
    rows = max(i['row'] for i in icons) + 1
    sheet = Image.new('RGB', (cols * step + 1, rows * step + 1), 'black')
    for icon in icons:
        origin = ALIASES.get(icon['name'], icon['name'])
        if origin not in artwork:
            tile = old_tiles.get(icon['name'])
            if tile is not None:
                sheet.paste(tile, (icon['col'] * step, icon['row'] * step))
            continue
        bitmap = artwork[origin]['bitmap']
        tile = Image.new('RGB', (32, 32))
        tile.putdata([(255, 255, 255) if b & (1 << bit) else (0, 0, 0) for b in bitmap for bit in range(8)])
        sheet.paste(tile, (icon['col'] * step, icon['row'] * step))
    manifest['rows'] = rows
    manifest['cols'] = cols
    wrapper = ('#!/usr/bin/env python3\n'
               '# Approved artwork generator. Original entry point is backed up.\n'
               'import runpy, sys\nfrom pathlib import Path\n'
               'here = Path(__file__).resolve().parent\n'
               'if len(sys.argv) == 1: sys.argv.append(str(here.parents[3]))\n'
               'runpy.run_path(str(here / "integrate_approved_icons.py"), run_name="__main__")\n')
    scripts = base / 'scripts'
    if not scripts.is_dir():
        raise ValueError('Expected firmware icons/scripts directory')
    metadata = (ROOT / 'firmware-icons.json').read_bytes()
    return [(manifest_path, (json.dumps(manifest, indent=2) + '\n').encode()), (path, sheet),
            (base / 'firmware-icons.json', metadata),
            (base / 'approved-generator.json', b'{"source": "iconsheet.json"}\n'),
            (scripts / 'integrate_approved_icons.py', Path(__file__).read_bytes()),
            (scripts / 'generate_icons.py', wrapper.encode())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path, help='HardwareOne firmware root')
    parser.add_argument('--check', action='store_true', help='Preview without writing')
    parser.add_argument('--output', type=Path, help='Write a prepared C++ copy instead of installing')
    args = parser.parse_args()
    source = args.project / 'components/hardwareone/System_Icons.cpp'
    artwork = read_artwork()
    metadata = json.loads((ROOT / 'firmware-icons.json').read_text())['guards']
    result, updated, added = merge(source.read_text(), artwork, metadata)
    print(f'{len(updated)} existing icons refreshed; {len(added)} new icons registered')
    if args.check:
        return
    if args.output:
        args.output.write_text(result)
        print(f'Prepared {args.output}')
        return
    # Prepare all changes before writing; reject unsupported generator assets first.
    assets = sync_generator_assets(args.project, artwork)
    edits = [(source, result.encode())] + assets
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    for path, data in edits:
        if isinstance(data, bytes) and path.exists() and path.read_bytes() == data:
            continue
        backup = path.with_name(path.name + '.before-icons-' + stamp)
        if path.exists():
            shutil.copy2(path, backup)
        with tempfile.NamedTemporaryFile(dir=path.parent, suffix=path.suffix, delete=False) as f:
            temp = Path(f.name)
        try:
            if isinstance(data, bytes):
                temp.write_bytes(data)
            else:
                data.save(temp, format='PNG')
            if path.exists():
                shutil.copymode(path, temp)
            temp.replace(path)
        finally:
            temp.unlink(missing_ok=True)
        print(f'Updated {path}; backup: {backup.name}')
    print('Existing feature guards and lookup code retained. Menu wiring unchanged.')


if __name__ == '__main__':
    main()
