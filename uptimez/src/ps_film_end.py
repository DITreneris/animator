"""PICK A SIDE: the new ending animated (story audit v1 §7-13, stills v8; Tomas 26 Nov: "taisom ir einam prie
animacijos"). Opt-in, a separate module: it patches ps_film's maps for scenes 5 and 6 at run time only, so the locked
scene 5 v8 and scene 6 v3 (and every other scene) build exactly as before from ps_film itself.

  python3 ps_film_end.py film 5 9     -> ../pick-a-side/ps_film_s5_v9_540.mp4
  python3 ps_film_end.py film 6 4     -> ../pick-a-side/ps_film_s6_v4_540.mp4

Scene 5: 5.1 the guard knocks at the shut glass, the blank invitation in his hand / 5.2 the pen writes SOFÍA (5 letters)
/ 5.3 the door slides open, the robot: "Welcome." -> the hand-over (variant C, 2/2 in the silhouette test) -> the can,
the heart (the old 5.3b) / 5.4, 5.5 as locked / 5.5b both her shoes over the tape, Don's on his side / 5.6, 5.7 as locked.
Scene 6: 6.1 "Everyone's with me." while Pam's thumb presses ACCEPT behind him / 6.1b (1.5 s) freeze -> shock -> the arms
drop / 6.2 (1.4 s) he yanks the blind down, eyes shut, scowling -> the robot yanks it up -> exactly 1.1's frame 0."""
import math
import os
import sys
import cairo
import numpy as np
import ps_film as pf
import ps_ending_v2 as e
import ps_motion as pm_

ps, pss, sp, hp, co = e.ps, e.pss, e.sp, e.hp, e.co
F = e.F
ease, lerp = pf.ease, pf.lerp


# --- 5.1: knock, knock ------------------------------------------------------------------------------------------------
KNOCKS_51 = (0.40, 0.58, 0.76)                               # three knocks; the fist back off the glass between them


def s51(t):
    near = any(0.0 <= t - k_ < 0.07 for k_ in KNOCKS_51)     # the drawing on the glass: the contact spot and strokes
    def cast(k):
        heads = {}
        def draw_():
            back = 0 if near else (-16 if t >= KNOCKS_51[0] - 0.12 else -30)
            return e.guard_at(k, e.sto.DOOR[0] + e.sto.DOOR[2] / 2 - 4, pose_r=(104 + back, -262 + 6 * (back != 0)), pose_l=(-40, -200))
        o = e.through_glass(k, draw_, 0.0)
        heads["guard"] = (o["head"][0], o["head"][1], 40 * e.GS)
        lx, ly = o["hands"][0]
        e.cv_plain(k, lx - 4, ly + 22, 0.62, word=False)
        e.fingers(k, lx + 6, ly + 2, d=-1)
        if near:
            rx, ry = o["hands"][1]
            c = k.c
            c.set_source_rgba(1, 1, 1, 0.55); c.save(); c.translate(rx + 8, ry); c.scale(5, 10); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            c.set_source_rgb(*e.INK); c.set_line_width(2.6); c.set_line_cap(1)
            for a in (-0.7, 0.0, 0.7):
                c.move_to(rx + 14 + 6 * math.cos(a), ry + 12 * math.sin(a)); c.line_to(rx + 14 + 18 * math.cos(a), ry + 24 * math.sin(a)); c.stroke()
            c.set_line_cap(0)
        return heads
    pss.DOOR_OPEN[0] = 0.0
    return dict(ps.S("5.1n", (130, F - 150, 1.75), dict(blind="torn", tape=True, spun=True), cast), own_cam=True)


# --- 5.2: the pen writes all five letters -------------------------------------------------------------------------------
PEN_52_END = ((0.15, 1, -36), (0.40, 2, -15), (0.65, 3, 0), (0.90, 4, 15), (1.15, 5, 36))   # (time, letters, nib dx): the
                                                             # name's advance at 10.5 pt x the insert's ~3 px a unit


