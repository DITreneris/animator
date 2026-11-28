"""Approved. (episode 16): the new props and Sofía's CEO power suit, stage 3 (Tomas /grill-me 28 Nov: "Props sheet,
then K1/K2"; the folding chair grey metal and cheap; Sofía's suit a restyle of episode 15's). Opt-in: nothing here
changes a module an earlier episode imports; a frame that does not call these draws as before.

Reuses episode 15's sheet tiles (da_props.tile) and its REVIEW tag (da_sheets._tag) as they are; so, like
rv_night_cast, it runs on a checkout with episode 15's modules (branch uptimez-double-agent) until that is merged.

  folding_chair(k, x, feet, s, state)    "open", "wobble" (a leg short, tilted), "folded" (carried flat)
  washer(k, x, y, s)                     the Client's washer, from his pocket
  review_tag(k, x, y, s, word)           TOMORROW = episode 15's tag as drawn; TODAY = the same tag, the other side
  invoice(k, x, y, s)                    COFFEE MACHINE REPAIR · $80 · UNPAID (a red stamp)
  name_card(k, x, y, s)                  the Client's tent card: a wrench and CLIENT
  report(k, x, y, s, unfurl)             the robot's report: folded (0) to an accordion run onto the floor (1)
  screen(k, x, y, r, kind)               ONE function for every screen of the episode (script v4): the robot's face
                                         and the machine's panel share its type and colours, so HUMAN APPROVAL
                                         REQUIRED is the same drawing at 3.3 and 6.1
  sofia_ceo(...)                         sofia_da.sofia in black, a gold pin
  python3 rv_props.py sheet  -> ../the-review/rv_props_v1.png and rv_props_v1_feed.png (the 270 px read)
"""
import math
import os
import sys
import cairo
from PIL import Image
import kit
from kit import INK
import bp_frame as bp
import da_props as dprp
import da_sheets as dsh
import sofia_da as sd

EP = "../the-review/"
STEEL, STEEL_DARK, SEAT = (0.62, 0.64, 0.67), (0.42, 0.44, 0.48), (0.50, 0.52, 0.55)
PAPER, RED = (0.99, 0.97, 0.90), (0.72, 0.08, 0.12)
SCREEN_BG, SCREEN_INK = (0.04, 0.07, 0.13), bp.NIGHT_MONITOR
CEO_SUIT = [(0.11, 0.11, 0.13), (0.04, 0.04, 0.05)]
GOLD = (0.86, 0.68, 0.22)


def _line(c, pts, w, col=INK):
    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1); c.set_line_join(1)
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.stroke()


def folding_chair(k, x, feet, s=1.0, state="open"):
    """a thin grey steel folding chair, a worn grey seat: the cheapest chair in the room (Father's, "Executive.")."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    if state == "folded":                                    # carried flat under an arm: one tall thin slab
        _line(c, [(-10, 0), (-6, -150)], 5, STEEL_DARK); _line(c, [(10, 0), (6, -150)], 5, STEEL_DARK)   # legs
        kit.cut(k, [(-12, -150), (12, -150), (12, -118), (-12, -118)], SEAT, lw=2.2)                  # the back panel
        kit.cut(k, [(-9, -86), (9, -86), (9, -52), (-9, -52)], SEAT, lw=2.2)                         # the seat, folded up
        _line(c, [(-12, -4), (12, -70)], 3.5, STEEL); _line(c, [(12, -4), (-12, -70)], 3.5, STEEL)
        c.restore(); return
    short = 9 if state == "wobble" else 0                   # v2 (review: "the tilt reads as a deformed drawing"): one
                                                             # leg plainly short of the floor, the chair upright
    for lx, top in ((-30, -112), (30, -112)):                # the back legs rise into the back frame
        _line(c, [(lx, 0), (lx * 0.9, top - 40)], 6, STEEL_DARK)
    kit.cut(k, [(-30, -152), (30, -152), (28, -120), (-28, -120)], SEAT, lw=2.2)     # the back panel
    _line(c, [(-38, 0), (34, -70)], 5, STEEL); _line(c, [(38, -short), (-34, -70)], 5, STEEL)
    if short:
        c.set_source_rgba(0, 0, 0, 0.35); c.set_line_width(1.6); c.move_to(30, 0); c.line_to(46, 0); c.stroke()   # the floor under the gap
    kit.cut(k, [(-40, -74), (40, -74), (36, -62), (-36, -62)], SEAT, lw=2.2)       # the seat
    c.set_source_rgba(1, 1, 1, 0.25); c.set_line_width(2); c.move_to(-30, -71); c.line_to(10, -71); c.stroke()
    c.restore()


def washer(k, x, y, s=1.0):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(0.74, 0.75, 0.78); c.arc(0, 0, 9, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.arc(0, 0, 9, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(0.97, 0.96, 0.93); c.arc(0, 0, 3.6, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.arc(0, 0, 3.6, 0, 2 * math.pi); c.stroke()
    c.restore()


def review_tag(k, x, y, s=1.0, word="TOMORROW"):
    """TOMORROW is episode 15's tag, called as it is. TODAY: the same card turned (its geometry, type and colours)."""
    if word == "TOMORROW":
        return dsh._tag(k, x, y, s)
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(0.93, 0.76, 0.28); c.set_line_width(3); c.move_to(0, 0); c.line_to(0, 22); c.stroke()
    kit.cut(k, [(-48, 22), (48, 22), (48, 64), (-48, 64)], PAPER, lw=2.4)
    c.select_font_face(kit.FONT); c.set_font_size(13); c.set_source_rgb(*RED)
    for txt, yy in (("REVIEW", 40), (word, 57)):
        e = c.text_extents(txt); c.move_to(-e.x_advance / 2, yy); c.show_text(txt)
    c.restore()


