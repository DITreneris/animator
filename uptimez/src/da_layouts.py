"""THE DOUBLE AGENT (episode 15): the layouts, v1 (stage 4.3; the-double-agent-layouts-plan-v1.md).

Every shot's key frame at 540x960 (shown at 270), drawn from the scene file's records (da_scenes.STAGE / TEXT: nothing
about a shot is typed here twice) with the drawings that already exist: the front desk room with the office glass
(da_set.room), the cast's rigs, S8's layers (da_s8), S8r's frame 0 (the file), the props (da_props). One map,
shot -> draw function, printed and asserted (lesson 109). Key poses only: the motion is stage 6.

  python3 da_layouts.py [act ...] [out_dir]  ->  da_layout_act<N>_v1.png (+ _feed: the sheet at half size)

The checks on every frame (the build exits 1 on a failure not in KNOWN): faces of the story cast out of the apps'
zones (uz_check.check_scale, measured where the rigs drew them), signs whole or out (uz_check.check_signs), the
mirror rule on the drawn frame (Don's head against the tape's x).
"""
import math
import os
import sys
import textwrap

import cairo

import kit
from kit import Ctx, INK
import cs_frame as cf
import fs_storyboard_v17 as sbv
import fs_set4 as s4
import ps_set as pss
import da_set as ds
import da_scenes as sc
import da_sheets as dsh
import da_props as dpr
import don_ps as dp
import pm_ps as pm
import robot_ps as rp
import dh_cast as dc
import sofia_da as sd
sd.LOOK_V5[0] = True   # Tomas 28 Nov: Sofía v5 locked (da_sofia_v5.png); da_s8's locked layers keep v4
import uz_check as uz

ds.EP15_SET[0] = True                                          # Tomas 27 Nov: the throne's back bare, no taped plan, no
ds.NAME_BADGES[0] = False                                      # shredder; only the robot's HR badge; Don's office chair low
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, "..", "the-double-agent")
W, H = 540, 960
F = pss.F
SC = dict(don=0.60, pam=0.54, mom=0.54, sofia=0.47, father=dsh.F_S, client=0.52, robot=0.48)
R = dict(don=50, pam=48, mom=50, sofia=46, father=48, client=50, robot=50)      # head radius, body units
R_TARGET = dict(W=30, M=50, MC=78, C=110)                                       # the biggest story face, px, by size
TX, TY, TS = pss.THRONE
CLIP_S = 0.55          # the audit 27 Nov: 0.9 drew a clip 3.5x a real one next to Don ("confetti"); 40 % smaller

# The marks (plan §2): world units, (x, feet). Measured from da_establish_v3 and ps_scenes.P.
MARKS = dict(
    don_tug=(360, F + 26), robot_tug=(560, F + 18),           # either side of the throne at the line (the loop's tug)
    don_hop=(372, F + 30),                                    # 1.2-1.5: on one leg beside the throne
    father_cross=(600, F + 250), sofia_cross=(600, F + 60),   # 1.3: crossing near the camera (his top out of frame);
                                                              # 1.4: Sofía crossing toward the office door
    robot_pile=(600, F + 40),                                 # 1.4-7.4: the clips between the throne and Mom's desk
    don_line=(500, F + 150), don_counter=(500, F + 90),       # his side, at the tape / facing the counter's end
    pam_counter=(650, F + 34),                                # in front of the counter's left end
    don_gift=(548, F + 80),                                   # 2.4: at the tape's edge, his side, close to her
    don_s7=(588, F + 330),                                    # S7: forward, toes at the tape's edge (establish v3's place)
    mom_wall=(612, F + 40), don_wall=(500, F + 70), don_peek=(548, F + 16),           # 3.4, 5.4: Mom planted at the counter's end, Don facing her
    mom_desk_s=(760, F - 70),                                 # Mom at her desk, behind the counter (drawn in floor_world's
                                                              # back pass: the counter hides her feet); 760, not the set's
                                                              # 824 (the audit: Pam at the door covered her)
    pam_door=(846, F + 30), client_door=(926, F + 4),         # 27 Nov (Tomas: "kabo ore"): v2 had both feet above the
                                                              # floor line (F-20, F-30): on the wall. Now on the floor:
                                                              # the Client in the door's gap (x 896-952) at its threshold,
                                                              # Pam in front of the counter's end, a step nearer
    pam_cross=(626, F + 64), don_take=(508, F + 84),          # 4.1: across the tape
    don_street=(150, F + 60), pam_back=(318, F + 34),         # 4.2: Don at the street door, Pam crossing behind
    don_stop=(552, F + 60), don_slip=(530, F + 290),                                   # 5.3: the dead stop at his line
    mom_desk=(824, F - 70),
)


def shadow(k, x, f, w):
    """the series' floor shadow and a tighter, darker contact under the feet (the audit: shadows too weak to read)."""
    s4.shadow(k, x, f, w)
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.14); c.save(); c.translate(x, f + 1); c.scale(w * 0.75, 4); c.new_path()
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()


def tilted(k, x, f, ang, draw):
    """a whole body pitched about its feet (a feint, the inertia of a dead stop): the key pose's lean."""
    c = k.c
    c.save(); c.translate(x, f); c.rotate(ang); c.translate(-x, -f)
    try:
        return draw()
    finally:
        c.restore()


def tape_x(feet):
    return pss.LINE_X + 34 * (feet - F) / 160.0


def _head(o, who):
    if who == "robot":
        x, y = o["screen"][:2]
    else:
        x, y = o["head"][:2]
    return (x, y, R[who] * SC[who])


# ---- the cast, at marks -----------------------------------------------------------------------------------------------
DON_FEET = [None]


def don(k, mark, pose="stand", face="neutral", look=(0, 0), **kw):
    x, f = MARKS[mark] if isinstance(mark, str) else mark
    DON_FEET[0] = (x, f)
    shadow(k, x, f + 2, 40)
    return _head(dp.don(k, x, f, SC["don"], pose, face, look, **kw), "don")


def robot(k, mark, **kw):
    x, f = MARKS[mark] if isinstance(mark, str) else mark
    shadow(k, x, f + 2, 36)
    return _head(rp.robot(k, x, f, SC["robot"], **kw), "robot")


def father(k, mark, **kw):
    x, f = MARKS[mark] if isinstance(mark, str) else mark
    shadow(k, x, f + 2, 36)
    return _head(dc.father(k, x, f, SC["father"], **kw), "father")


def sofia(k, mark, **kw):
    x, f = MARKS[mark] if isinstance(mark, str) else mark
    shadow(k, x, f + 2, 32)
    return _head(sd.sofia(k, x, f, SC["sofia"], **kw), "sofia")


MOM_LIB = [True]   # Tomas 28 Nov (/grill-me): Mom's fists on her hips and her folded arms in the hand library;
MOM_ORDER_S = 0.7  # and a smaller rosette (mom_fs.ORDER_S, 1.15 as before)


def mom(k, mark, pose="fists", face="unimpressed", look=(0, 0), **kw):
    import mom_fs as mfs
    x, f = MARKS[mark] if isinstance(mark, str) else mark
    shadow(k, x, f + 2, 34)
    keep_o = mfs.ORDER_S[0]; mfs.ORDER_S[0] = MOM_ORDER_S if MOM_LIB[0] else keep_o
    keep_c = mfs.CURLER_D[0]; mfs.CURLER_D[0] = (8, 9) if MOM_LIB[0] else keep_c    # (review 28 Nov: it "floated")
    try:
        if MOM_LIB[0] and pose in ("fists", "folded"):
            s_ = SC["mom"]
            if pose == "fists":                                # the fists on her hips, the knuckles in
                jobs = {a: dict(T=(x + a * 60 * s_, f + (mfs.WAIST - 6) * s_), pose="FIST", out=a) for a in (-1, 1)}
            else:                                              # folded: each hand on the other arm, the forearms crossed
                jobs = {-1: dict(T=(x + 30 * s_, f + (mfs.BT + 46) * s_), pose="CLUTCH", out=-1),
                        1: dict(T=(x - 30 * s_, f + (mfs.BT + 56) * s_), pose="CLUTCH", out=1)}
            kw.setdefault("bag", False)                              # (a pose given as angles: no handbag)
            import mom_bc as mbc
            keep_n = mbc.TUPLE_NAME[0]; mbc.TUPLE_NAME[0] = "angles"   # (angles alone: no tissue, no scrub marks)
            try:
                o = rig_hands(k, lambda kk, a4: mfs.mom(kk, x, f, s_, a4, face, look, **kw), s_, jobs, sex="f", skin=mfs.SKIN)
            finally:
                mbc.TUPLE_NAME[0] = keep_n
            return _head(o, "mom")
    finally:
        mfs.ORDER_S[0] = keep_o; mfs.CURLER_D[0] = keep_c
    if pose == "folded":                                       # pm_ps's folded arms (its M_POSES), the series' Mom
        return _head(pm.mom(k, x, f, SC["mom"], pose, face, look, **kw), "mom")
    return _head(mfs.mom(k, x, f, SC["mom"], pose, face, look, **kw), "mom")


def pam(k, mark, pose="stand", face="neutral", look=(0, 0), **kw):
    x, f = MARKS[mark] if isinstance(mark, str) else mark
    shadow(k, x, f + 2, 32)
    return _head(pm.pam(k, x, f, SC["pam"], pose, face, look, **kw), "pam")


# ---- a rig with the hand library's hands (rules-hands §0; the hand sheet's jobs, hand_lib_v4) ---------------------------
MALE, FEMALE = (0.96, 0.78, 0.66), (0.99, 0.86, 0.66)


ELBOW_RULE = [False]   # opt-in (the anim scenes turn it on): a job's elbow hangs under the shoulder-wrist line


def rig_hands(k, draw, scale, jobs, sex="m", skin=MALE):
    """draw(k, angles4) draws a rig with its arms at the given kit angles and returns its record. jobs: {-1: job, +1:
    job} for the screen-left / screen-right arm, job = dict(T=wrist (world), pose=library pose, out=elbow side +-1,
    obj=fn(k, P, w) drawn at the pose's contact, contact=name, behind=True: the object first; reach=True: a wrist past
    the arm's reach is moved to where it reaches, opt-in: Act I as approved). Arms with no job hang
    (RELAXED). The arms are solved for the shoulders the rig really draws (da_s8r._arm_log / _ik, as da_s52); the rig's
    own hands are not drawn at those wrists (of_cast.held); the library hand goes there with hands_lr's side."""
    import da_s8r as r8
    import of_cast as oc
    import hands_ps as hp
    import hand_lib_v4 as hl
    on = GROUND["on"][0]; GROUND["on"][0] = False             # the measuring pass draws nothing into the shot
    try:
        lg = r8._arm_log(lambda k_: draw(k_, (0, 0, 0, 0)))
    finally:
        GROUND["on"][0] = on
    (SL, l1, _), (SR, r1, _) = lg[0], lg[1]
    ang, T = {}, {}
    for arm, (S_, l_) in ((-1, (SL, l1)), (1, (SR, r1))):
        j = jobs.get(arm)
        if j is None:
            T[arm] = (S_[0] + arm * 0.25 * l_, S_[1] + 1.9 * l_)
            ang[arm] = r8._ik(S_, T[arm], l_, l_, arm)
        else:
            T[arm] = j["T"]
            d_ = math.hypot(T[arm][0] - S_[0], T[arm][1] - S_[1])
            if ELBOW_RULE[0] and not j.get("near") and not __import__("da_hand_gate").ARMS_OK[0] and 0 < d_ < 1.2 * l_:
                # (Tomas's deep audit 28 Nov: the minimum distance) a hand nearer the shoulder than 60 % of the arm
                # folds the elbow under ~74 degrees: it goes out along the same line, and what it holds goes with it
                T[arm] = (S_[0] + (T[arm][0] - S_[0]) * 1.2 * l_ / d_, S_[1] + (T[arm][1] - S_[1]) * 1.2 * l_ / d_)
                d_ = 1.2 * l_
            if j.get("reach") and d_ > 1.96 * l_:                                  # the audit 27 Nov (5.3): a wrist past the arm's reach drew
                u_ = 1.96 * l_ / d_                             # the hand apart from the arm; the hand goes where it reaches
                T[arm] = (S_[0] + (T[arm][0] - S_[0]) * u_, S_[1] + (T[arm][1] - S_[1]) * u_)
            ang[arm] = r8._ik(S_, T[arm], l_, l_, j.get("out", arm))
            rule = (ELBOW_RULE[0] and j.get("elbow") is None and T[arm][1] > S_[1] - 0.5 * l_   # (a hand well above
                    and not __import__("da_hand_gate").ARMS_OK[0])   # (a written exception draws as before the rule)
            if j.get("elbow") == "down" or rule:                # the shoulder keeps the side by x: a wave, the hair)
                # opt-in (28 Nov, 4.1 review; ELBOW_RULE: Tomas's deep audit, every job in the episode's scenes)
                two = [r8._ik(S_, T[arm], l_, l_, o_) for o_ in (1, -1)]   # shoulder-wrist; on a level reach the side by
                ang[arm] = max(two, key=lambda a_: math.cos(math.radians(a_[0])))   # x picks one at random (a raised V)
            if math.hypot(T[arm][0] - S_[0], T[arm][1] - S_[1]) <= 2.0 * l_:
                touch(*T[arm])                                  # a hand counts only where the arm gets it (the audit
            elif GROUND["on"][0]:                               # 27 Nov, 3.2: a hand drawn apart, at the jug)
                GROUND["short"].append((T[arm], S_, l_))
    old = kit.HAND[0]; kit.HAND[0] = hp.hand; hp.reset("quiet", "quiet")
    try:
        o = oc.held(k, lambda: draw(k, ang[-1] + ang[1]), lambda o_: [T[-1], T[1]])
    finally:
        kit.HAND[0] = old
    w = (17 if sex == "m" else 15) * 1.15 * 1.25 * scale
    hl.LWS[0] = scale
    try:
        for arm in (-1, 1):
            j = jobs.get(arm) or dict(pose="RELAXED")
            a1, a2 = ang[arm]
            d = (math.sin(math.radians(a1 + a2)), math.cos(math.radians(a1 + a2)))
            pose = j["pose"]
            obj = None
            if j.get("obj"):
                side = __import__("hands_lr").side(arm, d)
                if pose == "SAUCER_SUPPORT":                    # (28 Nov, scene 4) as hl.draw_lr draws it: level, the
                    side = arm                                  # thumb up, whatever the forearm; a forearm rising put the
                                                                # contact on the other side of the wrist from the palm
                P = hl.to_screen(pose, T[arm][0], T[arm][1], math.atan2(d[1], d[0]), w, side, hl.contact(pose, j["contact"]))
                if j.get("obj_info"):                          # opt-in (28 Nov, da_cups): the prop's drawer also gets the
                    info = dict(side=side, d=d, wrist=T[arm], arm=arm)   # hand's side and the forearm's direction
                    obj = (lambda P_, i_: (lambda k_: j["obj"](k_, P_, w, i_)))(P, info)
                else:
                    obj = (lambda P_: (lambda k_: j["obj"](k_, P_, w)))(P)
                if math.hypot(T[arm][0] - lg[0 if arm < 0 else 1][0][0], T[arm][1] - lg[0 if arm < 0 else 1][0][1]) <= 2.0 * lg[0 if arm < 0 else 1][1]:
                    touch(*P)
            if obj and j.get("behind"):
                front = None
                if j.get("front"):                              # opt-in (28 Nov, da_cups): a pass over the hand too
                    front = (lambda P_, i_: (lambda k_: j["front"](k_, P_, w, i_)))(P, dict(side=side, d=d, wrist=T[arm], arm=arm, skin=skin))
                hl.draw_lr(k, pose, T[arm][0], T[arm][1], d, w, skin, arm, back_obj=obj, obj=front)
            else:
                hl.draw_lr(k, pose, T[arm][0], T[arm][1], d, w, skin, arm, obj=obj)
    finally:
        hl.LWS[0] = 1.0
    if isinstance(o, dict):
        o["wrists"] = dict(T)                                   # where the hands really went (after the reach clamp)
    return o