# --- 5.3: the door slides open, "Welcome." -> the hand-over -> the can, the heart ----------------------------------------
A_53, B_53 = 1.25, 2.45
CAM_53A, ROB_53A, SOF_53A = [177], [238], [302]   # film: OUR FIRST CLIENT out past the right edge (stills v8 cut it), her face off the rail                                      # 5.3a .. 5.3c .. 5.3b (the old shot from its TREAT_AT on)
SLIDE_53 = (0.05, 0.20)                                      # the glass slides in ~0.15 s (lesson 133, The Onboarding)


def s53a(t):
    o_ = 0.85 * ease((t - SLIDE_53[0]) / (SLIDE_53[1] - SLIDE_53[0]))
    def cast(k):
        heads = {}
        step = ease((t - 0.22) / 0.35)                      # outside behind the glass until it has slid; then he steps in
        gx_ = pss.GX0 + pss.GW / 2 - 4 + 44 * step
        if step <= 0:
            o = e.through_glass(k, lambda: e.guard_at(k, gx_, pose_l=(-40, -200)), o_)
        else:
            o = e.guard_at(k, gx_, pose_l=(-40, -200))
        heads["guard"] = (o["head"][0], o["head"][1], 40 * e.GS)
        lx, ly = o["hands"][0]
        e.cv_plain(k, lx - 4, ly + 22, 0.62)
        e.fingers(k, lx + 6, ly + 2, d=-1)
        _, heads["sofia"] = ps.sofia(k, (SOF_53A[0], F + 60), "hip", "smile", (-1, -0.2))
        bob = -4 if 0.20 < t < 0.75 and int(t * 7.5) % 2 else 0   # its wheel-bob with its word (of_film s32)
        _, heads["robot"] = ps.robot(k, (ROB_53A[0], F + 40 + bob), arms=((-80, -30), (40, 0)), look=(-1, -0.3))
        return heads
    ps.ROBOT_WALL["5.3n"] = 1
    pss.DOOR_OPEN[0] = o_
    return dict(ps.S("5.3n", (CAM_53A[0], F - 160, 1.45), dict(blind="torn", tape=True, spun=True), cast), own_cam=True)


