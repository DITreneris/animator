"""ANIMATION v4 of "Secret Santa" (18 Nov): the fixes from two cold mute viewers and Tomas's notes. Wraps animation v3
(ss_anim3.py, kept and unchanged; it wraps v2):
- cold open: both viewers thought the stamp made the lip print. Now Pam's chin and freshly painted lips come down from
  the top of the frame and press the tag (0.06-0.50 s), the print stays, and only then THUNK (0.62 s);
- 0:01-0:08 (shots 1 and 2): the UptimeZ sign is off the wall (the bubbles sat on it), each bubble sits just above its
  speaker's head with a short tail, and one bubble at a time (Pam's goes when Sofia speaks);
- shot 4: both viewers took the held-out glasses for "a spoon". During "Agent Santa. Licensed to gift." a full-screen
  insert: her half-moon reading glasses, Don's mirrored, smug face in both lenses, her fingers on the frame;
- shot 15 (0:35-0:40): eleven pieces of text in one wide frame. Now the wide has no signs, no UNCLAIMED card and no
  "(SECRET!)"; the payoff is an insert: her barred tag above, his TO: SOFIA (heart) / FROM: DON below, and APPROVED
  stamps down on his (the THUNK and the tick at 37.9 s); "You're welcome." over it, then the wide for the faces.
Sound: ss_sound_v4.py. Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import cairo
import kit
from kit import Ctx, INK
import ss_anim as A
import ss_anim3 as M3
import ss_sb as sb
import ss_set as S
import ss_motion as mo
import pam_sheet_ss as pss
import props_ss as props
import robot_ss as rs
import pam_mf as pm
import pt42
import xmas_bubbles as xb

DURATION = A.DURATION
RAW_T = 0.0
X = S.POS

# ---------------------------------------------------------------- the wall without signs, per shot
NOSIGN, NOSANTA = [False], [False]
_wall0 = S.wall


def wall(k, t=0.0):
    if not (NOSIGN[0] or NOSANTA[0]):
        return _wall0(k, t)
    kit.rect(k, -600, -400, 2400, S.FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
    kit.rect(k, -600, S.FLOOR_Y, 2400, 900, kit.FLOOR, 101, shadow=False)
    kit.rect(k, -600, S.FLOOR_Y - 10, 2400, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    if not NOSIGN[0]:
        pt42.wall_sign(k, 580, 326, 26)
    S.paper_chains(k)
    if not NOSANTA[0]:
        S.santa_sign(k)


S.wall = wall


# ---------------------------------------------------------------- cold open: her lips on the tag, then THUNK
T_DOWN, T_PRESS, T_UP, T_HIT, T_UNCAP = 0.06, 0.24, 0.34, 0.66, 0.72
ROSE = (0.80, 0.42, 0.48)


_PH = [None]


def lips_from_top(k, bx, by, dy):
    """Pam herself, leaning in from the top edge: her head (glasses, bob, painted lips), cut off under the chin, with
    her lips at (bx, by + dy)."""
    c = k.c
    if _PH[0] is None:
        _PH[0] = sb.ps.pam(Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0), 0, 0, 1.0, "stand",
                           "neutral", look=(0, 1))["head"]
    hx, hy = _PH[0]
    s = 0.48
    c.save()
    c.translate(bx, by + dy); c.scale(s, s); c.translate(-hx, -(hy + 32))     # her mouth is 32 under the head point
    c.rectangle(hx - 200, hy - 400, 400, 400 + 42); c.clip()                    # head only: cut under the chin
    sb.ps.pam(Ctx(c, 0), 0, 0, 1.0, "stand", "neutral", look=(0, 1))
    c.restore()


def cold(k, t, tl):
    if tl < 1 / 12:
        sb.screen(Ctx(k.c, 0), tl, "s1", lambda: M3.frame0(Ctx(k.c, 0)))
        return

    def d():
        c = k.c
        M3._bg(k)
        dx, dy = mo.shake(tl, T_HIT, 1.4, seed=21)
        c.save(); c.translate(dx, dy)
        x, y = M3.TAG[0], M3.TAG[1]
        bx, by = x + 23 * M3.TAG[2], y + 10.5 * M3.TAG[2]
        M3.tag(k, x, y, kissed=tl >= T_PRESS + 0.04, barred=tl >= T_HIT)
        if T_DOWN < tl < T_UP + 0.14:
            if tl < T_PRESS:
                off = -170 * (1 - sb.ease((tl - T_DOWN) / (T_PRESS - T_DOWN)))
            elif tl < T_UP:
                off = 1.5                                            # pressed, a little squash
            else:
                off = -170 * sb.ease((tl - T_UP) / 0.14)
            lips_from_top(k, bx, by, off)
        lift = mo.stamp_track(tl, T_HIT, 70, up_after=0.2)
        if tl > T_HIT - 0.16 and lift < 69:                        # only after her head has gone
            rs.stamp_prop(k, bx, by - lift - 3, 0.6, "down" if lift < 1 else "up", 0.0, 7)
            if T_HIT <= tl < T_HIT + 0.18:
                rs.impact_lines(c, bx, by, 1, 0.6)
        c.restore()
        sb.sss.pam_hand(k, sb.ease((tl - T_UNCAP) / 0.3))
    sb.screen(k, tl, "s1", d)


# ---------------------------------------------------------------- shots 1 and 2: no sign, bubbles at the head
def s1_rest(k, t, tl):
    """sb.s1 from 1.0 s on, without the sign, Pam's whisper just over her head and gone when Sofia speaks."""
    u = sb.ease((tl - 1.0) / 0.35)
    hand = (X["pam"] + 40, S.FEET - 196)
    cam = (sb.lerp(hand[0], sb.CAM1[0], u), sb.lerp(hand[1], sb.CAM1[1], u), sb.lerp(5.0, sb.CAM1[2], u))

    def draw():
        S.backdrop(k, t=tl)
        o2 = sb.sss.sofia_seated(k, "stand", "neutral", look=(-0.8, 0.1), sparkle=0.4 if tl > 2.6 else 0.0,
                                 mouth=sb.talk(tl, 2.6, 3.4))
        S.desk(k)
        o = sb.ps.pam(k, X["pam"] + 40, S.FEET, 1.0, sb.ps.POSE_WHISPER, "neutral",
                      look=(1, 0) if tl < 2.0 or tl > 2.4 else (-1, 0), lips=None, mouth=sb.talk(tl, 1.4, 2.5, 5),
                      lean=4)
        sb.lipstick_in_hand(k, o, 1.0, 1.0)
        return o, o2
    NOSIGN[0] = True
    try:
        o, o2 = sb.world(k, tl, "s1", cam, draw)
    finally:
        NOSIGN[0] = False
    if u >= 1:
        if tl < 2.6:
            sb.whisper(k, "Sofía… do you think\nI could pull off nude?", sb.above(cam, o["head"], 70), t, 1.35,
                       at=(200, 292))
        else:
            xb.speech(k, "On your lips, Pam.", sb.above(cam, o2["head"] if "head" in o2 else (X["sofia"], 480), 80),
                      t, 2.6, size=26, at=(400, 398))