# ---- Don's raised leg (the Father audit 27 Nov: "the thigh a balloon, the knee and shin unclear, the shoe apart") ------
def don_shoes(k, x, feet, s):
    """opt-in (rough cut test 28 Nov, 3.4/5.4: his standing trousers end in nothing, "a box"): two shoes under the hems,
    toes out, in don_legs_ep's shoe colour. Call it after the rig, in the rig's own transform."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    for sg in (-1, 1):
        c.new_path(); c.move_to(sg * 6, -11); c.line_to(sg * 44, -11); c.curve_to(sg * 58, -9, sg * 62, -1, sg * 58, 3)
        c.line_to(sg * 6, 3); c.close_path()
        c.set_source_rgb(0.24, 0.18, 0.13); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.restore()


def don_legs_ep(k, x, feet, s, u):
    """don_ps._legs for this episode (don_ps unchanged; swapped in while the layouts draw): the screen-left leg
    planted; the screen-right one a clear chain hip -> thigh -> knee -> shin -> shoe: a thigh narrower than it is long,
    out and up to a knee that bends (a joint, its fold), the shin hanging back down from it, the shoe joined under the
    hem, its sole lifted; a contact shadow under each foot."""
    import don_v4 as dv
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    w = dp.WAIST_Y
    for sx_, sw in ((-24, 30), (60 + 30 * u, 26 - 8 * u)):    # the contact shadows first
        c.set_source_rgba(0, 0, 0, 0.22); c.save(); c.translate(sx_, 3); c.scale(sw, 5)
        c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    kit.cut(k, [(-45, w), (2, w), (-2, -10), (-47, -10)], dv.KHAKI, shadow=False, lw=2)          # the planted leg
    c.set_source_rgb(*INK); c.set_line_width(1.5); c.set_line_cap(1)                            # its knee
    c.new_path(); c.move_to(-34, w + 50); c.curve_to(-26, w + 54, -20, w + 54, -12, w + 50); c.stroke(); c.set_line_cap(0)
    c.new_path(); c.move_to(-50, -12); c.line_to(-6, -12); c.curve_to(6, -10, 8, -2, 6, 2); c.line_to(-56, 2)
    c.close_path(); c.set_source_rgb(0.24, 0.18, 0.13); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2)
    c.stroke()                                                                                  # the shoe, its toe out
    H_ = (22, w + 14)                                                                           # the hip
    K_ = (22 + 44 * u, w + 52 - 18 * u)                                                         # the knee, out and up
    A_ = (K_[0] + 6 * u, -14 - 30 * u)                                                          # the ankle, under it
    dp._cap(c, [H_, K_], 34, dv.KHAKI)                                                          # the thigh
    dp._cap(c, [K_, A_], 30, dv.KHAKI)                                                          # the shin
    c.set_source_rgb(*dv.KHAKI); c.new_path(); c.arc(K_[0], K_[1], 15, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_cap(1)                            # the knee's bend
    c.new_path(); c.arc(K_[0] + 2, K_[1] + 2, 12, -0.4, 1.2); c.stroke()
    c.new_path(); c.move_to(K_[0] - 10, K_[1] + 12); c.line_to(K_[0] - 4, K_[1] + 20); c.stroke(); c.set_line_cap(0)
    ax, ay = A_
    c.new_path()                                                                                # the shoe under the hem
    c.move_to(ax - 16, ay - 4); c.line_to(ax + 12, ay - 6); c.curve_to(ax + 34, ay - 4, ax + 44, ay + 4, ax + 42, ay + 12)
    c.line_to(ax - 18, ay + 12); c.close_path()
    c.set_source_rgb(0.24, 0.18, 0.13); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    dp._cap(c, [(ax - 16, ay - 8), (ax + 14, ay - 10)], 10, dv.KHAKI)                           # the hem over it
    if u < 0.2:                                                                                 # standing: its knee
        c.set_source_rgb(*INK); c.set_line_width(1.5); c.set_line_cap(1)
        c.new_path(); c.move_to(K_[0] - 10, K_[1] + 2); c.curve_to(K_[0] - 4, K_[1] + 6, K_[0] + 4, K_[1] + 6, K_[0] + 10, K_[1] + 2)
        c.stroke(); c.set_line_cap(0)
    c.restore()


class don_legs(object):
    def __enter__(self):
        self.old = dp._legs; dp._legs = don_legs_ep; return self

    def __exit__(self, *e):
        dp._legs = self.old


def sole_of(x, f, s, u=1.0):
    """the raised shoe's sole under don_legs_ep, in world units."""
    kx = 22 + 44 * u
    return (x + (kx + 6 * u + 12) * s, f + (-14 - 30 * u + 12) * s)


# ---- Sofía's two hands on a board: the library's CLUTCH (the canon's board_two stays as it is) --------------------------
def lib_board_two(k, x, y, bw, bh, ang, w, skin, skin2, draw_board):
    """hands_v4.board_two's signature (sofia_da.with_board calls it in her units): the board, then the library's CLUTCH
    at each upper corner, the wrist where her arm ends (her IK target), the knuckles over the top edge."""
    import hand_lib_v4 as hl
    draw_board(k)
    for arm in (-1, 1):
        cx, cy = arm * (bw / 2 - 0.42 * w), -bh / 2
        d = (-arm * 0.30, 1.0); n = math.hypot(*d); d = (d[0] / n, d[1] / n)
        hl.draw_lr(k, "CLUTCH", cx, cy - 0.30 * w, d, w * 0.95, skin, arm)


class sofia_lib_hands(object):
    def __enter__(self):
        import hands_v4 as hv
        self.hv = hv; self.old = hv.board_two; hv.board_two = lib_board_two; return self

    def __exit__(self, *e):
        self.hv.board_two = self.old


# ---- the state of the floor (what the film has changed so far) ---------------------------------------------------------
NO_CONFETTI = [True]   # Tomas 28 Nov: the floor shots without episode 9's blue strips (5.2 "as built" and S8r untouched)
TAG_V2 = [True]   # Tomas 28 Nov (/grill-me, da_tag_options_v2.png, "A"): the tag is a swing ticket like the price;
                  # False draws v1 (a stick over the crown's ball, the card stuck on), as the approved layouts had it


TAG_CORDS = {"A": ((0.93, 0.76, 0.28), (0.55, 0.40, 0.10)), "B": ((0.80, 0.12, 0.16), (0.55, 0.06, 0.08))}

def review_tag(k, x, y, s, style="A", ang=0.0):
    """REVIEW · TOMORROW as a swing ticket, hung like the price (dh_props._price_tag v2): a loop of cord round the crown
    point, two strands to a knot, a card with cut corners, an eyelet, a rule; style A gold cord, B red cord, C one thread."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    if style in ("A", "B"):
        CORD, CORD_D = TAG_CORDS[style]
        c.set_line_cap(1)
        for col, lw in ((INK, 6.5), (CORD, 3.5)):                 # the loop round the ball
            c.set_source_rgb(*col); c.set_line_width(lw)
            c.save(); c.translate(0, 20); c.scale(1, 0.45); c.arc(0, 0, 9, 0, 2 * math.pi); c.restore(); c.stroke()
        c.rotate(ang); ln = 26
        for col, lw in ((INK, 5.5), (CORD, 3.0)):
            c.set_source_rgb(*col); c.set_line_width(lw)
            for sx in (-1, 1):
                c.move_to(0, 24); c.curve_to(sx * 9, 24 + ln * 0.35, sx * 7, 24 + ln * 0.8, 0, 24 + ln + 9); c.stroke()
        kit.ellipse(k, 0, 24, 5, 4.5, CORD, 4601, shadow=False, lw=1.8)
        c.translate(0, 24 + ln)
    else:
        CORD, CORD_D = (0.25, 0.22, 0.20), (0.55, 0.40, 0.10)
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
        c.save(); c.translate(0, 20); c.scale(1, 0.45); c.new_path(); c.arc(0, 0, 8, 0, 2 * math.pi); c.restore(); c.stroke()
        c.rotate(ang + 0.12); ln = 30
        c.move_to(0, 24); c.line_to(0, 24 + ln + 8); c.stroke()
        c.translate(0, 24 + ln)
    W, H = 104, 58
    kit.cut(k, [(-W / 2, 8), (-W / 2 + 10, 0), (W / 2 - 10, 0), (W / 2, 8), (W / 2, H), (-W / 2, H)], (0.99, 0.97, 0.90), lw=2.6)
    c.set_source_rgb(*CORD_D); c.set_line_width(1.6)
    c.move_to(-W / 2 + 6, 15); c.line_to(W / 2 - 6, 15); c.line_to(W / 2 - 6, H - 6); c.line_to(-W / 2 + 6, H - 6); c.close_path(); c.stroke()
    kit.ellipse(k, 0, 8, 5.5, 5.5, CORD if style != "C" else (0.75, 0.62, 0.30), 4602, shadow=False, lw=1.8)
    kit.ellipse(k, 0, 8, 2.2, 2.2, (0.20, 0.16, 0.10), 4603, shadow=False, outline=False)
    c.select_font_face(kit.FONT); c.set_font_size(14); c.set_source_rgb(0.72, 0.08, 0.12)
    for txt, yy in (("REVIEW", 32), ("TOMORROW", 48)):
        e = c.text_extents(txt); c.move_to(-e.x_advance / 2, yy); c.show_text(txt)
    c.restore()


def tag_on_back(k):
    """REVIEW · TOMORROW on the throne's back, from 1.3b on (seen from the street side: its back), hung from the crown's
    left point, clear of the robot's card (episode 14's) and of the price tag's blank back on the right. v2 (TAG_V2):
    the price's swing ticket, a gold cord looped round the point."""
    if TAG_V2[0]:
        return review_tag(k, TX - 56 * TS, F - 432 * TS - 8, 0.55 * TS / 0.6 * 0.95, "A")
    dsh._tag(k, TX - 56 * TS, F - 432 * TS, 0.55 * TS / 0.6)


CLIPS_V3 = [True]   # Tomas 28 Nov ("darom", cold test s1 v1: "grey specks" to both viewers): each clip drawn twice,
                    # an ink outline under a bright silver wire, and CLIP_S 0.55 -> 0.70 (the 27 Nov audit's 0.9 read
                    # as confetti, 3.5x a real clip next to Don; 0.70 stays under it)
CLIP_SILVER = (0.88, 0.90, 0.94)
_paperclip0 = sd.paperclip


def _paperclip3(k, x, y, s=1.0, ang=0.0, col=None, lw=1.3):
    if not CLIPS_V3[0]:
        return _paperclip0(k, x, y, s, ang, **({} if col is None else {"col": col}), lw=lw)
    s = s * 0.70 / 0.55
    _paperclip0(k, x, y, s, ang, col=kit.INK, lw=lw * 2.4)
    _paperclip0(k, x, y, s, ang, col=CLIP_SILVER if col is None else col, lw=lw * 1.1)


sd.paperclip = _paperclip3


def clips_on_floor(k, n, seed=4710):
    """the robot's pile: n clips round the throne's casters and toward Mom's desk, always the same n first places (the
    pile shrinks from its far end: positions never jump between shots), and the one clip under the throne's caster
    from 1.4 on (da_scenes.PROPS: the last one, 7.4)."""
    import random
    r = random.Random(seed)
    spots = [(r.uniform(TX + 20, 700), F + r.uniform(4, 60), r.uniform(-3.1, 3.1)) for _ in range(30)]
    old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
    try:
        for x, y, a in spots[:max(0, n - 1)]:
            sd.paperclip(k, x, y, CLIP_S, a)
        if n:
            sd.paperclip(k, TX + 24 * TS, F + 6, CLIP_S, 0.3)     # under the caster: the last clip
    finally:
        sd.CLIPS_V2[0] = old


ROLL_V2 = [True]   # Tomas 28 Nov ("darom", cold test s1 v1: both viewers took the roll for the throne's caster wheel):
                   # the roll reads as tape: wound layers, a cardboard core; False draws v1
CORE = (0.80, 0.64, 0.44)


