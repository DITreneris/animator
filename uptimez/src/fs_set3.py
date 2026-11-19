"""FIRST SEARCH (episode 10): the set v3 and its planning sheets, after the two reviews of the set map v1 (19 Nov).
fs_setmap.py (v1) is kept. Tomas's decisions: some of episode 9's blue confetti is still in the corners, not yet
gathered; Don's office door is in zone C.

Three sheets, kept apart (the reviewer: the overlapping camera boxes gave no animator an instruction):
  fs_set_v3.png        the clean master set: three zones, each with one job; depth; every home position
  fs_shotplan_v1.png   top-down plan, five camera setups, and a table: shot, zone, setup, size, length, subject
  fs_blocking7_v1.png  Mom's beat 6.1b-8.1, step by step: where she stands, where she walks, what the camera sees

The geography:
  A, discovery and arrivals: the glass door, the screen over it, the robot's station; confetti in the corner.
  B, the irony: OUR FIRST CLIENT on the wall over Don's spot; the sale, the bonk, the payoff, the lick.
  C, the counter and the boss's door: Pam at its left end with her monitor and the plan; the shredder in front of
     that end; Mom at its right end, next to DON's office door (she guards it: ASSISTANT TO DON). Her way out front:
     round the counter's LEFT end, past the shredder, into B (the right end is the office door).
Depth: the counter and the door are the back plane; the Client, the robot and Sofía the middle; Don stands forward,
under the portrait; the shredder is a foreground piece at the counter's end.
python3 fs_set3.py [out_dir]"""
import os
import sys
import json
import math
import cairo
import kit
import brand
import set_ob as st
import acts_ob as ac
import fs_set as fs
import fs_storyboard_v17 as sb                                # pinned: drawn with board v17
import mom_fs as mfs
import sofia_fs as sfs
import pam_fs
from kit import INK, rect, ellipse
from charsheets import corp, wrap

F = st.FLOOR
WW = 940
DX = 300                                                   # the counter, moved right: 576..866
HOME = {"client": (110, F - 14, 0.52), "robot": (232, F + 4, 0.48), "sofia": (384, F - 26, 0.47),
        "don": (474, F + 26, 0.60), "pam": (368 + DX, F - 72, 0.50), "mom": (500 + DX, F - 70, 0.50)}
SHRED = (548, F + 12, 0.95)
PORT = (474, 392)
SCR = (26, 286, 162, 100)
OFFICE = (876, 470, 60, 330)                               # Don's office door: x, top, w, h
ZONES = [("A", "discovery and arrivals", 0, 300, (0.20, 0.45, 0.85)),
         ("B", "the irony: under OUR FIRST CLIENT", 300, 560, (0.85, 0.30, 0.25)),
         ("C", "the counter and the boss's door", 560, WW, (0.20, 0.60, 0.35))]
ZCOL = {z: col for z, n, a, b, col in ZONES}


def office_door(k):
    x, y, w, h = OFFICE
    c = k.c
    rect(k, x - 6, y - 6, w + 12, h + 6, (0.30, 0.24, 0.20), 801, shadow=False, lw=2.2)
    rect(k, x, y, w, h, (0.62, 0.44, 0.28), 802, shadow=False, lw=2.2)
    for yy in (y + 30, y + 190):
        rect(k, x + 8, yy, w - 16, 120, (0.56, 0.39, 0.24), 803, shadow=False, lw=1.4)
    ellipse(k, x + 10, y + 180, 4, 4, (0.85, 0.72, 0.38), 804, shadow=False, lw=1.2)
    rect(k, x + 6, y + 8, w - 12, 18, (0.15, 0.17, 0.22), 805, shadow=False, lw=1.2)
    c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(9)
    c.move_to(x + 12, y + 20); c.show_text("DON · CEO")


def monitor(k, x, y, s=1.0):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -30, -48, 60, 40, (0.15, 0.16, 0.20), 811, lw=2)
    rect(k, -26, -44, 52, 32, (0.30, 0.55, 0.85), 812, shadow=False, lw=1.2)
    rect(k, -5, -8, 10, 8, (0.15, 0.16, 0.20), 813, shadow=False, lw=1.2)
    c.restore()