def invoice(k, x, y, s=1.0, ang=-0.05):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    kit.cut(k, [(-44, -58), (44, -58), (44, 58), (-44, 58)], PAPER, lw=2.2)
    c.select_font_face(kit.FONT); c.set_source_rgb(*INK)
    for txt, yy, fs in (("COFFEE MACHINE", -38, 9), ("REPAIR", -26, 9)):
        c.set_font_size(fs); e = c.text_extents(txt); c.move_to(-e.x_advance / 2, yy); c.show_text(txt)
    c.set_line_width(1); c.set_source_rgba(*INK, 0.45)
    for yy in (-14, -6, 2):
        c.move_to(-32, yy); c.line_to(32, yy); c.stroke()
    c.set_source_rgb(*INK); c.set_font_size(26); e = c.text_extents("$80"); c.move_to(-e.x_advance / 2, 30); c.show_text("$80")
    c.save(); c.translate(0, 46); c.rotate(-0.22)                   # the stamp
    c.set_source_rgb(*RED); c.set_line_width(2.6); c.rectangle(-36, -11, 72, 22); c.stroke()
    c.set_font_size(15); e = c.text_extents("UNPAID"); c.move_to(-e.x_advance / 2, 6); c.show_text("UNPAID")
    c.restore()
    c.restore()


def _wrench(c, x, y, s, col=INK):
    c.save(); c.translate(x, y); c.rotate(-0.7); c.scale(s, s)
    c.set_source_rgb(*col)
    c.rectangle(-3, -2, 6, 26); c.fill()
    c.arc(0, -6, 8, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*PAPER); c.rectangle(-3, -16, 6, 10); c.fill()
    c.restore()


def name_card(k, x, y, s=1.0):
    """a tent card: a wrench pictogram and CLIENT (the mute read is the wrench)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    kit.cut(k, [(-50, 0), (50, 0), (44, -46), (-44, -46)], PAPER, lw=2.2)
    kit.cut(k, [(-44, -46), (44, -46), (40, -50), (-40, -50)], (0.88, 0.85, 0.76), lw=1.6, shadow=False)
    _wrench(c, -26, -24, 0.95)
    c.select_font_face(kit.FONT); c.set_font_size(13); c.set_source_rgb(*INK)
    c.move_to(-12, -18); c.show_text("CLIENT")
    c.restore()


def report(k, x, y, s=1.0, unfurl=0.0, seed=0):
    """unfurl 0: a folded stack held out; 1: an accordion run from (x, y) down and along the floor (to +x)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    if unfurl <= 0.0:
        kit.cut(k, [(-30, -20), (30, -20), (30, 20), (-30, 20)], PAPER, lw=2.2)
        c.set_source_rgba(*INK, 0.5); c.set_line_width(1)
        for yy in (-10, -3, 4, 11):
            c.move_to(-20, yy); c.line_to(20, yy); c.stroke()
        c.restore(); return
    # v2 (review: "steps, a little bridge"): ONE continuous strip, its folds marked, falling then running along the
    # floor; unfurl > 1 adds the second spill at its end (the extra portion that reaches Don's shoes, 5.2)
    fall, run = 150 * min(unfurl, 1.0), 260 * min(unfurl, 1.0) + 70 * max(0.0, unfurl - 1.0)
    pts = [(0, 0), (6, fall * 0.5), (0, fall), (20, fall + 6)]
    n = 6
    for i in range(1, n + 1):
        pts.append((20 + run * i / n, fall + 6 + (3 if i % 2 else -3)))
    c.set_source_rgb(*kit.INK); c.set_line_width(30); c.set_line_join(1); c.set_line_cap(0)
    c.move_to(*pts[0]); [c.line_to(*q) for q in pts[1:]]; c.stroke()
    c.set_source_rgb(*PAPER); c.set_line_width(26)
    c.move_to(*pts[0]); [c.line_to(*q) for q in pts[1:]]; c.stroke()
    c.set_source_rgba(*INK, 0.45); c.set_line_width(1.4)                 # the folds
    for i in range(1, n):
        x = 20 + run * i / n
        c.move_to(x, fall - 7); c.line_to(x + 2, fall + 19); c.stroke()
    for y in (fall * 0.33, fall * 0.66):
        c.move_to(-10, y); c.line_to(12, y); c.stroke()
    c.restore()


