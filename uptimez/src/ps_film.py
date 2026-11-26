"""PICK A SIDE (episode 14), stage 7: the film, scene by scene (plan v2, 25 Nov). Modelled on of_film.py (episode 13):
one function per shot taking the shot's own time t and returning the shot to draw (ps_scenes.S), drawn by ps_scenes'
rigs, set and cameras under board v4 (gags_v5), at 15 drawings a second on the 30 fps camera.

One map (lesson 109): SHOT_FN, printed and asserted by every build. A shot not in it is a hold on its board key frame.
Each shot's camera is locked to its board key frame's camera (a face-framed camera would follow the moving cast).

  python3 ps_film.py stills 1   ->  ../pick-a-side/ps_film_s1_stills_v1.png (the key poses of scene 1, before any video)"""
import math
import os
import sys
import cairo
import ps_scenes as ps
import ps_set as pss
import ps_motion as pm_
import don_ps as dp
from kit import Ctx, INK

DPS, FPS = 15, 30
OUT = ps.OUT
SCENES = {1: ["1.1", "1.2a", "1.3", "1.4"],
          5: ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7"],
          4: ["4.1", "4.2", "4.3"],
          3: ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7"],
          2: ["2.1", "2.1b", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.9b", "2.10", "2.11"]}                 # v3 (Tomas 25 Nov): 1.2b cut (misread 3 times), its 0.5 s to 1.3
import json as _json
TIMING = {r["shot"]: r for r in _json.load(open(os.path.join(ps.OUT, "ps_timing_v3.json")))["shots"]}
DUR = {k: v["len"] for k, v in TIMING.items()}               # the takes' timing (v3): 1.3 2.61, 1.4 2.65
DUR["1.3"] += DUR["1.2b"]                                    # v3: 1.3 starts where 1.2b did; its take stays where it was
TAKE_AT = {k: list(v["take_at"]) for k, v in TIMING.items()}
TAKE_AT["1.3"] = [TAKE_AT["1.3"][0] + DUR["1.2b"]]
DUR["4.3"] += 0.40                                           # Tomas 25 Nov (plan §7 a): Father's take 0.4 s later, the
TAKE_AT["4.3"] = [TAKE_AT["4.3"][0], TAKE_AT["4.3"][1] + 0.40 + 0.25]   # guards' close gets 0.45 s between the lines;
DUR["4.3"] += 0.25                                           # v2 (review 26 Nov): 0.38 s of Father's silence before "Invite her."
DUR["4.3"] += 0.45                                           # v8 (Tomas 26 Nov): the close 0.95 s, the guards react in turn
TAKE_AT["4.3"][1] += 0.45                                    # (A pinches, B covers his mouth and turns away), Father after
SIP_ON = [False]                                             # 3.7's sip: tried v3/v4, read as "a phone" 3 rounds; Tomas 25 Nov:
DUR["3.7"] += 0.40 if SIP_ON[0] else 0.0                     # the silence without the sip, the cup at her chin (the board)


def lead(sid):
    return TAKE_AT[sid][0] if TAKE_AT[sid] else 0.15


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


BOARD = {s["id"]: s for s in ps.SHOTS}


# --- scene 1 ------------------------------------------------------------------------------------------------------------
HOLD0 = 0.4                                                 # G5: frame 0 complete and held 0.4 s before anything moves


def s11(t):
    """the tug of war: motion test A (approved v3) after a 0.4 s frame 0; its four pulls in the remaining 1.4 s, each
    faster. Drawn by test A's own function on board v4's set (the robot a step left of the door frame, as the board)."""
    ta = 0.0 if t < HOLD0 else 0.2 + (t - HOLD0) * (1.6 / (DUR["1.1"] - HOLD0))
    return pm_.shot_A(ta, v4=True)


def s12a(t):
    """the blind tears off its rail and drops over Don (0.25 s), lands; daylight in through the bare glass."""
    u = ease(t / 0.25)
    base = BOARD["1.2a"]
    def cast(k):
        heads = {}
        o, heads["don"] = ps.don(k, "don_door", "stand", "shock", (0, -0.6 * (1 - u)))
        if u >= 1.0:
            dp.blind_over(k, o["head"], ps.SC["don"])
        else:                                                # in the air: the slats alone (blind_over's face gap would
            hx, hy = o["head"]; sc_ = ps.SC["don"]           # draw a second face up there), falling onto him
            w, h = 150 * sc_, 300 * sc_
            top = lerp(pss.GY0 - 10, hy - 70 * sc_, u)
            c = k.c
            c.save(); c.translate(hx, top); c.rotate(0.10 * (1 - u))
            c.new_path(); c.rectangle(-w / 2, 0, w, h); c.set_source_rgb(0.93, 0.91, 0.86); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
            c.set_line_width(1.2)
            for j in range(1, 22):
                c.move_to(-w / 2 + 4, j * h / 22); c.line_to(w / 2 - 4, j * h / 22); c.stroke()
            c.set_line_width(2.2)
            for dx in (-w * 0.3, 0, w * 0.3):                # speed lines above it
                c.move_to(dx, -14); c.line_to(dx, -44); c.stroke()
            c.restore()
        if u > 0.5:
            ps.light_in(k)
        _, heads["robot"] = ps.robot(k, (pss.GX0 + 196, ps.F + 4), visor="sun")
        return heads
    return ps.S("1.2a", base["cam"], base["room"], cast)


HEARD_12B = 0.12                                             # 1.2b: the crash reaches them (two drawings in)


def s12b(t):
    """v2 (cold test 0/2 twice: "a cutaway with no setup"): they are chatting, Pam's cup on its way up; the crash: three
    heads snap to it, the cup jolts and stops halfway, held. The rigs' own poses and faces, the cup's pose interpolated."""
    import pm_ps
    hit = t >= HEARD_12B
    q = min(t, HEARD_12B) / HEARD_12B                         # the cup rising, mid .. halfway to her chin
    if hit:
        q = 0.5 - 0.18 * math.exp(-(t - HEARD_12B) * 14)     # the jolt down, then it stops where it is
    else:
        q = 0.5 * q
    a, b = pm_ps.P_POSES["cup_mid"], pm_ps.P_POSES["cup_chin"]
    pm_ps.P_POSES["cup_t"] = tuple(x + (y - x) * q for x, y in zip(a, b)); pm_ps.P_HANDS["cup_t"] = ("relax_s", "cup")
    hop = 12 * math.exp(-(t - HEARD_12B) * 18) if hit else 0.0   # the startle: all three jump a little, together
    def cast(k):
        heads = {}
        k.c.translate(0, -hop)
        _, heads["pam"] = ps.pam(k, "trio_pam", "cup_t", "frozen" if hit else "neutral", (-1, -0.1) if hit else (0.8, 0))
        _, heads["mom"] = ps.mom(k, "trio_mom", "folded", "stern" if hit else "unimpressed", (-1, 0) if hit else (-0.6, 0))
        _, heads["sofia"] = ps.sofia(k, "trio_sof", "hip_out", "surprised" if hit else "smile", (-1, 0) if hit else (-0.8, 0))
        k.c.translate(0, hop)
        return {n: (h[0], h[1] - hop, h[2]) for n, h in heads.items()}
    return ps.S("1.2b", BOARD["1.2b"]["cam"], BOARD["1.2b"]["room"], cast)


def s13(t):
    """Don frozen under the blind, whispering. The visible change (lesson 200): the fallen blind still sways from the
    crash and settles (review 25 Nov: the loose slat read as "run through him"; cut)."""
    base = BOARD["1.3"]
    def cast(k):
        heads = {}
        o, heads["don"] = ps.don(k, "don_door", "stand", "neutral", (0, 0))
        hx, hy = o["head"]
        sw = 0.05 * math.cos(t * 9.0) * math.exp(-t * 2.2)    # a damped sway about the rail on his head
        c = k.c
        c.save(); c.translate(hx, hy - 70 * ps.SC["don"]); c.rotate(sw); c.translate(-hx, -(hy - 70 * ps.SC["don"]))
        dp.blind_over(k, o["head"], ps.SC["don"])
        c.restore()
        return heads
    return ps.S("1.3", base["cam"], base["room"], cast)


LIFT_14 = (1.35, 1.75)                                      # 1.4: the roll comes up on "Without me." (take 0.15-2.30)
LOOK_14 = 2.3                                               # then, after his line, the three look at each other


def s14(t):
    base = BOARD["1.4"]
    u = ease((t - LIFT_14[0]) / (LIFT_14[1] - LIFT_14[0]))
    v = ease((t - LOOK_14) / 0.25)
    close = t >= LOOK_14 - 0.05                               # review 25 Nov: at phone size the look was invisible: a cut
    def cast(k):                                             # in to the three, their own faces (the rigs' existing ones)
        ps.LOOK_14[0] = v
        ps.LIFT_14[0] = u
        ps.FACES_14[0] = FACES_LOOK if close else None
        ps.ROLL_RIGHT_14[0] = True                           # v2: his box sits left of his head in 1.4a: the roll goes up right
        return ps.cast_14(k)
    return ps.S("1.4b" if close else "1.4a", ["pam", "mom", "sofia"] if close else ["don"], base["room"], cast)


FACES_LOOK = ("doubt", "stern", "eyebrow")                   # Pam worried, Mom narrowed, Sofía one brow up


# --- scene 2 ------------------------------------------------------------------------------------------------------------
def s21(t):
    """the tape rips toward the camera through the group: motion test D (v2, approved), its own camera."""
    return dict(pm_.shot_D(t), own_cam=True)


def s21b(t):
    """the robot rolls in to the throne, the card in its claw; SLAP on the throne's side; it rolls off, pleased."""
    base = BOARD["2.1b"]
    rx0, rf = ps.at("rob_throne")
    if t < 0.30:
        dx, ph = 45 * (1 - ease(t / 0.30)), "in"            # in from the right, its face clear of the rail
    elif t < 0.55:
        dx, ph = 0.0, "slap"
    else:
        dx, ph = 70 * ease((t - 0.55) / 0.25), "off"
    reach = ease((t - 0.22) / 0.14) if ph != "off" else 1 - ease((t - 0.55) / 0.12)
    def cast(k):
        heads = {}
        arm = (lerp(-60, -150, reach), lerp(-40, -10, reach))
        o, heads["robot"] = ps.robot(k, (rx0 + dx, rf), arms=(arm, (-8, 0)), tilt=(0.06 if ph != "slap" else 0.0) * (1 if ph == "in" else -1),
                                     visor=None)
        hx, hy = o["hands"][0]
        if ph == "in" or (ph == "slap" and t < 0.36):        # the card in its claw
            ps.pss.robot_card(k, hx + 14, hy - 44, ps.SC["robot"] * 1.3, ang=-0.12)
        else:                                                # pressed on: it stays on the throne's side
            ps.pss.robot_card(k, CARD_21B[0], CARD_21B[1], ps.SC["robot"] * 1.3, ang=-0.12)
        if ph == "slap" and 0.36 <= t < 0.48:                # SLAP
            c = k.c; c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
            cx_, cy_ = CARD_21B
            for ang in (-2.6, -2.1, -1.6, 0.5, 1.0):
                r0, r1 = 66 * ps.SC["robot"] * 1.3, 84 * ps.SC["robot"] * 1.3
                c.move_to(cx_ + math.cos(ang) * r0, cy_ + math.sin(ang) * r0 * 0.7); c.line_to(cx_ + math.cos(ang) * r1, cy_ + math.sin(ang) * r1 * 0.7); c.stroke()
            c.set_line_cap(0)
        return heads
    return ps.S("2.1b", base["cam"], base["room"], cast)


def _card_21b():
    """where the board's 2.1b presses the card (its claw at the slap, arms (-150, -10))."""
    import cairo as _c
    k = Ctx(_c.Context(_c.ImageSurface(_c.FORMAT_RGB24, 4, 4)), 0)
    o, _ = ps.robot(k, "rob_throne", arms=((-150, -10), (-8, 0)), visor=None)
    return (o["hands"][0][0] + 14, o["hands"][0][1] - 44)


CARD_21B = _card_21b()
SPIN_22 = (0.55, 0.95)                                       # 2.2: the spin, after he sees the tag


def s22(t):
    """Don walks in past the throne, sees the price tag swinging, spins the throne (the tag to the wall, the card to the
    room), and walks on without looking back. The spin is drawn by ps_set's opt-in SPIN (a cut-out turn)."""
    base = BOARD["2.2"]
    x1, f1 = ps.at("don_throne")
    walk = ease(t / 0.40)
    u = ease((t - SPIN_22[0]) / (SPIN_22[1] - SPIN_22[0]))
    ps.pss.SPIN[0] = u if SPIN_22[0] <= t <= SPIN_22[1] else None
    room = dict(base["room"], spun=t > SPIN_22[1])
    def cast(k):
        heads = {}
        bob = -5 * abs(math.sin(math.pi * t / 0.20)) if t < 0.40 else 0.0
        if t < SPIN_22[0]:
            pose, face, look = "stand", ("neutral" if t < 0.42 else "confused"), ((1, 0) if t < 0.42 else (0.6, -0.8))
        elif t <= SPIN_22[1]:
            pose, face, look = "push", "confused", (-1, -0.3)
        else:
            pose, face, look = "vest", "smug", (-1, 0.3)
        if t < SPIN_22[0] + 0.05:                            # continuity (cold sheet 25 Nov): the card the robot slapped on
            ps.pss.robot_card(k, CARD_21B[0], CARD_21B[1], ps.SC["robot"] * 1.3, ang=-0.12)   # in 2.1b, until the spin
        o, heads["don"] = ps.don(k, (x1 - 120 * (1 - walk), f1 + bob), pose, face, look)
        return heads
    return ps.S("2.2", base["cam"], room, cast)


def s23(t):
    """he stamps on his half (a short knee-drop and the floor lines), then the roll points at each of them in turn."""
    base = BOARD["2.3"]
    beats = ((0.35, 0.75, 100), (0.75, 1.15, 120), (1.15, 1.55, 140))   # (the roll kept off the rail)
    a = 120
    for t0, t1, ang in beats:
        if t >= t0:
            a = ang
    pose = (-30, 60, a, a - 60)
    stamp = 1 - ease(t / 0.18) if t < 0.30 else 0.0
    def extra(k, o):
        ps.roll_up(k, o)
        if t < 0.30:
            c = k.c; c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
            fx, fy = ps.at("don_mid")
            for sd in (-1, 1):
                c.move_to(fx + sd * 40, fy + 4); c.line_to(fx + sd * 64, fy - 4); c.stroke()
            c.set_line_cap(0)
    ps.P.setdefault("pam_pre", (ps.tape_x(55) + 70, 55))      # v2 (2 of 3: "Pam holds the roll"): the board's 2.3 had Pam beside
    cast = ps.cast_scene2(don_pose=pose, extra=extra, pam_at="pam_pre")   # him already; she crosses only in 2.4
    def c2(k):
        k.c.translate(0, -10 * stamp)
        h = cast(k)
        k.c.translate(0, 10 * stamp)
        return h
    return ps.S("2.3", base["cam"], base["room"], c2, story=["don"])


def s24(t):
    """Pam hops over the line to Don first, her cup level; lands (the board's landing marks); her phone stays put."""
    base = BOARD["2.4"]
    x1, f1 = ps.at("pam_don")
    x0 = ps.tape_x(55) + 70
    u = ease((t - 0.15) / 0.40)
    hop = 34 * math.sin(math.pi * u) if 0 < u < 1 else 0.0
    def cast(k):
        heads = {}
        P_ = dict(ps.P); ps.P["pam_don"] = (lerp(x0, x1, u), P_["pam_don"][1])
        try:
            if u >= 1.0:
                return ps.cast_24(k)
            k.c.translate(0, -hop)
            h = ps._cast_scene2_24(k)
            k.c.translate(0, hop)
            return h
        finally:
            ps.P.update(P_)
    return ps.S("2.4", base["cam"], base["room"], cast)


def s25(t):
    """he salutes (solemn) on his line; she half returns it with her cup hand; then hides a small smile in the cup."""
    base = BOARD["2.5"]
    up = ease((t - 0.05) / 0.20)
    def cast(k):
        heads = {}
        dpose = tuple(a_ + (b_ - a_) * up for a_, b_ in zip(ps.dp.POSES["stand"], ps.dp.POSES["salute"]))
        _, heads["don"] = ps.don(k, (372, ps.F + 62), dpose, "pleased", (0.6, 0), chin=1)
        if t < 1.05:
            pp, pf = "cup_mid", "neutral"
        elif t < 1.55:
            pp, pf = "half_salute", "quiet"
        else:
            pp, pf = "cup_chin", "quiet"
        _, heads["pam"] = ps.pam(k, (530, ps.F + 56), pp, pf, (-0.6, 0))
        return heads
    return ps.S("2.5", base["cam"], base["room"], cast)


def s26(t):
    """Mom plants both feet on the tape: a small stamp-stamp, then nothing moves but her mouth."""
    base = BOARD["2.6"]
    st = 0.0
    for t0 in (0.0, 0.16):
        if t0 <= t < t0 + 0.12:
            st = math.sin(math.pi * (t - t0) / 0.12)
    def cast(k):
        k.c.translate(0, -6 * st)
        h = ps.cast_26(k)
        k.c.translate(0, 6 * st)
        return h
    return ps.S("2.6", base["cam"], base["room"], cast)


def s27(t):
    """Sofía steps toward Don and stops mid-step (the heel stays back); her eyes go to the door."""
    base = BOARD["2.7"]
    u = ease(t / 0.35)
    def cast(k):
        heads = {}
        x, f = ps.at("sof_heel")
        _, heads["sofia"] = ps.sofia(k, (x - 8 * u, f), "stand", "smile", (-1, 0) if t < 0.55 else (1, -0.4), lean=-5 * u)
        return heads
    return ps.S("2.7", base["cam"], base["room"], cast)


def s29(t):
    """the robot reports, its barrier on the visor; it bobs on its wheel with its words."""
    base = BOARD["2.9"]
    lo = loud("2.9", t)
    def cast(k):
        heads = {}
        _, heads["robot"] = ps.robot(k, (300, ps.F + 60 - 6 * lo), visor="barrier")
        return heads
    return ps.S("2.9", base["cam"], base["room"], cast)


ROBOT_210B = (90, 1.6)                                       # 2.10b: closer, the robot on the line in the middle (searched: no sign cut)
REACT_210 = 2.2                                              # 2.10: after "Both.", 0.4 s on Don's face


def s210(t):
    """2.10a Don, admiring his line: "And you?"; 2.10b the robot on the tape, its arms open across it (test H's first
    0.8 s): "Both."; then back on Don's face, 0.4 s (the script)."""
    if t < TAKE_AT["2.10"][1] - 0.10:                        # v2 (cold test 2 of 3: "who asks 'And you?'"): Don close, as 2.10c
        return ps.S("2.10c", ["don"], BOARD["2.10"]["room"], ps.cast_210)
    if t < REACT_210:                                        # v2 (3 of 3: "a blank wall"): the robot in the middle of its frame
        sh = pm_.shot_H(min(0.79, t - (TAKE_AT["2.10"][1] - 0.10)))
        fx, fy, z = sh["cam"]
        return dict(sh, cam=(fx - ROBOT_210B[0] / z, fy, z * ROBOT_210B[1]), own_cam=True)
    def cast(k):
        heads = {}
        _, heads["don"] = ps.don(k, (ps.tape_x(140) - 190, ps.F + 140), "vest", "confused", (1, 0), chin=1)
        _, heads["robot"] = ps.robot(k, "rob_tape", arms=((-95, 0), (95, 0)), tilt=0.10)
        return heads
    return ps.S("2.10c", ["don"], BOARD["2.10"]["room"], cast)  # his face, close (its own locked camera)


def s211(t):
    """one push: he hauls it onto his side, it rolls straight back into him, he staggers: motion test H (v4, 3 of 3)."""
    return dict(pm_.shot_H2(t), own_cam=True)


# --- scene 3 ------------------------------------------------------------------------------------------------------------
MOM_31 = 1.40                                               # 3.1: Mom's line from 1.52; the cut in to her just before it


def s31(t):
    """the arm telescopes up, Don swings into his pose: motion test E's first 0.8 s (approved), then held on its lines;
    v3 (Tomas 25 Nov; cold test 3/3 "who says 'Chin up'?"): a short cut in to Mom for her line."""
    sh = pm_.shot_E(min(t, 0.79))
    if t >= MOM_31:
        return ps.S("3.1c", ["mom"], sh["room"], sh["cast"])   # its own locked camera, framed on her face
    return dict(sh, own_cam=True)


def s32(t):
    """the FLASH (one white drawing), the photo fills the screen, held: motion test E from 0.8 s."""
    return pm_.shot_E(0.80 + t)


TURN_33 = 0.35


def s33(t):
    """the robot asks, its "?" on the visor; it bobs with its words (the phone at its arm's tip, PUBLIC POST?)."""
    base = BOARD["3.3"]
    lo = loud("3.3", t)
    def cast(k):
        heads = {}
        _, heads["robot"] = ps.robot(k, (ps.at("rob_tape")[0], ps.at("rob_tape")[1] - 6 * lo), selfie=0.6, phone="public",
                                     visor="ask", arms=((-95, 0), (120, 40)))
        return heads
    return ps.S("3.3", base["cam"], base["room"], cast)


SINK_34, MEET_34, BACK_34 = (0.05, 0.45), 0.52, (0.80, 1.05)


def s34(t):
    """his raised arm tires and sinks; the robot slides the phone in under his thumb (the pad goes green); thumb back up,
    smug. He never looks. The board's payoff pose is the meeting; the raised arm is that pose's arm lifted."""
    base = BOARD["3.4"]
    th = ps.dp.POSES["thumbs"]
    hi = (th[0], th[1], th[2] + 38, th[3] + 20)              # his arm (frame right, the phone side) up, before it tires
    sink = ease((t - SINK_34[0]) / (SINK_34[1] - SINK_34[0])) - ease((t - BACK_34[0]) / (BACK_34[1] - BACK_34[0]))
    pose = tuple(a + (b - a) * sink for a, b in zip(hi, th))
    slide = ease((t - 0.20) / (MEET_34 - 0.20))
    p_ = ps.PHONE_34
    def cast(k):
        heads = {}
        ps.robot(k, "rob_tape", selfie=p_["sel"], phone="approved" if t >= MEET_34 else "public", arms=p_["arms"],
                 tele=lerp(-1.05, p_["tele"], slide), phone_s=p_["s"])
        _, heads["don"] = ps.don(k, (ps.tape_x(140) - 190, ps.F + 140), pose, "grin", (0, -0.3), chin=1)
        return heads
    return ps.S("3.4", base["cam"], base["room"], cast)


def s35(t):
    """PUBLIC POST? slides up and away; the posted card comes in under it."""
    u = ease((t - 0.15) / 0.40)
    def draw(k):
        c = k.c                                              # (ins_screen paints the whole frame: the background once,
        c.set_source_rgb(0.20, 0.20, 0.24); c.paint()        # then the two phones, so the first isn't painted over)
        c.save(); c.translate(0, -ps.H * u); ps.rp.phone_screen(k, 270, 500, 2.3, "approved"); c.restore()
        c.save(); c.translate(0, ps.H * (1 - u)); ps.rp.phone_screen(k, 270, 430, 2.95, "posted"); c.restore()
    return ps.S("3.5", "screen", draw=draw)


DING_36 = 0.30


def s36(t):
    """DING behind the glass: the silhouette lifts a glowing phone to its face; Don, in front, smiles on."""
    base = BOARD["3.6"]
    room = base["room"] if t >= DING_36 else dict(base["room"], silhouette=True)
    return ps.S("3.6", base["cam"], room, base["cast"])


SIP_37 = 2.06                                               # v3 (Tomas 25 Nov: "matomas gurkšnis"): after her line, a visible sip


def s37(t):
    """Pam sees the glow (eyes out), her mouth opens to warn him, she looks at Don posing; her cup comes up to her chin
    and she says it into the cup."""
    import pm_ps
    q = ease((t - 0.45) / 0.45) + SIP_ON[0] * (0.40 * ease((t - SIP_37) / 0.16) - 0.40 * ease((t - SIP_37 - 0.52) / 0.14))   # v4: the sip,
                                                             # held 0.36 s at her mouth (two 4 fps drawings), then down
    a, b = pm_ps.P_POSES["cup_mid"], pm_ps.P_POSES["cup_chin"]
    pm_ps.P_POSES["cup_t"] = tuple(x + (y - x) * q for x, y in zip(a, b)); pm_ps.P_HANDS["cup_t"] = ("relax_s", "cup")
    base = BOARD["3.7"]
    def cast(k):
        heads = {}
        sip = SIP_ON[0] and SIP_37 + 0.05 <= t < SIP_37 + 0.56
        face = "shock" if 0.15 <= t < 0.40 else ("quiet" if sip else "doubt")
        look = (1, -0.4) if t < 0.35 else ((0, -1) if sip else (-1, 0))   # eyes up into the cup: drinking, not filming
        _, heads["pam"] = ps.pam(k, "pam_don", "cup_t", face, look)
        return heads
    return ps.S("3.7", base["cam"], base["room"], cast)


# --- scene 4 ------------------------------------------------------------------------------------------------------------
def s41(t):
    """red neon over the booth, one flicker; bodyguard 1's black sleeve lifts the #TeamDon phone into the frame."""
    u = ease(t / 0.30)
    def draw(k):
        ps.BRIDGE_DROP[0] = 420 * (1 - u)
        try:
            ps.ins_booth_wide(k)
        finally:
            ps.BRIDGE_DROP[0] = 0.0
        if 0.10 <= t < 0.17:                                 # the neon's one flicker: the room drops a step
            k.c.set_source_rgba(0, 0, 0, 0.45); k.c.paint()
    return ps.S("4.1", "screen", draw=draw)


def s42(t):
    """the oily finger comes in along its line and lands on the heel, its print: motion test J."""
    ps.FINGER_42[0] = ease(min(1.0, t / 0.7))
    return BOARD["4.2"]


GB_43 = dict(lean=-0.08, turn=(-8, 0.12), pose=(-74, -82), hand="palm")   # v8: guard B recoils, head away, palm over mouth and nose
CLOSE_43V5 = (1.25, -230, -220)                              # was (1.45, -345, -302): both guards cut by the frame's edges
A_43, B_43 = 0.95, 1.90                                      # 4.3a the Client .. 4.3b the guards' close .. 4.3c Father


def s43(t):
    """4.3a "That one."; 4.3b the guards turn away and pinch their noses, the stink rises (no line); 4.3c Father: "Invite
    her." The board's three framings (BOOTH_PART_V4), drawn in turn."""
    part = 0 if t < A_43 else (2 if t < B_43 else 1)
    pu = (ease((t - A_43 - 0.02) / 0.20), ease((t - A_43 - 0.42) / 0.22))   # v8: B 0.4 s after A (Tomas: different gestures)   # v5 (review 26 Nov): the second
                                                             # guard 2 drawings later (5 left him unpinched in the 0.45 s close)
    def draw(k):
        ps.PART[0] = part
        ps.BOOTH_PART_V4[2] = CLOSE_43V5                     # v5 (26 Nov audit): the close wide enough for both guards' hands
        ps.PINCH_43[0] = pu if t < B_43 + 0.4 else 1.0
        ps.GUARD_B[0] = GB_43
        ps.STINK_RISE[0] = 60 * t
        try:
            return ps.ins_booth_43(k)
        finally:
            ps.PINCH_43[0] = 1.0; ps.STINK_RISE[0] = 0.0; ps.GUARD_B[0] = None
    return ps.S("4.3", "screen", draw=draw)


# --- scene 5 ------------------------------------------------------------------------------------------------------------
LIT_51 = 0.45                                               # the buzz; his phone lights at his face behind the glass (3.6's)


def s51(t):
    """Outside the glass: bodyguard 2's phone buzzes and lights; the room as the board's."""
    base = BOARD["5.1"]
    return ps.S("5.1", base["cam"], dict(base["room"], silhouette="phone" if t >= LIT_51 else True), base["cast"])


PEN_52 = ((0.20, 1, -74), (0.62, 2, -38), (1.02, 3, 0))     # (time, letters written, the nib's x from its last place)


def s52(t):
    """The gold pen writes H, R, ? across the CV's foot, a letter at a time; the hand moves on with the nib."""
    n, dx = 0, PEN_52[0][2] - 26
    for at, n_, dx_ in PEN_52:
        if t >= at:
            n, dx = n_, dx_
    lift = 10 * max(0.0, 1 - abs((t - 0.44) / 0.10)) + 10 * max(0.0, 1 - abs((t - 0.84) / 0.10))   # the nib up between letters
    base = BOARD["5.2"]
    def draw(k):
        was, wn = ps.PEN_C[0], ps.sp.CV_N[0]
        ps.PEN_C[0] = (was[0] + dx, was[1] - lift); ps.sp.CV_N[0] = n
        try:
            return base["draw"](k)
        finally:
            ps.PEN_C[0], ps.sp.CV_N[0] = was, wn
    return ps.S("5.2", "screen", draw=draw)


TREAT_AT = 1.25                                             # 5.3a the door, "Welcome." .. 5.3b the oil can


def s53(t):
    """5.3a: the robot welcomes Sofía at the door (she walks in, it bobs with its word). 5.3b: bodyguard 2 has handed it
    an oil can: it lifts the can beside its head, the heart comes on."""
    if t < TREAT_AT:
        return BOARD["5.3"]
    u = ease((t - TREAT_AT - 0.10) / 0.35)                   # the can up from its side
    heart = t >= TREAT_AT + 0.42
    def cast(k):
        a0, a1 = (-98, -22), ps.LARM_53[0]
        was, wc = ps.LARM_53[0], ps.CAN_53[0]
        ps.LARM_53[0] = (a0[0] + (a1[0] - a0[0]) * u, a0[1] + (a1[1] - a0[1]) * u)
        ps.CAN_53[0] = 0.5 * (1 - u)
        ps.HEART_53[0] = heart
        try:
            return ps.cast_53_treat(k)
        finally:
            ps.LARM_53[0], ps.CAN_53[0] = was, wc; ps.HEART_53[0] = True
    return dict(ps.S("5.3b", ps.TREAT_53, BOARD["5.3"]["room"], cast), own_cam=True)


WIDE_54 = 0.85                                              # 5.4a the wide (his door across the tape) .. 5.4b test C


def s54(t):
    """5.4a: wide, Don at his line looks across the tape at DON · CEO. 5.4b (test C): the foot lifts over the line, held
    0.6 s, back; he straightens his vest."""
    if t < WIDE_54:
        look = (0.2, 0) if t < 0.25 else (1, 0)
        def cast(k):
            heads = {}
            _, heads["don"] = ps.don(k, "don_line", "stand", "neutral", look)
            return heads
        return dict(ps.S("5.4a", ps.KEYS_V4["5.4"][0], BOARD["5.4"]["room"], cast), own_cam=True)
    return dict(pm_.shot_C(t - WIDE_54), room=BOARD["5.4"]["room"])


def s55(t):
    """test K: Sofía steps onto the tape, the CV at her chest, HR? up."""
    return dict(pm_.shot_K(t), own_cam=True)                # test K's camera: the board's 5.5


DY_56 = -40
CAM_56, WALK_56 = (-78, 26, 1.45), (-72, 46)               # v2 (cold test: her cross 0 of 2, Pam's box "a sign" 2 of 2): the
                                                             # camera lower and wider, her walk above Pam's box, 190 units long

def s56(t):
    """over Pam on the stool, frozen with the blind (test F's staging, the film's camera); beyond her Sofía walks across
    the tape, in the clear above Pam's line."""
    F, lerp = pm_.F, pm_.lerp
    u = ease((t - 0.45) / 1.25)
    tx = ps.tape_x(60)
    step = int(t * 5) % 2 if 0.45 < t < 1.70 else 1
    import pm_ps as _pm
    def fg(k):                                               # the shot's own switches, set only while its near layer draws
        ps.PAM_X_56[0], ps.PAM_DY_56[0], ps.STOOL_56[0], _pm.BLIND_W[0] = PAM_56, DY_56, True, 26
        try:
            return ps.fg_56(k)
        finally:
            ps.PAM_X_56[0], ps.PAM_DY_56[0], ps.STOOL_56[0], _pm.BLIND_W[0] = 160, 0, False, 0.0
    def cast(k):
        heads = {}
        _, heads["sofia"] = ps.sofia(k, (lerp(tx + WALK_56[0], tx + WALK_56[1], u), F + 60), "walk" if step == 0 else "stand",
                                     "smile", (1, -0.1))
        return heads
    return dict(ps.S("5.6", (tx + CAM_56[0], F + CAM_56[1], CAM_56[2]), BOARD["5.6"]["room"], cast, fg=fg,
                     story=["pam", "sofia"]), own_cam=True)


PAM_56 = 150
BUZZ_57 = (0.10, 0.75)


def s57(t):
    """Pam's phone in her hand: INVITATION · DAD; it buzzes (shakes 3 px) and settles."""
    base = BOARD["5.7"]
    on = BUZZ_57[0] <= t < BUZZ_57[1]
    jx = (3.0 if int(round(t * DPS)) % 2 else -3.0) if on else 0.0   # a shake per drawing (a 7.5 Hz sine sampled at 15 is 0)
    def draw(k):
        k.c.save(); k.c.translate(jx, 0)
        try:
            return base["draw"](k)
        finally:
            k.c.restore()
    return ps.S("5.7", "screen", draw=draw)


SHOT_FN = {"1.1": s11, "1.2a": s12a, "1.2b": s12b, "1.3": s13, "1.4": s14,
           "2.1": s21, "2.1b": s21b, "2.2": s22, "2.3": s23, "2.4": s24, "2.5": s25, "2.6": s26, "2.7": s27,
           "2.9": s29, "2.10": s210, "2.11": s211,
           "3.1": s31, "3.2": s32, "3.3": s33, "3.4": s34, "3.5": s35, "3.6": s36, "3.7": s37,
           "4.1": s41, "4.2": s42, "4.3": s43,
           "5.1": s51, "5.2": s52, "5.3": s53, "5.4": s54, "5.5": s55, "5.6": s56, "5.7": s57}
HOLDS = {"2.8": "the heel insert, held by the script (0.6 s at least)", "2.9b": "Sofía flat, only her mouth moves"}


def print_map():
    for sid in sorted(SHOT_FN):
        assert sid in BOARD, sid
        print("  %-5s -> %s" % (sid, SHOT_FN[sid].__name__))


CAMS = {}


def shot_at(sid, t):
    """the shot to draw at its time t, its camera locked to the board key frame's."""
    ps.ROOM_OWN[0] = False
    pss.GLASS_PHONE_V2[0] = sid.startswith("5")              # scene 5 only for now (3.6 keeps its tested look until Tomas says)
    sh = SHOT_FN[sid](t) if sid in SHOT_FN else BOARD[sid]
    if sh["cam"] == "screen":                                # an insert drawn in frame units: no camera to lock
        ps.NO_SHIFT[0] = True; ps.ROOM_OWN[0] = False
        return dict(sh, id=sid)
    if sh.get("own_cam"):                                    # a motion test's own (already the board's) camera
        ps.NO_SHIFT[0] = True; ps.ROOM_OWN[0] = True
        return dict(sh, id=sid)
    key = sh["id"]                                           # a cut inside a shot ("1.4b") has its own locked camera
    if key not in CAMS:
        ps.NO_SHIFT[0] = key != sid
        ps.render(BOARD[sid] if key == sid else sh); CAMS[key] = ps._last_cam[0]
        if key in NUDGE:                                     # screen px: the frame moved so no sign is cut (G3);
            fx, fy, z = CAMS[key]; nx, ny, zz = NUDGE[key]     # zz: closer, about the frame's centre
            CAMS[key] = (fx + nx / z, fy + ny / z, z * zz)
    cam = CAMS[key]
    if key in PUSH:                                          # v3: a push in from another camera (the board's wide)
        frm, t0_, t1_ = PUSH[key]
        if frm not in CAMS:
            ps.NO_SHIFT[0] = False; ps.render(BOARD[frm]); CAMS[frm] = ps._last_cam[0]
        u = ease((t - t0_) / (t1_ - t0_))
        cam = tuple(a + (b - a) * u for a, b in zip(CAMS[frm], CAMS[key]))
    ps.NO_SHIFT[0] = True
    ps.ROOM_OWN[0] = sid in SHOT_FN                          # the board's 1.1 room is its key frame's; the film's moves
    return dict(sh, cam=cam, id=sid)


PUSH = {"1.4a": ("1.4", 0.20, 0.50)}                         # v3 (cold test 2/2 "another room"): 1.4 opens wide (the door,
                                                             # the three, one room), then pushes in to Don


NUDGE = {"1.4b": (10, 10, 1.3), "1.4a": (0, 40, 1.0), "2.2": (26, 0, 1.0), "2.10c": (112, 0, 1.0), "3.1c": (52, 64, 1.0)}   # 2.2: the front tag (before the spin) whole                                   # 1.4b: $49,999, SHRED off the right, OUR FIRST CLIENT off the top


def draw(sid, t):
    import ps_checks as pc
    sh = shot_at(sid, t)                                     # (its camera probe renders first, outside the checks)
    pc.install_scene(ps); pc.begin()
    surf, msgs = ps.render(sh)
    msgs += pc.frame_checks(ps, ps.LAST[0])
    return surf, msgs


STILLS_VER = {1: 4, 2: 1, 3: 3, 4: 7, 5: 5}
STILLS4 = [("4.1", 0.05, "the neon, the phone coming up"), ("4.1", 0.5, "#TeamDon in his hand"), ("4.2", 0.3, "the finger"),
           ("4.2", 1.5, "the print on the heel"), ("4.3", 0.6, "That one."), ("4.3", 1.0, "the guards turn"),
           ("4.3", 1.3, "A pinches"), ("4.3", 1.75, "B turns away"), ("4.3", 2.05, "Father, silent"), ("4.3", 2.85, "Invite her.")]
STILLS3 = [("3.1", 0.3, "the arm telescopes"), ("3.1", 1.8, "Chin up: in to Mom"), ("3.2", 0.02, "FLASH"), ("3.2", 1.5, "the photo"),
           ("3.3", 0.8, "Public post?"), ("3.4", 0.10, "the arm up"), ("3.4", 0.40, "it sinks, the phone slides"),
           ("3.4", 0.60, "APPROVED"), ("3.4", 1.15, "thumb back up"), ("3.5", 0.35, "the slide"), ("3.6", 0.1, "before"),
           ("3.6", 0.8, "DING"), ("3.7", 0.25, "she sees it"), ("3.7", 1.5, "into the cup")]
STILLS2 = [("2.1", 0.5, "the tape rips"), ("2.1", 1.2, "the feet hop"), ("2.1b", 0.40, "SLAP: the card"),
           ("2.1b", 0.75, "it rolls off"), ("2.2", 0.50, "he sees the tag"), ("2.2", 0.72, "the spin"),
           ("2.2", 1.20, "the card to the room"), ("2.3", 0.10, "the stamp"), ("2.3", 0.9, "the roll points"),
           ("2.4", 0.35, "Pam hops over"), ("2.4", 1.0, "lands"), ("2.5", 0.6, "the salute"),
           ("2.5", 1.3, "her half salute"), ("2.5", 1.75, "the smile in the cup"), ("2.6", 0.08, "Mom plants"),
           ("2.7", 0.6, "Sofía stops mid-step"), ("2.9", 0.8, "Border breach"), ("2.10", 0.5, "And you?"),
           ("2.10", 1.6, "Both."), ("2.10", 2.4, "Don's face"), ("2.11", 0.4, "the haul"), ("2.11", 1.3, "the bump")]
STILLS5 = [("5.1", 0.2, "the silhouette"), ("5.1", 0.9, "his phone lights"), ("5.2", 0.3, "H"), ("5.2", 0.7, "HR"),
           ("5.2", 1.3, "HR?"), ("5.3", 0.6, "Welcome."), ("5.3", 1.40, "the can comes up"), ("5.3", 2.0, "the heart"),
           ("5.4", 0.5, "his door, across the tape"), ("5.4", 1.5, "the foot over the line"), ("5.4", 2.6, "the vest"),
           ("5.5", 0.3, "onto the tape"), ("5.5", 1.0, "HR? up"), ("5.6", 0.6, "Pam frozen"), ("5.6", 1.3, "Sofía crosses"),
           ("5.6", 2.2, "across"), ("5.7", 0.3, "the buzz"), ("5.7", 1.1, "INVITATION · DAD")]
STILLS = {5: STILLS5, 4: STILLS4, 3: STILLS3, 2: STILLS2, 1: [("1.1", 0.0, "frame 0, held 0.4 s"), ("1.1", 0.70, "pull 1: Don, down"), ("1.1", 1.05, "the robot, up"),
              ("1.2a", 0.45, "the blind lands"), ("1.3", 0.3, "the blind still sways"),
              ("1.4", 0.2, "1.4a opens wide"), ("1.4", 1.2, "pushed in: Don speaks"), ("1.4", 1.9, "the roll up"), ("1.4", 2.5, "the three look")]}


def stills(n):
    ps.gags_v5()
    import dh_cast as dc_; dc_.FRONT_HAND[0], dc_.FRONT_HAND_S[0], dc_.BACK_HAND[0] = "pinch", 0.8, "quiet"   # 4.3b (26 Nov): the pinch through limb's
    ps.PINCH_POSE[0], ps.PINCH_LEAD[0] = (-73, -93), 1.6       # audit 26 Nov: under the glasses, the hand up the chest (not sideways)
    import client_ps as cps_, hands_ps as hp_; cps_.POINT_V2[0] = ps.SHOT43_V8[0] = hp_.PINCH_V2[0] = True; cps_.POINT_SKIN[0], cps_.POINT_W[0] = (0.86, 0.64, 0.50), 1.3
    hp_.PINCH_V4[0] = ps.NOSE_43[0] = True; hp_.PINCH_CLOSE[0] = 1.0; cps_.POINT_LEN[0] = 0.85; ps.PHOTO_43[0] = True; ps.FATHER_SPOT[0] = 0.35   # v9 (review 26 Nov): the same photo on the table phone, his index at Sofía; Father lit, the rest dim   # v8 (review 26 Nov): his index clear, the phone whole, his box off it
    ps.BRIDGE_V2[0] = ps.ZOOM_42[0] = ps.STINK_V2[0] = ps.FATHER_V2[0] = True   # scene 4 v2 (review 26 Nov)
    dp.BLIND_GAP_FIX[0] = dp.ROLL_TAIL[0] = True              # v4 (Tomas 25 Nov): the eye stroke gone, the roll a roll
    ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
    ps.LIGHT_V5[0] = True; import pm_ps; pm_ps.MUG_RING[0] = True   # the film's look (review 25 Nov)
    print_map()
    tiles, faults = [], []
    for sid, t, label in STILLS[n]:
        surf, msgs = drawing(sid, t)
        faults += ["%s @%.2f: %s" % (sid, t, m) for m in msgs]
        tiles.append((surf, "%s  %.2f s  %s" % (sid, t, label)))
    tw, th, cols = 270, 480, (4 if len(tiles) <= 12 else 6)
    rows = (len(tiles) + cols - 1) // cols
    o = cairo.ImageSurface(cairo.FORMAT_RGB24, 20 + cols * (tw + 14), 20 + rows * (th + 34))
    c = cairo.Context(o); c.set_source_rgb(0.55, 0.55, 0.55); c.paint()
    for j, (im, lab) in enumerate(tiles):
        x, y = 20 + (j % cols) * (tw + 14), 20 + (j // cols) * (th + 34)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.set_font_size(13); c.move_to(x, y + th + 18); c.show_text(lab)
    p = os.path.join(OUT, "ps_film_s%d_stills_v%d.png" % (n, STILLS_VER[n]))
    o.write_to_png(p)
    print("wrote", p)
    for f in faults:
        print("FAULT", f)
    return not faults


# --- the film: drawings, lips, bubbles, sound ----------------------------------------------------------------------------
LEAD, LIP_AHEAD = 0.15, 2.0 / FPS                            # the take starts 0.15 s into its shot; lips 2 frames ahead
TAKES = os.path.join(ps.HERE if hasattr(ps, "HERE") else os.path.dirname(os.path.abspath(__file__)), "ps_voices", "takes")
_TAKE = {}


def _take(sid):
    import soundfile as sf
    if sid not in _TAKE:
        a, sr = sf.read(os.path.join(TAKES, "%s.wav" % sid))
        _TAKE[sid] = (a if a.ndim == 1 else a.mean(axis=1), sr)
    return _TAKE[sid]


BOX_TO_END = ("5.6",)                                       # the box stays to the cut (it lifted off the floor's DON: "signed - DON" 2 of 2)


def part_at(sid, t, bubble=False):
    """-> the index of the take speaking at t in shot sid (a split shot has two), or None. bubble: its box's window
    (on from the take's start, or after a push; off one drawing after the take ends)."""
    for i, (tk, at) in enumerate(zip(TIMING[sid]["takes"], TAKE_AT[sid])):
        a, sr = _take(tk)
        t0 = at - 0.02 if bubble else at - LIP_AHEAD
        if bubble and i == 0:
            t0 = max(t0, max((p_[2] for k_, p_ in PUSH.items() if k_.startswith(sid)), default=0.0))   # v3: not on a push
        if t0 <= t <= at + len(a) / sr + (1.0 / DPS if bubble else 0.0) or (bubble and sid in BOX_TO_END and t >= t0):
            return i
    return None


def loud(sid, t):
    """0..1: the take's loudness at the drawing (the of_film fallback rule: no viseme track for these takes)."""
    i = part_at(sid, t)
    if i is None:
        return 0.0
    a, sr = _take(TIMING[sid]["takes"][i])
    tt = t - TAKE_AT[sid][i] + LIP_AHEAD
    if tt < 0 or tt > len(a) / sr:
        return 0.0
    i0, i1 = int(tt * sr), int((tt + 1.0 / DPS) * sr)
    w = a[i0:i1]
    peak = max(1e-6, (a ** 2).mean() ** 0.5 * 3.0)
    return float(min(1.0, (w ** 2).mean() ** 0.5 / peak)) if len(w) else 0.0


def bubble_on(sid, t):
    return part_at(sid, t, bubble=True) is not None


def mouth(k, head, o):
    """the speaker's open mouth over the rig's own closed one, its height the take's loudness."""
    if o < 0.12:
        return
    hx, hy, r = head
    c = k.c
    c.save(); c.translate(hx, hy + 0.64 * r); c.scale(0.15 * r, 0.11 * r * (0.40 + 0.60 * o))   # on the drawn mouth line
    c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(0.33, 0.10, 0.10); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()


ALLOW = {"5.6": ("SIGN partly covered: 'DON'",),         # Pam, near, stands over the floor's DON
         "2.11": ("SIGN partly covered: 'DON'",),             # test H's own allowance: the floor's DON under his shoes
         "*": ("SIGN partly covered: 'SHRED'",)}              # SHRED_OK: someone passing in front of it (render_test)


def drawing(sid, t):
    sh = shot_at(sid, t)
    line = TIMING[sid]["line"]
    bp = part_at(sid, t, bubble=True) if line else None
    split = line and len(ps.says(line)) > 1
    if bp is not None and not (sid == "1.4" and t >= LOOK_14 - 0.05):
        ps.PART[0] = bp if split else None                   # a split shot's box: the line being said
        try:
            surf, msgs = ps.board_frame(sh, line)
        finally:
            ps.PART[0] = None
    else:
        import ps_checks as pc
        pc.install_scene(ps); pc.begin()
        surf, msgs = ps.render(sh)
    msgs = msgs + __import__("ps_checks").frame_checks(ps, ps.LAST[0])
    msgs = [m for m in msgs if not any(m.startswith(a) for a in ALLOW.get(sid, ()) + ALLOW["*"])]
    lp = part_at(sid, t)
    who = ps.says(line)[lp][0] if (line and lp is not None) else None
    if who and who in ps.LAST[0]:
        if who == "robot":                                   # no mouth: the robot bobs on its wheel with its words (of_film s32)
            pass
        else:
            mouth(Ctx(cairo.Context(surf), 0), ps.LAST[0][who], loud(sid, t))
    return surf, msgs


def sound(n, path):
    """the scene's stretch: the takes at their shots, the effects from of_sound's synth (reused), room tone; -15 LUFS."""
    import numpy as np, soundfile as sf
    import of_sound as osd
    SR = osd.SR
    starts, acc = {}, 0.0                                    # the film's own cut (v3: 1.2b out)
    for sid in SCENES[n]:
        starts[sid] = acc; acc += DUR[sid]
    total = acc
    buf = np.zeros(int((total + 0.3) * SR))
    for sid in SCENES[n]:
        st = starts[sid]
        for tk, at in zip(TIMING[sid]["takes"], TAKE_AT[sid]):
            a, sr = _take(tk)
            if sr != SR:
                from scipy.signal import resample_poly
                a = resample_poly(a, SR, sr)
            osd.put(buf, a, st + at, 1.0)
    def rattle_run(d, pitch):                                # the slats running down or up: a burst of clicks
        out = np.zeros(int(d * SR))
        for j in range(int(d * 40)):
            c_ = osd.rattle() * (0.5 + 0.5 * osd.rng.random())
            i = int((j / 40.0 + 0.004 * osd.rng.random()) * SR)
            out[i:i + len(c_)] += c_[:max(0, len(out) - i)]
        return osd.hp(out, max(1, int(6 / pitch)))
    def tone(f0, f1, d, k_=8.0):
        tt = osd.t_(d); ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(tt))) / SR
        return np.sin(ph) * np.minimum(1.0, tt / 0.005) * np.exp(-tt * k_)
    if n == 5:                                               # the sound map (plan v2 §2: buzz, pen, knocks, clink, heels, buzz)
        S_ = starts
        import sound_bc_mix as bm_
        osd.put(buf, osd.lp(bm_.buzz_phone(0.5), 4), S_["5.1"] + LIT_51 - 0.25, 0.22)   # 5.1 outside, muffled
        for at, _n, _dx in PEN_52:                            # 5.2 a scratch per letter
            sc = osd.hp(osd.noise(0.16), 3) * np.sin(np.pi * osd.t_(0.16) / 0.16) * (1 + 0.5 * np.sin(2 * np.pi * 55 * osd.t_(0.16)))
            osd.put(buf, sc, S_["5.2"] + at - 0.12, 0.16)
        for j in range(3):                                    # 5.3 three knocks, then the latch
            osd.put(buf, osd.slam() * 0.22, S_["5.3"] + 0.0 + 0.11 * j, 0.28)
        osd.put(buf, tone(2100, 2100, 0.25, 9) + 0.5 * tone(3150, 3150, 0.25, 12), S_["5.3"] + TREAT_AT + 0.40, 0.14)   # the can: a clink
        osd.put(buf, bm_.chime([1319, 1568], gap=0.08, d=0.4), S_["5.3"] + TREAT_AT + 0.45, 0.10)                    # the heart
        tt = osd.t_(0.04); clk = osd.hp(osd.noise(0.04), 2) * np.exp(-tt * 120)
        for j in range(5):                                    # 5.6 her heels across (a step every 0.2 s, test F)
            osd.put(buf, clk, S_["5.6"] + 0.6 + 0.2 * j, 0.45)
        osd.put(buf, bm_.buzz_phone(BUZZ_57[1] - BUZZ_57[0]), S_["5.7"] + BUZZ_57[0], 0.38)   # 5.7 Pam's phone
    if n == 4:                                               # the sound map (plan v2 §7)
        S_ = starts
        for b in range(int(total / 0.48) + 1):                # the club's bass, low, through the whole stretch
            osd.put(buf, tone(55, 48, 0.30, 9), b * 0.48, 0.30)
        osd.put(buf, tone(120, 120, 0.6, 1.0) * 0.5, S_["4.1"], 0.06)                 # 4.1 the neon's hum
        sm = osd.lp(osd.noise(0.12), 5) * np.exp(-osd.t_(0.12) * 25)
        osd.put(buf, sm, S_["4.2"] + 0.70, 0.35)                                      # 4.2 the smudge as it lands
        sn = osd.hp(osd.noise(0.25), 2) * np.sin(np.pi * osd.t_(0.25) / 0.25)
        osd.put(buf, sn, S_["4.3"] + A_43 + 0.05, 0.12)                               # 4.3b a sharp sniff
        osd.put(buf, sn[::-1] * 0.7, S_["4.3"] + A_43 + 0.47, 0.09)                  # v8: guard B, a muffled huff
        osd.put(buf, osd.hp(osd.noise(0.4), 3) * np.sin(np.pi * osd.t_(0.4) / 0.4), S_["4.3"] + TAKE_AT["4.3"][1] + 1.45, 0.20)  # send
    if n == 3:                                               # the sound map (plan v2 §2)
        S_ = starts
        wh = tone(300, 900, 0.5, 2.5) * (1 + 0.4 * np.sin(2 * np.pi * 60 * osd.t_(0.5)))
        osd.put(buf, wh, S_["3.1"] + 0.02, 0.10)                                    # 3.1 the servo whir
        tt = osd.t_(0.06); sh_ = osd.hp(osd.noise(0.06), 2) * np.exp(-tt * 70)
        osd.put(buf, sh_, S_["3.2"] + 0.0, 0.6); osd.put(buf, sh_, S_["3.2"] + 0.05, 0.4)   # 3.2 the shutter
        osd.put(buf, tone(1320, 1320, 0.35, 6) + 0.6 * tone(1760, 1760, 0.35, 6), S_["3.4"] + MEET_34, 0.18)   # 3.4 chime
        osd.put(buf, osd.hp(osd.noise(0.35), 3) * np.sin(np.pi * osd.t_(0.35) / 0.35), S_["3.5"] + 0.15, 0.25)  # whoosh
        sl = osd.lp(osd.noise(0.22), 4) * np.sin(np.pi * osd.t_(0.22) / 0.22) ** 2
        if SIP_ON[0]:
            osd.put(buf, sl, S_["3.7"] + SIP_37 + 0.10, 0.30); osd.put(buf, sl, S_["3.7"] + SIP_37 + 0.34, 0.22)                          # 3.7 the sip (a small slurp)
        ding = tone(1046, 1046, 0.9, 3.5) + 0.5 * tone(1568, 1568, 0.9, 4.5)
        osd.put(buf, osd.lp(ding, 6), S_["3.6"] + DING_36, 0.16)                   # 3.6 DING, outside, muffled
    if n == 2:                                               # the sound map (plan v2 §2)
        S_ = starts
        sc_ = osd.hp(osd.noise(0.55), 3) * np.exp(-osd.t_(0.55) * 2.5)            # 2.1 the tape's long screech
        sc_ = sc_ * (0.6 + 0.4 * np.sin(2 * np.pi * 34 * osd.t_(0.55)))
        osd.put(buf, sc_ + 0.4 * tone(2400, 1600, 0.55, 3.0), S_["2.1"] + 0.25, 0.35)
        osd.put(buf, tone(1500, 1500, 0.09, 30), S_["2.1b"] + 0.10, 0.20)          # 2.1b its beep, the clip, the SLAP
        osd.put(buf, osd.slam() * 0.5, S_["2.1b"] + 0.36, 0.35)
        osd.put(buf, rattle_run(0.40, 0.8), S_["2.2"] + SPIN_22[0], 0.30)          # 2.2 the casters spin
        osd.put(buf, osd.slam() * 0.4, S_["2.3"] + 0.02, 0.45)                     # 2.3 the stamp
        osd.put(buf, osd.slam() * 0.25, S_["2.4"] + 0.55, 0.30)                    # 2.4 she lands
        osd.put(buf, osd.slam() * 0.2, S_["2.6"] + 0.0, 0.25); osd.put(buf, osd.slam() * 0.2, S_["2.6"] + 0.16, 0.25)
        tt = osd.t_(0.04); clk = osd.hp(osd.noise(0.04), 2) * np.exp(-tt * 120)
        osd.put(buf, clk, S_["2.7"] + 0.34, 0.5)                                    # 2.7 the heel click
        osd.put(buf, tone(880, 880, 0.12, 12), S_["2.9"] + 0.02, 0.15); osd.put(buf, tone(660, 660, 0.14, 12), S_["2.9"] + 0.15, 0.15)
        sq = lambda: tone(1800, 2500, 0.12, 6) * (1 + 0.3 * np.sin(2 * np.pi * 40 * osd.t_(0.12)))
        osd.put(buf, sq(), S_["2.10"] + TAKE_AT["2.10"][1] - 0.15, 0.10)          # 2.10 the wheels squeak
        H_ = dict(roll=0.40, hit=0.65) if pm_.VER["H"] >= 4 else dict(roll=pm_.H2["back"], hit=pm_.H2["hit"])   # test H v4: no
        osd.put(buf, sq(), S_["2.11"] + H_["roll"], 0.10); osd.put(buf, sq(), S_["2.11"] + H_["roll"] + 0.12, 0.10)  # haul; it
                                                             # rolls back from 0.40 and meets him at 0.65 (h2_state)
        bonk = osd.slam() * 0.6; bonk[:int(0.4 * SR)] += tone(140, 70, 0.4, 7)       # BONK on the hit
        osd.put(buf, bonk, S_["2.11"] + H_["hit"], 0.6)
    if n == 1:
        def rattle_run(d, pitch):                            # the slats running down or up: a burst of clicks
            out = np.zeros(int(d * SR))
            for j in range(int(d * 40)):
                c_ = osd.rattle() * (0.5 + 0.5 * osd.rng.random())
                i = int((j / 40.0 + 0.004 * osd.rng.random()) * SR)
                out[i:i + len(c_)] += c_[:max(0, len(out) - i)]
            return osd.hp(out, max(1, int(6 / pitch)))
        for k_, (a_, b_, kind, _w) in enumerate([x for x in pm_.TUG if x[2] != "hold"]):
            ta = HOLD0 + (a_ - 0.2) * ((DUR["1.1"] - HOLD0) / 1.6)
            tb = HOLD0 + (b_ - 0.2) * ((DUR["1.1"] - HOLD0) / 1.6)
            osd.put(buf, rattle_run(tb - ta, 1.0 + 0.25 * k_), ta, 0.25 + 0.08 * k_)   # rising, each faster
        st = starts["1.2a"]
        crash = osd.slam() * 1.0
        osd.put(buf, crash, st + 0.20, 0.9)                  # the blind lands
        osd.put(buf, rattle_run(0.45, 1.6), st + 0.18, 0.6)  # the slats
    rt = osd.room(len(buf) / SR + 0.01)[:len(buf)]; buf[:len(rt)] += rt * 0.012
    tmp = path + ".raw.wav"
    x = buf / (np.abs(buf).max() + 1e-9) * 0.5
    sf.write(tmp, x.astype(np.float32), SR)
    from scipy.ndimage import minimum_filter1d               # of_sound.master's loop (it writes 13's file, so not called):
    g, ceil = 1.0, 10 ** (-5.0 / 20)                         # one gain to -15 LUFS, a look-ahead limiter on the peak
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
    os.remove(tmp)
    return I, P


HOLD_D = 5                                                   # drawings (0.33 s), as of_film


def film(n, ver=1):
    import subprocess, shutil
    ps.gags_v5()
    import dh_cast as dc_; dc_.FRONT_HAND[0], dc_.FRONT_HAND_S[0], dc_.BACK_HAND[0] = "pinch", 0.8, "quiet"   # 4.3b (26 Nov): the pinch through limb's
    ps.PINCH_POSE[0], ps.PINCH_LEAD[0] = (-73, -93), 1.6       # audit 26 Nov: under the glasses, the hand up the chest (not sideways)
    import client_ps as cps_, hands_ps as hp_; cps_.POINT_V2[0] = ps.SHOT43_V8[0] = hp_.PINCH_V2[0] = True; cps_.POINT_SKIN[0], cps_.POINT_W[0] = (0.86, 0.64, 0.50), 1.3
    hp_.PINCH_V4[0] = ps.NOSE_43[0] = True; hp_.PINCH_CLOSE[0] = 1.0; cps_.POINT_LEN[0] = 0.85; ps.PHOTO_43[0] = True; ps.FATHER_SPOT[0] = 0.35   # v9 (review 26 Nov): the same photo on the table phone, his index at Sofía; Father lit, the rest dim   # v8 (review 26 Nov): his index clear, the phone whole, his box off it
    ps.BRIDGE_V2[0] = ps.ZOOM_42[0] = ps.STINK_V2[0] = ps.FATHER_V2[0] = True   # scene 4 v2 (review 26 Nov)
    dp.BLIND_GAP_FIX[0] = dp.ROLL_TAIL[0] = True              # v4 (Tomas 25 Nov): the eye stroke gone, the roll a roll
    ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
    ps.LIGHT_V5[0] = True; import pm_ps; pm_ps.MUG_RING[0] = True
    print_map()
    d = "/tmp/ps_film_s%d" % n
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    frames, faults = [], {}
    for sid in SCENES[n]:
        m = int(round(DUR[sid] * DPS))
        for i in range(m):
            t = i / DPS
            surf, msgs = drawing(sid, t)
            for x in msgs:
                faults.setdefault("%s: %s" % (sid, x.split(" at ")[0]), []).append(round(t, 2))
            p = os.path.join(d, "%04d.png" % len(frames)); surf.write_to_png(p); frames.append(p)
    import hashlib                                           # lesson 200 (plan §3.1): a shot whose drawings never change fails,
    k0 = 0                                                   # unless the script holds it (HOLDS, with the reason)
    for sid in SCENES[n]:
        m = int(round(DUR[sid] * DPS))
        hs = {hashlib.md5(open(p, "rb").read()).hexdigest() for p in frames[k0:k0 + m]}
        k0 += m
        if len(hs) == 1 and sid not in HOLDS:
            faults.setdefault("%s: STILL: no drawing changes (lesson 200)" % sid, []).append(0.0)
    lst = os.path.join(d, "list.txt")
    with open(lst, "w") as f:
        for p in frames:
            f.write("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
        f.write("file '%s'\n" % frames[-1])
    wav = os.path.join(d, "s%d.wav" % n)
    I, P = sound(n, wav)
    mp4 = os.path.join(OUT, "ps_film_s%d_v%d_540.mp4" % (n, ver))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                           "-vf", "fps=%d,format=yuv420p" % FPS, "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", mp4])
    sheets(n, frames)
    print("wrote %s  (%d drawings, %.1f LUFS, peak %.1f dB)" % (mp4, len(frames), I, P))
    real = {}
    for k_, v in faults.items():                             # of_film's held_only: a prop passing through a dead zone in a
        if ("ZONE" in k_ or "SIGN cut" in k_) and len(v) < HOLD_D:   # move (or a sign crossing the edge in a camera move) is not a fault; 5 drawings is
            print("passing %s  (%d drawings, from %.2f s)" % (k_, len(v), v[0]))
            continue
        real[k_] = v
        print("FAULT %s  (%d drawings, from %.2f s)" % (k_, len(v), v[0]))
    return not real


