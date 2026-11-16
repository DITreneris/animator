"""The board as animation v2 used it, pinned.
THE BEST CANDIDATE: storyboard v3, from interview script v5 (86 s, 64 panels). Still key frames drawn on the set
(bc_set v3) in 540 x 960, the lines as speech bubbles. SHOTS gives each panel's time span and drawing function, so the
animatic can be built on the same list. bc_sb_v1.py and bc_sb_v2.py are the earlier boards, kept.

v3 is the bubble pass, by the series' lessons (docs/lessons.md) and checked by qa_bc.py:
  - one speaker to a panel; panels with two lines are split. The speaker's mouth is open, every other mouth is shut;
  - a bubble sits BESIDE the face at mouth height with a short tail to the cheek wherever there is clear wall there
    (the candidates sit left of centre for it); in a tight shot it sits just ABOVE the speaker's own head with a short
    tail down. No long tails, and no tail across a face;
  - a repeated line keeps its spot: Don's question is in the same place three times, big, then normal, then small;
  - a bubble never covers a face, a sign, the monitor or a prop that is being read, and stays inside the app's safe
    zones (out of the top 10 %, the bottom 15 % and the right 12 %); text is 22 px or more at 540 wide;
  - a sign is whole in the frame or not in it: no cropped posters, notices or monitors;
  - the robot speaks in a mono face on a tinted bubble, and is on screen whenever it has a line the monitor does
    not show (its first ruling, "Experience?", the verdict); its other rulings are read off the monitor;
  - what must be read in a prop is a full-screen insert (the phone, the list, the stamp), never a corner inset.
New lines in script v5: Mom says "Good boy." and "Donnie. Father is coming." (script v6: "Father is parking.")
Also fixed from the v2 self-review: the robot is on screen; the pen hand-over is a single of the macho and a close-up
of Sofia; Don leaves the table in the three-shot; the feet and chair inserts are reframed.
Sections: 0 cold open, 1 the small one, 2 the nice macho, 3 Mom, 4 the verdict, 5 the reveal, 6 the father."""
import math
import cairo
import kit
import bc_set as S
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
SAFE = (20, 96, 475, 816)                                  # where a label may sit: x0, y0, x1, y1
MONO = "DejaVu Sans Mono"
MOM_X, DON_X = X["chair"] + 14, X["chair"] + 126          # where they stand for the reveal
# half the face's width at mouth height, and the top of the hair or hat above the mouth (world px at scale 1)
FACE = {"sofia": (42, 100), "don": (52, 84), "pam": (38, 86), "small": (40, 112), "macho": (46, 105),
        "mom": (52, 106), "robot": (48, 86)}
# signs on the wall and the table, as drawn (world boxes): a frame holds each of them whole or not at all
LABELS = {"poster": (253, 166, 449, 292), "notice": (150, 259, 244, 373), "monitor": (681, 164, 968, 315),
          "sign": (1085, 237, 1216, 289), "nameplate": (736, 612, 828, 640)}
POSE_POINT_L = (-75, -95) + dm.ik(1, 30, db.BT + 84)        # the finger at the door, under Sofia's chin; the list in the other hand
POSE_PHONE = (-8, 0) + dm.ik(1, 47, db.HY + 8)              # the phone at his ear
POSE_HAND_OUT = (-82, -8, 8, 0)                             # a handshake offered to screen left

db.MOUTH_FIX = True                                        # Don's "flat" and "sheepish" mouths are drawn (see don_bc)
BUBBLES = True                                             # qa_bc.py turns them off to find what they cover
HEADS, QA = {}, {"faces": [], "labels": [], "bubbles": []}
_BASE = [None]


def _to540(k, x, y):
    """A point in the current drawing space, in 540 x 960 frame coordinates."""
    return _BASE[0].transform_point(*k.c.user_to_device(x, y))


