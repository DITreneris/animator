"""v2, pinned. THE BEST CANDIDATE: storyboard v2, from interview script v4 (85 s, 52 shots). Still key frames, one per shot, drawn
on the set (bc_set v2) in 540 x 960 with the lines as speech bubbles. SHOTS gives each shot's time span and drawing
function, so the animatic can be built on the same list.
v2, after the director's audit of v1 (bc_sb_v1.py = v1, kept): the lines are unchanged; the camera is not.
  Each candidate gets a framing of his own. The small one is small in a tall frame, and we look up at the panel over
  the back of his head. The macho is drawn bigger than life and cropped by the frame. Mom is level and still, and it
  is Don who shrinks. These are cut-out cheats (size, crop, a foreground head), not redrawn perspective.
  New inserts: the dangling feet, the red cross, the chair legs, the pen at his boot, Don's eyes (twice: jealous, then
  afraid), the paddle, the phone full screen, the tissue on the stain.
  Both rejected candidates now get their exit. Don is seen walking round the table before the reveal. The vest hold is
  three cuts. One tilted close-up, on "He's applying for your job."
Don's question is the same words on the same camera three times; its bubble is big, then normal, then small.
Sections: 0 cold open, 1 the small one, 2 the nice macho, 3 Mom, 4 the verdict, 5 the reveal, 6 the father."""
import math
import cairo
import kit
import bc_set_v2 as S
import cand_bc as cb
import don_bc as db
import don_mf as dm
import mom_bc as mb
import pam_bc as pb
import sofia_bc as sb
import robot_mf as rm
import props_bc as props
from kit import INK, cut, rect, ellipse

X = S.POS
W, H = 540, 960
MOUTH = {"sofia": (X["sofia"], S.SEAT + sb.HY + 34), "don": (X["don"], S.SEAT + db.HY + 30),
         "pam": (X["pam"], S.SEAT + pb.HY + 30), "small": (X["chair"], 558), "macho": (X["chair"], 486),
         "mom": (X["chair"], 526)}
HEAD = {id(MOUTH["sofia"]): 112, id(MOUTH["don"]): 98, id(MOUTH["pam"]): 106, id(MOUTH["small"]): 124,
        id(MOUTH["macho"]): 106, id(MOUTH["mom"]): 136}  # mouth to the top of the hair or the hat, world px
DON_X, MOM_X = X["chair"] + 126, X["chair"] + 14          # where they stand for the reveal
POSE_POINT_L = (-75, -95) + dm.ik(1, 30, db.BT + 84)        # the finger at the door, under Sofia's chin; the list in the other hand
POSE_PHONE = (-8, 0) + dm.ik(1, 47, db.HY + 8)              # the phone at his ear
POSE_HAND_OUT = (-82, -8, 8, 0)                             # a handshake offered to screen left
POSE_PUSH = dm.ik(-1, -96, db.BT - 50) + (8, 0)             # one finger on Sofia's paddle
CAM = {"low": (335, 452, 1.22),                            # the small one, small in a tall frame
       "feet": (335, 716, 3.4), "pov": (745, 590, 1.8), "exit": (236, 452, 1.22),
       "loom": (335, 528, 2.25), "loom_line": (335, 512, 1.9),   # the macho, cropped by the frame
       "legs": (335, 700, 2.5), "boot": (296, 738, 3.8), "tower": (520, 655, 1.25),
       "eyes": (825, S.SEAT + db.HY - 2, 6.0), "paddle": (765, 480, 1.9), "don_small": (825, 640, 1.5),
       "round": (570, 500, 0.86), "stain": (446, 556, 3.4),
       "tilt": (DON_X + 4, S.FEET + db.HY + 20, 2.9, 0.13)}   # the one dutch angle


def world(k, cam, draw):
    c = k.c
    c.save(); S.with_cam(c, S.CAMS[cam] if isinstance(cam, str) else cam); draw(); c.restore()


_AIM = [None]                                              # (camera zoom, head height) of the last sp() call


def sp(cam, pt, dy=0):
    """A world point (usually a mouth) on screen. It also tells the next bubble how big that head is on screen, so
    the tail can stop at the hair or the chin and never cross the face."""
    cam = S.CAMS[cam] if isinstance(cam, str) else cam
    x, y = S.to_screen(cam, pt[0], pt[1])
    _AIM[0] = (cam[2], HEAD.get(id(pt), 100))
    return x, y + dy


