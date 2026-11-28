"""The Double Agent (episode 15): the props sheet (plan v2 §2, 3.4). Reuse first (CLAUDE.md rule 2): every prop that a
film already drew is called from where it lives; two are new here (the robot's minutes, Don's cup and saucer).

  prop                       shots            drawn by
  Pam's mustard mug          3.2-5.1, 8.1     da_set.pam_mug (the one silhouette in every shot)
  the gift: the mug + bow    2.4, 3.2         da_sheets.gift_mug
  her old blue mug, broken   2.4              da_sheets._shards
  Don's cup and saucer       3.2-5.3          NEW cup_and_saucer: hand_lib_sheet_v3.big_cup's china, the saucer's
  AGENDA: WITHOUT HIM        6.1-6.3          NEW minutes(): the robot's printout, a torn feed edge
  MY GARAGES, rolled / flat  6.6, 7.3, 8.1    client_ob.blueprint_roll / acts_ob.plan_open (GARAGES + TITLE)
  REVIEW · TOMORROW          1.3, the loop    da_sheets._tag
  the paperclip box, clips   1.4, 2.1-7.4     sofia_da.clip_box, da_s8r.clip
  Sofía's binder             1.4              sofia_da.binder
  Mom's knitting             3.4, 4.3, 5.4    mom_fs.knitting
  the peeled strip, the roll 7.1-7.2, 1.1     don_ps.tape_strip, da_s8r.roll_on_floor's roll

  v2 (27 Nov, after the props audit): python3 da_props.py ../the-double-agent v2 -> da_props_v2.png / _feed.png.
  Episode copies here: shards_v2, bow_v2 / gift_mug_v2, cup_and_saucer_v2 (slop in the well), plan_open_v2 (numbers
  off the lines, a hand-drawn ring round 7), roll_v2 (spiral ends), strip_v2 (thin, twisting), knitting_v2 (loops,
  yarn, wound ball), robot_picks_clip. Opt-in flags elsewhere: da_set.MUG_V2, sofia_da.BINDER_V2 / CLIPS_V2
  (+ sofia_da.paperclip), da_s8.V8 (python3 da_s8.py frame8 -> da_s8_final_v8.png).

  python3 da_props.py  -> ../the-double-agent/da_props_v1.png (the props at 2x) and da_props_v1_feed.png (each at its
                          film size, then at 270 px wide: a sign must read there)
"""
import math
import os
import sys

import cairo
from PIL import Image

import kit
from kit import Ctx, INK
import da_set as ds
import da_sheets as dsh
import da_hands as dh
import hand_lib_sheet_v3 as hs
import client_ob as cob
import acts_ob as ac
import sofia_da as sd
import mom_fs as mf
import don_ps as dp
import ps_set as pss
import da_s8r as r8

PAPER = (0.98, 0.98, 0.96)
ROBOT_TXT = (0.16, 0.18, 0.22)


def cup_and_saucer(k, x, y, s=1.0, slop=False):
    """Don's cup on its saucer (white china, not the shirt's white: the 5.2 audit); slop: coffee spilled in the saucer."""
    hs.saucer_at(k, x, y + 2 * s, 0.95 * 20 * s / 30.0 * 1.6)
    if slop:
        kit.ellipse(k, x + 8 * s, y - 3 * s, 7 * s, 2.2 * s, dh.COFFEE, 7301, shadow=False, lw=0.8)
    dh.cup(k, x, y - 4 * s, 0.9 * s, 1)


def gift_mug(k, x, y, s=1.0):
    """Don's gift (2.4): Pam's mug itself (da_set.pam_mug, the one silhouette: "one prop, one shape"), a gold bow tied
    on its handle (script v4: "a gold bow on the handle"). da_sheets.gift_mug drew the series mug, handle left and dark:
    a second silhouette for the same mug, not used."""
    ds.pam_mug(k, x, y, s)
    c = k.c
    c.save(); c.translate(x + 23 * s, y - 15 * s); c.scale(s, s)
    for sx in (-1, 1):
        kit.cut(k, [(0, 0), (sx * 9, -7), (sx * 9, 7)], dsh.GOLD_BOW, shadow=False, lw=1.6)
    kit.ellipse(k, 0, 0, 3, 3, dsh.GOLD_BOW, 7311, shadow=False, lw=1.4)
    c.restore()