def roll_at(k, x, floor, up=0.0, rot=0.0):
    """Don's tape roll (episode 14's): on its edge at (x, floor); up > 0 lifts it on his sole. v2: the wound layers
    (two darker rings), a fat cardboard core, the hole."""
    c = k.c
    cy = floor - 18 - up
    if not ROLL_V2[0]:
        kit.ellipse(k, x, cy, 18, 18, pss.TAPE, 4720, shadow=False, lw=2)
        kit.ellipse(k, x, cy, 8, 8, kit.WALL, 4721, shadow=False, lw=1.6)
        return
    kit.ellipse(k, x, cy, 19, 19, pss.TAPE, 4720, shadow=False, lw=2.2)
    c.set_source_rgb(0.78, 0.58, 0.06); c.set_line_width(1.0)
    for r_ in (16.0, 13.5):
        c.new_path(); c.arc(x, cy, r_, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(2.0); c.set_line_cap(1)
    c.new_path(); c.arc(x, cy, 17.2, -2.6, -1.7); c.stroke(); c.set_line_cap(0)     # the shine stays: the light's
    kit.ellipse(k, x, cy, 11, 11, CORE, 4722, shadow=False, lw=1.6)
    kit.ellipse(k, x, cy, 6.5, 6.5, kit.WALL, 4721, shadow=False, lw=1.4)
    if rot:                                                    # rolling (28 Nov audit): the core's seam and the tape's
        c.set_source_rgb(*kit.INK); c.set_line_width(1.6); c.set_line_cap(1)   # end turn with it
        c.new_path(); c.move_to(x + 6.5 * math.cos(rot), cy + 6.5 * math.sin(rot))
        c.line_to(x + 11 * math.cos(rot), cy + 11 * math.sin(rot)); c.stroke()
        a2 = rot + 2.2
        c.new_path(); c.move_to(x + 14 * math.cos(a2), cy + 14 * math.sin(a2))
        c.line_to(x + 19.5 * math.cos(a2), cy + 19.5 * math.sin(a2)); c.stroke(); c.set_line_cap(0)


def tape_strip(k, pts, w=9.0):
    """the roll's free end as flat tape (28 Nov): a band w wide along pts (a polyline), the line's yellow, an ink edge,
    a shine down its middle: tape, not a string."""
    c = k.c
    c.set_line_join(1); c.set_line_cap(0)
    for col, lw in ((kit.INK, w + 3.0), (pss.TAPE, w)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        c.stroke()
    c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(1.6); c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.stroke(); c.set_line_join(0)


# ---- the ground gate (Tomas 27 Nov: "Blogai, kabo ore zmones ir daiktai") -------------------------------------------------
# Act II v2 stood Pam and the Client at the office door with their feet above the floor's back edge (on the wall), drew
# Mom "behind her desk" after the counter (her feet on its front), and put the mugs where the feet put them (f - 96) instead
# of on the counter's top. Every check passed: none looked at the ground. This one logs what the rigs and the prop drawers
# really draw while a shot's cast is drawn (the world's own coordinates) and fails:
#   FLOOR  a person's feet above the floor line, unless drawn behind the counter (the `back` pass) and hidden by it;
#   DEPTH  two people overlapping on one floor line (set_gate's rule);
#   BEHIND a person drawn behind the counter whose feet the counter does not hide (off its x, or below its front);
#   PROP   a prop neither on the floor, nor on the counter's top, nor at a hand (a rig_hands wrist, or a drawn touch).
TOP_X = (s4.CX0 - 6, s4.CX1 + 2)                               # fs_set4.counter: the top plane, x
TOP_Y = (F - 198, F - 146)                                     # and its depth, y (front edge F-150, back F-196)
GROUND_KINDS = ("FLOOR", "DEPTH", "BEHIND", "PROP", "REACH")
HOLD_R = 46                                                    # world units: a held prop's middle to the hand's point
GROUND = dict(armed=[False], on=[False], back=[False], people=[], props=[], hands=[], short=[])
_PROP_BASE = dict(mug=lambda y, s: y, cup=lambda y, s: y + 2 * s, knit=lambda y, s: y + 30 * s, pot=lambda y, s: y)
_PROP_H = dict(mug=34, cup=26, knit=40, pot=36)


def touch(x, y):
    """a hand drawn by hand (fingers as ovals): its point, for the PROP rule."""
    if GROUND["on"][0]:
        GROUND["hands"].append((x, y))


class ground_log:
    """while a shot's cast is drawn: wrap the rigs and the prop drawers to log where they draw (outermost call only)."""
    def __enter__(self):
        import mom_fs as mfs
        import client_ps as cps
        me = sys.modules[__name__]
        self.keep = []
        depth = [0]

        def wrap(mod, fn, kind, name):
            real = getattr(mod, fn)
            self.keep.append((mod, fn, real))

            def logged(*a, **kw):
                if depth[0] == 0 and GROUND["on"][0]:
                    try:
                        x, y = float(a[1]), float(a[2])
                        s = float(a[3]) if len(a) > 3 else float(kw.get("s", 1.0))
                        if kind == "person":
                            GROUND["people"].append((name, x, y, s, GROUND["back"][0]))
                        else:
                            GROUND["props"].append((name, x, y, s))
                    except (IndexError, TypeError, ValueError):
                        pass
                depth[0] += 1
                try:
                    return real(*a, **kw)
                finally:
                    depth[0] -= 1
            setattr(mod, fn, logged)
        for mod, fn, name in ((dp, "don", "don"), (pm, "pam", "pam"), (pm, "mom", "mom"), (mfs, "mom", "mom"),
                              (rp, "robot", "robot"), (dc, "father", "father"), (sd, "sofia", "sofia"),
                              (cps, "client", "client")):
            wrap(mod, fn, "person", name)
        for mod, fn, name in ((ds, "pam_mug", "mug"), (dpr, "cup_and_saucer_v2", "cup"), (dpr, "knitting_v2", "knit"),
                              (me, "coffee_pot", "pot")):
            wrap(mod, fn, "prop", name)
        for key in ("people", "props", "hands", "short"):
            del GROUND[key][:]
        GROUND["armed"][0] = True                              # floor_world turns it on for the cast only (not the room,
        return self                                            # not the office behind the glass: another space)

    def __exit__(self, *a):
        GROUND["armed"][0] = GROUND["on"][0] = False
        for mod, fn, real in reversed(self.keep):
            setattr(mod, fn, real)


def ground_faults(sid, log=None):
    """this drawing's ground faults (see above); log: (people, props, hands) for the selftest."""
    import set_gate as sg
    people, props, hands = log or (GROUND["people"], GROUND["props"], GROUND["hands"])
    out = []
    front = [(("person", n, x, f, s)) for n, x, f, s, b in people if not b]
    out += [m for m in sg.faults(sid, front) if m.startswith(("FLOOR", "DEPTH"))]
    for n, x, f, s, b in people:
        if b and not (TOP_X[0] + 10 <= x <= TOP_X[1] and F - 196 < f <= F + 2):
            out.append("BEHIND %s at (%d, %d): drawn behind the counter, but it does not hide the feet" % (n, x, f))
    for n, x, y, s in props:
        base = _PROP_BASE[n](y, s)
        mid = (x, base - 0.5 * _PROP_H[n] * s)
        if base >= F - sg.FLOOR_TOL:
            continue                                           # on the floor
        if TOP_X[0] <= x <= TOP_X[1] and TOP_Y[0] <= base <= TOP_Y[1]:
            continue                                           # on the counter's top
        if any(math.hypot(hx - mid[0], hy - mid[1]) <= HOLD_R for hx, hy in hands):
            continue                                           # in a hand
        out.append("PROP %s at (%d, %d): not on the floor, the counter's top or a hand: in the air" % (n, x, base))
    if log is None:
        for (tx, ty), S_, l_ in GROUND["short"]:
            out.append("REACH a hand at (%d, %d) past its arm's reach (%d > %d): drawn apart from the arm"
                       % (tx, ty, math.hypot(tx - S_[0], ty - S_[1]), 2 * l_))
    return list(dict.fromkeys(out))


def ground_selftest():
    """each planted fault fails; the grounded versions pass (the faults are Act II v2's own)."""
    on_wall = ([("pam", 846, F - 20, 0.54, False)], [], [])                     # 3.3 v2: Pam at the office door
    assert any(m.startswith("FLOOR") for m in ground_faults("t", on_wall))
    assert not ground_faults("t", ([("pam", 846, F + 26, 0.54, False)], [], []))
    mom_on_front = ([("mom", 824, F - 70, 0.54, False)], [], [])                # 4.3 v2: drawn after the counter
    assert ground_faults("t", mom_on_front)
    assert not ground_faults("t", ([("mom", 824, F - 70, 0.54, True)], [], []))
    assert ground_faults("t", ([("mom", 560, F - 70, 0.54, True)], [], []))    # "behind" past the counter's end
    mug_air = ([], [("mug", 708, F - 62, 0.9)], [])                             # 3.2 v2: the mug at the feet - 96
    assert any(m.startswith("PROP") for m in ground_faults("t", mug_air))
    assert not ground_faults("t", ([], [("mug", 708, F - 158, 0.9)], []))       # on the counter's top
    assert not ground_faults("t", ([], [("mug", 888, F - 140, 0.9)], [(878, F - 150)]))   # in her hand
    assert ground_faults("t", ([], [("mug", 878, F - 128, 0.9)], [(820, F - 220)]))       # 3.3 v2: hands off it
    same_line = ([("don", 530, F + 60, 0.6, False), ("robot", 600, F + 70, 0.48, False)], [], [])   # 5.3 v2
    assert any(m.startswith("DEPTH") for m in ground_faults("t", same_line))
    return True


# ---- the setups ----------------------------------------------------------------------------------------------------------
def floor_world(k, cast, spun=True, tag=False, clips=0, inside=True, haze=0.0, office=None, back=(), throne_dx=0):
    """the front desk with the office glass, the throne (its back to the street side), the floor's state, the cast.
    back: callables drawing people behind the counter (after the glass, before the counter: it hides their feet)."""
    def behind(fn):
        def run(k_):
            GROUND["back"][0] = True; GROUND["on"][0] = GROUND["armed"][0]
            try:
                return fn(k_)
            finally:
                GROUND["back"][0] = GROUND["on"][0] = False
        return run
    keep = ds.INSIDE[0]; ds.INSIDE[0] = office                 # the office behind the glass in this shot's state
    keep_t = pss.THRONE
    keep_conf = pss.s4.s3.confetti
    if NO_CONFETTI[0]:                                         # Tomas 28 Nov: episode 9's blue strips under the throne go
        pss.s4.s3.confetti = lambda *a, **kw: None             # (no story use here; ep 14's viewers asked "blue squiggles?")
    if throne_dx:                                              # 7.4: rolled toward the gap (SET_MOVES: the episode's one)
        pss.THRONE = (TX + throne_dx, keep_t[1], keep_t[2])
    try:
        heads = {n: (v[0], v[1], (v[2] if len(v) > 2 else 48 * ds.S_IN)) for n, v in
                 (ds.room(k, inside=inside, spun=spun, behind=[behind(b) for b in back]) or {}).items()}
    finally:
        ds.INSIDE[0] = keep
        pss.THRONE = keep_t
        pss.s4.s3.confetti = keep_conf
    ds._tape_seam(k.c)
    c = k.c                                                    # the throne's casters on the floor: a contact shadow
    c.set_source_rgba(0, 0, 0, 0.16); c.save(); c.translate(TX, F + 12); c.scale(96 * TS, 6); c.new_path()
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    if tag:
        tag_on_back(k)
    if clips:
        clips_on_floor(k, clips)
    GROUND["on"][0] = GROUND["armed"][0]
    try:
        heads.update(cast(k) or {})
    finally:
        GROUND["on"][0] = False
    if haze:                                                   # a near layer comes next: the world a step back
        k.c.save(); k.c.identity_matrix(); k.c.set_source_rgba(*kit.WALL, haze); k.c.paint(); k.c.restore()
    return heads


def cam_on(heads, names, size, dy=0.0, dx=0.0, zmul=1.0):
    hs = [heads[n] for n in names if n in heads]
    cam = cf.face_cam(hs, r_target=R_TARGET[size])
    return (cam[0] + dx, cam[1] + dy, cam[2] * zmul)


# ---- Act I ----------------------------------------------------------------------------------------------------------------
def s11(k):
    """1.1 frame 0: the locked S8r still (the file da_s8r.still writes; 9.1 ends on it)."""
    img = cairo.ImageSurface.create_from_png(os.path.join(EP, "da_s8r_frame0_v5.png"))      # v5: no name badges
    k.c.save(); k.c.scale(W / float(img.get_width()), H / float(img.get_height()))
    k.c.set_source_surface(img, 0, 0); k.c.paint(); k.c.restore()
    return None, {}


def s12(k):
    """1.2 S3 M: his screen-right knee up, the roll stuck to that sole swung across into his other shin; one hand
    still on the throne's armrest (CLUTCH), the other flung open (PALM): the hand sheet's 1.1/1.2 jobs."""
    def cast(k_):
        x, f = MARKS["don_hop"]; DON_FEET[0] = (x, f)
        s_ = SC["don"]
        sole = sole_of(x, f, s_)                                 # the raised shoe's sole (knee 1.0)
        shin = (x - 18 * s_, f - 70 * s_)                        # the standing leg's shin
        arm = (TX - 66 * TS, F - 150 * TS)                       # the throne's near armrest
        shadow(k_, x, f + 2, 40)
        o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "panic", (0.6, 0.6), knee=1.0, hands=False), s_,
                      {1: dict(T=(arm[0] - 10, arm[1] + 4), pose="CLUTCH", out=1),
                       -1: dict(T=(x - 70 * s_, f - 250 * s_), pose="PALM", out=-1)})
        c = k_.c                                                 # the tongue from the sole to the roll at his shin
        roll_at(k_, shin[0] + 6, shin[1] + 18)
        dp._cap(c := k_.c, [(sole[0] - 2, sole[1] - 2), ((sole[0] + shin[0]) / 2 + 6, (sole[1] + shin[1]) / 2 + 14),
                            (shin[0] + 18, shin[1] + 12)], 6, pss.TAPE, lw=1.4)      # the sticky tongue: sole -> roll
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(1.2)
        c.new_path(); c.move_to(sole[0] - 2, sole[1] - 3); c.line_to(shin[0] + 18, shin[1] + 11); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(2.0); c.set_line_cap(1)
        c.new_path(); c.arc(x + 40 * s_, f - 60 * s_, 40, 0.35, 1.15); c.stroke()      # one swing arc
        for dy in (-7, 7):                                       # the hit: two short marks, not legs
            c.new_path(); c.move_to(shin[0] - 8, shin[1] + 18 + dy); c.line_to(shin[0] - 18, shin[1] + 18 + dy * 1.6); c.stroke()
        c.set_line_cap(0)
        return {"don": _head(o, "don"), "roll": (shin[0], shin[1], 18)}
    return ("floor", dict(cast=cast)), dict(names=["don"], size="M", dy=20, focus=("roll", "don"))


def s13(k):
    """1.3 S1 W, low: Father's polished shoes and burgundy hem step over the tape near the lens, his body out of the top
    of the frame; behind, small: Don on one leg holding his shin, the robot letting go."""
    def cast(k_):
        h = {}
        h["robot"] = robot(k_, (590, F + 18), look=(1, 0), tilt=-0.05)
        h["don"] = don(k_, "don_hop", "balance", "shock", look=(1, -0.6), knee=0.7)
        return h

    def near(k_, cam):                                         # frame units, drawn at the frame's own line weight
        father_step(k_, cam)
        return {}
    return ("floor", dict(cast=cast, clips=0, haze=0.18)), dict(names=["don", "robot"], size="W", dy=-40, near=near,
                                                    focus=("near",))


def _oxford(k, x, y, ln, ang, seed, lift=False):
    """a polished black oxford seen from the side-front, its heel at (x, y), toe along ang; lift: the heel up, the toe
    down (mid-step)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang)
    kit.cut(k, [(-6, -4), (-4, -30), (ln * 0.35, -34), (ln * 0.8, -28), (ln, -14), (ln + 2, 2), (-6, 2)], SHOE, lw=2.4)
    c.set_source_rgb(0.32, 0.32, 0.36); c.set_line_width(1.6)
    c.new_path(); c.move_to(ln * 0.62, -30); c.curve_to(ln * 0.70, -18, ln * 0.70, -8, ln * 0.64, 0); c.stroke()   # toe cap
    kit.cut(k, [(-6, 2), (ln + 2, 2), (ln, 7), (-6, 7)], (0.20, 0.15, 0.11), shadow=False, lw=1.4)          # the sole
    c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(2.4); c.set_line_cap(1)
    c.new_path(); c.move_to(ln * 0.72, -26); c.line_to(ln * 0.88, -20); c.stroke(); c.set_line_cap(0)    # the shine
    c.restore()


def _leg(k, hip, knee, ankle, w_hip, w_knee, w_cuff, col, crease):
    """a trouser leg as one tapered piece hip -> knee -> cuff (wider at the hip, narrowing to the cuff), the knee a
    visible bend (two fold lines on its inside), the crease running down it."""
    c = k.c
    def side(p, q, w):
        dx, dy = q[0] - p[0], q[1] - p[1]; n = math.hypot(dx, dy) or 1
        return (-dy / n * w / 2, dx / n * w / 2)
    a1 = side(hip, knee, w_hip); a2 = side(knee, ankle, w_knee); a3 = side(knee, ankle, w_cuff)
    pts = [(hip[0] + a1[0], hip[1] + a1[1]), (knee[0] + a2[0], knee[1] + a2[1]), (ankle[0] + a3[0], ankle[1] + a3[1]),
           (ankle[0] - a3[0], ankle[1] - a3[1]), (knee[0] - a2[0], knee[1] - a2[1]), (hip[0] - a1[0], hip[1] - a1[1])]
    kit.cut(k, pts, col, lw=2.4)
    c.set_source_rgb(*crease); c.set_line_width(1.8); c.set_line_cap(1)
    c.new_path(); c.move_to(*hip); c.line_to(*knee); c.line_to(*ankle); c.stroke()
    bend = abs(math.atan2(knee[0] - hip[0], knee[1] - hip[1]) - math.atan2(ankle[0] - knee[0], ankle[1] - knee[1]))
    if bend > 0.25:                                            # a bent knee: its folds
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        for i in (0, 1):
            c.new_path(); c.move_to(knee[0] - a2[0] * 0.8 + i * 6, knee[1] - a2[1] * 0.8 - 8 + i * 10)
            c.line_to(knee[0] - a2[0] * 0.2 + i * 6, knee[1] - a2[1] * 0.2 - 2 + i * 10); c.stroke()
    c.set_line_cap(0)


def father_step(k, cam):
    """1.3's near layer (frame units), drawn from Father's own parts and colours (dh_cast: the velvet jacket and its
    lighter nap, the black trousers and their crease, the shined black shoes and their rim) at the frame's line weight:
    the jacket's hem across the top (the body out of the frame), the hips, one leg planted on his side of the tape
    (screen right), the other mid-step over it: thigh forward, the knee bent, the shin back, the heel up; tapered legs,
    knee folds, a contact shadow under the planted shoe."""
    fx, fy, z = cam
    c = k.c
    ys = 652.0
    wy = fy + (ys - 480) / z
    tx = 270 + (tape_x(wy) - fx) * z
    VEL, VEL_L, BLK, BLK_L = dc.VELVET, dc.VELVET_L, dc.BLACK, dc.BLACK_L
    hipL, hipR = (tx - 54, 214), (tx + 40, 214)
    c.set_source_rgba(0, 0, 0, 0.26)                           # the planted shoe's contact shadow
    c.save(); c.translate(tx + 58, ys + 4); c.scale(64, 8); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    kit.cut(k, [(tx - 98, 160), (tx + 86, 160), (tx + 82, 236), (tx - 94, 236)], BLK, lw=2.4)   # the hips
    _leg(k, hipR, (tx + 52, 430), (tx + 58, ys - 22), 76, 62, 56, BLK, BLK_L)                 # planted
    _oxford(k, tx + 18, ys - 6, 98, -0.02, 4820)
    _leg(k, hipL, (tx - 30, 420), (tx - 84, ys - 112), 76, 62, 56, BLK, BLK_L)                # mid-step, the knee bent
    _oxford(k, tx - 104, ys - 96, 98, 0.38, 4830, lift=True)
    c.new_path()                                               # the jacket: one silhouette, its hem curving round the hips
    c.move_to(tx - 172, 88); c.line_to(tx + 160, 88); c.curve_to(tx + 166, 150, tx + 158, 196, tx + 142, 214)
    c.curve_to(tx + 100, 222, tx + 40, 220, tx + 6, 200); c.curve_to(tx - 30, 222, tx - 110, 224, tx - 156, 214)
    c.curve_to(tx - 172, 190, tx - 178, 140, tx - 172, 88); c.close_path()
    c.set_source_rgb(*VEL); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    c.set_source_rgb(0.20, 0.04, 0.07); c.set_line_width(3.0)  # the opening over the black shirt and belt
    c.new_path(); c.move_to(tx - 6, 88); c.curve_to(tx - 2, 140, tx + 2, 170, tx + 6, 200); c.stroke()
    c.set_source_rgba(*VEL_L, 0.9); c.set_line_width(3.2); c.set_line_cap(1)      # the nap catching light, both sides
    for sx in (-1, 1):
        c.new_path(); c.move_to(tx + sx * 140, 100); c.curve_to(tx + sx * 148, 140, tx + sx * 144, 180, tx + sx * 132, 206)
        c.stroke()
    c.set_line_cap(0)


def s13b(k):
    """1.3b S3 MC: the throne's back, the ringed hand hanging REVIEW · TOMORROW on it."""
    def cast(k_):
        c = k_.c
        tag_on_back(k_)
        hx, hy = TX - 56 * TS, F - 432 * TS                    # the hand at the tag's string, the sleeve up out of frame
        kit.cut(k_, [(hx + 160, hy - 40), (hx + 160, hy - 4), (hx + 14, hy + 8), (hx + 8, hy - 12)], (0.45, 0.10, 0.16), lw=2)
        kit.ellipse(k_, hx + 4, hy - 2, 10, 8, (0.94, 0.80, 0.68), 4731, shadow=False, lw=2)     # the hand at the string,
        kit.ellipse(k_, hx + 8, hy + 3, 3, 3, (0.93, 0.74, 0.22), 4732, shadow=False, lw=1)    # the ring; the sleeve from
                                                                                                # the right, off the sign
        return {"tag": (hx, hy + 30, 30)}
    return ("floor", dict(cast=cast)), dict(names=["tag"], size="MC", dy=60)


def s14(k):
    """1.4 S1 W: Sofía behind Father over the line, the clear box in both hands (board_two) catching the throne's
    armrest; clips in the air and on the floor round the casters, one under a caster; the robot kneeling to them."""
    def cast(k_):
        h = {}
        h["don"] = don(k_, "don_hop", "stand", "confused", look=(1, 0.5))
        bx, bf = TX + 92, F + 40
        shadow(k_, bx, bf + 2, 32)
        o = sd.with_board(k_, bx, bf, SC["sofia"], "box", face_kind="smile", look=(1, 0), full=0.5)
        h["sofia"] = (o["head"][0], o["head"][1], R["sofia"] * SC["sofia"])
        import random
        r = random.Random(4760)
        old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
        for i in range(9):                                      # in the air, from the box's tipped corner down
            sd.paperclip(k_, TX + 50 + r.uniform(-10, 30), F - 150 + i * 16 + r.uniform(-6, 6), CLIP_S, r.uniform(-3, 3))
        sd.CLIPS_V2[0] = old
        h["robot"] = robot(k_, (TX + 150, F + 70), tilt=0.30, look=(-1, 1))
        return h
    return ("floor", dict(cast=cast, tag=True, clips=30)), dict(names=["sofia", "don"], size="M", dy=30,
                                                               focus=("sofia",))


