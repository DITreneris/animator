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
END_53C = [(-40, 70)]
V2_53 = [True]                                               # 5.3c / 5.3b v2 (reviews 26 Nov); False = master v7's
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
    """the hand-over in 1.2 s, v2 (three reviews, 26 Nov: "the fingers merge", "he must let go before he pulls back",
    "one clear grip"): he holds it out (0-0.25), her open hand comes up (0.25-0.55), she steps in (0.55-0.72), both hold
    it, a card's width between their hands (0.72-0.85), HE LETS GO: his hand opens and comes off it (0.85-0.95), then
    his arm goes back down while she brings it in to her chest, held by its top edge, DAD and SOFÍA clear (0.95-1.2)."""
    heads = {}
    sb = sp.sbc
    full = e.SOF_53["C"]
    ua = ease(t / 0.25)
    ub = ease((t - 0.25) / 0.30)
    uc = ease((t - 0.55) / 0.17)
    held = t >= 0.72
    let_go = t >= 0.85
    ue = ease((t - 0.95) / 0.25)
    pr = _arm((120, -40), (185, -120), ua)                  # his arm from his side, out to her; back once he has let go
    if ue > 0:
        pr = _arm((185, -120), (120, -40), ue)
    o = e.guard_at(k, 148, pose_r=pr)
    heads["guard"] = (o["head"][0], o["head"][1], 40 * e.GS)
    gx, gy = o["hands"][1]
    sb.POSES["_take53"] = full + (8, 0)
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
    chest = END_53C[0]                                       # her arm at the end (the "chest" pose put her forearm over her face)
    if ue > 0:
        pose = _arm(full, chest, ue)                        # the card comes in to her chest
    sb.POSES["_take53a"] = pose + (8, 0)
    legs = {0: ((9, 7), (-7, 0))}.get(0 if 0.58 < t < 0.70 else None)
    sp.ss.LEGS[0] = legs
    try:
        os_, heads["sofia"] = ps.sofia(k, (sx, F + 60 - (2 if legs else 0)), "_take53a",
                                       "smile" if ue > 0.3 else "interested", (-1, 0.3) if ue < 0.5 else (-0.3, 0.9))
    finally:
        sp.ss.LEGS[0] = None
    hx, hy = min(os_["hands"], key=lambda h: h[0])
    skin_s = sb.sf.SKIN
    cx_held, cy_held = gx_f + e.C53_DX[0], gy_f + 6         # where the card is while both hold it (his reach)
    if not held:
        e._card_at(k, gx + e.C53_DX[0], gy + 6, -0.18)
        hp.draw(k, "grab", gx, gy, 24, co.SKIN, (1.0, 0.2), 1)
        if ub > 0:
            hp.draw(k, e.C53_SHAPE[0][0], hx, hy, e.C53_SHAPE[0][1], skin_s, e.C53_SHAPE[0][2], -1)
    elif not let_go or ue <= 0:                              # both on it, or he has just let go: the card stays put
        e._card_at(k, cx_held, cy_held, -0.18)
        hp.draw(k, "grab", hx, hy, 21, skin_s, (-1.0, -0.1), -1)
        if not let_go:
            hp.draw(k, "grab", gx, gy, 24, co.SKIN, (1.0, 0.2), 1)
        else:                                                # his hand open and off its edge: a clear gap
            hp.draw(k, "palm", gx - 22, gy - 8, 24, co.SKIN, (0.25, -1.0), 1)   # open, up, off it: let go
    else:                                                    # hers, coming in to her chest by its top edge
        tx, ty = lerp(cx_held, hx - 4, ue), lerp(cy_held, hy + 34, ue)
        e._card_at(k, tx, ty, lerp(-0.18, -0.03, ue), lerp(1.0, 0.85, ue))
        hp.draw(k, "grab", hx, hy, 21, skin_s, lerp(-1.0, 0.0, ue) and (lerp(-1.0, -0.2, ue), lerp(-0.1, 1.0, ue)), -1)
        if ue < 0.25:
            hp.draw(k, "palm", gx - 22, gy - 8, 24, co.SKIN, (0.25, -1.0), 1)
    return heads


