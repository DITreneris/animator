"""THE BEST CANDIDATE: the board for animation v3 (script v6, 64 panels). bc_sb_v3.py is storyboard v3 as delivered
and bc_sb_anim_v2.py the board animation v2 ran on, both kept.
This pass, after the frame audit of animation v2:
  - a tail is aimed at the speaker's cheek or crown as MEASURED on the drawing (measure()), never at a typed offset:
    the typed head sizes had put tips on Sofia's hair, Mom's hat, the small one's collar and in the air over Don;
  - every human speaker's bubble is beside the face, level with the mouth. Sofia has her own single for each line
    (the bubble on her left, the tail over her ringlets to the cheek), Pam has a single with the wall on her right,
    Mom's seated lines are framed with the wall on her right and her standing lines with Don at the right of frame;
  - a bubble goes overhead only for the robot (onto its antenna) and for Don at the table, where Sofia's and Pam's
    faces sit either side of his mouth (onto his bare scalp, touching it);
  - Don's "smug" face takes a spoken mouth; the chair insert sits under the macho's badge; Don's elbow is carried
    high when he pushes the paddle, so YES is never covered;
  - SAY holds every line's bubble once, for the board and the animation; qa_bc.py v2 checks it all on pixels.
Below, the notes of storyboard v3, which still hold except where the list above replaces them.
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
import numpy as np
import kit
import bc_set as S
import cand_bc as cb
import don_bc as db
import don_mf as dm
import iwry_mouths as im
import mom_bc as mb
import pam_bc as pb
import pam_mf
import sofia_bc as sb
import sofia_v4 as sf4
import robot_mf as rm
import props_bc as props
from kit import INK, cut, rect, ellipse

X = S.POS
W, H = 540, 960
SAFE = (20, 96, 475, 816)                                  # where a label may sit: x0, y0, x1, y1
MONO = "DejaVu Sans Mono"
THANKS_DROP = 208                                          # the macho's feet below the floor line in "Thank you.": his hand at her collar, under the tail
MOM_X, DON_X = X["chair"] + 14, X["chair"] + 126          # where they stand for the reveal
# Rough face boxes only (half the face's width at mouth height, the top of the hair or hat above the mouth, world px
# at scale 1): they mark where a listener's face is for qa_bc.py. No tail is aimed with these numbers any more:
# a speaker's mouth, cheeks and crown are measured from the drawing itself (see measure()).
FACE = {"sofia": (42, 100), "don": (52, 84), "pam": (38, 86), "small": (40, 112), "macho": (46, 105),
        "mom": (52, 106), "robot": (48, 86)}
# signs on the wall and the table, as drawn (world boxes): a frame holds each of them whole or not at all
LABELS = {"poster": (253, 166, 449, 292), "notice": (150, 259, 244, 373), "monitor": (681, 164, 968, 315),
          "sign": (1085, 237, 1216, 289), "nameplate": (736, 612, 828, 640)}
POSE_POINT_L = (-75, -95) + dm.ik(1, 30, db.BT + 84)        # the finger at the door, under Sofia's chin; the list in the other hand
POSE_PHONE = (-8, 0) + dm.ik(1, 47, db.HY + 8)              # the phone at his ear
POSE_HAND_OUT = (-82, -8, 8, 0)                             # a handshake offered to screen left
sb.POSES["yes_up"] = (-12, 24, 172, 20)                    # Sofia's paddle held up by her head: whole inside her single

db.MOUTH_FIX = True                                        # Don's "flat" and "sheepish" mouths are drawn (see don_bc)
BUBBLES = True                                             # qa_bc.py turns them off to find what they cover
HEADS, QA = {}, {"faces": [], "labels": [], "bubbles": []}
_BASE = [None]
# qa_bc.py redraws a frame with one of the cast changed, and reads the difference: {"who": name or "*", "mode": m}
#   "hide"  the character is not drawn (the difference is its silhouette, as the frame shows it)
#   "open" / "shut"  its mouth is forced (the difference is where the mouth is)
#   "skin"  its skin is drawn in a marker colour (the difference is its skin: face, ears, hands)
PROBE = {"who": None, "mode": None}
SKINS = {"sofia": [sf4.SKIN], "don": [db.SKIN], "pam": [pam_mf.SKIN], "small": [cb.S_SKIN],
         "macho": [cb.M_SKIN, cb.M_SKIN_DARK], "mom": [mb.SKIN], "robot": []}
MOUTHS = {"sofia": ("A", "M"), "don": ("A", "M"), "pam": ("A", "M"), "small": ("A", "M"), "macho": ("A", "M"),
          "mom": ("A", "O"), "robot": (1.0, 0.0)}           # two shapes to tell the mouth by (the robot's is its talk level)
_NULL = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4))
PAD = 140                                                  # the measuring sheet is the frame and this much around it


class _Swap:
    """A cairo context that paints the given colours in magenta: the skin, so it can be told from hair and cloth."""
    def __init__(self, c, cols):
        self._c, self._cols = c, cols

    def __getattr__(self, n):
        return getattr(self._c, n)

    def _map(self, r, g, b):
        for p, q, u in self._cols:
            if abs(r - p) + abs(g - q) + abs(b - u) < 0.012:
                return 1.0, 0.0, 1.0
        return r, g, b

    def set_source_rgb(self, r, g, b):
        self._c.set_source_rgb(*self._map(r, g, b))

    def set_source_rgba(self, r, g, b, a=1.0):
        self._c.set_source_rgba(*(self._map(r, g, b) + (a,)))


def _to540(k, x, y):
    """A point in the current drawing space, in 540 x 960 frame coordinates."""
    return _BASE[0].transform_point(*k.c.user_to_device(x, y))


def _box540(k, x0, y0, x1, y1):
    p = [_to540(k, x, y) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    return min(q[0] for q in p), min(q[1] for q in p), max(q[0] for q in p), max(q[1] for q in p)


def head(k, name, x, my, s=1.0):
    """Register a rough face box for a head just drawn (inside the camera transform), mouth near (x, my)."""
    r, top = FACE[name]
    mx, mY = _to540(k, x, my)
    ex, ey = _to540(k, x + 1, my)
    z = math.hypot(ex - mx, ey - mY) * s                   # screen px per unit of this character
    HEADS[name] = {"m": (mx, mY), "R": r * z, "top": mY - top * z}
    QA["faces"].append((name, _box540(k, x - (r - 5) * s, my - 56 * s, x + (r - 5) * s, my + 10 * s)))


def _cast(k, name, fn, mouth, x, my, s=1.0):
    """Draw one of the cast through fn(kk, mouth) and register it, so a bubble can measure its head from the drawing
    (measure()) and qa_bc.py can redraw the frame with it changed (PROBE)."""
    mode = PROBE["mode"] if PROBE["who"] in (name, "*") else None
    if mode == "hide":
        o = fn(kit.Ctx(_NULL, k.boil), mouth)
    elif mode == "skin":
        o = fn(kit.Ctx(_Swap(k.c, SKINS[name]), k.boil), mouth)
    elif mode in ("open", "shut"):
        o = fn(k, MOUTHS[name][mode == "shut"])
    else:
        o = fn(k, mouth)
    head(k, name, x, my, s)
    m = k.c.get_matrix()
    HEADS[name].update(fn=fn, mouth=mouth, M=m.multiply(_BASE[0]), boil=k.boil)
    return o


def measure(name):
    """The speaker's head, measured on its own drawing (540 x 960 frame px): the mouth (where two mouth shapes
    differ), the cheek edge on either side of it at mouth height (the last skin, walking out from the mouth) and
    the crown (the topmost pixel of the figure over the mouth). Nothing here is a typed number."""
    h = HEADS[name]
    if "meas" in h:
        return h["meas"]

    def shot(mouth, swap=False):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W + 2 * PAD, H + 2 * PAD)
        c = cairo.Context(surf)
        c.set_matrix(h["M"].multiply(cairo.Matrix(1, 0, 0, 1, PAD, PAD)))
        h["fn"](kit.Ctx(_Swap(c, SKINS[name]) if swap else c, h["boil"]), mouth)
        surf.flush()
        return np.frombuffer(surf.get_data(), np.uint8).reshape(H + 2 * PAD, W + 2 * PAD, 4).astype(int)

    z = math.hypot(h["M"].xx, h["M"].yx)
    base = shot(h["mouth"])
    mo = np.abs(shot(MOUTHS[name][0]) - shot(MOUTHS[name][1])).sum(axis=2) > 40
    sil = base[:, :, 3] > 128
    out = {"ok": False, "z": z}
    ys, xs = np.nonzero(mo)
    if len(xs):
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        skin = (np.abs(shot(h["mouth"], True) - base).sum(axis=2) > 60) if SKINS[name] else sil
        gmax = 5 * z + 2                                   # a line or a string of pearls on the cheek is stepped over
        edge = {}
        for sd in (-1, 1):
            ends = []
            for row in range(cy - 2, cy + 3):
                x = last = x1 if sd > 0 else x0
                gap = 0
                while 0 < x + sd < W + 2 * PAD - 1 and gap <= gmax:
                    x += sd
                    if skin[row, x] or mo[row, x]:
                        last, gap = x, 0
                    else:
                        gap += 1
                ends.append(last)
            edge[sd] = sorted(ends)[len(ends) // 2]
        band = int(round(16 * z))
        cols = sil[:cy, max(0, cx - band):cx + band + 1]
        rows = np.nonzero(cols.any(axis=1))[0]
        ty = int(rows.min()) if len(rows) else cy
        tx = float(np.nonzero(cols[ty])[0].mean()) + max(0, cx - band) if len(rows) else cx
        reach = {}
        for sd in (-1, 1):                                 # how far the figure runs on beside the cheek: hair
            x = edge[sd]
            while 0 < x + sd < W + 2 * PAD - 1 and sil[cy - 2:cy + 3, x + sd].any():
                x += sd
            reach[sd] = x
        out = {"ok": True, "z": z, "m": (cx - PAD, cy - PAD), "box": (x0 - PAD, y0 - PAD, x1 - PAD, y1 - PAD),
               "eL": edge[-1] - PAD, "eR": edge[1] - PAD, "top": (tx - PAD, ty - PAD),
               "sL": reach[-1] - PAD, "sR": reach[1] - PAD, "skin": skin}
    h["meas"] = out
    return out


# The set's cameras, and the framings that give a speaker clear wall beside the face (a sign is whole in each, or out)
CAM = dict(S.CAMS)
CAM.update(pov=(584, 590, 1.8),                             # Sofia alone over the table's edge, the wall on her left
           sofia_say=(611, 572, 2.2),                      # Sofia's single for a line: the bubble on her left
           mom_say=(423.5, 578, 1.7),                       # Mom on the chair, left of frame; the poster and notice are out
           pair=(344.2, 480, 1.38),                        # Mom and Don standing, right of frame: the wall is hers
           pam_say=(1040, 570, 2.0),                       # Pam's single: the wall on her right (the robot has rolled
           #                                                 off that way since "Experience?"; it rolls back in to rule)
           legs=(350, 766, 2.5))                           # the chair insert, under his badge


def world(k, cam, draw):
    c = k.c
    cam = CAM[cam] if isinstance(cam, str) else cam
    c.save(); S.with_cam(c, cam)
    for name, b in LABELS.items():
        QA["labels"].append((name, _box540(k, *b)))
    draw(); c.restore()


# ---------------------------------------------------------------- bubbles
def bubble(k, lines, who, form="R", size=30, kind="normal", dx=0, dy=0, gap=20, mono=False, at=None, fault=(0, 0),
           hair=False, lock=None):
    """One speaker's line. who: one of the cast drawn in this frame. form:
      "R" / "L"  beside the face, level with the mouth, a short tail that ends on the cheek's outline (every human
                 speaker who has clear wall beside the face; the shot is framed to give it);
      "T"        just above the speaker, the tail down onto the crown: the robot (its antenna), and Don at the table,
                 where a face sits on either side of his mouth;
      "off"      the speaker is out of frame to the right (the robot): at = (x, y), the tail goes to the edge.
    kind: normal / big / small (thin, wobbly) / shout. The box is kept inside SAFE. Where the tail ends comes from
    measure(): the mouth, the cheek and the crown as drawn. hair: the speaker's hair hangs beside the cheek (Sofia),
    so the box stands clear of the hair and the tail runs over it to the cheek. lock = (x, y) pins the box (the
    animation holds a bubble still through its shot; only the tail follows the head). fault moves the tip, for
    qa_bc.py's self-test only."""
    c = k.c
    if isinstance(lines, str):
        lines = [lines]
    c.select_font_face(MONO if mono else kit.FONT, cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if mono else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    ws = [c.text_extents(t).x_advance for t in lines]
    lh = size * 1.12
    bw, bh = max(ws) + 44, len(lines) * lh + 26
    ms = None
    if form == "off":
        bx, by = at
    else:
        ms = measure(who)
        if ms["ok"]:
            (mx, my), eL, eR, top = ms["m"], ms["eL"], ms["eR"], ms["top"]
            oL, oR = (ms["sL"] - 4 + gap, ms["sR"] + 4 - gap) if hair else (eL, eR)
        else:                                              # no mouth to be found in the drawing: the rough box
            h = HEADS[who]
            (mx, my), eL, eR, top = h["m"], h["m"][0] - h["R"], h["m"][0] + h["R"], (h["m"][0], h["top"])
            oL, oR = eL, eR
        if form in ("R", "L"):
            sd = 1 if form == "R" else -1
            bx = oR + gap if sd > 0 else oL - gap - bw
            by = my - bh / 2
        else:
            bx, by = top[0] - bw / 2, top[1] - gap - bh
    bx, by = bx + dx, by + dy
    by = max(SAFE[1], min(SAFE[3] - bh, by))
    if form in ("R", "L") and ms["ok"]:                     # an ear or a hand beside the box's own rows: stand clear of it
        r0, r1 = int(by) + PAD - 4, int(by + bh) + PAD + 4
        e = int(eR if sd > 0 else eL) + PAD
        span = ms["skin"][max(0, r0):r1, e:e + int(34 * ms["z"])] if sd > 0 else \
            ms["skin"][max(0, r0):r1, max(0, e - int(34 * ms["z"])):e + 1][:, ::-1]
        cols = np.nonzero(span.any(axis=0))[0]
        if len(cols):
            far = e + sd * int(cols.max()) - PAD
            bx = max(bx, far + 7) if sd > 0 else min(bx, far - 7 - bw)
    bx = max(SAFE[0], min(SAFE[2] - bw, bx))
    if lock:
        bx, by = lock
    if form in ("R", "L"):
        ex = bx + 3 if sd > 0 else bx + bw - 3
        ty = max(by + 15, min(by + bh - 15, my))
        tip = ((eR if sd > 0 else eL) + sd * 1.5, my)       # on the outline of the cheek
        tail = [(ex, ty - 11), tip, (ex, ty + 11)]
    elif form == "T":
        rx = max(bx + 28, min(bx + bw - 28, top[0]))
        tip = (top[0], top[1] + 1.5)                        # on the outline of the crown
        tail = [(rx - 12, by + bh - 3), tip, (rx + 12, by + bh - 3)]
    else:
        tip = (W - 5, by + bh / 2 + 16)
        tail = [(bx + bw - 3, by + bh / 2 - 11), tip, (bx + bw - 3, by + bh / 2 + 11)]
    if fault != (0, 0):
        tip = (tip[0] + fault[0], tip[1] + fault[1]); tail[1] = tip
    QA["bubbles"].append({"who": who, "form": form, "box": (bx, by, bx + bw, by + bh), "tip": tip, "size": size,
                          "text": " ".join(lines), "tail": math.hypot(tip[0] - (tail[0][0] + tail[2][0]) / 2,
                                                                      tip[1] - (tail[0][1] + tail[2][1]) / 2),
                          "base": ((tail[0][0] + tail[2][0]) / 2, (tail[0][1] + tail[2][1]) / 2),
                          "mouth": None if form == "off" else HEADS[who].get("mouth"),
                          "edges": (ms["eL"], ms["eR"]) if ms and ms["ok"] else None})
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


# Every line's bubble: shot -> (lines, speaker, form, size, options). The storyboard and the animation both read it.
SAY = {
    "s_first": (["First candidate."], "don", "T", 32, {}),
    "s_pov": (["Three", "degrees?"], "sofia", "L", 34, dict(hair=True)),
    "s_half": (["And", "a half."], "small", "R", 34, dict(dy=46)),
    "s_q1": (["What if I made", "a mistake?"], "don", "T", 36, dict(kind="big")),
    "s_data": (["I'd show you", "the data."], "small", "R", 28, dict(dy=10)),
    "s_short": (["Too short."], "don", "T", 34, {}),
    "s_robot_height": (["Height is not", "protected.", "Proceed."], "robot", "T", 22, dict(mono=True)),
    "s_dropped": (["You dropped", "this."], "macho", "R", 26, {}),
    "s_thanks": (["Thank you."], "sofia", "L", 32, dict(hair=True)),
    "s_q2": (["And you. What if", "I made a mistake?"], "don", "T", 30, {}),
    "s_okay": (["Everybody", "makes", "mistakes.", "It's okay."], "macho", "R", 26, {}),
    "s_true": (["That's", "so true."], "sofia", "L", 30, dict(hair=True)),
    "s_distracting": (["Too distracting."], "don", "T", 28, {}),
    "s_whom": (["For whom?"], "sofia", "L", 32, dict(hair=True)),
    "s_no_worries": (["No worries."], "macho", "R", 30, dict(dy=-14)),
    "s_mom_door": (["Good morning,", "everyone."], "mom", "R", 26, {}),
    "s_experience": (["Experience?"], "robot", "T", 26, dict(mono=True)),
    "s_forty": (["Forty years.", "One very", "difficult client."], "mom", "R", 26, {}),
    "s_five": (["Where do you", "see yourself", "in five—"], "sofia", "L", 25, dict(hair=True)),
    "s_family_q": (["Any family in", "the company?"], "pam", "R", 25, dict(hair=True)),
    "s_q3": (["What if I…", "made a mistake?"], "don", "T", 24, dict(kind="small")),
    "s_apologize": (["I'd make you", "apologize."], "mom", "R", 26, {}),
    "s_sorry": (["Sorry."], "don", "T", 30, {}),
    "s_sorry_client": (["Sorry."], "don", "T", 36, {}),
    "s_good_boy": (["Good boy."], "mom", "R", 36, {}),
    "s_verdict": (["She made him", "answer the client.", "Hired."], "robot", "T", 22, dict(mono=True)),
    "s_approved": (["…Approved."], "don", "T", 24, dict(kind="small")),
    "s_welcome": (["Welcome ab—"], "don", "T", 28, {}),
    "s_shout": (["DONNIE!", "Your vest!"], "mom", "L", 28, dict(kind="shout")),
    "s_father": (["Donnie.", "Father is", "parking."], "mom", "L", 26, {}),
    "s_why": (["Why?"], "don", "T", 32, {}),
    "s_job": (["He's", "applying for", "your job."], "mom", "L", 26, {}),
}


def say(k, shot, **over):
    lines, who, form, size, kw = SAY[shot]
    bubble(k, lines, who, form, size, **dict(kw, **over))


# ---------------------------------------------------------------- the cast, each registering its head
def sofia(k, pose="write", face="neutral", look=(-1, 0), mouth=None, **kw):
    fn = lambda kk, m: sb.sofia(kk, X["sofia"], S.SEAT, 1.0, pose, face, look=look, mouth=m, **kw)
    o = {}
    S.seated(k, lambda: o.update(_cast(k, "sofia", fn, mouth, X["sofia"], S.SEAT + sb.HY + 34)))
    return o


def don(k, pose=None, face="flat", look=(-0.6, 0.9), mouth=None, **kw):
    pose = db.POSE_PEN if pose is None else pose
    kw.setdefault("board", "front" if pose is db.POSE_PEN else None)
    def fn(kk, m):
        out = db.don(kk, X["don"], S.SEAT, 1.0, pose, face, look=look, mouth=m, **kw)
        if m and face == "smug":                           # the smirk takes no spoken mouth of its own: draw it over
            hx, hy = out["head"]
            ellipse(kk, hx + 1, hy + 28, 22, 12, db.SKIN, 597, shadow=False, outline=False)
            im.mouth(kk, hx, hy + 28, m, db.SKIN, erase=(1, 1), seed=596)
        return out
    o = {}
    S.seated(k, lambda: o.update(_cast(k, "don", fn, mouth, X["don"], S.SEAT + db.HY + 30)))
    return o


def pam(k, pose=None, face="neutral", look=(-1, 0), mouth=None, **kw):
    pose = pb.POSE_TABLE if pose is None else pose
    fn = lambda kk, m: pb.pam(kk, X["pam"], S.SEAT, 1.0, pose, face, look=look, mouth=m, **kw)
    o = {}
    S.seated(k, lambda: o.update(_cast(k, "pam", fn, mouth, X["pam"], S.SEAT + pb.HY + 30)))
    return o


def don_up(k, x, pose, face, feet=None, mouth=None, **kw):
    feet = S.FEET if feet is None else feet
    return _cast(k, "don", lambda kk, m: db.don(kk, x, feet, 1.0, pose, face, mouth=m, **kw), mouth, x,
                 feet + db.HY + 30)


def mom_up(k, x, feet, s, pose, face, mouth=None, **kw):
    return _cast(k, "mom", lambda kk, m: mb.mom(kk, x, feet, s, pose, face, mouth=m, **kw), mouth, x,
                 feet + (mb.HY + 30) * s, s)


def mom_sit(k, mouth=None, **kw):
    return _cast(k, "mom", lambda kk, m: S.mom_on_chair(kk, mouth=m, **kw), mouth, X["chair"], 526)


def small(k, pose, face, x=None, seated=True, mouth=None, **kw):
    x = X["chair"] if x is None else x
    feet = S.CHAIR_SEAT if seated else S.FEET
    return _cast(k, "small", lambda kk, m: cb.small(kk, x, feet, 1.0, pose, face, seated=seated, mouth=m, **kw), mouth, x,
                 feet - (80 if seated else 128))


def macho(k, pose, face, x=None, feet=None, s=1.0, seated=False, mouth=None, **kw):
    x = X["chair"] if x is None else x
    feet = S.FEET if feet is None else feet
    return _cast(k, "macho", lambda kk, m: cb.macho(kk, x, feet, s, pose, face, seated=seated, mouth=m, **kw), mouth, x,
                 feet + (cb.M_HY + 40 + (56 if seated else 0)) * s, s)


def robot(k, pose="stand", talk=0.0):
    return _cast(k, "robot", lambda kk, m: rm.robot(kk, X["robot"], S.FEET_BACK, 1.0, pose, "eager", talk=m, seed=97),
                 talk, X["robot"], S.FEET_BACK - 219)


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
    say(k, "s_first")


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
    world(k, "pov", lambda: panel(k, "idle", so=dict(pose="write", face="curious", look=(-0.8, 0.9), mouth="O"),
                                  do=dict(look=(-0.2, 1.0)), pa=False))
    rect(k, -20, 752, 580, 240, S.ts.WOOD, 931, shadow=False, outline=False)   # from down here the table is a wall
    head_from_behind(k, 196, 900)
    say(k, "s_pov")


def s_half(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        small(k, "finger", "proud", look=(0.7, -0.1), mouth="E")
    world(k, "small_say", d)
    say(k, "s_half")


def s_q1(k):
    world(k, "don", lambda: panel(k, "idle", do=dict(look=(-0.2, 1.0), mouth="E"), phone="buzz"))
    say(k, "s_q1")


def s_data(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        small(k, "hug", "proud", cv=True, look=(0.7, -0.1), mouth="E")
    world(k, "small_say", d)
    say(k, "s_data")


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
    say(k, "s_short")


def s_robot_height(k):
    def d():
        S.backdrop(k, 0.0, "proceed_height")
        robot(k, "present", talk=0.8)
        S.table(k, phone=None)
    world(k, "robot", d)
    say(k, "s_robot_height")


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
    say(k, "s_dropped")


def s_thanks(k):
    def d():
        panel(k, "idle", so=dict(pose="aside", face="tiny", look=(-1, -0.8), lag=(-7, 0), blush=0.7, mouth="E"),
              do=False, pa=False)
        macho(k, "pinch_low", "warm", x=X["sofia"] - 292, feet=S.FEET + THANKS_DROP, s=1.3, look=(0.9, 0.6), pen=True)
    world(k, "sofia_say", d)
    del HEADS["macho"]; QA["faces"][:] = [f for f in QA["faces"] if f[0] != "macho"]   # only his hand is in the frame
    say(k, "s_thanks")


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
    say(k, "s_q2")


def s_okay(k):
    def d():
        S.backdrop(k, 0.0, "idle")
        macho(k, "sit", "warm", seated=True, look=(0.8, 0.1), mouth="E")
    world(k, "macho_say", d)
    say(k, "s_okay")


def s_true(k):
    world(k, "sofia_say", lambda: panel(k, "idle", so=dict(pose="yes_up", face="smile", look=(-1, -0.3), paddle="YES",
                                                            blush=0.6, mouth="E"),
                                        do=dict(face="drop", look=(-1, 0.0), mouth="M"), pa=dict(face="peer")))
    say(k, "s_true")


def s_distracting(k):
    world(k, "sofia_don", lambda: panel(k, "idle", so=dict(pose="aside", face="eyebrow", look=(1, 0)),
                                        do=dict(face="pout", look=(-1, 0.0), tense=True, marks=2, mouth="A"), pa=dict(face="peer")))
    say(k, "s_distracting")


def s_whom(k):
    world(k, "sofia_say", lambda: panel(k, "idle", so=dict(pose="aside", face="eyebrow", look=(1, 0), mouth="O"),
                                        do=dict(face="pout", look=(-1, 0.0), tense=True, marks=2, mouth="M"), pa=dict(face="peer")))
    say(k, "s_whom")


def ik_over(side, tx, ty, ln=48):
    """Don's arm to (tx, ty) with the elbow carried high (dm.ik lets it hang): the forearm comes down onto the paddle
    from above, so no sleeve lies across the word on it."""
    sx, sy = side * 40, db.BT + 14
    vx, vy = tx - sx, ty - sy
    dist = min(math.hypot(vx, vy), 2 * ln - 0.5)
    ang, al = math.degrees(math.atan2(vx, vy)), math.degrees(math.acos(dist / (2 * ln)))
    sg = min((1, -1), key=lambda g: math.cos(math.radians(ang + g * al)))
    return ang + sg * al, -2 * sg * al


def _push(k):
    S.backdrop(k, 0.0, "proceed_looks")
    sofia(k, "paddle", "unimpressed", look=(1, -0.2), paddle="YES")
    o = don(k, ik_over(-1, -94, db.BT - 100) + (8, 0), "flat", look=(-1, -0.3), tense=True, board=None)
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
    say(k, "s_no_worries")


# ---------------------------------------------------------------- 3. Mom
def s_mom_door(k):
    def d():
        S.backdrop(k, 0.9, "idle")
        mom_up(k, X["door"] + 22, S.FLOOR_Y + 52, 0.96, "bag", "sweet", mouth="E")
    world(k, "door", d)
    say(k, "s_mom_door")


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
    say(k, "s_experience")


def s_forty(k):
    _mom(k, "mom_say", pose="bag", face="sweet", look=(0.9, 0.0), mouth="E")
    say(k, "s_forty")


def s_five(k):
    world(k, "sofia_say", lambda: panel(k, "idle", so=dict(pose="ask", face="neutral", look=(-1, 0.0), mouth="E"),
                                        do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-1, 0.2), board="back", tense=True),
                                        pa=dict()))
    say(k, "s_five")


def s_ageism(k):
    world(k, "sofia_don", lambda: panel(k, "ageism", so=dict(pose="ask", face="flustered", look=(0.6, -0.9), blush=0.0),
                                        do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-1, 0.2), board="back", tense=True),
                                        pa=dict()))