def s15(k):
    """1.5 S3 M: his knee up, he pulls the roll off his sole (GRAB, the hand sheet's 1.5 job), annoyed; it drops by
    the throne next."""
    def cast(k_):
        x, f = MARKS["don_hop"]; DON_FEET[0] = (x, f)
        s_ = SC["don"]
        sole = sole_of(x, f, s_)
        shadow(k_, x, f + 2, 40)
        o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "confused", (1, 0.8), knee=1.0, hands=False), s_,
                      {1: dict(T=(sole[0] - 14, sole[1] - 10), pose="GRAB", out=1, contact="object",
                               obj=lambda kk, P, w: roll_at(kk, P[0], P[1] + 18))})
        return {"don": _head(o, "don"), "roll": (sole[0], sole[1], 18)}
    return ("floor", dict(cast=cast, tag=True, clips=29)), dict(names=["don"], size="M", dy=20, focus=("roll", "don"))


S7 = (659, 700, 0.90)                                          # the episode's master (da_establish_v3)


def s21(k):
    """2.1 S7 W: Don toes at his line; inside the glass Father sits down in Don's chair (establish's inside); the robot
    low, picking clips."""
    def cast(k_):
        h = {}
        h["robot"] = robot(k_, (MARKS["robot_pile"][0], F + 60), tilt=0.25, look=(0, 1))
        h["don"] = don(k_, "don_s7", "stand", "confused", look=(1, -0.5))
        return h
    return ("floor", dict(cast=cast, tag=True, clips=28)), dict(names=["don"], size="W", cam=S7)


S8_MUG = [None]   # 28 Nov (Tomas: 3.5's mug = the cups canon's): opt-in drawer for the S8 desk mug; None = as locked


def s8_compose(k, pam_in=False, plan=None, mug=False, client="stand", photo=None, outside=None, mug_at=(378, 702)):
    """S8 (inside Don's office) in the state of a given shot, from da_s8's layers and da_push91's split of its meeting:
    the glass (v9: S8r small behind it; its state is the tug's, a known gap until S8r takes a cast: layout v2), Don's
    chair and Father, Sofía reading, the desk; Pam and the plan and her mug only once they are there; the Client
    standing (before 7.3) or over the plan (7.3, 8.1). photo: None | "down_heel" (2.2)."""
    import da_s8 as s8
    import da_push91 as pu
    import da_arms
    da_arms.setup()
    s8.V5[0] = s8.V6[0] = s8.V8[0] = s8.V9[0] = True; ds.MUG_V2[0] = True
    s8.CHAIR_VARIANT[0] = "L"; s8.S8R_FILE[0] = "da_s8r_frame0_v5.png"; s8.GLASS_SOFT[0] = 0.62   # v11's glass
    heads = {}
    keep = s8._S8R_IMG[0]
    if outside:                                               # the floor behind the glass in this shot's state
        s8._S8R_IMG[0] = s8r_floor(outside)
    try:
        s8.window_only(k, "tidy8")
    finally:
        s8._S8R_IMG[0] = keep
    if photo == "finger":                                     # 2.2 v2 (Tomas 28 Nov: the feet on the desk "look very bad"):
        st = PHOTO22                                          # upright in Don's chair, one finger tips Don's photo over
        s8.chair(k, 336, 378, 1.0)
        hp, hv = pu._hands_on()
        try:
            hp.reset("point" if st["reach"] > 0.5 else "quiet", "quiet")
            bt = -300 * 1.12 + 78
            r0, r1 = (4, bt + 112), ((PHOTO_AT[0] + 2 - 336) / 0.78, (st["top"] - 12 - st["feet"]) / 0.78)
            u = st["reach"]
            s8.seated(k, lambda: s8._father_rest(k, feet=st["feet"], left=None if u <= 0 else
                                                 (r0[0] + (r1[0] - r0[0]) * u, r0[1] + (r1[1] - r0[1]) * u)))
        finally:
            hv.disable(); kit.HAND[0] = None
    elif photo == "down_heel":                                # slouched for his feet on the desk: lower in the chair
        s8.chair(k, 336, 378, 1.0)
        hp, hv = pu._hands_on()
        try:
            hp.reset("quiet", "quiet")
            s8.seated(k, lambda: s8._father_rest(k, feet=716))
        finally:
            hv.disable(); kit.HAND[0] = None
    else:
        pu.father_layer(k)
    heads["father"] = (336, 470 + (10 if photo == "down_heel" else 0), 40)
    if client == "stand":                                     # behind the desk, left, glancing at the photo
        import client_ps as cps
        o = cps.client(k, 120, 800, 0.66, look=(1, 0.6))
        heads["client"] = (o["head"][0], o["head"][1], 50 * 0.66)
    hp, hv = pu._hands_on()
    try:
        hp.reset("quiet", "quiet")
        s8.seated(k, lambda: sd.with_board(k, 444, 748, 0.66, "binder", face_kind="interested", look=(-1.0, 0.9), lift=62))
    finally:
        hv.disable(); kit.HAND[0] = None
    if pam_in:
        heads["pam"] = s8.seated(k, lambda: s8.pam_taking(k))["head"] + (48 * 0.66,)
    s8.desk(k)
    if plan == "open":
        s8.blueprint(k, *s8.PLAN_AT)
    if mug:
        s8.prop_shadow(k, mug_at[0] + 6, mug_at[1], 18)
        (S8_MUG[0] or ds.pam_mug)(k, mug_at[0], mug_at[1], 1.15)
    if pam_in and plan == "open":
        s8.pam_hands_over(k)
    if client == "over":
        heads.update({n: v + (50 * 0.70,) if len(v) == 2 else v for n, v in s8.client_over_desk(k).items()})
    if photo == "finger":
        heads["photo"] = photo22(k, PHOTO22["tip"])
    if photo == "down_heel":                                  # both feet up on the desk from his chair, toward us: the
        heads.update(feet_on_desk(k))                                       # legs over the far edge, the soles to the camera, his left
                                                              # heel on Don's gold photo (face down), the right crossed
    s8.light(k)
    return heads


def s8r_floor(cast):
    """the floor seen from the office side (S8r) with a shot's own cast and state, as a 2x surface for the S8 glass
    (da_s8.s8r_world): da_s8r's room and throne (upright, its price tag to us), then cast(k) in S8r's frame units."""
    import da_s8r as r8
    import dh_props as dhp
    r8.use("v4")
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2)
    c = cairo.Context(surf); c.scale(2, 2); k = Ctx(c, 0)
    r8.room(k)
    tx, tf, ts = r8.THRONE
    shadow(k, tx, tf + 2, 120)
    old = dhp.TAG[0], dhp.TAG_FONT[0]; dhp.TAG[0] = True; dhp.TAG_FONT[0] = r8.TAG_FONT
    try:
        dhp.ceo_chair(k, tx, tf, ts)
    finally:
        dhp.TAG[0], dhp.TAG_FONT[0] = old
    cast(k)
    surf.flush()
    return surf


def out_22(k):
    """2.2's outside: Don at his line, facing his office; the robot crouched on Father's side, picking a clip."""
    import da_s8r as r8
    old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
    import random
    r = random.Random(4750)
    for i in range(18):
        sd.paperclip(k, r.uniform(20, 200), r8.FEET + r.uniform(-6, 40), CLIP_S * 1.15 / 0.6, r.uniform(-3, 3))
    sd.CLIPS_V2[0] = old
    shadow(k, 120, r8.FEET + 4, 60)
    rp.robot(k, 120, r8.FEET + 2, 0.92, tilt=0.32, look=(0, 1))
    shadow(k, 392, r8.FEET + 10, 70)
    dp.don(k, 392, r8.FEET + 8, 1.15, "stand", "squint", look=(0, -0.2))


TROUSER, TROUSER_L = (0.11, 0.10, 0.12), (0.24, 0.23, 0.27)
SHOE, SOLE, HEEL = (0.06, 0.05, 0.05), (0.30, 0.22, 0.16), (0.16, 0.11, 0.08)


def _sole_to_us(k, x, y, w, h, seed):
    """a shoe seen from its sole's end (the foot up on a desk, toward the camera): the upper's rim, the leather sole,
    the heel block at the bottom, a shine on the toe."""
    kit.ellipse(k, x, y, w, h, SHOE, seed, lw=2.2)
    kit.ellipse(k, x, y - 1, w * 0.78, h * 0.82, SOLE, seed + 1, shadow=False, lw=1.4)
    kit.cut(k, [(x - w * 0.62, y + h * 0.42), (x + w * 0.62, y + h * 0.42), (x + w * 0.56, y + h * 0.98),
                (x - w * 0.56, y + h * 0.98)], HEEL, shadow=False, lw=1.6)
    c = k.c; c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(1.4)
    c.new_path(); c.arc(x, y - h * 0.55, w * 0.5, 3.6, 5.8); c.stroke()


def feet_on_desk(k):
    """2.2: Father slouched in Don's chair, both feet up on the desk toward us, drawn in his rig's colours (dh_cast's
    black trousers and their lighter crease, his shined black shoes). The chain reads from his lap (the jacket's hem
    over it, above the desk's far edge) -> the thigh coming at us (short: foreshortened) -> the knee -> the shin down to
    the shoe on the desk, its sole to the camera. His screen-left heel on Don's gold photo, face down; the other leg
    crossed over that ankle, casting its shadow on it; a contact shadow under each heel."""
    BLACK, BLACK_L = dc.BLACK, dc.BLACK_L
    c = k.c
    kit.cut(k, [(276, 707), (326, 703), (329, 714), (274, 718)], (0.62, 0.48, 0.18), lw=2)      # the photo, face down
    kit.cut(k, [(280, 708), (322, 705), (324, 711), (279, 714)], (0.83, 0.66, 0.24), shadow=False, lw=1)
    kit.cut(k, [(304, 612), (368, 612), (372, 640), (300, 640)], BLACK, lw=2)                  # his lap, over the far edge
    for sx in (-1, 1):                                                                       # the jacket's hem on it
        kit.cut(k, [(336 + sx * 4, 600), (336 + sx * 38, 598), (336 + sx * 40, 626), (336 + sx * 8, 630)], dc.VELVET,
                shadow=False, lw=1.8)
    legs = (((318, 638), (308, 660), (300, 690), 4800), ((354, 638), (360, 658), (342, 678), 4810))
    for i, ((hx, hy), (kx, ky), (fx, fy), seed) in enumerate(legs):
        dp._cap(c, [(hx, hy), (kx, ky)], 30, BLACK, lw=2.2)                                   # thigh (toward us: short)
        dp._cap(c, [(kx, ky), (fx, fy - 18)], 26, BLACK, lw=2.2)                              # shin down to the shoe
        c.set_source_rgb(*BLACK_L); c.set_line_width(1.6)
        c.new_path(); c.move_to(hx, hy + 2); c.line_to(kx, ky); c.line_to(fx, fy - 20); c.stroke()     # the crease
        if i == 0:
            c.set_source_rgba(0, 0, 0, 0.30); c.save(); c.translate(fx + 2, fy + 18); c.scale(22, 5)  # heel on the photo
            c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        else:
            c.set_source_rgba(0, 0, 0, 0.28); c.save(); c.translate(fx - 12, fy + 4); c.scale(18, 9)  # on the other shin
            c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        _sole_to_us(k, fx, fy, 19, 25, seed)
    return {"feet": (320, 684, 34)}


def crop(k, z, cx, cy, draw):
    """an S8 key frame as a crop of the frame-unit drawing: z about (cx, cy); the heads mapped to the crop."""
    c = k.c
    c.save(); c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)
    h = draw(k)
    c.restore()
    return {n: (270 + (x - cx) * z, 480 + (y - cy) * z, r * z) for n, (x, y, r) in h.items()}


PHOTO22_MODE = ["down_heel"]                                 # opt-in "finger" (2.2 v2); the layout as approved by default
PHOTO22 = dict(reach=0.0, tip=0.0, feet=706, top=612)
PHOTO_AT = (304, 674, 1.25)                                   # Don's gold photo on his desk, before Father's chest


def photo22(k, tip):
    """DON · CEO in its gold frame, standing on the desk; tip 0..1: pushed over from its top, forward onto its face (we
    then see its back: the darker card, the easel's leg)."""
    c = k.c
    px, py, z = PHOTO_AT
    s8 = __import__("da_s8")
    s8.prop_shadow(k, px + 3, py + 2, 30)
    if tip < 0.5:
        c.save(); c.translate(px, py); c.scale(z, z * max(0.10, math.cos(tip * math.pi)))
        kit.cut(k, [(-24, -50), (24, -50), (24, 0), (-24, 0)], (0.83, 0.66, 0.24), lw=2)
        kit.cut(k, [(-18, -44), (18, -44), (18, -6), (-18, -6)], (0.72, 0.82, 0.90), shadow=False, lw=1.4)
        if tip < 0.25:
            dp.don(k, 0, -6, 0.13, "stand", "smug", (0, 0))
            c.select_font_face(kit.FONT); c.set_font_size(6); c.set_source_rgb(*kit.INK)
            e = c.text_extents("DON · CEO"); c.move_to(-e.x_advance / 2, -1); c.show_text("DON · CEO")
        c.restore()
    else:
        d = 30 * math.sin((tip - 0.5) * math.pi)              # its back, lying toward us
        kit.cut(k, [(px - 30, py), (px + 30, py - 3), (px + 33, py - 3 + d), (px - 34, py + 2 + d)], (0.62, 0.48, 0.18), lw=2)
        if d > 14:
            kit.cut(k, [(px - 4, py + 4), (px + 5, py + 3), (px + 7, py + d - 6), (px - 5, py + d - 5)], (0.48, 0.36, 0.12),
                    shadow=False, lw=1.2)                      # the easel's leg, folded flat
    return (px, py - 30, 34)


def s22(k):
    """2.2 S8 M: Father's heel on Don's face-down desk photo; the Client glancing at it; Sofía reading; no Pam yet.
    (v2, opt-in: one finger tips the photo over.)"""
    return None, crop(k, 1.45, 330, 560, lambda k_: s8_compose(k_, photo=PHOTO22_MODE[0], outside=out_22))


def s23(k):
    """2.3 S3 MC: both fists on the vest's hem (CLUTCH, the hand sheet's 2.3 job), a hard tug, chin up, offended; his
    screen-left hem stays crooked (the audit's cheap gag)."""
    def cast(k_):
        x, f = MARKS["don_counter"]; DON_FEET[0] = (x, f)
        s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "smug", (1, -0.4), chin=1, hands=False), s_,
                      {-1: dict(T=(x - 34 * s_, f - 168 * s_), pose="CLUTCH", out=-1),
                       1: dict(T=(x + 34 * s_, f - 160 * s_), pose="CLUTCH", out=1)})
        c = k_.c                                                 # the crooked hem: a fold left up on his screen-left side
        kit.cut(k_, [(x - 46 * s_, f - 150 * s_), (x - 12 * s_, f - 156 * s_), (x - 14 * s_, f - 142 * s_)],
                (0.14, 0.20, 0.33), shadow=False, lw=1.6)
        return {"don": _head(o, "don")}
    return ("floor", dict(cast=cast, tag=True, clips=26)), dict(names=["don"], size="MC", dy=-70, focus=("don",))


def s24(k):
    """2.4 S3 M two-shot: Don holds the gift out at her chest height (GRAB, the hand sheet's 2.4 job), a wide, fake
    grin (a bribe for loyalty, just after Father's humiliation); Pam looks at the mug, unsure; her blue mug dropping from
    her open hand (PALM), the shards already starting at her feet."""
    def cast(k_):
        h = {}
        px, pf = MARKS["pam_counter"]
        shadow(k_, px, pf + 2, 32)
        o = pm.pam(k_, px, pf, SC["pam"], "stand", "doubt", (-1, 0.6), mug=False)
        h["pam"] = _head(o, "pam")
        dpr.shards_v2(k_, px - 6, pf + 8, 0.6)
        kit.ellipse(k_, px + 24, pf - 60, 8, 10, dpr.BLUE_MUG, 4770, lw=1.8)           # the blue mug, falling
        x, f = MARKS["don_gift"]; DON_FEET[0] = (x, f)
        s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        T = (px - 46, pf - 112)                                  # her chest height, between them
        od = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "grin", (1, 0), hands=False), s_,
                       {1: dict(T=T, pose="GRAB", out=1, contact="object",
                                obj=lambda kk, P, w: dpr.gift_mug_v2(kk, P[0], P[1] + 12, 0.55))})
        h["don"] = _head(od, "don")
        h["gift"] = (T[0] + 14, T[1], 14)
        return h
    return ("floor", dict(cast=cast, tag=True, clips=25)), dict(names=["don", "pam"], size="M", dy=-60,
                                                               focus=("gift", "pam"))


