"""v1, pinned. THE BEST CANDIDATE: storyboard v1, from interview script v4 (87 s). Still key frames, one per shot, drawn on the
set (bc_set v2) in 540 x 960 with the lines as speech bubbles. No motion and no voices yet: SHOTS gives each shot's
time span, camera and drawing function, so the animatic can be built on the same list.
Don's question is the same words three times; its bubble is big, then normal, then small.
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
    world(k, "chair", d)


def s04(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k, "write", "curious", look=(-1, 0.1)); don(k, look=(-0.2, 1.0))
        S.table(k, phone="still")
    world(k, "sofia", d)
    bubble(k, "Three degrees?", sp("sofia", MOUTH["sofia"]), 40, 34)


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


# ---------------------------------------------------------------- 2. the nice macho
def s09(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        cb.macho(k, X["chair"], S.FEET, 1.0, "sit", "smile", seated=True, glint=True)
        c = k.c                                                            # the chair complains
        c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)
        for sx in (-1, 1):
            for i in range(2):
                c.move_to(X["chair"] + sx * (62 + i * 10), S.CHAIR_SEAT + 30 + i * 14)
                c.line_to(X["chair"] + sx * (80 + i * 10), S.CHAIR_SEAT + 24 + i * 16); c.stroke()
    world(k, "chair", d)


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


def s11(k):
    def d():
        S.backdrop(k, 0.0, "idle", with_chair=False)
        sofia(k, "aside", "tiny", look=(-1, -0.5), lag=(-7, 0), blush=0.7)
        S.table(k, phone="still")
        cb.macho(k, X["sofia"] - 250, S.FEET + 22, 1.0, "pinch_low", "warm", look=(0.9, 0.5), pen=True)
    world(k, "macho_sofia", d)
    bubble(k, ["You dropped", "this."], sp("macho_sofia", (X["sofia"] - 250, S.FEET + 22 + cb.M_HY + 40)), 96, 30)
    bubble(k, "Thank you.", sp("macho_sofia", MOUTH["sofia"]), 790, 28, x=420)


def s12(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k, "aside", "smile", look=(-1, -0.4), blush=0.6, lag=(-5, 0))
        don(k, face="pout", look=(-1, 0.1), tense=True)
        pam(k, pb.POSE_WRITE, "peer", note="KIND", pen=True)
        S.table(k, phone="still")
    world(k, "chain", d)


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
    world(k, "macho_cu", d)
    bubble(k, ["Everybody makes", "mistakes. It's okay."], sp("macho_cu", MOUTH["macho"]), 96, 29)


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
        don(k, POSE_PUSH, "flat", look=(-1, -0.3), tense=True, board=None)
        pam(k, pb.POSE_LOWER, "dip", paddle="YES")
        S.table(k, phone="still")
    world(k, "panel", d)
    off_bubble(k, "No worries.", -1, 560, 26)
    off_bubble(k, ["Attractiveness is not", "protected. Proceed."], 1, 742, 22)


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
    world(k, "don", d)
    bubble(k, "Sorry.", sp("don", MOUTH["don"]), 60, 40)


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
    insert_phone(k, "missed")


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
    world(k, "panel", d)


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


def s39(k):
    world(k, "door", lambda: S.backdrop(k, 0.78, "clear"))


SHOTS = [
    # (id, section, t0, t1, draw, what happens, script rows)
    ("01", 0, 0.0, 1.5, s01, "The door opens. Frame 0, and the last frame.", "0.1"),
    ("02", 0, 1.5, 4.0, s02, "The client calls. Don turns the phone over.", "0.2"),
    ("03", 1, 4.0, 6.0, s03, "Feet off the floor, the CV on his knees.", "1.1"),
    ("04", 1, 6.0, 7.5, s04, "Sofía reads the cover.", "1.2"),
    ("05", 1, 7.5, 8.7, s05, "Three fingers. Optional.", "1.3"),
    ("06", 1, 8.7, 11.0, s06, "The question, flat and bored. Big bubble.", "1.4"),
    ("07", 1, 11.0, 13.0, s07, "The right answer.", "1.5"),
    ("08", 1, 13.0, 17.0, s08, "Two YES. A red cross, a finger at the door.", "1.6, 1.7"),
    ("09", 2, 17.0, 18.8, s09, "The chair creaks.", "2.1"),
    ("10", 2, 18.8, 20.0, s10, "Her one crack. The pen goes.", "2.2"),
    ("11", 2, 20.0, 23.2, s11, "Two fingertips, one pen. Too wide for the frame.", "2.3, 2.4"),
    ("12", 2, 23.2, 25.4, s12, "The camera pans along the table: she looks at him, Don at her, Pam at Don. KIND.", "2.5"),
    ("13", 2, 25.4, 27.6, s13, "The question, pointed. Normal bubble.", "2.6"),
    ("14", 2, 27.6, 29.8, s14, "He comforts him.", "2.7"),
    ("15", 2, 29.8, 31.2, s15, "Her paddle is up early. His smile dies.", "2.8"),
    ("16", 2, 31.2, 33.4, s16, "He says it to her. She answers.", "2.9, 2.10, 2.11"),
    ("17", 2, 33.4, 35.0, s17, "One finger on her paddle. Pam watches Don.", "2.12"),
    ("18", 3, 35.0, 36.6, s18, "A sweet old lady. One curler.", "3.1, 3.3"),
    ("19", 3, 36.6, 38.0, s19, "Bolt upright. The doodle face down.", "3.2"),
    ("20", 3, 38.0, 40.0, s20, "She sits. The chair fits. One look at Don.", "3.3"),
    ("20b", 3, 40.0, 43.0, s20b, "The robot asks. She answers.", "3.4, 3.5"),
    ("21", 3, 43.0, 45.0, s21, "Cut off mid-question. Two seconds.", "3.6, 3.7"),
    ("22", 3, 45.0, 48.4, s22, "The one question that would catch it.", "3.8, 3.9"),
    ("23", 3, 48.4, 51.0, s23, "The question, half the voice. Small bubble.", "3.10"),
    ("24", 3, 51.0, 53.0, s24, "Her eyes open.", "3.11"),
    ("25", 3, 53.0, 54.0, s25, "Before he can stop himself.", "3.12"),
    ("26", 3, 54.0, 56.4, s26, "The longest pause. Pam turns; Sofía has seen it.", "3.13"),
    ("27", 3, 56.4, 57.6, s27, "She looks at the phone. Then at him.", "3.14"),
    ("28", 3, 57.6, 60.0, s28, "He says it to the client. First call in 47.", "3.15"),
    ("29", 3, 60.0, 62.0, s29, "As if nothing had happened.", "3.16"),
    ("30", 4, 62.0, 66.0, s30, "The stamp. His catchphrase, very small.", "4.1, 4.2"),
    ("31", 5, 66.0, 68.0, s31, "A handshake she ignores. She has seen the vest.", "5.1"),
    ("32", 5, 68.0, 69.4, s32, "The tissue.", "5.2"),
    ("33", 5, 69.4, 71.0, s33, "Brief.", "5.3"),
    ("34", 5, 71.0, 75.4, s34, "The frame the film holds.", "5.4, 5.5"),
    ("35", 5, 75.4, 78.0, s35, "He leans away. She does not look up.", "5.6"),
    ("36", 5, 78.0, 80.0, s36, "His chair is empty between them.", "5.7"),
    ("37", 6, 80.0, 83.0, s37, "Folding the tissue.", "6.1, 6.2"),
    ("38", 6, 83.0, 85.4, s38, "Horror.", "6.3"),
    ("39", 6, 85.4, 87.0, s39, "The door begins to open. Cut to 01.", "6.4"),
]
DURATION = SHOTS[-1][3]


def frame(c, x, y, w, draw):
    """Draw one shot into a w-wide 9:16 box at (x, y)."""
    c.save(); c.translate(x, y); c.scale(w / 540.0, w / 540.0)
    c.rectangle(0, 0, 540, 960); c.clip()
    c.set_source_rgb(*kit.WALL); c.paint()
    draw(kit.Ctx(c, 0))
    c.restore()
