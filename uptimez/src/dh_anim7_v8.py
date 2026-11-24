"""DADDY'S HOME v8, scene 7 "The Arrival": v7's scene (dh_anim7.sc: clock, takes, mix) through dh_anim_v8 (v8 bubbles,
dead zones, set_gate), with the shots that failed redrawn:
  - the throne on its set mark (452; v7 418): Don in front of it where scene 6 left him, the line-up and the cameras with them
  - 9.4, 9.4', 9.5'' (the thumb): see THUMB below (hands audit #6: his raised arm behind the price tag, his body cut by
    the frame's edge: "an arm without a body, holding the tag"; rules: a finger near a sign = holding it)
  python3 dh_anim7_v8.py [gate|nobub]  ->  ../daddys-home/dh_s7_anim_v8.mp4"""
import sys
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


def _don_zipped(k, x, feet, s, pose=None, **kw):
    if pose is None:
        return _dz(k, x, feet, s, **kw)
    if tuple(pose) in THUMB:
        pose = THUMB[tuple(pose)]
    return _dz(k, x, feet, s, pose=pose, **kw)


_don_zipped._v7 = _dz
dq.don_zipped = _don_zipped

# ---- the thumb, drawn here (v7: s7_thumb / _thumb_don): the series' thumbs-up hand (hands_ps "thumb") in place of v7's
# rectangle on a fist, which read as "a raised index finger" and "a phone" 2 of 2, and the shake as real movement (v7's white
# "(( ))" marks read as "a ringing phone" 2 of 2).
GEST = ["relax", "thumb"]                                    # hp.reset(first hand drawn, second): the thumb on his far hand
THUMB_W = 1.3
# Round 1 (2 viewers, 3 heights, near hand): "clearest" 2/2 and no phone 2/2 at chest height, but beside Father the thumb
# touched his arm once Father stood near enough to leave room for his box. Round 2: the far hand, at shoulder height against
# the wall: clear of his ear, the tag and Father.
THUMB[(-150, -40, 10, 0)] = (-8, 0, 35, 125)
THUMB[(-146, -34, 4, 0)] = (-8, 0, 31, 119)


def thumb_don(k, n, up, shake, face, look, sink, father=None):
    dp.ceo_chair(k, ds.THR5, CH[1], CH[2])
    ds._arm_phone(k)
    if father:
        dc.father(k, ds.FA2[0], ds.FA2[1], ds.FS, face=father[0], look=father[1])
    pose = THUMB[(-150, -40, 10, 0)] if up else THUMB[(-146, -34, 4, 0)]
    if shake:                                               # it shakes: the forearm trembles, 2 degrees each way
        pose = (pose[0], pose[1] + (2 if n % 2 else -2)) + tuple(pose[2:])
    hp.reset(*GEST)
    real, cnt = kit.HAND[0], [0]

    def big(k_, hx, hy, w, *a):                             # the thumbs-up hand 1.3x: at feed size the thumb read as "a finger" (1 of 2)
        g = GEST[min(cnt[0], 1)]; cnt[0] += 1
        return real(k_, hx, hy, w * (THUMB_W if g == "thumb" else 1.0), *a)
    kit.HAND[0] = big
    try:
        d = _dz(k, ds.DON6[0], ds.DON6[1] + sink, 0.60, pose=pose, face=face, look=look)
    finally:
        kit.HAND[0] = real
        hp.reset()
    return d


def r_offer(s, k, o, t, tt, n):                             # 9.4: the arm comes up from his side to the thumb
    i = V7.idx(t)
    if i < 3:
        u = (0.25, 0.55, 0.85)[i]
        p = THUMB[(-150, -40, 10, 0)]
        THUMB["_way"] = (-8, 0, p[2] * u, p[3] * u)
        dp.ceo_chair(k, ds.THR5, CH[1], CH[2])
        dc.father(k, ds.FA2[0], ds.FA2[1], ds.FS, face="hard", look=(1, 0))
        hp.reset(*GEST)
        _dz(k, ds.DON6[0], ds.DON6[1], DS_, pose=THUMB["_way"], face="happy", look=(-1, 0))
        hp.reset()
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


sc.DRAW.update({"9.4": r_offer, "9.4'": r_approved, "9.5''": r_react})


SET_MOVES, SET_AIR, SET_BEHIND = {}, set(), set()
SET_WALKS = set()
ENTRANCES = set()


def frame8(tt, n, hi=1):
    A3.AVOID_EXTRA[:] = []
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