def s53c(t):
    pss.DOOR_OPEN[0] = 0.0
    return dict(ps.S("5.3c", (300, F - 150, 1.4), dict(blind="rehung", tape=True, spun=True, mark=False),
                     lambda k: cast_53c_anim(k, t)), own_cam=True)


CAN_TILT_53B = 0.55
FAR_53B = (130, 80)                                          # its far arm, up: the can beside its head, in frame
GUARD_53B = (156, 278)                                       # v2: him where 5.3c left him; the robot where Sofía stood
CAM_53B = (262, 752, 2.05)


def cast_53b(k, t):
    """5.3b v2 (three reviews, 26 Nov: "the can's handle and spout across his chest", "two fists stuck together", "who
    holds it?"): where 5.3c left them. He has one hand down at his side, the other at his belt (no clasped pair). The
    robot holds the can up in its FAR hand by the loop handle, the spout turned away from him (mirrored), at 0.9 of its
    size; its near arm reaches to him. The heart beats in two drawings. Sofía walks out of frame right with her card
    for 0.4 s (she goes on to the tape: 5.5)."""
    import dh_cast as dc
    import robot_ps as rp
    from cand_bc import ik
    c = k.c
    heads = {}
    give = 1 - ease((t - 0.05) / 0.30)                       # his giving hand back to his side
    down = ik(-dc.co.SH[0], dc.co.BT + 26, -dc.co.SH[0] - 6, dc.co.HIP + 64, dc.co.LN1, dc.co.LN2, -1)
    belt = ik(dc.co.SH[0], dc.co.BT + 26, -16, dc.co.HIP + 2, dc.co.LN1, dc.co.LN2, 1)
    gp = (down[0], down[1], belt[0] + (10 - belt[0]) * give, belt[1] + (20 - belt[1]) * give)
    og = dc.guard(k, GUARD_53B[0], F + 46, ps.GUARD_S, pose=gp)
    heads["guard"] = (og["head"][0], og["head"][1], 40 * ps.GUARD_S)
    if t < 0.45:                                             # Sofía off to the right, the card at her chest
        u = ease(t / 0.45)
        o, _h = ps.sofia(k, (400 + 150 * u, F + 60), "walk", "smile", (1, 0))
        hx, hy = o["hands"][1]
        sp.cv_coo(k, hx + 6, hy + 10, 0.55)
    up = ease((t - 0.10) / 0.35)                             # the can comes up in its far hand
    heart = t >= 0.42
    far = (20 + (FAR_53B[0] - 20) * up, 10 + (FAR_53B[1] - 10) * up)
    arms = ((-70, -20), far)
    rxy = (GUARD_53B[1], F + 50)
    c.push_group(); orb, _ = ps.robot(k, rxy, arms=arms); c.pop_group()
    rh = orb["hands"][1]
    _, heads["robot"] = ps.robot(k, rxy, arms=arms, look=(0.6, -0.5) if heart else (-1, -0.3),
                                 **({"visor": "heart"} if heart else {}))
    cs = 0.9 * 1.15
    hx_, hy_ = rp.CAN_HANDLE[0] * cs, rp.CAN_HANDLE[1] * cs
    tilt = CAN_TILT_53B * up                                 # tipped back as it comes up: the spout points up, in frame
    c.save(); c.translate(rh[0], rh[1]); c.scale(-1, 1); c.rotate(tilt)   # mirrored: the spout away from him
    rp.oil_can(k, -hx_, -hy_, cs, 0.0, label=False)
    c.restore()
    c.save(); c.translate(rh[0], rh[1]); c.rotate(-tilt); c.translate(hx_, -hy_); c.scale(cs, cs)   # its label, unmirrored
    c.set_source_rgb(0.97, 0.95, 0.88); c.rectangle(-17, -24, 34, 19); c.fill_preserve()
    c.set_source_rgb(*e.INK); c.set_line_width(1.6); c.stroke()
    c.select_font_face("Lilita One"); c.set_font_size(15)
    ex = c.text_extents("OIL"); c.move_to(-ex.x_advance / 2, -9.5); c.show_text("OIL")
    c.restore()
    rp.hand_again(k, rh[0], rh[1], ps.SC["robot"])
    if heart and int((t - 0.42) * 7.5) % 2 == 0:             # the heartbeat: every other drawing a bigger heart over it
        hxr, hyr, rr = heads["robot"]
        c.save(); c.translate(hxr, hyr + rr * 0.05); s_ = rr * 0.82
        c.move_to(0, 0.35 * s_)
        c.curve_to(-1.0 * s_, -0.35 * s_, -0.45 * s_, -0.95 * s_, 0, -0.45 * s_)
        c.curve_to(0.45 * s_, -0.95 * s_, 1.0 * s_, -0.35 * s_, 0, 0.35 * s_)
        c.set_source_rgba(0.85, 0.97, 1.0, 0.85); c.set_line_width(2.2); c.stroke()   # a pale ring round it: the beat
        c.restore()
    ps.HANDS_LOG.extend(orb["hands"]); ps.HANDS_LOG.extend(og["hands"])
    return heads


