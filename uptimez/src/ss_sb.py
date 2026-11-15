"""v2 (ss_sb_v1.py = v1, kept), concept v5: 34.6 s. 4: Don leans in and purrs at his reflection in Pam's lenses
("Agent Santa. Licensed to gift."), Pam melts; 6: "Sofia." / a smug hold, the palm on the dome / "Or a full-length
mirror."; 7B is denial (she brightens anyway, a hand on the box); 8, 11-13: the whole tag in frame and the kiss 2.5x,
the third stamp lands on it after a 0.6 s hover; 15 (wider, still): the robot moves Pam's present to the UNCLAIMED
corner, Don sets down TO: SOFIA (SECRET!) and it gets a green APPROVED; "He won't." / pause / the tick / "You're
welcome."; 16 matches frame 0 (Sofia soft behind the hand). The v2 shots are defined after the v1 ones.
v1: Secret Santa, silent storyboard v1 (engine_v.py, 540x960, 30 fps, 12 fps drawing). 36.5 s, the camera plan of
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

DURATION = 34.6
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


PUSH_TL = [None]                 # the animatic sets the engine's own panel time here, so the push is undone exactly


def unpush(c, name, tl):
    if PUSH_TL[0] is not None:
        tl = PUSH_TL[0]
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


# ================================================================ v2 (concept v5)
KISS = 2.1


TAIL_FIX = [False]  # full animation: Sofia's tail in 2 on her real head; Don's tail in 6 up to his mouth
TAG_FIX = [False]   # animatic v2: the write-on in 8 draws the names without the kiss's bar (v1 left a black block
                    # after "PAM" that cut the M)


def tag2(k, x, y, s, bars=(), rot=0.0, blank=False, kiss=True):
    pss.k = k
    pss.gift_tag(k.c, x, y, s, rot=rot, bars=bars, blank=blank, bar_style=2, big=True, kiss_k=KISS, kiss=kiss,
                 kiss_dx=3.5 if TAG_FIX[0] else 0.0)


BC2 = {"from": (3, 8.5), "to": (1, -9), "kiss": (23, 10.5)}


def s1b(k, t, tl):
    s1(k, t, tl * 3.6 / 3.4 if tl > 1.0 else tl)


def s2b(k, t, tl):
    def draw():
        S.backdrop(k, t=tl)
        o2 = sss.sofia_seated(k, "compact", "knowing" if tl > 1.5 else "neutral", look=(-0.8, 0.1), compact_open=1.0,
                              mouth=talk(tl, 1.15, 1.8))
        S.desk(k)
        o = ps.pam(k, X["pam"] + 40, S.FEET, 1.0, "stand", "neutral",
                   look=(-1, 0.1) if 0.45 < tl < 1.0 else (0.6, 0.2), apply=True, mouth=talk(tl, 0.15, 0.8, 6))
        return o, o2
    o, o2 = world(k, tl, "s2b", CAM2, draw)
    xb.speech(k, "Would Don notice?", above(CAM2, o["head"], 70), t, 0.1, size=26, at=(170, 200))
    if tl > 1.1:
        anc = above(CAM2, o2["head"], 60) if TAIL_FIX[0] else above(CAM2, (X["sofia"], 470), 60)
        xb.speech(k, "Don notices mirrors.", anc, t, 1.15, size=26, at=(360, 330))


def s3b(k, t, tl):
    c = k.c
    sh = (8 if int(tl * 30) % 2 == 0 else -8) if tl < 0.12 else 0
    sh2 = (4 if int(tl * 30) % 2 == 0 else -4) if 1.3 < tl < 1.45 else 0
    c.save(); c.translate(sh + sh2, 0)
    op = ease(tl / 0.15)

    def draw():
        S.backdrop(k, door_open=op)
        o = rs.robot(k, X["robot"], S.FEET_BACK, 1.0, rs.POSE_CLIP, "tick" if tl > 1.3 else "eager")
        hx, hy = o["hands"][1]
        rs.clipboard(k, hx + 6, hy - 4, 1.2, tl > 1.3, 42)
        if 1.3 < tl < 1.5:
            rs.impact_lines(k.c, hx + 6, hy + 4, 2, 0.8)
        d = None
        if op > 0.4:
            d = ds.don(k, X["door"] + 40, S.FEET, 1.0, ds.POSE_WIDE_CARD, "showman", card="hand",
                       mouth=talk(tl, 0.3, 1.6))
        S.santa_table(k)
        return d
    o = world(k, tl, "s3b", CAM3, draw)
    c.restore()
    if o and tl > 0.25:
        xb.shout(k, "Secret Santa!\nHR-approved!", above(CAM3, o["head"], 60), t, 0.3, cy=170, size=36)
    if 1.3 < tl < 1.9:
        xb.burst(k, "THUNK", 400, 700, t, 1.3, size=40)


CAM4B = (600, 440, 1.95)
CAM4F = (650, 430, 1.8)
S4_FIX = [False]   # animatic v2: Don stands clear of Pam and leans less, her held-out lenses sit in the gap


def s4b(k, t, tl):
    """Glasses off and held out; Don leans in from the right and purrs at his reflection in her lenses."""
    def draw():
        S.backdrop(k, t=tl)
        fx = S4_FIX[0]
        lean = -lerp(0, 8 if fx else 14, ease((tl - 0.8) / 0.4)) if tl > 0.8 else 0
        d = ds.don(k, X["pam"] + (165 if fx else 130), S.FEET, 1.0, "stand", "smug", look=(-1, 0.4), shades="down",
                   lean=lean,
                   mouth=talk(tl, 1.25, 2.3)) if tl > 0.7 else None
        if tl < 0.4:
            o = ps.pam(k, X["pam"] - 40, S.FEET, 1.0, "stand", "hopeful", look=(1, 0))
        elif tl < 0.7:
            o = ps.pam(k, X["pam"] - 40, S.FEET, 1.0, ps.POSE_GLASSES, "hopeful", look=(1, 0), finger="bridge")
        else:
            melt = tl > 2.0
            o = ps.pam(k, X["pam"] - 40, S.FEET, 1.0, ps.POSE_GLASSES_OUT, "dinner" if melt else "hopeful",
                       look=(1, -0.35), glasses="hand", lean=2)
            if d is not None and tl > 1.1:                      # his reflection in her lenses
                hx, hy = o["hands"][1]
                for sx in (-17, 17):
                    lx, ly = hx + 10 + sx, hy - 12
                    kit.ellipse(k, lx, ly, 4.2, 3.8, ds.SKIN, 51, shadow=False, lw=0.8)
                    k.c.set_source_rgb(0.05, 0.05, 0.07); k.c.rectangle(lx - 3.5, ly - 1.4, 7, 1.8); k.c.fill()
        return o, d
    cam = CAM4F if S4_FIX[0] else CAM4B
    o, d = world(k, tl, "s4b", cam, draw)
    if d is not None and tl > 1.2:
        xb.speech(k, "Agent Santa.\nLicensed to gift.", above(cam, d["head"], 70), t, 1.25, size=26, at=(380, 190))
    if tl > 2.05:
        hx, hy = S.to_screen(cam, X["pam"] - 70, S.FEET - 330)
        pop_heart(k, hx, hy, tl, 2.05, 0.6, 28)


def s5b(k, t, tl):
    def draw():
        S.backdrop(k, t=tl)
        sss.sofia_seated(k, "stand", "neutral", look=(-1, 0.1))
        S.desk(k)
        o = ps.pam(k, X["don"] + 30, S.FEET, 1.0, ps.POSE_SHY, "hopeful", look=(1, -0.1), glasses="chain", lean=4,
                   mouth=talk(tl, 0.2, 1.6, 6))
        ds.don(k, X["pam"] + 20, S.FEET, 1.0, "stand", "smug" if tl > 1.7 else "neutral", look=(1, -0.1),
               shades="down", lean=4)
        return o
    o = world(k, tl, "s5b", CAM5, draw)
    xb.speech(k, "Don… what would you\nlike Santa to bring?", above(CAM5, o["head"], 70), t, 0.15, size=24,
              at=(220, 190))


def s6b(k, t, tl):
    def d():
        c = k.c
        sss.wall_bg(k)
        def bg(lc):
            rs.robot(Ctx(lc, 0), 90, 150, 0.42, "stand", "tick", seed=93)
        props.soft(c, bg, 1.8)
        def tgt(lc):
            so.sofia(Ctx(lc, 0), 132, 60 - SHY * 0.9, 0.9, "stand", "unimpressed", look=(-1, 0.1), badge=False, seed=96)
        props.soft(c, tgt, 1.6)
        props.sparkle(c, 92, 74, 7, 1.0 if 0.2 < tl < 0.7 else 0.4)
        smooth = 0.75 < tl < 1.6
        ds.don(k, 40, 322, 0.85, ds.POSE_SMOOTH if smooth else "stand", "smug", look=(1, 0), shades="down",
               glint=smooth and int(tl * 6) % 2 == 0, mouth=talk(tl, 0.2, 0.6) or talk(tl, 1.55, 2.6), seed=95)
        def fg(lc):
            ps.pam(Ctx(lc, 0), -26, 330, 1.1, "stand", "hopeful", look=(1, 0), glasses="chain", seed=94)
        props.soft(c, fg, 2.4)
    screen(k, tl, "s6b", d)
    anc = (300, 560)
    if TAIL_FIX[0]:                                     # up to his mouth: head at feet + HY * s, mouth 28 below
        anc = (44 * U, (322 + ds.HY * 0.85 + 30 * 0.85) * U)
    if tl < 1.5:
        xb.speech(k, "Sofía.", anc, t, 0.15, size=30, at=(270, 770))
    else:
        xb.speech(k, "Or a full-length mirror.", anc, t, 1.5, size=28, at=(270, 770))


def s7b(k, t, tl):
    def d():
        c = k.c
        sss.wall_bg(k)
        sss.soft_sofia(k, 0)
        if tl < 0.6:
            face, lk = "hurt", (0, 0)
        elif tl < 0.85:
            face, lk = "pressed", (0.3, 0.2)                     # half a beat
        else:
            face, lk = "hopeful", (0.8, 0.4)                     # denial: she brightens anyway
        ps.pam(k, 40, 112 - ps.HY * 1.05 - (2 if tl > 0.85 else 0), 1.05, "stand", face, look=lk, glasses="chain")
        if tl > 0.85:
            c.set_source_rgb(*S.RED); c.rectangle(70, 138, 40, 40); c.fill()
            c.set_source_rgb(*S.GOLD); c.rectangle(86, 138, 6, 40); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(70, 138, 40, 40); c.stroke()
            kit.ellipse(k, 74, 146, 8, 7, ps.SKIN, 7, shadow=False, lw=1.6)   # a hand on the box
    screen(k, tl, "s7b", d)


def s8b(k, t, tl):
    def d():
        c = k.c
        c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(0, 0, 98, 174); c.fill()
        c.set_source_rgb(*S.RED); c.rectangle(-10, 118, 120, 70); c.fill()
        c.set_source_rgb(*S.GOLD); c.rectangle(40, 118, 14, 70); c.fill()
        tx, ty, sc = 49, 90, 1.22
        tag2(k, tx, ty, sc, blank=True)
        for (t0, t1, y0, y1) in ((0.25, 1.0, ty - 16 * sc, ty - 2 * sc), (1.15, 1.8, ty + 1 * sc, ty + 15 * sc)):
            u = clamp((tl - t0) / (t1 - t0))
            if u <= 0:
                continue
            x0 = tx - 16 * sc
            c.save(); c.rectangle(x0, y0, (36 if TAG_FIX[0] else 34) * sc * u, y1 - y0); c.clip()
            if TAG_FIX[0]:
                tag2(k, tx, ty, sc, kiss=False)
            else:
                tag2(k, tx, ty, sc, bars=("kiss",))
            c.restore()
            if u < 1:
                px_, py_ = x0 + 34 * sc * u, (y0 + y1) / 2
                c.set_source_rgb(0.15, 0.15, 0.30); c.set_line_width(3.2); c.set_line_cap(1)
                c.move_to(px_, py_); c.line_to(px_ + 18, py_ - 32); c.stroke()
        if tl > 1.95:                                            # the kiss, pressed on: its own beat
            a = clamp((tl - 1.95) / 0.15)
            c.save(); c.translate(tx + (26.5 if TAG_FIX[0] else 23) * sc, ty + 10.5 * sc); c.scale(0.7 + 0.3 * a, 0.7 + 0.3 * a)
            props.kiss(k, 0, 0, 0.26 * KISS * sc)
            c.restore()
    screen(k, tl, "s8b", d)


def s9b(k, t, tl):
    def d():
        c = k.c
        c.set_source_rgb(1.0, 0.94, 0.95); c.rectangle(0, 0, 98, 174); c.fill()
        ps.pam(k, 49, 84 - ps.HY * 1.12, 1.12, "stand", "proud", glasses="chain")
        tag2(k, 52, 160, 1.1, rot=-0.04)
    screen(k, tl, "s9b", d)


def s10b(k, t, tl):
    c = k.c
    sh = (5 if int(tl * 30) % 2 == 0 else -5) if 0.25 < tl < 0.4 else 0
    c.save(); c.translate(sh, 0)

    def draw():
        S.backdrop(k)
        return rs.robot(k, X["robot"], S.FEET_BACK, 1.0, "stand", "personal" if tl > 0.25 else "eager",
                        talk=0.6 if 0.5 < tl < 1.9 else 0, t=tl)
    world(k, tl, "s10b", CAM10, draw)
    c.restore()
    if tl > 0.45:
        xb.speech(k, "Personal data detected.\nAnonymizing.", (270, 640), t, 0.5, size=26, at=(270, 830))


def hit2(k, x, y, s, bar, wt, lift):
    bx, by = x + BC2[bar][0] * s, y + BC2[bar][1] * s
    rs.stamp_prop(k, bx, by - lift - 3, 0.6, "down" if lift < 1 else "up", 0.0, 7)
    return bx, by


def s11b(k, t, tl):
    def d():
        c = k.c
        th = 0.33
        dx, dy = mo.shake(tl, th, 1.2, seed=11)
        c.translate(dx, dy)
        sss.table_top(c, 40)
        hit = tl >= th
        tag2(k, 49, 110, 1.25, ("from",) if hit else ())
        bx, by = hit2(k, 49, 110, 1.25, "from", 1, mo.stamp_track(tl, th, 60))
        if hit and tl < th + 0.18:
            rs.impact_lines(c, bx, by, 1, 0.6)
    screen(k, tl, "s11b", d)


def s12b(k, t, tl):
    def d():
        import pam_mf as pm
        c = k.c
        th = 0.4
        dx, dy = mo.shake(tl, th, 2.4, 0.3, seed=12)
        c.translate(dx, dy)
        c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(-10, -10, 120, 200); c.fill()
        c.set_source_rgb(0.86, 0.86, 0.83); c.set_line_width(1.2)
        for gx in range(-20, 120, 16):
            c.move_to(gx, 0); c.line_to(49 + (gx - 49) * 1.4, 174); c.stroke()
        hit = tl >= th
        c.save(); c.translate(49, 96); c.scale(1, 0.84); c.translate(-49, -96)
        tag2(k, 47, 96, 1.25, ("from", "to") if hit else ("from",), rot=0.06)
        c.restore()
        for sx in (-1, 1):
            cx_ = 49 + sx * 34
            kit.cut(k, [(cx_ - 16, 180), (cx_ + 16, 180), (cx_ + 12, 150), (cx_ - 12, 150)], pm.PURPLE, shadow=False, lw=2)
            kit.ellipse(k, cx_ - sx * 2, 146 + (1.5 if hit and tl < th + 0.2 else 0), 11, 9, pm.SKIN, 6, shadow=False, lw=2)
        lift = mo.stamp_track(tl, th, 70, up_after=0.35)
        c.save(); c.translate(48, 80 - lift * 0.55); c.scale(1, 0.62)
        rs.stamp_prop(k, 0, 0, 0.75 + 0.4 * (lift / 70), "up", 0.0, 7)
        c.restore()
        if hit and tl < th + 0.24:
            rs.impact_lines(c, 48, 84, 2, 0.8)
    screen(k, tl, "s12b", d)


def s13b(k, t, tl):
    """The kiss: the stamp arrives, hangs about 0.6 s over the big kiss, THUNK (take A)."""
    def d():
        c = k.c
        th = 0.95
        dx, dy = mo.shake(tl, th, 3.6, 0.35, seed=13)
        c.translate(dx, dy)
        sss.table_top(c, 60)
        hit = tl >= th
        tx, ty, sc = 46, 116, 1.25
        tag2(k, tx, ty, sc, ("from", "to", "kiss") if hit else ("from", "to"))
        bx, by = tx + (BC2["kiss"][0] + (3.5 if TAG_FIX[0] else 0)) * sc, ty + BC2["kiss"][1] * sc
        if tl < 0.15:
            lift = 60 * (1 - ease(tl / 0.15)) + 24
        elif tl < 0.8:
            lift = 24 + 1.0 * math.sin(tl * 6)
        else:
            lift = mo.stamp_track(tl, th, 24, up_after=0.4)
        rs.stamp_prop(k, bx, by - lift - 3, 0.6, "down" if lift < 1 else "up", 0.0, 9)
        if hit and tl < th + 0.3:
            rs.impact_lines(c, bx, by, 3, 0.6)
        kx, ky = bx, by - lift - 3 - 46 * 0.6
        def fg(lc):
            import waiter_kit as w
            k2 = Ctx(lc, 0)
            kit.ellipse(k2, -4, 14, 40, 36, w.BODY, 3, shadow=False, lw=2.4)
            lc.set_source_rgb(*INK); lc.set_line_width(10); lc.set_line_cap(1)
            lc.move_to(14, 34); lc.line_to(kx - 5, ky - 2); lc.stroke()
            lc.set_source_rgb(0.60, 0.62, 0.66); lc.set_line_width(6.5)
            lc.move_to(14, 34); lc.line_to(kx - 5, ky - 2); lc.stroke()
        props.soft(c, fg, 1.6)
        kit.ellipse(k, kx - 3, ky, 5.5, 5.5, (0.60, 0.62, 0.66), 41, shadow=False, lw=1.6)
    screen(k, tl, "s13b", d)


def s14b(k, t, tl):
    def d():
        c = k.c
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()
        face = "incredulous" if 0.42 <= tl < 0.58 else "pressed"
        sink = 0.0
        if tl >= 0.58:
            face = "hurt"
            sink = 3.0 * ease((tl - 0.58) / 0.3)
        ps.pam(k, 49, 78 + sink - ps.HY * 1.5, 1.5, "stand", face, look=(0.1, 1.0), glasses="chain")
        tag2(k, 50, 164, 1.1, ("from", "to", "kiss"), rot=0.03)
    screen(k, tl, "s14b", d)


CAM15B = (492, 470, 1.15)
UNCL = (S.SST[0] + 26, S.TABLE_TOP + 24)                    # the UNCLAIMED corner of the table


def unclaimed_card(k, x, y):
    c = k.c
    kit.cut(k, [(x - 26, y), (x + 26, y), (x + 22, y - 22), (x - 22, y - 22)], (0.99, 0.99, 0.97), lw=1.6)
    c.select_font_face("Inter", 0, 1); c.set_font_size(8.4)
    e = c.text_extents("UNCLAIMED")
    c.set_source_rgb(0.45, 0.45, 0.50); c.move_to(x - e.x_advance / 2, y - 8); c.show_text("UNCLAIMED")


def don_gift(k, x, y, approved):
    c = k.c
    S.present(k, x, y, 124, 104, (0.20, 0.42, 0.70), (0.97, 0.97, 0.97), 980)
    kit.rect(k, x - 54, y - 94, 108, 64, (0.99, 0.99, 0.97), 981, shadow=False, lw=1.8)
    c.select_font_face("Permanent Marker", 0, 0)
    for txt, yy, sz, col in (("TO: SOFÍA", y - 74, 15, S.RED), ("FROM: DON", y - 54, 14, INK),
                             ("(SECRET!)", y - 36, 13, INK)):
        c.set_font_size(sz); e = c.text_extents(txt)
        dxh = 8 if txt.startswith("TO") else 0
        c.set_source_rgb(*col); c.move_to(x - e.x_advance / 2 - dxh, yy); c.show_text(txt)
        if dxh:
            pss.heart(c, x + e.x_advance / 2 + 2, yy - 5, 4.5, S.RED)
    if approved:
        c.save(); c.translate(x + 4, y - 14); c.rotate(-0.2)
        c.set_source_rgb(*rs.GREEN); c.set_line_width(3.2); c.rectangle(-50, -14, 100, 26); c.stroke()
        c.select_font_face("Inter", 0, 1); c.set_font_size(17); c.move_to(-45, 6); c.show_text("APPROVED")
        c.restore()


def s15b(k, t, tl):
    """Still, wide enough for both gifts: glasses back on; "Will Don get it?"; the robot moves her present to the
    UNCLAIMED corner; Don sets down his; "He won't." / pause / the tick / "You're welcome."; APPROVED on Don's."""
    def draw():
        S.backdrop(k, t=tl)
        sss.sofia_seated(k, "stand", "unimpressed" if tl > 3.4 else "neutral", look=(1, 0.1) if tl > 3.4 else (-1, 0.1),
                         lean=4 if tl > 3.4 else 0, lag=(-5, 0))
        S.desk(k)
        gx = X["sofia"] - 140
        gift_y = lerp(S.FEET - 200, S.FEET, ease((tl - 0.6) / 0.5)) if tl > 0.6 else None
        dd = ds.don(k, X["sofia"] - 215, S.FEET, 1.0, "stand", "smug", look=(1, -0.2), shades="down",
                    lean=6 if tl > 1.2 else 0)
        if gift_y is not None:
            don_gift(k, gx, gift_y, tl > 3.3)
        st = "eager" if tl < 2.4 else ("proud" if tl < 3.3 else "tick")
        moving = 1.8 <= tl < 2.4
        r = rs.robot(k, X["robot"] + 62, S.FEET_BACK, 1.0, rs.POSE_STAMP_DOWN if moving else "stand", st,
                     head_rot=0.1 if st == "proud" else None, talk=0.6 if (2.4 < tl < 2.9 or 3.3 < tl < 3.9) else 0,
                     t=tl)
        if tl < 0.4:
            o = ps.pam(k, X["don"], S.FEET, 1.0, ps.POSE_SHY, "pressed", look=(0, 1), glasses="chain")
        elif tl < 0.8:
            o = ps.pam(k, X["don"], S.FEET, 1.0, ps.POSE_GLASSES, "pressed", look=(0, 0.6), finger="bridge")
        else:
            o = ps.pam(k, X["don"], S.FEET, 1.0, ps.POSE_SHY, "incredulous",
                       look=(-0.6, 0.5) if tl < 1.0 else ((-1, -0.2) if tl < 2.4 else (-1, 0.3)),
                       mouth=talk(tl, 1.0, 1.7, 6))
        S.santa_table(k, pams=False)
        unclaimed_card(k, UNCL[0], UNCL[1] - 2)
        u = ease((tl - 1.8) / 0.6)
        px_ = lerp(X["don"] + 2, UNCL[0] + 4, u)
        py_ = lerp(S.FEET - 112, UNCL[1] - 22, u)
        S.present(k, px_, py_, 64 - 14 * u, 50 - 11 * u, S.RED, S.GOLD, 966)
        sss.tag(k, px_ + 28 - 6 * u, py_ - 38 + 8 * u, 1.0 - 0.2 * u, ("from", "to", "kiss"), rot=0.18)
        return o, r
    o, r = world(k, tl, "s15b", CAM15B, draw)
    if 0.95 < tl < 2.4:
        xb.speech(k, "Will Don get it?", above(CAM15B, o["head"], 70), t, 1.0, size=26, at=(330, 190))
    if 2.4 <= tl < 3.25:
        xb.speech(k, "He won't.", above(CAM15B, r["screen"], 60), t, 2.4, size=28, at=(170, 300))
    if tl >= 3.3:
        xb.speech(k, "You're welcome.", above(CAM15B, r["screen"], 60), t, 3.3, size=28, at=(190, 300))