def _don_face(c, x, y, r):
    """APPROVER: CEO's face: Don as a pictogram (bald, the curl, the headset)."""
    c.set_source_rgb(0.98, 0.84, 0.72); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(max(1.0, r * 0.12)); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    for ex in (-0.36, 0.36):
        c.set_source_rgb(1, 1, 1); c.arc(x + ex * r, y - 0.05 * r, 0.24 * r, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(*INK); c.arc(x + ex * r, y - 0.05 * r, 0.10 * r, 0, 2 * math.pi); c.fill()
    c.set_line_width(max(1.0, r * 0.10)); c.move_to(x - 0.25 * r, y + 0.45 * r); c.line_to(x + 0.25 * r, y + 0.45 * r); c.stroke()
    c.arc(x + 0.1 * r, y - 1.05 * r, 0.22 * r, math.pi * 0.2, math.pi * 1.3); c.stroke()          # the curl
    c.arc(x, y, 1.12 * r, math.pi * 1.1, math.pi * 1.9); c.stroke()                               # the headset band


SCREENS = {"POSITION VACANT": ["POSITION", "VACANT"], "NOTED.": ["NOTED."], "UPTIME 100%": ["UPTIME", "100%"],
           "SALARY $0": ["SALARY", "$0"], "HUMAN APPROVAL REQUIRED": ["HUMAN", "APPROVAL", "REQUIRED"],
           "APPROVER: CEO": ["APPROVER:", "CEO"]}


def screen(k, x, y, r, kind, shape="round", face_fn=None):
    """Every screen of the episode in one drawing: the robot's face (round) and the machine's panel (rect). The type
    fills the screen so it reads at 270 px (cold round 4: "unreadable", "covers its face")."""
    c = k.c
    lines = SCREENS[kind]
    c.save()
    c.set_source_rgb(*SCREEN_BG)
    if shape == "round":
        c.arc(x, y, r, 0, 2 * math.pi)
    else:
        c.rectangle(x - r * 1.25, y - r * 0.8, r * 2.5, r * 1.6)
    c.fill()
    c.set_source_rgba(*SCREEN_INK, 0.18); c.set_line_width(r * 0.10)
    if shape == "round":
        c.arc(x, y, r * 0.92, 0, 2 * math.pi)
    else:
        c.rectangle(x - r * 1.18, y - r * 0.73, r * 2.36, r * 1.46)
    c.stroke()
    face = kind == "APPROVER: CEO"
    if kind == "SALARY $0":                                  # v2 (review): a small SALARY over a big $0
        c.select_font_face("Inter", 0, 1); c.set_source_rgb(*SCREEN_INK)
        for t, fs, yy in (("SALARY", r * 0.26, y - r * 0.38), ("$0", r * 0.95, y + r * 0.40)):
            c.set_font_size(fs); e = c.text_extents(t); c.move_to(x - e.width / 2 - e.x_bearing, yy); c.show_text(t)
        c.restore(); return
    ty = y - (r * 0.30 if face else 0)
    c.select_font_face("Inter", 0, 1); c.set_source_rgb(*SCREEN_INK)
    width = (1.55 if shape == "round" else 2.2) * r
    size = r * (0.58 if len(lines) == 1 else 0.40 if len(lines) == 2 else 0.31)
    c.set_font_size(size)
    wmax = max(c.text_extents(t).width for t in lines)
    if wmax > width:
        size *= width / wmax; c.set_font_size(size)
    for i, t in enumerate(lines):
        e = c.text_extents(t)
        c.move_to(x - e.width / 2 - e.x_bearing, ty + (i - (len(lines) - 1) / 2.0) * size * 1.12 + size * 0.36)
        c.show_text(t)
    if face:
        if face_fn:                                          # v2 (both reviews: the pictogram "a baby's head"): Don's
            c.save(); c.arc(x, y + r * 0.45, r * 0.36, 0, 2 * math.pi); c.clip()        # rig head, clipped
            face_fn(k, x, y + r * 0.45, r * 0.36); c.restore()
        else:
            _don_face(c, x, y + r * 0.45, r * 0.30)
    c.restore()


def sofia_ceo(k, x, feet, s=1.0, *a, **kw):
    """Sofía's CEO power suit (episode 16): episode 15's suit cut in black, a gold pin on the lapel."""
    old = list(sd.SUIT)
    sd.SUIT[:] = CEO_SUIT
    try:
        o = sd.sofia(k, x, feet, s, *a, **kw)
    finally:
        sd.SUIT[:] = old
    c = k.c
    hx, hy = o["head"][:2]
    px, py = hx - 20 * s, hy + 74 * s                        # the left lapel, above the binder she holds
    c.set_source_rgb(*GOLD); c.arc(px, py, 6.5 * s, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6 * s); c.arc(px, py, 6.5 * s, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.6); c.arc(px - 2 * s, py - 2 * s, 1.8 * s, 0, 2 * math.pi); c.fill()
    return o


def _tile_night(draw, label, w=260, h=200, scale=2.0):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, int(w * scale), int(h * scale))
    c = cairo.Context(s); c.scale(scale, scale)
    import rv_night as rn
    c.set_source_rgb(*rn.NIGHT_WALL); c.paint()
    k = kit.Ctx(c, 0)
    c.save(); c.translate(w / 2, h / 2 + 10); draw(k); c.restore()
    c.select_font_face("Inter", 0, 1); c.set_font_size(11); c.set_source_rgb(0.95, 0.95, 0.97)
    c.move_to(8, 16); c.show_text(label)
    s.flush()
    return Image.frombuffer("RGB", (s.get_width(), s.get_height()), bytes(s.get_data()), "raw", "BGRX", 0, 1)


