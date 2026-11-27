"""The Blueprint. One scene file.

Phase 1 shot list lives in the-blueprint/the-blueprint-shot-list-v1.md and is not overwritten.
This file repeats those durations, generates the script, and renders the opt-in 16:9 stills,
the night and final layouts, five motion tests, and rough cut v1. kit.py and fs_set4.py are not edited.

Rough-cut budget is 5. Version 1 is the old room and is not rewritten.
Version 2 writes bp_rough_v2.mp4 and the no-night cut. It does not rewrite the script.
Version 3 adds the Client's two walks. It does not rewrite version 1 or version 2.
Version 4 adds the word crops. It does not rewrite version 1, version 2, or version 3.
Version 5 adds the cannon, the one star, and the mute week. It does not rewrite versions 1 to 4.
"""
import json
import math
import os
import subprocess
import sys

import cairo

import bp_frame as fr
import kit

FPS = 30
ROUGH_BUDGET = 5
VERSION = 1
# x264 does not write these into the file from -color_primaries alone. The checker reads them.
_BSF = ["-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
EP = os.path.join(ROOT, "the-blueprint")
SRC = os.path.dirname(__file__)

# Paper cut. Durations sum to 400 s. id 05 is the night scene.
SHOTS = [
    {"id": "01", "dur": 18, "cam": "S0", "hide": True, "grade": 1.0,
     "title": "The frame drops", "line": "", "take": "", "motion": "frame"},
    {"id": "02", "dur": 32, "cam": "PUSH", "hide": True, "grade": 1.0,
     "title": "The pearl", "line": "Does your missus love your garages?",
     "take": "ob_voices/film 3.2", "motion": ""},
    {"id": "03", "dur": 30, "cam": "SHRED", "hide": True, "grade": 1.0,
     "title": "He shreds it while looking at her", "line": "We'll take care of it.",
     "take": "ob_voices/film 4.3", "motion": "shred"},
    {"id": "04", "dur": 20, "cam": "S0", "hide": True, "grade": 1.0,
     "title": "Cannon", "line": "ONBOARDING COMPLETE.",
     "take": "ob_voices/film 10.4", "motion": ""},
    {"id": "05", "dur": 40, "cam": "NIGHT", "hide": True, "grade": 0.55,
     "title": "Night. She will not draw a bay", "line": "I won't draw one.",
     "take": "NEW", "motion": ""},
    {"id": "06", "dur": 30, "cam": "S0", "hide": False, "grade": 1.0,
     "title": "Friday, the bank", "line": "Garage eleven. Guaranteed by Friday.",
     "take": "fs_voices/film_v13 2.2", "motion": ""},
    {"id": "07", "dur": 35, "cam": "PUSH", "hide": False, "grade": 1.0,
     "title": "Make the zero green", "line": "Can you make the zero green?",
     "take": "fs_voices/film_v13 4.1", "motion": ""},
    {"id": "08", "dur": 30, "cam": "COUNTER", "hide": False, "grade": 1.0,
     "title": "The week, mute", "line": "", "take": "", "motion": ""},
    {"id": "09", "dur": 30, "cam": "S0", "hide": False, "grade": 1.0,
     "title": "Where is his blueprint?", "line": "Ask the machine.",
     "take": "fs_voices/film_v13 x2", "motion": ""},
    {"id": "10", "dur": 20, "cam": "COUNTER", "hide": False, "grade": 1.0,
     "title": "The post", "line": "Stupid human.",
     "take": "cs_voices/film_v9 1.4b", "motion": ""},
    {"id": "11", "dur": 50, "cam": "PUSH", "hide": False, "grade": 1.0,
     "title": "Check your pocket", "line": "Check your pocket.",
     "take": "cs_voices/film_v9 4.2p", "motion": "pocket"},
    {"id": "12", "dur": 40, "cam": "S0", "hide": False, "grade": 1.0,
     "title": "Still one star", "line": "Still one star.",
     "take": "cs_voices/film_v9 6.5", "motion": ""},
    {"id": "13", "dur": 25, "cam": "S0", "hide": False, "grade": 1.0,
     "title": "The stamp", "line": "", "take": "", "motion": "stamp"},
]

CAM = {"S0": fr.S0, "SHRED": fr.SHRED, "COUNTER": fr.COUNTER, "PUSH": fr.PUSH, "NIGHT": fr.NIGHT,
       "ZERO": fr.ZERO, "STAMP": fr.STAMP, "PLAN": fr.PLAN}

# Motion marks, in world points of the locked room. They hang off the props and homes in bp_set,
# so a mark cannot drift back to the 9:16 floor (y about 800). bp_draw_audit reads these.
import bp_set as _room

_sx, _sf, _ss = _room.SHRED_AT
SHRED_SLOT = (_sx + 5, _sf - 123 * _ss)          # top of the bin's slot
SHEET_FROM = (SHRED_SLOT[0], SHRED_SLOT[1] - 18)  # sheet resting on the slot
SHEET_TO = (SHRED_SLOT[0], SHRED_SLOT[1] + 5)     # sheet gone in
POCKET_FROM = (_room.CLIENT[0] + 30, _room.CLIENT[1] - 146)
POCKET_TO = (_room.PAM[0] + 62, _room.PAM[1] - 128)
# Control of the arc. The slip at halfway sits above Don's head, not on his face.
# The control itself is above the PUSH frame. The drawn point at t=0.5 is inside it.
POCKET_BEND = (459, 150)
# In front of the wheel, below the body. The head and the HR badge stay clear.
STAMP_PAGE = (_room.ROBOT[0] - 8, _room.ROBOT[1] + 28)
STAMP_DROP = 228                                  # the stamp starts this far above the page
# Shot 04 hold. The shredder's right edge is about x 581. The desk starts at x 658.
# Feet stay on Don's floor. The scale is the shredder's. The muzzle points up-left, at the bin.
CANNON_AT = (619, _room.SHRED_AT[1], 0.72)

INHERIT = {
    "ob_voices/film": ["3.1", "3.2", "3.3", "3.7", "3.12", "4.1", "4.3", "5.4", "5.5", "8.1", "8.3", "10.4"],
    "ob_voices/film_v10": ["9.1"],
    "fs_voices/film_v13": ["1.2", "2.2", "3.3", "4.1", "4.2", "4.3", "5.2", "7.1", "x1", "x2", "x3", "t1", "t2"],
    "cs_voices/film_v9": ["1.2", "1.4r", "1.4d", "1.4b", "3.5", "4.2p", "4.4", "5.1", "5.4d", "6.3p", "6.5"],
}
NEW = [
    ("SOFIA", "Put recovered on it."),
    ("PAM", "Recovered from what?"),
    ("SOFIA", "He needs a page by Friday."),
    ("PAM", "He needs the bays."),
    ("SOFIA", "I won't draw one."),
    ("PAM", "I'm matching them."),
]


def total(shots=None):
    shots = SHOTS if shots is None else shots
    return sum(s["dur"] for s in shots)


def without_night():
    return [s for s in SHOTS if s["id"] != "05"]


assert total() == 400, total()
assert total(without_night()) == 360


def _load(rel):
    with open(os.path.join(SRC, rel, "takes.json"), encoding="utf-8") as f:
        return json.load(f)


def check_takes():
    faults = []
    for rel, keys in INHERIT.items():
        data = _load(rel)
        for key in keys:
            if key not in data:
                faults.append("%s missing %s" % (rel, key))
    film = _load("ob_voices/film")
    if "9.1" in film:
        faults.append("ob_voices/film now has 9.1; the ledger says it does not")
    return faults


def write_script(path=None):
    path = path or os.path.join(EP, "the-blueprint-script-v1.md")
    lines = [
        "<!-- GENERATED by src/bp_scenes.py from SHOTS. Edit the shot list and this file's source, not this file. -->",
        "",
        "# The Blueprint — script v1",
        "",
        "400 s. 1920×1080. Generated from the phase-1 paper cut.",
        "",
    ]
    t = 0
    for s in SHOTS:
        lines.append("## %s  %d:%02d  %ds  %s" % (s["id"], t // 60, t % 60, s["dur"], s["title"]))
        lines.append("")
        if s["line"]:
            lines.append(s["line"])
            lines.append("")
            lines.append("Take: %s" % (s["take"] or "silent"))
        else:
            lines.append("Silent.")
        lines.append("")
        t += s["dur"]
    lines.append("## Night lines, no takes yet")
    lines.append("")
    for who, text in NEW:
        lines.append("- %s: %s" % (who, text))
    lines.append("")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def _paper(c, x, y, w, h, ang=0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.set_source_rgb(0.97, 0.96, 0.93)
    c.rectangle(-w / 2, -h / 2, w, h)
    c.fill()
    c.set_source_rgb(0.15, 0.12, 0.1)
    c.set_line_width(1.2)
    c.rectangle(-w / 2, -h / 2, w, h)
    c.stroke()
    c.restore()


def overlay_still(which):
    def draw(c):
        if which == "shred":
            shred_sheet(c, 0.15)
        elif which == "finger":
            finger(c, 1.0)
        elif which == "pocket":
            pocket(c, 1.0)
        elif which == "counter":
            c.set_source_rgba(0.12, 0.10, 0.08, 0.85)
            c.arc(POCKET_TO[0], POCKET_TO[1], 14, 0, 6.3)
            c.fill()
        elif which == "stamp":
            stamp(c, 1.0)
        elif which == "frame":
            frame_fall(c, 1.0)
    return draw


def frame_fall(c, t):
    y = 250 + (392 - 250) * t
    c.save()
    c.translate(440, y)
    c.rotate(0.08 * (1 - t))
    c.set_source_rgb(0.25, 0.18, 0.12)
    c.rectangle(-46, -62, 92, 118)
    c.fill()
    c.set_source_rgb(0.72, 0.78, 0.55)
    c.rectangle(-36, -48, 72, 88)
    c.fill()
    c.restore()


def shred_sheet(c, t):
    # t=0 sits on the slot; t=1 has gone in.
    x, y0 = SHEET_FROM
    y = y0 + (SHEET_TO[1] - y0) * t
    _paper(c, x, y, 28, 36, -0.04)


def finger(c, t):
    # Pam's raised finger. Pam is outside SHRED, so this shot draws none.
    # A finger with no arm would be a stray on the bin.
    return


def _arc(t, a, b, bend):
    u = 1.0 - t
    x = u * u * a[0] + 2 * u * t * bend[0] + t * t * b[0]
    y = u * u * a[1] + 2 * u * t * bend[1] + t * t * b[1]
    return x, y


def pocket(c, t):
    x, y = _arc(t, POCKET_FROM, POCKET_TO, POCKET_BEND)
    _paper(c, x, y, 22, 14, 0.35 * (1 - t))


def cannon_overlay(c):
    """The celebration, on the hold. Default off: only an insert calls this. The label is restored after."""
    import set_ob
    x, floor, s = CANNON_AT
    k = kit.Ctx(c, 0)
    prev = set_ob.CANNON_LABEL[0]
    set_ob.CANNON_LABEL[0] = True
    try:
        set_ob.cannon(k, x, floor, s, fuse=0.0)
    finally:
        set_ob.CANNON_LABEL[0] = prev


def _star(c, x, y, r, fill):
    """The mark from cs_scene6.star. One gold star, or an empty one."""
    c.new_path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        (c.move_to if i == 0 else c.line_to)(x + math.cos(a) * rr, y + math.sin(a) * rr)
    c.close_path()
    if fill:
        c.set_source_rgb(0.98, 0.78, 0.10)
        c.fill_preserve()
        c.set_source_rgb(*kit.INK)
    else:
        c.set_source_rgb(0.72, 0.74, 0.78)
    c.set_line_width(max(1.2, r * 0.12))
    c.stroke()


def star_overlay(c):
    """Sofía's phone, in front of her body. Her head stays above it. The poster is not in this drawing."""
    # Between the robot and Don. Top is below her head (feet 458, head about 388).
    x, y, w, h = 360, 470, 108, 120
    c.save()
    c.translate(x, y)
    c.rotate(-0.06)
    c.set_source_rgb(0.16, 0.17, 0.20)
    c.rectangle(-w / 2, -h / 2, w, h)
    c.fill()
    c.set_source_rgb(0.94, 0.95, 0.96)
    c.rectangle(-w / 2 + 8, -h / 2 + 14, w - 16, h - 26)
    c.fill()
    c.set_source_rgb(0.30, 0.32, 0.38)
    c.rectangle(-16, -h / 2 + 4, 32, 5)
    c.fill()
    _star(c, 0, -16, 18, True)
    for i in range(4):
        _star(c, -36 + i * 24, 22, 8, False)
    c.set_source_rgb(*kit.INK)
    c.select_font_face("Inter", 0, 1)
    c.set_font_size(16)
    word = "1/5"
    ext = c.text_extents(word)
    c.move_to(-ext.x_advance / 2, 46)
    c.show_text(word)
    c.restore()


def _week_plate(c, w, h):
    c.save()
    c.translate(WEEK_AT[0], WEEK_AT[1])
    c.set_source_rgb(0.12, 0.12, 0.14)
    c.rectangle(-w / 2 - 6, -h / 2 - 6, w + 12, h + 12)
    c.fill()
    c.set_source_rgb(0.98, 0.97, 0.94)
    c.rectangle(-w / 2, -h / 2, w, h)
    c.fill()


def _week_text(c, text, y, size, col):
    c.select_font_face("Inter", 0, 1)
    c.set_font_size(size)
    ext = c.text_extents(text)
    c.move_to(-ext.x_advance / 2, y)
    c.set_source_rgb(*col)
    c.show_text(text)


def retry_overlay(c):
    """0 RESULTS, then RETRY UNTIL FRIDAY. The colours are the retry screen in fs_film35."""
    _week_plate(c, 280, 78)
    _week_text(c, "0 RESULTS", -10, 22, (0.18, 0.55, 0.32))
    c.set_source_rgb(0.10, 0.12, 0.18)
    c.rectangle(-128, 6, 256, 28)
    c.fill()
    _week_text(c, "RETRY UNTIL FRIDAY", 26, 16, (1.0, 0.86, 0.30))
    c.restore()


def _lipstick(c, x, y):
    """Pam's lipstick from fs_film35.lipstick. The tip is at (x, y)."""
    c.save()
    c.translate(x, y)
    c.rotate(0.4)
    c.scale(0.62, 0.62)
    c.set_source_rgb(*kit.INK)
    c.rectangle(-8, 6, 16, 44)
    c.fill()
    c.set_source_rgb(0.85, 0.72, 0.30)
    c.rectangle(-6, 16, 12, 32)
    c.fill()
    c.set_source_rgb(0.20, 0.20, 0.24)
    c.rectangle(-6, 8, 12, 9)
    c.fill()
    c.new_path()
    c.move_to(-5, 8)
    c.line_to(-5, -4)
    c.line_to(0, -9)
    c.line_to(5, -2)
    c.line_to(5, 8)
    c.close_path()
    c.set_source_rgb(0.80, 0.10, 0.30)
    c.fill_preserve()
    c.set_source_rgb(*kit.INK)
    c.set_line_width(1.4)
    c.stroke()
    c.restore()


def _lipstick_word(c, x, y, size):
    """STUPID, from fs_film35.lipstick_word. All six letters."""
    c.select_font_face("Lilita One", 0, 0)
    c.set_font_size(size)
    word = "STUPID"
    wd = [c.text_extents(ch).x_advance for ch in word]
    x0 = x - sum(wd) / 2
    lip = (0.80, 0.10, 0.30)
    for i, ch in enumerate(word):
        c.save()
        c.translate(x0 + sum(wd[:i]), y + (3, -4, 2, -2, 4, -3)[i] * size / 34)
        c.rotate((-0.10, 0.06, -0.04, 0.09, -0.07, 0.05)[i])
        c.move_to(0, 0)
        c.text_path(ch)
        c.set_source_rgb(*lip)
        c.fill_preserve()
        c.set_line_width(size * 0.07)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke()
        c.restore()
    c.set_source_rgba(lip[0], lip[1], lip[2], 0.75)
    c.set_line_width(size * 0.14)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.new_path()
    c.move_to(x0 + 4, y + size * 0.30)
    c.curve_to(x, y + size * 0.42, x + 20, y + size * 0.22, x0 + sum(wd) - 2, y + size * 0.34)
    c.stroke()


def lipstick_overlay(c):
    """The word, on a sheet. The robot is outside COUNTER, so it is not on his back."""
    _week_plate(c, 300, 78)
    _lipstick(c, -112, 4)
    _lipstick_word(c, 22, 6, 26)
    c.restore()


def _cal_page(c, day, num):
    """One tear-off page. The drawing is fs_film35.calendar's page, without the breath."""
    red = (0.86, 0.15, 0.16)
    c.set_source_rgb(0.99, 0.99, 0.97)
    c.rectangle(-30, -34, 60, 68)
    c.fill()
    c.set_source_rgb(*red)
    c.rectangle(-30, -34, 60, 12)
    c.fill()
    c.set_source_rgb(*kit.INK)
    c.set_line_width(1.6)
    c.rectangle(-30, -34, 60, 68)
    c.stroke()
    for i in range(4):
        c.new_path()
        c.arc(-21 + i * 14, -34, 2.6, math.pi, 2 * math.pi)
        c.set_line_width(1.4)
        c.stroke()
    c.select_font_face("Inter", 0, 1)
    d3 = day[:3]
    c.set_font_size(24)
    ext = c.text_extents(d3)
    fit = min(1.0, 54.0 / ext.width)
    c.save()
    c.scale(fit, 1.0)
    c.set_source_rgb(*red)
    c.move_to(-ext.x_bearing - ext.width / 2, 7)
    c.show_text(d3)
    c.restore()
    c.set_font_size(19)
    ext = c.text_extents(str(num))
    c.set_source_rgb(*kit.INK)
    c.move_to(-ext.x_bearing - ext.width / 2, 29)
    c.show_text(str(num))


def calendar_overlay(c):
    """MON 1 and THU 4, side by side, both whole. The shot list stops at Thursday."""
    for dx, day, num, tilt in ((-78, "MON", 1, 0.18), (78, "THU", 4, -0.04)):
        c.save()
        c.translate(WEEK_AT[0] + dx, WEEK_AT[1] + 6)
        c.rotate(tilt)
        c.scale(1.05, 1.05)
        if day == "THU":
            c.set_source_rgb(*kit.INK)
            c.arc(0, -40, 2.4, 0, 2 * math.pi)
            c.fill()
        _cal_page(c, day, num)
        c.restore()


def deleted_overlay(c):
    """One message, struck out. First Search has no separate drawing for this card."""
    _week_plate(c, 280, 78)
    c.set_source_rgb(0.55, 0.56, 0.58)
    c.rectangle(-96, -22, 192, 12)
    c.fill()
    c.set_source_rgb(0.75, 0.16, 0.18)
    c.set_line_width(3)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(-100, -16)
    c.line_to(100, -16)
    c.stroke()
    _week_text(c, "DELETED", 24, 22, kit.INK)
    c.restore()


def stamp(c, t):
    # The page is in front of the robot. The stamp comes down onto it.
    page_x, page_y = STAMP_PAGE
    _paper(c, page_x, page_y, 52, 66, 0.03)
    top = page_y - STAMP_DROP
    y = top + (page_y - top) * min(1.0, t * 1.15)
    c.save()
    c.translate(page_x, y)
    c.set_source_rgb(0.75, 0.12, 0.14)
    c.rectangle(-22, -14, 44, 28)
    c.fill()
    c.set_source_rgb(1, 1, 1)
    c.select_font_face("Inter", 0, 1)
    c.set_font_size(5)
    for i, word in enumerate(("CUSTOMER", "SUCCESS")):
        ext = c.text_extents(word)
        c.move_to(-ext.x_advance / 2.0, -4 + i * 8)
        c.show_text(word)
    c.restore()


def _slate(c, text):
    c.set_source_rgba(0.08, 0.07, 0.06, 0.72)
    c.rectangle(24, 500, 912, 28)
    c.fill()
    c.set_source_rgb(0.96, 0.94, 0.90)
    c.select_font_face("Inter", 0, 0)
    c.set_font_size(14)
    c.move_to(32, 519)
    c.show_text(text[:90])


def holds(directory=None):
    """One slate still per shot. The same hold() the assembler loops."""
    directory = directory or os.path.join(EP, "rough")
    os.makedirs(directory, exist_ok=True)
    out = []
    for shot in SHOTS:
        path = os.path.join(directory, "bp_rough_v2_hold_%s.png" % shot["id"])
        hold(shot, slate=True).write_to_png(path)
        out.append(path)
    return out


def hold(shot, slate=False, scale=fr.SCALE):
    over = overlay_still(shot["motion"]) if shot["motion"] else None
    surf = fr.paint(CAM[shot["cam"]], overlay=over, hide_plan=shot["hide"], grade=shot["grade"], scale=scale)
    if slate:
        c = cairo.Context(surf)
        label = "%s  %s" % (shot["id"], shot["title"])
        if shot["line"]:
            label += "  —  " + shot["line"]
        _slate(c, label)
    return surf


def _crop_png(src, dst, x, y, w, h):
    full = cairo.ImageSurface.create_from_png(src)
    crop = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    ctx = cairo.Context(crop)
    ctx.set_source_surface(full, -x, -y)
    ctx.paint()
    crop.write_to_png(dst)
    return dst


def insert_stills(directory=None):
    """Pictures for rough v5. Not the locked stills, and not written by stills()."""
    directory = directory or os.path.join(EP, "stills")
    os.makedirs(directory, exist_ok=True)
    by_id = {s["id"]: s for s in SHOTS}
    out = []
    shot = by_id["04"]
    path = os.path.join(directory, "bp_still_cannon.png")
    fr.paint(CAM[shot["cam"]], overlay=cannon_overlay, hide_plan=shot["hide"], grade=shot["grade"]).write_to_png(path)
    out.append(path)
    # World (619, 504) on S0 is the same point on the 960 frame, then 2x.
    out.append(_crop_png(path, os.path.join(directory, "bp_still_cannon_crop.png"), 1000, 760, 520, 300))
    shot = by_id["12"]
    path = os.path.join(directory, "bp_still_star.png")
    fr.paint(CAM[shot["cam"]], overlay=star_overlay, hide_plan=shot["hide"], grade=shot["grade"]).write_to_png(path)
    out.append(path)
    # Phone centre (360, 470) on S0, at 2x.
    out.append(_crop_png(path, os.path.join(directory, "bp_still_star_crop.png"), 560, 780, 400, 280))
    shot = by_id["08"]
    for name, overlay in (
        ("retry", retry_overlay),
        ("lipstick", lipstick_overlay),
        ("calendar", calendar_overlay),
        ("deleted", deleted_overlay),
    ):
        path = os.path.join(directory, "bp_still_%s.png" % name)
        fr.paint(CAM[shot["cam"]], overlay=overlay, hide_plan=shot["hide"], grade=shot["grade"]).write_to_png(path)
        out.append(path)
        out.append(_crop_png(path, os.path.join(directory, "bp_still_%s_crop.png" % name), 420, 0, 1080, 560))
    return out


def stills(directory=None):
    directory = directory or os.path.join(EP, "stills")
    os.makedirs(directory, exist_ok=True)
    jobs = [
        ("bp_still_s0.png", fr.S0, True, 1.0, None),
        ("bp_still_shred.png", fr.SHRED, True, 1.0, None),
        ("bp_still_counter.png", fr.COUNTER, False, 1.0, None),
        ("bp_still_night.png", fr.NIGHT, True, 0.55, None),
    ]
    out = []
    for name, cam, hide, grade, over in jobs:
        surf = fr.paint(cam, overlay=over, hide_plan=hide, grade=grade)
        out.append(fr.write_png(surf, os.path.join(directory, name)))
    import bp_set
    out.append(bp_set.ground_plan(os.path.join(EP, "bp_ground_plan.png")))
    return out


def _head(world, cam, r=28):
    x, y = world
    cx, cy, z = cam
    return ((x - cx) * z + fr.W / 2, (y - cy) * z + fr.H / 2, r * z)


def layouts(directory=None):
    import speech
    from speech_gate import SAFE_16X9
    directory = directory or os.path.join(EP, "layouts")
    os.makedirs(directory, exist_ok=True)
    night = next(s for s in SHOTS if s["id"] == "05")
    cam = CAM[night["cam"]]
    surf = fr.paint(cam, hide_plan=True, grade=night["grade"], scale=1)
    c = cairo.Context(surf)
    k = kit.Ctx(c, 0)
    import bp_set
    sof = _head((bp_set.SOFIA[0], bp_set.SOFIA[1] - 70), cam)
    pam = _head((bp_set.PAM[0], bp_set.PAM[1] - 80), cam)
    speech.draw(k, "I won't draw one.", sof, safe=SAFE_16X9, others=[pam])
    speech.draw(k, "I'm matching them.", pam, safe=SAFE_16X9, others=[sof])
    night_path = fr.write_png(surf, os.path.join(directory, "bp_layout_night.png"))

    final = fr.paint(fr.S0, overlay=overlay_still("stamp"), hide_plan=False, grade=1.0, scale=1)
    c = cairo.Context(final)
    _slate(c, "13  final wide  —  stamp, no loop")
    final_path = fr.write_png(final, os.path.join(directory, "bp_layout_final.png"))
    return [night_path, final_path]


def _encode(path, draw_frame, nframes):
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", "%dx%d" % (fr.OUT_W, fr.OUT_H), "-r", str(FPS), "-i", "-",
           "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709"] + _BSF + [path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(nframes):
        surf = draw_frame(i, nframes)
        raw, w, h = fr.rgb_bytes(surf)
        if (w, h) != (fr.OUT_W, fr.OUT_H):
            proc.kill()
            raise RuntimeError("frame %s x %s" % (w, h))
        proc.stdin.write(raw)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed: %s" % path)
    return path


# Door opening to the home, then a short step back toward the opening. Pose stays stand.
ARRIVE = (48, 132)
STEP_BACK = (132, 80)
WALK_N = 90
CROP_N = 90
# Shot 08 is 30 s. Four reads fill it. 225 frames is 7.5 s.
WEEK_N = 225
# COUNTER's visible world is about x 426..1034, y 149..491.
# Pam's head is near (694, 338). This point is on the wall above both heads.
WEEK_AT = (700, 196)
# A still on a tighter camera. strips forces the plan on; the night hold keeps it hidden.
CROPS = {"zero": "ZERO", "stampword": "STAMP", "strips": "PLAN"}


def _place_client(c, x):
    """The room Client, at a path x. Same scale, same face, same stand pose."""
    import fs_storyboard_v17 as sb
    import bp_set
    k = kit.Ctx(c, 0)
    bp_set._contact(k, x, bp_set.CLIENT[1], 36)
    sb.client(k, x, bp_set.CLIENT[1], bp_set.CLIENT[2], "stand", "confident", (0.9, 0))


def _walk_x(ends, i, n):
    t = i / max(1, n - 1)
    return ends[0] + (ends[1] - ends[0]) * t


def _static(shot, overlay):
    """One painted frame, repeated. The insert does not move the room."""
    base = fr.paint(CAM[shot["cam"]], overlay=overlay, hide_plan=shot["hide"], grade=shot["grade"])

    def draw(i, n, base=base):
        return base
    return draw


def _motion_draw(kind, n_base_shot):
    shot = n_base_shot
    if kind == "cannon":
        return _static(shot, cannon_overlay)
    if kind == "star":
        return _static(shot, star_overlay)
    week = {
        "retry": retry_overlay,
        "lipstick": lipstick_overlay,
        "calendar": calendar_overlay,
        "deleted": deleted_overlay,
    }
    if kind in week:
        return _static(shot, week[kind])
    if kind in CROPS:
        hide = False if kind == "strips" else shot["hide"]
        over = overlay_still("stamp") if kind == "stampword" else None
        base = fr.paint(CAM[CROPS[kind]], overlay=over, hide_plan=hide, grade=shot["grade"])

        def draw(i, n, base=base):
            return base
        return draw
    walking = kind in ("arrive", "back")
    import bp_set
    if walking:
        bp_set.SKIP_CLIENT[0] = True
    try:
        base = fr.paint(CAM[shot["cam"]], hide_plan=shot["hide"], grade=shot["grade"])
    finally:
        if walking:
            bp_set.SKIP_CLIENT[0] = False
    fn = {"frame": frame_fall, "shred": shred_sheet, "finger": finger, "pocket": pocket, "stamp": stamp}.get(kind)

    def draw(i, n):
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, fr.OUT_W, fr.OUT_H)
        surf.set_device_scale(fr.SCALE, fr.SCALE)
        c = cairo.Context(surf)
        c.set_source_surface(base, 0, 0)
        c.paint()
        c.save()
        c.rectangle(0, 0, fr.W, fr.H)
        c.clip()
        fr.view(c, *CAM[shot["cam"]])
        if kind == "arrive":
            _place_client(c, _walk_x(ARRIVE, i, n))
            frame_fall(c, min(1.0, i / 59.0))
        elif kind == "back":
            _place_client(c, _walk_x(STEP_BACK, i, n))
        else:
            fn(c, i / max(1, n - 1))
        c.restore()
        return surf
    return draw


def motion_frames(directory=None):
    """First, middle and last frame of each moving beat, under rough_work/v2."""
    directory = directory or os.path.join(EP, "rough_work", "v2")
    os.makedirs(directory, exist_ok=True)
    by_id = {s["id"]: s for s in SHOTS}
    jobs = (
        ("frame", "01", 60),
        ("shred", "03", 60),
        ("finger", "03", 45),
        ("pocket", "11", 60),
        ("stamp", "13", 60),
    )
    out = []
    for kind, sid, n in jobs:
        draw = _motion_draw(kind, by_id[sid])
        for label, i in (("00", 0), ("mid", n // 2), ("last", n - 1)):
            path = os.path.join(directory, "bp_rough_v2_%s_%s.png" % (kind, label))
            draw(i, n).write_to_png(path)
            out.append(path)
    return out


def walk_frames(directory=None):
    """Start, mid-step and home for the arrival and the step back."""
    directory = directory or os.path.join(EP, "rough_work", "v3")
    os.makedirs(directory, exist_ok=True)
    by_id = {s["id"]: s for s in SHOTS}
    out = []
    jobs = (
        ("arrive", "01", WALK_N, (0, WALK_N // 2, WALK_N - 1), ("00", "mid", "home")),
        ("back", "04", WALK_N, (0, WALK_N // 2, WALK_N - 1), ("00", "mid", "far")),
    )
    for kind, sid, n, frames, labels in jobs:
        draw = _motion_draw(kind, by_id[sid])
        for label, i in zip(labels, frames):
            path = os.path.join(directory, "bp_rough_v3_%s_%s.png" % (kind, label))
            draw(i, n).write_to_png(path)
            out.append(path)
    # The step back returns to the mark for the hold. That still is the shot 04 hold.
    path = os.path.join(directory, "bp_rough_v3_back_home.png")
    hold(by_id["04"], slate=False).write_to_png(path)
    out.append(path)
    return out


def motion_tests(directory=None):
    directory = directory or os.path.join(EP, "motion")
    os.makedirs(directory, exist_ok=True)
    by_id = {s["id"]: s for s in SHOTS}
    jobs = [
        ("bp_motion_frame.mp4", "frame", by_id["01"], 60),
        ("bp_motion_shred.mp4", "shred", by_id["03"], 60),
        ("bp_motion_finger.mp4", "finger", by_id["03"], 45),
        ("bp_motion_pocket.mp4", "pocket", by_id["11"], 60),
        ("bp_motion_stamp.mp4", "stamp", by_id["13"], 60),
    ]
    out = []
    for name, kind, shot, n in jobs:
        out.append(_encode(os.path.join(directory, name), _motion_draw(kind, shot), n))
    return out


def _hold_clip(shot, frames, directory):
    path = os.path.join(directory, "hold_%s.mp4" % shot["id"])
    png = os.path.join(directory, "hold_%s.png" % shot["id"])
    hold(shot, slate=True).write_to_png(png)
    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", png,
        "-frames:v", str(frames), "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "20",
        "-preset", "veryfast", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
        "-color_primaries", "bt709", "-color_trc", "bt709"] + _BSF + [path])
    return path


def _concat(parts, out, seconds):
    lst = out + ".txt"
    with open(lst, "w", encoding="utf-8") as f:
        for p in parts:
            f.write("file '%s'\n" % p.replace("\\", "/"))
    silent = out + ".silent.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error", "-i", silent,
        "-f", "lavfi", "-t", str(seconds), "-i", "anoisesrc=d=%d:c=pink:r=48000:a=0.4" % seconds,
        # 0.80: the v5 no-night join at 0.85 peaked at -0.94. The full file was left at 0.85.
        "-filter:a", "loudnorm=I=-15:TP=-1.5:LRA=11,alimiter=limit=0.80:level=disabled",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"] + _BSF + [
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", out])
    os.remove(silent)
    os.remove(lst)
    return out


def _refuse(path, extra=()):
    name = os.path.basename(path)
    banned = ("bp_rough_v1.mp4", "bp_rough_v1_nonight.mp4") + tuple(extra)
    if name in banned:
        raise SystemExit("refusing to write %s" % name)


def _older(version):
    names = []
    if version >= 3:
        names += ["bp_rough_v2.mp4", "bp_rough_v2_nonight.mp4"]
    if version >= 4:
        names += ["bp_rough_v3.mp4", "bp_rough_v3_nonight.mp4"]
    if version >= 5:
        names += ["bp_rough_v4.mp4", "bp_rough_v4_nonight.mp4"]
    return tuple(names)


def _motions(version):
    motions = {
        "01": [("frame", 60)],
        "03": [("shred", 60), ("finger", 45)],
        "11": [("pocket", 60)],
        "13": [("stamp", 60)],
    }
    if version >= 3:
        motions["01"] = [("arrive", WALK_N)]
        motions["04"] = [("back", WALK_N)]
    if version >= 4:
        motions["05"] = [("strips", CROP_N)]
        motions["07"] = [("zero", CROP_N)]
        motions["12"] = [("zero", CROP_N)]
        motions["13"] = [("stamp", 60), ("stampword", CROP_N)]
    if version >= 5:
        # After the walk. The hold underneath is unchanged: the client is back on his mark.
        motions["04"] = [("back", WALK_N), ("cannon", CROP_N)]
        motions["08"] = [
            ("retry", WEEK_N), ("lipstick", WEEK_N), ("calendar", WEEK_N), ("deleted", WEEK_N),
        ]
        motions["12"] = [("zero", CROP_N), ("star", CROP_N)]
    return motions


def _assemble(shots, out, work, version=2):
    _refuse(out, _older(version))
    os.makedirs(work, exist_ok=True)
    parts = []
    motions = _motions(version)
    by = {s["id"]: s for s in shots}
    for shot in shots:
        need = shot["dur"] * FPS
        for kind, n in motions.get(shot["id"], []):
            path = os.path.join(work, "m_%s_%s.mp4" % (shot["id"], kind))
            _encode(path, _motion_draw(kind, shot), n)
            parts.append(path)
            need -= n
        if need < 0:
            raise RuntimeError("motion longer than shot %s" % shot["id"])
        if need:
            parts.append(_hold_clip(shot, need, work))
    return _concat(parts, out, sum(s["dur"] for s in shots))


def rough(version=VERSION):
    if version < 1 or version > ROUGH_BUDGET:
        raise SystemExit("rough-cut budget is %d versions; refused %s" % (ROUGH_BUDGET, version))
    if version == 1:
        raise SystemExit("version 1 is the old room and is not rewritten")
    if version not in (2, 3, 4, 5):
        raise SystemExit("only v2, v3, v4 or v5 is built in this pass")
    work = os.path.join(EP, "rough_work", "v%d" % version)
    master = _assemble(SHOTS, os.path.join(EP, "bp_rough_v%d.mp4" % version), os.path.join(work, "full"), version)
    cut = _assemble(without_night(), os.path.join(EP, "bp_rough_v%d_nonight.mp4" % version),
                    os.path.join(work, "nonight"), version)
    return master, cut


def check(path, frames):
    import uz_check
    return uz_check.check_film(path, frames=frames, format="16x9", loop_max=None)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stills"
    if cmd == "takes":
        faults = check_takes()
        print("takes", "ok" if not faults else faults)
    elif cmd == "script":
        print(write_script())
    elif cmd == "stills":
        for p in stills():
            print(p)
    elif cmd == "inserts":
        for p in insert_stills():
            print(p)
    elif cmd == "layouts":
        for p in layouts():
            print(p)
    elif cmd == "holds":
        for p in holds():
            print(p)
    elif cmd == "motionframes":
        for p in motion_frames():
            print(p)
    elif cmd == "walks":
        for p in walk_frames():
            print(p)
    elif cmd == "motion":
        for p in motion_tests():
            print(p)
    elif cmd == "rough":
        if len(sys.argv) < 3:
            raise SystemExit("rough 2  — version 1 is the old room and is not rewritten")
        print(rough(int(sys.argv[2])))
    elif cmd == "check":
        print(check(os.path.join(EP, "bp_rough_v1.mp4"), 400 * FPS))
        print(check(os.path.join(EP, "bp_rough_v1_nonight.mp4"), 360 * FPS))
    else:
        raise SystemExit("takes | script | stills | inserts | layouts | motion | motionframes | holds | rough 2 | check")