def minutes(k, x, y, s=1.0, ang=0.0):
    """The robot's printed minutes: thermal paper, a torn feed edge at the top, AGENDA: small, WITHOUT HIM big, three
    grey lines under it (6.3's insert reads it whole; at 6.1 it only has to read as a page)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    top = [(-40 + i * 8, -60 + (3 if i % 2 else 0)) for i in range(11)]
    kit.cut(k, top + [(40, 60), (-40, 60)], PAPER, lw=2)
    c.select_font_face(kit.FONT, 0, 1)
    c.set_source_rgb(*ROBOT_TXT); c.set_font_size(11)
    e = c.text_extents("AGENDA:"); c.move_to(-e.x_advance / 2, -34); c.show_text("AGENDA:")
    for line, yy in (("WITHOUT", -10), ("HIM", 14)):
        c.set_font_size(15.5); e = c.text_extents(line); c.move_to(-e.x_advance / 2, yy); c.show_text(line)
    c.set_source_rgb(0.70, 0.72, 0.74); c.set_line_width(2.4)
    for yy in (30, 40, 50):
        c.move_to(-30, yy); c.line_to(30 - (yy - 30), yy); c.stroke()
    c.restore()


# ---- v2 (27 Nov, the props audit 7.1/10; Tomas: "anything that does not change other series") ---------------------
# Shared drawers stay as they are: the episode copies live here, ep15 modules got opt-in flags (da_set.MUG_V2,
# sofia_da.BINDER_V2 / CLIPS_V2), defaults off, so S8 v7, S8r v4 and Sofía's sheets rebuild byte-identical.

BLUE_MUG = (0.36, 0.62, 0.80)
BLUE_MUG_IN = (0.62, 0.80, 0.90)                               # the glazed inside, lighter: a curved piece shows both faces


def shards_v2(k, x, y, s=1.0, seed=5650):
    """Her old blue mug, broken (2.4), lying at (x, y): the handle snapped off whole with a stub of wall, the base (a
    disc with its foot ring), three curved wall pieces showing the light inside face, and chips."""
    import random
    r = random.Random(seed)
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    # the base: a flattened disc, its broken wall edge jagged
    pts = [(-13 + i * 2.6, -3 - (2.5 if i % 2 else 0) - 2 * math.sin(i * 0.6)) for i in range(11)]
    kit.cut(k, pts + [(13, 1), (11, 4), (-11, 4), (-13, 1)], BLUE_MUG, shadow=False, lw=1.6)
    kit.ellipse(k, 0, -1.5, 10, 2.4, BLUE_MUG_IN, seed + 1, shadow=False, lw=1.0)
    # the handle with a stub of wall, on its side to the right
    c.save(); c.translate(30, -3); c.rotate(0.5)
    kit.cut(k, [(-4, -9), (2, -10), (3, -4), (1, 2), (3, 9), (-4, 9), (-6, 0)], BLUE_MUG, shadow=False, lw=1.5)
    c.set_source_rgb(*INK); c.set_line_width(5.2); c.new_path(); c.arc(2, 0, 7, -1.3, 1.3); c.stroke()
    c.set_source_rgb(*BLUE_MUG); c.set_line_width(2.6); c.new_path(); c.arc(2, 0, 7, -1.3, 1.3); c.stroke()
    c.restore()
    # three curved wall pieces: the outer face blue, a strip of the inside face along the curve
    for px, py, a, ln in ((-34, -4, -0.3, 15), (-20, 9, 0.6, 12), (14, 10, -0.9, 11)):
        c.save(); c.translate(px, py); c.rotate(a)
        kit.cut(k, [(-ln / 2, 0), (-ln / 4, -4), (ln / 4, -4.5), (ln / 2, -1), (ln / 2 - 2, 3), (-ln / 2 + 1, 3)],
                BLUE_MUG, shadow=False, lw=1.4)
        c.set_source_rgb(*BLUE_MUG_IN); c.set_line_width(1.6); c.new_path()
        c.move_to(-ln / 2 + 2, -0.5); c.curve_to(-ln / 4, -3, ln / 4, -3.4, ln / 2 - 1.5, -1); c.stroke()
        c.restore()
    for _ in range(7):                                                                        # chips
        px, py = r.uniform(-44, 44), r.uniform(-4, 12)
        if abs(px) < 16 and py < 6:
            continue
        c.save(); c.translate(px, py); c.rotate(r.uniform(0, 6.3)); z = r.uniform(1.6, 3)
        kit.cut(k, [(-z, 0), (z * 0.4, -z), (z, z * 0.5)], BLUE_MUG, shadow=False, lw=1.0)
        c.restore()
    c.restore()


def bow_v2(k, x, y, s=1.0, seed=7311):
    """The gold bow tied round the mug's handle at (x, y): two round loops, a knot, two tails hanging with V ends."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    for sx, a in ((-1, 0.45), (1, -0.35)):                                                    # the tails, behind
        c.save(); c.rotate(a * sx * 0.3)
        kit.cut(k, [(sx * 1, 1), (sx * 4, 2), (sx * 7, 13), (sx * 4.5, 11), (sx * 3, 14), (sx * -0.5, 3)],
                dsh.GOLD_BOW, shadow=False, lw=1.3)
        c.restore()
    for sx in (-1, 1):                                                                        # the loops
        c.new_path(); c.move_to(0, 0)
        c.curve_to(sx * 4, -9, sx * 14, -9, sx * 12, -2); c.curve_to(sx * 11, 3, sx * 4, 3, 0, 0); c.close_path()
        c.set_source_rgb(*dsh.GOLD_BOW); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
        c.set_source_rgba(0, 0, 0, 0.22); c.new_path(); c.move_to(sx * 2, -1); c.curve_to(sx * 5, -5, sx * 9, -5, sx * 10, -2.5)
        c.set_line_width(1.2); c.stroke()
    kit.ellipse(k, 0, -0.5, 2.6, 3.0, (0.86, 0.66, 0.16), seed, shadow=False, lw=1.3)     # the knot
    c.restore()


