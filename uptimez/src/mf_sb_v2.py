"""v2 (mf_sb_v1.py = v1, kept): shot 4 split: 4a and 4c a two-shot from Sofia's side (she is centred, Don leans in
from the right, Pam out of frame); 4b a 0.6 s cutaway to Pam's close-up, 💗, on the word "arrest".
Mandatory Fun, silent storyboard v1 (engine_v.py, 540x960, 30 fps, 12 fps drawing). 33.0 s, the camera plan from
concept v2.2 / set sheet v2, the yank from mf_yank v2. Lines as bubbles, no voices yet. Only shots 1 (the slam) and 9
(the push-in) move; the engine's slow push is undone everywhere else. Shot list (s):
 1 0.0-2.6 slide + robot | 2 2.6-3.4 reverse | 3 3.4-5.6 the door, low + dutch | 4 5.6-10.0 tight two-shot, 💗 |
 4b 10.0-10.9 page turn insert | 5 10.9-13.9 three-shot | 6a 13.9-14.6 scan on Don | 6b 14.6-16.3 robot red |
 7 16.3-17.9 "a cop!", dutch | 8a 17.9-18.8 cuffs insert | 8b 18.8-20.0 turns to Pam | 9a 20.0-21.0 APPROVED! |
 9b 21.0-21.8 tick, DING | 10 21.8-24.2 wrists insert | 11 24.2-29.4 exit and yank | 12 29.4-33.0 FUN DETECTED."""
import math
import kit
from kit import INK, W, H
import mf_set as ms
import mf_set_sheet as ss
import mf_yank as yk
import sofia_mf as sm
import don_mf as dm
import pam_mf as pm
import robot_mf as rm
import props_mf as pr
import xmas_bubbles as xb
import emoji as _emoji

DURATION = 33.0
RAW_T = 0.0
X = ms.POS
SEAT = ss.SEAT
PANEL_DUR = {}


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def world(k, tl, name, cam, draw):
    """Undo the engine push, apply the camera, draw the world; returns what draw() returns."""
    c = k.c
    d = PANEL_DUR[name]
    push = 1 + 0.03 * (tl / d)
    c.save()
    c.translate(W / 2, H / 2); c.scale(1 / push, 1 / push); c.translate(-W / 2, -H / 2)
    ms.with_cam(c, cam)
    out = draw()
    c.restore()
    return out


def scr(cam, x, y):
    return ms.to_screen(cam, x, y)


def pop_heart(k, x, y, tl, t0=0.0, hold=0.6, r=40):
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


# ---------------------------------------------------------------- 1. the slide slams on
CAM1 = (330, 400, 1.35)


def s1(k, t, tl):
    z = lerp(1.6, 1.35, ease(tl / 0.22))                     # the slam: an instant punch, settling in 0.2 s
    cam = (CAM1[0], CAM1[1], z)

    def draw():
        ss.base(k)
        return rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", "eager", talk=0.6 if 0.5 < tl < 2.2 else 0,
                        t=tl, seed=97)
    o = world(k, tl, "s1", cam, draw)
    xb.speech(k, "Attendance is mandatory.\nSo is fun.", scr(cam, *o["screen"]), t, 0.45, size=24)


# ---------------------------------------------------------------- 2. reverse: they read
CAM2 = (690, 520, 1.3)


def s2(k, t, tl):
    def draw():
        ss.base(k)
        o = ss.sofia_writing(k)
        ss.pam_seated(k, "stand", "read")
        ms.table(k)
        ss.sofia_props(k, o)
    world(k, tl, "s2", CAM2, draw)


# ---------------------------------------------------------------- 3. the door bangs: low + dutch
CAM3 = (96, 420, 1.75, -0.14)


def s3(k, t, tl):
    c = k.c
    sh = (8 if int(tl * 30) % 2 == 0 else -8) if tl < 0.1 else 0
    c.save(); c.translate(sh, 0)
    op = ease(tl / 0.15)

    def draw():
        ss.base(k, door_open=op)
        if op > 0.4:
            return dm.don(k, X["door"] + 26, ms.FLOOR_Y + 60, 1.05, ss.POSE_DOORWAY, "hero", lean=4, seed=98)
        return None
    o = world(k, tl, "s3", CAM3, draw)
    c.restore()
    if o:
        xb.speech(k, "AI Police!\nWho's going to jail?", scr(CAM3, *o["head"]), t, 3.75, size=26)


# ---------------------------------------------------------------- 4. two-shot from Sofia's side (v2), Pam's cutaway
CAM4 = (596, 515, 1.55)


