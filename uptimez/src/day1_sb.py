"""SILENT STORYBOARD for "How Sofía Survived Day One" (concept v4): 17 shots, 25 s, no audio.
One office set drawn in world coordinates; each shot is a camera (world centre, zoom) on that set, so
characters keep their places between cuts. Bubbles sit beside the speaker's mouth, in screen space.
Render: python3 engine_v.py day1_sb (frames) -- see day1_render.sh."""
import math
import cairo
import kit
import pt42
import anim
import sofia as sf
import day1_kit as dk
from kit import W, H, INK, rect, ellipse, text, sfx, ease, clamp, lerp, cut, rough_rect_pts

DURATION = 25.0
RAW_T = 0.0

# world layout (feet y); Don and the robot have their heads at y 538
CM_X, COUNTER = 87, 777                 # coffee maker, counter top
SOF_A = (260, 900)                      # Sofía at the coffee maker (9:00, 17:00)
SOF_B = (230, 940)                      # Sofía in front of Don's desk, left (9:02)
SOF_C = (470, 950)                      # Sofía steps up to the robot (9:05)
ROB = (530, 840)                        # robot on Don's right, behind the partition until the reveal
DON = (430, 840)
PAM = (730, 840)
DESK_TOP = 710
TRACK = (440, 870, 170, 40)
DON_TUG = anim.key((-8, 0, -20, -140))
DON_WAVE = anim.key((-8, 0, 112, -42))

CARDS = [(0.0, "9:00"), (3.0, "9:02"), (12.2, "9:05"), (20.2, "17:00")]
DINGS = [10.6, 23.2]


def u(t, t0, dur):
    return ease(clamp((t - t0) / dur))


# ------------------------------------------------------------------ state of the set at time t
def state(t):
    s = dict(sof=SOF_A if (t < 3.0 or t >= 20.2) else (SOF_B if t < 12.2 else SOF_C), sof_pose="tuck", sof_face="neutral", sof_look=(0, 0),
             sof_mug=False, don_pose="stand", don_face="smug", don_look=(-0.8, 0.3), don_tilt=0.0,
             rob=ROB, rob_pose="stand", rob_eyes="neutral", rob_look=(0, 0), rob_tilt=0.0, rob_talk=0.0, rob_paper=False,
             pam=PAM, pam_pose="type", pam_face="neutral", pam_look=(-1, 0.4), pam_thermos=False,
             part=0.0, train=None, pressed=False, cm="waiting", pour=0.0, overflow=0.0)
    if t < 3.0:                                           # 9:00 coffee maker
        s.update(sof_pose="press" if (0.3 <= t < 0.6 or 1.2 <= t < 1.5 or 2.0 <= t < 2.3) else "stand",
                 sof_look=(-1, 0), sof_face="eyebrow" if t >= 2.4 else "neutral")
    elif t < 12.2:                                        # 9:02 Don
        s.update(sof_look=(0.9, -0.3))
        if 5.8 <= t < 6.6:
            s["don_pose"] = DON_TUG
        if 6.2 <= t < 7.0:
            s["rob_pose"] = "tug"
        if t >= 6.4:
            s["sof_look"] = (0.6, -0.5)
        if 7.8 <= t < 9.6:
            s.update(don_pose=DON_WAVE, don_tilt=0.08 * u(t, 7.8, 0.2))
        if 7.6 <= t < 9.6:
            s["rob_look"] = (1, 0)                       # the robot watches the lesson
        if 8.6 <= t:
            s["pam_pose"] = "point_l" if t < 9.6 else "type"
            s["pam_look"] = (-1, 0)
        s["part"] = u(t, 9.6, 0.4)
        if t >= 9.9:
            ang = lerp(0.3, 1.75, u(t, 9.9, 0.6))
            s.update(train=ang, pressed=10.6 <= t < 10.9)
        if t >= 11.0:
            s["sof_face"] = "eyebrow"
    elif t < 20.2:                                        # 9:05 Pam
        s.update(part=1.0, train=1.75, sof_look=(0.6, -0.6))
        if t < 14.4:
            s.update(sof_pose="offer", sof_face="smile")
        else:
            s.update(sof_pose="stand")
        if 14.4 <= t < 15.0:
            s["rob_look"] = (-0.8, 0.6)
        elif t >= 15.0:
            s.update(rob_pose="wave" if t < 17.0 else "stand", rob_tilt=0.12 if t < 17.0 else 0, rob_look=(1, 0))
            s["rob_talk"] = 0.8 if 15.4 <= t < 16.0 and int(t * 8) % 2 == 0 else 0.0
        if t >= 16.8:
            s.update(don_face="happy", don_look=(-1, 0))
        if 17.8 <= t < 18.8:
            s.update(pam_look=(0, 0), pam_pose="stand")
        if t >= 18.8:                                    # Pam brings Sofía coffee
            s.update(pam=(585, 948), pam_pose="reach_r" if t < 19.6 else "stand", pam_look=(-1, 0.2), pam_thermos=True,
                     sof_mug=t >= 19.4, sof_pose="mug" if t >= 19.4 else "stand", sof_face="smile" if t >= 19.6 else "neutral",
                     sof_look=(1, 0))
    else:                                                 # 17:00
        s.update(part=1.0, sof_mug=True, sof_pose="mug", sof_look=(0.6, 0))
        rx = lerp(560, 400, u(t, 20.3, 0.6))
        s.update(rob=(rx, 900), rob_pose="hold", rob_paper=True, rob_look=(-1, 0))
        s["rob_talk"] = 0.8 if 20.9 <= t < 21.7 and int(t * 8) % 2 == 0 else 0.0
        if t >= 21.9:
            s.update(sof_pose="wave", sof_face="knowing", sof_look=(0.2, 0), sof_mug=False)
        s.update(train=lerp(0.4, 1.75, u(t, 22.8, 0.35)), pressed=23.2 <= t < 23.5, don_face="happy", don_look=(-1, 0))
        if t >= 23.25:
            s.update(cm="approved", pour=u(t, 23.7, 0.7), overflow=u(t, 24.3, 0.6))
    return s


