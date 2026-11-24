"""THE OFFER (episode 13), stage 7: the animation, scene by scene (decided 22 Nov: scene 1 first, reviewed with sound
and cold viewers, then the rest). Drawn from the scene file (of_scenes.py) at 15 drawings a second on the 30 fps
camera; every drawing goes through the scene file's checks (signs, scale, dead zones, tails); bubbles live as long as
their line (lesson 362), lips follow the take's loudness.

  python3 of_film.py 1        ->  ../the-offer/of_scene1_v1_540.mp4 (with the scene's stretch of of_sound_v1.wav)
                                  /tmp/of_film/s1_sheet4.png (4 fps) for the cold viewers
1080 masters are rendered in /tmp only (series rule: 540 copies are committed)."""
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf
import of_scenes as sc
import of_cast as oc
import of_motion as om

TMP = "/tmp/of_film"
VER = {1: 41, 2: 41, 3: 41, 4: 41, 5: 41}
SOUND = "of_sound_v19.wav"                                   # v8: re-keyed to timing v4                                   # each scene's current version (new versions, new files)
DPS, FPS = 15, 30
LEAD = 0.15
TAKES = os.path.join(sc.HERE, "of_voices", "takes")


def ease(u):
    return om.ease(u)


# --- what moves in each shot: id -> f(t, L) -> (state overrides, pose overrides) ----------------------------------------
def still(t, L):
    return {}, {}


def s02(t, L):                                             # the headlights cross the wall; his hand finds the wrench
    return dict(sweep_x=-260 + 420 * ease(t / 0.6), reach=ease((t - 0.35) / 0.45)), {}       # v2: a longer reach


def s03(t, L):                                             # two pairs of black shoes, together; they step apart
    u = ease((t - 0.30) / 0.35)
    return dict(moved=dict(g1=(150 - 46 * u, 856), g2=(172 + 46 * u, 856))), {}


def s11(t, L):                                             # the finger goes to 7; then he looks round at the real bay
    turn = 0.9 * ease((t - 0.50) / 0.30)                  # v2 (timing v10, 1.0 s): the look round, earlier
    return {}, dict(g2=dict(targets=["bay7_point"], point=ease(t / 0.40) > 0.5, turn=turn))


def _T(sid, t):
    return sc._timing()[sid]["start"] + t


LAND_AT = ("1.3", 0.50)                                    # the burning 7 lands by his boot
FLOOR_BURN = 4.6                                           # and burns out in this long


def _floor(sid, t):
    p = (_T(sid, t) - _T(*LAND_AT)) / FLOOR_BURN
    return None if p < 0 else min(1.0, p)


def s12(t, L):                                             # v2 (23 Nov): the lighter; CLICK; the 7 CATCHES and the fire climbs
    up = ease(t / 0.30)
    lit = t > 0.35
    import of_set as gs
    bx, by = gs.bay7()
    hand = (bx + 2, by + 18 + sc.LIGHTER_LIFT + 60 * (1 - up))   # v11: the smaller flame still licks the corner of 7
    f = ease((t - 0.42) / 0.80)
    return dict(burn=0.7 * f, fire=f, fire_t=_T("1.2", t)), dict(g2=dict(targets_xy=[hand], lighter=1.0 if lit else 0.0,
                                                                          lid=1.0 if t > 0.25 else 0.0))


def s13(t, L):                                             # v2: he TEARS the burning 7 off and flings it over the car: it lands by
    import of_set as gs                                    # the boot (the boot doesn't move); then the creeper rolls out past it;
    bx, by = gs.bay7()                                     # he sits up, looks at the fire by his feet, then at his watch
    ft = _T("1.3", t)
    fly = None if t < 0.15 else min(1.0, (t - 0.15) / 0.35)
    st = dict(burn=0.7 if t < 0.15 else 0.8, fire=1.0 if t < 0.15 else 0.25, fire_t=ft,
              sheet_fly=fly if (fly is not None and fly < 1.0) else None, sheet_floor=_floor("1.3", t))
    g2 = dict(targets_xy=[(bx - 6, by - 20) if t < 0.15 else (bx + 30, by - 70)], lighter=1.0, lid=1.0)
    gu_ = ease((t - 0.5) / 0.3)                             # v3 (cold test v37, 3 of 3 "a statue"): bodyguard 1's head follows the creeper out
    g1 = dict(turn=0.6 * gu_, look_down=12 * gu_)
    if t < 0.88:
        out = gs.LEGS_OUT * ease((t - 0.55) / 0.30)
        return dict(st, _cast=("father", "g1", "g2"), sit=False, legs_out_v=out), dict(g2=g2, g1=g1)
    look = (0.6, 1.0) if t < 1.10 else (0.9, 2.0)              # at the fire by his feet, then down at the watch
    return st, dict(g2=g2, g1=g1, client=dict(kind="sit", look=look, face="glance" if t >= 1.10 else "bored"))


SMOTHER_AT = (2.75, 3.15)                                  # v3 (23 Nov, decided): after the line, the rag on the fire


def s14(t, L):                                             # "Burn them...": he wipes his hands on the rag as he talks; then,
    import of_set as gs                                    # not looking, he presses the rag down on the burning 7 and takes it
    a, b = SMOTHER_AT
    gs.SMOTHER[0] = 0.0
    cl = dict(kind="sit", look=(-1, -0.2), wipe=math.sin(t * 2 * math.pi * 0.9))
    fl = _floor("1.4", min(t, a))
    if t >= a:
        u = ease((t - a) / (b - a))
        sx, sy = gs.SHEET_LAND
        cl["hands_at"] = (sx - 4, sy - 10 + 6 * (1 - u)) if t < b + 0.2 else (sx - 30 * min(1, (t - b - 0.2) / 0.2) - 4, sy - 40)
        gs.SMOTHER[0] = u if t < b else 1.0
        if t >= b:
            fl = None
    return dict(sheet_floor=fl, fire_t=_T("1.4", t), burn=0.8), dict(client=cl)


