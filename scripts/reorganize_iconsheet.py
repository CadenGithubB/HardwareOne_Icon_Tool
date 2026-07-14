#!/usr/bin/env python3
"""
Reorganize the icon sheet into sorted category bands with growth gaps.

Source of truth = the firmware's own icon copy (105 icons, already has the
pair_* rename and the 18 icons the standalone tool was missing). We crop each
named tile out of that (black-on-white) sheet, INVERT it to the tool's
white-on-black convention, and re-place it into a fresh 15-column grid sorted
by category, leaving trailing gaps per band plus whole reserved rows for known
future categories. Firmware looks icons up by NAME, so grid position is free.

Tool-compat details (from index.html):
  * ICONS_PER_ROW = 15, step = tileSize+spacing = 33
  * import reads a tile at (col*33+1, row*33+1); foreground = bright (gray>128)
  * so: 1px grid border, icons drawn WHITE on BLACK at the +1 offset

Run:  python3 scripts/reorganize_iconsheet.py
Writes: assets/iconsheet.png + iconsheet.json  (true originals already at *.orig)
"""
import json, os, shutil, sys
from PIL import Image

TOOL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = "/Users/morgan/esp/hardwareone-idf/components/hardwareone/icons"
TILE, SPACING, COLS = 32, 1, 15
STEP = TILE + SPACING
BG, GRID, FG = (0, 0, 0), (51, 51, 51), (255, 255, 255)

# ---- Ordered category bands (real, drawn icons). Trailing cells = gaps. ------
BANDS = [
    ("Faces & status",        ["smiley", "frowny"]),
    ("Arrows & navigation",   ["arrow_up", "arrow_down", "arrow_left", "arrow_right",
                               "chevron_left", "chevron_right", "back", "home", "menu"]),
    ("Actions",               ["plus", "minus", "check", "close", "edit", "save", "trash",
                               "search", "refresh", "upload", "download", "settings"]),
    ("Alerts & help",         ["info", "warning", "help", "debug"]),
    ("Time & light",          ["clock", "sun", "moon"]),
    ("Files & storage",       ["file", "folder", "file_text", "file_code", "file_image",
                               "file_zip", "file_json", "file_pdf", "file_bin", "sdcard", "memory"]),
    ("Wi-Fi & signal",        ["wifi_off", "wifi_0", "wifi_1", "wifi_2", "wifi_3"]),
    ("Bluetooth",             ["bt_off", "bt_idle", "bt_advertising", "bt_connected"]),
    ("ESP-NOW pairing/link",  ["pair_link", "pair_link_off", "pair_sync", "pair_search"]),
    ("Battery & power",       ["battery_0", "battery_25", "battery_50", "battery_75",
                               "battery_100", "battery_full", "battery_charging", "power"]),
    ("Notifications",         ["notify_bell", "notify_espnow", "notify_server", "notify_automation",
                               "notify_sensor", "notify_logging", "notify_files", "notify_system",
                               "notify_cli", "notify_display"]),
    ("Connectivity & comms",  ["mqtt", "web", "radio"]),
    ("Sensors",               ["compass", "imu_axes", "thermal", "tof_radar", "presence", "rtc", "gesture"]),
    ("Devices & peripherals", ["device", "smartphone", "laptop", "watch", "smart_glasses",
                               "headphones", "gamepad", "camera", "led", "neopixel", "servo", "terminal"]),
    ("Audio & voice",         ["speaker", "vol_mute", "vol_min", "vol_max", "mic", "microphone", "espsr"]),
    ("AI / ML",               ["edgeimpulse"]),
    ("User & security",       ["user", "lock", "unlock"]),
]
# ---- Whole reserved rows for known future categories (labels for the legend). -
RESERVED = [
    ("ESP-NOW bonding",       "row 17"),
    ("Maps & navigation",     "row 18"),
    ("Automation & triggers", "row 19"),
    ("Notifications (more)",  "row 20"),
    ("Future / spare",        "row 21"),
]

# ---- Backlog: planned/missing icons seeded as NAMED BLANK slots (no art yet).
#      Each lands in a real empty cell (category-row gap or a reserved row) so
#      it's selectable & drawable in the tool and survives export. (name, row, col)
SEEDS = [
    ("logo", 0, 2),                                                    # branding (renders blank today)
    ("text", 2, 12), ("animation", 2, 13),                            # UI modes (blank today)
    ("wifi", 6, 5), ("signal", 6, 6),                                 # base wifi + peer RSSI bars
    ("pair_beacon", 8, 4),                                            # pairing window broadcasting
    ("notify_auth", 10, 10), ("notify_power", 10, 11), ("notify_voice", 10, 12),
    ("notify_camera", 10, 13), ("notify_bluetooth", 10, 14),         # new notification categories
    ("gps", 12, 7), ("sensor", 12, 8),                               # GPS fix + generic sensor (blank today)
    ("ring", 13, 12), ("rotary_encoder", 13, 13), ("video", 13, 14), # R1 ring, ANO encoder, video capture
    ("llm", 15, 1), ("model", 15, 2), ("guardrail", 15, 3),          # on-device LLM / model / topic gate
    ("password", 16, 3), ("key", 16, 4), ("shield", 16, 5), ("fingerprint", 16, 6),  # auth (password blank today)
    ("bond", 17, 0), ("bond_master", 17, 1), ("bond_worker", 17, 2),
    ("mesh_nodes", 17, 3), ("mesh_master", 17, 4),                   # bonding + mesh topology
    ("map", 18, 0), ("map_pin", 18, 1), ("route", 18, 2), ("layers", 18, 3),
    ("zoom_in", 18, 4), ("zoom_out", 18, 5), ("recenter", 18, 6),    # maps + controls
    ("bolt", 19, 0), ("branch", 19, 1), ("calendar", 19, 2),
    ("hourglass", 19, 3), ("stopwatch", 19, 4),                      # automation triggers/conditions
    ("notify_network", 20, 0), ("notify_mqtt", 20, 1),
    ("notify_storage", 20, 2), ("notify_time", 20, 3),               # more notification categories
]

