"""DADDY'S HOME v8, scene 7 "The Arrival": v7's scene (dh_anim7.sc: clock, takes, mix) through dh_anim_v8 (v8 bubbles,
dead zones, set_gate), with the shots that failed redrawn:
  - the throne on its set mark (452; v7 418): Don in front of it where scene 6 left him, the line-up and the cameras with them
  - 9.4, 9.4', 9.5'' (the thumb): see THUMB below (hands audit #6: his raised arm behind the price tag, his body cut by
    the frame's edge: "an arm without a body, holding the tag"; rules: a finger near a sign = holding it)
  python3 dh_anim7_v8.py [gate|nobub]  ->  ../daddys-home/dh_s7_anim_v8.mp4"""
import sys
import math
import cairo
import kit
import dh_props as dp
import dh_layout as dl
import dh_scenes as ds
import dh_poses as dq
import dh_cast as dc
import dh_anim7 as V7
import dh_anim_v8 as E
import dh_anim3_v8 as A3
import hands_ps as hp
import dh_animatic as da

sc = V7.sc
F, CH, DS_ = V7.F, V7.CH, V7.DS_
D = 34                                                      # the throne's mark (452) minus v7's 418

# ---- the set: as scene 6 v8 left it (the same patch as dh_anim6_v8)
ds.THR5 = V7.THR5 = dl.CH[0]
ds.DON6 = V7.DON6 = (ds.DON6[0] + D, ds.DON6[1]) if ds.DON6[0] < 450 else ds.DON6
ds.HD6 = dl.hd(ds.DON6[0], ds.DON6[1], 0.60)
ds.LINE6 = V7.LINE6 = ((ds.DON6[0], F + 26), (ds.DON6[0] + 72, F + 6), (ds.DON6[0] + 162, F + 8))
ds.CAM6B = (ds.DON6[0] + 92, 762, 1.95)
ds.FA2 = V7.FA2 = (376, ds.FA2[1])                          # Father's two steps in end nearer Don (v7 330, 88 from him): the room on
#                                                             his left holds his "Approved." box, and the frame holds the shredder's SHRED whole
ds.HF2 = dl.hd(ds.FA2[0], ds.FA2[1], ds.FS)
CAM2 = (398, 668, 1.8)                                                               # the two-shot: Father and Don whole, the tag and the crown in, as big as fits
sc.CAM8 = {"9.1r": (ds.DON6[0] + 64, 740, 1.75),            # the line-up whole: Don and the tag no longer cut at the left edge
           "9.4": CAM2, "9.4'": CAM2, "9.5''": CAM2}

# ---- the thumb (hands audit #6). v7's poses: (-150, -40) up, (-146, -34) after "Approved." (and in 9.5''): the arm straight up
# along the price tag, "holding the tag". THUMB swaps them where don_zipped is called with them; a test picks THUMB.
THUMB = {(-150, -40, 10, 0): (-150, -40, 10, 0), (-146, -34, 4, 0): (-146, -34, 4, 0)}
_dz = getattr(dq.don_zipped, "_v7", dq.don_zipped)


def _don_zipped(k, x, feet, s, pose=None, *a, **kw):        # dh_poses calls it positionally too (don_block)
    if pose is None:
        return _dz(k, x, feet, s, *a, **kw)
    if not isinstance(pose, str) and tuple(pose) in THUMB:
        pose = THUMB[tuple(pose)]
    return _dz(k, x, feet, s, pose, *a, **kw)


_don_zipped._v7 = _dz
dq.don_zipped = _don_zipped