def confetti(k, x, y, w, seed=0):
    """A drift of episode 9's blue strips, swept into a corner and left there."""
    c = k.c
    import random
    r = random.Random(seed)
    for i in range(int(w * 1.2)):
        px, py = x + r.uniform(0, w), y - r.uniform(0, 14) * (1 - abs(r.uniform(-1, 1)))
        c.save(); c.translate(px, py); c.rotate(r.uniform(0, math.pi))
        c.set_source_rgb(*r.choice(((0.18, 0.42, 0.85), (0.30, 0.55, 0.95), (0.55, 0.75, 1.0))))
        c.rectangle(-4, -1, 8, 2.2); c.fill(); c.restore()


def draw_set(k, people=True):
    c = k.c
    oldW = st.W
    st.W = WW
    try:
        st.stage(k, open_=0.85, decor=False, back=False)
    finally:
        st.W = oldW
    brand.mark(c, 300, 230, 56, zzz=False)
    fs.screen(k, "query", *SCR)
    fs.PSTATE[0] = "clean"
    try:
        fs.portrait(k, *PORT, fs.PORTRAIT_S)
    finally:
        fs.PSTATE[0] = None
    office_door(k)
    confetti(k, 4, F + 2, 60, 1)                                                     # the corner by the glass door
    confetti(k, 560, F - 2, 24, 2)                                                   # behind the shredder
    with pam_fs.look(False):
        c.save(); c.translate(DX, 0)
        if people:
            sb.pam_taping(k, 368, F - 72, 0.50)
            mfs.mom(k, 500, F - 70, 0.50, "bag", "sweet", look=(-0.8, 0))
        st.desk(k, terminal=False, shred=None)
        fs.PLAN_V2[0] = True
        try:
            fs.plan_taped(k, 360, F - 166, 0.34)                                     # on the counter, below her face
        finally:
            fs.PLAN_V2[0] = False
        monitor(k, 300, F - 176, 1.0)                                                # beside her, turned to her
        fs.counter_plate(k, 470, F - 176)
        mfs.knitting(k, 522, F - 160, 0.36); mfs.mug(k, 548, F - 192, 0.5); mfs.candy(k, 430, F - 170, 0.55)
        c.restore()
        if people:
            sb.client(k, *HOME["client"], "stand", "confident", (0.9, 0))
            fs.robot_finger(k, *HOME["robot"])
            sfs.sofia(k, *HOME["sofia"], "hold", "charm", look=(0.6, -0.2))
            sb.DON_STATE[0] = ("up", "up")
            try:
                sb.don(k, *HOME["don"], "stand", "neutral", (-1, 0))
            finally:
                sb.DON_STATE[0] = None
        ac.shredder(k, SHRED[0], SHRED[1], SHRED[2], fill=0.4)


def sheet_set(d):
    S = 1.25
    W1, H1 = int(WW * S), int(960 * S)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W1 + 40, H1 + 240)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    corp(c, "FIRST SEARCH  ·  set v3: the master set, clean", 20, 52, 32, brand.NAVY, True)
    wrap(c, "940 wide, three zones with one job each, depth in three planes. Some of episode 9's blue confetti is "
            "still in the corners. DON's office door is in C, next to Mom's end of the counter: she guards it.",
         20, 86, 17, W1)
    c.save(); c.translate(20, 130); c.scale(S, S); c.rectangle(0, 0, WW, 960); c.clip()
    draw_set(k)
    for z, name, x0, x1, col in ZONES:
        c.set_source_rgba(*col, 0.12); c.rectangle(x0, F + 40, x1 - x0, 120); c.fill()
        c.set_source_rgb(*col); c.select_font_face("Inter", 0, 1); c.set_font_size(34); c.move_to(x0 + 12, F + 86)
        c.show_text(z); c.set_font_size(15); c.move_to(x0 + 46, F + 82); c.show_text(name)
    c.restore()
    y = 130 + H1 + 30
    for t in ("Back plane: the counter (Pam left with her monitor and the plan; Mom right, her desk), DON's door, "
              "the screen, the portrait.",
              "Middle: the Client at the door, the robot at its station, Sofía. Front: Don under the portrait, the "
              "shredder at the counter's left end.",
              "Mom's way out front: round the counter's LEFT end, past the shredder, into B."):
        wrap(c, "·  " + t, 20, y, 16, W1, (0.2, 0.2, 0.25)); y += 24
    out = os.path.join(d, "fs_set_v3.png"); s.write_to_png(out); return out