# --- scene 3, The Offer ----------------------------------------------------------------------------------------------
def _work(t):
    return math.sin(t * 2 * math.pi * 1.3)


CUT_21 = 1.3                                              # v2 (23 Nov, cold tests 3 of 3: "4 s of one frame, I'd scroll"):


def s21(t, L):                                             # v3 (24 Nov, cold test v31: 'My son says...' drags, 4 s; decided): THREE pictures over the one
    cl = dict(client=dict(kind="bent", work=_work(t)))     # line (lesson 197): Father close (the guard behind him adjusts his
    fx_, ff_ = sc.BLOCK[3]["father"]                       # sunglasses), the two-shot (Father's open hand),
    gu = ease((t - 0.35) / 0.3) - ease((t - 3.2) / 0.3) + 0.12 * math.sin(t * 5.0) * (1 if 0.7 < t < 3.0 else 0)   # v4: his open hand up through the whole line
    gest = dict(targets_xy=[(fx_ + 34 + 30 * gu, ff_ - 96 - 78 * gu)]) if gu > 0.02 else {}
    if t < CUT_21:
        return dict(_cam=sc.FATHER_LAMP, _cast=("father", "g2")), dict(father=dict(face="hard", look=(1, 0), lean=0.03 * gu, **gest), **cl)
    if t < 2.55:
        return {}, dict(father=dict(face="hard", look=(1, 0), **gest), **cl)
    return dict(_cam=sc.FATHER_LAMP, _cast=("father", "g2")), dict(father=dict(face="brow" if t > 3.55 else "hard", look=(1, 0), lean=0.03 * gu, **gest), **cl)


def s22(t, L):
    return {}, dict(client=dict(kind="bent", work=_work(t + 0.4)))


def s23b(t, L):                                            # his eyes go from the lamp, up there, to the Client: he decides
    u = ease((t - 0.25) / 0.45)
    return {}, dict(father=dict(look=(1, -0.9 + 1.1 * u)))


def s25(t, L):                                             # v2 (23 Nov audit, decided): he straightens; "Without him." with a
    u = ease(t / 0.3)                                      # thumb jerked over his shoulder at the door (the hand at his neck
    return {}, dict(client=dict(kind="thumb", thumb_u=u, look=(-1, 0),   # read as scratching, or a call)
                                face="bored"))


def s27(t, L):                                             # the phone out of the top pocket, turned round
    return {}, dict(client=dict(kind="pocket", pocket_u=min(1.0, t / 0.55)))   # v5: pocket, wipe, out


GAG_AT = 1.1                                               # v2 (23 Nov, decided: the mid-film gag): after "Done.", CUT to


def s28c(t, L):                                            # v4 (24 Nov, cold test v31: the PAM gag read as "proof of the deal", 0 of 3 as a joke; decided
    return {}, dict(father=dict(face="low" if 0.25 < t < 0.7 else "hard"))   # CUT): "Done." and one nod, then straight to the key


PAM_GAG_CAM = (166, 742, 3.4)


def s28d(t, L):                                            # SLAM
    T0 = 0.3                                               # v3 (24 Nov, cold test v30: 0 of 3 saw it; at 10 fps it fell for 0.4 s with a small
    u = ease((t - T0) / 0.09)                              # shake): UP with his hand on it for 0.3 s, down in 0.09 s, and the frame JOLTS
    return dict(anim=True, bonnet=1.0 - u, shake=0 if t < T0 + 0.09 else 14 * math.exp(-(t - T0 - 0.09) * 11) * math.sin(t * 110)), \
        dict(client=dict(kind="slam", slam_b=1.0 - u))


def s28e(t, L):                                            # the key turns; a cough; it runs
    ku = ease(t / 0.3)
    run = 0.0 if t < 0.45 else (4 if t < 0.65 else 1.6) * math.sin(t * 2 * math.pi * 11)
    return dict(key_u=ku, run=run, shake=0.6 * run), {}


STEP_T = 0.5                                               # v2 (23 Nov, decided): a step every 0.5 s, feet planted


def s29(t, L):                                             # on his way to the door: real steps. Each step: the back foot lifts and
    import dh_cast as dc                                   # swings past; the body moves only while a foot is in the air; the
    n = int(t / STEP_T); ph = (t % STEP_T) / STEP_T         # planted foot does not slide (it moves with the body by 0)
    stride = 26.0
    x = 280 - stride * (n + ease(min(1.0, ph / 0.7)))
    lift = 10 * math.sin(math.pi * min(1.0, ph / 0.7))
    a = -stride / 2 + stride * ease(min(1.0, ph / 0.7))     # the swing foot from behind to ahead (body units, left is ahead)
    feet = [(-a * 0.9, lift), (0.0, 0.0)] if n % 2 == 0 else [(0.0, 0.0), (-a * 0.9, lift)]
    bob = 3 * math.sin(math.pi * min(1.0, ph / 0.7))
    cam = WALK_CAM if t < 1.1 else CAL_CAM                 # v3 (cold tests 3 of 3: it drags; "a calculator"): CUT IN on the two
    return dict(_cam=cam, father_step=feet, moved=dict(father=(x, 880 - bob), g2=(120, 872))), {}   # of them, the calendar readable


CAL_CAM = (172, 770, 2.6)


WALK_CAM = (170, 815, 1.8)                                 # locked: he walks through the frame (a following camera jumped)