def s1_new(k, t, tl):
    return cold(k, t, tl) if tl < 1.0 else s1_rest(k, t, tl)


def s2_new(k, t, tl):
    def draw():
        S.backdrop(k, t=tl)
        o2 = sb.sss.sofia_seated(k, "compact", "knowing" if tl > 1.5 else "neutral", look=(-0.8, 0.1),
                                 compact_open=1.0, mouth=sb.talk(tl, 1.15, 1.8))
        S.desk(k)
        o = sb.ps.pam(k, X["pam"] + 40, S.FEET, 1.0, "stand", "neutral",
                      look=(-1, 0.1) if 0.45 < tl < 1.0 else (0.6, 0.2), apply=True, mouth=sb.talk(tl, 0.15, 0.8, 6))
        return o, o2
    NOSIGN[0] = True
    try:
        o, o2 = sb.world(k, tl, "s2b", sb.CAM2, draw)
    finally:
        NOSIGN[0] = False
    if tl < 1.15:
        xb.speech(k, "Would Don notice?", sb.above(sb.CAM2, o["head"], 70), t, 0.1, size=26, at=(170, 282))
    else:
        anc = sb.above(sb.CAM2, o2["head"], 60) if sb.TAIL_FIX[0] else sb.above(sb.CAM2, (X["sofia"], 470), 60)
        xb.speech(k, "Don notices mirrors.", anc, t, 1.15, size=26, at=(392, 432))


# ---------------------------------------------------------------- shot 4: his face in her lenses
G0, G1 = 1.15, 1.95                         # storyboard time of the insert inside shot 4
LENS = ((27, 84), (71, 84))                 # lens centres (98 x 174 units)
LW, LH = 38, 28


def _lens_path(c, cx, cy):
    c.move_to(cx - LW / 2, cy - LH / 2); c.line_to(cx + LW / 2, cy - LH / 2)
    c.curve_to(cx + LW / 2, cy + LH * 0.85, cx - LW / 2, cy + LH * 0.85, cx - LW / 2, cy - LH / 2); c.close_path()