# ---- the thumb, drawn here (v7: s7_thumb / _thumb_don): the series' thumbs-up hand (hands_ps "thumb") in place of v7's
# rectangle on a fist, which read as "a raised index finger" and "a phone" 2 of 2, and the shake as real movement (v7's white
# "(( ))" marks read as "a ringing phone" 2 of 2).
GEST = ["relax", "palm"]                                     # hp.reset(first hand drawn, second): the far hand raised
THUMB_W = 1.3
# Round 1 (2 viewers, 3 heights, the "thumb" hand on his near hand): no phone 2/2, but beside Father it touched his arm.
# Round 2 (the far hand, mute test of the scene): the story 2/2, no phone 2/2, but the thumb read "an index finger" 2/2 (the
# third time) and the arm "a white V". Rule 178, Tomas (24 Nov): change the gesture. Round 3: his hand up, palm open, the
# elbow bent: "me! the human!" ("clearest" 2/2: "volunteering", "that's me"; no phone 2/2; the straighter arms read "a pole").
# After "Approved." it stays up, forgotten.
THUMB[(-150, -40, 10, 0)] = (-8, 0, 120, 60)
THUMB[(-146, -34, 4, 0)] = (-8, 0, 116, 56)


def thumb_don(k, n, up, shake, face, look, sink, father=None):
    dp.ceo_chair(k, ds.THR5, CH[1], CH[2])
    ds._arm_phone(k)
    if father:
        dc.father(k, ds.FA2[0], ds.FA2[1], ds.FS, face=father[0], look=father[1])
    pose = THUMB[(-150, -40, 10, 0)] if up else THUMB[(-146, -34, 4, 0)]
    if shake:                                               # it shakes: the forearm trembles, 2 degrees each way
        pose = tuple(pose[:3]) + (pose[3] + (2 if n % 2 else -2),)
    hp.reset(*GEST)
    real, cnt = kit.HAND[0], [0]

    def big(k_, hx, hy, w, *a):                             # the thumbs-up hand 1.3x: at feed size the thumb read as "a finger" (1 of 2)
        g = GEST[min(cnt[0], 1)]; cnt[0] += 1
        return real(k_, hx, hy, w * (THUMB_W if g in ("thumb", "palm") else 1.0), *a)
    kit.HAND[0] = big
    try:
        d = _dz(k, ds.DON6[0], ds.DON6[1] + sink, 0.60, pose=pose, face=face, look=look)
    finally:
        kit.HAND[0] = real
        hp.reset()
    return d


def _way_don(k, pose):
    hp.reset(*GEST)
    real = kit.HAND[0]
    kit.HAND[0] = lambda k_, hx, hy, w, *a: real(k_, hx, hy, w * THUMB_W if hp._N[0] >= 1 else w, *a)
    try:
        return _dz(k, ds.DON6[0], ds.DON6[1], DS_, pose=pose, face="happy", look=(-1, 0))
    finally:
        kit.HAND[0] = real
        hp.reset()


def r_offer(s, k, o, t, tt, n):                             # 9.4: the arm comes up from his side to the thumb
    i = V7.idx(t)
    if i < 3:
        # the way up with the elbow bent from the first drawing (a straight in-between slanted down onto the shredder:
        # "a pole", "pressing the SHRED box" 2/2)
        THUMB["_way"] = ((-8, 0, 20, 110), (-8, 0, 60, 90), (-8, 0, 95, 72))[i]
        dp.ceo_chair(k, ds.THR5, CH[1], CH[2])
        dc.father(k, ds.FA2[0], ds.FA2[1], ds.FS, face="hard", look=(1, 0))
        thumb_way = THUMB["_way"]
        THUMB["_now"] = thumb_way
        d = _way_don(k, thumb_way)
    else:
        thumb_don(k, n, True, False, "happy", (-1, 0), 0, father=("hard", (1, 0)))


def r_approved(s, k, o, t, tt, n):                          # 9.4': "Approved." to the robot; the thumb stays up, shaking
    d = thumb_don(k, n, False, True, "neutral", (-1, 0.5), 9, father=("talk", (-1, 0)))
    ds._sweat8(k, d["head"], 1)
    hd = (ds.FA2[0], ds.FA2[1] - 302 * ds.FS)
    V7.father_mouth(k, hd, s.loud("9.4", tt))
    if s.speaking("9.4", tt):
        o["say"] = ("Approved.", (hd[0] - 26, hd[1] + 28 * ds.FS), -1, True, -20, 170)