VETO_AT = (505, 880)                                       # v9 (22 Nov, decided): Father shuts the lighter himself
VETO_CAM = (594, 836, 2.00)                                # v12: the two men and the lighter in the safe band
VETO_G2 = (688, 880)                                       # v12: the guard beside Father, in front of the car
VETO_FIST = (596, 756)                                     # his fist with the lighter, at his chest, toward Father


def _veto(t16, t17):
    """one continuous two-shot over 1.6 + 1.7: the guard's lighter comes up to him; the brow; his palm on the lid; SNAP.
    v12 (23 Nov, outside audit "the arm out of an impossible place", lesson 292): the guard has stepped ROUND the car and
    stands beside him on the same floor; the lighter in his own hand at his chest, held out to Father; Father's palm comes
    down on it at chest height. No arm drawn over the car."""
    import of_scenes as sc_
    st = dict(_cast=("g2", "father"), _cam=VETO_CAM, moved=dict(father=VETO_AT, g2=VETO_G2), front_of_car=("g2",),
              burn=0.8 if t17 is None else 1.0)
    rest = (VETO_AT[0] + 30, 800)
    g_rest = (VETO_G2[0] - 40, VETO_G2[1] - 100)               # his hand at his side
    lx, ly = VETO_FIST[0], VETO_FIST[1] - sc_.LIGHTER_LIFT     # the flame's foot
    lid_pt = (lx - 13, ly - 16)                               # Father's wrist; the flat palm across the shut lid
    if t17 is None:
        t = t16
        d = ease(t / 0.30)
        g = om.lerp(g_rest, VETO_FIST, d)
        u = ease((t - 0.40) / 0.35)
        hand = [om.lerp(rest, lid_pt, u)] if u > 0 else []
        return st, dict(father=dict(face="brow2" if t > 0.15 else "hard", look=(1, -0.2), targets_xy=hand, palm=u > 0.9),
                        g2=dict(targets_xy=[g], turn=-1.0, lighter=1.0, lid=1.0, elbow_low=True))
    t = t17
    lid = 1.0 - ease((t - 0.05) / 0.10)                      # SNAP, under his palm
    off = ease((t - 0.64) / 0.06)                             # the palm HELD on the shut lid, 0.5 s
    hand = [om.lerp(lid_pt, rest, off)] if off < 0.95 else []
    return st, dict(father=dict(face="brow2" if t < 0.4 else "hard", look=(1, -0.2), targets_xy=hand, palm=off < 0.5),
                    g2=dict(targets_xy=[VETO_FIST], turn=-1.0, lighter=1.0 if lid > 0.6 else 0.0, lid=lid, elbow_low=True))


# --- scene 4, The Calendar ---------------------------------------------------------------------------------------------
def _loud(sid, t):
    m = mouth_at(sid, t)
    return {None: 0.0, "M": 0.15, "F": 0.3, "C": 0.45, "U": 0.5, "E": 0.7, "O": 0.85, "A": 1.0}.get(m, 0.5)   # v2: every viseme


def s32(t, L):                                             # the visor: the line pops on, and glows as it talks; v2 (cold tests
    k_ = 0.02 + 0.98 * min(1.0, max(0.0, (t / 0.15))) if t < 0.15 else 1.0 + 0.08 * math.sin(min(1.0, (t - 0.15) / 0.12) * math.pi)
    lo = _loud("3.2", t)                                   # 2 of 3 "held too long"): it bobs on its wheel with each word
    return dict(visor_k=k_, visor_glow=lo, robot_bob=-6 * lo * abs(math.sin(t * 2 * math.pi * 2.4))), {}


def s33(t, L):                                             # he sits up for good news
    return dict(don_over=dict(forward=0.6 * ease(t / 0.3))), {}


def s35(t, L):                                             # he follows the look down, to himself; the smile goes in ONE drawing
    if t < 0.40:
        u = ease(t / 0.35)
        return dict(don="happy", don_over=dict(look=(1 - 0.8 * u, u))), {}
    return {}, {}


def s36(t, L):                                             # v4 (23 Nov, decided, 2.6 s): buzz; glasses DOWN; the invitation,
    if t < 0.22:                                           # readable; a small smile (she knows); her eyes to Don, held 0.5 s;
        return dict(buzz=4 * math.sin(t * 2 * math.pi * 18) if t > 0.03 else 0.0, pam_look=(0.4, 0.8)), {}   # back; face down
    if t < 0.45:
        return dict(pam_look=(0.4, 0.8), pam_glasses="up" if t < 0.33 else "low"), {}
    if t < 1.40:
        return dict(_cam="insert", insert="invite"), {}
    g = dict(pam_glasses="low")
    if t < 1.65:
        return dict(g, pam_look=(0.4, 0.8), pam_face="proud"), {}          # reads it again; the corner of her mouth goes up
    if t < 2.15:
        return dict(g, pam_look=(-1, 0.2), pam_face="proud"), {}           # her eyes to Don, held
    return dict(g, pam_look=(1, 0.3) if t > 2.35 else (-1, 0.2), pam_face="proud", phone_down=True, pam_pose=(-8, 0, 40, 40)), {}


def s37(t, L):                                             # the smile is gone; he grabs the phone; DAD; the sweat comes back
    if t < 0.2:
        return dict(don="stiff"), {}
    u = ease((t - 0.2) / 0.3)
    if t < 1.0:                                            # DAD on the screen, at his chest (v3: held 0.8 s, cold tests 3 of 3)
        return dict(don_over=dict(sweat=1 + int(2 * u), forward=u)), {}
    return dict(don_over=dict(sweat=3, forward=1.0, phone_ear=True, pose=(-72, -108, 30, 10))), {}   # then at his ear