def gift_mug_v2(k, x, y, s=1.0):
    """The gift (2.4): Pam's mug v2 and the bow v2 knotted on its handle."""
    old = ds.MUG_V2[0]; ds.MUG_V2[0] = True
    try:
        ds.pam_mug(k, x, y, s)
    finally:
        ds.MUG_V2[0] = old
    bow_v2(k, x + 20 * s, y - 20 * s, 0.85 * s)


def cup_and_saucer_v2(k, x, y, s=1.0, slop=False):
    """v2: the slop pools in the saucer's well on the side away from the handle, a drip down the cup's side."""
    sc = 0.95 * 20 * s / 30.0 * 1.6
    hs.saucer_at(k, x, y + 2 * s, sc)
    if slop:
        wy = y + 2 * s - 12 * sc
        c = k.c
        c.save(); c.translate(x - 14 * sc, wy + 0.8 * sc); c.scale(9 * sc, 3.2 * sc); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi)
        c.restore(); c.set_source_rgb(*dh.COFFEE); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(0.8); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(1.0)
        c.save(); c.translate(x - 16 * sc, wy - 0.2 * sc); c.scale(4 * sc, 1.0 * sc); c.new_path(); c.arc(0, 0, 1, 3.6, 5.6)
        c.restore(); c.stroke()
    dh.cup(k, x, y - 4 * s, 0.9 * s, 1)
    if slop:
        c = k.c
        c.set_source_rgb(*dh.COFFEE); c.set_line_width(1.3 * s); c.set_line_cap(1); c.new_path()
        c.move_to(x - 9.5 * s, y - 12 * s); c.curve_to(x - 10 * s, y - 9 * s, x - 9.6 * s, y - 7 * s, x - 10.2 * s, y - 5 * s)
        c.stroke(); c.set_line_cap(0)


def _bays_v2():
    """Two facing rows of five, 22 tall (v1 26): room for the numbers inside the sheet, off every line."""
    return [(i + 1 + 5 * r, -52 + i * 21.25, (-33, 11)[r], 19, 22) for r in (0, 1) for i in range(5)]


