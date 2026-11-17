"""ANIMATION v2 of the Christmas special "Happy Compliance": the approved v1 (xmas_anim.py, untouched) with, per
frame and only for this render:
- Pam v4 (pam_xmas3 + xmas_pam3): the canon head, deadpan pressed lips, the side-eye at Don in the still beat,
  "Human in the loop." said with the mask up, then the visible drop over her readers, the push-in and the hold;
- the banner on two rows, "MERRY CHRISTMAS" over "TO ALL", inside the widest frame (it read "Y CHRISTMAS TO AL");
- the company sign moved in (it was cropped to "UPTIME" at 4 s) and lower in the last shot (its top was cut);
- Sofia's badge raised above her forearm (the arm hid its A: "SOFI");
- the razor on the floor without Don's fingers (it read as a cut-off hand), bigger, with a blob of foam;
- every bubble tail aimed at the speaker and stopping at the edge of the head ("Eww." keeps its two tails).
v4 (xmas_anim2_v3.py = v3 kept), after the fourth tail review: every box placed by hand clear of the speaker's
head, hat, cap or mask (V4), tails leave the box outside the face and hook in beside the mouth drawn this frame;
"Eww." as two bubbles a beat apart with their own emoticons (Sofia's eye-roll, Pam's queasy green); "Merry Christmas,
Don." beside him with its tail to the left edge (Sofia off screen); the door's PARTY sign also out of shots 1 and 4,
where it was only ever hidden behind the old boxes.
v3 (xmas_anim2_v2.py = v2 kept), after the third frame review: tails curve around the outside of the head and end
on the cheek right beside the mouth corner (a tapered curved wedge), keyed by the speaker's x so a box pushed by the
safe area keeps its tail; the tip used to overshoot the face (onto the tree) or fall back to the crown.
v2 (xmas_anim2_v1.py = v1 kept), after the frame review: no cropped words anywhere:
- the banner rows sit where every camera shows them whole or not at all ("MERRY CHRISTMAS" y 176, "TO ALL" y 208
  under MERRY); the company sign is left out of the shots whose camera would cut it (6, 7, 9), the incident board
  out of shot 8, the door's PARTY sign out of 10b;
- tails reach the speaker's mouth from the side: the box stays where it was, the tip lands at the cheek at mouth
  height on the side facing the frame centre, so it points at the mouth without covering eyes or mouth.
Render: python3 engine_v.py xmas_anim2 (540) / python3 engine_hd.py xmas_anim2 (1080)."""
import math
import kit
import brand
from kit import INK, rect, text, ellipse, cut, ease, clamp
import xmas_anim as xa
import xmas_set as xs
import xmas_sb_v2 as sb
import sofia_xmas as sx
import don_xmas as dx
import pt42
import xmas_pam3 as route
import xmas_bubbles as xb
import iwry_mouths as imo
MOUTHS = []                                                    # device positions of the mouths drawn this frame

RAW_T = 0.0
DURATION = xa.DURATION
SHOT11 = (26.9, 28.9)
NO_SIGN = ((11.8, 13.4), (13.4, 15.8), (19.8, 21.5))               # shots 6, 7, 9 (cameras 6 and 7)
NO_BOARD = ((15.8, 19.8),)                                          # shot 8 (motion test A's camera)
NO_PARTY = ((0.0, 2.4), (6.7, 9.5), (13.4, 15.8), (19.8, 21.5), (25.5, 26.9))   # v4: + shots 1 and 4 (boxes beside Don)
TIPS = {}
_saved = {}


def banner2(k, x0=None, x1=None, y=None, words=None):
    """Two rows of bunting, the same flags, both inside the widest camera (world x 118-550)."""
    xs_banner = _saved["banner"]
    xs_banner(k, 140, 520, 176, "MERRY CHRISTMAS")
    step = (520 - 140) / 15
    xs_banner(k, 140, 140 + 6 * step, 208, "TO ALL")                 # under MERRY: out of the push-in's frame