# --- scene 5, Frame 0 ------------------------------------------------------------------------------------------------
def s41(t, L):                                             # v3 (23 Nov, cold tests 3 of 3: "a faceless hand"): FATHER in the
    if t < 1.1:                                            # doorway, DONNIE buzzing in his hand; he looks at it. Then CLOSE:
        bz = 2.5 * math.sin(t * 2 * math.pi * 18)          # his thumb on red, DECLINED, face down
        lk = ease((t - 0.1) / 0.3); nd = ease((t - 0.5) / 0.22) - ease((t - 0.82) / 0.22)
        return (dict(_cam=DOOR_CAM, _cast=("father",), black_car=True, burn=1.0, insert=None, moved=dict(father=(156, F_ + 26))),
                dict(father=dict(face="hard" if t < 0.5 else "low" if t < 0.95 else "brow", look=(1 - 0.4 * lk, 0.2 + 1.0 * lk), lean=0.03 * nd,
                                 targets_xy=[(190, F_ - 110)], phone_donnie=True, buzz=bz)))   # v5 (decided): eyes from the room to
                                                                                               # the phone, ONE slow nod, brow down
    u = t - 1.1                                            # v4 (timing v12, cold tests 3 of 3 "too fast"): DECLINED held 1.0 s
    th = ease((u - 0.25) / 0.2)
    return dict(_cam=DONNIE_CAM, hand_dx=0.0, buzz=3 * math.sin(u * 2 * math.pi * 18) if u < 0.3 else 0.0,
                thumb=th if u < 1.4 else 0.0, declined=u > 0.45, donnie_down=u > 1.45), {}


DONNIE_CAM = (98, 668, 3.0)                                # v3: the phone big enough to read on a phone


def s42(t, L):                                             # frame 0's drawing; the black car's lights go across the wall, leaving
    u = ease((t - 0.3) / 0.8)
    return (dict(sweep_x=160 - 420 * u) if 0 < u < 1 else {}), {}


# --- v3 opening (22 Nov, decided): the joke at 0:00. SLAM; "Off the car."; the hand snaps off, in the SAME frame -------
def s08_slam(t, L):
    import of_set as gs
    x, f = sc.BLOCK[1]["g1"]
    rx, ry = 322, 652                                     # v10: the roof's TOP (the "roof" point sat at the pillar)
    if t < 0.07:                                           # frame 0: the hand already up, coming down
        return dict(tilt=0.0, legs_jolt=0.0), dict(g1=dict(targets_xy=[(rx - 10, ry - 70 + 300 * t)], push=False))
    ph = (t - 0.07) / 0.28
    a = -0.19 * abs(math.sin(ph * math.pi)) if ph < 2 else -0.19 * abs(math.sin(ph * math.pi)) * math.exp(-(ph - 2) * 1.5)
    imp = max(0.0, 1 - (t - 0.07) / 0.25)
    px, py = gs.STANDS[1], gs.SILL + 50                     # v9: the palm rides the roof as the car tips (it hung in the air)
    hx = px + (rx - px) * math.cos(a) - (ry - py) * math.sin(a)
    hy = py + (rx - px) * math.sin(a) + (ry - py) * math.cos(a)
    return dict(tilt=a, legs_jolt=-60 * a), dict(g1=dict(targets_xy=[(hx, hy + 2)], push=True, impact=imp,
                                                         dent=1.0 if 0.07 <= t < 0.17 else 0.0))


def s010_same(t, L):                                       # the SAME frame as the slam: the hand snaps off; he steps back
    x, f = sc.BLOCK[1]["g1"]
    roof, off = sc._pt("roof", x, f), sc._pt("off_r", x, f)
    u = om.hold(t / 0.13)                                  # two drawings
    back = -30 * om.hold((t - 0.12) / 0.20)
    turn = -1.0 * om.hold((t - 0.45) / 0.20)              # then he looks left, to Father (off screen)
    return dict(_cam=sc.CAR_CAM, _cast=("g1",)), dict(g1=dict(targets_xy=[om.lerp(roof, off, u)], back=back, turn=turn, push=False))


NEW_PLAN_G2 = (410, 818)                                   # v3 (23 Nov, decided): the other guard, behind the car, at the wall


def s42_service(t, L):                                     # the last frame (and the loop): the other guard slides a FRESH plan up
    x, f = sc.BLOCK[1]["g1"]                               # over the burnt one ("again"); the lamp man puts the lamp down and
    if t < 0.55:                                           # v4 (cold tests 3 of 3: the plan "healed"): CLOSE, his thumb pins
        return dict(_cam="insert", insert="pin", pin_u=ease(t / 0.35)), {}   # the fresh plan up (v5: see MOTION["4.2"])
    u = 1.0                                                # his hand comes up over the roof, as in frame 0
    top = 449 + (586 - 449) * (1 - u)
    hands = [(372, 586 - 0 * u + (top - 449) * 0), (448, 586)]
    st = dict(legs_work=math.sin(t * 2 * math.pi * 1.2), new_plan=u, _cast=("g1", "g2"),
              moved=dict(g1=(206, 862), g2=NEW_PLAN_G2), behind_car=("g2",))
    g2 = dict(targets_xy=[(372, 590), (448, 590)], turn=0.0)
    if t > 0.55:                                           # done: his hands down; he stands at the wall, as in frame 0
        v_ = ease((t - 0.55) / 0.35)
        g2 = dict(targets_xy=[om.lerp((372, 590), (380, 760), v_), om.lerp((448, 590), (440, 760), v_)], turn=0.0) if v_ < 1 else dict(turn=0.0)
    if t < 0.7:
        g1 = dict(targets_xy=[(x + 58, f - 70)], lamp=True, lamp_ang=3.0, push=False)
    elif t < 1.0:                                          # v5 (decided): he lobs it underarm onto its spot on the floor, 0.3 s
        w_ = (t - 0.7) / 0.3
        g1 = dict(targets_xy=[om.lerp((x + 58, f - 70), (x + 40, f - 120), w_)], push=False, lamp=False)
        st["lamp_fly"] = w_
    else:
        v = ease((t - 1.0) / 0.4)
        g1 = dict(targets_xy=[om.lerp((x + 40, f - 120), (322 - 10, 652 - 70), v)], push=False, lamp=False)
        st["lamp_floor"] = True
    return st, dict(g1=g1, g2=g2)


