"""Old vs new for one row of the hand class sheet. Tomas picks; a tie keeps old.

Left column: the accepted drawing. Right column: the attempt. Each column
shows male and female at 100 %, 50 % and 25 % of the sheet, and the
silhouette (the hand filled flat, no inside lines) at 100 % and 25 %.

  python3 bp_hand_compare.py phone_grip          # accepted vs its candidate
  python3 bp_hand_compare.py grab v2 v3          # any two versions
"""
import os
import sys

import cairo
from PIL import Image, ImageDraw, ImageFont

import bp_hand_sheet_v2 as v2
import bp_hand_sheet_v4 as v4
import kit

CELL = (0.97, 0.96, 0.93)
PAD = 24
TITLE_H = 70
CAPTION_H = 34
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def _font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT, size)
    except OSError:
        return ImageFont.load_default()


def _spots(job):
    if job == "phone_grip":
        return (0.27, 0.73), 0.74
    if job == "point_t":
        return (0.30, 0.74), 0.34
    return (0.30, 0.74), 0.56


def _cell(job, drawer, w, skin):
    """One cell, left and right hand, no labels, at the sheet's device scale."""
    h = v2._row_h(job)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, v2.COL_W * 2, h * 2)
    surf.set_device_scale(2, 2)
    c = cairo.Context(surf)
    k = kit.Ctx(c, 0)
    c.set_source_rgb(*CELL)
    c.paint()
    (fl, fr), fy = _spots(job)
    for frac, arm in ((fl, -1), (fr, 1)):
        c.save()
        c.new_path()
        drawer(k, v2.COL_W * frac, h * fy, w, skin, arm) if job == "phone_grip" else drawer(
            c, v2.COL_W * frac, h * fy, w, skin, arm
        )
        c.restore()
    data = bytes(surf.get_data())
    img = Image.frombuffer("RGBA", (surf.get_width(), surf.get_height()), data, "raw", "BGRA", 0, 1)
    return img.convert("RGB")


def _silhouette(img):
    bg = tuple(int(round(v * 255)) for v in CELL)
    out = Image.new("L", img.size, 255)
    src = img.load()
    dst = out.load()
    for yy in range(img.size[1]):
        for xx in range(img.size[0]):
            r, g, b = src[xx, yy]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > 24:
                dst[xx, yy] = 0
    return out.convert("RGB")


def _scale(img, f):
    return img.resize((max(1, int(img.size[0] * f)), max(1, int(img.size[1] * f))), Image.LANCZOS)


def _column(job, drawer):
    male = _cell(job, drawer, v2.MALE_W, v2.MALE_SKIN)
    female = _cell(job, drawer, v2.FEMALE_W, v2.FEMALE_SKIN)
    sil_m = _silhouette(male)
    sil_f = _silhouette(female)
    cw, ch = male.size
    blocks = [
        ("male 100 %", [male]),
        ("female 100 %", [female]),
        ("male and female 50 %", [_scale(male, 0.5), _scale(female, 0.5)]),
        ("25 %: male, female, then their silhouettes", [_scale(i, 0.25) for i in (male, female, sil_m, sil_f)]),
        ("silhouette, male 100 %", [sil_m]),
    ]
    height = sum(CAPTION_H + max(i.size[1] for i in imgs) + PAD for _cap, imgs in blocks)
    col = Image.new("RGB", (cw, height), (255, 255, 255))
    draw = ImageDraw.Draw(col)
    y = 0
    for cap, imgs in blocks:
        draw.text((4, y + 6), cap, fill=(40, 30, 25), font=_font(20))
        y += CAPTION_H
        x = 0
        for i in imgs:
            col.paste(i, (x, y))
            x += i.size[0] + 8
        y += max(i.size[1] for i in imgs) + PAD
    return col


def compare(job, old, new):
    a = _column(job, v4.DRAWERS[(job, old)])
    b = _column(job, v4.DRAWERS[(job, new)])
    width = a.size[0] + b.size[0] + PAD * 3
    height = TITLE_H + max(a.size[1], b.size[1]) + PAD
    sheet = Image.new("RGB", (width, height), (236, 230, 218))
    draw = ImageDraw.Draw(sheet)
    draw.text((PAD, 16), "%s: old %s" % (job, old), fill=(40, 30, 25), font=_font(30, True))
    draw.text((PAD * 2 + a.size[0], 16), "new %s" % new, fill=(40, 30, 25), font=_font(30, True))
    sheet.paste(a, (PAD, TITLE_H))
    sheet.paste(b, (PAD * 2 + a.size[0], TITLE_H))
    out = os.path.join(v4.PICS, "compare_%s_%s_vs_%s.png" % (job, old, new))
    sheet.save(out)
    return out


if __name__ == "__main__":
    row = sys.argv[1]
    if len(sys.argv) >= 4:
        old_v, new_v = sys.argv[2], sys.argv[3]
    else:
        old_v, new_v = v4.ACCEPTED[row], v4.CANDIDATES[row]
    print(compare(row, old_v, new_v))