PROPS = [
    ("Father's folding chair", lambda k: folding_chair(k, 0, 80, 0.9, "open")),
    ("... wobbling (1.5)", lambda k: folding_chair(k, 0, 80, 0.9, "wobble")),
    ("... folded, leaving (6.10)", lambda k: folding_chair(k, 0, 80, 0.9, "folded")),
    ("the washer", lambda k: washer(k, 0, 0, 3.0)),
    ("REVIEW · TODAY (1.7)", lambda k: review_tag(k, 0, -50, 1.6, "TODAY")),
    ("REVIEW · TOMORROW (E15, 6.10)", lambda k: review_tag(k, 0, -50, 1.6, "TOMORROW")),
    ("the $80 invoice (5.4)", lambda k: invoice(k, 0, 0, 1.25)),
    ("the Client's name card (4.1)", lambda k: name_card(k, 0, 30, 1.5)),
    ("the report, held out (2.3)", lambda k: report(k, 0, 0, 1.6, 0)),
    ("the report, unfurled (5.2)", lambda k: report(k, -90, -80, 0.5, 1.0)),
    ("... its second spill (5.2)", lambda k: report(k, -90, -80, 0.5, 1.6)),
    ("screen: POSITION VACANT", lambda k: screen(k, 0, 0, 56, "POSITION VACANT")),
    ("screen: NOTED.", lambda k: screen(k, 0, 0, 56, "NOTED.")),
    ("screen: UPTIME 100%", lambda k: screen(k, 0, 0, 56, "UPTIME 100%")),
    ("screen: SALARY $0", lambda k: screen(k, 0, 0, 56, "SALARY $0")),
    ("panel: HUMAN APPROVAL REQUIRED (3.3)", lambda k: screen(k, 0, 0, 48, "HUMAN APPROVAL REQUIRED", "rect")),
    ("screen: HUMAN APPROVAL REQUIRED (6.1)", lambda k: screen(k, 0, 0, 56, "HUMAN APPROVAL REQUIRED")),
    ("screen: APPROVER: CEO (6.2)", lambda k: screen(k, 0, 0, 56, "APPROVER: CEO")),
    ("Sofía, CEO power suit", lambda k: sofia_ceo(k, 0, 96, 0.46, "hold", "smile")),
]


def sheet(out=EP + "rv_props_v2.png"):
    big = [_tile_night(fn, lab) for lab, fn in PROPS]
    cols = 6
    rows = (len(big) + cols - 1) // cols
    tw, th = big[0].size
    sh = Image.new("RGB", (cols * tw, rows * th), (255, 255, 255))
    for i, im in enumerate(big):
        sh.paste(im, ((i % cols) * tw, (i // cols) * th))
    sh.save(out)
    feed = Image.new("RGB", (cols * tw // 4, rows * th // 4), (255, 255, 255))
    for i, im in enumerate(big):                              # the 270 px feed: half of the film's 540, as da_props
        feed.paste(im.resize((tw // 4, th // 4), Image.LANCZOS), ((i % cols) * tw // 4, (i // cols) * th // 4))
    feed.save(out.replace(".png", "_feed.png"))
    print("wrote", out)


if __name__ == "__main__":
    {"sheet": sheet}[sys.argv[1]]()