def s24(t, L):                                             # v1 (23 Nov audit, decided): Father acts the question. He leans
    ln = 0.035 * ease(min(1.0, max(0.0, (t - 0.5) / 0.6)))  # in toward the Client as he asks; the brow goes up on "company?"
    face = "hard" if t < 2.35 else ("brow" if t < 3.05 else "hard")   # v2: the mouth comes from the take
    fx_, ff_ = sc.BLOCK[3]["father"]   # v4 (24 Nov, cold test 3 of 3 "arms down in
    gu = ease((t - 0.7) / 0.3) - ease((t - 2.7) / 0.3)     # every shot"): his hand comes up, open, toward the Client, on the question
    gest = dict(targets_xy=[(fx_ + 34 + 30 * gu, ff_ - 96 - 78 * gu)]) if gu > 0.02 else {}
    if t >= 1.5:                                           # v3 (cold tests 3 of 3: it drags): CUT to the medium, the question
        return (dict(_cam=(467, 872, 1.80), _cast=("father", "client")),   # lands on the Client, at the engine (2.1's two-shot)
                dict(father=dict(face=face, lean=ln, look=(1, 0), **gest), client=dict(kind="bent", work=_work(t))))
    return {}, dict(father=dict(face=face, lean=ln, look=(1, 0), **gest))


def s26(t, L):                                             # v1: "And then?" -- the lean in, then the big brow after the line,
    ln = 0.045 * ease(min(1.0, t / 0.4))                   # held: business, waiting
    face = "hard" if t < 1.1 else "brow2"
    return {}, dict(father=dict(face=face, lean=ln, look=(1, 0)))


LAMP_GAG_CAM = (606, 700, 2.6)                             # the guard and the lamp fill the frame; the plan is out, to the left


def s28f(t, L):                                            # v5 (24 Nov, cold test v37: "long for what it delivers", "his face does not react"): 1.8 s.
    fl = t > 0.35 and (t < 0.4 or 0.47 < t < 0.52 or t > 0.6)   # It flickers and DIES (0.35-0.6); he lifts it and looks INTO the bulb
    dn = ease((t - 0.25) / 0.2) - ease((t - 1.15) / 0.18)  # (0.65-0.95); it sags, his shoulders drop (1.0-1.2); he looks at US
    lift = ease((t - 0.65) / 0.3) - ease((t - 1.0) / 0.25)  # (1.3) and holds it 0.5 s
    sag = ease((t - 1.0) / 0.2)
    x, y = 556 + 12 * lift, 652 - 26 * lift + 26 * sag
    gx_, gf_ = sc.BLOCK[3]["g1"]
    return (dict(_cam=LAMP_GAG_CAM, moved=dict(g1=(gx_, gf_ + 7 * sag))),
            dict(g1=dict(targets_xy=[(x + 2, y)], lamp="held", cone_side=0.03 if fl else 1.0, lamp_ang=0.35 + 0.2 * lift - 0.55 * sag,
                         cable_floor=sc.F + 8,
                         turn=0.01 - 0.6 * dn, look_down=12 * dn)))


def s28b(t, L):                                            # v2 (24 Nov, cold test v31: the held 'One month' shot dragged): after the line's first half, CUT to
    if t < 1.35:                                           # Father, his eyes on the held-out phone, and the line goes on over him
        return {}, {}
    return dict(_cam=(580, 790, 3.2), _cast=("client",)), {}


MOTION = {"0.2": s02, "0.3": s03, "1.1": s11, "1.2": s12, "1.3": s13, "1.4": s14,
          "2.1": s21, "2.2": s22, "2.3b": s23b, "2.5": s25, "2.7": s27, "2.8b": s28b, "2.8c": s28c, "2.8d": s28d, "2.8e": s28e,
          "2.9": s29, "2.4": s24, "2.6": s26, "2.8f": s28f,
          "3.2": s32, "3.3": s33, "3.5": s35, "3.6": s36, "3.7": s37,
          "4.1": s41, "4.2": s42}
HANDS_CAM = (500, 742, 3.0)                                # v9: the cut-in: his hands, working in the light


LAMP_G1 = (692, 884)                                       # v5: in front of the car, by the open bay
LAMP_IN_BAY = (636, 650)                                   # below his chin, the cage down in the bay: the light on the engine


def s23(t, L):
    """lamp v4 (22 Nov, decided after the cold test read 'interrogation'): the handover as v3, but the bodyguard holds
    it LOW, BESIDE the bay, aimed at the hands; then a cut-in on the hands working in the light."""
    bx, bf = sc.BENT_AT
    start, out_ = (bx - 30, 718), (bx + 60, 724)
    x, f = LAMP_G1                                         # v5 (23 Nov, lesson 292): he stands at the bay's side, in front
    rest = (x - 44, f - 120)
    u1 = om.hold(t / 0.30)
    u2 = om.hold((t - 0.30) / 0.22)
    u3 = om.hold((t - 0.55) / 0.30)
    st = dict(moved=dict(g1=LAMP_G1), front_of_car=("g1",))
    if t >= 0.7:                                           # v7 (23 Nov, decided): CUT IN, 0.9 s: his hands in the light; the bolt comes free
        return dict(_cam="insert", insert="bay", work=math.sin(t * 2 * math.pi * 1.3) if t < 1.2 else 0.0,
                    bay_reach=ease((t - 1.2) / 0.3), bolt_out=ease((t - 1.6) / 0.35), bay_u=1.0), {}     # v8 (timing v11): the cut-in 1.2 s, the bolt later
    if u3 > 0:
        gh = om.lerp(out_, LAMP_IN_BAY, u3)
        return st, dict(client=dict(kind="bent", hand_back=False, work=math.sin(t * 2 * math.pi * 1.3) if t > 0.9 else 0.0),
                        g1=dict(targets_xy=[gh], lamp=True, lamp_xy=gh, cone_side=u3, cable_floor=LAMP_G1[1] - 4, pool=(494, 716), lamp_ang=0.1), father=dict(look=(1, -0.2)))
    gh = om.lerp(rest, out_, u2)
    return st, dict(client=dict(kind="bent", hand_back=True, hand_back_at=om.lerp(start, out_, u1), lamp_lit=False),
                    g1=dict(targets_xy=[gh]), father=dict(look=(1, -0.2)))


