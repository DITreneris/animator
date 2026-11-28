"""THE DOUBLE AGENT (episode 15): the cups' canon (Tomas 28 Nov: "visi puodeliai laikomi bet kaip, jokio kanono nera").

One size, three holds, every vessel registered with the hand gate by its own drawer (da_hand_gate.vessel), so the gate
checks the hold at the handle or the base it really drew, not a box typed at a wrist.

  size   a mug's scale = MUG_K x its holder's rig scale (1.7: the locked S8 final image's mug, 1.15 beside Pam at 0.66);
         a cup and saucer = CUP_K x the rig scale
  holds  by the handle   CUP_GRIP, the vessel drawn first, the fist closed on its handle    by_handle()
         on a palm       SAUCER_SUPPORT, the vessel standing on it, the thumb over its rim  on_palm()
         by its body     GRAB, someone taking it from a hand that has its handle            by_body()
  never  a GRAB or a fist beside a mug; a mug drawn in scene coordinates at an offset from a wrist (rules 60, 61)

Vessels: "mustard" (Pam's, ds.pam_mug v2), "gift" (the same with the gold bow, on its body: a hand takes the handle),
"blue" (her old one, the same silhouette), "cup" (Don's white cup on its saucer), "jug" (the coffee pot).
"""
import math

import da_set as ds
import da_props as dpr
import da_hand_gate as g
import kit

MUG_FLOOR, MUG_S8 = 0.92, 1.15   # ONE size per space (the outside review, 28 Nov: the holder's scale must not resize the
CUP_FLOOR = 0.65                  # prop when it changes hands): the floor's mug 0.92 = the locked S8 image's 1.15 x 0.54/0.66
BLUE = dpr.BLUE_MUG
CERAMIC = [True]                  # mug v3 (the review: v2's dark top oval and hard shine read as a metal tankard): matt
                                  # glaze, a light rim, coffee inside, a wider handle ring. False: ds.pam_mug v2 (S8's)
_IN = [0]
HC = 22.5                         # the handle's grip point: its ring's outer middle, x from the base's middle (x s)


def _mug_v3(k, s, col):
    c = k.c
    INK = kit.INK
    lite = tuple(min(1.0, v * 1.18 + 0.06) for v in col)
    hx, hy = 13 * s, -15 * s
    c.new_path(); c.arc(hx, hy, 12.5 * s, -1.78, 1.78); c.arc_negative(hx, hy, 8.0 * s, 1.62, -1.62); c.close_path()   # its ends
    # under the body (3.2b's insert at 6x showed a gap between the ring and the wall)
    c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2 * s ** 0.5); c.stroke()
    w, h, r = 13 * s, 30 * s, 4 * s
    c.new_path(); c.move_to(-w, -h); c.line_to(-w, -r); c.curve_to(-w, 0, -w + r, 0, -w + 2 * r, 0)
    c.line_to(w - 2 * r, 0); c.curve_to(w - r, 0, w, 0, w, -r); c.line_to(w, -h); c.close_path()
    c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.set_source_rgba(0, 0, 0, 0.09); c.rectangle(5 * s, -27 * s, 7 * s, 25 * s); c.fill()          # a soft shaded side
    c.set_source_rgba(1, 1, 1, 0.16); c.rectangle(-9 * s, -25 * s, 2.2 * s, 18 * s); c.fill()       # a matt highlight
    for rx, ry, fill in ((w, 3.6 * s, lite), (w - 2.2 * s, 2.5 * s, (0.97, 0.93, 0.84)), (w - 4.2 * s, 1.7 * s, (0.36, 0.22, 0.12))):
        c.save(); c.translate(0, -h); c.scale(rx, ry); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*fill); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()


def mug(k, x, y, s, handle=1, kind="mustard", state="rest", name=None):
    """a mug standing on (x, y) (its base's middle), its handle on screen side `handle`."""
    c = k.c
    _IN[0] += 1
    keep_v2, keep_col = ds.MUG_V2[0], ds.MUG
    ds.MUG_V2[0] = True
    col = BLUE if kind == "blue" else keep_col
    try:
        c.save(); c.translate(x, y); c.scale(handle, 1)
        if CERAMIC[0]:
            _mug_v3(k, s, col)
        else:
            ds.MUG = col
            _RAW["pam_mug"](k, 0, 0, s)
        c.restore()
        if kind == "gift":                                     # the bow on its body's front, clear of the handle
            dpr.bow_v2(k, x - handle * 3 * s, y - 13 * s, 0.7 * s)
    finally:
        ds.MUG_V2[0], ds.MUG = keep_v2, keep_col
        _IN[0] -= 1
    g.vessel(k, name or kind, state, handle=(x + handle * HC * s, y - 15 * s), base=(x, y),
             rect=(x - 14 * s - (12 * s if handle < 0 else 0), y - 34 * s, 40 * s, 36 * s))