def r_react(s, k, o, t, tt, n):                             # 9.5'': frozen, the thumb still up, no longer shaking
    dc.father(k, ds.FA2[0], ds.FA2[1], ds.FS, face="hard", look=(-1, 0))
    d = thumb_don(k, n, False, False, "shock", (-1, 0), 9)
    V7.A.fear(k, d["head"], DS_, "o")
    ds._sweat8(k, d["head"], 2)


# ---- 9.2': his one step, toward us (v7: a second black leg and shoe drawn under his feet, "a black blob at his foot" 2/2)
def r_step(s, k, o, t, tt, n):
    u = V7.A.ease(min(1.0, t / 0.5))
    dl._guards(k, ds.GAP7[0], ds.GAP7[1])                  # nothing else moves
    lift = 5 * (1 - abs(2 * u - 1)) if 0 < u < 1 else 0   # up over the step, down onto the front foot
    fy, sc_ = F + 22 + 12 * u, ds.FS * (1 + 0.05 * u)
    dc.father(k, 125, fy - lift, sc_, look=(0.3, 0.1))


# ---- 9.5': the hop, the robot off the floor and its shadow on it (v7: impact dashes that rose with it, "floating dashes" 2/2)
def r_hop(s, k, o, t, tt, n):
    up = V7.seq(t, [0, 10, 18, 14, 4, 0, 6, 2, 0])
    rx, ry = da.RB[0], da.RB[1]
    c = k.c
    w = 30 * (1 - up / 40.0)
    c.set_source_rgba(0, 0, 0, 0.20); c.save(); c.translate(rx, ry + 8); c.scale(1, 0.22); c.arc(0, 0, w, 0, 6.2832); c.fill(); c.restore()
    c.save(); c.translate(0, -up); da._rb("tick")(k, o); c.restore()
    if s.speaking("9.5", tt):
        o["say"] = ("Welcome, majority shareholder.", (da.RH[0] + 24, da.RH[1] + 4 - up), 1, False, 20, 200)


sc.DRAW.update({"9.2'": r_step, "9.4": r_offer, "9.4'": r_approved, "9.5'": r_hop, "9.5''": r_react})


# ---- v8c (24 Nov, Tomas: "Father presses APPROVE himself"): who approves read "Don" 2/2 (whole-film and scene tests): his
# raised hand and Father's box beside him. Now: 9.4 is Don alone, his hand up ("me!"); 9.4' cuts back to Father at the robot
# by the door (9.3's frame, everyone on his mark): without a look at Don he presses the robot's chest himself, "Approved.",
# and its face goes green. Father walks to Don off the screen before 9.5''. Lessons: 179 (his own shoulder, in reach, the
# elbow bent), 207 (a press is a point), contact all the way, 263, 417/264.
PRESS = [(218.0, 706.0)]                                    # the robot's face: its screen (its chest is below his hand's reach)
FARM = {}


STEP = [24.0]                                               # his one step to the robot (from 9.3's mark it is out of his reach)


def _father_hands(pose, x=None):
    k = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    return dc.father(k, ds.FA1[0] + STEP[0] if x is None else x, ds.FA1[1], ds.FS, pose=pose, face="hard", look=(1, 0))["hands"]


def _father_reach(target):
    key = (round(target[0]), round(target[1]))
    if key not in FARM:
        rest = _father_hands((-8, 0, 8, 0))
        side = 0 if rest[0][0] > rest[1][0] else 1           # his screen-right hand
        best = None
        for a1 in range(0, 151, 3):
            for a2 in range(20, 121, 3):                    # the elbow bent
                pose = (-8, 0, a1, a2) if side == 1 else (-a1, -a2, 8, 0)
                hx, hy = _father_hands(pose)[side]
                e = math.hypot(hx - target[0], hy - target[1])
                if best is None or e < best[0]:
                    best = (e, pose, side)
        FARM[key] = best
    return FARM[key]