def _two(k, t, tl, name):
    face = "wink" if t < 8.5 else "smug"
    sface = "neutral" if not (7.6 <= t < 8.4) else "eyebrow"
    slook = (0, 0.7) if not (7.6 <= t < 8.4) else (0.9, 0.1)

    def draw():
        ss.base(k, empty_chair=False)
        o = {}
        ms.seated(k, lambda: o.update(sm.sofia(k, X["sofia"], SEAT, 1.0, "write", sface, look=slook, seed=95)))
        ms.chair_back(k, X["don"], seed=130)
        d = dm.don(k, X["don"] - 26, ms.FEET, 1.0, dm.POSE_LEAN, face, lean=-11, look=(-1, 0.5), seed=98)
        ms.table(k)
        ss.sofia_props(k, o)
        return o, d
    o, d = world(k, tl, name, CAM4, draw)
    if t < 6.9:
        xb.speech(k, "Sofía, you're\nunder arrest.", scr(CAM4, *d["head"]), t, 5.75, size=26)
    elif 7.6 <= t < 8.4:
        xb.speech(k, "For what?", scr(CAM4, *o["head"]), t, 7.6, size=26)
    elif t >= 8.5:
        xb.speech(k, "Stealing my\nattention.", scr(CAM4, *d["head"]), t, 8.5, size=26)


def s4(k, t, tl):
    _two(k, t, tl, "s4")


def s4c(k, t, tl):
    _two(k, t, tl, "s4c")


CAM4P = (838, 512, 2.7)


def s4p(k, t, tl):                                         # Pam hears "arrest": over the glasses, 💗
    def draw():
        ss.base(k, empty_chair=False)
        p_ = ss.pam_seated(k, "stand", "peer", look=(-1, -0.2))
        ms.table(k)
        return p_
    p_ = world(k, tl, "s4p", CAM4P, draw)
    hx, hy = scr(CAM4P, *p_["head"])
    pop_heart(k, hx + 120, hy - 150, tl, 0.08, 0.42, 48)


# ---------------------------------------------------------------- 4b. insert: the page turn
CAM4B = (552, 650, 5.0)


def s4b(k, t, tl):
    turn = ease((tl - 0.15) / 0.45)

    def draw():
        ss.base(k, empty_chair=False)
        o = {}
        ms.seated(k, lambda: o.update(sm.sofia(k, X["sofia"], SEAT, 1.0, "page", "unimpressed", look=(0, 0.9),
                                               seed=95)))
        ms.table(k)
        sm.notebook(k, X["sofia"] + 2, ms.TABLE_TOP + 4, 0.62, "open", turn)
        for hx, hy in o["hands"]:
            kit.ellipse(k, hx, min(hy, ms.TABLE_TOP + 2), 8.5, 8.5, sm.SKIN, 1403, shadow=False, lw=2)
    world(k, tl, "s4b", CAM4B, draw)


# ---------------------------------------------------------------- 5. three-shot: the confession, the sulk
CAM5 = (720, 500, 1.35)


def s5(k, t, tl):
    sulk = t >= 12.4
    pface = "hopeful" if t < 13.2 else "fade"

    def draw():
        ss.base(k, empty_chair=False)
        o = ss.sofia_writing(k)
        p_ = ss.pam_seated(k, pm.POSE_FINGER if t < 13.2 else "stand", pface, finger=t < 13.2, look=(-0.8, 0))
        if sulk:
            dm.don(k, X["don"], ms.FEET, 1.0, dm.POSE_CROSS, "pout", look=(-1, 0), seed=98)
        else:
            dm.don(k, X["don"], ms.FEET, 1.0, "stand", "hero", look=(-1, 0.3), seed=98)
        ms.table(k)
        ss.sofia_props(k, o)
        return p_
    p_ = world(k, tl, "s5", CAM5, draw)
    if t < 12.6:
        xb.speech(k, "Officer?\nI confess.", scr(CAM5, *p_["head"]), t, 11.1, size=24)


# ---------------------------------------------------------------- 6a. the scan sweeps Don's sulk
CAM6A = (690, 390, 2.7)


def s6a(k, t, tl):
    c = k.c

    def draw():
        ss.base(k, empty_chair=False)
        return dm.don(k, X["don"], ms.FEET, 1.0, dm.POSE_CROSS, "pout", look=(-1, 0), seed=98)
    d = world(k, tl, "s6a", CAM6A, draw)
    hx, hy = scr(CAM6A, *d["head"])
    p = clamp(tl / 0.6)
    rm.scan_beam(k, (-60, hy - 40), (hx, hy), 130, p)