# ---- Act II ---------------------------------------------------------------------------------------------------------------
def coffee_pot(k, x, y, s=1.0, ang=0.0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    kit.cut(k, [(-14, -30), (14, -30), (18, 0), (-18, 0)], (0.80, 0.86, 0.92), lw=2)     # the glass jug
    kit.cut(k, [(-17, -14), (17, -14), (18, 0), (-18, 0)], (0.30, 0.18, 0.10), shadow=False, lw=1.4)   # coffee
    kit.cut(k, [(-16, -36), (16, -36), (14, -30), (-14, -30)], (0.15, 0.15, 0.16), shadow=False, lw=1.6)  # lid
    c.set_source_rgb(*INK); c.set_line_width(5); c.new_path(); c.arc(22, -16, 9, -1.6, 1.6); c.stroke()
    c.restore()


def s31(k):
    """3.1 S3 MC: Don not turning, eyes front, smug, holding his empty white cup up over his shoulder, upside down: "fill
    this". An order, not a hello. 27 Nov: the snap read as a wave or a head-scratch in three cold tests; the gesture
    changed (rules-hands: change the gesture after three misreads) to the prop: an empty cup held up needs no sound."""
    def cast(k_):
        x, f = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]   # 24 off the floor's DON (his shoe on its N)
        DON_FEET[0] = (x, f); s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        T = (x - 130 * s_, f - 400 * s_)                       # screen-left (off the apps' rail), out beside his head

        def cup_up(kk, P, w):                                  # hung from his grip by its handle, mouth down: empty
            c = kk.c; u = 1.35
            cx_, top = P[0] - 16 * u, P[1] - 4 * u
            kit.cut(kk, [(cx_ - 9 * u, top), (cx_ + 9 * u, top), (cx_ + 13 * u, top + 26 * u), (cx_ - 13 * u, top + 26 * u)],
                    (0.98, 0.98, 0.96), shadow=False, lw=1.8)          # the body, its foot up
            kit.ellipse(kk, cx_, top + 26 * u, 13 * u, 3.6 * u, (0.86, 0.86, 0.84), 3101, shadow=False, lw=1.6)   # the
            c.set_source_rgb(*INK); c.set_line_width(4.2)                                 # mouth: empty, pale
            c.new_path(); c.arc(cx_ + 12 * u, top + 12 * u, 6 * u, -1.4, 1.4); c.stroke()  # the handle, into his grip
            c.set_source_rgb(0.98, 0.98, 0.96); c.set_line_width(2.0)
            c.new_path(); c.arc(cx_ + 12 * u, top + 12 * u, 6 * u, -1.4, 1.4); c.stroke()
        o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "smug", (-0.4, -0.1), chin=1, hands=False), s_,
                      {-1: dict(T=T, pose="CUP_GRIP", out=-1, reach=True, obj=cup_up, contact="handle")})
        T = o["wrists"][-1]
        c = k_.c; c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)   # a shake: two short arcs by it
        for r_ in (26, 34):                                    # left of the cup, away from his face
            c.new_path(); c.arc(T[0] - 22, T[1] + 18, r_, 2.6, 3.7); c.stroke()
        c.set_line_cap(0)
        return {"don": _head(o, "don"), "cup": (T[0] - 20, T[1] + 14, 30)}
    return ("floor", dict(cast=cast, tag=True, clips=24)), dict(names=["don"], size="MC", dy=-40, focus=("cup", "don"),
                                                              frame_on=["don"])   # framed on his face


def s32(k):
    """3.2 S6 M: Pam pours from the jug: a visible stream into HER mustard mug first; Don's white cup and saucer
    waiting beside it. Through the glass, still: Father and the Client waiting.
    27 Nov (the audit, round 3): from in front she could not reach the counter's top (a hand drawn apart, at the jug);
    she pours from her own place behind it (fs_set4.HOME's Pam), the mugs on its top in front of her."""
    px, pf = 692, F - 128                                      # behind the counter, a step back from fs_set4.HOME's
                                                               # F-72: Pam is shorter than Mom (at F-72 only her head showed)
    mug = (748, F - 156)                                       # on the counter's top at her right, clear of the monitor
                                                               # (at 646 it hid the jug) and of Mom's place (760 behind)

    def pam_back(k_):
        T = (mug[0] - 34, mug[1] - 58)                         # the wrist over the mug, the jug tipped to it
        o = rig_hands(k_, lambda kk, a4: pm.pam(kk, px, pf, SC["pam"], a4, "neutral", (1, 0.9), mug=False), SC["pam"],
                      {1: dict(T=T, pose="GRAB", out=1)}, sex="f", skin=FEMALE)
        T = o["wrists"][1]
        ang = 1.05
        coffee_pot(k_, T[0] + 12, T[1] + 10, 0.75, ang)
        sx = T[0] + 12 + (16 * math.cos(ang) - (-34) * math.sin(ang)) * 0.75        # the jug's lip, tipped
        sy = T[1] + 10 + (16 * math.sin(ang) + (-34) * math.cos(ang)) * 0.75
        STREAM[0] = (sx, sy)
        return {"pam": _head(o, "pam")}

    def cast(k_):
        h = {}
        ds.MUG_V2[0] = True
        ds.pam_mug(k_, mug[0], mug[1], 0.9)
        dpr.cup_and_saucer_v2(k_, mug[0] - 70, mug[1] - 2, 0.7)   # left of hers (round 4: on the right it framed
                                                                  # Mom's nameplate in: Pam read as "Assistant to Don")
        sx, sy = STREAM[0]
        c = k_.c                                               # the stream: the jug's lip -> her mug
        c.set_source_rgb(0.30, 0.18, 0.10); c.set_line_width(3.2); c.set_line_cap(1)
        c.new_path(); c.move_to(sx, sy); c.curve_to(sx + 4, sy + 10, mug[0] - 2, mug[1] - 40, mug[0], mug[1] - 24)
        c.stroke(); c.set_line_cap(0)
        h["mug"] = (mug[0], mug[1] - 14, 16)
        return h
    office = dict(client="stand", sofia=True)
    return ("floor", dict(cast=cast, tag=True, clips=23, office=office, back=[pam_back])), dict(names=["pam"], size="M",
                                                                                         dy=0, dx=-60, focus=("mug", "pam"))


STREAM = [(0.0, 0.0)]


def s33(k):
    """3.3 S7 M: at the office door the Client, half in the gap (the door's frame over his near side), takes her mug
    with his hand; Pam's hand still on it; Mom behind her desk rising (in the scene, not required in frame).
    27 Nov (Tomas: "kabo ore"): everyone on the floor or behind the counter; the mug in both their hands."""
    def mom_back(k_):
        return {"mom": mom(k_, "mom_desk_s", "fists", "glare", look=(1, 0))}

    def cast(k_):
        h = {}
        import client_ps as cps
        cx_, cf_ = MARKS["client_door"]
        o = cps.client(k_, cx_, cf_, SC["client"], pose="open", face="bored", look=(-1, 0))
        h["client"] = (o["head"][0], o["head"][1], R["client"] * SC["client"])
        kit.cut(k_, [(898, F - 330), (910, F - 330), (910, F - 2), (898, F - 2)], ds.DESK_D, lw=2)   # the door's jamb
                                                               # (v2 at 884-898 stood on the counter's end, over Mom's mug)
        x, f = MARKS["pam_door"]
        shadow(k_, x, f + 2, 32)
        mx, my = 892, F - 112                                  # the mug between them at waist height, past the door's edge
        o = rig_hands(k_, lambda kk, a4: pm.pam(kk, x, f, SC["pam"], a4, "doubt", (1, -0.2), mug=False), SC["pam"],
                      {1: dict(T=(mx - 14, my - 12), pose="GRAB", out=1)}, sex="f", skin=FEMALE)
        h["pam"] = _head(o, "pam")
        ds.MUG_V2[0] = True
        ds.pam_mug(k_, mx, my, 0.9)
        fx_, fy_ = mx + 16, my - 18
        kit.ellipse(k_, fx_, fy_, 8, 7, (0.80, 0.68, 0.56), 4840, shadow=False, lw=1.4)       # his fingers on it
        kit.ellipse(k_, fx_ + 2, fy_ + 9, 7, 6, (0.80, 0.68, 0.56), 4842, shadow=False, lw=1.4)
        touch(fx_, fy_)
        h["mug"] = (mx, my - 14, 16)
        return h
    return ("floor", dict(cast=cast, tag=True, clips=22, back=[mom_back])), dict(names=["pam", "client"], size="M",
                                                                              dx=0, focus=("mug", "client"))


def s34(k):
    """3.4 S7 M: Mom planted at the counter's end, fists on her hips, chin up, not moving; Don behind her shoulder on
    tiptoe, craning to see the glass past her: he cannot get round her. Low behind her the robot frozen, pincer up.
    Through the glass, still: her mug on Father's table, Pam's hand on it.
    27 Nov (Tomas: B): the feint (his whole body pitched) read as a stagger, a shove or a fall in four cold tests; now
    no contact and no pitch: on his toes behind her, looking past her."""
    def cast(k_):
        h = {}
        h["robot"] = robot(k_, (MARKS["robot_pile"][0] + 40, F + 64), tilt=0.1, look=(-1, -0.4), arms=((0, 0), (160, 20)))
        x, f = MARKS["don_peek"]; DON_FEET[0] = (x, f)        # behind her (further back: feet higher), his side
        shadow(k_, x, f + 2, 36)
        c = k_.c
        c.save(); c.translate(0, -12 * SC["don"] / 0.6)        # on his toes: the heels up, the body a hand higher
        try:
            o = tilted(k_, x, f, 0.12, lambda: dp.don(k_, x, f, SC["don"], "stand", "confused", (1, -0.8), chin=1))
                                                               # craning toward the glass; his hands his own, off her
        finally:
            c.restore()
        hx, hy, r_ = _head(o, "don")
        hx, hy = x + (hx - x) * math.cos(0.12) - (hy - f) * math.sin(0.12), f + (hx - x) * math.sin(0.12) + (hy - f) * math.cos(0.12)
        h["don"] = (hx, hy - 12 * SC["don"] / 0.6, r_)
        c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_cap(1)   # the tiptoe: two lift ticks under his heels
        for dx in (-14, 10):
            c.new_path(); c.move_to(x + dx, f - 2); c.line_to(x + dx, f - 10); c.stroke()
        c.set_line_cap(0)
        h["mom"] = mom(k_, "mom_wall", "fists", "unimpressed", look=(-1, 0.2), chin=True)   # in front of him
        return h
    office = dict(client="stand", sofia=True, mug=True, pam="hand_on_mug")
    return ("floor", dict(cast=cast, tag=True, clips=20, office=office)), dict(names=["don", "mom"], size="M", dy=-10,
                                                                            focus=("mom", "don"))


def out_35(k):
    """3.5's outside (S8r frame units): Mom in profile at the line's end, facing Don, her fists on her hips; Don behind
    her, leaning to look round her (his head bobbing past her shoulder)."""
    import da_s8r as r8
    import mom_fs as mfs
    shadow(k, 300, r8.FEET + 4, 70)
    shadow(k, 392, r8.FEET + 10, 70)
    dp.don(k, 392, r8.FEET + 8, 1.15, "stand", "confused", look=(-1, -0.2))
    mfs.mom(k, 300, r8.FEET + 4, 1.05, "fists", "unimpressed", (1, 0), chin=True)


def s35(k):
    """3.5 S8 M: inside, Pam sets HER mustard mug down on Father's side of the desk, in front of him, her hand still on
    it; Father looking at it. 27 Nov (two cold tests: the napkin's wipe read as "a note slipped in" by 5 of 5 viewers;
    Tomas: "bandom kita kadra"): a new shot, not a third napkin. The Client out (simplify); Sofía at the frame's edge."""
    import hand_lib_v4 as hl
    mug_at = (304, 676)                                        # under her own reaching hand (da_s8.pam_taking ends at
                                                               # ~(295, 650)): no second hand drawn (a hand apart, again)

    def draw(k_):
        h = s8_compose(k_, pam_in=True, mug=True, client=None, outside=out_35, mug_at=mug_at)
        h["mug"] = (mug_at[0], mug_at[1] - 20, 24)
        return h
    return None, crop(k, 1.9, 300, 610, draw)


def s41(k):
    """4.1 S6 M: Pam across the tape mid-step, the saucer on her palm (SAUCER_SUPPORT), the cup held out; Don's pinch
    reaching for it (PINCH). Mom sitting back down: in the scene, out of this frame. Through the glass, still: the
    Client and Father seated, her mug between them."""
    def cast(k_):
        h = {}
        x, f = MARKS["pam_cross"]
        shadow(k_, x, f + 2, 32)
        T = (x - 56, f - 112)                                 # the audit: the handover at chest height, clear of his face
        o = rig_hands(k_, lambda kk, a4: pm.pam(kk, x, f, SC["pam"], a4, "neutral", (-1, 0.4), mug=False), SC["pam"],
                      {-1: dict(T=T, pose="SAUCER_SUPPORT", out=-1, contact="saucer",
                                obj=lambda kk, P, w: dpr.cup_and_saucer_v2(kk, P[0], P[1] - 6, 0.8))},
                      sex="f", skin=FEMALE)
        h["pam"] = _head(o, "pam")
        h["cup"] = (T[0] - 8, T[1] - 18, 18)
        dx, df = MARKS["don_take"]; DON_FEET[0] = (dx, df)
        shadow(k_, dx, df + 2, 40)
        od = rig_hands(k_, lambda kk, a4: dp.don(kk, dx, df, SC["don"], a4, "pleased", (1, 0.2), hands=False), SC["don"],
                       {1: dict(T=(T[0] - 22, T[1] - 18), pose="PINCH", out=1)})
        h["don"] = _head(od, "don")
        return h
    office = dict(client="seated", sofia=True, mug=True)
    back = [lambda k_: {"mom": mom(k_, "mom_desk_s", "folded", "unimpressed", look=(-1, 0.2))}]
    return ("floor", dict(cast=cast, tag=True, clips=18, office=office, back=back)), dict(names=["don", "pam"], size="M",
                                                                            dy=-20, focus=("cup",))


def s42(k):
    """4.2 S1 W: Don at the street door preening in its glass (his reflection faint in it), a hand at his hair, his back
    to his office; behind him Pam crossing back to the office (her path dashed: layout notation); the robot working.
    27 Nov (the cold test, then Tomas: "paprastinam, maziau heroju"): Pam out of this shot. Wherever she stood behind him
    she read as "at the throne" (both viewers), and her hand reaching read as reaching for it; her slip is 4.3's (her
    hand on the office door's handle). This shot is Don alone, his back to everything, preening: he sees nothing."""
    def cast(k_):
        h = {}
        h["robot"] = robot(k_, (480, F + 64), tilt=0.25, look=(0, 1))
        x, f = MARKS["don_street"]; DON_FEET[0] = (x, f); s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "smug", (-1, -0.2), hands=False), s_,
                      {-1: dict(T=(x - 30 * s_, f - 330 * s_), pose="PALM", out=-1)})
        h["don"] = _head(o, "don")
        c = k_.c                                                # his reflection in the door's glass, faint
        hx, hy, r_ = h["don"]
        c.save(); c.rectangle(40, F - 360, 100, 360); c.clip()
        c.push_group(); dp.don(k_, 2 * 92 - x, f, s_, "stand", "smug", (1, -0.2)); c.pop_group_to_source(); c.paint_with_alpha(0.22)
        c.restore()
        return h
    return ("floor", dict(cast=cast, tag=True, clips=16)), dict(names=["don"], size="M", dy=-20,
                                                               focus=("don",))


def s43(k):
    """4.3 S5 M: Pam slips past Mom's desk side-on and small (hunched, elbows in); Mom knitting, eyes on it, not
    looking up. 27 Nov: Mom behind the counter (v2 drew her on its front), the knitting on its top at her hands, Pam
    on the floor in front, clear of Mom's silhouette."""
    mx, mf_ = MARKS["mom_desk_s"]

    def mom_back(k_):
        return {"mom": mom(k_, "mom_desk_s", "folded", "unimpressed", look=(0.2, 1.0))}

    def cast(k_):
        h = {}
        dpr.knitting_v2(k_, mx - 66, F - 190, 0.85)            # on the counter's top at her side (the cold test round:
        h["knit"] = (mx - 66, F - 180, 28)                     # in front of her it hid her face)
        px_, pf_ = mx + 96, F + 24                             # the cold test 27 Nov: "stands at the door"; now the
        shadow(k_, px_, pf_ + 2, 32)                           # sneak: hunched, elbows in, pitched toward the door,
        o = tilted(k_, px_, pf_, 0.16, lambda: rig_hands(      # her eyes on it, her hand at its handle
            k_, lambda kk, a4: pm.pam(kk, px_, pf_, SC["pam"], a4, "neutral", (1, -0.1), mug=False, lean=-10),
            SC["pam"], {1: dict(T=(px_ + 64, F - 176), pose="GRAB", out=1, reach=True)}, sex="f", skin=FEMALE))
        h["pam"] = _head(o, "pam")
        return h
    return ("floor", dict(cast=cast, tag=True, clips=15, back=[mom_back])), dict(names=["mom", "pam"], size="M", dy=0,
                                                                              focus=("mom", "knit"))


