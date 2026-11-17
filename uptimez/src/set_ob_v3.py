"""v3, pinned.
THE ONBOARDING: the set, v3 (set_ob_v2.py = v2, kept): the walls are dressed (the grill of 17 Nov).
  - "OUR FIRST CLIENT": a gilt frame with a brass plate, on the wall between the door and the logo. It is empty, and
    stays empty to the last frame; nobody mentions it. first_client() draws it anywhere (the three-shot of beat 03).
  - the ficus from The Best Candidate (bc_set.ficus, redrawn here so that this film stands alone), by the door,
    behind the robot's parking place. sway: degrees, a breath of air when the door slides.
  stage(decor=True) draws both; decor=False is the bare wall of v2. The arms of everyone posed here are acts_ob v3.
THE ONBOARDING: the set and the robot's actions (v1), from the grill of 17 Nov. The front desk, at the door: the
glass door on the left (it slides; it opens the film and closes it), a reception desk on the right, the floor
shredder at the desk's near end, the card terminal on the desk. The camera is always inside, looking at the door.
The stage is 540 x 960 with the floor line at FLOOR; draw it inside any transform.
The robot is the HR robot of the last films (robot_mf), untouched: this file adds four actions and their props.
  "block"    it has rolled in between them and lifts a red paddle between the two palms (beat 02)
  "approve"  the same paddle, green, for the card (beat 07); v2: it leans toward the card. It stops the hand and
             loves the card, and it shows that with its body, not with a face
  "tip"      it tips the shredder's clear bin into the cannon (beat 08)
  "stamp"    its arm out, the stamp in it: ONBOARDING COMPLETE on the inside of the glass (beat 10)"""
import math
import cairo
import kit
import brand
import robot_mf as rm
import acts_ob as ac
from kit import INK, cut, rect, ellipse

FLOOR = 800
W, H = 540, 960
GLASS = (0.80, 0.90, 0.95)
DESK = (0.86, 0.80, 0.68)
DESK_DARK = (0.66, 0.58, 0.44)
GREEN = (0.20, 0.66, 0.38)
RED = (0.86, 0.16, 0.16)
DOOR = (22, 392, 150, FLOOR - 392)                         # x, y, w, h of the opening
SHRED_X = 246                                             # the shredder: at the near end of the desk, beside Don


def door(k, open_=0.0, seed=300):
    """The glass door. open_ 0 = shut, 1 = slid fully to the left. Behind it: the bright street."""
    c = k.c
    x, y, w, h = DOOR
    rect(k, x - 8, y - 8, w + 16, h + 8, (0.36, 0.38, 0.44), seed, shadow=False, lw=2.2)          # the frame
    c.set_source_rgb(0.95, 0.96, 0.92); c.rectangle(x, y, w, h); c.fill()                           # outside
    c.save(); c.rectangle(x, y, w, h); c.clip()
    px = x - w * 0.92 * open_
    c.set_source_rgba(*GLASS, 0.62); c.rectangle(px, y, w, h); c.fill()
    c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(7)
    for dx in (26, 44):
        c.move_to(px + dx, y + h - 20); c.line_to(px + dx + 54, y + 20); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.rectangle(px, y, w, h); c.stroke()
    rect(k, px + w - 22, y + h * 0.46, 8, 62, (0.72, 0.74, 0.78), seed + 1, shadow=False, lw=1.4)    # the handle
    c.restore()
    return px


GILT, BRASS, MAT = (0.76, 0.60, 0.24), (0.85, 0.72, 0.38), (0.96, 0.94, 0.88)
FRAME_AT = (262, 356)                                      # the centre of OUR FIRST CLIENT on the stage wall
FICUS_X = 216


