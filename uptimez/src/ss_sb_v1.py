"""v1 (pinned). Secret Santa, silent storyboard v1 (engine_v.py, 540x960, 30 fps, 12 fps drawing). 36.5 s, the camera plan of
concept v4 / set sheet v2, the redaction from motion test v2 (take A, Pam's sad 14). Lines as bubbles, no voices
yet (Pam's first line in a dashed whisper bubble). Only shot 1 moves (the ECU pulls out to the two-shot); every
other shot holds still (the engine's slow push is undone). Don's shades are already down in 5; no beard gag.
Shots (s): 1 0.0-3.6 ECU uncap, pull-out | 2 3.6-6.0 compact | 3 6.0-8.6 Agent Santa, low + dutch | 4 8.6-10.0
glasses off | 5 10.0-13.2 one heart | 6 13.2-15.8 "a full-length mirror" | 7 15.8-17.4 hurt, decides | 8 17.4-20.6
the tag | 9 20.6-22.1 proud | 10 22.1-24.6 detected | 11 24.6-25.5 sender | 12 25.5-27.2 recipient (high) |
13 27.2-29.5 the kiss | 14 29.5-30.7 Pam, silent | 15 30.7-35.1 "You're welcome." | 16 35.1-36.5 attempt two."""
import math
import kit
from kit import INK, W, H, Ctx
import ss_set as S
import ss_set_sheet as sss
import ss_motion as mo
import sofia_ss as so
import pam_ss as ps
import don_ss as ds
import robot_ss as rs
import props_ss as props
import pam_sheet_ss as pss
import sofia_sheet_ss as sfs
import xmas_bubbles as xb
import emoji as _emoji
from sofia_sheet_mf import HY as SHY

DURATION = 36.5
RAW_T = 0.0
X = S.POS
U = 540 / 98.0
PANEL_DUR = {}
rs.BIG_ICON = True
mo.SAD14 = True


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def unpush(c, name, tl):
    push = 1 + 0.03 * (tl / PANEL_DUR[name])
    c.translate(W / 2, H / 2); c.scale(1 / push, 1 / push); c.translate(-W / 2, -H / 2)


def world(k, tl, name, cam, draw):
    c = k.c
    c.save(); unpush(c, name, tl); S.with_cam(c, cam)
    out = draw()
    c.restore()
    return out


def screen(k, tl, name, draw):
    """Screen-space shots drawn in 98 x 174 units (the sheets' crop boxes)."""
    c = k.c
    c.save(); unpush(c, name, tl); c.scale(U, U)
    out = draw()
    c.restore()
    return out


def sp(x, y):
    return (x * U, y * U)


def above(cam, pt, lift=72):
    return S.to_screen(cam, pt[0], pt[1] - lift)


def whisper(k, s, anchor, t, t0, at=None, size=24):
    c = k.c
    c.set_dash([10, 6])
    xb.speech(k, s, anchor, t, t0, size=size, at=at, fill=(0.97, 0.97, 1.0))
    c.set_dash([])