def s28e2(t, L):                                           # v9: the key turns; at the cough, CUT to the car: it runs
    if t < 0.55:
        return dict(key_u=ease(t / 0.3), run=0.0 if t < 0.45 else 4 * math.sin(t * 2 * math.pi * 11)), {}
    j = 1.4 * math.sin(t * 2 * math.pi * 13) * (1.6 if t < 0.75 else 1.0)
    return dict(_cam=RUN_CAM, _cast=(), insert=None, bonnet=0.0, burn=1.0,
                running=ease((t - 0.55) / 0.08), puff=t - 0.55, tilt=0.004 * j), {}


RUN_CAM = (350, 790, 1.25)                                 # the whole car, nose right: the lights, the puff, the shudder


MOTION["2.3"] = s23
MOTION["1.3"] = lambda t, L: s13(t * 1.3 / 1.6, L)   # v3 (timing v11, cold tests 3 of 3 "too fast"): the throw, the roll-out
                                                    # and the sit-up at 0.8x speed
MOTION["2.8e"] = lambda t, L: s28e(max(0.0, t - 0.3), L)   # v11 (24 Nov, cold test 3 of 3 "the car leaves, then is back"): no cut
_old_28e = lambda t, L: s28e2(max(0.0, t - 0.3), L)   # v10 (timing v11): his fingers on the key 0.3 s, then the turn
for _sid, _fn in om.veto():
    MOTION[_sid] = _fn
_s15 = MOTION.get("1.5")


def s15_fire(t, L):                                        # the plan still smoulders at the hole while he turns to Father
    st, po = _s15(t, L) if _s15 else ({}, {})
    return dict(st, burn=0.8, fire=0.15, fire_t=_T("1.5", t)), po


MOTION["1.5"] = s15_fire
MOTION["1.6"] = lambda t, L: _veto(t, None)
MOTION["1.7"] = lambda t, L: _veto(None, t)
for _sid, _fn in om.turn():
    MOTION[_sid] = _fn
for _sid, _fn in om.rock():
    MOTION[_sid] = _fn
def s09_work(t, L):                                       # the sump sways; he finishes one small turn, stops, then the line
    st, po = om.rock()[1][1](t, L)
    st = dict(st, wrench_t=math.pi * min(1.0, t / 0.35))
    return st, po


def s34b(t, L):                                            # v9: turned to Don, it glows as it talks
    lo = _loud("3.4b", t)
    return dict(visor_glow=lo, robot_bob=-6 * lo * abs(math.sin(t * 2 * math.pi * 2.4))), {}   # v10: it bobs as it talks


def s35b(t, L):                                            # v9: he turns to the counter: "Pam?"
    u = ease(t / 0.25)
    return dict(don_over=dict(look=(0.2 + 1.8 * u, 0.4 - 0.4 * u))), {}   # v10: the eyes all the way to the counter


def s36b(t, L):                                            # v9: MEETING IN 4:59 ... 4:58, ticking
    return dict(count=299 - int(t / 0.6)), {}


MOTION["3.4b"] = s34b
MOTION["3.5b"] = s35b
MOTION["3.6b"] = s36b
def s09_wide(t, L):                                       # v3 (23 Nov, cold tests 3 of 3 gave the line to the GUARD): on the
    x, f = sc.BLOCK[1]["g1"]                               # first word the legs KICK (out and back) and the knee works; the
    kick = 16 * math.sin(math.pi * min(1.0, max(0.0, (t - 0.12) / 0.25)))   # guard's head drops to look down AT the legs
    lk = ease(min(1.0, max(0.0, (t - 0.25) / 0.2)))       # (a listener looks at whoever speaks)
    return dict(_cam=sc.CAR_CAM, _cast=("g1",), legs_work=math.sin(t * 2 * math.pi * 2.0), legs_jolt=kick,
                shake=(9 * math.exp(-(t - 0.2) * 12) * math.sin(t * 100)) if t > 0.2 else 0.0), \
        dict(g1=dict(targets_xy=[(322, 654)], push=True, turn=0.7 * lk, look_down=10 * lk))


MOTION["0.9"] = s09_wide
MOTION["0.8"] = s08_slam                                   # v8 (22 Nov): the joke at 0:00
MOTION["0.10"] = s010_same
PIN_T = 1.25                                               # v5 (24 Nov, decided): the burnt plan 0.25 s, the fresh one slides
MOTION["4.2"] = lambda t, L: (dict(_cam="insert", insert="pin", pin_slide=ease((t - 0.25) / 0.28),   # up over it, the finger pins
                                   pin_u=ease((t - 0.72) / 0.2)), {}) if t < PIN_T else s42_service(t - PIN_T + 0.55, L)