def first_client(k, x, y, s=1.0, seed=420):
    """The empty frame. (x, y) is the centre of the frame; the plate hangs below it."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.arc(0, -66, 2.2, 0, 2 * math.pi); c.fill()                          # the nail
    c.set_line_width(1.0); c.move_to(-18, -52); c.line_to(0, -66); c.line_to(18, -52); c.stroke()  # the wire
    rect(k, -44, -54, 88, 108, GILT, seed, lw=2.2)
    rect(k, -36, -46, 72, 92, (0.60, 0.46, 0.17), seed + 1, shadow=False, lw=1.4)                  # the inner edge
    rect(k, -32, -42, 64, 84, MAT, seed + 2, shadow=False, lw=1.2)                                 # nothing in it
    c.set_source_rgba(0.60, 0.56, 0.48, 0.55); c.set_line_width(1.1); c.set_dash([4, 4])            # where a photo goes
    c.rectangle(-20, -28, 40, 52); c.stroke(); c.set_dash([])
    rect(k, -52, 62, 104, 20, BRASS, seed + 3, lw=1.5)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(9.6)
    c.set_source_rgb(0.24, 0.18, 0.06)
    e = c.text_extents("OUR FIRST CLIENT"); c.move_to(-e.x_advance / 2, 75.5); c.show_text("OUR FIRST CLIENT")
    c.restore()


def ficus(k, x, floor, s=1.0, sway=0.0, seed=440):
    """The office ficus of The Best Candidate, drawn as there."""
    c = k.c
    c.save(); c.translate(x, floor); c.scale(s, s)
    cut(k, [(-26, -44), (26, -44), (20, 0), (-20, 0)], (0.72, 0.42, 0.28), lw=2.2)
    rect(k, -30, -52, 60, 10, (0.78, 0.47, 0.32), seed, shadow=False, lw=2)
    c.translate(0, -50); c.rotate(math.radians(sway))
    c.set_source_rgb(0.36, 0.26, 0.18); c.set_line_width(5); c.set_line_cap(1)
    c.move_to(0, 0); c.curve_to(-6, -46, 8, -78, 2, -120); c.stroke()
    leaves = [(-26, -76, -0.9, 0), (24, -86, 0.8, 1), (-34, -108, -0.6, 1), (30, -118, 0.5, 0), (-22, -138, -0.3, 0),
              (22, -150, 0.35, 1), (-38, -160, -0.7, 0), (36, -170, 0.75, 1), (-12, -178, -0.2, 1), (12, -192, 0.15, 0),
              (-28, -196, -0.5, 1), (30, -200, 0.55, 0), (0, -212, 0.0, 1)]
    for i, (dx, dy, rot, tone) in enumerate(leaves):
        c.save(); c.translate(dx, dy); c.rotate(rot)
        ellipse(k, 0, 0, 13, 23, ((0.20, 0.50, 0.30), (0.26, 0.60, 0.36))[tone], seed + 3 + i, shadow=False, lw=1.8)
        c.set_source_rgb(0.14, 0.36, 0.22); c.set_line_width(1.2); c.move_to(0, -17); c.line_to(0, 17); c.stroke()
        c.restore()
    c.restore()


def stage(k, open_=0.0, shred=0.0, terminal=True, back=True, decor=True, sway=0.0):
    """Wall, floor, the door, the desk with its in-tray, the shredder beside it; v3: the frame and the ficus."""
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, W, FLOOR); c.fill()
    c.set_source_rgb(0.72, 0.63, 0.50); c.rectangle(0, FLOOR, W, H - FLOOR); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(0, FLOOR); c.line_to(W, FLOOR); c.stroke()
    if back:
        brand.mark(c, 372, 300, 64, zzz=False)
    px = door(k, open_)
    if decor:
        first_client(k, *FRAME_AT)
        ficus(k, FICUS_X, FLOOR + 6, 0.95, sway)
    return px


def desk(k, terminal=True, shred=None, seed=320):
    """Background: draw it BEFORE the people, who stand in front of it. shred: None, or the bin's fill 0..1 to draw
    the shredder at the desk's near end too (draw it yourself, later, when someone must stand behind it)."""
    rect(k, 300, FLOOR - 150, 250, 150, DESK, seed, lw=2.4)
    rect(k, 292, FLOOR - 162, 266, 16, DESK_DARK, seed + 1, shadow=False, lw=2)
    rect(k, 318, FLOOR - 182, 66, 20, (0.30, 0.32, 0.38), seed + 2, shadow=False, lw=1.6)          # the in-tray
    rect(k, 324, FLOOR - 190, 54, 8, (0.98, 0.97, 0.94), seed + 3, shadow=False, lw=1.2)
    if terminal:
        card_terminal(k, 446, FLOOR - 162, 1.0)
    if shred is not None:
        ac.shredder(k, SHRED_X, FLOOR, 1.0, fill=shred)


