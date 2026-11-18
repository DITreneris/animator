"""OFFICE NOIR 2: contact sheets of the animation for the cold mute test (gate G4). 18 Nov.
Draws the frames of on2_motion (the current cut) with no captions, no bubbles and no sound, and lays them out as numbered
tiles with a time on each. on2_motion itself is not changed: its caption and bubble functions are switched off here.
  - the film at 4 frames a second, 21 tiles (7 x 3) a sheet, tiles 270 px wide: what a phone shows;
  - four quick moments drawing by drawing (12 a second), because a grid at 4 a second misses an impact:
    the coin, the stamp, the dive under the desk, the pop.
Writes PNG sheets into the folder given (default /tmp/cartoon) under names that say nothing about the film:
sheet_01.png ..., detail_A.png ... D.  python3 on2_mute_anim.py [--with-text] [folder]"""
import math
import os
import sys
import cairo

import on2_motion as m

if "--with-text" not in sys.argv:                           # 18 Nov: --with-text keeps the lines on screen (a pacing test)
    m.caption = lambda *a, **kw: None                       # mute: no narration line,
    m.b5.bubble = lambda *a, **kw: None                     # no bubbles,
    m.b68.say = lambda *a, **kw: None                       # no cards
else:
    sys.argv.remove("--with-text")

TW, TH, LAB = 270, 480, 26
COLS, ROWS = 7, 3
DETAILS = [("A", "4.1a", range(3, 13)), ("B", "5.10", range(5, 14)), ("C", "6.7", range(0, 8)), ("D", "7.3", range(0, 9))]


def tile(c, x, y, surf, label):
    c.save(); c.translate(x, y + LAB); c.scale(TW / 540.0, TW / 540.0); c.set_source_surface(surf, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(17)
    c.move_to(x + 6, y + 19); c.show_text(label)


def sheet(tiles, out, cols=COLS):
    rows = (len(tiles) + cols - 1) // cols
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * TW, rows * (TH + LAB)); c = cairo.Context(S)
    c.set_source_rgb(0.07, 0.07, 0.08); c.paint()
    for i, (surf, label) in enumerate(tiles):
        tile(c, (i % cols) * TW, (i // cols) * (TH + LAB), surf, label)
    S.write_to_png(out)


def main(folder="/tmp/cartoon"):
    os.makedirs(folder, exist_ok=True)
    rows, total = m.timing("A2")
    n = int(math.floor(total * 4 - 1e-6)) + 1
    tiles = []
    for i in range(n):
        t = i / 4.0
        row = [r for r in rows if r["start"] <= t + 1e-6 < r["start"] + r["len"]][0]
        tiles.append((m.frame(row, t - row["start"], t), "%d   %d:%05.2f" % (i + 1, int(t // 60), t % 60)))
    per = COLS * ROWS
    names = []
    for j in range(0, len(tiles), per):
        out = "%s/sheet_%02d.png" % (folder, j // per + 1)
        sheet(tiles[j:j + per], out); names.append(out)
    for letter, shot, drawings in DETAILS:
        row = [r for r in rows if r["shot"] == shot][0]
        dt = []
        for d in drawings:
            if d / 12.0 >= row["len"]:
                break
            t = row["start"] + d / 12.0
            dt.append((m.frame(row, d / 12.0, t), "%s%d   %d:%05.2f" % (letter, d - drawings[0] + 1, int(t // 60), t % 60)))
        out = "%s/detail_%s.png" % (folder, letter)
        sheet(dt, out, cols=len(dt)); names.append(out)
    return names, n, total


if __name__ == "__main__":
    names, n, total = main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/cartoon")
    print("%d tiles, %.2f s, %d sheets" % (n, total, len(names)))