def s_family_q(k):
    world(k, "pam_say", lambda: panel(k, "idle", so=dict(pose="ask", face="flustered", look=(0.6, -0.9), blush=0.0),
                                      do=dict(pose=db.POSE_HIDE, face="sheepish", look=(1, 0.3), board="back", tense=True),
                                      pa=dict(pose=pb.POSE_ASK, face="probe", mouth="E", pen=True, lean=-3)))
    say(k, "s_family_q")


def s_family(k):
    world(k, "don_pam", lambda: panel(k, "family", so=dict(pose="fold", face="neutral", look=(1, 0)),
                                      do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-0.4, 1.0), board="back", tense=True),
                                      pa=dict(pose=pb.POSE_ASK, face="frozen", pen=True)))


def s_q3(k):
    world(k, "don", lambda: panel(k, "family", do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-0.4, 1.0), board="back",
                                                        tense=True, mouth="O"), phone="buzz"))
    say(k, "s_q3")


def s_apologize(k):
    _mom(k, "mom_cu", pose="bag", face="stern", look=(0.9, 0.0), mouth="E")
    say(k, "s_apologize")


def s_sorry(k):
    world(k, "panel", lambda: panel(k, "family", do=dict(pose=db.POSE_STRAIGHT, face="obey", look=(-1, 0.1), tense=True,
                                                          mouth="O"), phone="buzz"))
    say(k, "s_sorry")


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
    say(k, "s_sorry_client")