def pop_heart(k, x, y, tl, t0=0.0, hold=0.8, r=40):
    a = tl - t0
    if a < 0 or a > hold + 0.2:
        return
    sc = min(1.0, a / 0.12) * (1.15 if a < 0.2 else 1.0) if a < hold else 1 - (a - hold) / 0.2
    sc = max(0.02, sc)
    c = k.c
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.set_source_rgba(0, 0, 0, 0.12); c.arc(4, 5, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(1.0, 0.91, 0.93); c.arc(0, 0, r, 0, 2 * math.pi); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    _emoji.draw_emoji(c, "\U0001F497", 0, 0, r * 1.25)
    c.restore()


def talk(tl, t0, t1, rate=7):
    if t0 <= tl < t1:
        return "EAOEAMOE"[int((tl - t0) * rate) % 8]
    return None


def lipstick_in_hand(k, o, s=1.0, uncap=0.0):
    hx, hy = o["hands"][1]
    props.lipstick(k, hx - 2 * s, hy + 2 * s, 0.85 * s, -0.25, uncap, 31, cap_col=props.CAP_BLACK)
    kit.ellipse(k, hx, hy, 10 * s, 10 * s, ps.SKIN, 32, shadow=False, lw=2 * s)


# ---------------------------------------------------------------- 1. ECU: the uncap, then the pull-out
CAM1 = (700, 470, 1.7)


def s1(k, t, tl):
    if tl < 1.0:                                                  # frame 0: the same ECU as 16
        def d():
            c = k.c
            c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()
            def bg(lc):
                so.sofia(Ctx(lc, 0), 98 * 0.40, 174 * 0.34 - SHY, 1.0, "stand", "neutral", look=(-0.6, 0.1),
                         lag=(3, 0), badge=False, sparkle=1.0 if 0.2 < tl < 0.7 else 0.0)
            props.soft(c, bg, 1.5)
            x, y = 98 * 0.24, 174 * 0.74
            sss.pam_hand(k, ease((tl - 0.25) / 0.35))
        screen(k, tl, "s1", d)
        return
    u = ease((RAW_T - 1.0 - 0.0) / 0.35) if False else ease((tl - 1.0) / 0.35)
    hand = (X["pam"] + 40, S.FEET - 196)
    cam = (lerp(hand[0], CAM1[0], u), lerp(hand[1], CAM1[1], u), lerp(5.0, CAM1[2], u))

    def draw():
        S.backdrop(k, t=tl)
        o2 = sss.sofia_seated(k, "stand", "neutral", look=(-0.8, 0.1), sparkle=0.4 if tl > 2.6 else 0.0,
                              mouth=talk(tl, 2.6, 3.4))
        S.desk(k)
        o = ps.pam(k, X["pam"] + 40, S.FEET, 1.0, ps.POSE_WHISPER, "neutral",
                   look=(1, 0) if tl < 2.0 or tl > 2.4 else (-1, 0), lips=None, mouth=talk(tl, 1.4, 2.5, 5), lean=4)
        lipstick_in_hand(k, o, 1.0, 1.0)
        return o, o2
    o, o2 = world(k, tl, "s1", cam, draw)
    if u >= 1:
        whisper(k, "Sofía… do you think\nI could pull off nude?", above(cam, o["head"], 70), t, 1.35, at=(250, 200))
        if tl > 2.55:
            xb.speech(k, "On your lips, Pam.", above(cam, o2["head"] if "head" in o2 else (X["sofia"], 480), 80),
                      t, 2.6, size=26, at=(330, 330))


# ---------------------------------------------------------------- 2. tight, into the compact
CAM2 = (700, 470, 1.9)


def s2(k, t, tl):
    def draw():
        S.backdrop(k, t=tl)
        o2 = sss.sofia_seated(k, "compact", "knowing" if tl > 1.6 else "neutral", look=(-0.8, 0.1), compact_open=1.0,
                              mouth=talk(tl, 1.3, 2.0))
        S.desk(k)
        o = ps.pam(k, X["pam"] + 40, S.FEET, 1.0, "stand", "neutral",
                   look=(-1, 0.1) if 0.5 < tl < 1.1 else (0.6, 0.2), apply=True, mouth=talk(tl, 0.2, 0.9, 6))
        return o, o2
    o, o2 = world(k, tl, "s2", CAM2, draw)
    xb.speech(k, "Would Don notice?", above(CAM2, o["head"], 70), t, 0.15, size=26, at=(170, 200))
    if tl > 1.25:
        xb.speech(k, "Don notices mirrors.", above(CAM2, (X["sofia"], 470), 60), t, 1.3, size=26, at=(360, 330))


# ---------------------------------------------------------------- 3. Agent Santa: low + dutch, the THUNK
CAM3 = (150, 460, 1.55, -0.12)


def s3(k, t, tl):
    c = k.c
    sh = (8 if int(tl * 30) % 2 == 0 else -8) if tl < 0.12 else 0
    sh2 = (4 if int(tl * 30) % 2 == 0 else -4) if 1.55 < tl < 1.7 else 0
    c.save(); c.translate(sh + sh2, 0)
    op = ease(tl / 0.15)

    def draw():
        S.backdrop(k, door_open=op)
        o = rs.robot(k, X["robot"], S.FEET_BACK, 1.0, rs.POSE_CLIP, "tick" if tl > 1.6 else "eager")
        hx, hy = o["hands"][1]
        rs.clipboard(k, hx + 6, hy - 4, 1.2, tl > 1.6, 42)
        if 1.6 < tl < 1.8:
            rs.impact_lines(k.c, hx + 6, hy + 4, 2, 0.8)
        d = None
        if op > 0.4:
            d = ds.don(k, X["door"] + 40, S.FEET, 1.0, ds.POSE_WIDE_CARD, "showman", card="hand",
                       mouth=talk(tl, 0.4, 1.9))
        S.santa_table(k)
        return d
    o = world(k, tl, "s3", CAM3, draw)
    c.restore()
    if o and tl > 0.35:
        xb.shout(k, "Secret Santa!\nHR-approved!", above(CAM3, o["head"], 60), t, 0.4, cy=170, size=36)
    if 1.6 < tl < 2.2:
        xb.burst(k, "THUNK", 400, 700, t, 1.6, size=40)


# ---------------------------------------------------------------- 4. MCU Pam: glasses off, a small head lift
CAM4 = (560, 470, 2.4)


def s4(k, t, tl):
    def draw():
        S.backdrop(k, t=tl)
        if tl < 0.45:
            ps.pam(k, X["pam"] - 40, S.FEET, 1.0, "stand", "hopeful", look=(-1, 0))
        elif tl < 0.8:
            ps.pam(k, X["pam"] - 40, S.FEET, 1.0, ps.POSE_GLASSES, "hopeful", look=(-1, 0), finger="bridge")
        else:
            ps.pam(k, X["pam"] - 40, S.FEET, 1.0, ps.POSE_GLASSES_OUT, "hopeful", look=(-1, -0.35), glasses="hand",
                   lean=2)
    world(k, tl, "s4", CAM4, draw)


# ---------------------------------------------------------------- 5. one heart; Don already past her
CAM5 = (585, 480, 1.55)


def s5(k, t, tl):
    def draw():
        S.backdrop(k, t=tl)
        sss.sofia_seated(k, "stand", "neutral", look=(-1, 0.1))
        S.desk(k)
        o = ps.pam(k, X["don"] + 30, S.FEET, 1.0, ps.POSE_SHY, "hopeful", look=(1, -0.1), glasses="chain", lean=4,
                   mouth=talk(tl, 0.3, 1.8, 6))
        ds.don(k, X["pam"] + 20, S.FEET, 1.0, "stand", "smug" if tl > 1.9 else "neutral", look=(1, -0.1),
               shades="down", lean=4)
        return o
    o = world(k, tl, "s5", CAM5, draw)
    xb.speech(k, "Don… what would you\nlike Santa to bring?", above(CAM5, o["head"], 70), t, 0.25, size=24,
              at=(220, 190))
    hx, hy = S.to_screen(CAM5, o["head"][0] - 18, o["head"][1] - 78)
    pop_heart(k, hx, hy + 60, tl, 2.0, 0.8, 30)


# ---------------------------------------------------------------- 6. CU Don over Pam's shoulder
def s6(k, t, tl):
    def d():
        c = k.c
        sss.wall_bg(k)
        def bg(lc):
            rs.robot(Ctx(lc, 0), 90, 150, 0.42, "stand", "tick", seed=93)
        props.soft(c, bg, 1.8)
        def tgt(lc):
            so.sofia(Ctx(lc, 0), 132, 60 - SHY * 0.9, 0.9, "stand", "unimpressed", look=(-1, 0.1), badge=False, seed=96)
        props.soft(c, tgt, 1.6)
        props.sparkle(c, 92, 74, 7, 1.0 if 0.3 < tl < 0.9 else 0.4)
        smooth = tl > 1.2
        ds.don(k, 40, 322, 0.85, ds.POSE_SMOOTH if smooth else "stand", "smug", look=(1, 0),
               shades="down", glint=smooth and int(tl * 6) % 2 == 0, mouth=talk(tl, 0.3, 2.0), seed=95)
        def fg(lc):
            ps.pam(Ctx(lc, 0), -26, 330, 1.1, "stand", "hopeful", look=(1, 0), glasses="chain", seed=94)
        props.soft(c, fg, 2.4)
    screen(k, tl, "s6", d)
    xb.speech(k, "Sofía.\nOr a full-length mirror.", (300, 560), t, 0.25, size=26, at=(270, 770))


# ---------------------------------------------------------------- 7. CU Pam: 7A hurt, 7B decides
def s7(k, t, tl):
    def d():
        c = k.c
        sss.wall_bg(k)
        sss.soft_sofia(k, 0)
        decide = tl > 0.6
        ps.pam(k, 40, 112 - ps.HY * 1.05, 1.05, "stand", "decide" if decide else "hurt",
               look=(0.8, 0.4) if decide else (0, 0), glasses="chain")
        if decide:
            c.set_source_rgb(*S.RED); c.rectangle(70, 138, 40, 40); c.fill()
            c.set_source_rgb(*S.GOLD); c.rectangle(86, 138, 6, 40); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(70, 138, 40, 40); c.stroke()
    screen(k, tl, "s7", d)


# ---------------------------------------------------------------- 8. ECU the tag: she writes, she kisses it
def s8(k, t, tl):
    def d():
        c = k.c
        c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(0, 0, 98, 174); c.fill()
        c.set_source_rgb(*S.RED); c.rectangle(-10, 118, 120, 70); c.fill()
        c.set_source_rgb(*S.GOLD); c.rectangle(40, 118, 14, 70); c.fill()
        sss.tag(k, 50, 88, 2.2, blank=True, rot=-0.04)
        for (t0, t1, y0, y1) in ((0.3, 1.2, 50, 86), (1.4, 2.1, 86, 122)):    # the names, written on
            u = clamp((tl - t0) / (t1 - t0))
            if u <= 0:
                continue
            c.save(); c.rectangle(0, y0, 22 + 64 * u, y1 - y0); c.clip()
            pss.k = k
            pss.gift_tag(c, 50, 88, 2.2, rot=-0.04, bars=("kiss",), bar_style=2, big=True)
            c.restore()
            if u < 1:                                               # the pen at the writing front
                px_, py_ = 22 + 64 * u, (y0 + y1) / 2
                c.set_source_rgb(0.15, 0.15, 0.30); c.set_line_width(4); c.set_line_cap(1)
                c.move_to(px_, py_); c.line_to(px_ + 22, py_ - 40); c.stroke()
        if tl > 2.3:                                                # the kiss, pressed on
            a = clamp((tl - 2.3) / 0.15)
            c.save(); c.translate(50 + 24 * 2.2, 88 + 9 * 2.2); c.scale(0.6 + 0.4 * a, 0.6 + 0.4 * a)
            props.kiss(k, 0, 0, 0.26 * 2.2)
            c.restore()
    screen(k, tl, "s8", d)


# ---------------------------------------------------------------- 9. CU Pam: proud
def s9(k, t, tl):
    screen(k, tl, "s9", lambda: sss.shot9(k))


# ---------------------------------------------------------------- 10. CU robot: detected
CAM10 = (X["robot"], 418, 3.6)


def s10(k, t, tl):
    c = k.c
    sh = (5 if int(tl * 30) % 2 == 0 else -5) if 0.3 < tl < 0.45 else 0
    c.save(); c.translate(sh, 0)

    def draw():
        S.backdrop(k)
        return rs.robot(k, X["robot"], S.FEET_BACK, 1.0, "stand", "personal" if tl > 0.3 else "eager",
                        talk=0.6 if 0.6 < tl < 2.3 else 0, t=tl)
    world(k, tl, "s10", CAM10, draw)
    c.restore()
    if tl > 0.55:
        xb.speech(k, "Personal data detected.\nAnonymizing.", (270, 640), t, 0.6, size=26, at=(270, 830))


# ---------------------------------------------------------------- 11-14. the redaction (motion test v2, take A)
def s11(k, t, tl):
    screen(k, tl, "s11", lambda: mo.shot11(k, tl))


def s12(k, t, tl):
    screen(k, tl, "s12", lambda: mo.shot12(k, tl))


def s13(k, t, tl):
    screen(k, tl, "s13", lambda: mo.shot13(k, tl, "A"))


def s14(k, t, tl):
    screen(k, tl, "s14", lambda: mo.shot14(k, tl))


# ---------------------------------------------------------------- 15. still two-shot: five beats
CAM15 = (380, 500, 1.65)


def s15(k, t, tl):
    def draw():
        S.backdrop(k, t=tl)
        sss.sofia_seated(k, "stand", "unimpressed", look=(1, 0.1), lean=4, lag=(-5, 0))
        S.desk(k)
        ds.don(k, X["sofia"] - 120, S.FEET - 40, 0.9, "stand", "smug", look=(1, -0.2), lean=6, shades="down")
        st = "eager" if tl < 2.0 else ("proud" if tl < 2.8 else "tick")
        r = rs.robot(k, X["robot"] + 30, S.FEET_BACK, 1.0, "stand", st, head_rot=0.1 if st == "proud" else None,
                     talk=0.6 if 2.0 < tl < 3.6 else 0, t=tl)
        if tl < 0.4:
            o = ps.pam(k, X["don"], S.FEET, 1.0, ps.POSE_SHY, "pressed", look=(0, 1), glasses="chain")
        elif tl < 0.8:
            o = ps.pam(k, X["don"], S.FEET, 1.0, ps.POSE_GLASSES, "pressed", look=(0, 0.6), finger="bridge")
        else:
            o = ps.pam(k, X["don"], S.FEET, 1.0, ps.POSE_SHY, "incredulous", look=(-0.6, 0.5) if tl < 1.0 else (-1, -0.2),
                       mouth=talk(tl, 1.0, 1.8, 6))
        S.santa_table(k, pams=False)
        S.present(k, X["don"] + 2, S.FEET - 112, 64, 50, S.RED, S.GOLD, 966)
        sss.tag(k, X["don"] + 30, S.FEET - 150, 1.0, ("from", "to", "kiss"), rot=0.18)
        return o, r
    o, r = world(k, tl, "s15", CAM15, draw)
    if tl > 0.95:
        xb.speech(k, "Will Don get it?", above(CAM15, o["head"], 70), t, 1.0, size=26, at=(360, 200))
    if tl > 1.95:
        xb.speech(k, "He won't.\nYou're welcome.", above(CAM15, r["screen"], 60), t, 2.0, size=26, at=(170, 330))


# ---------------------------------------------------------------- 16. ECU: attempt two (the cut back to 1)
def s16(k, t, tl):
    def d():
        c = k.c
        def bg(lc):
            k2 = Ctx(lc, 0)
            lc.save(); lc.scale(1 / U, 1 / U); lc.translate(270, 480); lc.scale(2.2, 2.2); lc.translate(-760, -470)
            S.wall(k2); S.fairy_lights(k2, t=tl); S.desk(k2)
            lc.restore()
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()
        props.soft(c, bg, 1.5)
        sss.tag(k, lerp(130, 60, ease(tl / 0.5)), 120, 1.15, blank=True, rot=0.06)
        sss.pam_hand(k, 0.0)
    screen(k, tl, "s16", d)


PANELS = [(0.0, 3.6, s1), (3.6, 6.0, s2), (6.0, 8.6, s3), (8.6, 10.0, s4), (10.0, 13.2, s5), (13.2, 15.8, s6),
          (15.8, 17.4, s7), (17.4, 20.6, s8), (20.6, 22.1, s9), (22.1, 24.6, s10), (24.6, 25.5, s11),
          (25.5, 27.2, s12), (27.2, 29.5, s13), (29.5, 30.7, s14), (30.7, 35.1, s15), (35.1, 36.5, s16)]
for _t0, _t1, _fn in PANELS:
    PANEL_DUR[_fn.__name__] = _t1 - _t0


def shake(t):
    return 0