def _box540(k, x0, y0, x1, y1):
    p = [_to540(k, x, y) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    return min(q[0] for q in p), min(q[1] for q in p), max(q[0] for q in p), max(q[1] for q in p)


def head(k, name, x, my, s=1.0):
    """Register a head just drawn (inside the camera transform): mouth at (x, my). Bubbles and the QA read it."""
    r, top = FACE[name]
    mx, mY = _to540(k, x, my)
    ex, ey = _to540(k, x + 1, my)
    z = math.hypot(ex - mx, ey - mY) * s                   # screen px per unit of this character
    HEADS[name] = {"m": (mx, mY), "R": r * z, "top": mY - top * z}
    QA["faces"].append((name, _box540(k, x - (r - 5) * s, my - 56 * s, x + (r - 5) * s, my + 10 * s)))


def world(k, cam, draw):
    c = k.c
    cam = S.CAMS[cam] if isinstance(cam, str) else cam
    c.save(); S.with_cam(c, cam)
    for name, b in LABELS.items():
        QA["labels"].append((name, _box540(k, *b)))
    draw(); c.restore()


# ---------------------------------------------------------------- bubbles
def bubble(k, lines, who, form="T", size=30, kind="normal", dx=0, dy=0, gap=20, mono=False, at=None):
    """One speaker's line. who: a head registered in this frame. form:
      "R" / "L"  beside the face at mouth height, a short tail to the cheek (the default wherever the wall is clear);
      "T"        just above the speaker's own head, a short tail straight down (tight shots);
      "off"      the speaker is out of frame to the right (the robot): at = (x, y), the tail goes to the edge.
    kind: normal / big / small (thin, wobbly) / shout. The box is kept inside SAFE."""
    c = k.c
    if isinstance(lines, str):
        lines = [lines]
    c.select_font_face(MONO if mono else kit.FONT, cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if mono else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    ws = [c.text_extents(t).x_advance for t in lines]
    lh = size * 1.12
    bw, bh = max(ws) + 44, len(lines) * lh + 26
    if form == "off":
        bx, by = at
        mx = my = R = top = None
    else:
        h = HEADS[who]
        (mx, my), R, top = h["m"], h["R"], h["top"]
        if form in ("R", "L"):
            sd = 1 if form == "R" else -1
            bx = mx + R + gap if sd > 0 else mx - R - gap - bw
            by = my - bh / 2
        else:
            bx, by = mx - bw / 2, top - gap - bh
    bx, by = bx + dx, by + dy
    bx = max(SAFE[0], min(SAFE[2] - bw, bx)); by = max(SAFE[1], min(SAFE[3] - bh, by))
    if form in ("R", "L"):
        ex = bx + 3 if sd > 0 else bx + bw - 3
        ty = max(by + 15, min(by + bh - 15, my))
        tip = (mx + sd * (R + 3), my)
        tail = [(ex, ty - 11), tip, (ex, ty + 11)]
    elif form == "T":
        rx = max(bx + 28, min(bx + bw - 28, mx))
        tip = (max(rx - 10, min(rx + 10, mx)), top - 3)
        tail = [(rx - 12, by + bh - 3), tip, (rx + 12, by + bh - 3)]
    else:
        tip = (W - 5, by + bh / 2 + 16)
        tail = [(bx + bw - 3, by + bh / 2 - 11), tip, (bx + bw - 3, by + bh / 2 + 11)]
    QA["bubbles"].append({"who": who, "form": form, "box": (bx, by, bx + bw, by + bh), "tip": tip, "size": size,
                          "text": " ".join(lines), "tail": math.hypot(tip[0] - (tail[0][0] + tail[2][0]) / 2,
                                                                      tip[1] - (tail[0][1] + tail[2][1]) / 2),
                          "head": None if form == "off" else {"m": (mx, my), "R": R, "top": top}})
    if not BUBBLES:
        return
    fill = (0.90, 0.96, 1.0) if mono else (1, 1, 1)
    lw = {"shout": 4.4, "small": 1.8, "big": 3.0}.get(kind, 2.6)
    pts = kit.rough_rect_pts(k, bx, by, bw, bh, 900 + len(lines[0]), j=3.4 if kind == "small" else 1.6)
    cut(k, tail, fill, lw=lw)
    cut(k, pts, fill, lw=lw)
    c.move_to(*tail[0]); c.line_to(*tail[1]); c.line_to(*tail[2]); c.close_path(); c.set_source_rgb(*fill); c.fill()
    c.select_font_face(MONO if mono else kit.FONT, cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if mono else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size); c.set_source_rgb(*(S.NAVY if mono else INK))
    for i, t in enumerate(lines):
        c.move_to(bx + (bw - ws[i]) / 2, by + 13 + size * 0.86 + i * lh); c.show_text(t)


# ---------------------------------------------------------------- the cast, each registering its head
def sofia(k, pose="write", face="neutral", look=(-1, 0), **kw):
    o = {}
    S.seated(k, lambda: o.update(sb.sofia(k, X["sofia"], S.SEAT, 1.0, pose, face, look=look, **kw)))
    head(k, "sofia", X["sofia"], S.SEAT + sb.HY + 34)
    return o


def don(k, pose=None, face="flat", look=(-0.6, 0.9), **kw):
    o = {}
    pose = db.POSE_PEN if pose is None else pose
    kw.setdefault("board", "front" if pose is db.POSE_PEN else None)
    S.seated(k, lambda: o.update(db.don(k, X["don"], S.SEAT, 1.0, pose, face, look=look, **kw)))
    head(k, "don", X["don"], S.SEAT + db.HY + 30)
    return o


def pam(k, pose=None, face="neutral", look=(-1, 0), **kw):
    o = {}
    S.seated(k, lambda: o.update(pb.pam(k, X["pam"], S.SEAT, 1.0, pb.POSE_TABLE if pose is None else pose, face, look=look,
                                        **kw)))
    head(k, "pam", X["pam"], S.SEAT + pb.HY + 30)
    return o


def don_up(k, x, pose, face, feet=None, **kw):
    feet = S.FEET if feet is None else feet
    o = db.don(k, x, feet, 1.0, pose, face, **kw)
    head(k, "don", x, feet + db.HY + 30)
    return o


def mom_up(k, x, feet, s, pose, face, **kw):
    o = mb.mom(k, x, feet, s, pose, face, **kw)
    head(k, "mom", x, feet + (mb.HY + 30) * s, s)
    return o


def mom_sit(k, **kw):
    S.mom_on_chair(k, **kw)
    head(k, "mom", X["chair"], 526)


def small(k, pose, face, x=None, seated=True, **kw):
    x = X["chair"] if x is None else x
    feet = S.CHAIR_SEAT if seated else S.FEET
    o = cb.small(k, x, feet, 1.0, pose, face, seated=seated, **kw)
    head(k, "small", x, feet - (80 if seated else 128))
    return o


def macho(k, pose, face, x=None, feet=None, s=1.0, seated=False, **kw):
    x = X["chair"] if x is None else x
    feet = S.FEET if feet is None else feet
    o = cb.macho(k, x, feet, s, pose, face, seated=seated, **kw)
    head(k, "macho", x, feet + (cb.M_HY + 40 + (56 if seated else 0)) * s, s)
    return o


def robot(k, pose="stand", talk=0.0):
    rm.robot(k, X["robot"], S.FEET_BACK, 1.0, pose, "eager", talk=talk, seed=97)
    head(k, "robot", X["robot"], S.FEET_BACK - 219)


def panel(k, state, so=None, do=None, pa=None, phone="still"):
    """The three at the table under the monitor. so / do / pa: keyword dicts for each; False leaves that seat empty
    (only when the seat is out of frame, or its owner has stood up). In a two-shot the third is cut by the edge."""
    S.backdrop(k, 0.0, state)
    out = [None, None, None]
    if so is not False:
        out[0] = sofia(k, **(so or {}))
    if do is not False:
        out[1] = don(k, **(do or {}))
    if pa is not False:
        out[2] = pam(k, **(pa or {}))
    S.table(k, phone=phone)
    return out


# ---------------------------------------------------------------- inserts and small helpers (screen space)
def wood(k):
    """A table top filling the frame, for inserts."""
    c = k.c
    rect(k, -20, -20, 580, 1000, S.ts.WOOD, 930, shadow=False, outline=False)
    c.set_source_rgb(*S.ts.WOOD_DARK); c.set_line_width(3)
    for y in (250, 700):
        c.move_to(-10, y); c.line_to(550, y + 14); c.stroke()


def ticks(k, pts, lw=3.0):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(lw); c.set_line_cap(1)
    for x0, y0, x1, y1 in pts:
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()


def phone_insert(k, state, hand):
    """The client's phone, full screen. hand: "flip" (Don turns it over), "hover" (he does not want to), None."""
    wood(k)
    props.phone(k, 244, 440, 3.5, state, state == "missed", rot=-0.05)
    k.c.new_path()
    if hand:
        hx, hy = (392, 762) if hand == "hover" else (398, 706)
        cut(k, [(560, hy - 122), (hx + 38, hy - 62), (hx + 60, hy + 38), (560, hy + 38)], db.BLAZER, lw=3)
        cut(k, [(hx + 40, hy - 62), (hx + 60, hy + 38), (hx + 46, hy + 44), (hx + 26, hy - 54)], (0.96, 0.96, 0.94), lw=2.4)
        ellipse(k, hx, hy, 44, 36, db.SKIN, 951, lw=3)
        rect(k, hx - 58, hy - 20, 46, 17, db.SKIN, 952, shadow=False, lw=2.6)
        if hand == "hover":
            ticks(k, [(hx - 74, hy - 46, hx - 88, hy - 58), (hx - 92, hy - 14, hx - 110, hy - 16), (hx - 76, hy + 20, hx - 92, hy + 30)])


def eye_slit(k, face, **kw):
    """Don's eyes and nothing else: a band across a dark frame. Used twice, jealous and then afraid."""
    c = k.c
    rect(k, -20, -20, 580, 1000, (0.07, 0.08, 0.12), 933, shadow=False, outline=False)
    c.save(); c.rectangle(0, 348, 540, 264); c.clip()

    def d():
        S.backdrop(k, 0.0, "idle")
        don(k, face=face, **kw)
    world(k, "eyes", d)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(5)
    for y in (348, 612):
        c.move_to(0, y); c.line_to(540, y); c.stroke()
    QA["labels"][:] = []                                   # nothing but his eyes is in this frame


def head_from_behind(k, x, y, r=118):
    """The back of the small one's head in the foreground: we look up with him."""
    hair = tuple(v * 0.62 for v in cb.S_HAIR)
    pts, n = [], 9
    for i in range(n + 1):
        a0 = math.pi * (1.0 + i / n)
        pts.append((x + math.cos(a0) * r, y + math.sin(a0) * r * 0.92))
        if i < n:
            a1 = math.pi * (1.0 + (i + 0.5) / n)
            lift = 1.42 if i % 2 == 0 else 1.26
            pts.append((x + math.cos(a1) * r * lift, y + math.sin(a1) * r * lift))
    pts += [(x + r, 980), (x - r, 980)]
    for sx in (-1, 1):
        ellipse(k, x + sx * (r + 4), y + 34, 17, 26, tuple(v * 0.7 for v in db.SKIN), 940 + sx, shadow=False, lw=2.6)
    cut(k, pts, hair, lw=3.2)
    cut(k, [(x + r - 4, y + 4), (x + r + 12, y - 2), (x + r + 46, y - 96), (x + r + 30, y - 102)], (0.93, 0.74, 0.20), lw=2.4)


def bent_chair(k, x):
    """The candidate's chair under him: the seat sags, the legs bow out."""
    col, dark = (0.36, 0.39, 0.46), (0.22, 0.23, 0.27)
    y0, y1 = S.CHAIR_SEAT + 20, S.FEET + 4
    for sx in (-1, 1):
        cut(k, [(x + sx * 40, y0), (x + sx * 50, y0), (x + sx * 76, (y0 + y1) / 2), (x + sx * 84, y1), (x + sx * 74, y1),
                (x + sx * 64, (y0 + y1) / 2)], dark, lw=2)
    cut(k, [(x - 58, S.CHAIR_SEAT + 4), (x + 58, S.CHAIR_SEAT + 4), (x + 54, S.CHAIR_SEAT + 22), (x, S.CHAIR_SEAT + 30),
            (x - 54, S.CHAIR_SEAT + 22)], col, lw=2.2)


# ---------------------------------------------------------------- 0. cold open
def s_door(k, state="idle"):
    world(k, "door", lambda: S.backdrop(k, 0.78, state))


def s_first(k):
    world(k, "don", lambda: panel(k, "idle", do=dict(face="smug", look=(-0.2, 1.0), mouth="E"), phone="buzz"))
    bubble(k, "First candidate.", "don", "T", 32)


def s_phone47(k):
    phone_insert(k, "missed", "flip")


# ---------------------------------------------------------------- 1. the small one
def s_small_low(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        small(k, "hug", "hopeful", cv=True, look=(0.7, -0.2))
    world(k, "low", d)


def s_feet(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        small(k, "hug", "hopeful", cv=True, look=(0.7, -0.2))
        cx = X["chair"]
        ticks(k, [(cx - 50, 722, cx - 62, 716), (cx - 50, 734, cx - 64, 736), (cx + 50, 722, cx + 62, 716),
                  (cx + 50, 734, cx + 64, 736)], 1.2)
    world(k, "feet", d)


def s_pov(k):
    world(k, "pov", lambda: panel(k, "idle", so=dict(pose="write", face="curious", look=(-0.8, 0.9)),
                                  do=dict(look=(-0.2, 1.0)), pa=False))
    rect(k, -20, 752, 580, 240, S.ts.WOOD, 931, shadow=False, outline=False)   # from down here the table is a wall
    head_from_behind(k, 196, 900)
    bubble(k, "Three degrees?", "sofia", "T", 34)


def s_half(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        small(k, "finger", "proud", look=(0.7, -0.1), mouth="E")
    world(k, "small_say", d)
    bubble(k, ["And", "a half."], "small", "R", 34, dy=34)


def s_q1(k):
    world(k, "don", lambda: panel(k, "idle", do=dict(look=(-0.2, 1.0), mouth="E"), phone="buzz"))
    bubble(k, ["What if I made", "a mistake?"], "don", "T", 36, kind="big")


def s_data(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        small(k, "hug", "proud", cv=True, look=(0.7, -0.1), mouth="E")
    world(k, "small_say", d)
    bubble(k, ["I'd show you", "the data."], "small", "R", 28)


def s_short(k):
    def d():
        S.backdrop(k, 0.0, "proceed_height")
        sofia(k, "paddle", "neutral", paddle="YES")
        o = don(k, POSE_POINT_L, "flat", look=(-1.0, 0.7), tense=True, mouth="O")
        p = pam(k, pb.pm.ik(-1, -58, pb.BT - 16) + (8, 0), "dip")           # her YES in the other hand: inside the frame
        hx, hy = p["hands"][0]
        props.paddle(k, hx, hy - 2, 0.9, -0.10, "YES", 130)
        S.table(k, phone="still")
        props.clipboard(k, o["hands"][1][0] + 2, o["hands"][1][1] - 26, 0.9, 0.08, 91, side="front", marks=1)
        ellipse(k, o["hands"][1][0], o["hands"][1][1] + 8, 10, 10, db.SKIN, 92, shadow=False, lw=2)
        hx, hy = o["hands"][0]
        rect(k, hx - 22, hy - 4, 19, 8, db.SKIN, 94, shadow=False, lw=2)
    world(k, "panel", d)
    bubble(k, "Too short.", "don", "T", 34)


def s_robot_height(k):
    def d():
        S.backdrop(k, 0.0, "proceed_height")
        robot(k, "present", talk=0.8)
        S.table(k, phone=None)
    world(k, "robot", d)
    bubble(k, ["Height is not", "protected.", "Proceed."], "robot", "T", 22, mono=True)


def s_cross(k):
    wood(k)
    props.clipboard(k, 262, 520, 7.0, -0.05, 91, side="front", marks=1)
    props.ballpen(k, 384, 462, 5.0, math.pi - 0.62)                      # the pen, just lifting off the cross


def s_small_out(k):
    def d():
        S.backdrop(k, 0.6, "proceed_height")
        small(k, "hug", "crushed", x=276, seated=False, cv=True, look=(-0.4, 0.8))
    world(k, "door", d)


# ---------------------------------------------------------------- 2. the nice macho
def s_loom(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        macho(k, "wave", "smile", glint=True)
    world(k, "loom", d)


def s_legs(k):
    def d():
        S.backdrop(k, 0.0, "idle", with_chair=False)
        bent_chair(k, X["chair"])
        macho(k, "sit", "smile", seated=True)
        cx = X["chair"]
        ticks(k, [(cx - 92, 690, cx - 108, 682), (cx - 94, 706, cx - 112, 706), (cx + 92, 690, cx + 108, 682),
                  (cx + 94, 706, cx + 112, 706)], 1.6)
        kit.text(k, "creak", cx - 76, 762, 15, INK, font="Permanent Marker", rot=-0.12)
    world(k, "legs", d)


def s_pen_goes(k):
    def d():
        panel(k, "idle", so=dict(pose="chest", face="flustered", look=(-1, -0.1), lag=(11, 0)), do=False, pa=False)
        props.pen(k, X["sofia"] - 96, S.TABLE_TOP + 46, 1.0, 1.9)             # on its way to the floor
        c = k.c
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
        c.new_path(); c.arc(X["sofia"] - 62, S.TABLE_TOP + 48, 44, math.pi * 1.05, math.pi * 1.5); c.stroke()
    world(k, "sofia", d)


def s_boot(k):
    def d():
        S.backdrop(k, 0.0, "idle", with_chair=False)
        macho(k, "sit", "smile", seated=True)
        cx = X["chair"]
        props.pen(k, cx - 78, S.FEET + 6, 0.8, 0.12)                            # it stops at his boot
        ticks(k, [(cx - 104, S.FEET - 4, cx - 96, S.FEET - 1), (cx - 108, S.FEET + 12, cx - 98, S.FEET + 11)], 0.9)
    world(k, "boot", d)


def s_dropped(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        macho(k, "pinch_near", "warm", look=(0.9, 0.3), pen=True, mouth="E")
    world(k, "loom_say", d)
    bubble(k, ["You dropped", "this."], "macho", "R", 26, dy=-44)


def s_thanks(k):
    def d():
        panel(k, "idle", so=dict(pose="aside", face="tiny", look=(-1, -0.8), lag=(-7, 0), blush=0.7, mouth="E"),
              do=False, pa=False)
        macho(k, "pinch_low", "warm", x=X["sofia"] - 292, feet=S.FEET + 96, s=1.3, look=(0.9, 0.6), pen=True)
    world(k, "sofia", d)
    del HEADS["macho"]; QA["faces"][:] = [f for f in QA["faces"] if f[0] != "macho"]   # only his hand is in the frame
    bubble(k, "Thank you.", "sofia", "T", 32)


def s_chain(k):
    world(k, "panel", lambda: panel(k, "idle", so=dict(pose="aside", face="smile", look=(-1, -0.4), blush=0.6, lag=(-5, 0)),
                                    do=dict(face="pout", look=(-1, 0.1), tense=True, mouth="M"),
                                    pa=dict(pose=pb.POSE_WRITE, face="peer", note="KIND", pen=True)))


def s_eyes_jealous(k):
    eye_slit(k, "pout", look=(-1, 0.1), tense=True, mouth="M")


def s_q2(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        sofia(k, "aside", "smile", look=(-1, -0.4), blush=0.5)
        o = don(k, (-104, 6) + dm.ik(1, 30, db.BT + 84), "pout", look=(-1.0, 0.1), tense=True, mouth="A")
        pam(k, face="peer")
        S.table(k, phone="buzz")
        hx, hy = o["hands"][0]
        props.ballpen(k, hx - 30, hy + 2, 1.0, math.pi / 2 + 0.05)
        ellipse(k, hx, hy, 10, 10, db.SKIN, 95, shadow=False, lw=2)
    world(k, "don", d)
    bubble(k, ["And you. What if", "I made a mistake?"], "don", "T", 30)


def s_okay(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        macho(k, "sit", "warm", seated=True, look=(0.8, 0.1), mouth="E")
    world(k, "macho_say", d)
    bubble(k, ["Everybody", "makes", "mistakes.", "It's okay."], "macho", "R", 26)


def s_true(k):
    world(k, "sofia_don", lambda: panel(k, "idle", so=dict(pose="paddle", face="smile", look=(-1, -0.3), paddle="YES",
                                                            blush=0.6, mouth="E"),
                                        do=dict(face="drop", look=(-1, 0.0), mouth="M"), pa=dict(face="peer")))
    bubble(k, "That's so true.", "sofia", "T", 30)


def s_distracting(k):
    world(k, "sofia_don", lambda: panel(k, "idle", so=dict(pose="aside", face="eyebrow", look=(1, 0)),
                                        do=dict(face="pout", look=(-1, 0.0), tense=True, marks=2, mouth="A"), pa=dict(face="peer")))
    bubble(k, "Too distracting.", "don", "T", 28)


def s_whom(k):
    world(k, "sofia_don", lambda: panel(k, "idle", so=dict(pose="aside", face="eyebrow", look=(1, 0), mouth="O"),
                                        do=dict(face="pout", look=(-1, 0.0), tense=True, marks=2, mouth="M"), pa=dict(face="peer")))
    bubble(k, "For whom?", "sofia", "T", 32)


def _push(k):
    S.backdrop(k, 0.0, "proceed_looks")
    sofia(k, "paddle", "unimpressed", look=(1, -0.2), paddle="YES")
    o = don(k, dm.ik(-1, -94, db.BT - 100) + (8, 0), "flat", look=(-1, -0.3), tense=True, board=None)
    pam(k, face="peer")                                                       # she watches him do it
    S.table(k, phone="still")
    hx, hy = o["hands"][0]
    rect(k, hx - 5, hy + 4, 9, 22, db.SKIN, 953, shadow=False, lw=2)           # one fingertip on the rim
    ticks(k, [(hx - 34, hy + 14, hx - 34, hy + 30), (hx + 30, hy + 14, hx + 30, hy + 30)], 1.6)


def s_push(k):
    world(k, "sofia_don", lambda: _push(k))


def s_push_cu(k):
    world(k, "paddle", lambda: _push(k))
    HEADS.clear(); QA["faces"][:] = []                                        # a detail: no whole face is in it


def s_no_worries(k):
    def d():
        S.backdrop(k, 0.0, "proceed_looks")
        macho(k, "shrug", "gracious", seated=True, look=(0.8, 0.1), mouth="E")
    world(k, "macho_say", d)
    bubble(k, "No worries.", "macho", "R", 30)


# ---------------------------------------------------------------- 3. Mom
def s_mom_door(k):
    def d():
        S.backdrop(k, 0.9, "idle")
        mom_up(k, X["door"] + 22, S.FLOOR_Y + 52, 0.96, "bag", "sweet", mouth="E")
    world(k, "door", d)
    bubble(k, ["Good morning,", "everyone."], "mom", "R", 26)


def s_eyes_afraid(k):
    eye_slit(k, "panic", pose=db.POSE_HIDE, look=(-1, 0.1), board="back", tense=True, mouth="M")


def s_upright(k):
    world(k, "don", lambda: panel(k, "idle", do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-1, 0.2), board="back",
                                                      tense=True)))


def _mom(k, cam, **kw):
    def d():
        S.backdrop(k, 0.0, "idle")
        mom_sit(k, **kw)
    world(k, cam, d)


def s_mom_sits(k):
    _mom(k, "mom", pose="bag", face="sweet")


def s_experience(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        robot(k, "stand", talk=0.8)
        S.table(k, phone=None)
    world(k, "robot", d)
    bubble(k, "Experience?", "robot", "T", 26, mono=True)


def s_forty(k):
    _mom(k, "mom", pose="bag", face="sweet", mouth="E")
    bubble(k, ["Forty years.", "One very", "difficult client."], "mom", "T", 26, dx=8)


def s_five(k):
    world(k, "sofia_don", lambda: panel(k, "idle", so=dict(pose="ask", face="neutral", look=(-1, 0.0), mouth="E"),
                                        do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-1, 0.2), board="back", tense=True),
                                        pa=dict()))
    bubble(k, ["Where do you see", "yourself in five—"], "sofia", "T", 25)


def s_ageism(k):
    world(k, "sofia_don", lambda: panel(k, "ageism", so=dict(pose="ask", face="flustered", look=(0.6, -0.9), blush=0.0),
                                        do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-1, 0.2), board="back", tense=True),
                                        pa=dict()))


def s_family_q(k):
    world(k, "don_pam", lambda: panel(k, "idle", so=dict(pose="ask", face="flustered", look=(0.6, -0.9), blush=0.0),
                                      do=dict(pose=db.POSE_HIDE, face="sheepish", look=(1, 0.3), board="back", tense=True),
                                      pa=dict(pose=pb.POSE_ASK, face="probe", mouth="E", pen=True, lean=-3)))
    bubble(k, ["Any family in", "the company?"], "pam", "T", 25)


def s_family(k):
    world(k, "don_pam", lambda: panel(k, "family", so=dict(pose="fold", face="neutral", look=(1, 0)),
                                      do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-0.4, 1.0), board="back", tense=True),
                                      pa=dict(pose=pb.POSE_ASK, face="frozen", pen=True)))


def s_q3(k):
    world(k, "don", lambda: panel(k, "family", do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-0.4, 1.0), board="back",
                                                        tense=True, mouth="O"), phone="buzz"))
    bubble(k, ["What if I…", "made a mistake?"], "don", "T", 24, kind="small")


def s_apologize(k):
    _mom(k, "mom_cu", pose="bag", face="stern", look=(0.9, 0.0), mouth="E")
    bubble(k, ["I'd make you", "apologize."], "mom", "R", 26)


def s_sorry(k):
    world(k, "panel", lambda: panel(k, "family", do=dict(pose=db.POSE_STRAIGHT, face="obey", look=(-1, 0.1), tense=True,
                                                          mouth="O"), phone="buzz"))
    bubble(k, "Sorry.", "don", "T", 30)


def s_pause(k):
    world(k, "panel", lambda: panel(k, "family", so=dict(pose="fold", face="sideeye", look=(1, 0)),
                                    do=dict(pose=db.POSE_STRAIGHT, face="obey", look=(-1, 0.1), tense=True),
                                    pa=dict(face="frozen", look=(-1, 0)), phone="buzz"))


def s_mom_looks(k):
    _mom(k, "mom_cu", pose="bag", face="stern", look=(0.9, 0.8))


def s_phone_hover(k):
    phone_insert(k, "missed", "hover")


def s_sorry_client(k):
    def d():
        S.backdrop(k, 0.0, "family")
        sofia(k)
        o = don(k, POSE_PHONE, "obey", look=(-1, 0.1), tense=True, mouth="O")
        pam(k)
        S.table(k)                                                         # the phone is at his ear
        hx, hy = o["hands"][1]
        rect(k, hx - 9, hy - 26, 18, 34, (0.10, 0.10, 0.13), 96, shadow=False, lw=2)
        ellipse(k, hx + 3, hy + 2, 10, 10, db.SKIN, 97, shadow=False, lw=2)
    world(k, "don", d)
    bubble(k, "Sorry.", "don", "T", 36)


def s_answered(k):
    phone_insert(k, "answered", None)


def s_good_boy(k):
    _mom(k, "mom", pose="bag", face="sweet", mouth="E")
    bubble(k, "Good boy.", "mom", "T", 36)


# ---------------------------------------------------------------- 4. the verdict
def s_verdict(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        robot(k, "slap_up", talk=0.8)
        S.table(k, phone=None)
    world(k, "robot", d)
    bubble(k, ["She made him", "answer the client.", "Hired."], "robot", "T", 22, mono=True)


def s_stamp(k):
    wood(k)
    S.hired_stamp(k, 262, 470, 1.9, -0.07, paper=True)
    ticks(k, [(70, 320, 44, 300), (470, 330, 496, 312), (60, 640, 34, 660), (478, 630, 504, 652)], 4)


def s_approved(k):
    world(k, "panel", lambda: panel(k, "clear", so=dict(pose="fold", face="sideeye", look=(1, 0)),
                                    do=dict(pose=db.POSE_STRAIGHT, face="obey", tense=True, mouth="U"),
                                    pa=dict(face="frozen")))
    bubble(k, "…Approved.", "don", "T", 24, kind="small")


# ---------------------------------------------------------------- 5. the reveal
def s_leaves(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        don_up(k, 694, "stand", "sheepish", feet=S.FEET_BACK, look=(-1, 0.1), tense=True, lean=-3)   # behind her chair
        sofia(k, "fold", "sideeye", look=(1, -0.8))
        pam(k, face="frozen")
        S.table(k, phone="still")
        ticks(k, [(752, 400, 776, 400), (756, 430, 784, 430), (752, 460, 776, 460)], 3.2)
    world(k, "panel", d)


def _two(k, don_kw, mom_kw, cam="reveal", state="clear"):
    def d():
        S.backdrop(k, 0.0, state)
        don_up(k, DON_X, **don_kw)
        mom_up(k, MOM_X, S.FEET, 1.0, **mom_kw)
    world(k, cam, d)


def s_welcome(k):
    _two(k, dict(pose=POSE_HAND_OUT, face="sheepish", look=(-1, 0.1), tense=True, mouth="E"),
         dict(pose="bag", face="stern", look=(0.9, 0.9), bag=True))
    bubble(k, "Welcome ab—", "don", "T", 28)


def s_lick(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        mom_up(k, MOM_X, S.FEET, 1.0, "lick", "stern", look=(1.0, 0.4))
    world(k, "lick", d)


def s_shout(k):
    _two(k, dict(pose="stand", face="obey", tense=True), dict(pose="hip", face="shout", look=(0.9, 0.4), thrust=0.7, bag=False))
    bubble(k, "DONNIE! Your vest!", "mom", "T", 32, kind="shout")


def _scrub(k, cam):
    _two(k, dict(pose="stand", face="obey", tense=True),
         dict(pose=mb.wipe_at(DON_X - MOM_X - 21, db.BT + 96), face="stern", look=(0.9, 0.9), bag=False), cam)


def s_stain(k):
    _scrub(k, "stain")
    HEADS.clear(); QA["faces"][:] = []                                        # a detail: no whole face is in it


def s_scrub(k):
    _scrub(k, "reveal")


def s_witnesses(k):
    world(k, "panel", lambda: panel(k, "clear", so=dict(pose="fold", face="deadpan"), do=False,
                                    pa=dict(face="approve", look=(-1, 0))))


def s_lapel(k):
    _two(k, dict(pose="stand", face="obey", tense=True, lean=7, look=(1, 0.2)),
         dict(pose=mb.wipe_at(DON_X - MOM_X - 14, db.BT + 60), face="stern", look=(0.9, 0.9), bag=False))


# ---------------------------------------------------------------- 6. the father and the loop
def s_father(k):
    _two(k, dict(pose="stand", face="obey", tense=True, look=(-1, 0)),
         dict(pose="hip", face="stern", look=(0.9, 0.2), bag=False, mouth="E"))
    bubble(k, ["Donnie. Father", "is parking."], "mom", "T", 26)


def s_why(k):
    _two(k, dict(pose="stand", face="obey", tense=True, look=(-1, 0), mouth="O"),
         dict(pose="hip", face="stern", look=(0.9, 0.2), bag=False))
    bubble(k, "Why?", "don", "T", 32)


def s_job(k):
    _two(k, dict(pose="stand", face="obey", tense=True, look=(-1, 0)),
         dict(pose="hip", face="unimpressed", look=(0.9, 0.2), bag=False, mouth="E"))
    bubble(k, ["He's applying", "for your job."], "mom", "T", 26)


def s_tilt(k):
    _two(k, dict(pose="stand", face="panic", tense=True, look=(-1, 0)),
         dict(pose="hip", face="unimpressed", look=(0.9, 0.2), bag=False), "tilt")


def s_door_end(k):
    s_door(k, "clear")


N, C, K = "new", "changed", ""
_ROWS = [
    # (section, seconds, draw, what happens, script rows, status against v2: new / changed / "")
    (0, 1.5, s_door, "The door opens on the whole wall. Frame 0, and the last frame.", "0.1", C),
    (0, 1.6, s_first, "The client calls. Don does not look.", "0.2", C),
    (0, 0.9, s_phone47, "Insert, full screen: 47 missed calls. He turns it over.", "0.2", N),
    (1, 1.4, s_small_low, "Small in a tall frame. Feet off the floor, the CV on his knees.", "1.1", C),
    (1, 0.5, s_feet, "Insert: the feet do not reach.", "1.1", C),
    (1, 1.5, s_pov, "We look up with him. The table is a wall. Don has not looked.", "1.2", C),
    (1, 1.2, s_half, "Three fingers. Optional.", "1.3", C),
    (1, 2.3, s_q1, "The question, flat and bored. Big bubble.", "1.4", C),
    (1, 2.0, s_data, "The right answer.", "1.5", C),
    (1, 1.4, s_short, "Two YES. The monitor says proceed. A finger at the door.", "1.6", C),
    (1, 1.8, s_robot_height, "The robot, seen for the first time: this is whose voice the monitor is.", "1.7", N),
    (1, 0.5, s_cross, "Insert: the red cross.", "1.6", K),
    (1, 1.0, s_small_out, "Hold on his face. He carries the CV out.", "1.7", C),
    (2, 1.0, s_loom, "Too big for the frame. A small hello.", "2.1", C),
    (2, 0.8, s_legs, "Insert: he sits. The chair legs bow.", "2.1", C),
    (2, 1.1, s_pen_goes, "Her one crack. The pen goes.", "2.2", C),
    (2, 0.5, s_boot, "Insert: it stops at his boot.", "2.2", K),
    (2, 1.6, s_dropped, "Two fingertips, one pen.", "2.3", N),
    (2, 1.1, s_thanks, "His hand fills her close-up. A smile she cannot put away.", "2.4", N),
    (2, 1.8, s_chain, "Along the table: she looks at him, Don at her, Pam at Don. KIND.", "2.5", C),
    (2, 0.6, s_eyes_jealous, "Punch in: Don's eyes. Jealous before he speaks.", "2.5", K),
    (2, 2.2, s_q2, "The question, pointed. Same camera, same spot, normal bubble.", "2.6", C),
    (2, 2.2, s_okay, "He fills the frame and comforts him.", "2.7", C),
    (2, 1.4, s_true, "Her paddle is up early. His smile dies.", "2.8", C),
    (2, 1.1, s_distracting, "He says it to her.", "2.9", C),
    (2, 1.1, s_whom, "She answers. Herself again for two words.", "2.10", N),
    (2, 1.4, s_push, "One fingertip pushes her YES down. The monitor says proceed.", "2.11, 2.12", C),
    (2, 0.5, s_push_cu, "Insert: the fingertip on the rim.", "2.12", N),
    (2, 1.0, s_no_worries, "He takes it kindly.", "2.12", C),
    (3, 1.6, s_mom_door, "A sweet old lady. One curler.", "3.1, 3.3", C),
    (3, 0.6, s_eyes_afraid, "Punch in: the same eyes, afraid.", "3.2", K),
    (3, 0.8, s_upright, "Bolt upright. The doodle face down.", "3.2", C),
    (3, 2.0, s_mom_sits, "Level and centred under the poster. Her feet reach; the chair does not creak.", "3.3", C),
    (3, 0.9, s_experience, "The robot asks.", "3.4", N),
    (3, 2.1, s_forty, "She answers. The same frame.", "3.5", C),
    (3, 1.0, s_five, "The standard question.", "3.6", C),
    (3, 1.0, s_ageism, "The buzzer cuts her off. Her pen stops in the air.", "3.7", N),
    (3, 1.6, s_family_q, "The one question that would catch it.", "3.8", C),
    (3, 1.8, s_family, "Withdrawn. Don breathes out.", "3.9", N),
    (3, 2.6, s_q3, "The question, half the voice. Same camera, same spot, small bubble.", "3.10", C),
    (3, 2.0, s_apologize, "Her one close-up. Her eyes open.", "3.11", C),
    (3, 1.0, s_sorry, "A smaller Don, under the ruling.", "3.12", C),
    (3, 2.4, s_pause, "The longest pause. Pam turns; Sofía has seen it.", "3.13", C),
    (3, 0.6, s_mom_looks, "She looks at the phone. Then at him.", "3.14", C),
    (3, 0.8, s_phone_hover, "Insert, full screen: 47 missed calls. His hand does not want to.", "3.14", K),
    (3, 1.5, s_sorry_client, "He says it to the client.", "3.15", C),
    (3, 0.7, s_answered, "Insert, full screen: the first call answered in 47.", "3.15", N),
    (3, 2.0, s_good_boy, "As if nothing had happened.", "3.16", C),
    (4, 1.5, s_verdict, "The robot rolls forward, the stamp up.", "4.1", N),
    (4, 0.6, s_stamp, "Insert, full screen: the stamp.", "4.1", N),
    (4, 1.5, s_approved, "No bias detected. His catchphrase, very small.", "4.2", C),
    (5, 1.0, s_leaves, "He leaves the table, behind Sof\u00eda. His chair is empty.", "5.1", C),
    (5, 1.8, s_welcome, "A handshake she ignores. She has seen the vest.", "5.1", C),
    (5, 1.2, s_lick, "The tissue.", "5.2", C),
    (5, 1.6, s_shout, "Brief.", "5.3", C),
    (5, 0.6, s_stain, "Insert: the tissue lands on the ketchup.", "5.4", K),
    (5, 1.6, s_scrub, "She scrubs. He stands still for it, under WE HIRE ON MERIT.", "5.4, 5.5", C),
    (5, 1.0, s_witnesses, "Cut away: his empty chair between them. Sofía looks at us.", "5.7", C),
    (5, 2.0, s_lapel, "Back: he leans away, she pulls him in by the lapel.", "5.6", C),
    (6, 1.8, s_father, "Folding the tissue.", "6.1", C),
    (6, 1.2, s_why, "He has to ask.", "6.2", N),
    (6, 1.6, s_job, "She says it like the weather.", "6.3", C),
    (6, 1.0, s_tilt, "The one tilted frame: his world, not the room.", "6.3", C),
    (6, 1.6, s_door_end, "The door begins to open. Level again. Cut to 01.", "6.4", C),
]
SHOTS, _t = [], 0.0
for _n, (_sec, _dur, _fn, _cap, _row, _st) in enumerate(_ROWS, 1):
    # (id, section, t0, t1, draw, what happens, script rows, status)
    SHOTS.append(("%02d" % _n, _sec, _t, round(_t + _dur, 1), _fn, _cap, _row, _st))
    _t = round(_t + _dur, 1)
DURATION = SHOTS[-1][3]


def frame(c, x, y, w, draw):
    """Draw one shot into a w-wide 9:16 box at (x, y)."""
    c.save(); c.translate(x, y); c.scale(w / 540.0, w / 540.0)
    c.rectangle(0, 0, 540, 960); c.clip()
    m = c.get_matrix(); m.invert(); _BASE[0] = m
    HEADS.clear()
    for v in QA.values():
        v[:] = []
    c.set_source_rgb(*kit.WALL); c.paint()
    draw(kit.Ctx(c, 0))
    c.restore()