# ---------------------------------------------------------------- 6b. robot close-up: red
CAM6 = (420, 470, 2.6)


def s6b(k, t, tl):
    state = "scan" if tl < 0.15 else "insufficient"

    def draw():
        ss.base(k, empty_chair=False)
        return rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", state, t=tl, seed=97)
    o = world(k, tl, "s6b", CAM6, draw)
    xb.speech(k, "Failure to enjoy training.\nDetention required.", (270, 760), t, 14.9, at=(270, 810), size=22)


# ---------------------------------------------------------------- 7. "You can't arrest a cop!" dutch
CAM7 = (690, 440, 2.0, 0.13)


def s7(k, t, tl):
    def draw():
        ss.base(k, empty_chair=False)
        ss.sofia_writing(k)
        return dm.don(k, X["don"], ms.FEET, 1.0, dm.POSE_CLUTCH, "indignant", look=(-0.6, -0.2), seed=98)
    d = world(k, tl, "s7", CAM7, draw)
    xb.speech(k, "You can't\narrest a cop!", scr(CAM7, *d["head"]), t, 16.4, size=28)


# ---------------------------------------------------------------- 8a. insert: the robot lifts the cuffs
CAM8A = (668, 618, 3.2)


def s8a(k, t, tl):
    u = ease((tl - 0.2) / 0.5)

    def draw():
        ss.base(k, empty_chair=False)
        dm.don(k, X["don"], ms.FEET, 1.0, "stand", "freeze", belt_cuffs_on=tl < 0.2, look=(-1, 0.6), seed=98)
        hand = (0.0, -6, 0, (-20, 0), (lerp(62, 92, u), lerp(34, 20, u)))
        rm.robot(k, X["don"] - 110, ms.FEET + 40, 1.0, hand, "approval" if tl > 0.6 else "eager", cuffs=tl >= 0.2,
                 seed=97)
    world(k, tl, "s8a", CAM8A, draw)


# ---------------------------------------------------------------- 8b. it freezes, turns to Pam
CAM8B = (610, 470, 1.15)


def s8b(k, t, tl):
    u = ease(tl / 0.3)
    pose = (lerp(0.0, -0.14, u), -6, 0, (-20, 0), (150, 24))

    def draw():
        ss.base(k, empty_chair=False)
        ss.sofia_writing(k)
        ss.pam_seated(k, "stand", "neutral", look=(-1, 0))
        dm.don(k, X["don"], ms.FEET, 1.0, dm.POSE_CLUTCH, "indignant", belt_cuffs_on=False, look=(-1, 0), seed=98)
        ms.table(k)
        return rm.robot(k, X["robot"] + 90, ms.FEET + 30, 1.1, pose, "approval", cuffs=True, seed=97,
                        head_rot=lerp(0, -0.16, u), head_dx=lerp(0, -6, u))
    o = world(k, tl, "s8b", CAM8B, draw)
    xb.speech(k, "Human approval\nrequired.", scr(CAM8B, *o["screen"]), t, 19.0, size=24)


# ---------------------------------------------------------------- 9a. Pam: APPROVED! (push-in)
def s9a(k, t, tl):
    cam = (840, 500, lerp(2.4, 2.9, ease(tl / 0.35)))
    loud = tl >= 0.22

    def draw():
        ss.base(k, empty_chair=False)
        if loud:
            p_ = ss.pam_seated(k, pm.POSE_APPROVE, "approve", glasses="flash", thumb=True)
        else:
            p_ = ss.pam_seated(k, "stand", "neutral", look=(-1, 0))
        ms.table(k)
        return p_
    p_ = world(k, tl, "s9a", cam, draw)
    if loud:
        xb.shout(k, "APPROVED!", scr(cam, p_["head"][0], p_["head"][1] - 62), t, 20.22, cy=190, size=44)


# ---------------------------------------------------------------- 9b. the robot: tick, nod, DING
def s9b(k, t, tl):
    nod = math.sin(clamp(tl / 0.35) * math.pi) * 0.18

    def draw():
        ss.base(k, empty_chair=False)
        return rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", "approved", head_rot=nod, head_dx=nod * 20,
                        seed=97)
    o = world(k, tl, "s9b", CAM6, draw)
    if tl > 0.05:
        sx, sy = scr(CAM6, *o["screen"])
        k.c.set_source_rgb(*rm.GREEN); k.c.set_line_width(5); k.c.set_line_cap(1)
        for a in (-1.0, -0.5, 0.0, 0.5, 1.0):
            k.c.move_to(sx + 150 * math.sin(a), sy - 150 * math.cos(a))
            k.c.line_to(sx + 185 * math.sin(a), sy - 185 * math.cos(a)); k.c.stroke()