def s51(k):
    """5.1 S9 C: through the glass (the blinds' edge at the top, the tint kept): her mustard mug on Father's table.
    27 Nov (Tomas: A, and "paprastinam: maziau heroju, maziau detaliu"): only Father and the mug behind the glass (the
    Client and Sofía out of this shot); the room round the mug dimmed, the mug in a pool of light: the one thing to see."""
    def cast(k_):
        return {}
    office = dict(client=None, sofia=False, mug=True)
    mx, my = ds.WIN[0] + ds.WIN[2] * 0.5 + 34, ds.WIN[1] + ds.WIN[3] - 122
    cam = (mx - 18, my - 10, 4.4)                               # the mug in the middle; Father beside it, second

    def light(k_, cam_):
        fx, fy, z = cam_
        sx, sy = (mx - fx) * z + 270, (my + 4 - fy) * z + 480
        c = k_.c
        g = cairo.RadialGradient(sx, sy - 20, 20, sx, sy - 20, 190)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(0.3, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0.05, 0.04, 0.06, 0.68)
        c.set_source(g); c.paint()
        g = cairo.RadialGradient(sx, sy - 20, 0, sx, sy - 20, 90)
        g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.30); g.add_color_stop_rgba(1, 1, 0.95, 0.75, 0.0)
        c.set_source(g); c.paint()
    return ("floor", dict(cast=cast, tag=True, clips=14, office=office)), dict(cam=cam, names=[], size="C", focus=(),
                                                                            near=light)


def s52(k):
    """5.2 S3 MC: the pinky out, the saucer held out (the 5.2 still, da_s52, as built and gated in stage 3)."""
    import da_s52 as s52_
    import io
    surf = s52_.render(scale=1)
    k.c.set_source_surface(surf, 0, 0); k.c.paint()
    return None, {}


def s53(k):
    """5.3 S1 M: he charges at the glass (his mug's betrayal behind it) and his foot lands on the robot's clips: the
    whole body in the air, flat, the feet higher than the head, a fountain of clips from under the shoe; the tape just
    ahead (he lands and stops dead at it: 5.4). 27 Nov: three cold tests read the dead stop as a slip (Tomas: keep the
    slip, two moments); round 4 read the slip as a push (the throne's red lever at his hip, his fall back toward it).
    /grill-me: all in the air; the fountain; away from the throne, the glass and her mug ahead of him."""
    def cast(k_):
        h = {}
        x, f = MARKS["don_slip"]; DON_FEET[0] = (x, f); s_ = SC["don"]
        c = k_.c
        c.set_source_rgba(0.25, 0.18, 0.12, 0.55); c.set_line_cap(1)          # the run up: two skid streaks into the clips
        for dy_, w_ in ((-3, 4.0), (4, 3.0)):
            c.set_line_width(w_); c.new_path(); c.move_to(x - 150, f + dy_); c.line_to(x + 30, f + dy_); c.stroke()
        c.set_line_cap(0)
        old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
        try:
            for dx, dy, a_ in ((12, 2, 0.4), (26, 5, 2.0), (40, 1, -0.8), (20, -2, 1.2)):   # the pile he stepped on
                sd.paperclip(k_, x + dx, f + dy, CLIP_S, a_)
            import random
            r = random.Random(53)                              # the fountain: up and forward from under his shoe
            for i in range(14):
                a_ = r.uniform(-2.6, -0.9); d_ = r.uniform(40, 150)
                px, py = x + 30 + d_ * math.cos(a_) + 40, f - 6 + d_ * math.sin(a_)
                sd.paperclip(k_, px, py, CLIP_S * 1.3, r.uniform(-3, 3))
                if i % 2 == 0:
                    c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_cap(1)
                    c.new_path(); c.move_to(px - 8 * math.cos(a_), py - 8 * math.sin(a_))
                    c.line_to(px - 22 * math.cos(a_), py - 22 * math.sin(a_)); c.stroke(); c.set_line_cap(0)
        finally:
            sd.CLIPS_V2[0] = old
        c.set_source_rgba(0, 0, 0, 0.16); c.save(); c.translate(x - 10, f + 4); c.scale(120, 9); c.new_path()  # his shadow
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()                                               # under him, flat
        hip = (x - 10, f - 190 * s_)
        lift, ang = -20 * s_, -1.95                            # up off the floor; past flat: the feet above the head

        def body():
            c.save(); c.translate(0, -lift); c.translate(*hip); c.rotate(ang); c.translate(-hip[0], -hip[1])
            try:
                return rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "shock", (1, -0.6), knee=0.6, hands=False), s_,
                                 {-1: dict(T=(x - 140 * s_, f - 330 * s_), pose="PALM", out=-1, reach=True),
                                  1: dict(T=(x + 140 * s_, f - 330 * s_), pose="PALM", out=1, reach=True)})
            finally:
                c.restore()
        o = body()
        hx, hy, r_ = _head(o, "don")
        dx_, dy_ = hx - hip[0], hy - hip[1]
        h["don"] = (hip[0] + dx_ * math.cos(ang) - dy_ * math.sin(ang), hip[1] - lift + dx_ * math.sin(ang) + dy_ * math.cos(ang), r_)
        return h
    office = dict(client="seated", sofia=True, mug=True)
    return ("floor", dict(cast=cast, tag=True, clips=12, office=office)), dict(names=["don"], size="W", dy=-200, dx=70,
                                                                             focus=("don",), dutch=0.12)   # he loses control


def s54(k):
    """5.4 S7 M: Mom planted between him and the glass, fists on her hips, wide; Don small, shrunk back; the robot
    frozen, a clip held up in its pincer."""
    def cast(k_):
        h = {}
        o = rp.robot(k_, MARKS["robot_pile"][0] + 40, F + 64, SC["robot"], arms=((0, 0), (160, 20)), look=(-1, -0.4))
        shadow(k_, MARKS["robot_pile"][0] + 40, F + 66, 36)
        h["robot"] = _head(o, "robot")
        hx, hy = o["hands"][1]
        old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
        sd.paperclip(k_, hx + 4, hy - 8, CLIP_S * 1.6, 1.2); sd.CLIPS_V2[0] = old
        h["mom"] = mom(k_, "mom_wall", "fists", "glare", look=(-1, 0.2), chin=True)
        x, f = MARKS["don_wall"]; DON_FEET[0] = (x, f)
        shadow(k_, x, f + 2, 36)
        o2 = tilted(k_, x, f, 0.10, lambda: dp.don(k_, x, f, SC["don"] * 0.94, "stand", "confused", (1, -0.3), knee=0.0))
        h["don"] = _head(o2, "don")
        return h
    office = dict(client="seated", sofia=True, mug=True)
    return ("floor", dict(cast=cast, tag=True, clips=11, office=office)), dict(names=["don", "mom"], size="M", dy=-10,
                                                                            focus=("mom",))


# ---- Act III (27 Nov) -------------------------------------------------------------------------------------------------
# Built after Act II's six cold-test rounds (lessons 254-255): everyone on the floor or behind the counter, props in a hand
# or on a surface, no contact a viewer can take for a shove, a prop before a gesture, fewer people where it is hard.
def _page(k_, P, w, s=0.42, ang=0.0):
    dpr.minutes(k_, P[0], P[1] + 60 * s - 6, s, ang)          # held by its top edge at the hand's tip


def s61(k):
    """6.1 S6 M: Pam out of the office door (behind the counter's end), mid-step toward Don, the robot's printed page
    in her hand; Mom behind her desk, knitting, not looking up."""
    def mom_back(k_):
        return {"mom": mom(k_, "mom_desk_s", "folded", "unimpressed", look=(0.2, 1.0))}

    def cast(k_):
        x, f = 858, F + 26                                     # a step out of the door's gap (896-952), on the floor
        shadow(k_, x, f + 2, 32)
        o = tilted(k_, x, f, -0.08, lambda: rig_hands(         # mid-step, leaning to where she goes (screen-left)
            k_, lambda kk, a4: pm.pam(kk, x, f, SC["pam"], a4, "neutral", (-1, 0.2), mug=False), SC["pam"],
            {-1: dict(T=(x - 60 * SC["pam"] / 0.54, f - 190), pose="PINCH", out=-1, reach=True, contact="tip",
                      obj=lambda kk, P, w: _page(kk, P, w, 0.40, -0.1))}, sex="f", skin=FEMALE))
        return {"pam": _head(o, "pam")}
    return ("floor", dict(cast=cast, tag=True, clips=6, back=[mom_back])), dict(names=["pam"], size="M", focus=("pam",))


def _two_62(k_, page=True, don_face="confused", don_look=(1, 0.1), pam_face="neutral", don_pose=None):
    h = {}
    dx_, df_ = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]
    DON_FEET[0] = (dx_, df_)
    shadow(k_, dx_, df_ + 2, 40)
    if don_pose:
        h["don"] = _head(dp.don(k_, dx_, df_, SC["don"], don_pose, don_face, don_look), "don")
    else:
        h["don"] = _head(dp.don(k_, dx_, df_, SC["don"], "stand", don_face, don_look), "don")
    px, pf = 626, F + 60                                       # across the tape from him, a step back
    shadow(k_, px, pf + 2, 32)
    jobs = {-1: dict(T=(px - 70, pf - 170), pose="PINCH", out=-1, reach=True, contact="tip",
                     obj=lambda kk, P, w: _page(kk, P, w, 0.44, 0.05))} if page else {}
    o = rig_hands(k_, lambda kk, a4: pm.pam(kk, px, pf, SC["pam"], a4, pam_face, (-1, 0.3), mug=False), SC["pam"],
                  jobs, sex="f", skin=FEMALE)
    h["pam"] = _head(o, "pam")
    return h


def s62(k):
    """6.2 S3 M two-shot: Don eyes her, suspicious; she holds the page out to him across the tape ("I took notes.")."""
    def cast(k_):
        h = _two_62(k_, True, "confused", (1, 0.1))
        h["page"] = (626 - 70, F + 60 - 150, 30)
        return h
    return ("floor", dict(cast=cast, tag=True, clips=6)), dict(names=["don", "pam"], size="M", focus=("page",))


def s63(k):
    """6.3 Insert: the page whole, AGENDA: WITHOUT HIM; her fingers at its edge (the insert's owner, lesson 134)."""
    import hand_lib_v4 as hl
    def draw(k_):
        c = k_.c
        c.set_source_rgb(0.72, 0.63, 0.50); c.paint()          # the floor behind it, out of focus
        kit.cut(k_, [(-40, 700), (170, 640), (200, 760), (-40, 860)], (0.40, 0.24, 0.50), lw=3)   # her sleeve
        dpr.minutes(k_, 290, 470, 2.9, -0.04)
        hl.LWS[0] = 2.6
        hl.draw_lr(k_, "PINCH", 186, 640, (0.7, -0.7), 58, FEMALE, -1)                  # her fingers on its corner
        hl.LWS[0] = 1.0
        return {}
    return None, crop(k, 1.0, 270, 480, draw)


def s64(k):
    """6.4 S3 MC: suspicion -> delight: Don, thumbs up, grinning ("You're spying for me?")."""
    def cast(k_):
        x, f = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]; DON_FEET[0] = (x, f)
        shadow(k_, x, f + 2, 40)
        return {"don": _head(dp.don(k_, x, f, SC["don"], "thumbs", "grin", (1, 0.0)), "don")}
    return ("floor", dict(cast=cast, tag=True, clips=6)), dict(names=["don"], size="MC", dy=-30, focus=("don",))


def _pam_close(k_, mouth, face):
    px, pf = 626, F + 60
    shadow(k_, px, pf + 2, 32)
    o = pm.pam(k_, px, pf, SC["pam"], "stand", face, (0.7, -0.7), mug=False, mouth=mouth)   # her eyes up on the glass
                                                               # (the cold test: 6.6's man came "out of nowhere")
    return {"pam": _head(o, "pam")}


def s65(k):
    """6.5 C: Pam opens her mouth to correct him."""
    return ("floor", dict(cast=lambda k_: _pam_close(k_, "A", "doubt"), tag=True, clips=6)), dict(
        names=["pam"], size="C", focus=("pam",))


def s66(k):
    """6.6 S9 C: her view through the glass: the Client waiting, his blueprint rolled in his hands, looking at her.
    Simplified (Act II's 5.1): the Client and the roll alone behind the glass, the room dimmed round him."""
    office = dict(client="stand", sofia=False, roll="held", client_look=(0.6, 0.9))   # looking down out at her

    def light(k_, cam_):
        g = cairo.RadialGradient(270, 500, 60, 270, 500, 340)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(0.4, 0, 0, 0, 0.0)
        g.add_color_stop_rgba(1, 0.05, 0.04, 0.06, 0.55)
        k_.c.set_source(g); k_.c.paint()
    return ("floor", dict(cast=lambda k_: {}, tag=True, clips=6, office=office)), dict(names=["client"], size="C",
                                                                                     dy=40, focus=(), near=light)


def s67(k):
    """6.7 C: Pam closes her mouth (the peak: she chooses silence), held."""
    return ("floor", dict(cast=lambda k_: _pam_close(k_, "M", "neutral"), tag=True, clips=6)), dict(
        names=["pam"], size="C", focus=("pam",))


def s68(k):
    """6.8 S3 MC: Don pulls his headset mic to his mouth and whispers into it ("Keep infiltrating."), though Pam is half
    a metre away (the audit: the mic IS the joke; the cold test read the v1 pose as waving because the mic was not at
    his mouth). His hand holds the mic boom at his lips; Pam beside him."""
    def cast(k_):
        h = {}
        x, f = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]; DON_FEET[0] = (x, f); s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        o = dp.don(k_, x, f, s_, "cord", "smug", (1, 0.3))
        hx, hy, r_ = _head(o, "don")
        c = k_.c                                                # the boom pulled round to his lips, the mic at his mouth
        c.set_source_rgb(0.20, 0.20, 0.22); c.set_line_width(4.0 * s_ / 0.6); c.set_line_cap(1)
        c.new_path(); c.move_to(hx + r_ * 0.95, hy - r_ * 0.1)
        c.curve_to(hx + r_ * 1.05, hy + r_ * 0.5, hx + r_ * 0.6, hy + r_ * 0.62, hx + r_ * 0.28, hy + r_ * 0.55); c.stroke()
        c.set_line_cap(0)
        kit.ellipse(k_, hx + r_ * 0.24, hy + r_ * 0.55, r_ * 0.13, r_ * 0.10, (0.10, 0.10, 0.12), 6801, shadow=False, lw=1.2)
        h["don"] = (hx, hy, r_)
        px, pf = 604, F + 62
        shadow(k_, px, pf + 2, 32)
        h["pam"] = _head(pm.pam(k_, px, pf, SC["pam"], "stand", "neutral", (-1, 0.1), mug=False), "pam")
        return h
    return ("floor", dict(cast=cast, tag=True, clips=6)), dict(names=["don", "pam"], size="MC", focus=("don", "pam"))


def s71(k):
    """7.1 S4 C, low: his hand peels a long strip of his tape up off the floor (the strip the shot). Frame units,
    simplified to the floor, the tape, the peeled strip and his hand on its end."""
    import hand_lib_v4 as hl
    def draw(k_):
        c = k_.c
        c.set_source_rgb(0.72, 0.63, 0.50); c.paint()
        kit.cut(k_, [(130, 960), (250, 960), (330, -20), (250, -20)], pss.TAPE, shadow=False, lw=3)   # the tape, low
        kit.cut(k_, [(250, 960), (130, 960), (172, 620), (268, 620)], (0.72, 0.63, 0.50), shadow=False, lw=0)
        c.set_source_rgba(0, 0, 0, 0.12); c.rectangle(0, 0, W, H); c.new_path()                # its bare stripe:
        kit.cut(k_, [(250, 960), (130, 960), (172, 620), (268, 620)], (0.66, 0.57, 0.45), shadow=False, lw=1.5)  # peeled
        dpr.strip_v2(k_, (220, 625), (330, 300), 9.0, twist=0.6)                               # the peeled length
        kit.cut(k_, [(560, 40), (560, 200), (392, 312), (350, 262)], (0.98, 0.98, 0.96), lw=3)    # his sleeve, from the
        kit.cut(k_, [(560, -20), (560, 60), (380, 250), (330, 210)], (0.98, 0.98, 0.96), lw=3)    # top right
        hl.LWS[0] = 3.0
        hl.draw_lr(k_, "PINCH", 336, 284, (-0.55, 0.84), 70, MALE, 1)                       # his pinch on its end
        hl.LWS[0] = 1.0
        return {"strip": (290, 460, 60)}
    return None, crop(k, 1.0, 270, 480, draw)


def bow(k, x, f, s_, ang, draw, hip=150):
    """a bow at the waist, not a pitched body (lesson 255: a body pitched at the feet reads as a fall): the legs drawn
    upright below the hip line, the rest rotated about the hip above it. Returns (the rig's record, the head as seen)."""
    c = k.c
    hy = f - hip * s_
    c.save(); c.rectangle(-5000, hy, 10000, 5000); c.clip(); o = draw(); c.restore()       # the legs, upright
    c.save(); c.rectangle(-5000, -5000, 10000, hy + 5000 + 2); c.clip()
    c.translate(x, hy); c.rotate(ang); c.translate(-x, -hy); draw(); c.restore()             # bent at the hip
    hx, hy0, r_ = _head(o, "don")
    dx, dy = hx - x, hy0 - hy
    return o, (x + dx * math.cos(ang) - dy * math.sin(ang), hy + dx * math.sin(ang) + dy * math.cos(ang), r_)