def glasses_insert(k, t, tl):
    scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    hx, hy = sb.ds.don(scratch, 0, 0, 1.0, "stand", "smug", look=(-1, 0.4), shades="down")["head"]

    def d():
        c = k.c
        c.set_source_rgb(*kit.WALL); c.rectangle(-5, -5, 108, 184); c.fill()

        def bg(lc):                                    # the room behind, soft
            lk = Ctx(lc, 0)
            lc.save(); lc.translate(49, 150); lc.scale(0.09, 0.09); lc.translate(-X["pam"], -S.FEET)
            S.fairy_lights(lk, x0=X["pam"] - 400, x1=X["pam"] + 400, y=S.FEET - 520, t=tl)
            lc.restore()
        props.soft(c, bg, 1.5)
        for i, (cx, cy) in enumerate(LENS):            # his face, mirrored, in each lens
            c.save(); _lens_path(c, cx, cy); c.clip()
            c.set_source_rgb(0.93, 0.96, 1.0); c.paint()
            c.translate(cx, cy + 6); c.scale(-0.30, 0.30); c.translate(-hx, -hy)
            sb.ds.don(k, 0, 0, 1.0, "stand", "smug", look=(-1, 0.4), shades="down", mouth=sb.talk(tl, 1.25, 2.3))
            c.restore()
            c.save(); _lens_path(c, cx, cy); c.clip()
            c.set_source_rgba(0.75, 0.88, 1.0, 0.14); c.paint()
            c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(3)
            c.move_to(cx - LW / 2 + 6, cy + 10); c.line_to(cx - LW / 2 + 16, cy - LH / 2 - 2); c.stroke()
            c.restore()
            _lens_path(c, cx, cy); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
        c.set_line_width(2.4); c.set_line_cap(1)
        c.move_to(LENS[0][0] + LW / 2, 72); c.curve_to(46, 67, 52, 67, LENS[1][0] - LW / 2, 72); c.stroke()   # bridge
        c.move_to(LENS[0][0] - LW / 2, 71); c.line_to(2, 68); c.stroke()                                     # temples
        c.move_to(LENS[1][0] + LW / 2, 71); c.line_to(96, 68); c.stroke()
        c.set_source_rgb(*pm.GOLD)                     # the bead chain
        for i in range(18):
            u = i / 17
            c.set_source_rgb(*INK); c.arc(4 - 8 * u, 69 - 10 * u + 18 * u * u, 1.6, 0, 2 * math.pi); c.fill()
            c.set_source_rgb(*pm.GOLD); c.arc(4 - 8 * u, 69 - 10 * u + 18 * u * u, 1.15, 0, 2 * math.pi); c.fill()
        kit.cut(k, [(70, 180), (98, 180), (98, 128), (84, 120)], pm.PURPLE, shadow=False, lw=1.8)       # her sleeve
        for j, (fx, fy) in enumerate(((88, 104), (93, 110), (96, 117))):                                   # fingers
            kit.ellipse(k, fx, fy, 5.5, 4.2, pm.SKIN, 60 + j, shadow=False, lw=1.4)
        kit.ellipse(k, 86, 92, 4.6, 6.0, pm.SKIN, 64, shadow=False, lw=1.4)                                 # thumb
    sb.screen(k, tl, "s4b", d)
    sx = sb.U
    xb.speech(k, "Agent Santa.\nLicensed to gift.", (LENS[1][0] * sx, (LENS[1][1] - LH / 2) * sx), t, 1.25,
              size=26, at=(330, 300))


def s4_new(fn_v2):
    def g(k, t, tl):
        return glasses_insert(k, t, tl) if G0 <= tl < G1 else fn_v2(k, t, tl)
    return g


# ---------------------------------------------------------------- shot 15: the two tags, then the faces
I0, I1 = 3.05, 4.15                          # storyboard time of the insert inside shot 15
HIT = 3.3