def _arm(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def cast_53c_anim(k, t):
    """the hand-over in 1.2 s (variant C): he holds it out (0-0.25), her arm comes up open (0.25-0.55), she steps in
    (0.55-0.75), her hand closes on its edge (0.75-0.85), he lets go and folds his hands, it goes with her (0.85-1.2)."""
    heads = {}
    sb = sp.sbc
    full = e.SOF_53["C"]
    ua = ease(t / 0.25)
    ub = ease((t - 0.25) / 0.30)
    uc = ease((t - 0.55) / 0.20)
    held = t >= 0.75
    ue = ease((t - 0.85) / 0.30)
    pr = _arm((120, -40), (185, -120), ua)                  # his arm from his side, out to her
    if ue > 0:
        pr = _arm((185, -120), (120, -40), ue)
    o = e.guard_at(k, 148, pose_r=pr if ue < 1 else None)
    heads["guard"] = (o["head"][0], o["head"][1], 40 * e.GS)
    gx, gy = o["hands"][1]
    sb.POSES["_take53"] = full + (8, 0)
    gx_f, gy_f = None, None                                  # where his hand is when fully out (the still's solve)
    k.c.push_group()
    try:
        of = e.guard_at(k, 148, pose_r=(185, -120)); gx_f, gy_f = of["hands"][1]
    finally:
        k.c.pop_group()
    H = (gx_f + e.C53_DX[0] + 26 + 17 + e.C53_GAP[0], gy_f + 14)
    ox, oy = e._sofia_hand_off(k, "_take53")
    sx0 = H[0] - ox
    sx = sx0 - (e.C53_GAP[0] + 4) * uc                      # the step in: her fingertips onto the card's edge
    pose = _arm((-8, 0), full, ub)
    if ue > 0:
        pose = _arm(full, (-30, 110), ue)                   # the card comes in to her (the "hip" arm)
    sb.POSES["_take53a"] = pose + (8, 0)
    legs = {0: ((9, 7), (-7, 0))}.get(0 if 0.58 < t < 0.70 else None)
    sp.ss.LEGS[0] = legs
    try:
        os_, heads["sofia"] = ps.sofia(k, (sx, F + 60 - (2 if legs else 0)), "_take53a", "interested", (-1, 0.3))
    finally:
        sp.ss.LEGS[0] = None
    hx, hy = min(os_["hands"], key=lambda h: h[0])
    skin_s = sb.sf.SKIN
    if not held:
        e._card_at(k, gx + e.C53_DX[0], gy + 6, -0.18)
        hp.draw(k, "grab", gx, gy, 24, co.SKIN, (1.0, 0.2), 1)
        if ub > 0:
            hp.draw(k, e.C53_SHAPE[0][0], hx, hy, e.C53_SHAPE[0][1], skin_s, e.C53_SHAPE[0][2], -1)
    else:                                                    # hers now: the card off her fingers' far side
        e._card_at(k, hx - 17 - 26 + 8, hy - 8, lerp(-0.18, -0.06, ue))
        if ue < 0.35:
            hp.draw(k, "grab", gx, gy, 24, co.SKIN, (1.0, 0.2), 1)
        hp.draw(k, "grab", hx, hy, 21, skin_s, (-1.0, -0.1), -1)
    return heads


def s53c(t):
    pss.DOOR_OPEN[0] = 0.0
    return dict(ps.S("5.3c", (300, F - 150, 1.4), dict(blind="rehung", tape=True, spun=True, mark=False),
                     lambda k: cast_53c_anim(k, t)), own_cam=True)


def s53(t):
    if t < A_53:
        return s53a(t)
    if t < B_53:
        return s53c(t - A_53)
    pss.DOOR_OPEN[0] = 0.0
    return pf.s53(t - B_53 + pf.TREAT_AT)                    # the old 5.3b, from its own TREAT_AT


# --- 5.5b: her step over the tape; his shoe stays -----------------------------------------------------------------------
def s55b(t):
    lift = ease((t - 0.25) / 0.25) * (1 - ease((t - 0.55) / 0.25))   # her far foot steps on, away from his side
    def draw(k):
        c = k.c
        was = e.ins_55b
        c.set_source_rgb(*e.kit.FLOOR); c.paint()
        tb = 70
        e.cut(k, [(70 + tb, 960), (150 + tb, 960), (300, 0), (250, 0)], pss.TAPE, shadow=False, lw=2.4)
        c.set_source_rgba(1, 1, 1, 0.40); c.set_line_width(3); c.move_to(96 + tb, 940); c.line_to(262, 20); c.stroke()
        for j, (x, y, s) in enumerate(((340, 540, 0.80), (395, 800, 0.95))):
            dy = -40 * lift if j == 0 else 0
            c.save(); c.translate(x + 10 * lift * (j == 0), y + dy); c.scale(-1, 1)
            sp.heel(k, 0, 0, s, tape=False)
            c.restore()
        e.cut(k, [(150, -10), (470, -10), (480, 120), (420, 140), (330, 150), (230, 140), (160, 120)], (0.97, 0.95, 0.90), lw=2.6)
        c.set_source_rgb(0.80, 0.76, 0.66); c.set_line_width(2); c.move_to(320, 0); c.line_to(318, 146); c.stroke()
        e.don_foot_55b(k)
        e.kit.text(k, "DON", 60, 600, 30, e.INK)
        return {}
    return ps.S("5.5b", "screen", draw=draw)


# --- 6.1: "Everyone's with me." and, behind him, her thumb on ACCEPT ------------------------------------------------------
PRESS_61 = 1.90                                              # after his line: the thumb comes down, the ring comes on


def cast_61(k, t, buzz=False):
    heads = {}
    _, heads["mom"] = ps.mom(k, "mom_tape", "folded", "stern", (1, -0.6))
    o, heads["sofia"] = ps.sofia(k, (ps.SOF_61[0], F + 40), "chest", "smile", (0.2, 0.6))
    hx, hy = o["hands"][0]
    sp.cv_coo(k, hx + 4, hy + 40, ps.CV_61[0] * 0.82)
    o, heads["pam"] = ps.pam(k, (e.PAM_X_61N[0], F + 40), "cup_mid", "avert", (0.6, 0.8), mug=False)
    px, py = o["hands"][1]
    c = k.c
    ph = 0.34
    cy = py + 8
    pressed = t >= PRESS_61
    jx = (2.0 if int(round(t * pf.DPS)) % 2 else -2.0) if buzz else 0.0
    c.save(); c.translate(px + 2 + jx, cy)
    pss.phone_close(k, 0, 0, ph, lit=True, buzz=buzz)
    if pressed and not buzz:
        c.set_source_rgba(0.20, 0.85, 0.40, 0.65); c.set_line_width(3.5)
        c.new_path(); c.arc(0, 62 * ph, 30 * ph, 0, 2 * math.pi); c.stroke()
    c.restore()
    u = ease((t - (PRESS_61 - 0.35)) / 0.30) if not buzz else 1.0   # the thumb from above the button, down onto it
    bx, by = px + 2 + jx, cy + 62 * ph - 14 * (1 - u)
    sk = __import__("pam_mf").SKIN
    for col, lw in ((e.INK, 6.4), (sk, 4.4)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.move_to(bx + 16, by + 14); c.line_to(bx + 3, by + 1); c.stroke()
    c.set_line_cap(0)
    return heads


def s61(t):
    sh = pf.s61(t)                                           # his thumbs come up with the line (the locked 6.1's fg)
    return dict(sh, cast=lambda k: cast_61(k, t), room=dict(sh["room"], phone=None))


# --- 6.1b: freeze -> shock -> the arms drop (1.5 s) -----------------------------------------------------------------------
FREEZE_61B, DROP_61B = 0.30, 0.90


def s61b(t):
    i = int(round(t * pf.DPS))
    b = pf.BOARD["6.1b"]
    buzz = t < DROP_61B
    def fg(k):
        e.k_hold[0] = k
        if t < FREEZE_61B:
            return e.fg_61x(e.LOOK_PHONE[0], "grin", "thumbs", spring=None)
        if t < DROP_61B:
            j = i - int(round(FREEZE_61B * pf.DPS))
            sp_ = {0: 1.35, 1: 0.80, 2: 1.12}.get(j, 1.0)   # the spring's overshoot (test I's SPRING_AT)
            ln = e.LEAN_TEAM[0] * min(1.0, (j + 1) / 2.0)    # the head goes over to the team in two drawings
            return e.fg_61x(e.LOOK_TEAM[0], "shock", "vest", spring=sp_, lean=ln)
        return e.fg_61x(e.LOOK_DROP[0], e.FACE_DROP[0], "stand", spring=None)
    return dict(b, cast=lambda k: cast_61(k, t + 3.0, buzz=buzz), room=dict(b["room"], phone=None), fg=fg)


# --- 6.2: down (eyes shut, scowling) -> the robot up -> 1.1's frame 0 (1.4 s) ---------------------------------------------
DOWN_62, UP_62, END_62 = (0.0, 0.45), (0.45, 0.90), 0.90


def s62(t):
    if t >= END_62:
        return dict(pm_.shot_A(0.0, v4=True), id="6.2")     # exactly 1.1's frame 0: no switch of ours set
    if t < DOWN_62[1]:
        tt = 0.20 + 0.35 * ease((t - DOWN_62[0]) / (DOWN_62[1] - DOWN_62[0]))
        sh = e.s62x(tt, "6.2", True)
    else:
        tt = 0.55 + 0.2999 * ease((t - UP_62[0]) / (UP_62[1] - UP_62[0]))
        sh = e.s62x(tt, "6.2", False)
        inner = sh["cast"]
        def cast(k):                                         # his eyes snap open as it goes up
            orig = ps.don
            def don_(k_, at, pose, face, *a, **kw):
                return orig(k_, at, pose, "shock", *a, **kw)
            ps.don = don_; pm_.ps.don = don_
            try:
                return inner(k)
            finally:
                ps.don = orig; pm_.ps.don = orig
        sh = dict(sh, cast=cast)
    return dict(sh, id="6.2")


# --- the maps ----------------------------------------------------------------------------------------------------------
def _door_reset(fn):
    def f(t):
        pss.DOOR_OPEN[0] = 0.0
        return fn(t)
    f.__name__ = fn.__name__
    return f


def setup():
    e.look()
    pf.SCENES[5] = ["5.1", "5.2", "5.3", "5.4", "5.5", "5.5b", "5.6", "5.7"]
    pf.TIMING["5.5b"] = dict(shot="5.5b", len=1.0, line=None, takes=[], take_at=[])
    pf.DUR["5.5b"], pf.TAKE_AT["5.5b"] = 1.0, []
    pf.BOARD["5.5b"] = dict(e.s55b(), id="5.5b")
    pf.DUR["5.3"] = pf.DUR["5.3"] + (B_53 - pf.TREAT_AT)     # 5.3c's 1.2 s
    pf.DUR["6.1b"], pf.DUR["6.2"] = 1.5, 1.4
    pf.PEN_52 = PEN_52_END
    for sid, fn in (("5.1", s51), ("5.3", s53), ("5.5b", s55b), ("6.1", s61), ("6.1b", s61b), ("6.2", s62)):
        pf.SHOT_FN[sid] = fn
    for sid in ("5.2", "5.4", "5.5", "5.6", "5.7"):
        pf.SHOT_FN[sid] = _door_reset(pf.SHOT_FN[sid])
    pf.sound = sound
    pf.ALLOW["5.3"] = ("ZONE: the robot's card",)            # 5.3c: the throne's card is background here (the hand-over is the
                                                             # story), in the rail at x 429-534; moving the camera puts her face there
    ps.ROBOT_WALL["5.3"] = 1                                 # the film renders 5.3a under its sid: its box right of its visor
    pf.STRIP8[5], pf.STRIP8[6] = (2.8, 5.6), (2.9, 5.9)


# --- sound ---------------------------------------------------------------------------------------------------------------
_old_sound = pf.sound


def sound(n, path):
    """the scene's takes at their shots, then the ending's own effect map; room tone; mastered as ps_film's (-15 LUFS)"""
    import soundfile as sf
    import of_sound as osd
    import sound_bc_mix as bm_
    SR = osd.SR
    starts, acc = {}, 0.0
    for sid in pf.SCENES[n]:
        starts[sid] = acc; acc += pf.DUR[sid]
    buf = np.zeros(int((acc + 0.3) * SR))
    for sid in pf.SCENES[n]:
        for tk, at in zip(pf.TIMING[sid]["takes"], pf.TAKE_AT[sid]):
            a, sr = pf._take(tk)
            if sr != SR:
                from scipy.signal import resample_poly
                a = resample_poly(a, SR, sr)
            osd.put(buf, a, starts[sid] + at, 1.0)
    def rattle_run(d, pitch):
        out = np.zeros(int(d * SR))
        for j in range(int(d * 40)):
            c_ = osd.rattle() * (0.5 + 0.5 * osd.rng.random())
            i = int((j / 40.0 + 0.004 * osd.rng.random()) * SR)
            out[i:i + len(c_)] += c_[:max(0, len(out) - i)]
        return osd.hp(out, max(1, int(6 / pitch)))
    def tone(f0, f1, d, k_=8.0):
        tt = osd.t_(d); ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(tt))) / SR
        return np.sin(ph) * np.minimum(1.0, tt / 0.005) * np.exp(-tt * k_)
    S_ = starts
    tt = osd.t_(0.04); clk = osd.hp(osd.noise(0.04), 2) * np.exp(-tt * 120)
    if n == 5:
        for k_ in KNOCKS_51:                                  # 5.1 three knocks on glass (outside: a little muffled)
            osd.put(buf, osd.lp(osd.slam() * 0.30, 2), S_["5.1"] + k_, 0.30)
        for at, _n, _dx in pf.PEN_52:                         # 5.2 a scratch per letter
            sc = osd.hp(osd.noise(0.16), 3) * np.sin(np.pi * osd.t_(0.16) / 0.16) * (1 + 0.5 * np.sin(2 * np.pi * 55 * osd.t_(0.16)))
            osd.put(buf, sc, S_["5.2"] + at - 0.10, 0.16)
        osd.put(buf, osd.hp(osd.noise(0.18), 3) * np.sin(np.pi * osd.t_(0.18) / 0.18), S_["5.3"] + SLIDE_53[0], 0.22)   # the glass slides
        osd.put(buf, osd.slam() * 0.12, S_["5.3"] + SLIDE_53[1], 0.20)
        osd.put(buf, osd.hp(osd.noise(0.12), 2) * np.sin(np.pi * osd.t_(0.12) / 0.12), S_["5.3"] + A_53 + 0.80, 0.18)   # paper: hers
        osd.put(buf, clk, S_["5.3"] + A_53 + 0.62, 0.40)      # her step in
        osd.put(buf, tone(2100, 2100, 0.25, 9) + 0.5 * tone(3150, 3150, 0.25, 12), S_["5.3"] + B_53 + 0.40, 0.14)   # the can
        osd.put(buf, bm_.chime([1319, 1568], gap=0.08, d=0.4), S_["5.3"] + B_53 + 0.45, 0.10)                     # the heart
        osd.put(buf, clk, S_["5.5b"] + 0.68, 0.50)            # 5.5b her heel down past the tape
        for j in range(5):                                    # 5.6 her heels across
            osd.put(buf, clk, S_["5.6"] + 0.6 + 0.2 * j, 0.45)
        osd.put(buf, bm_.buzz_phone(pf.BUZZ_57[1] - pf.BUZZ_57[0]), S_["5.7"] + pf.BUZZ_57[0], 0.38)
    if n == 6:
        osd.put(buf, tone(1700, 1700, 0.05, 40), S_["6.1"] + PRESS_61, 0.10)                   # the tap on ACCEPT
        osd.put(buf, bm_.buzz_phone(0.45), S_["6.1b"] + 0.0, 0.40)                             # its buzz: his cue
        osd.put(buf, tone(500, 1400, 0.16, 5) * (1 + 0.4 * np.sin(2 * np.pi * 45 * osd.t_(0.16))), S_["6.1b"] + FREEZE_61B, 0.16)
        osd.put(buf, rattle_run(DOWN_62[1] - DOWN_62[0], 0.9), S_["6.2"] + DOWN_62[0], 0.40)   # down, hard
        osd.put(buf, rattle_run(UP_62[1] - UP_62[0], 1.6), S_["6.2"] + UP_62[0], 0.40)         # up, into 1.1's
    rt = osd.room(len(buf) / SR + 0.01)[:len(buf)]; buf[:len(rt)] += rt * 0.012
    from scipy.ndimage import minimum_filter1d
    x = buf / (np.abs(buf).max() + 1e-9) * 0.5
    g, ceil = 1.0, 10 ** (-5.0 / 20)
    for _ in range(8):
        y = x * g
        need = np.minimum(1.0, ceil / (np.abs(y) + 1e-9))
        need = minimum_filter1d(need, size=int(0.004 * SR) * 2 + 1)
        need = np.minimum(need, osd.lp(need, int(0.05 * SR)))
        y = y * need
        sf.write(path, y.astype(np.float32), SR)
        I, P = osd.levels(path)
        if abs(I + 15.0) < 0.3 and P <= -3.0:
            break
        g *= 10 ** ((-15.0 - I) / 20)
    return I, P


if __name__ == "__main__":
    setup()
    if len(sys.argv) > 2 and sys.argv[1] == "film":
        sys.exit(0 if pf.film(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1) else 1)
    print(__doc__)