def wall2(k):
    c = k.c
    rect(k, -600, -400, 2200, xs.FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -600, xs.FLOOR_Y, 2200, 900, kit.FLOOR, 101, shadow=False)
    rect(k, -600, xs.FLOOR_Y - 10, 2200, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    t = xa.ACT.get("t", 0.0)
    y = 340 if SHOT11[0] <= t < SHOT11[1] else 300                  # lower in the last shot's tight frame
    if not any(a <= t < b for a, b in NO_SIGN):                      # left out where the camera would cut it
        pt42.wall_sign(k, 340, y, 30)


def badge_high(k, body_top, seed):
    """Sofia's badge, raised above the forearm of her ornament pose."""
    c = k.c
    rect(k, 5, body_top + 30, 34, 20, (1, 1, 1), seed + 40, shadow=False, lw=1.8)
    c.set_source_rgb(*brand.GREEN); c.rectangle(8, body_top + 32, 28, 3.5); c.fill()
    text(k, "SOFÍA", 22, body_top + 42, 9.5, INK)


def razor_floor(k, hand, s=1.0, ang=-0.9, seed=540):
    """The razor on its own (no fingers), a size bigger, with a blob of foam on the blade."""
    t = xa.ACT.get("t", 0.0)
    if not (SHOT11[0] <= t < SHOT11[1]):
        return _saved["razor"](k, hand, s, ang, seed)
    c = k.c
    hx, hy = hand
    s *= 1.3
    c.save(); c.translate(hx, hy); c.scale(s, s); c.rotate(ang)
    rect(k, -4, -30, 8, 40, dx.RAZOR, seed, shadow=False, lw=1.8)                   # the handle
    rect(k, -11, -40, 22, 10, (0.88, 0.90, 0.93), seed + 1, shadow=False, lw=1.8)   # the head
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.move_to(-9, -35); c.line_to(9, -35); c.stroke()
    for fx, fy, r in ((-5, -44, 5), (2, -46, 6), (8, -43, 4.5)):                     # the foam
        ellipse(k, fx, fy, r, r, (1, 1, 1), seed + 5, shadow=False, lw=1.2)
    c.restore()


def top2(cam, x, feet, hy, lift=62):
    """The anchor that places the box is unchanged; the speaker's head and mouth are remembered (by the anchor's
    x) for _tail2's curved tail."""
    a = _saved["top"](cam, x, feet, hy, lift)
    hx, hy_s = xs.to_screen(cam, x, feet + hy)
    z = cam[2]
    robot = lift >= 100
    TIPS[round(a[0], 1)] = dict(head=(hx, hy_s), z=z, robot=robot)
    return a


def _tail2(c, bx, by, bw, bh, ax, ay, width=13):
    info = TIPS.get(round(ax, 1))
    if not info or ay < by:                                    # off-screen speakers and boxes below: as before
        return _saved["tail"](c, bx, by, bw, bh, ax, ay, width)
    hx, hy = info["head"]; z = info["z"]
    if info["robot"]:
        mouth_dy, corner, outside = 14 * z, 24 * z, 66 * z
    else:
        mouth_dy, corner, outside = 27 * z, 17 * z, 58 * z
    cx_box = bx + bw / 2
    side = 1 if cx_box >= hx else -1                           # come in from the box's side
    tip = (hx + side * corner, hy + mouth_dy)
    if not info["robot"] and MOUTHS:                           # the mouth as actually drawn this frame, if near
        best = None
        for dxy in MOUTHS:
            mx, my = c.device_to_user(*dxy)
            dd = (mx - hx) ** 2 + (my - hy - mouth_dy) ** 2
            if dd < (70 * z) ** 2 and (best is None or dd < best[0]):
                best = (dd, mx, my)
        if best:
            hx = best[1] - side * 2 * z
            tip = (best[1] + side * 15 * z, best[2])
    ctrl = (hx + side * outside, hy - 6 * z)                   # around the outside of the head
    ex = min(max(hx + side * outside * 0.6, bx + 26), bx + bw - 26)
    base = (ex, by + bh - 2)
    pts_l, pts_r = [], []
    n = 14
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * base[0] + 2 * (1 - t) * t * ctrl[0] + t * t * tip[0]
        y = (1 - t) ** 2 * base[1] + 2 * (1 - t) * t * ctrl[1] + t * t * tip[1]
        dx = 2 * (1 - t) * (ctrl[0] - base[0]) + 2 * t * (tip[0] - ctrl[0])
        dy = 2 * (1 - t) * (ctrl[1] - base[1]) + 2 * t * (tip[1] - ctrl[1])
        ln = (dx * dx + dy * dy) ** 0.5 or 1
        w = width * (1 - t) ** 1.1
        pts_l.append((x - dy / ln * w, y + dx / ln * w)); pts_r.append((x + dy / ln * w, y - dx / ln * w))
    return pts_l + pts_r[::-1]


def _speech_poly():
    """xmas_bubbles.speech with tails drawn as polygons of any length (the curved tails)."""
    import inspect
    src = inspect.getsource(_saved.get("speech0") or xb.speech)
    src = src.replace("c.move_to(*tl[0]); c.line_to(*tl[1]); c.line_to(*tl[2]); c.close_path()",
                      "c.move_to(*tl[0]); [c.line_to(*q) for q in tl[1:]]; c.close_path()")
    ns = dict(xb.__dict__)
    exec(src, ns)
    return ns["speech"], ns


def board2(k, x, y, w=118, h=86):
    t = xa.ACT.get("t", 0.0)
    if any(a <= t < b for a, b in NO_BOARD):
        return
    _saved["board"](k, x, y, w, h)


def door2(k, x=None, open_amt=0.0):
    t = xa.ACT.get("t", 0.0)
    x = xs.POS["door_x"] if x is None else x
    if not any(a <= t < b for a, b in NO_PARTY):
        return kit.door(k, x, xs.FLOOR_Y - 250, 110, 250, 960, open_amt=open_amt, sign="PARTY")
    c = k.c; y = xs.FLOOR_Y - 250
    c.save(); c.rectangle(x - 40, y - 12, 200, 400); c.clip()                 # the door without its sign above it
    try:
        kit.door(k, x, y, 110, 250, 960, open_amt=open_amt, sign="PARTY")
    finally:
        c.restore()


def _mouth_rec(k, x, my, code, *a, **kw):
    MOUTHS.append(k.c.user_to_device(x, my))
    return _saved["mouth"](k, x, my, code, *a, **kw)


def _on():
    MOUTHS.clear()
    _saved["mouth"] = imo.mouth
    imo.mouth = _mouth_rec
    _saved.update(banner=xs.banner, wall=xs.wall, razor=dx.razor, top=sb.top, hook=sx.BADGE_HOOK, tail=xb._tail,
                  board=xs.incident_board, door=xs.door)
    xs.banner, xs.wall, dx.razor, sb.top = banner2, wall2, razor_floor, top2
    xb._tail, xs.incident_board, xs.door = _tail2, board2, door2
    _saved["speech"] = xb.speech
    xb.speech = speech4
    sx.BADGE_HOOK = badge_high
    route.apply()


def _off():
    route.restore()
    xs.banner, xs.wall, dx.razor, sb.top = _saved["banner"], _saved["wall"], _saved["razor"], _saved["top"]
    xb._tail, xs.incident_board, xs.door = _saved["tail"], _saved["board"], _saved["door"]
    xb.speech = _saved["speech"]
    imo.mouth = _saved["mouth"]
    TIPS.clear()
    sx.BADGE_HOOK = _saved["hook"]


def _wrap(fn):
    def panel(k, t, tl):
        xa.RAW_T = RAW_T
        _on()
        try:
            fn(k, t, tl)
        finally:
            _off()
    panel.__name__ = getattr(fn, "__name__", "panel")
    return panel


LOG = []                                                       # v4 probe: what each bubble knew
# v4 (fourth tail review): every box placed by hand clear of the speaker's head, hat, cap or mask; the tail leaves
# the box outside the face, runs down beside it and hooks in level with the mouth actually drawn this frame.
# (x, y) = the box's top-left, size, the text as laid out, the side the tail comes from (+1 right, -1 left);
# tip="edge": an off-screen speaker (to the frame edge at edge_y); icon: an emoticon at the box's right end.
V4 = {
    "Sorry. Getting ready\nfor the ball.": [dict(x=None, y=150, size=22, text="Sorry.\nGetting ready\nfor the ball.", side=1)],
    "Nice balls.\nI've got two for you.": [dict(x=356, y=118, size=23, text="Nice balls.\nI've got two\nfor you.", side=1)],
    "Eww.": [dict(x=18, y=112, size=30, text="Eww.", side=-1, who=0, icon="roll"),
             dict(x=None, y=112, size=30, text="Eww.", side=1, who=1, icon="queasy", delay=0.25, reach=511)],
    "Violation resolved.": [dict(x=196, y=104, size=26, text="Violation resolved.", side=1)],
    "Get him.": [dict(x=222, y=234, size=30, text="Get him.", side=1)],          # under the sign, off her cap
    "Human in the loop.": [dict(x=None, y=158, size=26, text="Human in the loop.", side=1)],
    "Merry Christmas, Don.": [dict(x=18, y=380, size=22, text="Merry\nChristmas,\nDon.", tip="edge", edge_y=440,
                                   sweet=True)],
    "Happy compliance!": [dict(x=None, y=170, size=25, text="Happy\ncompliance!", side=1)],
}


def _emoticon(c, kind, cx, cy, r):
    c.save()
    face = (1.0, 0.82, 0.25) if kind == "roll" else (0.62, 0.84, 0.42)
    c.arc(cx, cy, r, 0, 2 * math.pi); c.set_source_rgb(*face); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    if kind == "roll":                                           # the eye-roll: pupils up, a flat mouth
        for sx_ in (-1, 1):
            c.arc(cx + sx_ * r * 0.36, cy - r * 0.12, r * 0.24, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
            c.arc(cx + sx_ * r * 0.36, cy - r * 0.26, r * 0.10, 0, 2 * math.pi); c.fill()
        c.set_line_width(2.2); c.move_to(cx - r * 0.35, cy + r * 0.45); c.line_to(cx + r * 0.35, cy + r * 0.40); c.stroke()
    else:                                                        # queasy: squeezed eyes, puffed cheeks, wavy mouth
        c.set_line_width(2.0)
        for sx_ in (-1, 1):
            ex = cx + sx_ * r * 0.36
            c.move_to(ex - r * 0.18, cy - r * 0.30); c.line_to(ex + r * 0.18 * 0, cy - r * 0.18); c.line_to(ex + r * 0.18, cy - r * 0.30)
            c.stroke()
            c.arc(cx + sx_ * r * 0.62, cy + r * 0.22, r * 0.17, 0, 2 * math.pi); c.set_source_rgb(0.45, 0.70, 0.30); c.fill()
            c.set_source_rgb(*INK)
        c.move_to(cx - r * 0.42, cy + r * 0.42)
        for i in range(1, 5):
            c.line_to(cx - r * 0.42 + i * r * 0.21, cy + r * (0.32 if i % 2 else 0.48))
        c.stroke()
    c.restore()


def _mouth_tip(c, info, side):
    """The speaker's mouth this frame (MOUTHS) or its usual place; the tip sits just beside it."""
    hx, hy = info["head"]; z = info["z"]
    if info["robot"]:
        mx, my, R = hx, hy + 15 * z, 44 * z
        return (mx + side * 13 * z, my), (mx, my), R
    mx, my, R = hx, hy + 27 * z, 37 * z
    best = None
    for dxy in MOUTHS:
        x_, y_ = c.device_to_user(*dxy)
        dd = (x_ - hx) ** 2 + (y_ - hy - 27 * z) ** 2
        if dd < (70 * z) ** 2 and (best is None or dd < best[0]):
            best = (dd, x_, y_)
    if best:
        mx, my = best[1], best[2]
    return (mx + side * 11 * z, my), (mx, my), R


def _bubble4(k, B, info, t, t0):
    c = k.c
    lines = B["text"].split("\n"); size = B["size"]
    tw, lh = xb._measure(c, lines, size)
    icon = B.get("icon")
    iw = 44 if icon else 0
    bw, bh = tw + 2 * xb.PAD_X + iw, lh * len(lines) + 2 * xb.PAD_Y
    bx = B["x"] if B["x"] is not None else xb.SAFE[2] - bw
    by = B["y"]
    t0 = t0 + B.get("delay", 0.0)
    if t < t0:
        return None
    if B.get("tip") == "edge":
        tip, mouth, head = (-14, B["edge_y"]), None, None
        base = (bx + 3, min(max(B["edge_y"] - 20, by + 22), by + bh - 22))
        p1 = (base[0] + (tip[0] - base[0]) / 3, base[1] + (tip[1] - base[1]) / 3)
        p2 = (base[0] + 2 * (tip[0] - base[0]) / 3, base[1] + 2 * (tip[1] - base[1]) / 3)
    else:
        side = B["side"]
        tip, mouth, R = _mouth_tip(c, info, side)
        hx, hy = info["head"]
        ox = B.get("reach", hx + side * (R + 12))
        base = (min(max(ox, bx + 26), bx + bw - 26), by + bh - 3)
        if (base[0] - hx) * side > R + 12 and "reach" not in B:
            ox = base[0]
        p1 = (ox, base[1] + 0.45 * (tip[1] - base[1]))
        p2 = (ox, tip[1])
        head = (hx, hy, R)
    L, Rr = [], []
    n = 24
    for i in range(n + 1):
        u = i / n; a, b_, c_, d_ = (1 - u) ** 3, 3 * (1 - u) ** 2 * u, 3 * (1 - u) * u * u, u ** 3
        px = a * base[0] + b_ * p1[0] + c_ * p2[0] + d_ * tip[0]
        py = a * base[1] + b_ * p1[1] + c_ * p2[1] + d_ * tip[1]
        dx_ = 3 * (1 - u) ** 2 * (p1[0] - base[0]) + 6 * (1 - u) * u * (p2[0] - p1[0]) + 3 * u * u * (tip[0] - p2[0])
        dy_ = 3 * (1 - u) ** 2 * (p1[1] - base[1]) + 6 * (1 - u) * u * (p2[1] - p1[1]) + 3 * u * u * (tip[1] - p2[1])
        ln = math.hypot(dx_, dy_) or 1
        wd = 12 * (1 - u) ** 1.1
        L.append((px - dy_ / ln * wd, py + dx_ / ln * wd)); Rr.append((px + dy_ / ln * wd, py - dx_ / ln * wd))
    poly = L + Rr[::-1]
    p = xb._pop(t, t0)
    c.save(); c.translate(bx + bw / 2, by + bh / 2); c.scale(p, p); c.translate(-(bx + bw / 2), -(by + bh / 2))
    c.set_line_join(1)

    def shapes():
        c.new_path(); c.move_to(*poly[0]); [c.line_to(*q) for q in poly[1:]]; c.close_path()
        xb._round_rect(c, bx, by, bw, bh, 16)
    shapes(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    shapes(); c.set_source_rgb(1, 1, 1); c.fill()
    c.select_font_face(xb.FONT); c.set_font_size(size); c.set_source_rgb(*INK)
    for i, l in enumerate(lines):
        e = c.text_extents(l)
        c.move_to(bx + (bw - iw) / 2 - e.x_advance / 2, by + xb.PAD_Y + lh * i + size * 0.88); c.show_text(l)
    if icon:
        _emoticon(c, icon, bx + bw - xb.PAD_X - 14, by + bh / 2, 17)
    if B.get("sweet"):
        c.set_source_rgb(0.86, 0.10, 0.16)
        hx_, hy_, hs = bx + bw - 10, by + 8, 7
        c.move_to(hx_, hy_ + hs * 0.9); c.curve_to(hx_ - hs * 1.5, hy_ - hs * 0.2, hx_ - hs * 0.7, hy_ - hs * 1.2, hx_, hy_ - hs * 0.4)
        c.curve_to(hx_ + hs * 0.7, hy_ - hs * 1.2, hx_ + hs * 1.5, hy_ - hs * 0.2, hx_, hy_ + hs * 0.9); c.fill()
    c.restore()
    return dict(box=(bx, by, bw, bh), tip=tip, mouth=mouth, head=head, poly=poly)


def speech4(k, s, anchors, t, t0, side="up", size=28, at=None, fill=(1, 1, 1), italic_sweet=False):
    a = [anchors] if isinstance(anchors, tuple) else anchors
    rec = dict(s=s, t=t, anchors=a, tips={kk: dict(v) for kk, v in TIPS.items()},
               mouths=[k.c.device_to_user(*m) for m in MOUTHS], drawn=[])
    LOG.append(rec)
    if s not in V4:
        return SPEECH(k, s, anchors, t, t0, side, size, at, fill, italic_sweet)
    for B in V4[s]:
        info = None
        if B.get("tip") != "edge":
            ax = a[B.get("who", 0)][0]
            info = TIPS.get(round(ax, 1))
        rec["drawn"].append(_bubble4(k, B, info, t, t0))


SPEECH, _NS = _speech_poly()
_NS["_tail"] = lambda *a, **k: xb._tail(*a, **k)            # the copy looks the tail up live (patched per frame)
PANELS = [(t0, t1, _wrap(fn)) for t0, t1, fn in xa.PANELS]