def _ring(c, cx, cy, rx, ry, seed=0):
    """A hand-drawn marker ring: one stroke a little more than once round, its ends passing each other, wobbling."""
    import random
    r = random.Random(seed)
    ph = [r.uniform(0, 6.3) for _ in range(3)]
    c.new_path()
    a0, a1, n = -0.9, 2 * math.pi + 0.15, 48
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        f = 1.0 + 0.035 * math.sin(2 * a + ph[0]) + 0.02 * math.sin(3 * a + ph[1]) + 0.07 * i / n
        px, py = cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)
        (c.move_to if i == 0 else c.line_to)(px, py)
    c.stroke()


def plan_open_v2(k, x, y, s=1.0, seed=60):
    """MY GARAGES flat, the episode's copy of acts_ob.plan_open (GARAGES + TITLE): the two rows still face each other
    across the yard (the plan's joke); every number clear of the lines; no. 7 ringed by hand round its garage and its
    number, not through them."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    kit.rect(k, -62, -46, 124, 92, ac.BLUE, seed, lw=2.2)
    kit.rect(k, -62, -64, 124, 20, ac.BLUE, seed + 5, lw=2.2)
    c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(11.5); e = c.text_extents("MY GARAGES")
    c.move_to(-e.x_advance / 2 - e.x_bearing, -50); c.show_text("MY GARAGES")
    c.set_line_join(1)
    seven = None
    for n, bx, by, bw, bh in _bays_v2():
        c.set_source_rgb(1, 1, 1); c.set_line_width(1.5); ac._garage(c, bx, by, bw, bh, by < 0)
        c.set_font_size(8.5); t = str(n); e = c.text_extents(t)
        ny = by - 3 if by < 0 else by + bh + 3 + e.height
        c.move_to(bx + bw / 2 - e.x_advance / 2 - e.x_bearing, ny); c.show_text(t)
        if n == 7:
            seven = (bx + bw / 2, (by + ny - e.height / 2 + 1) / 2 + bh / 4)
    c.set_line_width(1.2); c.set_dash([5, 4]); c.move_to(-52, -0.5); c.line_to(52, -0.5); c.stroke(); c.set_dash([])
    c.set_source_rgb(0.90, 0.18, 0.20); c.set_line_width(2.2); c.set_line_cap(1)
    _ring(c, seven[0], seven[1] - 1.5, 12.0, 16.5, seed + 9)
    c.set_line_cap(0)
    c.restore()


def roll_v2(k, x, y, ang, ln=150, r=11, seed=0):
    """MY GARAGES rolled, the episode's copy of client_ob.blueprint_roll: blue paper (its back) outside; each end a
    white spiral, the blue edge of every turn showing; the paper's loose edge running along the roll."""
    c = k.c
    BP = cob.BLUEPRINT
    c.save(); c.translate(x, y); c.rotate(ang)
    kit.rect(k, -r, -ln / 2, 2 * r, ln, BP, seed + 1, shadow=False, lw=2)
    c.set_source_rgba(0, 0, 0, 0.16); c.rectangle(r * 0.35, -ln / 2 + 2, r * 0.55, ln - 4); c.fill()     # round: its shade
    c.set_source_rgba(1, 1, 1, 0.30); c.rectangle(-r * 0.7, -ln / 2 + 2, r * 0.25, ln - 4); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.5); c.move_to(-r * 0.15, -ln / 2 + 1); c.line_to(-r * 0.05, ln / 2 - 1); c.stroke()
    for end in (-1, 1):                                                                      # the spiral ends
        ey = end * ln / 2
        kit.ellipse(k, 0, ey, r, r * 0.42, (0.97, 0.97, 0.99), seed + 3 + end, shadow=False, lw=1.8)
        c.save(); c.translate(0, ey); c.scale(1, 0.42)
        c.set_source_rgb(*BP); c.set_line_width(1.3); c.new_path()
        for i in range(61):
            a = i * 0.33; rr = r * 0.88 * (1 - i / 66.0)
            (c.move_to if i == 0 else c.line_to)(rr * math.cos(a), rr * math.sin(a))
        c.stroke(); c.restore()
    c.restore()