# ---------------------------------------------------------------- the top-down plan
DEPTH = {"client": 150, "robot": 175, "sofia": 140, "don": 215, "pam": 40, "mom": 40}
COL = {"client": (0.42, 0.44, 0.24), "robot": (0.4, 0.42, 0.5), "sofia": (0.86, 0.20, 0.55),
       "don": (0.13, 0.16, 0.30), "pam": (0.40, 0.26, 0.55), "mom": (0.13, 0.55, 0.58)}
SETUPS = {"S1": ("master, far front", 280, 420, (280, 140)),
          "S2": ("A, front left", 170, 330, (150, 150)),
          "S3": ("B, front", 450, 320, (450, 180)),
          "S4": ("B, low, close under Don", 500, 270, (474, 150)),
          "S5": ("C, front right", 720, 320, (720, 60)),
          "S6": ("B-C, the counter's end", 590, 320, (590, 120))}
PLAN = [  # shot, zone, setup, size, subject
    ("1.1a", "A+B", "S1", "wide", "red zero; the portrait jumps"), ("1.1b", "A+B", "S1", "wide", "the bonk on Don"),
    ("1.2", "A", "S2", "medium-wide", "the Client comes in; Sofía flirts"), ("1.3", "B", "S3", "two-shot", "Don's sales smile"),
    ("2.1", "B", "S3", "close", "Don: the calendar"), ("2.2", "A+B", "S3", "medium three", "the tablet in Don's hand"),
    ("2.3", "—", "insert", "insert", "the Client's thumb"), ("3.1", "B", "S3", "medium", "red again: the duck"),
    ("3.2", "—", "insert", "insert", "PAID $999"), ("3.3", "B", "S3", "two-shot", "It found nothing."),
    ("3.4", "B", "S3", "close", "the plaster"), ("4.1", "B", "S3", "medium", "make the zero green?"),
    ("4.2", "A", "S2", "medium", "the robot: approval"), ("4.3", "—", "insert", "insert", "APPROVED"),
    ("4.4", "—", "insert", "insert", "Pam's tape"), ("4.5", "A", "S2", "close", "the sweep to green"),
    ("5.1", "A+B", "S2", "medium three", "the Client at the green zero"), ("5.2", "B", "S4", "low", "Where's my blueprint?"),
    ("5.2b", "B", "S3", "close", "his eyes dart to the shredder"), ("5.2c", "—", "flashback", "insert", "episode 9: the shredder"),
    ("5.3", "B+C", "S6", "two-shot", "The zero's green.; Pam's plan held up"), ("6.1", "A+B", "S2", "medium-wide", "the photo"),
    ("6.1b", "C", "S5", "close", "Mom: Machines."), ("6.2a", "—", "insert", "insert", "the post, LinkedIn's manner"),
    ("6.2b", "—", "insert", "insert", "the comments"), ("7.1", "C", "S5", "close", "Mom: Young man."),
    ("7.2", "B+C", "S6", "two-shot", "Mom comes round; the men step back"), ("7.3", "—", "insert", "insert", "the lick"),
    ("7.4", "B", "S3", "two-shot", "the hair; Eww."), ("7.5", "B+C", "S6", "medium three", "That hussy.; Pam's hand"),
    ("8.1", "B+C", "S6", "medium-wide", "Pam has a plan."), ("8.2", "C", "S6", "medium", "the near-shred"),
    ("9.1", "A", "S2", "close", "100% COMPLETE"), ("9.2", "A", "S2", "close", "RETRY UNTIL FRIDAY"),
    ("9.3", "B", "S3", "close", "the plaster drops"), ("9.4", "A+B", "S1", "wide", "frame 0")]