def card(k, x, y, s, approved_lift):
    """His tag, big: TO: SOFIA (heart) / FROM: DON on white; APPROVED when the stamp is down."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(-0.04); c.scale(s, s)
    kit.rect(k, -40, -20, 80, 40, (0.99, 0.99, 0.97), 981, shadow=False, lw=1.8)
    c.select_font_face("Permanent Marker", 0, 0)
    for txt, yy, sz, col in (("TO: SOFÍA", -3, 12, S.RED), ("FROM: DON", 13, 11, INK)):
        c.set_font_size(sz); e = c.text_extents(txt)
        dxh = 5 if txt.startswith("TO") else 0
        c.set_source_rgb(*col); c.move_to(-e.x_advance / 2 - dxh, yy); c.show_text(txt)
        if dxh:
            pss.heart(c, e.x_advance / 2 - 2, yy - 4, 3.6, S.RED)
    c.restore()
    if approved_lift is not None and approved_lift < 1:
        c.save(); c.translate(x + 13 * s, y + 24 * s); c.rotate(-0.2); c.scale(s, s)
        c.set_source_rgb(*rs.GREEN); c.set_line_width(2.2); c.rectangle(-30, -8, 60, 15); c.stroke()
        c.select_font_face("Inter", 0, 1); c.set_font_size(10.5); e = c.text_extents("APPROVED")
        c.move_to(-e.x_advance / 2, 4); c.show_text("APPROVED")
        c.restore()


def tags_insert(k, t, tl):
    def d():
        c = k.c
        dx, dy = mo.shake(tl, HIT, 1.2, seed=15)
        c.translate(dx, dy)
        c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(-10, -10, 120, 200); c.fill()      # the table cloth
        c.set_source_rgb(0.86, 0.86, 0.83); c.set_line_width(1.2)
        for gx in range(-20, 120, 16):
            c.move_to(gx, 0); c.line_to(49 + (gx - 49) * 1.4, 174); c.stroke()
        S.present(k, 34, 76, 40, 32, S.RED, S.GOLD, 966)                                     # hers, barred
        sb.tag2(k, 60, 58, 0.95, ("from", "to", "kiss"), rot=0.12)
        S.present(k, 62, 150, 52, 30, (0.20, 0.42, 0.70), (0.97, 0.97, 0.97), 980)          # his, approved
        lift = mo.stamp_track(tl, HIT, 60, up_after=0.12)
        card(k, 49, 112, 1.0, 0.0 if tl >= HIT else None)
        if tl > HIT - 0.25 and lift < 30:
            rs.stamp_prop(k, 62, 136 - lift - 3, 0.6, "down" if lift < 1 else "up", 0.0, 7)
            if HIT <= tl < HIT + 0.18:
                rs.impact_lines(c, 62, 136, 1, 0.6)
    sb.screen(k, tl, "s15b", d)
    if tl >= HIT:                                     # the robot is off screen: a bubble without a tail
        xb.speech(k, "You're welcome.", [], t, HIT, size=28, at=(270, 150))


def s15_wide(k, t, tl):
    """sb.s15b without signs, without the UNCLAIMED card and without "(SECRET!)" on his gift."""
    _dg0, _uc0 = sb.don_gift, sb.unclaimed_card

    def don_gift(k, x, y, approved):
        S.present(k, x, y, 124, 104, (0.20, 0.42, 0.70), (0.97, 0.97, 0.97), 980)
        card(k, x, y - 64, 1.3, 0.0 if approved else None)
    sb.don_gift, sb.unclaimed_card = don_gift, (lambda *a, **kw: None)
    NOSIGN[0] = NOSANTA[0] = True
    _sp0 = xb.speech
    if A.CUR[0] > 38.96:                              # v4.1: "You're welcome." ended at 38.86; no bubble over the faces
        xb.speech = lambda *a, **kw: None
    try:
        sb.s15b(k, t, tl)
    finally:
        sb.don_gift, sb.unclaimed_card = _dg0, _uc0
        NOSIGN[0] = NOSANTA[0] = False
        xb.speech = _sp0


def s15_new(k, t, tl):
    return tags_insert(k, t, tl) if I0 <= tl < I1 else s15_wide(k, t, tl)


# ---------------------------------------------------------------- the panels: v3's, with the new shots swapped in
_NEW = {"s1": lambda f: s1_new, "s2b": lambda f: s2_new, "s4b": s4_new, "s15b": lambda f: s15_new}
_rows = []
for a0, a1, fn, t0, t1, ks in M3._rows:
    name = fn.__name__
    if name in _NEW:
        g = _NEW[name](getattr(sb, name))
        g.__name__ = name
        fn = g
    _rows.append((a0, a1, fn, t0, t1, ks))
# v4.1: the tags insert held 0.8 s longer (2.1 s on screen). Shot 15 is stretched only between the APPROVED hit and
# the insert's end, after "You're welcome." has been said; shot 16 moves 0.8 s later. Every voice keeps its time.
EXTRA = 0.8
for i, (a0, a1, fn, t0, t1, ks) in enumerate(_rows):
    if fn.__name__ == "s15b":
        (x3, y3), (x4, y4) = ks[-2], ks[-1]
        r = (y4 - y3) / (x4 - x3)
        ks = list(ks[:-1]) + [(I1, y3 + (I1 - x3) * r + EXTRA), (x4, y4 + EXTRA)]
        _rows[i] = (a0, a1 + EXTRA, fn, t0, t1, ks)
        HOLD_AT = a0 + y3 + (I1 - x3) * r          # film time where the 0.8 s are added (the insert's old end)
    elif fn.__name__ == "s16b":
        _rows[i] = (a0 + EXTRA, a1 + EXTRA, fn, t0, t1, ks)
DURATION = round(A.DURATION + EXTRA, 3)
PANELS = [(a0, a1, A._wrap(a0, a1, fn, t0, t1, ks)) for a0, a1, fn, t0, t1, ks in _rows]


def shake(t):
    return A.shake(t)