def strip_v2(k, a, b, s, twist=0.55, seed=0):
    """The peeled strip (7.1-7.2), the episode's copy of don_ps.tape_strip: thin (6 s wide, v1 13) and flexible: it
    sags, waves and turns over once, so it narrows to an edge where it twists; the sticky side a shade darker."""
    c = k.c
    mx, my = (a[0] + b[0]) / 2, max(a[1], b[1]) + 30 * s
    P = []
    for i in range(41):
        t = i / 40.0
        bx = (1 - t) ** 3 * a[0] + 3 * (1 - t) ** 2 * t * mx + 3 * (1 - t) * t * t * mx + t ** 3 * b[0]
        by = (1 - t) ** 3 * a[1] + 3 * (1 - t) ** 2 * t * my + 3 * (1 - t) * t * t * my + t ** 3 * b[1]
        by += 4 * s * math.sin(t * math.pi * 3)
        P.append((bx, by, t))
    left, right, faces = [], [], []
    for i, (px, py, t) in enumerate(P):
        qx, qy = P[min(i + 1, 40)][:2] if i < 40 else P[i][:2]
        if i == 40:
            qx, qy = 2 * px - P[39][0], 2 * py - P[39][1]
        dx, dy = qx - px, qy - py; L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        wv = 3 * s * math.cos((t - twist) * math.pi * 1.4)
        faces.append(wv >= 0)
        left.append((px + nx * wv, py + ny * wv)); right.append((px - nx * wv, py - ny * wv))
    for i in range(40):                                                                      # quad by quad, both faces
        quad = [left[i], left[i + 1], right[i + 1], right[i]]
        c.new_path(); c.move_to(*quad[0])
        for q in quad[1:]:
            c.line_to(*q)
        c.close_path()
        c.set_source_rgb(*(dp.TAPE if faces[i] else (0.80, 0.63, 0.10))); c.fill_preserve()
        c.set_line_width(0.6); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.3)
    for side in (left, right):
        c.new_path(); c.move_to(*side[0])
        for q in side[1:]:
            c.line_to(*q)
        c.stroke()
    for end in (0, 40):
        c.new_path(); c.move_to(*left[end]); c.line_to(*right[end]); c.stroke()


def knitting_v2(k, x, y, s=1.0, seed=0):
    """Mom's knitting (3.4, 4.3, 5.4), the episode's copy of mom_fs.knitting: the scarf's rows as loops (V stitches in
    every stripe), DON knitted in whole, the live loops on the top needle, a yarn line from the needle to the ball, the
    ball wound (crossing strands)."""
    import mom_fs as mf
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(5):
        kit.cut(k, [(-30, -10 + i * 8), (24, -10 + i * 8), (24, -2 + i * 8), (-30, -2 + i * 8)],
                mf.TEAL if i % 2 == 0 else mf.MUSTARD, shadow=False, lw=1.2)
    c.set_line_width(0.9)
    for j in range(5):
        dark = (0.10, 0.36, 0.38) if j % 2 == 0 else (0.62, 0.46, 0.08)
        c.set_source_rgb(*dark)
        for i in range(9):
            x0, y0 = -28 + i * 6, -9 + j * 8
            c.new_path(); c.move_to(x0, y0); c.curve_to(x0 + 0.5, y0 + 5, x0 + 2.5, y0 + 6, x0 + 3, y0 + 6)
            c.curve_to(x0 + 3.5, y0 + 6, x0 + 5.5, y0 + 5, x0 + 6, y0); c.stroke()
    c.select_font_face("Inter", 0, 1); c.set_font_size(19)
    c.move_to(-26, 17); c.text_path("DON")
    c.set_source_rgb(*INK); c.set_line_width(3.5); c.stroke_preserve(); c.set_source_rgb(1, 1, 1); c.fill()
    for i in range(8):                                                                      # the live loops, on the needle
        x0 = -27 + i * 6.5
        c.set_source_rgb(*INK); c.set_line_width(2.4); c.new_path(); c.arc(x0, -12, 3, math.pi, 2 * math.pi); c.stroke()
        c.set_source_rgb(*mf.TEAL); c.set_line_width(1.2); c.new_path(); c.arc(x0, -12, 3, math.pi, 2 * math.pi); c.stroke()
    for a in (-0.5, -0.8):
        c.save(); c.rotate(a)
        c.set_source_rgb(*INK); c.set_line_width(5); c.new_path(); c.move_to(-10, -14); c.line_to(52, -14); c.stroke()
        c.set_source_rgb(0.75, 0.75, 0.80); c.set_line_width(3); c.new_path(); c.move_to(-10, -14); c.line_to(52, -14); c.stroke()
        kit.ellipse(k, 54, -14, 4, 4, (0.80, 0.10, 0.20), seed + 3, shadow=False, lw=1.2)
        c.restore()
    c.set_source_rgb(*mf.TEAL); c.set_line_width(1.6); c.new_path()                         # the yarn, needle to ball
    c.move_to(24, -12); c.curve_to(40, -10, 30, 14, 36, 18); c.stroke()
    kit.ellipse(k, 44, 26, 15, 15, mf.TEAL, seed + 5, lw=2)
    c.save(); c.new_path(); c.arc(44, 26, 14, 0, 2 * math.pi); c.clip()
    c.set_source_rgb(*mf.mo.TEAL_DARK); c.set_line_width(1.2)
    for a in (-0.9, -0.45, 0.0, 0.45, 0.9, 1.35):
        c.save(); c.translate(44, 26); c.rotate(a); c.scale(1, 0.45); c.new_path(); c.arc(0, 0, 13, 0, 2 * math.pi)
        c.restore(); c.stroke()
    c.restore()
    c.restore()