def plan_room(c, ox, oy, sc, people=None, arrows=(), note=None):
    """The front desk from above. y grows towards the camera (the back wall at y=0, the front at y=260)."""
    c.save(); c.translate(ox, oy); c.scale(sc, sc)
    c.set_source_rgb(0.93, 0.90, 0.84); c.rectangle(0, 0, WW, 260); c.fill()
    for z, name, x0, x1, col in ZONES:
        c.set_source_rgba(*col, 0.08); c.rectangle(x0, 0, x1 - x0, 260); c.fill()
        c.set_source_rgb(*col); c.select_font_face("Inter", 0, 1); c.set_font_size(26); c.move_to(x0 + 8, 252)
        c.show_text(z)
    c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(0, 0); c.line_to(WW, 0); c.stroke()
    c.set_font_size(12)
    for x0, w, lab, col in ((40, 100, "glass door", (0.55, 0.75, 0.85)), (26, 162, "screen (over the door)", None),
                            (420, 108, "OUR FIRST CLIENT", (0.76, 0.60, 0.24)), (876, 60, "DON's office", (0.62, 0.44, 0.28))):
        if col:
            c.set_source_rgb(*col); c.rectangle(x0, -10, w, 10); c.fill()
        c.set_source_rgb(0.25, 0.25, 0.3); c.move_to(x0, -16 if lab != "screen (over the door)" else -30); c.show_text(lab)
    c.set_source_rgb(0.84, 0.74, 0.58); c.rectangle(576, 22, 290, 34); c.fill()                       # the counter
    c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(576, 22, 290, 34); c.stroke()
    c.set_source_rgb(0.25, 0.25, 0.3); c.move_to(640, 44); c.show_text("the counter")
    c.set_source_rgb(0.5, 0.52, 0.58); c.rectangle(SHRED[0] - 16, 66, 32, 26); c.fill()                # the shredder
    c.set_source_rgb(0.25, 0.25, 0.3); c.move_to(SHRED[0] - 30, 106); c.show_text("shredder")
    for (x0, w) in ((4, 60), (560, 24)):
        c.set_source_rgb(0.30, 0.55, 0.95)
        for i in range(10):
            c.rectangle(x0 + (i * 7) % w, 230 - (i * 5) % 18 if x0 < 100 else 70 + (i * 3) % 10, 5, 2); c.fill()
    for who, (x, y) in (people or {}).items():
        c.set_source_rgb(*COL[who]); c.arc(x, y, 15, 0, 6.3); c.fill()
        c.set_source_rgb(1, 1, 1); c.set_font_size(13); e = c.text_extents(who[0].upper())
        c.move_to(x - e.x_advance / 2, y + 5); c.show_text(who[0].upper())
    for (x0, y0, x1, y1, col) in arrows:
        c.set_source_rgb(*col); c.set_line_width(3); c.set_dash([8, 5]); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
        c.set_dash([]); a = math.atan2(y1 - y0, x1 - x0)
        c.move_to(x1, y1); c.line_to(x1 - 14 * math.cos(a - 0.4), y1 - 14 * math.sin(a - 0.4))
        c.line_to(x1 - 14 * math.cos(a + 0.4), y1 - 14 * math.sin(a + 0.4)); c.close_path(); c.fill()
    c.restore()


def home_people():
    return {w: (HOME[w][0], DEPTH[w]) for w in HOME}


def sheet_plan(d):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1700, 1880)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    corp(c, "FIRST SEARCH  ·  shot plan v1: the room from above, six camera setups", 30, 52, 32, brand.NAVY, True)
    wrap(c, "Circles: home positions (C Client, R robot, S Sofía, D Don, P Pam, M Mom). Cameras: the setups below "
            "the front of the room, each aimed at what it frames. Every shot uses one setup (or is an insert).",
         30, 86, 17, 1640)
    plan_room(c, 40, 160, 1.7, home_people())
    sc, ox, oy = 1.7, 40, 160
    for key, (name, cx, cy, (tx, ty)) in SETUPS.items():                     # the cameras
        X, Y = ox + cx * sc, oy + cy * sc
        TX, TY = ox + tx * sc, oy + ty * sc
        c.set_source_rgba(0.1, 0.1, 0.15, 0.55); c.set_line_width(2); c.move_to(X, Y); c.line_to(TX, TY); c.stroke()
        c.save(); c.translate(X, Y); c.rotate(math.atan2(TY - Y, TX - X) + math.pi / 2)
        c.set_source_rgb(0.12, 0.12, 0.16); c.rectangle(-14, -9, 28, 20); c.fill()
        c.move_to(-8, -9); c.line_to(-14, -20); c.line_to(14, -20); c.line_to(8, -9); c.fill(); c.restore()
        c.set_source_rgb(0.12, 0.12, 0.16); c.select_font_face("Inter", 0, 1); c.set_font_size(16)
        c.move_to(X - 16, Y + 36); c.show_text(key)
    y = 160 + int(470 * sc) + 20
    c.select_font_face("Inter", 0, 1); c.set_font_size(15)
    for i, (key, (name, *_)) in enumerate(SETUPS.items()):
        c.set_source_rgb(0.12, 0.12, 0.16); c.move_to(40 + (i % 3) * 540, y + (i // 3) * 24)
        c.show_text("%s  %s" % (key, name))
    y += 70
    t = {r["shot"]: r for r in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         "../first-search/fs_timing_v16.json")))}
    cols = [40, 110, 190, 270, 420, 500]
    for j, h in enumerate(("shot", "zone", "setup", "size", "at · s", "what we see")):
        c.set_source_rgb(*brand.NAVY); c.move_to(cols[j], y); c.show_text(h)
    y += 8
    c.set_font_size(14)
    for i, (sh, zone, setup, size, what) in enumerate(PLAN):
        yy = y + 22 + i * 22
        if i % 2 == 0:
            c.set_source_rgba(0, 0, 0, 0.04); c.rectangle(30, yy - 16, 1640, 22); c.fill()
        zc = ZCOL.get(zone[0], (0.45, 0.45, 0.5))
        r = t.get(sh)
        vals = (sh, zone, setup, size, "%.1f · %.1f" % (r["start"], r["len"]) if r else "", what)
        for j, v in enumerate(vals):
            c.set_source_rgb(*(zc if j in (0, 1) else (0.15, 0.15, 0.2))); c.move_to(cols[j], yy); c.show_text(v)
    out = os.path.join(d, "fs_shotplan_v1.png"); s.write_to_png(out); return out