# ---------------------------------------------------------------- 10. insert: two clicks, hers louder
CAM10 = (764, 622, 3.2)


def s10(k, t, tl):
    don_open = 0.0 if tl >= 0.6 else 1.0
    pam_open = 0.0 if tl >= 1.4 else 1.0

    def draw():
        ss.base(k, empty_chair=False)
        ms.table(k)
        dx_, px_ = X["don"] + 10, X["pam"] - 60
        y = ms.TABLE_TOP - 4
        kit.ellipse(k, dx_ - 12, y + 2, 10, 10, dm.SKIN, 8, shadow=False, lw=2)
        kit.ellipse(k, px_ + 12, y + 2, 9, 9, pm.SKIN, 9, shadow=False, lw=2)
        a_ = pr.cuff(k, dx_ + 2, y, 1.0, math.pi / 2, open=don_open, loop_side=1)
        b_ = pr.cuff(k, px_ - 2, y, 1.0, math.pi / 2, open=pam_open, loop_side=-1)
        pr.chain(k, a_[0], a_[1], b_[0], b_[1], 1.0, sag=0.2)
        if 0.6 <= tl < 1.0:
            pr.click(k, a_[0] - 22, y - 16, 0.9)
        if 1.4 <= tl < 1.9:
            pr.click(k, b_[0] + 22, y - 16, 1.5)
    world(k, tl, "s10", CAM10, draw)


# ---------------------------------------------------------------- 11. wide: exit and yank (mf_yank v2 timing)
def s11(k, t, tl):
    yt = min(tl, yk.DURATION - 0.01)
    yk.RAW_T = yt
    yk.frame(k, yt, yt)
    if t >= 27.6:
        hx, hy = scr(yk.CAM, X["pam"], SEAT + pm.HY - 30)
        xb.speech(k, "So… dinner?", (hx, hy), t, 27.6, size=28)


# ---------------------------------------------------------------- 12. the beam crosses Don, lands on Pam
CAM12 = (622, 470, 1.15)


def s12(k, t, tl):
    land = tl >= 1.0
    state = "scan" if not land else "detected"

    def draw():
        ss.base(k, empty_chair=False)
        d = {}
        ms.seated(k, lambda: d.update(dm.don(k, X["don"], SEAT - 20, 1.0, dm.POSE_STIFF, "panic",
                                             belt_cuffs_on=False, seed=98)))
        p_ = ss.pam_seated(k, ss.PAM_ARM, "happy")
        o = rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", state, t=tl, seed=97)
        ms.table(k)
        ss.chain_on_table(k, (X["don"] + 44, ms.TABLE_TOP - 6))
        kit.ellipse(k, X["don"] + 36, ms.TABLE_TOP - 2, 9, 9, dm.SKIN, 8, shadow=False, lw=2)
        pr.cuff(k, X["don"] + 46, ms.TABLE_TOP - 4, 1.0, math.pi / 2, loop_side=1)
        if tl >= 0.2:
            u = ease((tl - 0.2) / 0.7)
            tx = lerp(d["head"][0], p_["head"][0], u)
            ty = lerp(d["head"][1], p_["head"][1], u)
            ss.laser(k, o["screen"], (tx, ty), rm.GREEN if land else rm.CYAN)
        return o
    o = world(k, tl, "s12", CAM12, draw)
    if t >= 30.9:
        xb.speech(k, "Mandatory fun.\nSuccessful.", scr(CAM12, *o["screen"]), t, 30.9, size=24)


PANELS = [(0.0, 2.6, s1), (2.6, 3.4, s2), (3.4, 5.6, s3), (5.6, 6.9, s4), (6.9, 7.5, s4p), (7.5, 10.0, s4c), (10.0, 10.9, s4b), (10.9, 13.9, s5),
          (13.9, 14.6, s6a), (14.6, 16.3, s6b), (16.3, 17.9, s7), (17.9, 18.8, s8a), (18.8, 20.0, s8b),
          (20.0, 21.0, s9a), (21.0, 21.8, s9b), (21.8, 24.2, s10), (24.2, 29.4, s11), (29.4, 33.0, s12)]
for _t0, _t1, _fn in PANELS:
    PANEL_DUR[_fn.__name__] = _t1 - _t0


def shake(t):
    return 0