def s16b(k, t, tl):
    """The same ECU as frame 0: Sofia soft behind the hand, a fresh blank tag slides in; cut to 1."""
    def d():
        c = k.c
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()
        def bg(lc):
            so.sofia(Ctx(lc, 0), 98 * 0.40, 174 * 0.34 - SHY, 1.0, "stand", "neutral", look=(-0.6, 0.1),
                     lag=(3, 0), badge=False, sparkle=0.0)
        props.soft(c, bg, 1.5)
        tag2(k, lerp(130, 62, ease(tl / 0.5)), 122, 1.0, blank=True, rot=0.06)
        sss.pam_hand(k, 0.0)
    screen(k, tl, "s16b", d)


PANELS = [(0.0, 3.6, s1), (3.6, 5.8, s2b), (5.8, 8.0, s3b), (8.0, 10.8, s4b), (10.8, 13.0, s5b), (13.0, 16.0, s6b),
          (16.0, 17.6, s7b), (17.6, 20.4, s8b), (20.4, 21.6, s9b), (21.6, 23.6, s10b), (23.6, 24.4, s11b),
          (24.4, 25.9, s12b), (25.9, 27.6, s13b), (27.6, 28.8, s14b), (28.8, 33.6, s15b), (33.6, 34.6, s16b)]
for _t0, _t1, _fn in PANELS:
    PANEL_DUR[_fn.__name__] = _t1 - _t0


def shake(t):
    return 0