def main():
    sj = json.load(open(os.path.join(SRC_DIR, "iconsheet.json")))
    src = Image.open(os.path.join(SRC_DIR, sj["sheet"])).convert("RGB")
    sts, ssp = sj["tileSize"], sj["spacing"]
    pos = {ic["name"]: (ic["row"], ic["col"]) for ic in sj["icons"]}

    placed = [n for _, names in BANDS for n in names]
    dupes = sorted({n for n in placed if placed.count(n) > 1})
    miss, extra = sorted(set(pos) - set(placed)), sorted(set(placed) - set(pos))
    if dupes or miss or extra:
        sys.exit(f"VALIDATION FAILED\n dupes={dupes}\n in-source-not-placed={miss}\n placed-not-in-source={extra}")

    rows = len(BANDS) + len(RESERVED)
    W, H = COLS * STEP + 1, rows * STEP + 1
    out = Image.new("RGB", (W, H), BG)
    px = out.load()
    # Spacing/grid lines sit on the 1px gap AFTER each tile (col*STEP+TILE), so
    # tiles stay flush at offset 0 — matching generate_icons.py / export_*.py,
    # which crop at (col*STEP, row*STEP). Consumers ignore the spacing pixel.
    for c in range(COLS):                           # vertical spacing lines
        for y in range(H): px[c * STEP + TILE, y] = GRID
    for r in range(rows):                           # horizontal spacing lines
        for x in range(W): px[x, r * STEP + TILE] = GRID

    out_icons, legend = [], []
    for r, (label, names) in enumerate(BANDS):
        for c, name in enumerate(names):
            sr, sc = pos[name]
            tile = src.crop((sc * (sts + ssp), sr * (sts + ssp),
                             sc * (sts + ssp) + sts, sr * (sts + ssp) + sts))
            ox, oy = c * STEP, r * STEP             # tiles flush at offset 0
            for yy in range(TILE):                  # INVERT: dark source -> white fg
                for xx in range(TILE):
                    rr, gg, bb = tile.getpixel((xx, yy))
                    if 0.299 * rr + 0.587 * gg + 0.114 * bb <= 128:
                        px[ox + xx, oy + yy] = FG
            out_icons.append({"name": name, "row": r, "col": c})

    # ---- place backlog seeds as NAMED BLANK slots (JSON entries only, no art) --
    real_cells = {(ic["row"], ic["col"]) for ic in out_icons}
    real_names = {ic["name"] for ic in out_icons}
    seen_cells, seen_names, seeds_per_row = set(), set(), {}
    for name, r, c in SEEDS:
        if r >= rows or c >= COLS:            sys.exit(f"SEED OUT OF GRID: {name} at {r},{c}")
        if (r, c) in real_cells | seen_cells: sys.exit(f"SEED CELL COLLISION: {name} at {r},{c}")
        if name in real_names | seen_names:   sys.exit(f"SEED DUP NAME: {name}")
        seen_cells.add((r, c)); seen_names.add(name)
        seeds_per_row[r] = seeds_per_row.get(r, 0) + 1
        out_icons.append({"name": name, "row": r, "col": c})
    out_icons.sort(key=lambda ic: (ic["row"], ic["col"]))

    for r, (label, names) in enumerate(BANDS):
        s = seeds_per_row.get(r, 0)
        legend.append(f"  row {r:2d}  {label:<24} {len(names):2d} icons"
                      + (f" + {s} seeded" if s else "") + f", {COLS-len(names)-s:2d} free")
    for k, (label, _) in enumerate(RESERVED):
        r = len(BANDS) + k
        s = seeds_per_row.get(r, 0)
        legend.append(f"  row {r:2d}  {label:<24} RESERVED"
                      + (f" + {s} seeded" if s else " (empty)") + f", {COLS-s:2d} free")

    png, jsn = os.path.join(TOOL, "assets", "iconsheet.png"), os.path.join(TOOL, "iconsheet.json")
    for p in (png, jsn):
        if os.path.exists(p) and not os.path.exists(p + ".orig"):
            shutil.copy2(p, p + ".orig")
    out.save(png)
    json.dump({"tileSize": TILE, "spacing": SPACING, "threshold": 128,
               "sheet": "assets/iconsheet.png", "cols": COLS, "rows": rows,
               "icons": out_icons},
              open(jsn, "w"), indent=2)
    print(f"OK  {len(out_icons)} entries = {len(out_icons)-len(SEEDS)} drawn + {len(SEEDS)} seeded blanks, "
          f"{COLS}x{rows} grid, {W}x{H}px\n" + "\n".join(legend))

if __name__ == "__main__":
    main()