# ---------------------------------------------------------------- Mom's beat, step by step
STEPS = [
    ("6.1b · 7.1", "Mom at her end of the counter (C), by DON's door; the camera S5 close on her. 6.1b: the flash "
     "from B, she glares across at the robot. 7.1: his post on her phone; \"Young... man.\"",
     {"mom": (800, 40), "pam": (668, 40), "don": (474, 215), "client": (420, 190), "sofia": (384, 140), "robot": (232, 175)}, []),
    ("7.2", "She comes out: round the counter's LEFT end, past the shredder, into B (dashed). The Client (by Don) and "
     "Don step back from her. Camera S6 at the counter's end: Mom entering frame right, the two men left.",
     {"mom": (540, 140), "pam": (668, 40), "don": (450, 225), "client": (380, 205), "sofia": (330, 140), "robot": (232, 175)},
     [(800, 64, 572, 64, (0.13, 0.55, 0.58)), (566, 72, 545, 125, (0.13, 0.55, 0.58))]),
    ("7.3 · 7.4", "7.3, insert: the lick. 7.4: she stands at Don's right, between him and the counter; Sofía at his "
     "left. Camera S3: Sofía | Don | Mom, the counter and Pam behind Mom.",
     {"mom": (512, 205), "pam": (668, 40), "don": (474, 215), "client": (380, 205), "sofia": (420, 175), "robot": (232, 175)},
     []),
    ("7.5", "On her way back to C she stops at the counter's end and turns on Sofía, who followed to the edge of B. "
     "Her hand finds Pam's on the counter's end. Camera S6: Sofía left, Mom centre, Pam behind the counter right.",
     {"mom": (580, 90), "pam": (620, 40), "don": (474, 215), "client": (380, 205), "sofia": (510, 130), "robot": (232, 175)},
     [(512, 205, 575, 100, (0.13, 0.55, 0.58))]),
    ("8.1", "Pam comes out round the same end with the plan, to Don (dashed); Mom, at the end, points after her: "
     "\"Pam has a plan.\" Don's eyes on Sofía. Camera S6, wider.",
     {"mom": (580, 90), "pam": (520, 170), "don": (474, 215), "client": (300, 190), "sofia": (430, 140), "robot": (232, 175)},
     [(620, 60, 540, 160, (0.40, 0.26, 0.55))]),
]


def sheet_blocking(d):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1700, 2120)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    corp(c, "FIRST SEARCH  ·  blocking v1: Mom's beat, 6.1b to 8.1", 30, 52, 32, brand.NAVY, True)
    wrap(c, "The test: an animator can stage 7.2 without asking where Mom came from, where she stands or what the "
            "camera sees. Her way out: round the counter's LEFT end (the right end is DON's door).", 30, 86, 17, 1640)
    y = 130
    for title, text, ppl, arrows in STEPS:
        corp(c, title, 30, y + 26, 24, (0.13, 0.55, 0.58), True)
        plan_room(c, 230, y, 0.82, ppl, arrows)
        wrap(c, text, 1020, y + 30, 16, 650, (0.15, 0.15, 0.2))
        y += 260 * 0.82 + 170
    out = os.path.join(d, "fs_blocking7_v1.png"); s.write_to_png(out); return out


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    os.makedirs(d, exist_ok=True)
    print(sheet_set(d)); print(sheet_plan(d)); print(sheet_blocking(d))