def card_terminal(k, x, y, s=1.0, state=None, seed=340):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -17, -44, 34, 44, (0.20, 0.21, 0.26), seed, lw=1.8)
    col = GREEN if state == "ok" else (0.70, 0.86, 0.92)
    rect(k, -13, -40, 26, 16, col, seed + 1, shadow=False, lw=1.2)
    for i in range(6):
        ellipse(k, -8 + (i % 3) * 8, -17 + (i // 3) * 7, 2.2, 2.0, (0.60, 0.62, 0.68), seed + 2 + i, shadow=False, lw=0.8)
    c.restore()


def payment(c, k, x, y, s):
    """The insert of beat 07."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -84, -110, 168, 220, (0.20, 0.21, 0.26), 360, lw=2.4)
    rect(k, -72, -98, 144, 120, GREEN, 361, shadow=False, lw=1.8)
    c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1)
    for txt, size, yy in (("PAYMENT", 19, -66), ("APPROVED", 19, -44), ("$1.00", 30, -8), ("PILOT", 13, 12)):
        c.set_font_size(size); e = c.text_extents(txt); c.move_to(-e.x_advance / 2, yy); c.show_text(txt)
    for i in range(9):
        ellipse(k, -40 + (i % 3) * 40, 44 + (i // 3) * 22, 11, 7, (0.60, 0.62, 0.68), 362 + i, shadow=False, lw=1.2)
    c.restore()


def paddle(k, x, y, s, ok=False, seed=380):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(6 * s); c.set_line_cap(1); c.move_to(x, y + 4 * s); c.line_to(x, y - 30 * s); c.stroke()
    c.set_source_rgb(0.72, 0.60, 0.40); c.set_line_width(3.4 * s); c.move_to(x, y + 4 * s); c.line_to(x, y - 30 * s); c.stroke()
    ellipse(k, x, y - 54 * s, 27 * s, 27 * s, GREEN if ok else RED, seed, lw=2.4 * s)
    c.set_source_rgb(1, 1, 1); c.set_line_width(7 * s); c.set_line_cap(1); c.set_line_join(1)
    if ok:
        c.move_to(x - 13 * s, y - 54 * s); c.line_to(x - 4 * s, y - 44 * s); c.line_to(x + 14 * s, y - 66 * s)
    else:
        c.move_to(x - 15 * s, y - 54 * s); c.line_to(x + 15 * s, y - 54 * s)
    c.stroke()


def cannon(k, x, floor, s=1.0, seed=400):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(3.2 * s); c.set_line_cap(1)
    for dx in (-22, 0, 22):
        c.move_to(x, floor - 44 * s); c.line_to(x + dx * s, floor); c.stroke()
    c.save(); c.translate(x, floor - 52 * s); c.rotate(-0.55)
    cut(k, [(-14 * s, 22 * s), (14 * s, 22 * s), (24 * s, -44 * s), (-24 * s, -44 * s)], (0.93, 0.74, 0.20), lw=2.2 * s)
    for yy in (8, -12, -32):
        c.set_source_rgb(0.86, 0.22, 0.20); c.set_line_width(5 * s); c.move_to(-17 * s, yy * s); c.line_to(17 * s, yy * s); c.stroke()
    c.restore()


def stamp(c, x, y, s, ang=-0.10):
    """The show's signature: a green stamp, a little uneven, technically true."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgba(*GREEN, 0.92); c.set_line_width(5)
    c.rectangle(-92, -36, 184, 72); c.stroke()
    c.set_line_width(1.6); c.rectangle(-85, -29, 170, 58); c.stroke()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    for txt, size, yy in (("ONBOARDING", 22, -4), ("COMPLETE", 22, 21)):
        c.set_font_size(size); e = c.text_extents(txt); c.move_to(-e.x_advance / 2, yy); c.show_text(txt)
    c.restore()


def confetti(k, x0, y0, x1, y1, n=40, seed=7, s=1.0):
    c = k.c
    for i in range(n):
        u = ((i * 7919 + seed * 97) % 1000) / 1000.0
        v = ((i * 15485863 + seed * 31) % 1000) / 1000.0
        c.save(); c.translate(x0 + (x1 - x0) * u, y0 + (y1 - y0) * v); c.rotate(u * 6.3 + v)
        c.set_source_rgb(*ac.STRIP); c.rectangle(-9 * s, -2 * s, 18 * s, 4 * s); c.fill()
        c.set_source_rgb(1, 1, 1); c.rectangle(-6 * s, -0.5 * s, 10 * s, 1 * s); c.fill()
        c.restore()


# act -> (the robot_mf state whose layout is borrowed, the words for this film or None for the tick alone)
STATES = {"block": ("insufficient", (("CONTACT NOT", "VERIFIED"), rm.RED, "x")),
          "approve": ("detected", (("CONTACT", "APPROVED"), rm.GREEN, "tick")),
          "tip": ("approved", None), "stamp": ("approved", None)}


def robot(k, x, feet, s=1.0, act="idle", look=(0, 0), side=1, seed=900):
    if act == "idle":
        return rm.robot(k, x, feet, s, "stand", "eager", look, side, seed=seed)
    pose = {"block": rm.POSE_CUFFS, "approve": (0.16, -6, 0, (-20, 0), (150, 24)), "tip": (0.10, -4, 0, (-20, 0), (118, 30)),
            "stamp": (-0.06, 0, 0, (-96, 4), (20, 0))}[act]
    state, words = STATES[act]
    old = rm.STATES[state]
    if words:
        rm.STATES[state] = words
    try:
        o = rm.robot(k, x, feet, s, pose, state, look, side, seed=seed)
    finally:
        rm.STATES[state] = old
    c = k.c
    if act in ("block", "approve"):
        hx, hy = o["hands"][1]
        paddle(k, hx, hy, s, ok=act == "approve", seed=seed + 50)
    elif act == "tip":                                     # the clear bin, tipped, blue pouring out
        hx, hy = o["hands"][1]
        c.save(); c.translate(hx + 18 * s, hy - 10 * s); c.rotate(2.2)
        rect(k, -24 * s, -30 * s, 48 * s, 56 * s, (0.86, 0.92, 0.96), seed + 60, lw=1.8 * s)
        c.restore()
        confetti(k, hx + 20 * s, hy + 10 * s, hx + 62 * s, hy + 70 * s, n=12, seed=3, s=0.7 * s)
    elif act == "stamp":                                   # the stamp block in its near hand
        hx, hy = o["hands"][0]
        rect(k, hx - 26 * s, hy - 13 * s, 22 * s, 26 * s, GREEN, seed + 70, lw=1.8 * s)
        rect(k, hx - 8 * s, hy - 6 * s, 12 * s, 12 * s, (0.30, 0.32, 0.38), seed + 71, shadow=False, lw=1.4 * s)
    return o