def office_door_open(k, o, x0=896, w=56, top=470, knob_y=None, inward=False):
    """the office door (fs_set4: x 896-952, y 470-F) open by o (0..1): the dark gap, the leaf swung out toward us on
    its left hinge; returns the leaf's free edge (the handle) for a hand."""
    if o <= 0:
        return (x0 + w - 8, F - 170)
    kit.cut(k, [(x0, top), (x0 + w, top), (x0 + w, F), (x0, F)], (0.16, 0.12, 0.10), shadow=False, lw=2)   # the gap
    if inward:                                                 # opened into the office: only its edge shows, inside
        kit.cut(k, [(x0 + w - 10 * o, top + 4), (x0 + w, top), (x0 + w, F), (x0 + w - 10 * o, F - 4)], (0.42, 0.27, 0.16),
                shadow=False, lw=1.6)
        return (x0 + 4, F - 62 if knob_y is None else knob_y)    # her hand on the jamb, at her waist (higher read as a wave)
    ex = x0 - 44 * o                                           # the free edge comes out to the left, a little lower
    kit.cut(k, [(x0, top), (ex, top + 10 * o), (ex, F + 14 * o), (x0, F)], (0.42, 0.27, 0.16), lw=2.2)
    ky = (F - 170 if knob_y is None else knob_y) + 4 * o       # knob_y: opt-in (the motion test: at her hand's height)
    kit.ellipse(k, ex + 6, ky, 3.5, 3.5, (0.85, 0.72, 0.30), 7201, shadow=False, lw=1)       # its knob
    return (ex + 6, ky)


def s72(k):
    """7.2 S3 MC: the doorman, close: at his own line Don bows low at the waist, both arms rolled out toward the office
    door off screen, beaming; behind him the glass (a state). ("Approved."; the door's sound off screen.)
    28 Nov (Tomas: 1): the wide doorman (Don and Pam at opposite ends of the room) failed three mute tests and the
    tape gate four: no gesture read at that size. One clear action, close, like every beat that did read."""
    def cast(k_):
        f = F + 70; x = tape_x(f) - 46; s_ = SC["don"]; DON_FEET[0] = (x, f)   # his side, toes near the tape
        shadow(k_, x, f + 2, 40)
        o, head = bow(k_, x, f, s_, 0.40, lambda: rig_hands(
            k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "happy", (1, 0.3), hands=False), s_,
            {1: dict(T=(x + 190 * s_, f - 200 * s_), pose="PALM", out=1, reach=True),
             -1: dict(T=(x + 140 * s_, f - 160 * s_), pose="PALM", out=-1, reach=True)}))
        return {"don": head}
    office = dict(client="seated", sofia=True, roll="held")
    return ("floor", dict(cast=cast, tag=True, clips=1, office=office)), dict(names=["don"], size="MC", dy=-60,
                                                                            focus=("don",))


def s73(k):
    """7.3 S8 MC two-shot: the Client slides MY GARAGES across the desk to Pam; she takes it with both hands; Father
    nods once (not turning). The casters start outside (J-cut)."""
    def draw(k_):
        h = s8_compose(k_, pam_in=True, plan="open", client="over", outside=None)
        c = k_.c; c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)   # the cold test: "she lays out the
        for yy in (652, 668, 684):                                                   # map"; it slides from his side
            c.new_path(); c.move_to(112, yy); c.line_to(134, yy); c.stroke()
        c.set_line_cap(0)
        return h
    return None, crop(k, 1.35, 230, 630, draw)                    # the Client in frame (v1 showed only his arm)


def _local(pt, x, f, ang):
    """a world point into the frame of a body tilted by ang about its feet (x, f): where rig_hands must aim."""
    dx, dy = pt[0] - x, pt[1] - f
    return (x + dx * math.cos(-ang) - dy * math.sin(-ang), f + dx * math.sin(-ang) + dy * math.cos(-ang))


def s74(k):
    """7.4 S1 M: the tug. The throne rolled toward the gap in his line; Don, on his side, both arms straight out on the
    near armrest, pulls it back: he wants the chair. Past it, the robot (it crosses lines) reaches its pincer down for
    the last clip, dragged along under the caster: it wants the clip. ("NOT THE CHAIR!") Upright bodies, no pitch
    (lesson 255); through the glass, still: Pam with MY GARAGES, Father."""
    DX = 40
    def cast(k_):
        h = {}
        rx, rf = 690, F + 30                                   # past the gap, well clear of the chair (the cold test:
                                                               # near it, it "takes the chair to sell it")
        o = rp.robot(k_, rx, rf, SC["robot"], arms=((-40, -20), (8, 0)), look=(-1, 0.9), tilt=-0.35)   # bent to the floor,
        shadow(k_, rx, rf + 2, 36)                                                                     # its left arm down
        h["robot"] = _head(o, "robot")
        clip = (rx - 58, rf - 2)                                # the clip on the floor just under that pincer
        old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
        try:
            sd.paperclip(k_, clip[0], clip[1], CLIP_S * 2.6, 0.3)      # bigger: the thing it wants
        finally:
            sd.CLIPS_V2[0] = old
        c = k_.c; c.set_source_rgb(1, 0.95, 0.55); c.set_line_cap(1)            # a glint: the thing it wants
        for a_ in range(8):
            r0, r1 = (16, 30) if a_ % 2 == 0 else (14, 22)
            c.set_line_width(3.0 if a_ % 2 == 0 else 2.0)
            c.new_path(); c.move_to(clip[0] + r0 * math.cos(a_ * 0.785), clip[1] - 8 + r0 * math.sin(a_ * 0.785))
            c.line_to(clip[0] + r1 * math.cos(a_ * 0.785), clip[1] - 8 + r1 * math.sin(a_ * 0.785)); c.stroke()
        c.set_line_cap(0)
        h["clip"] = (clip[0], clip[1], 20)
        x, f = 350, F + 64; DON_FEET[0] = (x, f); s_ = SC["don"]   # his side, behind the chair's near side
        shadow(k_, x, f + 2, 44)
        arm = (TX + DX - 66 * TS, F - 150 * TS)                 # the throne's near (left) armrest after its roll
        o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "panic", (1, -0.1), hands=False), s_,
                      {1: dict(T=(arm[0] - 4, arm[1] - 4), pose="CLUTCH", out=1, reach=True),
                       -1: dict(T=(arm[0] - 10, arm[1] + 14), pose="CLUTCH", out=-1, reach=True)})
        h["don"] = _head(o, "don")
        return h
    office = dict(client="seated", sofia=False, pam="with_plan")
    return ("floor", dict(cast=cast, tag=False, clips=0, office=office, throne_dx=DX)), dict(
        names=["don", "robot"], size="M", focus=("don", "robot"))


def s81(k):
    """8.1 move: the pull-back's held end (S8 v11 itself: the deal inside, the tug in the glass)."""
    def draw(k_):
        img = cairo.ImageSurface.create_from_png(os.path.join(EP, "da_s8_final_v11.png"))
        c = k_.c; c.save(); c.scale(W / img.get_width(), H / img.get_height()); c.set_source_surface(img, 0, 0)
        c.paint(); c.restore()
        return {}
    return None, crop(k, 1.0, 270, 480, draw)


def s91(k):
    """9.1 move: the push's middle (the glass passing), da_push91.render_e at e 0.55 (v11)."""
    def draw(k_):
        import da_push91 as pu
        pu.V[0] = "v11"
        _, img = pu.setup(EP)
        surf = pu.render_e(0.55, img)
        c = k_.c; c.save(); c.scale(W / surf.get_width(), H / surf.get_height()); c.set_source_surface(surf, 0, 0)
        c.paint(); c.restore()
        return {}
    return None, crop(k, 1.0, 270, 480, draw)


# ---- the comedy micro-shots (27 Nov: the pre-animatic audit; Tomas: all seven, the clips stay A) --------------------------
def _twitch(c, x, y, s=1.0):
    c.set_source_rgb(*INK); c.set_line_width(2.2 * s); c.set_line_cap(1)
    for dx, dy, ex, ey in ((0, 0, 8, -10), (12, 2, 22, -6)):
        c.new_path(); c.move_to(x + dx * s, y + dy * s); c.line_to(x + ex * s, y + ey * s); c.stroke()
    c.set_line_cap(0)


def s13c(k):
    """1.3c S3 C: Don's eyes follow the polished shoe over his line, one eyebrow twitching (the robot let go: he is
    still on one leg, holding his shin)."""
    def cast(k_):
        x, f = MARKS["don_hop"]; DON_FEET[0] = (x, f); s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        o = dp.don(k_, x, f, s_, "stand", "shock", (1, 0.9), knee=1.0)
        hx, hy, r_ = _head(o, "don")
        _twitch(k_.c, hx + 6, hy - r_ * 0.62, 1.2)
        return {"don": (hx, hy, r_)}
    return ("floor", dict(cast=cast, tag=False, clips=0)), dict(names=["don"], size="C", dy=40, focus=("don",))


def s23b(k):
    """(cut 27 Nov, Tomas: frames 10-13 dragged; kept for the record, not in MAP) 2.3b S3 C: his smile frozen: a forced grin, chin up (the boss who is fine with it)."""
    def cast(k_):
        x, f = MARKS["don_counter"]; DON_FEET[0] = (x, f); s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        o = dp.don(k_, x, f, s_, "vest", "grin", (0, 0), chin=1)
        hx, hy, r_ = _head(o, "don")
        _twitch(k_.c, hx + r_ * 0.25, hy - r_ * 0.55, 1.2)            # the eye twitching over the grin
        return {"don": (hx, hy, r_)}
    return ("floor", dict(cast=cast, tag=True, clips=26)), dict(names=["don"], size="C", dy=-10, focus=("don",))


def s32b(k):
    """3.2b Insert: the two cups side by side on the counter: her big steaming mustard mug, his tiny white cup."""
    def draw(k_):
        c = k_.c
        c.set_source_rgb(*kit.WALL); c.paint()
        kit.cut(k_, [(-20, 560), (560, 560), (560, 980), (-20, 980)], (0.93, 0.89, 0.80), lw=3)     # the counter's top
        kit.cut(k_, [(-20, 560), (560, 560), (560, 600), (-20, 600)], (0.86, 0.82, 0.72), shadow=False, lw=2)
        ds.MUG_V2[0] = True
        ds.pam_mug(k_, 190, 720, 6.0)                                                          # hers: big
        c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(7); c.set_line_cap(1)                # its steam
        for dx in (-40, 0, 40):
            c.new_path(); c.move_to(190 + dx, 500)
            c.curve_to(170 + dx, 440, 215 + dx, 400, 190 + dx, 340); c.stroke()
        c.set_line_cap(0)
        dpr.cup_and_saucer_v2(k_, 420, 720, 2.2)                                                # his: tiny
        return {"mug": (190, 620, 90)}
    return None, crop(k, 1.0, 270, 480, draw)


def s34b(k):
    """3.4b S7 M: Mom the goalkeeper: Don steps to his left, she steps to her right with him, never looking at him;
    the two moves drawn as matching arcs (no contact, upright: lesson 255)."""
    def cast(k_):
        h = {}
        mx, mf = MARKS["mom_wall"][0] - 26, MARKS["mom_wall"][1]
        h["mom"] = mom(k_, (mx, mf), "fists", "unimpressed", look=(1, -0.6), chin=True)    # eyes away, up
        x, f = 470, F + 70; DON_FEET[0] = (x, f)
        shadow(k_, x, f + 2, 40)
        h["don"] = _head(dp.don(k_, x, f, SC["don"], "stand", "confused", (1, -0.2)), "don")
        c = k_.c; c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
        for cx_, cy_ in ((x + 6, f - 10), (mx + 6, mf - 10)):          # each one's step: the same arc, the same side
            c.new_path(); c.arc_negative(cx_ + 30, cy_, 34, -0.2, -2.6); c.stroke()
            c.new_path(); c.move_to(cx_ - 10, cy_ - 10); c.line_to(cx_ - 2, cy_ - 22); c.line_to(cx_ + 8, cy_ - 8); c.stroke()
        c.set_line_cap(0)
        return h
    office = dict(client="stand", sofia=True, mug=True, pam="hand_on_mug")
    return ("floor", dict(cast=cast, tag=True, clips=20, office=office)), dict(names=["don", "mom"], size="M",
                                                                            focus=("mom", "don"))


def s42b(k):
    """4.2b S1 C: at the street door's glass Don rehearses Father's hard face: chin up, lips flat; his reflection does it
    too (faint)."""
    def cast(k_):
        x, f = MARKS["don_street"]; DON_FEET[0] = (x, f); s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        o = dp.don(k_, x, f, s_, "stand", "neutral", (-1, 0.0), chin=1)
        c = k_.c
        c.save(); c.rectangle(40, F - 360, 100, 360); c.clip()
        c.push_group(); dp.don(k_, 2 * 92 - x, f, s_, "stand", "neutral", (1, 0.0), chin=1)
        c.pop_group_to_source(); c.paint_with_alpha(0.25); c.restore()
        return {"don": _head(o, "don")}
    return ("floor", dict(cast=cast, tag=True, clips=16)), dict(names=["don"], size="C", dx=-30, focus=("don",))


def s53b(k):
    """5.3b Insert: his cup flies; the coffee arcs out and lands in a splash right at the tape, not over it."""
    import da_hands as dh_
    def draw(k_):
        c = k_.c
        c.set_source_rgb(0.72, 0.63, 0.50); c.paint()
        kit.cut(k_, [(330, 960), (470, 960), (420, -20), (330, -20)], pss.TAPE, shadow=False, lw=3)   # the tape
        c.save(); c.translate(150, 300); c.rotate(-2.3); dh_.cup(k_, 0, 0, 3.6, 1); c.restore()       # the cup, tumbling
        c.set_source_rgb(0.30, 0.18, 0.10); c.set_line_width(14); c.set_line_cap(1)                  # the coffee's arc
        c.new_path(); c.move_to(190, 330); c.curve_to(270, 330, 310, 470, 318, 600); c.stroke()
        c.set_line_cap(0)
        kit.ellipse(k_, 300, 640, 70, 22, (0.30, 0.18, 0.10), 5301, shadow=False, lw=2)              # the splash, on his side
        for dx, dy, r_ in ((-60, -30, 8), (40, -40, 7), (-20, -60, 6), (70, -10, 5)):
            kit.ellipse(k_, 300 + dx, 640 + dy, r_, r_, (0.30, 0.18, 0.10), 5302 + dx, shadow=False, lw=1.4)
        c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)                              # the cup's spin
        for r_ in (60, 74):
            c.new_path(); c.arc(150, 300, r_, 3.6, 4.6); c.stroke()
        c.set_line_cap(0)
        return {"splash": (300, 640, 70)}
    return None, crop(k, 1.0, 270, 480, draw)


def s68b(k):
    """6.8b C: Pam looks at his headset mic, then at him (half a metre away): the look at the mic is the key frame."""
    def cast(k_):
        px, pf = 604, F + 60
        shadow(k_, px, pf + 2, 32)
        return {"pam": _head(pm.pam(k_, px, pf, SC["pam"], "stand", "doubt", (-1, -0.5), mug=False), "pam")}
    return ("floor", dict(cast=cast, tag=True, clips=6)), dict(names=["pam"], size="C", focus=("pam",))


MAP = {"3.1": s31, "3.2": s32, "3.3": s33, "3.4": s34, "3.5": s35, "4.1": s41, "4.2": s42, "4.3": s43, "5.1": s51,
       "5.2": s52, "5.3": s53, "5.4": s54, "1.1": s11, "1.2": s12, "1.3": s13, "1.3b": s13b, "1.4": s14, "1.5": s15, "2.1": s21, "2.2": s22, "2.3": s23,
       "2.4": s24, "6.1": s61, "6.2": s62, "6.3": s63, "6.4": s64, "6.5": s65, "6.6": s66, "6.7": s67, "6.8": s68,
       "7.2": s72, "7.3": s73, "7.4": s74, "8.1": s81, "9.1": s91,
       "1.3c": s13c, "3.2b": s32b, "4.2b": s42b, "5.3b": s53b, "6.8b": s68b}
ACTS = {3: ["6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.8b", "7.2", "7.3", "7.4", "8.1", "9.1"],
        1: ["1.1", "1.2", "1.3", "1.3c", "1.3b", "1.4", "1.5", "2.1", "2.2", "2.3", "2.4"],
        2: ["3.1", "3.2", "3.2b", "3.3", "3.4", "3.5", "4.1", "4.2", "4.2b", "4.3", "5.1", "5.2", "5.3", "5.3b",
            "5.4"]}
