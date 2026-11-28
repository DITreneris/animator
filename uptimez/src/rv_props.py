"""Approved. (episode 16): the new props and Sofía's CEO power suit, stage 3 (Tomas /grill-me 28 Nov: "Props sheet,
then K1/K2"; the folding chair grey metal and cheap; Sofía's suit a restyle of episode 15's). Opt-in: nothing here
changes a module an earlier episode imports; a frame that does not call these draws as before.

Reuses episode 15's sheet tiles (da_props.tile) and its REVIEW tag (da_sheets._tag) as they are; so, like
rv_night_cast, it runs on a checkout with episode 15's modules (branch uptimez-double-agent) until that is merged.

  folding_chair(k, x, feet, s, state)    "open", "wobble" (a leg short, tilted), "folded" (carried flat)
  washer(k, x, y, s)                     the Client's washer, from his pocket
  review_tag(k, x, y, s, word)           v2: episode 15's swing ticket "A" (TOMORROW its own function, TODAY the same)
  setup_canon(), props_selftest()        the throne's price as episode 15's (style B here), the retired props gated
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
    """v2 (Tomas 28 Nov /grill-me: episode 15's tag as it ends, not as it began): da_layouts.review_tag style "A", the
    price's swing ticket (a gold cord looped round the point at (x, y), two strands to a knot, a card with cut corners,
    an eyelet, a gold rule, red letters). TOMORROW is episode 15's function itself; TODAY the same drawing, the other
    word (the same lines, checked against it in props_selftest()). v1 (dsh._tag: a stick, the card stuck on) is gone."""
    import da_layouts as dl
    if word == "TOMORROW":
        _record(k, lambda k_: dl.review_tag(k_, x, y, s, "A"), "REVIEW " + word)
        return dl.review_tag(k, x, y, s, "A")
    _record(k, lambda k_: _review_tag_word(k_, x, y, s, word), "REVIEW " + word)
    return _review_tag_word(k, x, y, s, word)


def _review_tag_word(k, x, y, s, word):
    """da_layouts.review_tag "A" line for line, with `word` in place of TOMORROW."""
    import da_layouts as dl
    c = k.c
    CORD, CORD_D = dl.TAG_CORDS["A"]
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_line_cap(1)
    for col, lw in ((INK, 6.5), (CORD, 3.5)):
        c.set_source_rgb(*col); c.set_line_width(lw)
        c.save(); c.translate(0, 20); c.scale(1, 0.45); c.arc(0, 0, 9, 0, 2 * math.pi); c.restore(); c.stroke()
    ln = 26
    for col, lw in ((INK, 5.5), (CORD, 3.0)):
        c.set_source_rgb(*col); c.set_line_width(lw)
        for sx in (-1, 1):
            c.move_to(0, 24); c.curve_to(sx * 9, 24 + ln * 0.35, sx * 7, 24 + ln * 0.8, 0, 24 + ln + 9); c.stroke()
    kit.ellipse(k, 0, 24, 5, 4.5, CORD, 4601, shadow=False, lw=1.8)
    c.translate(0, 24 + ln)
    W, H = 104, 58
    kit.cut(k, [(-W / 2, 8), (-W / 2 + 10, 0), (W / 2 - 10, 0), (W / 2, 8), (W / 2, H), (-W / 2, H)], (0.99, 0.97, 0.90), lw=2.6)
    c.set_source_rgb(*CORD_D); c.set_line_width(1.6)
    c.move_to(-W / 2 + 6, 15); c.line_to(W / 2 - 6, 15); c.line_to(W / 2 - 6, H - 6); c.line_to(-W / 2 + 6, H - 6); c.close_path(); c.stroke()
    kit.ellipse(k, 0, 8, 5.5, 5.5, CORD, 4602, shadow=False, lw=1.8)
    kit.ellipse(k, 0, 8, 2.2, 2.2, (0.20, 0.16, 0.10), 4603, shadow=False, outline=False)
    c.select_font_face(kit.FONT); c.set_font_size(14); c.set_source_rgb(0.72, 0.08, 0.12)
    for txt, yy in (("REVIEW", 32), (word, 48)):
        e = c.text_extents(txt); c.move_to(-e.x_advance / 2, yy); c.show_text(txt)
    c.restore()


# ---- the props by episode 15's canon (Tomas 28 Nov /grill-me, after "kodel tu nupaisei tokia nauja?") -------------------
# The throne's price: dh_props' swing ticket v2 (episode 15's S8 and S8r), style "A" on the crown's left point, as
# episode 15 ends (Tomas 28 Nov: "B", under the left armrest, was tried first and Don's mark or the robot covered it in
# 9 shots), TAG_FONT 19 (S8r: 23 ran past the card's rule). Episode 14's
# ps_set.price_tag (a white arrow card from the crown's right point), which the night set inherited, is off on the front.
# The props gate: drawing a retired prop's function records a fault (props_faults(); rv_hands.check reports it).
PROP_FAULTS = []
_CANON = [False]


def setup_canon():
    if _CANON[0]:
        return
    import dh_props as dhp
    import ps_set as pss
    dhp.TAG[0] = True; dhp.TAG_STYLE[0] = "A"; dhp.TAG_FONT[0] = 19
    old_price = pss.price_tag

    def price_tag(k, *a, **kw):
        if kw.get("back"):
            return old_price(k, *a, **kw)                       # its blank back, as episode 14/15 draw a spun throne
        if PLANT[0]:
            PROP_FAULTS.append("PROP ps_set.price_tag (episode 14's arrow card) drawn on the throne's front: the canon "
                               "is dh_props' swing ticket v2, style A")
            return old_price(k, *a, **kw)
    pss.price_tag = price_tag
    old_tag = dsh._tag

    def tag_v1(k, *a, **kw):
        PROP_FAULTS.append("PROP da_sheets._tag (REVIEW card v1, a stick and a card) drawn: the canon is "
                           "da_layouts.review_tag 'A' (rv_props.review_tag)")
        return old_tag(k, *a, **kw)
    dsh._tag = tag_v1
    old_pt = dhp._price_tag

    def dh_tag(k, style, seed):
        if style != "A":
            PROP_FAULTS.append("PROP the price tag in style %r: this episode's is 'A' (the crown's left point)" % style)
        _record(k, lambda k_: old_pt(k_, style, seed), "$49,999")
        return old_pt(k, style, seed)
    dhp._price_tag = dh_tag
    _CANON[0] = True


PLANT = [False]                                                 # props_selftest() only: draw the retired front tag

# COVER (Tomas 28 Nov: "yes, add it"): G3 fails a sign the frame's edge cuts; nothing failed one a person covers. Each
# canon sign this module draws (the price, the REVIEW card) is recorded with the matrix it was drawn under; after the
# frame is finished, the sign is drawn again alone on a blank page under that matrix, its red letters found, and the
# finished frame must still show red at most of them. Under 70 % (and not all hidden: "whole or out") is a fault.
RECORDED = []


def begin_frame():
    del RECORDED[:]


def _record(k, fn, name):
    c = k.c
    m = c.get_matrix()
    probe = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); pc = cairo.Context(probe)
    pc.set_matrix(m); fn(kit.Ctx(pc, 0))
    import numpy as np
    a = np.ndarray((960, 540, 4), np.uint8, probe.get_data())
    red = (a[..., 2].astype(int) > a[..., 1].astype(int) + 70) & (a[..., 2].astype(int) > a[..., 0].astype(int) + 70) \
        & (a[..., 3] > 200)                                     # BGRA: letters red on the cream card
    ink = a[..., 3] > 200                                       # the whole card (and its cord), on this page
    if ink.sum() < 8:
        return                                                  # off the page: out, as G3 wants
    ys, xs = np.nonzero(red) if red.sum() else np.nonzero(ink)
    key = (round(m.x0), round(m.y0), name)
    if any(r[3] == key for r in RECORDED):                      # the rim pass draws the throne again
        return
    iy, ix = np.nonzero(ink)
    full = (ix.min(), iy.min(), ix.max(), iy.max()) if len(ix) else None
    RECORDED.append((name, red, (xs.min(), ys.min(), xs.max(), ys.max()), key, full))


def cover_faults(surface, w=540, h=960):
    import numpy as np
    surface.flush()
    a = np.ndarray((h, w, 4), np.uint8, surface.get_data()).astype(int)
    seen = (a[..., 2] > a[..., 1] + 40) & (a[..., 2] > a[..., 0] + 40)
    out = []
    for name, red, box, _, full in RECORDED:
        if full and (full[0] <= 0 or full[2] >= w - 1 or full[1] <= 0 or full[3] >= h - 1):
            out.append("EDGE '%s': its card is cut by the frame (a sliver with no letters is still a cut sign)" % name)
            continue
        if box[0] <= 1 or box[1] <= 1 or box[2] >= w - 2 or box[3] >= h - 2:
            continue                                            # at the edge: G3's case
        n = int(red.sum()); v = int((red & seen).sum())
        if n == 0:
            continue
        if 0 < v < 0.70 * n:
            out.append("COVER '%s' %d %% visible (letters at (%d, %d)): whole or out" % (name, 100 * v // n, box[0], box[1]))
    return out


def props_faults():
    out = list(PROP_FAULTS)
    del PROP_FAULTS[:]
    return out


def props_selftest():
    """the retired drawings must fail; the canon ones must pass; TODAY's tag must match TOMORROW's but for the word."""
    import ps_set as pss
    import da_layouts as dl
    setup_canon()
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 300, 300)
    k = kit.Ctx(cairo.Context(s), 0)
    ok = True
    props_faults()
    PLANT[0] = True; pss.price_tag(k, 100, 100, 2.4); PLANT[0] = False
    f = props_faults(); ok &= bool(f); print("plant ps_set front tag:", "FAIL as it must" if f else "PASSED: broken")
    dsh._tag(k, 100, 100, 1.0)
    f = props_faults(); ok &= bool(f); print("plant REVIEW v1:", "FAIL as it must" if f else "PASSED: broken")
    import dh_props as dhp
    dhp._price_tag(k, "B", 1)
    f = props_faults(); ok &= bool(f); print("plant price style B:", "FAIL as it must" if f else "PASSED: broken")
    pss.throne(k)
    f = props_faults(); ok &= not f; print("canon throne + tag A:", "PASS" if not f else f)
    # COVER: the price drawn whole, then a person's block over half of it
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); kk = kit.Ctx(cairo.Context(S), 0)
    kk.c.set_source_rgb(0.3, 0.3, 0.35); kk.c.paint(); begin_frame()
    kk.c.save(); kk.c.translate(270 - pss.THRONE[0], 800 - pss.THRONE[1]); pss.throne(kk); kk.c.restore()
    f = cover_faults(S); ok &= bool(RECORDED) and not f
    print("cover, the tag whole:", "PASS" if RECORDED and not f else ("nothing recorded" if not RECORDED else f))
    box = RECORDED[0][2]
    RECORDED.append(RECORDED[0][:4] + ((530, 300, 539, 340),))   # plant: a card's sliver at the right edge
    f = cover_faults(S); ok &= any("EDGE" in x for x in f); print("plant a sliver at the edge:", "FAIL as it must" if f else "PASSED: broken")
    RECORDED.pop()
    kk.c.set_source_rgb(0.1, 0.1, 0.4); kk.c.rectangle(box[0], box[1], (box[2] - box[0]) * 0.6, box[3] - box[1]); kk.c.fill()
    f = cover_faults(S); ok &= bool(f); print("plant a person over 60 % of it:", "FAIL as it must" if f else "PASSED: broken")
    def png(fn):
        s2 = cairo.ImageSurface(cairo.FORMAT_RGB24, 300, 300); k2 = kit.Ctx(cairo.Context(s2), 0)
        k2.c.set_source_rgb(1, 1, 1); k2.c.paint(); fn(k2)
        return bytes(s2.get_data())
    a = png(lambda k2: dl.review_tag(k2, 150, 60, 2.0, "A"))
    b = png(lambda k2: _review_tag_word(k2, 150, 60, 2.0, "TOMORROW"))
    ok &= a == b; print("TODAY's drawing = episode 15's but for the word:", "PASS" if a == b else "FAIL")
    return ok


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


SOFIA_V5 = [False]   # opt-in (28 Nov, Tomas: "refresh the characters from episode 15"): the suit over episode 15's
                     # locked Sofía v5 (sofia_da.LOOK_V5: library hands, no badge, the fuller ponytail, the gold
                     # necklace and drop earrings). False draws the props sheet v2 as committed.


def sofia_ceo(k, x, feet, s=1.0, *a, **kw):
    """Sofía's CEO power suit (episode 16): episode 15's suit cut in black, a gold pin on the lapel."""
    old = list(sd.SUIT)
    old_v5 = sd.LOOK_V5[0] if hasattr(sd, "LOOK_V5") else None
    sd.SUIT[:] = CEO_SUIT
    if SOFIA_V5[0] and old_v5 is not None:
        sd.LOOK_V5[0] = True
    try:
        o = sd.sofia(k, x, feet, s, *a, **kw)
    finally:
        sd.SUIT[:] = old
        if old_v5 is not None:
            sd.LOOK_V5[0] = old_v5
    c = k.c
    hx, hy = o["head"][:2]
    px, py = hx - 20 * s, hy + 74 * s                        # the left lapel, above the binder she holds
    c.set_source_rgb(*GOLD); c.arc(px, py, 6.5 * s, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6 * s); c.arc(px, py, 6.5 * s, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.6); c.arc(px - 2 * s, py - 2 * s, 1.8 * s, 0, 2 * math.pi); c.fill()
    return o


NEEDLE = {"green": 0.15, "yellow": 0.40, "orange": 0.66, "red": 0.90}    # the needle's place on the dial, 0..1


def gauge(k, x, base, s, needle="green"):
    """Episode 16's b-story dial, drawn over the machine's own gauge (dh_props.coffee_machine: centre (36, -108) x s):
    a bigger face with four zones, green, yellow, orange, red, and the needle in one of them. A new drawing: the
    machine itself is unchanged."""
    c = k.c
    cx, cy, r = x + 36 * s, base - 108 * s, 15 * s
    c.save()
    c.set_source_rgb(0.97, 0.96, 0.91); c.arc(cx, cy, r, 0, 2 * math.pi); c.fill()
    zones = [((0.20, 0.70, 0.30), 0.0, 0.3), ((0.95, 0.80, 0.15), 0.3, 0.55), ((0.95, 0.50, 0.12), 0.55, 0.78),
             ((0.86, 0.14, 0.14), 0.78, 1.0)]
    a0, a1 = math.pi * 0.85, math.pi * 2.15                     # the dial's sweep, left-bottom round the top to right
    for col, u0, u1 in zones:
        c.set_source_rgb(*col); c.set_line_width(4.2 * s)
        c.new_path(); c.arc(cx, cy, r * 0.74, a0 + (a1 - a0) * u0, a0 + (a1 - a0) * u1); c.stroke()
    a = a0 + (a1 - a0) * NEEDLE[needle]
    c.set_source_rgb(*INK); c.set_line_width(2.4 * s); c.set_line_cap(1)
    c.move_to(cx, cy); c.line_to(cx + math.cos(a) * r * 0.86, cy + math.sin(a) * r * 0.86); c.stroke(); c.set_line_cap(0)
    c.arc(cx, cy, 2.2 * s, 0, 2 * math.pi); c.fill()
    c.set_line_width(1.8 * s); c.arc(cx, cy, r, 0, 2 * math.pi); c.stroke()
    c.restore()
    return (cx, cy, r)


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
    if sys.argv[1] == "selftest":
        sys.exit(0 if props_selftest() else 1)
    {"sheet": sheet}[sys.argv[1]]()
