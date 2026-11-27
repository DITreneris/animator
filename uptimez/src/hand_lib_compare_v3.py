"""Hand library v3 against the canon's rows, in the canon's own comparison format (DITreneris/uptimez CANON.md,
"Changing a row", step 2: bp_hand_compare.py). Not a canon change: Tomas 27 Nov, the library goes to the canon only
after episode 15; this is the sheet that step will need, kept up to date.

Rows (the library's pose -> the canon row it would replace or add):
  CUP_GRIP        -> handle_grip  ("Handle (lamp, tool)": of_cast.handle_grip), a cup's handle
  RELAXED         -> quiet        (hands_ps "quiet", through hands_v4)
  SAUCER_SUPPORT  -> a NEW row    ("a flat thing on one palm": the canon has none)
Each sheet: old | new; male (17) and female (15); left and right hand; 100 %, 50 %, 25 %; the flat silhouette at
100 % and 25 %. Left and right by hands_lr (the canon's module, copied verbatim).

  python3 hand_lib_compare_v3.py   -> ../the-double-agent/compare_<row>_canon_vs_lib3.png
"""
import math
import os

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import kit
from kit import Ctx, INK
import hands_lr as lr
import hands_ps as hp
import hands_v4 as hv
import of_cast as oc
import hand_lib_v3 as hl
import hand_lib_sheet_v3 as hs

SKIN_M, SKIN_F = (0.96, 0.78, 0.66), (0.99, 0.86, 0.66)
K = 2.6                                                          # 100 %: 2.6 px per character unit (the cell holds it)
OUT = "../the-double-agent"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CELL = 300


def _w(sex):
    return (17 if sex == "male" else 15) * 1.15 * 1.25 * K      # the rig's hand size (kit.arm w x 1.15, hands_ps x 1.25)


def draw_cell(row, which, sex, arm, scale):
    """one hand, its forearm and its object, at scale (1, 0.5, 0.25), centred in a CELL x CELL tile."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, CELL, CELL)
    c = cairo.Context(s); k = Ctx(c, 0)
    c.translate(CELL / 2, CELL / 2); c.scale(scale, scale)
    w = _w(sex); skin = SKIN_M if sex == "male" else SKIN_F
    lr.reset_log(); lr.frame(cut=True)
    if row == "handle_grip":
        d = (-arm * math.sin(0.35), -math.cos(0.35))             # the forearm rising, leaning in
        x, y = -d[0] * 0.6 * w, -d[1] * 0.6 * w + 0.2 * w
        if which == "new":
            hs.forearm(k, x, y, math.atan2(d[1], d[0]), w, skin=skin)
            sd = lr.side(arm, d)
            ang = math.atan2(d[1], d[0])
            H = hl.to_screen("CUP_GRIP", x, y, ang, w, sd, hl.contact("CUP_GRIP", "handle"))
            Y1 = hl.to_screen("CUP_GRIP", x, y, ang, w, sd, (1.10, 1.06))
            bl = 1 if Y1[0] < H[0] else -1
            hl.draw_lr(k, "CUP_GRIP", x, y, d, w, skin, arm,
                       back_obj=lambda k_: hs.big_cup(k_, H[0], H[1], 1.1 * w / 26.0, bl, w))
        else:
            hx, hy = x + d[0] * 0.55 * w, y + d[1] * 0.55 * w
            hs.forearm(k, hx, hy, math.atan2(d[1], d[0]), w, skin=skin)       # the canon's fist sits on the handle: the arm ends there
            hs.big_cup(k, hx, hy, 1.1 * w / 26.0, 1 if arm > 0 else -1, w)
            oc.handle_grip(k, hx, hy, 0.62 * w, 0.0, skin)
    elif row == "quiet":
        d = (0.0, 1.0)
        x, y = 0, -0.6 * w
        hs.forearm(k, x, y, math.pi / 2, w, skin=skin)
        if which == "new":
            hl.draw_lr(k, "RELAXED", x, y, d, w, skin, arm)
        else:
            hp.draw(k, "quiet", x, y, w, skin, d, arm)
    else:                                                        # saucer_support
        x, y = arm * 0.7 * w, 0.1 * w
        if which == "new":
            hs.forearm(k, x, y, (0.0 if -arm > 0 else math.pi) - 0.45 * (-arm), w, skin=skin)
            Sp = hl.to_screen("SAUCER_SUPPORT", x, y, 0, w, -arm, hl.contact("SAUCER_SUPPORT", "saucer"))
            hl.draw_lr(k, "SAUCER_SUPPORT", x, y, (-arm, 0.0), w, skin, arm, reach=-arm,
                       obj=lambda k_: hs.saucer_at(k_, Sp[0], Sp[1], 0.95 * w / 30.0))
    s.flush()
    a = np.frombuffer(s.get_data(), np.uint8).reshape(CELL, CELL, 4).copy()
    rgb = a[:, :, [2, 1, 0]].astype(float); al = a[:, :, 3:4] / 255.0
    bg = np.array([247, 245, 237], float)
    col = (rgb + bg * (1 - al)).astype(np.uint8)                  # premultiplied ARGB over the cell colour
    sil = np.where(a[:, :, 3:4] > 40, 0, 255).repeat(3, axis=2).astype(np.uint8)
    return Image.fromarray(col), Image.fromarray(sil)


def sheet(row, label):
    f = ImageFont.truetype(FONT, 18)
    cols = [("old", "canon: %s" % ("of_cast.handle_grip" if row == "handle_grip" else "hands_ps quiet" if row == "quiet" else "none (no row)")),
            ("new", "library v3: %s" % label)]
    W_ = 2 * (8 * 160 + 40)
    img = Image.new("RGB", (W_, 2 * 230 + 120), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((20, 10), "%s: canon vs hand library v3 (male 17 / female 15, left | right, 100 / 50 / 25 %%, silhouette)" % row, fill=(0, 0, 0), font=f)
    for ci, (which, title) in enumerate(cols):
        x0 = 20 + ci * (8 * 160 + 40)
        d.text((x0, 44), title, fill=(0, 0, 0), font=f)
        for ri, sex in enumerate(("male", "female")):
            y0 = 80 + ri * 230
            d.text((x0, y0), sex, fill=(90, 90, 90), font=f)
            x = x0
            for arm in (-1, 1):
                for sc in (1.0, 0.5, 0.25):
                    if row == "saucer_support" and which == "old":
                        continue
                    col, sil = draw_cell(row, which, sex, arm, sc)
                    img.paste(col.resize((150, 150)), (x, y0 + 24)); x += 155
            if not (row == "saucer_support" and which == "old"):
                _, s1 = draw_cell(row, which, sex, 1, 1.0)
                _, s4 = draw_cell(row, which, sex, 1, 0.25)
                img.paste(s1.resize((110, 110)), (x0 + 6 * 155 + 4, y0 + 40))
                img.paste(s4.resize((110, 110)), (x0 + 6 * 155 + 120, y0 + 40))
            else:
                d.text((x0 + 20, y0 + 90), "the canon has no row for a flat thing on one palm", fill=(120, 0, 0), font=f)
    p = os.path.join(OUT, "compare_%s_canon_vs_lib3.png" % row)
    img.save(p)
    print("wrote", os.path.basename(p))


if __name__ == "__main__":
    lr.setup(); hv.enable()
    for row, label in (("handle_grip", "CUP_GRIP"), ("quiet", "RELAXED"), ("saucer_support", "SAUCER_SUPPORT")):
        sheet(row, label)
    print("hands_lr over the sheets:", "clean" if not lr.check() else lr.check())