KNOWN = {("1.5", "REACH a hand at (408, 800) past its arm's reach (117 > 57)"): "approved Act I frame (Tomas 27 Nov); found by the round-3 gate, the hand short of the roll: left for Tomas to decide"}
FOCUS_MIN = 28          # px at 540, the radius of a story prop in focus (the audit 27 Nov: the mugs too small)
FACES_N = ("don", "pam", "mom", "sofia", "father", "client", "robot")
POSE_STATE = {"3.1": "library", "3.2": "library", "3.4": "tilted (feint)", "3.5": "library", "4.1": "library",
              "4.2": "library", "5.3": "library + tilt", "5.4": "rig (fists)","2.2": "drawn feet (rig colours)", "1.4": "rig + library hands", "1.3": "drawn legs (rig parts), near", "1.1": "locked", "1.2": "library", "1.5": "library", "2.3": "library", "2.4": "library",
              }      # "stand-in": a placeholder pose (the audit: green OK must not hide it)
FEET_IN = {"3.4": ["don"], "5.3": ["don"]}   # shots whose action is in the feet: they stay in frame
MUST = {"4.2": ["don"], "4.1": ["don", "pam"], "3.3": ["pam", "client"], "4.3": ["mom", "pam"], "5.4": ["mom", "don"]}
MIN_SIGN = 5          # px at 540: a text shorter than this is a smudge at 270 (the sign-size note, plan v2), not a sign


# ---- rendering and checks --------------------------------------------------------------------------------------------------
class TextRec(cairo.Context):
    """keeps every text shown (in device units) for uz_check.check_signs (ps_scenes.TextRec, copied)."""
    def __new__(cls, surf):
        return super().__new__(cls, surf)

    def __init__(self, surf):
        self.texts = []

    def show_text(self, s):
        x, y = self.get_current_point()
        e = self.text_extents(s)
        pts = [self.user_to_device(x + e.x_bearing + dx, y + e.y_bearing + dy) for dx in (0, e.width) for dy in (0, e.height)]
        self.texts.append(dict(text=s, bbox=(min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts),
                                              max(p[1] for p in pts)), clip=(-1e9, -1e9, 1e9, 1e9)))
        return super().show_text(s)


_FACE_SEEN = {}
_DON0, _PAM0 = dp.don, pm.pam                                  # the rigs themselves (the guard wraps them while drawing)


def _face_px(rig, face):
    """(28 Nov: a scratch drawing: the hand gate paused. It used to run the first time a face was asked, in the middle of
    a shot's draw, inside rig_hands' hand swap: that drawing's hands came out wrong (the scene 1 gate, 1.2). The
    guard now measures every face before drawing: face_guard.__enter__.)"""
    import da_hand_gate as g_
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 200, 260); c = cairo.Context(surf); c.set_source_rgb(1, 1, 1); c.paint()
    k = Ctx(c, 0)
    with g_.paused():
        if rig == "don":
            _DON0(k, 100, 250, 0.6, "stand", face)
        else:
            _PAM0(k, 100, 250, 0.54, "stand", face, mug=False)
    surf.flush()
    return bytes(surf.get_data())


def face_known(rig, face):
    """a face name the rig really draws: its drawing differs from a name no rig has (an unknown name falls back without
    an error: the audit's "Don has one face", 27 Nov)."""
    key = (rig, face)
    if key not in _FACE_SEEN:
        _FACE_SEEN[key] = face in ("neutral",) or _face_px(rig, face) != _face_px(rig, "zz_no_such_face")
    return _FACE_SEEN[key]


FACES_DON = ("neutral", "confused", "pleased", "grin", "happy", "panic", "shock", "smug", "squint", "hard")   # measured 27 Nov
FACES_PAM_WARM = ("neutral", "doubt", "peer", "quiet", "hopeful", "pressed", "shock", "smile", "worried", "sad")
FACES_NOTE = "squint draws shut eyes: it reads as asleep (lesson: eyes open for 'approves without looking')"


class face_guard(object):
    """while drawing: every face asked of Don's and Pam's rigs is logged; render() fails on one they don't have."""
    def __enter__(self):
        self.bad = []
        for f_ in FACES_DON:                                   # measured now, never in the middle of a shot's draw
            face_known("don", f_)
        for f_ in FACES_PAM_WARM:
            face_known("pam", f_)
        self.d, self.p = dp.don, pm.pam
        guard = self

        def don_(k, x, feet, s=0.60, pose="stand", face="neutral", *a, **kw):
            if not face_known("don", face):
                guard.bad.append("FACE: Don has no face %r (drawn as his default)" % face)
            return guard.d(k, x, feet, s, pose, face, *a, **kw)

        def pam_(k, x, feet, s=0.54, pose="stand", face="neutral", *a, **kw):
            if not face_known("pam", face):
                guard.bad.append("FACE: Pam has no face %r (drawn as her default)" % face)
            return guard.p(k, x, feet, s, pose, face, *a, **kw)
        dp.don, pm.pam = don_, pam_
        return self

    def __exit__(self, *e):
        dp.don, pm.pam = self.d, self.p


def render(sid):
    """-> (surface 540x960, faults); the people's name badges off throughout (the robot's HR kept)."""
    with ds.no_badges(), don_legs(), sofia_lib_hands(), face_guard() as fg:
        surf, msgs = _render(sid)
    return surf, msgs + sorted(set(fg.bad))


def _render(sid):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = TextRec(surf); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    spec, fr = MAP[sid](Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)), 0))   # a dry pass: the faces
    if spec is None:                                            # frame units (S8r file, S8): drawn as they are
        c2 = TextRec(surf); k2 = Ctx(c2, 0)
        _, heads = MAP[sid](k2)
        f = dict(cam=(270, 480, 1.0), heads=heads, scene=dict(text=[]), bubbles=[], shot=sid)
        return surf, uz.check_scale(f, sc.STAGE[sid]["cast"]) if heads else []
    kind, args = spec
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
    heads0 = floor_world(Ctx(cairo.Context(tmp), 0), **args)
    names = fr.get("frame_on") or (list(fr["names"]) + [n for n in fr.get("focus", ()) if n not in fr["names"] and n != "near"])
    base = fr.get("cam") or cam_on(heads0, names, fr["size"], fr.get("dy", 0.0), fr.get("dx", 0.0))
    best = None
    cands = sorted(((ox, oy, zm) for zm in (1.0, 1.12, 1.25, 1.4, 1.6, 1.8, 2.0, 2.2) for ox in range(-90, 91, 15) for oy in range(-60, 61, 15)),
                   key=lambda o: (o[2], abs(o[0]) + abs(o[1])))
    for ox, oy, zm in cands:
        cam = (base[0] + ox / base[2], base[1] + oy / base[2], base[2] * zm)   # offsets in frame px; a closer framing last
        surf, msgs = _draw(sid, args, fr, cam)
        framing = [m for m in msgs if not m.startswith(GROUND_KINDS)]   # the ground's faults: no camera fixes them
        if best is None:
            best = (surf, msgs)
        if not framing:
            best = (surf, msgs); break
    return best


def _draw(sid, args, fr, cam):
    DON_FEET[0] = None
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = TextRec(surf); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save()
    if fr.get("dutch"):                                        # a tilted camera (5.3, the audit: once, when he loses it)
        c.translate(270, 480); c.rotate(fr["dutch"]); c.scale(1.12, 1.12); c.translate(-270, -480)
    sbv.view(c, *cam); ds._floor_on(c)
    with ground_log():
        heads = floor_world(k, **args)
    c.restore()
    gmsgs = ground_faults(sid)
    if fr.get("near"):
        fr["near"](k, cam)
    fx, fy, z = cam
    text = []
    for t in c.texts:
        b = t["bbox"]
        if b[3] - b[1] < MIN_SIGN:                             # can't be read: can't be misread
            continue
        text.append(dict(text=t["text"], bbox=((b[0] - 270) / z + fx, (b[1] - 480) / z + fy, (b[2] - 270) / z + fx,
                                               (b[3] - 480) / z + fy), clip=t["clip"]))
    f = dict(cam=cam, heads={n: v for n, v in heads.items() if n != "tag"}, scene=dict(text=text), bubbles=[], shot=sid)
    msgs = uz.check_signs(f) + uz.check_scale(f, sc.STAGE[sid]["cast"]) + mirror(sid, cam, heads)
    msgs += in_frame(sid, f) + covered(surf, c.texts, args, cam) + focus_check(fr, heads, cam) + gmsgs
    return surf, [m for m in msgs if (sid, m.split(":")[0]) not in KNOWN]


def focus_check(fr, heads, cam):
    """the shot's one centre of attention (the audit, 27 Nov: "one dominant element per frame"): each named item whole in
    the frame and their middle in the frame's middle band (x 60-480, y 150-700); "near": a frame-unit layer, not
    measured here."""
    names = [n for n in fr.get("focus", ()) if n != "near"]
    if not names:
        return []
    fx, fy, z = cam
    pts = []
    for n in names:
        if n not in heads:
            return ["FOCUS: %s not drawn" % n]
        x, y, r = heads[n]
        X, Y, Rr = 270 + (x - fx) * z, 480 + (y - fy) * z, r * z
        if not (Rr <= X <= W - Rr and 96 + Rr <= Y <= 960 - Rr):
            return ["FOCUS: %s out of the frame (%d, %d)" % (n, X, Y)]
        if n not in FACES_N and Rr < FOCUS_MIN:                # a story prop big enough to read at 270 (14 px there)
            return ["FOCUS: %s too small (%d px, wants %d)" % (n, Rr, FOCUS_MIN)]
        if n not in FACES_N and (Y > cf.BOTTOM or (X > cf.RAIL[0] and cf.RAIL[1] < Y < cf.RAIL[2])):
            return ["PROP: %s in the apps' zones (%d, %d)" % (n, X, Y)]
        pts.append((X, Y))
    mx = sum(p[0] for p in pts) / len(pts); my = sum(p[1] for p in pts) / len(pts)
    if not (60 <= mx <= 480 and 150 <= my <= 700):
        return ["FOCUS: the centre of attention off the middle (%d, %d)" % (mx, my)]
    return []


def in_frame(sid, f):
    """every story face of the shot (STAGE's cast, the floor's own people) inside the frame, under the top bar."""
    out = []
    faces = uz.faces(f)
    for n in (MUST.get(sid) or sc.STAGE[sid]["cast"]):        # who must be in frame (not everyone in the scene)
        if n not in faces:
            continue
        x, y, r = faces[n]
        if not (r <= x <= W - r and 96 + r <= y <= H):
            out.append("FRAME: %s's face out of the frame (%d, %d)" % (n, x, y))
    fx, fy, z = f["cam"]
    for n in FEET_IN.get(sid, ()):                             # the audit 27 Nov (5.3): the stop is in his feet
        for pn, x, ft, s_, b in GROUND["people"]:
            if pn == n and not b:
                sx, sy = (x - fx) * z + 270, (ft - fy) * z + 480
                if not (60 <= sx <= W - 60 and sy <= H - 40):          # the whole shoe, not its edge
                    out.append("FEET: %s's feet out of the frame (%d, %d): the action is in them" % (n, sx, sy))
                break
    return out


def covered(surf, texts, args, cam):
    """ps_scenes.covered (lesson 295, copied): a set sign partly hidden by someone in front of it reads as another word
    ("ON" for DON). The same frame without the cast: a sign whose pixels differ over 10-88 % of its box is partly
    covered."""
    import numpy as np
    bare = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    cb = TextRec(bare); kb = Ctx(cb, 0); cb.set_source_rgb(*kit.WALL); cb.paint()
    cb.save(); sbv.view(cb, *cam); ds._floor_on(cb)
    floor_world(kb, **dict(args, cast=lambda k_: {}))
    cb.restore()
    surf.flush(); bare.flush()
    A = np.ndarray((H, W, 4), np.uint8, surf.get_data()).astype(int)
    B = np.ndarray((H, W, 4), np.uint8, bare.get_data()).astype(int)
    room = {(t["text"], tuple(round(v) for v in t["bbox"])) for t in cb.texts}
    out = []
    for t in texts:
        if (t["text"], tuple(round(v) for v in t["bbox"])) not in room:
            continue
        x0, y0, x1, y1 = [int(round(v)) for v in t["bbox"]]
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
        if x1 - x0 < 4 or y1 - y0 < MIN_SIGN:
            continue
        d = (np.abs(A[y0:y1, x0:x1] - B[y0:y1, x0:x1])[..., :3].max(axis=2) > 24).mean()
        if 0.04 < d < 0.88:                                    # 1.3: one letter under a leg ("CLIEN") is 6 %
            out.append("SIGN partly covered: %r (%d %%)" % (t["text"], round(100 * d)))
    return out


def mirror(sid, cam, heads):
    """the mirror rule on the drawn frame: from the street side, Don's head left of the tape (at his feet' depth)."""
    want = sc.STAGE[sid]["don_side"]
    if "don" not in heads or want is None:
        return []
    fx, fy, z = cam
    x = DON_FEET[0][0] if DON_FEET[0] else heads["don"][0]    # his feet: a body pitched over the line is still his side
    feet = DON_FEET[0][1] if DON_FEET[0] else F
    side = "L" if x < tape_x(feet) else "R"                     # the tape at his own depth (it splays to the camera)
    return [] if side == want else ["MIRROR: Don's head at x %d, %s of the tape; the rule wants %s" % (x, side, want)]


def zones(c):
    c.set_source_rgb(0.85, 0.1, 0.1); c.set_line_width(1.5); c.set_dash([6, 4])
    c.move_to(0, cf.BOTTOM); c.line_to(W, cf.BOTTOM); c.stroke()
    c.rectangle(cf.RAIL[0], cf.RAIL[1], W - cf.RAIL[0], cf.RAIL[2] - cf.RAIL[1]); c.stroke(); c.set_dash([])
    c.set_source_rgba(0.1, 0.1, 0.1, 0.18); c.rectangle(0, 0, W, 96); c.fill()


def sheet(act, out_dir=EP):
    ids = ACTS[act]
    tm = {s["shot"]: s for s in sc.timing()["shots"]}
    cols, tw, th = 4, 270, 480
    nr = (len(ids) + cols - 1) // cols
    SW, SH = 30 + cols * (tw + 30), 110 + nr * (th + 140)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW, SH); c = cairo.Context(s)
    c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_font_size(22); c.set_source_rgb(*INK); c.move_to(30, 44)
    c.show_text("THE DOUBLE AGENT · layouts v1 · act %d" % act)
    c.select_font_face("Inter", 0, 0); c.set_font_size(13); c.set_source_rgb(0.3, 0.3, 0.3); c.move_to(30, 70)
    c.show_text("generated by da_layouts.py from da_scenes.py · each frame at 270 · red: the apps' zones · key poses only")
    fails = []
    for i, sid in enumerate(ids):
        surf, msgs = render(sid)
        zones(cairo.Context(surf))
        x = 30 + (i % cols) * (tw + 30); y = 90 + (i // cols) * (th + 140)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(surf, 0, 0); c.paint(); c.restore()
        t = sc.TEXT[sid]; st_ = sc.STAGE[sid]
        c.select_font_face("Inter", 0, 1); c.set_font_size(12); c.set_source_rgb(*INK)
        head = "%s  %s · %.1f s" % (sid, t["setup"], tm[sid]["len"])
        c.move_to(x, y + th + 18); c.show_text(head)
        c.select_font_face("Inter", 0, 0)
        c.set_source_rgb(0.55, 0.25, 0.05); c.move_to(x, y + th + 33)
        c.show_text(("sees first: " + sc.STAGE[sid].get("focus", "?"))[:46]); c.set_source_rgb(*INK)
        for j, ln in enumerate(textwrap.wrap(t["picture"].replace("**", ""), 44)[:2]):
            c.move_to(x, y + th + 49 + j * 15); c.show_text(ln)
        if st_["other"]:
            c.set_source_rgb(0.15, 0.40, 0.45); c.move_to(x, y + th + 82); c.show_text(st_["other"][:46])
        if t["line"] not in ("—", ""):
            c.set_source_rgb(0.2, 0.3, 0.6); c.move_to(x, y + th + 98); c.show_text(t["line"].replace("**", "")[:46])
        ok = not msgs
        c.set_source_rgb(*((0.1, 0.45, 0.2) if ok else (0.8, 0.1, 0.1))); c.move_to(x, y + th + 116)
        c.show_text(("checks pass · pose: %s" % POSE_STATE.get(sid, "stand-in")) if ok
                    else ("FAIL: " + "; ".join(m.split(":")[0] for m in msgs))[:60])
        fails += [(sid, m) for m in msgs]
    out = os.path.join(out_dir, "da_layout_act%d_v1.png" % act)
    s.write_to_png(out)
    from PIL import Image
    im = Image.open(out); im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(out.replace(".png", "_feed.png"))
    print("wrote", out)
    return fails


def main(args):
    assert ground_selftest(), "the ground gate passes a planted fault"
    acts = [int(a) for a in args if a.isdigit()] or [1]
    out = ([a for a in args if not a.isdigit()] or [EP])[0]
    for sid, fn in sorted(MAP.items()):                       # lesson 109: the map, printed
        print("  %-5s -> %s" % (sid, fn.__name__))
    assert all(MAP[s].__name__ == "s" + s.replace(".", "") for s in MAP), "the map points a shot at another's drawing"
    fails = []
    for a in acts:
        fails += sheet(a, out)
    for sid, m in fails:
        print("FAIL %-5s %s" % (sid, m))
    return not fails


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:]) else 1)