def robot_picks_clip(k, x, y, s=1.0):
    """The robot taking one clip from the box (2.1-7.4): its forearm down, the canon gripper (da_hand_gate.robot_grip),
    the clip held at the block's face, two thirds of it past the block so it reads."""
    import da_hand_gate as g
    c = k.c
    w = 17 * s
    ax, ay = x, y - 70 * s
    c.set_source_rgb(*INK); c.set_line_width(w + 4); c.set_line_cap(1); c.new_path(); c.move_to(ax, ay - 60 * s); c.line_to(ax, ay)
    c.stroke(); c.set_source_rgb(*g.METAL); c.set_line_width(w); c.new_path(); c.move_to(ax, ay - 60 * s); c.line_to(ax, ay)
    c.stroke(); c.set_line_cap(0)
    g.robot_grip(k, ax, ay, (0, 1), w)
    sd.paperclip(k, ax, ay + 52 * w / 22.0, 1.25 * s, math.pi / 2, lw=1.8)


def tile(draw, label, w=260, h=200, scale=2.0):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, int(w * scale), int(h * scale))
    c = cairo.Context(s); c.scale(scale, scale)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    c.save(); c.translate(w / 2, h / 2 + 10); draw(k); c.restore()
    c.select_font_face("Inter", 0, 1); c.set_font_size(11); c.set_source_rgb(*INK)
    c.move_to(8, 16); c.show_text(label)
    s.flush()
    return Image.frombuffer("RGB", (s.get_width(), s.get_height()), bytes(s.get_data()), "raw", "BGRX", 0, 1)


PROPS = [
    ("Pam's mug (mustard)", lambda k: ds.pam_mug(k, 0, 30, 2.2), 0.54),
    ("the gift: her mug + a bow", lambda k: gift_mug(k, 0, 30, 2.2), 0.54),
    ("her blue mug, shattered", lambda k: dsh._shards(k, 0, 20, 2.0), 0.54),
    ("Don's cup and saucer", lambda k: cup_and_saucer(k, 0, 20, 2.2), 0.60),
    ("... coffee in the saucer (5.2)", lambda k: cup_and_saucer(k, 0, 20, 2.2, slop=True), 0.60),
    ("AGENDA: WITHOUT HIM", lambda k: minutes(k, 0, 0, 1.3), 0.60),
    ("MY GARAGES, rolled", lambda k: cob.blueprint_roll(k, 0, 0, 1.2, 150, 11), 0.52),
    ("MY GARAGES, flat", lambda k: _plan(k), 0.52),
    ("REVIEW · TOMORROW", lambda k: dsh._tag(k, 0, -50, 1.6), 1.15),
    ("the paperclip box", lambda k: sd.clip_box(k, 0, 20, 1.6), 0.47),
    ("Sofía's binder", lambda k: sd.binder(k, 0, 0, 1.4), 0.47),
    ("Mom's knitting", lambda k: mf.knitting(k, 0, 0, 1.8), 0.54),
    ("the peeled strip", lambda k: dp.tape_strip(k, (-90, 0), (90, -10), 1.6), 0.60),
]