def thumb_on_handle(k, x, y, s, handle, w, skin):
    """over the fist: the thumb lying along the top of the handle's ring, toward the mug's wall (the review: the
    thumb on top, the fingers through the ring)."""
    cx, cy = x + handle * 13 * s, y - 15 * s
    a = (cx + handle * 12 * s, cy - 6.5 * s); b = (cx + handle * 2.5 * s, cy - 11.0 * s)
    c = k.c
    c.set_line_cap(1)
    for col, lw in ((kit.INK, 0.36 * w + 2.4), (skin, 0.36 * w)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.move_to(*a); c.line_to(*b); c.stroke()
    c.set_line_cap(0)
    c.set_source_rgba(*kit.INK, 0.6); c.set_line_width(1.0)                                    # the nail
    c.new_path(); c.arc(b[0], b[1], 0.11 * w, 0, 2 * math.pi); c.stroke()


def thumb_on_body(k, x, y, s, from_side, w, skin):
    """a hand taking the mug by its body from the side `from_side` (GRAB drawn before the mug: its palm behind it):
    the four fingers wrap round the near wall, over the front, their tips short of the middle (the cold test 28 Nov:
    one thumb drawn across the mug read as "a stick poking through it")."""
    c = k.c
    fs = from_side
    fw = 0.17 * w                                               # a finger's width
    for i in range(4):
        yy = y - (24 - i * 1.02 * fw / s) * s
        x0, x1 = x + fs * 14.5 * s, x + fs * (6.5 + 1.2 * (i == 0) - 1.0 * (i == 3)) * s
        c.set_line_cap(1)
        for col, lw in ((kit.INK, fw + 2.2), (skin, fw)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.move_to(x0, yy); c.line_to(x1, yy); c.stroke()
        c.set_line_cap(0)
    c.set_source_rgba(*kit.INK, 0.5); c.set_line_width(1.0)    # the knuckle line at the wall's edge
    c.new_path(); c.move_to(x + fs * 12.5 * s, y - 25.5 * s); c.line_to(x + fs * 12.5 * s, y - 24 * s + 3.2 * fw); c.stroke()


def stream(k, lip, mug_base, s, wob=0.0):
    """the pour: from the jug's lip into the mug's mouth: wide, lighter than the coffee in the jug, a highlight."""
    c = k.c
    mx, my = mug_base[0], mug_base[1] - 30 * s
    c.set_line_cap(1)
    for col, lw in ((kit.INK, 6.5 * s + 2), ((0.52, 0.32, 0.16), 6.5 * s), ((0.80, 0.60, 0.40), 1.6 * s)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.move_to(*lip)
        c.curve_to(lip[0] + (mx - lip[0]) * 0.55 + wob, lip[1] + 1 * s, mx + wob, lip[1] + (my - lip[1]) * 0.35, mx, my + 1.0 * s); c.stroke()
    c.set_line_cap(0)


def cup_saucer(k, x, y, s, state="rest", slop=False):
    """Don's white cup on its saucer; (x, y): the saucer's underside middle."""
    _IN[0] += 1
    try:
        _RAW["cup_and_saucer_v2"](k, x, y - 2 * s, s, slop=slop)
    finally:
        _IN[0] -= 1
    g.vessel(k, "cup", state, handle=(x + 21.5 * 0.9 * s, y - 2 * s - 4 * s - 12 * 0.9 * s), base=(x, y),
             rect=(x - 32 * s, y - 34 * s, 64 * s, 38 * s))


def jug(k, hx, hy, s, tilt, handle=-1, state="held"):
    """the coffee pot with its handle's middle at (hx, hy), its handle on side `handle`, tipped by tilt toward the
    other side (its lip)."""
    import da_layouts as L
    c = k.c
    a = -handle * tilt
    lx, ly = handle * 31 * s, -16 * s                           # the handle's middle, local
    x = hx - (lx * math.cos(a) - ly * math.sin(a))
    y = hy - (lx * math.sin(a) + ly * math.cos(a))
    c.save(); c.translate(x, y); c.rotate(a); c.scale(handle, 1)
    L.coffee_pot(k, 0, 0, s, 0.0)
    c.restore()
    g.vessel(k, "jug", state, handle=(hx, hy), base=(x, y), rect=(x - 40 * s, y - 44 * s, 80 * s, 52 * s))
    px, py = -handle * 16 * s, -34 * s                          # its lip, for the stream
    return (x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a))


# ---- the holds: rig_hands jobs ------------------------------------------------------------------------------------------
def _away(info):
    """which side of the hand the vessel sits on: away from the arm it hangs from."""
    dx = info["d"][0]
    return (1 if dx > 0 else -1) if abs(dx) > 0.35 else info["arm"]


def by_handle(T, s, kind="mustard", out=None, name=None, tilt_jug=None, got=None):
    """CUP_GRIP: the vessel first, the fist closed on its handle. got: a dict that receives the vessel's base (x, y)
    and its lip (the jug)."""
    def obj(k, P, w, info):
        side = _away(info)                                      # the vessel beyond the hand; its handle toward the hand
        if kind == "jug":
            lip = jug(k, P[0], P[1], s, tilt_jug or 0.0, handle=-side)
            if got is not None:
                got["lip"] = lip
            return
        x, y = P[0] + side * HC * s, P[1] + 15 * s
        mug(k, x, y, s, handle=-side, kind=kind, state="held", name=name)
        if got is not None:
            got["base"] = (x, y); got["handle"] = -side

    def front(k, P, w, info):
        if kind != "jug":
            side = _away(info)
            thumb_on_handle(k, P[0] + side * HC * s, P[1] + 15 * s, s, -side, w, info["skin"])
    j = dict(T=T, pose="CUP_GRIP", obj=obj, front=front, contact="handle", behind=True, reach=True, obj_info=True)
    if out is not None:
        j["out"] = out
    return j


def on_palm(T, s, kind="cup", out=None, got=None, slop=False, handle=1):
    """SAUCER_SUPPORT: the palm up and level, the vessel standing on it, the thumb over its near rim."""
    def obj(k, P, w, info):
        if kind == "cup":
            cup_saucer(k, P[0], P[1], s, state="held", slop=slop)
        else:
            mug(k, P[0], P[1] - 1, s, handle=handle, kind=kind, state="held")
        if got is not None:
            got["base"] = P
    j = dict(T=T, pose="SAUCER_SUPPORT", obj=obj, contact="saucer", reach=True, obj_info=True)
    if out is not None:
        j["out"] = out
    return j


def palm_under(base, w, arm, out=None):
    """the wrist for a SAUCER_SUPPORT palm (no vessel of its own) under a vessel someone else's job draws: the
    hand-over's second hand, the cradle's lower hand. base: that vessel's base; w: this hand's width."""
    j = dict(T=(base[0] - arm * 0.98 * w, base[1] + 0.36 * w + 1), pose="SAUCER_SUPPORT", reach=True)
    if out is not None:
        j["out"] = out
    return j


def hand_w(rig_scale, sex="m"):
    return (17 if sex == "m" else 15) * 1.15 * 1.25 * rig_scale


def by_body(T, out=None):
    """GRAB on a mug's body (someone taking it): the mug is drawn by its holder; this hand closes over it."""
    j = dict(T=T, pose="GRAB", reach=True)
    if out is not None:
        j["out"] = out
    return j


# ---- raw drawers called past this module fail the gate -------------------------------------------------------------
_RAW = {}


def install():
    if _RAW:
        return
    _RAW["pam_mug"] = ds.pam_mug
    _RAW["cup_and_saucer_v2"] = dpr.cup_and_saucer_v2

    def pam_mug(k, x, y, s=1.0):
        r = _RAW["pam_mug"](k, x, y, s)
        if not _IN[0]:
            g.vessel(k, "mug (raw ds.pam_mug)", "unknown", base=(x, y), rect=(x - 14 * s, y - 34 * s, 37 * s, 36 * s))
        return r

    def cup_and_saucer_v2(k, x, y, s=1.0, slop=False):
        r = _RAW["cup_and_saucer_v2"](k, x, y, s, slop=slop)
        if not _IN[0]:
            g.vessel(k, "cup (raw cup_and_saucer_v2)", "unknown", base=(x, y), rect=(x - 32 * s, y - 34 * s, 64 * s, 38 * s))
        return r
    ds.pam_mug = pam_mug
    dpr.cup_and_saucer_v2 = cup_and_saucer_v2