STRIP8 = {1: (0.0, 2.8), 2: (1.6, 4.4), 3: (7.6, 10.4), 4: (2.6, 5.0), 5: (4.0, 6.8)}                      # 2: 2.1b's slap and 2.2's spin


def sheets(n, frames):
    """the cold viewers' 4 fps sheet of the scene and an 8 fps strip of its first 2.8 s (1.1-1.2b), time stamps."""
    a_, b_ = STRIP8.get(n, (0.0, 2.8))                        # the 8 fps strip: the scene's fastest stretch
    for fps, span, name in ((4, (0.0, len(frames) / DPS), "sheet4"), (8, (a_, b_), "strip8")):
        picks = [(span[0] + j / fps, frames[min(len(frames) - 1, int(round((span[0] + j / fps) * DPS)))])
                 for j in range(int((span[1] - span[0]) * fps) + 1)]
        tw, th, cols = 180, 320, 8
        rows = (len(picks) + cols - 1) // cols
        o = cairo.ImageSurface(cairo.FORMAT_RGB24, 20 + cols * (tw + 10), 20 + rows * (th + 26))
        c = cairo.Context(o); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
        for j, (t, p) in enumerate(picks):
            x, y = 20 + (j % cols) * (tw + 10), 20 + (j // cols) * (th + 26)
            im = cairo.ImageSurface.create_from_png(p)
            c.save(); c.translate(x, y); c.scale(tw / 540, tw / 540); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
            c.set_source_rgb(1, 1, 1); c.set_font_size(13); c.move_to(x, y + th + 16); c.show_text("%d  %.2f s" % (j + 1, t))
        o.write_to_png("/tmp/ps_film_s%d/%s.png" % (n, name))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "film":
        sys.exit(0 if film(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1) else 1)   # a new version, a new name
    if len(sys.argv) > 2 and sys.argv[1] == "stills":
        sys.exit(0 if stills(int(sys.argv[2])) else 1)
    print(__doc__)