# v6 (timing v12): the pin held 0.3 s longer, the rest as it was
MOTION["0.4"] = lambda t, L: (dict(legs_work=math.sin(t * 2 * math.pi * 1.2)), {})    # the knee taps: he works on


# --- the lips: the take's loudness per drawing -> a mouth code ---------------------------------------------------------
_TAKE = {}


VISEME = {"A": "M", "B": "C", "C": "E", "D": "A", "E": "O", "F": "U", "G": "F", "H": "E", "X": None}   # Rhubarb -> our mouths
_CUES = {}


LIP_AHEAD = 2 / 30.0


def accent(sid, t):
    """v1 (24 Nov, decided): 0..1, a stressed syllable of the speaker this drawing (the take's loudness rising fast);
    the speaker's head dips with it."""
    if sid not in sc.SAY:
        return 0.0
    if sid not in _TAKE:
        a, sr = sf.read(os.path.join(TAKES, "%s.wav" % sid))
        _TAKE[sid] = (a, sr)
    a, sr = _TAKE[sid]
    def env(x):
        if x < 0 or x > len(a) / sr:
            return 0.0
        seg = a[int(x * sr):int((x + 0.06) * sr)]
        return float(np.sqrt(np.mean(seg ** 2))) / (np.abs(a).max() + 1e-9) if len(seg) else 0.0
    tt = t - LEAD
    best = 0.0
    for back in (0.0, 0.05, 0.10, 0.15):                    # the dip lasts ~0.2 s after the rise
        rise = env(tt - back) - env(tt - back - 0.12)
        best = max(best, min(1.0, max(0.0, rise / 0.25)) * (1 - back / 0.2))
    return best


def mouth_at(sid, t):
    """the mouth for the speaker of shot sid, t seconds into the shot (None: not speaking). v2 (23 Nov, decided): the
    take's own mouth shapes (Rhubarb Lip Sync, of_voices/visemes/<shot>.json, phonetic, with the line's text), held
    to the drawing; the loudness rule only where a take has no cue track."""
    if sid not in sc.SAY:
        return None
    if sid not in _TAKE:
        a, sr = sf.read(os.path.join(TAKES, "%s.wav" % sid))
        _TAKE[sid] = (a, sr)
    a, sr = _TAKE[sid]
    tt = t - LEAD + LIP_AHEAD                              # v3 (24 Nov, decided): the mouth 2 frames ahead of the sound
    if tt < 0 or tt > len(a) / sr:
        return None
    vp = os.path.join(TAKES, "..", "visemes", "%s.json" % sid)
    if sid not in _CUES and os.path.exists(vp):
        import json as _json
        _CUES[sid] = _json.load(open(vp))["mouthCues"]
    if sid in _CUES:
        mid = tt + 0.5 / DPS                                   # the middle of this drawing
        for cu in _CUES[sid]:
            if cu["start"] <= mid < cu["end"]:
                return VISEME.get(cu["value"])
        return None
    i0, i1 = int(tt * sr), int((tt + 1.0 / DPS) * sr)
    seg = a[i0:max(i1, i0 + 1)]
    v = float(np.sqrt(np.mean(seg ** 2))) / (np.abs(a).max() + 1e-9)
    return "M" if v < 0.05 else ("C" if v < 0.12 else ("E" if v < 0.2 else ("O" if v < 0.3 else "A")))


def bubble_on(sid, t):
    if sid not in sc.SAY:
        return False
    if sid not in _TAKE:
        mouth_at(sid, 0.0)
    a, sr = _TAKE[sid]
    return LEAD - 0.02 <= t <= LEAD + len(a) / sr + 1.0 / DPS


SPLIT = {"1.4": (0.20, ("Burn them.", "Your son loses his only customer."))}   # v12: where the take splits


HOLD_D = 5                                                 # drawings (0.33 s): a prop passing through a zone in a move is fine


def held_only(probs):
    """dead-zone faults count only when they last HOLD_D drawings in a row (a lighter rising into frame through the
    caption zone is a move, not a prop left there); every other fault counts at once."""
    out, runs = [], {}
    for sid, i, t, q in probs:
        if not q.startswith("ZONE"):
            out.append("%s t=%.2f: %s" % (sid, t, q)); continue
        key = (sid, q.split(" (")[0])
        r = runs.get(key)
        if r and r[1] == i - 1:
            r[1] = i; r[2] += 1
        else:
            runs[key] = r = [i, i, 1, t, q]
            runs.setdefault("_all", []).append(r)
    for r in runs.get("_all", []):
        if r[2] >= HOLD_D:
            out.append("%s t=%.2f: %s (for %d drawings)" % ([k for k, v in runs.items() if v is r][0][0], r[3], r[4], r[2]))
    return out