def r_press(s_, k, o, t, tt, n):
    """9.4': Father at the robot; his hand comes up to its chest, presses, stays on it; its face goes green."""
    st = V7.seq(t, [0.0, 0.6, 1.0])                         # the step in, then the hand up and on it
    u = V7.seq(t, [0.0, 0.0, 0.0, 0.5, 1.0])
    fx = ds.FA1[0] + STEP[0] * st
    mid = (fx + 26, 690.0)                                  # the in-between: his hand up at his chest, the elbow bent
    tx, ty = (mid if u == 0.5 else PRESS[0])
    e, pose, side = _father_reach((tx, ty))
    if u == 0:
        pose = (-8, 0, 8, 0)
    hp.reset(*(("relax", "point") if side == 1 else ("point", "relax")))
    dc.father(k, fx, ds.FA1[1], ds.FS, pose=pose, face="talk", look=(1, 0))
    hp.reset()
    if u >= 1 and t >= 0.25:                                # its face: the green tick, as 9.5's close shot
        rx, ry = o["robot"]["screen"]
        c = k.c
        c.set_source_rgb(0.30, 0.95, 0.55); c.set_line_width(4); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(rx - 9, ry); c.line_to(rx - 2, ry + 7); c.line_to(rx + 11, ry - 8); c.stroke()
    hd = (fx, ds.FA1[1] - 302 * ds.FS)
    V7.father_mouth(k, hd, s_.loud("9.4", tt))
    if s_.speaking("9.4", tt):
        o["say"] = ("Approved.", (hd[0] + 26, hd[1] + 28 * ds.FS), 1, True, -20, 170)


def r_offer_alone(s_, k, o, t, tt, n):                      # 9.4: Don alone, his hand coming up: "me!"
    i = V7.idx(t)
    if i < 3:
        dp.ceo_chair(k, ds.THR5, CH[1], CH[2])
        _way_don(k, ((-8, 0, 20, 110), (-8, 0, 60, 90), (-8, 0, 95, 72))[i])
    else:
        thumb_don(k, n, True, False, "happy", (-1, 0), 0)


sc.shot["9.4'"] = dict(sc.shot["9.3"])                      # 9.3's frame: Father and the robot by the door
sc.CAM8["9.4"] = (ds.DON6[0] + 18, 640, 2.3)                # Don alone, the throne behind him, his raised hand in the frame
_scr = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 54, 96)), 0)
_c93 = dl.draw(dict(sc.shot["9.3"], draw=lambda k_, o_: None), _scr)
sc.CAM8["9.4'"] = (_c93[0] - 14, _c93[1], _c93[2] * 0.88)   # 9.3's camera, a little wider and left: wall on his left for his box, the robot's face out of the button rail
sc.DRAW.update({"9.4": r_offer_alone, "9.4'": r_press})


SET_MOVES, SET_AIR, SET_BEHIND = {}, set(), set()
SET_WALKS = set()
ENTRANCES = set()


def frame8(tt, n, hi=1):
    A3.AVOID_EXTRA[:] = []
    if "Approved." not in A3.HELD:                          # 9.4': his box on his left (the robot is on his right)
        A3.HELD["Approved."] = (None, -1)
    if "Approved." not in A3.HELD:                          # Father says it to the robot, off the frame on his left: the box on
        A3.HELD["Approved."] = (None, -1)                   # his left, not between him and Don (v8 first pass: over Don's head)
    return E.frame(sc, tt, n, hi)


if __name__ == "__main__":
    me = sys.modules[__name__]
    if "gate" in sys.argv[1:]:
        sys.exit(1 if E.gate(sc, me, SET_MOVES, SET_AIR, SET_BEHIND, SET_WALKS, entrances=ENTRANCES) else 0)
    if "nobub" in sys.argv[1:]:
        E.NOBUB[0] = True
    E.run(sc, me, 7)