# ------------------------------------------------------------------ the set
def world(k, st):
    c = k.c
    rect(k, -400, -400, 1600, 1060, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -400, 660, 1600, 900, kit.FLOOR, 101, shadow=False)
    rect(k, -400, 650, 1600, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    pt42.wall_sign(k, 470, 380, 30)
    # Pam's desk area
    px, pf = st["pam"]
    if px == PAM[0]:
        pt42.branded_person(k, "PAM", px, pf, 1.0, pose=st["pam_pose"], face=st["pam_face"], look=st["pam_look"], seed=44)
        kit.desk(k, 640, DESK_TOP, 170, 731)
        rect(k, 646, DESK_TOP + 24, 158, 106, (0.55, 0.40, 0.28), 732)
        dk.thermos(k, 676, DESK_TOP + 2)
    else:
        kit.desk(k, 640, DESK_TOP, 170, 731)
        rect(k, 646, DESK_TOP + 24, 158, 106, (0.55, 0.40, 0.28), 732)
    # track (back half), Don, his desk
    tx, ty, trx, tryy = TRACK
    if st["part"] > 0.5:
        dk.railway(k, tx, ty, trx, tryy, front=False)
    rbx, rbf = st["rob"]
    rob = None
    if rbf == ROB[1]:                                     # beside Don: behind him, so his wave reads on top
        rob = dk.robot(k, rbx, rbf, 1.0, st["rob_pose"], st["rob_eyes"], look=st["rob_look"], tilt=st["rob_tilt"],
                       talk=st["rob_talk"], paper=st["rob_paper"])
    c.save()
    c.translate(DON[0], DON[1]); c.rotate(st["don_tilt"]); c.translate(-DON[0], -DON[1])
    don = pt42.branded_person(k, "DON", DON[0], DON[1], 1.0, pose=st["don_pose"], face=st["don_face"],
                              look=st["don_look"], seed=500)
    c.restore()
    kit.desk(k, 320, DESK_TOP, 200, 501)
    rect(k, 326, DESK_TOP + 24, 188, 116, (0.55, 0.40, 0.28), 502)
    if rbf != ROB[1]:                                     # 17:00: rolled forward, in front of the desk
        rob = dk.robot(k, rbx, rbf, 1.0, st["rob_pose"], st["rob_eyes"], look=st["rob_look"], tilt=st["rob_tilt"],
                       talk=st["rob_talk"], paper=st["rob_paper"])
    # railway front + train
    btn = None
    if st["part"] > 0.5:
        dk.railway(k, tx, ty, trx, tryy, front=True)
        if st["train"] is not None:
            btn = dk.train(k, tx, ty, trx, tryy, st["train"], button_y=DESK_TOP - 16, pressed=st["pressed"])
    # partition slides out to the right
    if st["part"] < 1:
        off = 520 * st["part"]
        dk.partition(k, 315 + off, 640 + off, 640, 860)
    # coffee counter (front left)
    dk.counter(k, -60, 200, COUNTER)
    dk.coffee_maker(k, CM_X, COUNTER, 1.0, st["cm"], pour=st["pour"], overflow=st["overflow"])
    # Pam at Sofía's side (9:05 thermos)
    if px != PAM[0]:
        pam = pt42.branded_person(k, "PAM", px, pf, 1.0, pose=st["pam_pose"], face=st["pam_face"], look=st["pam_look"], seed=44)
        hx, hy = pam["hands"][1]
        dk.thermos(k, hx + 6, hy + 30)
    # Sofía (front)
    sx, sfeet = st["sof"]
    sof = sf.sofia(k, sx, sfeet, 1.0, st["sof_pose"], st["sof_face"], look=st["sof_look"], seed=7,
                   folder="tuck" if not st["sof_mug"] and st["sof_pose"] in ("stand", "tuck") and sx != SOF_A[0] else None)
    if st["sof_mug"]:
        hx, hy = sof["hands"][1]
        dk.mug(k, hx + 4, hy + 8, 1.0, steam=1.0)
    return {"don": don, "rob": rob, "sof": sof, "btn": btn}


# ------------------------------------------------------------------ screen-space bits
def to_screen(p, cam):
    cx, cy, z = cam
    return 270 + (p[0] - cx) * z, 480 + (p[1] - cy) * z


def bubble(k, s, mouth, side, size=30, t=0.0, t0=0.0):
    """Box beside the mouth (side = 'left' | 'right'), short side tail ending at the mouth."""
    c = k.c
    c.select_font_face(kit.FONT); c.set_font_size(size)
    e = c.text_extents(s)
    bw, bh = e.x_advance + 44, size + 34
    mx, my = mouth
    gap = 34
    bx = mx + gap if side == "right" else mx - gap - bw
    bx = clamp(bx, 20, W * 0.88 - bw)
    by = clamp(my - bh / 2, H * 0.11, H * 0.84 - bh)
    pop = 0.85 + 0.15 * ease(clamp((t - t0) / 0.12))
    c.save(); c.translate(bx + bw / 2, by + bh / 2); c.scale(pop, pop); c.translate(-(bx + bw / 2), -(by + bh / 2))
    ex = bx + 3 if side == "right" else bx + bw - 3
    ty = clamp(my, by + 18, by + bh - 18)
    tail = [(ex, ty - 12), (mx + (8 if side == "right" else -8), my), (ex, ty + 12)]
    cut(k, tail, (1, 1, 1))
    cut(k, rough_rect_pts(k, bx, by, bw, bh, 900 + len(s), j=1.6), (1, 1, 1))
    kit._poly(c, tail); c.set_source_rgb(1, 1, 1); c.fill()
    c.set_source_rgb(*INK); c.move_to(bx + 22, by + bh / 2 + size * 0.36); c.show_text(s)
    c.restore()


def clock_card(k, t):
    for t0, lbl in CARDS:
        if t0 <= t < t0 + 0.7:
            c = k.c
            sc = max(0.02, anim.back_out(clamp((t - t0) / 0.18), 2.0))
            c.save(); c.translate(270, 752); c.rotate(-0.05); c.scale(sc, sc)   # lower third: clear of faces
            c.select_font_face(kit.FONT); c.set_font_size(76)
            e = c.text_extents(lbl)
            rect(k, -e.x_advance / 2 - 24, -54, e.x_advance + 48, 92, (1, 1, 1), 1400, lw=3)
            c.move_to(-e.x_advance / 2, 27); c.set_source_rgb(*INK); c.show_text(lbl)
            c.restore()


def ding(k, t, x, y):
    for t0 in DINGS:
        if t0 <= t < t0 + 0.6:
            if t - t0 < 1 / 12:
                k.c.set_source_rgba(1, 1, 1, 0.6); k.c.paint()
            sc = max(0.02, anim.back_out(clamp((t - t0) / 0.15), 2.2))
            c = k.c
            c.save(); c.translate(x, y); c.scale(sc, sc); sfx(k, "DING!", 0, 0, 64, rot=-0.1); c.restore()


# ------------------------------------------------------------------ shots
DON_HEAD = (DON[0], DON[1] - 302)
ROB_HEAD = (ROB[0], ROB[1] - 302)


def head(p, feet, h=1.02):
    return p, feet - (300 * h - 78 + 44)


SHOTS = [  # (t0, t1, camera (world cx, cy, zoom) or function of t, bubbles [(t0, t1, text, who, side)])
    (0.0, 1.0, (190, 720, 1.9), []),
    (1.0, 1.8, (CM_X, 662, 4.4), []),
    (1.8, 3.0, (225, 690, 2.3), []),
    (3.0, 5.6, (322, 625, 1.7), [(3.3, 5.5, "I approve everything.", "don", "left")]),
    (5.6, 7.6, (475, 595, 1.8), [(5.7, 7.4, "Trained it myself.", "don", "right")]),
    (7.6, 9.0, (470, 590, 2.0), [(8.0, 9.0, "Pam?", "don", "left")]),
    (9.0, 9.6, (730, 620, 2.3), []),
    (9.6, 11.6, (420, 690, 0.78), []),
    (11.6, 12.2, (230, 690, 3.4), []),
    (12.2, 14.4, (500, 650, 2.0), [(12.5, 14.3, "Can you help me?", "sof", "right")]),
    (14.4, 16.8, (570, 590, 2.0), [(15.4, 16.8, "Pam?", "rob", "left")]),
    (16.8, 17.8, (420, 545, 2.8), [(16.9, 17.8, "Perfect.", "don", "left")]),
    (17.8, 18.8, (730, 600, 2.9), []),
    (18.8, 20.2, (525, 690, 2.0), []),
    (20.2, 22.8, lambda t: (330, 760, 1.8) if t < 21.9 else (340, 680, 2.0),
     [(20.9, 21.8, "Can you help me?", "rob", "right"), (22.0, 22.8, "Pam?", "sof", "left")]),
    (22.8, 23.6, (505, 690, 3.6), []),
    (23.6, 25.0, (CM_X, 690, 3.0), []),
]


def make_shot(t0, t1, cam, bubbles):
    def fn(k, t, tl):
        st = state(t)
        cm = cam(t) if callable(cam) else cam
        c = k.c
        c.save()
        c.translate(270, 480); c.scale(cm[2], cm[2]); c.translate(-cm[0], -cm[1])
        out = world(k, st)
        c.restore()
        for b0, b1, s, who, side in bubbles:
            if b0 <= t < b1:
                if who == "don":
                    m = (DON[0], DON[1] - 302 + 32)
                elif who == "rob":
                    rx, rf = st["rob"]
                    m = (rx + (54 if side == "right" else -54), rf - 302 + 18)
                else:
                    sx, sfeet = st["sof"]
                    m = (sx, sfeet - 272 + 33)
                sm = to_screen(m, cm)
                if who != "rob":                         # tail starts just outside the cheek
                    sm = (sm[0] + (58 if side == "right" else -58) * cm[2], sm[1])
                bubble(k, s, sm, side, t=t, t0=b0)
        if out["btn"] is not None:
            bx_, by_ = to_screen(out["btn"], cm)
            ding(k, t, min(bx_ + 70, 430), by_ + 60)           # beside the button, clear of Don's face
        elif t >= 23.2:
            ding(k, t, 300, 330)
        clock_card(k, t)
    fn.__name__ = f"shot_{t0:04.1f}"
    return fn


PANELS = [(t0, t1, make_shot(t0, t1, cam, b)) for t0, t1, cam, b in SHOTS]


def shake(t):
    return 0