def bubble(k, lines, tip, y, size=30, kind="normal", x=None):
    """A speech bubble in screen space. lines: one string or a list. tip: where the tail points (screen x, y).
    kind: big / normal / small (thin, wobbly) / shout. x: the bubble's centre (default: above the tip)."""
    c = k.c
    if isinstance(lines, str):
        lines = [lines]
    size = {"big": 40, "normal": size, "small": 24, "shout": 40}[kind]
    c.select_font_face(kit.FONT); c.set_font_size(size)
    ws = [c.text_extents(t).x_advance for t in lines]
    bw, bh = max(ws) + 44, len(lines) * size * 1.12 + 26
    cx = tip[0] if x is None else x
    bx = max(12, min(W - 12 - bw, cx - bw / 2))
    tx = max(bx + 30, min(bx + bw - 30, tip[0]))
    up = tip[1] < y
    base = y + 3 if up else y + bh - 3
    pts = kit.rough_rect_pts(k, bx, y, bw, bh, 900 + len(lines[0]), j=3.4 if kind == "small" else 1.6)
    aim, _AIM[0] = _AIM[0], None
    if aim:                                                # stop short of the face: at the hair from above, the chin from below
        vx, vy = tip[0] - tx, tip[1] - base
        ln = math.hypot(vx, vy) or 1.0
        l2 = max(24.0, min(ln - aim[0] * (34 if up else aim[1]), 120.0))
        tip = (tx + vx * l2 / ln, base + vy * l2 / ln)
    tail = [(tx - 13, base), (tip[0], tip[1]), (tx + 13, base)]
    lw = {"shout": 4.2, "small": 1.8}.get(kind, 2.6)
    cut(k, tail, (1, 1, 1), lw=lw)
    cut(k, pts, (1, 1, 1), lw=lw)
    c.move_to(*tail[0]); c.line_to(*tail[1]); c.line_to(*tail[2]); c.close_path(); c.set_source_rgb(1, 1, 1); c.fill()
    c.select_font_face(kit.FONT); c.set_font_size(size); c.set_source_rgb(*INK)
    for i, t in enumerate(lines):
        c.move_to(bx + (bw - ws[i]) / 2, y + 13 + size * 0.86 + i * size * 1.12); c.show_text(t)


def off_bubble(k, lines, side, y, size=26):
    """A line from someone out of frame: the tail points at the frame edge."""
    bubble(k, lines, (W - 4 if side > 0 else 4, y + 60), y, size, x=W - 150 if side > 0 else 150)


def insert_phone(k, state, buzz=True):
    """The client's phone as an insert, bottom left."""
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.18); c.arc(104, 818, 112, 0, 2 * math.pi); c.fill()
    props.phone(k, 100, 812, 1.05, state, buzz)


def head_from_behind(k, x, y, r=118):
    """The back of the small one's head, in the foreground (screen space): we look up with him."""
    hair = tuple(v * 0.62 for v in cb.S_HAIR)
    pts = []
    n = 9
    for i in range(n + 1):                                 # a fan of spikes over the dome
        a0 = math.pi * (1.0 + i / n)
        pts.append((x + math.cos(a0) * r, y + math.sin(a0) * r * 0.92))
        if i < n:
            a1 = math.pi * (1.0 + (i + 0.5) / n)
            lift = 1.42 if i % 2 == 0 else 1.26
            pts.append((x + math.cos(a1) * r * lift, y + math.sin(a1) * r * lift))
    pts += [(x + r, 980), (x - r, 980)]
    for sx in (-1, 1):                                     # ears, and the pencil behind one of them
        ellipse(k, x + sx * (r + 4), y + 34, 17, 26, tuple(v * 0.7 for v in db.SKIN), 940 + sx, shadow=False, lw=2.6)
    cut(k, pts, hair, lw=3.2)
    cut(k, [(x + r - 4, y + 4), (x + r + 12, y - 2), (x + r + 46, y - 96), (x + r + 30, y - 102)], (0.93, 0.74, 0.20), lw=2.4)


def wood(k):
    """A table top filling the frame, for inserts (screen space)."""
    c = k.c
    rect(k, -20, -20, 580, 1000, S.ts.WOOD, 930, shadow=False, outline=False)
    c.set_source_rgb(*S.ts.WOOD_DARK); c.set_line_width(3)
    for y in (250, 700):
        c.move_to(-10, y); c.line_to(550, y + 14); c.stroke()


def eye_slit(k, draw):
    """Don's eyes and nothing else: a band across a dark frame (screen space). Used twice, jealous and then afraid."""
    c = k.c
    rect(k, -20, -20, 580, 1000, (0.07, 0.08, 0.12), 933, shadow=False, outline=False)
    c.save(); c.rectangle(0, 348, 540, 264); c.clip()
    world(k, CAM["eyes"], draw)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(5)
    for y in (348, 612):
        c.move_to(0, y); c.line_to(540, y); c.stroke()


def ticks(k, pts, lw=3.0):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(lw); c.set_line_cap(1)
    for x0, y0, x1, y1 in pts:
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()


# ---------------------------------------------------------------- the panel
def sofia(k, pose="write", face="neutral", look=(-1, 0), **kw):
    o = {}
    S.seated(k, lambda: o.update(sb.sofia(k, X["sofia"], S.SEAT, 1.0, pose, face, look=look, **kw)))
    return o