def s_answered(k):
    phone_insert(k, "answered", None)


def s_good_boy(k):
    _mom(k, "mom_cu", pose="bag", face="sweet", look=(0.9, 0.0), mouth="E")
    say(k, "s_good_boy")


# ---------------------------------------------------------------- 4. the verdict
def s_verdict(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        robot(k, "slap_up", talk=0.8)
        S.table(k, phone=None)
    world(k, "robot", d)
    say(k, "s_verdict")


def s_stamp(k):
    wood(k)
    S.hired_stamp(k, 262, 470, 1.9, -0.07, paper=True)
    ticks(k, [(70, 320, 44, 300), (470, 330, 496, 312), (60, 640, 34, 660), (478, 630, 504, 652)], 4)


def s_approved(k):
    world(k, "panel", lambda: panel(k, "clear", so=dict(pose="fold", face="sideeye", look=(1, 0)),
                                    do=dict(pose=db.POSE_STRAIGHT, face="obey", tense=True, mouth="U"),
                                    pa=dict(face="frozen")))
    say(k, "s_approved")


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
    say(k, "s_welcome")


def s_lick(k):
    def d():
        S.backdrop(k, 0.0, "clear")
        mom_up(k, MOM_X, S.FEET, 1.0, "lick", "stern", look=(1.0, 0.4))
    world(k, "lick", d)


def s_shout(k):
    _two(k, dict(pose="stand", face="obey", tense=True), dict(pose="hip", face="shout", look=(0.9, 0.4), thrust=0.7, bag=False, mouth="A"),
         "pair")
    say(k, "s_shout")


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
         dict(pose="hip", face="stern", look=(0.9, 0.2), bag=False, mouth="E"), "pair")
    say(k, "s_father")


def s_why(k):
    _two(k, dict(pose="stand", face="obey", tense=True, look=(-1, 0), mouth="O"),
         dict(pose="hip", face="stern", look=(0.9, 0.2), bag=False), "pair")
    say(k, "s_why")


def s_job(k):
    _two(k, dict(pose="stand", face="obey", tense=True, look=(-1, 0)),
         dict(pose="hip", face="unimpressed", look=(0.9, 0.2), bag=False, mouth="E"), "pair")
    say(k, "s_job")


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