def s53b(t):
    pss.DOOR_OPEN[0] = 0.0
    return dict(ps.S("5.3b", CAM_53B, pf.BOARD["5.3"]["room"], lambda k: cast_53b(k, t)), own_cam=True)


def s53(t):
    if t < A_53:
        return s53a(t)
    if t < B_53:
        return s53c(t - A_53)
    if V2_53[0]:
        return s53b(t - B_53)
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
        if pss.DAD_MARK[0]:                                  # her side named: she is on DAD's
            e.kit.text(k, "DAD", 440, 600, 30, e.INK)
        return {}
    return ps.S("5.5b", "screen", draw=draw)


# --- 6.1: "Everyone's with me." and, behind him, her thumb on ACCEPT ------------------------------------------------------
PRESS_61 = 1.90                                              # after his line: the thumb comes down, the ring comes on


V2_61 = [True]                                               # reviews 26 Nov: the phone held, ACCEPTED, eyes; Sofía's card in two hands
PH_61 = 0.34 * 0.75                                          # the phone 25 % smaller ("a tablet")
CARD_61 = 0.80                                               # her card 10 % smaller
BTN_61 = (0, 51)                                             # ACCEPT on phone_close's screen (of_ui.invite_small's pill), local units


def cast_61_v2(k, t, buzz=False):
    """6.1 v2: Mom as before. Sofía holds the card in BOTH hands by its side edges (hands_ps "grab"), her eyes on it.
    Pam holds the phone in the series' grip (of_cast.phone_grip: the palm behind, the thumb on its near edge, three
    fingertips round the far one); her eyes on the screen; her thumb comes onto ACCEPT, which turns to ACCEPTED with a
    tick, and she smiles."""
    import of_cast as ofc
    import pam_mf
    heads = {}
    c = k.c
    _, heads["mom"] = ps.mom(k, "mom_tape", "folded", "stern", (1, -0.6))
    o, heads["sofia"] = ps.sofia(k, (ps.SOF_61[0], F + 40), "chest", "smile", (0.1, 1.0))
    (ax, ay), (bx_, by_) = o["hands"]
    cs = ps.CV_61[0] * 0.82 * CARD_61
    cx, cy = (ax + bx_) / 2, max(ay, by_) + 34 * cs
    sp.cv_coo(k, cx, cy, cs)
    w2 = 26 * cs
    for side, (hxx, hyy) in ((-1, (cx - w2, cy - 24 * cs)), (1, (cx + w2, cy - 24 * cs))):   # its upper corners
        hp.draw(k, "grab", hxx, hyy, 15, sp.sbc.sf.SKIN, (-side * 1.0, 0.1), side)
    pressed = t >= PRESS_61 and not buzz
    import pm_ps
    was_h = pm_ps.P_HANDS["cup_mid"]
    pm_ps.P_HANDS["cup_mid"] = (was_h[0], "fist")            # her rig's cup hand read as "a stick" across the phone: a fist,
    try:                                                     # under the grip's palm
        o, heads["pam"] = ps.pam(k, (e.PAM_X_61N[0], F + 40), "cup_mid", "quiet" if pressed else "doubt",
                                 (0.15, 1.0), mug=False)     # doubt -> the press -> her private smile, eyes on the screen
    finally:
        pm_ps.P_HANDS["cup_mid"] = was_h
    px, py = o["hands"][1]
    jx = (2.0 if int(round(t * pf.DPS)) % 2 else -2.0) if buzz else 0.0
    gs = 0.48                                                # the grip to the smaller phone (0.62: its thumb a "stick")
    palm = (px + jx, py + 6)
    ofc.phone_grip(k, palm[0], palm[1], gs, part="back", skin=pam_mf.SKIN, body_x=e.PAM_X_61N[0])
    pcx, pcy = palm[0], palm[1] - 30 * PH_61 * 2.2
    c.save(); c.translate(pcx, pcy)
    pss.phone_close(k, 0, 0, PH_61, lit=True, buzz=buzz)
    if pressed:                                              # ACCEPT -> ACCEPTED, a tick
        c.save(); c.scale(PH_61, PH_61)
        c.new_path(); c.rectangle(BTN_61[0] - 44, BTN_61[1] - 15, 88, 30)
        c.set_source_rgb(0.10, 0.45, 0.22); c.fill()
        c.select_font_face("Lilita One"); c.set_font_size(17); c.set_source_rgb(1, 1, 1)
        ex = c.text_extents("ACCEPTED"); c.move_to(BTN_61[0] - ex.x_advance / 2 + 7, BTN_61[1] + 6); c.show_text("ACCEPTED")
        c.set_line_width(3.2); c.set_line_cap(1)
        c.move_to(BTN_61[0] - ex.x_advance / 2 - 14, BTN_61[1]); c.line_to(BTN_61[0] - ex.x_advance / 2 - 8, BTN_61[1] + 6)
        c.line_to(BTN_61[0] - ex.x_advance / 2 + 2, BTN_61[1] - 7); c.stroke(); c.set_line_cap(0)
        c.restore()
    c.restore()
    u = ease((t - (PRESS_61 - 0.35)) / 0.30) if not buzz else 0.0   # the thumb comes onto the button
    bxw, byw = pcx + BTN_61[0] * PH_61, pcy + BTN_61[1] * PH_61
    tip_rest = ((bxw - palm[0]) / gs + 14, (byw - palm[1]) / gs + 10)
    tip_on = ((bxw - palm[0]) / gs, (byw - palm[1]) / gs)
    tip = (lerp(tip_rest[0], tip_on[0], u), lerp(tip_rest[1], tip_on[1], u))
    ofc.phone_grip(k, palm[0], palm[1], gs, part="front", skin=pam_mf.SKIN, body_x=e.PAM_X_61N[0], thumb_tip=tip)
    return heads


def cast_61(k, t, buzz=False):
    if V2_61[0]:
        return cast_61_v2(k, t, buzz)
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
SHOCK_POSE_61B = ["vest"]                                   # ps_film_fix (audit P15): "balance", the arms flung out


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
            return e.fg_61x(e.LOOK_TEAM[0], "shock", SHOCK_POSE_61B[0], spring=sp_, lean=ln)
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


_DUR53 = pf.DUR["5.3"]


def setup():
    e.look()
    pf.SCENES[5] = ["5.1", "5.2", "5.3", "5.4", "5.5", "5.5b", "5.6", "5.7"]
    pf.TIMING["5.5b"] = dict(shot="5.5b", len=1.0, line=None, takes=[], take_at=[])
    pf.DUR["5.5b"], pf.TAKE_AT["5.5b"] = 1.0, []
    pf.BOARD["5.5b"] = dict(e.s55b(), id="5.5b")
    pf.DUR["5.3"] = _DUR53 + (B_53 - pf.TREAT_AT)            # 5.3c's 1.2 s (idempotent: setup() may run twice)
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