def _plan(k):
    old = ac.GARAGES[0], ac.TITLE[0]
    ac.GARAGES[0] = ac.TITLE[0] = True
    try:
        ac.plan_open(k, 0, 0, 1.4)
    finally:
        ac.GARAGES[0], ac.TITLE[0] = old


def _with(flags, fn):
    """run fn with the given opt-in flags on, then put them back."""
    def run(k):
        old = [f[0] for f in flags]
        for f in flags:
            f[0] = True
        try:
            fn(k)
        finally:
            for f, o in zip(flags, old):
                f[0] = o
    return run


PROPS_V2 = [
    ("Pam's mug v2 (rim, wall, loop)", _with([ds.MUG_V2], lambda k: ds.pam_mug(k, 0, 30, 2.2)), 0.54),
    ("the gift: her mug + a bow v2", lambda k: gift_mug_v2(k, 0, 30, 2.2), 0.54),
    ("her blue mug, broken v2", lambda k: shards_v2(k, 0, 10, 2.2), 0.54),
    ("Don's cup and saucer", lambda k: cup_and_saucer_v2(k, 0, 20, 2.2), 0.60),
    ("... coffee in the saucer v2", lambda k: cup_and_saucer_v2(k, 0, 20, 2.2, slop=True), 0.60),
    ("AGENDA: WITHOUT HIM", lambda k: minutes(k, 0, 0, 1.3), 0.60),
    ("MY GARAGES, rolled v2", lambda k: roll_v2(k, 0, 0, 1.2, 150, 11), 0.52),
    ("MY GARAGES, flat v2", lambda k: plan_open_v2(k, 0, 0, 1.4), 0.52),
    ("REVIEW · TOMORROW", lambda k: dsh._tag(k, 0, -50, 1.6), 1.15),
    ("clip box v2: full", _with([sd.CLIPS_V2], lambda k: sd.clip_box(k, 0, 20, 1.6, 1.0)), 0.47),
    ("clip box v2: a few / empty", _with([sd.CLIPS_V2], lambda k: (sd.clip_box(k, -55, 20, 1.3, 0.15),
                                                                  sd.clip_box(k, 55, 20, 1.3, 0.0))), 0.47),
    ("one clip; the robot takes one", lambda k: (sd.paperclip(k, -60, 0, 3.0, 0.4),
                                                 robot_picks_clip(k, 40, 60, 1.2)), 0.60),
    ("Sofía's binder v2", _with([sd.BINDER_V2], lambda k: sd.binder(k, 0, 0, 1.4)), 0.47),
    ("Mom's knitting v2", lambda k: knitting_v2(k, 0, 0, 1.8), 0.54),
    ("the peeled strip v2", lambda k: strip_v2(k, (-90, 0), (90, -10), 1.6), 0.60),
]


def main(out_dir="../the-double-agent", ver="v1"):
    props = PROPS_V2 if ver == "v2" else PROPS
    big = [tile(fn, lab) for lab, fn, _ in props]
    cols = 4
    rows = (len(big) + cols - 1) // cols
    tw, th = big[0].size
    sheet = Image.new("RGB", (cols * tw, rows * th), (255, 255, 255))
    for i, im in enumerate(big):
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(os.path.join(out_dir, "da_props_%s.png" % ver))
    feed = Image.new("RGB", (cols * tw // 4, rows * th // 4), (255, 255, 255))
    for i, im in enumerate(big):                                  # the 270 px feed: half of the film's 540
        feed.paste(im.resize((tw // 4, th // 4), Image.LANCZOS), ((i % cols) * tw // 4, (i // cols) * th // 4))
    feed.save(os.path.join(out_dir, "da_props_%s_feed.png" % ver))
    print("wrote da_props_%s.png, da_props_%s_feed.png" % (ver, ver))


if __name__ == "__main__":
    main(*sys.argv[1:])