def don(k, pose=None, face="flat", look=(-0.6, 0.9), **kw):
    o = {}
    pose = db.POSE_PEN if pose is None else pose
    kw.setdefault("board", "front" if pose is db.POSE_PEN else None)
    S.seated(k, lambda: o.update(db.don(k, X["don"], S.SEAT, 1.0, pose, face, look=look, **kw)))
    return o


def pam(k, pose=None, face="neutral", look=(-1, 0), **kw):
    o = {}
    S.seated(k, lambda: o.update(pb.pam(k, X["pam"], S.SEAT, 1.0, pb.POSE_TABLE if pose is None else pose, face, look=look,
                                        **kw)))
    return o


def robot(k):
    rm.robot(k, X["robot"], S.FEET_BACK, 1.0, "stand", "eager", seed=97)


# ---------------------------------------------------------------- 0. cold open
def s01(k):
    world(k, "door", lambda: S.backdrop(k, 0.78, "idle"))


def s02(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k); don(k, face="smug", look=(-0.2, 1.0)); pam(k)
        S.table(k, phone="buzz")
    world(k, "don", d)
    insert_phone(k, "missed")
    bubble(k, "First candidate.", sp("don", MOUTH["don"]), 34, 34)


# ---------------------------------------------------------------- 1. the small one
def s03(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        cb.small(k, X["chair"], S.CHAIR_SEAT, 1.0, "hug", "hopeful", cv=True, seated=True, look=(0.7, -0.2))
    world(k, CAM["low"], d)



def s03b(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        cb.small(k, X["chair"], S.CHAIR_SEAT, 1.0, "hug", "hopeful", cv=True, seated=True, look=(0.7, -0.2))
        ticks(k, [(X["chair"] - 50, 722, X["chair"] - 62, 716), (X["chair"] - 50, 734, X["chair"] - 64, 736),
                  (X["chair"] + 50, 722, X["chair"] + 62, 716), (X["chair"] + 50, 734, X["chair"] + 64, 736)], 1.2)
    world(k, CAM["feet"], d)


def s04(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k, "write", "curious", look=(-0.8, 0.9)); don(k, look=(-0.2, 1.0))
        S.table(k, phone="still")
    world(k, CAM["pov"], d)
    rect(k, -20, 752, 580, 240, S.ts.WOOD, 931, shadow=False, outline=False)   # from down here the table is a wall
    head_from_behind(k, 196, 900)
    bubble(k, "Three degrees?", sp(CAM["pov"], MOUTH["sofia"]), 36, 34, x=170)


def s05(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        cb.small(k, X["chair"], S.CHAIR_SEAT, 1.0, "finger", "proud", seated=True, look=(0.7, -0.1))
    world(k, "small_cu", d)
    bubble(k, "And a half.", sp("small_cu", MOUTH["small"]), 96, 34)


def s06(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k); don(k, look=(-0.2, 1.0)); pam(k)
        S.table(k, phone="buzz")
    world(k, "don", d)
    bubble(k, ["What if I made", "a mistake?"], sp("don", MOUTH["don"]), 22, kind="big")


def s07(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        cb.small(k, X["chair"], S.CHAIR_SEAT, 1.0, "hug", "proud", cv=True, seated=True, look=(0.7, -0.1))
    world(k, "small_cu", d)
    bubble(k, ["I'd show you", "the data."], sp("small_cu", MOUTH["small"]), 80, 34)


def s08(k):
    def d():
        S.backdrop(k, 0.0, "proceed_height")
        sofia(k, "paddle", "neutral", paddle="YES")
        o = don(k, POSE_POINT_L, "flat", look=(-1.0, 0.7), tense=True)
        pam(k, pb.POSE_YES, "dip", paddle="YES")
        S.table(k, phone="still")
        props.clipboard(k, o["hands"][1][0] + 2, o["hands"][1][1] - 26, 0.9, 0.08, 91, side="front", marks=1)
        ellipse(k, o["hands"][1][0], o["hands"][1][1] + 8, 10, 10, db.SKIN, 92, shadow=False, lw=2)
        hx, hy = o["hands"][0]
        rect(k, hx - 22, hy - 4, 19, 8, db.SKIN, 94, shadow=False, lw=2)
    world(k, "panel", d)
    bubble(k, "Too short.", sp("panel", MOUTH["don"]), 610, 34)
    off_bubble(k, ["Height is not", "protected. Proceed."], 1, 742, 24)



def s08b(k):
    wood(k)
    props.clipboard(k, 262, 520, 7.0, -0.05, 91, side="front", marks=1)
    props.ballpen(k, 384, 462, 5.0, math.pi - 0.62)                      # the pen, just lifting off the cross



def s08c(k):
    def d():
        S.backdrop(k, 0.55, "proceed_height")
        cb.small(k, 262, S.FEET, 1.0, "hug", "crushed", cv=True, look=(-0.4, 0.8))
    world(k, CAM["exit"], d)


# ---------------------------------------------------------------- 2. the nice macho
def s09(k):
    def d():
        S.backdrop(k, 0.0, "idle", with_poster=False)
        cb.macho(k, X["chair"], S.FEET, 1.0, "wave", "smile", glint=True)
    world(k, CAM["loom"], d)


def bent_chair(k, x):
    """The candidate's chair under him: the seat sags, the legs bow out."""
    col, dark = (0.36, 0.39, 0.46), (0.22, 0.23, 0.27)
    y0, y1 = S.CHAIR_SEAT + 20, S.FEET + 4
    for sx in (-1, 1):
        cut(k, [(x + sx * 40, y0), (x + sx * 50, y0), (x + sx * 76, (y0 + y1) / 2), (x + sx * 84, y1), (x + sx * 74, y1),
                (x + sx * 64, (y0 + y1) / 2)], dark, lw=2)
    cut(k, [(x - 58, S.CHAIR_SEAT + 4), (x + 58, S.CHAIR_SEAT + 4), (x + 54, S.CHAIR_SEAT + 22), (x, S.CHAIR_SEAT + 30),
            (x - 54, S.CHAIR_SEAT + 22)], col, lw=2.2)


def s09b(k):
    def d():
        S.backdrop(k, 0.0, "idle", with_chair=False, with_poster=False)
        bent_chair(k, X["chair"])
        cb.macho(k, X["chair"], S.FEET, 1.0, "sit", "smile", seated=True)
        ticks(k, [(X["chair"] - 92, 690, X["chair"] - 108, 682), (X["chair"] - 94, 706, X["chair"] - 112, 706),
                  (X["chair"] + 92, 690, X["chair"] + 108, 682), (X["chair"] + 94, 706, X["chair"] + 112, 706)], 1.6)
        kit.text(k, "creak", X["chair"] - 76, 762, 15, INK, font="Permanent Marker", rot=-0.12)
    world(k, CAM["legs"], d)


def s10(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k, "chest", "flustered", look=(-1, -0.1), lag=(11, 0))
        S.table(k, phone="still")
        props.pen(k, X["sofia"] - 96, S.TABLE_TOP + 46, 1.0, 1.9)             # on its way to the floor
        c = k.c
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
        c.new_path(); c.arc(X["sofia"] - 62, S.TABLE_TOP + 48, 44, math.pi * 1.05, math.pi * 1.5); c.stroke()
    world(k, "sofia", d)



def s10b(k):
    def d():
        S.backdrop(k, 0.0, "idle", with_chair=False, with_poster=False)
        cb.macho(k, X["chair"], S.FEET, 1.0, "sit", "smile", seated=True)
        props.pen(k, X["chair"] - 78, S.FEET + 6, 0.8, 0.12)                   # it stops at his boot
        ticks(k, [(X["chair"] - 104, S.FEET - 4, X["chair"] - 96, S.FEET - 1), (X["chair"] - 108, S.FEET + 12, X["chair"] - 98, S.FEET + 11)], 0.9)
    world(k, CAM["boot"], d)


def s11(k):
    mx, mf, ms = X["sofia"] - 292, S.FEET + 96, 1.3                         # nearer to us, so bigger than life
    def d():
        S.backdrop(k, 0.0, "idle", with_chair=False, with_poster=False)
        sofia(k, "aside", "tiny", look=(-1, -0.8), lag=(-7, 0), blush=0.7)
        S.table(k, phone="still")
        cb.macho(k, mx, mf, ms, "pinch_low", "warm", look=(0.9, 0.6), pen=True)
    world(k, CAM["tower"], d)
    bubble(k, ["You dropped", "this."], sp(CAM["tower"], (mx + 40, mf + (cb.M_HY + 40) * ms)), 120, 30, x=390)
    bubble(k, "Thank you.", sp(CAM["tower"], MOUTH["sofia"]), 620, 28, x=430)


def s12(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k, "aside", "smile", look=(-1, -0.4), blush=0.6, lag=(-5, 0))
        don(k, face="pout", look=(-1, 0.1), tense=True)
        pam(k, pb.POSE_WRITE, "peer", note="KIND", pen=True)
        S.table(k, phone="still")
    world(k, "chain", d)



def s12b(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        don(k, face="pout", look=(-1, 0.1), tense=True)
    eye_slit(k, d)


def s13(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k, "aside", "smile", look=(-1, -0.4), blush=0.5)
        o = don(k, (-104, 6) + dm.ik(1, 30, db.BT + 84), "pout", look=(-1.0, 0.1), tense=True)
        pam(k, face="peer")
        S.table(k, phone="buzz")
        hx, hy = o["hands"][0]
        props.ballpen(k, hx - 30, hy + 2, 1.0, math.pi / 2 + 0.05)
        ellipse(k, hx, hy, 10, 10, db.SKIN, 95, shadow=False, lw=2)
    world(k, "don", d)
    bubble(k, ["And you. What if", "I made a mistake?"], sp("don", MOUTH["don"]), 30, 31)


def s14(k):
    def d():
        S.backdrop(k, 0.0, "idle", with_poster=False)                       # the poster is cheated out of his close-up
        cb.macho(k, X["chair"], S.FEET, 1.0, "sit", "warm", seated=True, look=(0.8, 0.1))
    world(k, CAM["loom_line"], d)
    bubble(k, ["Everybody makes", "mistakes. It's okay."], sp(CAM["loom_line"], MOUTH["macho"]), 28, 29)


def s15(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k, "paddle", "smile", look=(-1, -0.3), paddle="YES", blush=0.6)
        don(k, face="drop", look=(-1, 0.0))
        S.table(k, phone="still")
    world(k, "sofia_don", d)
    bubble(k, "That's so true.", sp("sofia_don", MOUTH["sofia"]), 700, 30, x=170)


def s16(k):
    def d():
        S.backdrop(k, 0.0, "proceed_looks")
        sofia(k, "aside", "eyebrow", look=(1, 0))
        don(k, face="pout", look=(-1, 0.0), tense=True, marks=2)
        S.table(k, phone="still")
    world(k, "sofia_don", d)
    bubble(k, "Too distracting.", sp("sofia_don", MOUTH["don"]), 690, 30, x=386)
    bubble(k, "For whom?", sp("sofia_don", MOUTH["sofia"]), 790, 30, x=140)


def s17(k):
    def d():
        S.backdrop(k, 0.0, "proceed_looks")
        sofia(k, "paddle", "unimpressed", look=(1, -0.2), paddle="YES")
        o = don(k, dm.ik(-1, -94, db.BT - 100) + (8, 0), "flat", look=(-1, -0.3), tense=True, board=None)
        S.table(k, phone="still")
        hx, hy = o["hands"][0]
        rect(k, hx - 5, hy + 4, 9, 22, db.SKIN, 953, shadow=False, lw=2)       # one fingertip on the rim
        ticks(k, [(hx - 34, hy + 14, hx - 34, hy + 30), (hx + 30, hy + 14, hx + 30, hy + 30)], 1.6)
    world(k, CAM["paddle"], d)
    off_bubble(k, ["Attractiveness is not", "protected. Proceed."], 1, 760, 24)


def s17b(k):
    def d():
        S.backdrop(k, 0.0, "proceed_looks", with_poster=False)
        cb.macho(k, X["chair"], S.FEET, 1.0, "shrug", "gracious", look=(0.8, 0.1))
    world(k, CAM["loom_line"], d)
    bubble(k, "No worries.", sp(CAM["loom_line"], MOUTH["macho"]), 28, 32)


# ---------------------------------------------------------------- 3. Mom
def s18(k):
    def d():
        S.backdrop(k, 0.9, "idle")
        mb.mom(k, X["door"] + 22, S.FLOOR_Y + 52, 0.96, "bag", "sweet")
    world(k, "door", d)
    bubble(k, ["Good morning,", "everyone."], sp("door", (X["door"] + 22, S.FLOOR_Y + 52 - 264 * 0.96)), 36, 28, x=170)


def s19(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        don(k, db.POSE_HIDE, "panic", look=(-1, 0.1), board="back", tense=True)
    eye_slit(k, d)


def s19b(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k); don(k, db.POSE_HIDE, "sheepish", look=(-1, 0.2), board="back", tense=True); pam(k)
        S.table(k, phone="still")
    world(k, "don", d)


def s20(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        S.mom_on_chair(k, pose="bag", face="sweet")
    world(k, "chair", d)


def s20b(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        S.mom_on_chair(k, pose="bag", face="sweet")
    world(k, "mom_cu", d)
    bubble(k, ["Forty years. One", "very difficult client."], sp("mom_cu", MOUTH["mom"]), 10, 27)
    off_bubble(k, "Experience?", 1, 700, 26)


def s21(k):
    def d():
        S.backdrop(k, 0.0, "ageism")
        sofia(k, "ask", "flustered", look=(0.6, -0.9), blush=0.0)
        don(k, db.POSE_HIDE, "sheepish", look=(-1, 0.2), board="back", tense=True)
        S.table(k, phone="still")
    world(k, "sofia_don", d)
    bubble(k, ["Where do you see", "yourself in five—"], sp("sofia_don", MOUTH["sofia"]), 700, 26, x=170)


def s22(k):
    def d():
        S.backdrop(k, 0.0, "family")
        don(k, db.POSE_HIDE, "sheepish", look=(1, 0.3), board="back", tense=True)
        pam(k, pb.POSE_ASK, "probe", mouth="E", pen=True, lean=-3)
        S.table(k, phone="still")
    world(k, "don_pam", d)
    bubble(k, ["Any family in", "the company?"], sp("don_pam", MOUTH["pam"]), 700, 27, x=380)


def s23(k):
    def d():
        S.backdrop(k, 0.0, "family")
        sofia(k); don(k, db.POSE_HIDE, "sheepish", look=(-0.4, 1.0), board="back", tense=True, mouth="O"); pam(k)
        S.table(k, phone="buzz")
    world(k, "don", d)
    insert_phone(k, "missed")
    bubble(k, ["What if I…", "made a mistake?"], sp("don", MOUTH["don"]), 60, kind="small")


def s24(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        S.mom_on_chair(k, pose="bag", face="stern", look=(0.9, 0.0))
    world(k, "mom_cu", d)
    bubble(k, ["I'd make you", "apologize."], sp("mom_cu", MOUTH["mom"]), 10, 32)


def s25(k):
    def d():
        S.backdrop(k, 0.0, "family")
        sofia(k); don(k, db.POSE_STRAIGHT, "obey", look=(-1, 0.1), tense=True); pam(k)
        S.table(k, phone="buzz")
    world(k, CAM["don_small"], d)                                          # the same man, a smaller frame
    bubble(k, "Sorry.", sp(CAM["don_small"], MOUTH["don"]), 110, 30)


def s26(k):
    def d():
        S.backdrop(k, 0.0, "family")
        sofia(k, "fold", "sideeye", look=(1, 0))
        don(k, db.POSE_STRAIGHT, "obey", look=(-1, 0.1), tense=True)
        pam(k, face="frozen", look=(-1, 0))
        S.table(k, phone="buzz")
    world(k, "panel", d)


def s27(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        S.mom_on_chair(k, pose="bag", face="stern", look=(0.9, 0.8))
    world(k, "mom_cu", d)


def s27b(k):
    c = k.c
    wood(k)
    props.phone(k, 244, 430, 3.5, "missed", True, rot=-0.05)
    cut(k, [(560, 640), (430, 700), (452, 800), (560, 800)], db.BLAZER, lw=3)   # his hand, not yet on it
    cut(k, [(432, 700), (452, 800), (438, 806), (418, 708)], (0.96, 0.96, 0.94), lw=2.4)
    ellipse(k, 392, 762, 44, 36, db.SKIN, 951, lw=3)
    rect(k, 334, 742, 46, 17, db.SKIN, 952, shadow=False, lw=2.6)
    ticks(k, [(318, 716, 304, 704), (300, 748, 282, 746), (316, 782, 300, 792)], 3)


def s28(k):
    def d():
        S.backdrop(k, 0.0, "family")
        sofia(k)
        o = don(k, POSE_PHONE, "obey", look=(-1, 0.1), tense=True)
        pam(k)
        S.table(k)                                                         # the phone is at his ear
        hx, hy = o["hands"][1]
        rect(k, hx - 9, hy - 26, 18, 34, (0.10, 0.10, 0.13), 96, shadow=False, lw=2)
        ellipse(k, hx + 3, hy + 2, 10, 10, db.SKIN, 97, shadow=False, lw=2)
    world(k, "don", d)
    insert_phone(k, "answered", buzz=False)
    bubble(k, "Sorry.", sp("don", MOUTH["don"]), 60, 40)


def s29(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        S.mom_on_chair(k, pose="bag", face="sweet")
    world(k, "mom_cu", d)
    bubble(k, "Good.", sp("mom_cu", MOUTH["mom"]), 26, 40)


# ---------------------------------------------------------------- 4. the verdict
def s30(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        sofia(k, "fold", "sideeye", look=(1, 0)); don(k, db.POSE_STRAIGHT, "obey", tense=True); pam(k, face="frozen")
        S.table(k, phone="still")
    world(k, "monitor", d)
    S.hired_stamp(k, 270, 868, 1.4, -0.07, paper=True)                                 # stamped across the table front
    off_bubble(k, ["She made him answer", "the client. Hired."], 1, 40, 26)
    bubble(k, "…Approved.", sp("monitor", MOUTH["don"]), 730, kind="small", x=300)



def s30b(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        sofia(k, "fold", "sideeye", look=(-1, 0)); pam(k, face="frozen")
        S.table(k, phone="still")
        mb.mom(k, MOM_X, S.FEET, 1.0, "bag", "sweet", look=(0.9, 0.1))
        db.don(k, 512, S.FEET + 8, 1.0, POSE_HAND_OUT, "sheepish", look=(-1, 0.1), tense=True, lean=-5)
        ticks(k, [(566, 560, 590, 560), (570, 600, 600, 600), (566, 640, 590, 640)], 3.2)
    world(k, CAM["round"], d)


# ---------------------------------------------------------------- 5. the reveal
def _two(k, don_kw, mom_kw, state="clear"):
    def d():
        S.backdrop(k, 0.0, state)
        db.don(k, DON_X, S.FEET, 1.0, **don_kw)
        mb.mom(k, MOM_X, S.FEET, 1.0, **mom_kw)
    return d


def s31(k):
    world(k, "reveal", _two(k, dict(pose=POSE_HAND_OUT, face="sheepish", look=(-1, 0.1), tense=True),
                            dict(pose="bag", face="stern", look=(0.9, 0.9), bag=True)))
    bubble(k, "Welcome ab—", sp("reveal", (DON_X, S.FEET + db.HY + 30)), 330, 28, x=420)


def s32(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        mb.mom(k, MOM_X, S.FEET, 1.0, "lick", "stern", look=(1.0, 0.4))
    world(k, (MOM_X + 14, 452, 2.15), d)


def s33(k):
    world(k, "reveal", _two(k, dict(pose="stand", face="obey", tense=True),
                            dict(pose="hip", face="shout", look=(0.9, 0.4), thrust=0.7, bag=False)))
    bubble(k, ["DONNIE!", "Your vest!"], sp("reveal", (MOM_X, S.FEET + mb.HY + 30)), 264, kind="shout", x=404)


def s34(k):
    world(k, CAM["stain"], _two(k, dict(pose="stand", face="obey", tense=True),
                                dict(pose=mb.wipe_at(DON_X - MOM_X - 21, db.BT + 96), face="stern", look=(0.9, 0.9), bag=False)))


def s34b(k):
    world(k, "reveal", _two(k, dict(pose="stand", face="obey", tense=True),
                            dict(pose=mb.wipe_at(DON_X - MOM_X - 21, db.BT + 96), face="stern", look=(0.9, 0.9), bag=False)))


def s35(k):
    world(k, "reveal", _two(k, dict(pose="stand", face="obey", tense=True, lean=7, look=(1, 0.2)),
                            dict(pose=mb.wipe_at(DON_X - MOM_X - 14, db.BT + 60), face="stern", look=(0.9, 0.9), bag=False)))


def s36(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        sofia(k, "fold", "deadpan")
        pam(k, face="approve", look=(-1, 0))
        S.table(k, phone="still")
    world(k, "chain", d)


# ---------------------------------------------------------------- 6. the father and the loop
def s37(k):
    world(k, "reveal", _two(k, dict(pose="stand", face="obey", tense=True, look=(-1, 0)),
                            dict(pose="hip", face="stern", look=(0.9, 0.2), bag=False)))
    bubble(k, ["Donnie. Your father", "is parking."], sp("reveal", (MOM_X, S.FEET + mb.HY + 30)), 800, 26, x=170)
    bubble(k, "Why?", sp("reveal", (DON_X, S.FEET + db.HY + 30)), 330, 32, x=440)


def s38(k):
    world(k, "reveal", _two(k, dict(pose="stand", face="panic", tense=True, look=(-1, 0)),
                            dict(pose="hip", face="unimpressed", look=(0.9, 0.2), bag=False)))
    bubble(k, ["He's applying", "for your job."], sp("reveal", (MOM_X, S.FEET + mb.HY + 30)), 800, 30, x=170)



def s38b(k):
    world(k, CAM["tilt"], _two(k, dict(pose="stand", face="panic", tense=True, look=(-1, 0)),
                               dict(pose="hip", face="unimpressed", look=(0.9, 0.2), bag=False)))


def s39(k):
    world(k, "door", lambda: S.backdrop(k, 0.78, "clear"))


SHOTS = [
    # (id, section, t0, t1, draw, what happens, script rows, v2 status: new / changed / "")
    ("01", 0, 0.0, 1.5, s01, 'The door opens. Frame 0, and the last frame.', "0.1", ""),
    ("02", 0, 1.5, 4.0, s02, 'The client calls. Don turns the phone over.', "0.2", ""),
    ("03", 1, 4.0, 5.4, s03, 'Small in a tall frame. Feet off the floor, the CV on his knees.', "1.1", "changed"),
    ("04", 1, 5.4, 5.9, s03b, 'Insert: the feet do not reach.', "1.1", "new"),
    ("05", 1, 5.9, 7.4, s04, 'We look up with him. The table is a wall. Don has not looked.', "1.2", "changed"),
    ("06", 1, 7.4, 8.6, s05, 'Three fingers. Optional.', "1.3", ""),
    ("07", 1, 8.6, 10.9, s06, 'The question, flat and bored. Big bubble.', "1.4", ""),
    ("08", 1, 10.9, 12.9, s07, 'The right answer.', "1.5", ""),
    ("09", 1, 12.9, 15.9, s08, 'Two YES. The monitor says proceed. A finger at the door.', "1.6, 1.7", ""),
    ("10", 1, 15.9, 16.4, s08b, 'Insert: the red cross.', "1.6", "new"),
    ("11", 1, 16.4, 17.4, s08c, 'Hold on his face. He carries the CV out.', "1.7", "new"),
    ("12", 2, 17.4, 18.4, s09, 'Too big for the frame. A small hello.', "2.1", "changed"),
    ("13", 2, 18.4, 19.2, s09b, 'Insert: he sits. The chair legs bow.', "2.1", "new"),
    ("14", 2, 19.2, 20.3, s10, 'Her one crack. The pen goes.', "2.2", ""),
    ("15", 2, 20.3, 20.8, s10b, 'Insert: it stops at his boot.', "2.2", "new"),
    ("16", 2, 20.8, 23.5, s11, 'He towers. Two fingertips, one pen. She looks up.', "2.3, 2.4", "changed"),
    ("17", 2, 23.5, 25.3, s12, 'Along the table: she looks at him, Don at her, Pam at Don. KIND.', "2.5", ""),
    ("18", 2, 25.3, 25.9, s12b, "Punch in: Don's eyes. Jealous before he speaks.", "2.5", "new"),
    ("19", 2, 25.9, 28.1, s13, 'The question, pointed. Same camera, normal bubble.', "2.6", ""),
    ("20", 2, 28.1, 30.3, s14, 'He fills the frame and comforts him.', "2.7", "changed"),
    ("21", 2, 30.3, 31.7, s15, 'Her paddle is up early. His smile dies.', "2.8", ""),
    ("22", 2, 31.7, 33.9, s16, 'He says it to her. She answers.', "2.9, 2.10", ""),
    ("23", 2, 33.9, 35.7, s17, 'Close: one fingertip pushes her YES down. The monitor says proceed.', "2.11, 2.12", "changed"),
    ("24", 2, 35.7, 36.7, s17b, 'He takes it kindly and goes.', "2.12", "new"),
    ("25", 3, 36.7, 38.3, s18, 'A sweet old lady. One curler.', "3.1, 3.3", ""),
    ("26", 3, 38.3, 38.9, s19, 'Punch in: the same eyes, afraid.', "3.2", "new"),
    ("27", 3, 38.9, 39.7, s19b, 'Bolt upright. The doodle face down.', "3.2", ""),
    ("28", 3, 39.7, 41.7, s20, 'Level and still. Her feet reach; the chair does not creak.', "3.3", ""),
    ("29", 3, 41.7, 44.7, s20b, 'The robot asks. She answers.', "3.4, 3.5", ""),
    ("30", 3, 44.7, 46.7, s21, 'Cut off mid-question. Two seconds.', "3.6, 3.7", ""),
    ("31", 3, 46.7, 50.1, s22, 'The one question that would catch it.', "3.8, 3.9", ""),
    ("32", 3, 50.1, 52.7, s23, 'The question, half the voice. Same camera, small bubble.', "3.10", ""),
    ("33", 3, 52.7, 54.7, s24, 'Her eyes open.', "3.11", ""),
    ("34", 3, 54.7, 55.7, s25, 'A smaller Don behind a bigger table.', "3.12", "changed"),
    ("35", 3, 55.7, 58.1, s26, 'The longest pause. Pam turns; Sofía has seen it.', "3.13", ""),
    ("36", 3, 58.1, 58.7, s27, 'She looks at the phone. Then at him.', "3.14", "changed"),
    ("37", 3, 58.7, 59.5, s27b, 'Insert, full screen: 47 missed calls. His hand does not want to.', "3.14", "new"),
    ("38", 3, 59.5, 61.7, s28, 'He says it to the client. First call in 47.', "3.15", ""),
    ("39", 3, 61.7, 63.7, s29, 'As if nothing had happened.', "3.16", ""),
    ("40", 4, 63.7, 66.9, s30, 'No bias detected. The stamp. His catchphrase, very small.', "4.1, 4.2", ""),
    ("41", 5, 66.9, 68.0, s30b, 'He comes round the table. His chair is empty behind him.', "5.1", "new"),
    ("42", 5, 68.0, 69.8, s31, 'A handshake she ignores. She has seen the vest.', "5.1", ""),
    ("43", 5, 69.8, 71.0, s32, 'The tissue.', "5.2", ""),
    ("44", 5, 71.0, 72.6, s33, 'Brief.', "5.3", ""),
    ("45", 5, 72.6, 73.2, s34, 'Insert: the tissue lands on the ketchup.', "5.4", "new"),
    ("46", 5, 73.2, 74.8, s34b, 'She scrubs. He stands still for it.', "5.4, 5.5", ""),
    ("47", 5, 74.8, 75.8, s36, 'Cut away: his empty chair between them. Sofía looks at us.', "5.7", "changed"),
    ("48", 5, 75.8, 77.8, s35, 'Back: he leans away, she pulls him in by the lapel.', "5.6", ""),
    ("49", 6, 77.8, 80.8, s37, 'Folding the tissue.', "6.1, 6.2", ""),
    ("50", 6, 80.8, 82.4, s38, 'She says it like the weather.', "6.3", ""),
    ("51", 6, 82.4, 83.4, s38b, 'The one tilted frame: his world, not the room.', "6.3", "new"),
    ("52", 6, 83.4, 85.0, s39, 'The door begins to open. Level again. Cut to 01.', "6.4", ""),
]
DURATION = SHOTS[-1][3]


def frame(c, x, y, w, draw):
    """Draw one shot into a w-wide 9:16 box at (x, y)."""
    c.save(); c.translate(x, y); c.scale(w / 540.0, w / 540.0)
    c.rectangle(0, 0, 540, 960); c.clip()
    c.set_source_rgb(*kit.WALL); c.paint()
    draw(kit.Ctx(c, 0))
    c.restore()