def render_scene(n):
    title, where, scene, shots = sc.SCENES[n - 1]
    tm = sc._timing()
    d = os.path.join(TMP, "s%d" % n)
    os.makedirs(d, exist_ok=True)
    for f_ in os.listdir(d):
        os.remove(os.path.join(d, f_))
    k = 0
    probs, sheet = [], []
    t0 = tm[shots[0]["id"]]["start"]
    for sh0 in shots:
        sid = sh0["id"]
        L = tm[sid]["len"]
        fn = MOTION.get(sid, still)
        st0 = tm[sid]["start"]                                 # v2 (rough cut): drawings on the timeline's own grid, so
        nd = max(1, int(round((st0 + L) * DPS)) - int(round(st0 * DPS)))   # the picture never drifts from the sound
        for i in range(nd):
            t = i / DPS
            st_over, pose_over = fn(t, L)
            st_over = dict(st_over)
            cast = st_over.pop("_cast", None)
            cam_ = st_over.pop("_cam", None)
            sh = dict(sh0, state=dict(sh0["state"], **st_over))
            if cam_ is not None:
                sh["cam"] = cam_
            if cast is not None:
                sh["cast"] = cast
            saved = sc.POSES.get(sid)
            if pose_over:
                base = dict(saved or {})
                for who, ps in pose_over.items():
                    base[who] = dict(base.get(who, {}), **ps)
                sc.POSES[sid] = base
            who = sc.SAY.get(sid, (None,))[0]
            oc.NOW[0] = st0 + t                                    # v1 (23 Nov): the film's clock, for blinks and breaths
            oc.SHOT_T[0] = t
            oc.ACCENT[0] = (who, accent(sid, t))
            oc.LOOP_T[0] = sc._timing_total()
            mc_ = mouth_at(sid, t)
            oc.MOUTH[0] = mc_ if who == "client" else None
            oc.FATHER_MOUTH[0] = mc_ if who == "father" else None
            oc.DON_MOUTH[0] = mc_ if who == "don" else None
            try:
                if sid in SPLIT:                                    # v12 (cold tests 3 of 3): two short bubbles, not one long
                    fr_, parts = SPLIT[sid]
                    mouth_at(sid, 0.0)
                    a_, sr_ = _TAKE[sid]
                    u_ = (t - LEAD) / (len(a_) / sr_)
                    sh = dict(sh, state=dict(sh["state"], say_txt=parts[0] if u_ < fr_ else parts[1]))
                surf, p = sc.board_frame(sh, scene, bubble=bubble_on(sid, t))
            finally:
                oc.MOUTH[0] = oc.FATHER_MOUTH[0] = oc.DON_MOUTH[0] = None
                if saved is None:
                    sc.POSES.pop(sid, None)
                else:
                    sc.POSES[sid] = saved
            probs += [(sid, i, t, q) for q in p]
            for _ in range(FPS // DPS):
                surf.write_to_png(os.path.join(d, "f%04d.png" % k)); k += 1
            if (k // 2) % 4 == 1 or i == 0:                       # about 4 fps for the sheet, and every shot's first drawing
                sheet.append((sid, tm[sid]["start"] + t - t0, surf))
    probs = held_only(probs)
    dur = k / FPS
    a, sr = sf.read(os.path.join(sc.OUT, SOUND))
    seg = a[int(t0 * sr):int((t0 + dur) * sr)]
    wav = os.path.join(TMP, "s%d.wav" % n)
    sf.write(wav, seg, sr)
    m1080 = os.path.join(TMP, "of_scene%d_v%d_1080.mp4" % (n, VER.get(n, 1)))
    m540 = os.path.join(sc.OUT, "of_scene%d_v%d_540.mp4" % (n, VER.get(n, 1)))
    tags = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", os.path.join(d, "f%04d.png"), "-i", wav,
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast"] + tags +
                   ["-c:a", "aac", "-b:a", "192k", "-shortest", m1080], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", m1080, "-vf", "scale=540:960:flags=lanczos,format=yuv420p", "-c:v",
                    "libx264", "-crf", "20", "-preset", "veryfast"] + tags + ["-c:a", "copy", m540], check=True)
    # the 4 fps sheet
    cols, tw, th = 8, 216, 384
    rows = (len(sheet) + cols - 1) // cols
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, (cols * (tw + 8) + 8) * 2, (rows * (th + 30) + 10) * 2); S.set_device_scale(2, 2)
    c = cairo.Context(S); c.set_source_rgb(1, 1, 1); c.paint()
    for j, (sid, tt, img) in enumerate(sheet):
        x = 8 + (j % cols) * (tw + 8); y = 6 + (j // cols) * (th + 30)
        c.save(); c.translate(x, y); c.scale(tw / 540.0, th / 960.0); c.set_source_surface(img, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, y + th + 18); c.show_text("%d   %.1f s" % (j + 1, tt))
    S.write_to_png(os.path.join(TMP, "s%d_sheet4.png" % n))
    return k, dur, probs, m540, m1080


def _at_wall(r):
    """v1 (23 Nov, the loop): bodyguard 2 stands at the wall behind the car from frame 0 (the man who will burn the plan,
    and who pins the fresh one in the last shot), so the last frame and frame 0 are one picture."""
    st, po = r
    st = dict(st, _cast=("g1", "g2"), behind_car=("g2",))
    st["moved"] = dict(st.get("moved", {}), g2=NEW_PLAN_G2)
    po = dict(po, g2=dict(turn=0.0))
    return st, po


MOTION["0.8"] = lambda t, L, f_=MOTION.get("0.8", s08_slam): _at_wall(f_(t, L))
MOTION["0.10"] = lambda t, L, f_=MOTION.get("0.10", s010_same): _at_wall(f_(t, L))
MOTION["0.9"] = lambda t, L, f_=MOTION.get("0.9", s09_wide): _at_wall(f_(t, L))   # v2: the same picture as 0.8
DOOR_CAM = (168, 700, 1.9)                                # v1 (23 Nov, decided): the doorway, Father in it, held


def s06_arrive(t, L):                                      # Father in the doorway, the black car behind him: he has arrived.
    u = ease((t - 0.45) / 0.3)                             # v2 (cold test 3 of 3: "a statue"): his eyes go from the room down
    return (dict(_cam=DOOR_CAM, _cast=("father",), black_car=True, moved=dict(father=(156, F_ + 26))),   # to the legs, he leans
            dict(father=dict(face="low" if u < 0.9 else "brow", look=(1 - 0.4 * u, 0.3 + 1.1 * u), lean=0.03 * u)))


F_ = sc.F
MOTION["0.6"] = s06_arrive


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    k, dur, probs, m540, m1080 = render_scene(n)
    print("scene %d: %d frames, %.2f s -> %s" % (n, k, dur, m540))
    for q in probs[:20]:
        print("FAIL", q)
    sys.exit(1 if probs else 0)

