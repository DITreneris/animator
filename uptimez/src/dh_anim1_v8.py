"""DADDY'S HOME v8, scene 1 "The Call": v10's scene (dh_anim1: its own clock, drawings and mix) through dh_anim_v8 (v8
bubbles, dead zones, set_gate, a mode without bubbles), by a bridge that turns dh_anim1.frame's branches into shots and
inserts, with the call redrawn:
  - 0.4, 0.5b, 0.6, 0.7b (on the phone): of_cast.phone_grip at his ear, the palm behind the phone, its back against his
    head, the arm from his own shoulder with the elbow out (v10: his hand behind his head and the phone by his cheek, not
    in it, hands audit #1; rules: one grip for every phone, lesson 179)
  - Father's lines (the booth, his face above the frame, and through the phone) on named cards: an off-screen speaker
  python3 dh_anim1_v8.py [gate|nobub]  ->  ../daddys-home/dh_s1_anim_v8.mp4"""
import math
import sys
import cairo
import kit
import fs_storyboard as sb
import dh_props as dp
import dh_layout as dl
import dh_scenes as ds
import of_cast as oc
import dh_anim1 as V7
import dh_anim_v8 as E
import dh_anim3_v8 as A3

F, CH, DON = V7.F, V7.CH, V7.DON
SKIN = V7.SKIN
CALL = {"0.4", "0.5b", "0.6", "0.7b"}
INSERT = {"0.1", "0.3", "0.5a", "0.7a"}


# ---- the call: the phone in his hand at his ear
EAR = [(40, 34)]                                            # the palm, from his head's centre (screen right): under the ear
PHONE_S = [0.7]
# Round 1 (2 viewers; v10, the grip at his ear, two speaker holds): at his ear the phone "is stuck to his cheek" 2/2 (his
# head is wider than his arm is long: the hand cannot reach round it with the elbow out). Held up in front of him, on speaker,
# DAD on its screen: "clearly in his hand, on a visible arm", "his dad" 2/2 (rules: upright when it must be read, 200; 178).
SPEAKER = [(54, -110)]                                      # (dx, dy) from his feet: the phone held up in front of him, on speaker                                            # the phone_grip scale at DON's size
ARMS = {}


def _hands(x, feet, pose, face, look):
    k = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    real = getattr(sb.don, "_real", sb.don)
    return real(k, x, feet, DON[2], pose, face, look=look)


def _ear_pose(target, face, look):
    """His screen-right arm's angles that put its hand on target, the elbow bent and out (searched, cached)."""
    key = (round(target[0]), round(target[1]))
    if key not in ARMS:
        best = None
        for a1 in range(0, 181, 4):
            for a2 in range(40, 171, 4):
                hx, hy = _hands(DON[0], DON[1], (-8, 0, a1, a2), face, look)["hands"][1]
                e = math.hypot(hx - target[0], hy - target[1])
                if best is None or e < best[0]:
                    best = (e, (-8, 0, a1, a2))
        ARMS[key] = best[1]
    return ARMS[key]


def d_call(t, tt, face, key=None, lower=0.0, lit=True, face2=None, at2=9.0, look=(0.3, 0), afraid=None, drop=None, still=False):
    """v10's d_call, the phone in a phone_grip at his ear; lower 0..1 brings the hand and phone down in front of him."""
    def f(k, o):
        dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
        u = V7.ease(lower)
        fc = face2 if (face2 and t >= at2) else face
        lk = (look[0] + (0.6 - look[0]) * u, look[1] + (0.6 - look[1]) * u)
        head = _hands(DON[0], DON[1], (-8, 0, 8, 0), fc, lk)["head"]
        ear = (head[0] + EAR[0][0], head[1] + EAR[0][1]) if not SPEAKER[0] else (DON[0] + SPEAKER[0][0], DON[1] + SPEAKER[0][1])
        low = (DON[0] + 34, DON[1] - 230) if not SPEAKER[0] else (DON[0] + 46, DON[1] - 70)   # lowered: to his side
        target = (ear[0] + (low[0] - ear[0]) * u, ear[1] + (low[1] - ear[1]) * u)
        pose = _ear_pose(target, fc, lk)
        seen, real = [], kit.HAND[0]

        def keep(k_, hx, hy, *a):                           # his screen-right hand is the grip's palm; the other the series hand
            seen.append((hx, hy))
            if len(seen) == 2:
                return None
            return real(k_, hx, hy, *a) if real else None
        kit.HAND[0] = keep
        try:
            with V7.About(k.c, DON[0], DON[1], 1.0, 1.0 if still else V7.breath(tt, 0.3)):
                d = sb.don(k, DON[0], DON[1], DON[2], pose, fc, look=lk)
                px, py = d["hands"][1]
                ang = -0.10 + 0.5 * u                       # upright at his ear; it tips as it comes down
                if SPEAKER[0]:
                    ang = 0.6 * u                           # upright; it tips as his hand drops
                oc.phone_grip(k, px, py, PHONE_S[0], screen=(_dad if (lit and SPEAKER[0]) else (_lit if lit else None)), ang=ang, skin=SKIN,
                              body_x=DON[0], back=False)
                if afraid:
                    V7.fear(k, d["head"], DON[2], afraid, V7.loud(key, tt) if key else 0.0)
                elif key:
                    V7.mouth(k, d["head"], DON[2], V7.loud(key, tt))
                if drop is not None:
                    V7.sweat(k, d["head"], DON[2], drop)
        finally:
            kit.HAND[0] = real
        o["mouth"] = (d["head"][0] - 27, d["head"][1] + 27 * DON[2])
    return f


def _lit(c):                                                # the screen, lit while the call is on (v10: a pale blue strip)
    c.set_source_rgb(0.55, 0.80, 1.0); c.rectangle(-18, -34, 36, 66); c.fill()


def _dad(c):                                                # on speaker: the call screen, DAD, the word said aloud
    c.set_source_rgb(0.55, 0.80, 1.0); c.rectangle(-18, -34, 36, 66); c.fill()
    c.set_source_rgb(0.05, 0.08, 0.14); c.select_font_face(kit.FONT, 0, 1); c.set_font_size(13)
    e = c.text_extents("DAD"); c.move_to(-e.x_advance / 2, -6); c.show_text("DAD")


# ---- the bridge: dh_anim1.frame's branches as shots and inserts
class Bridge1:
    def __init__(self):
        self.rows, self.T0, self.total, self.phone = V7.ROWS, V7.T0, V7.TOTAL, False
        self.shot, self.DRAW, self.INS = {}, {}, {}
        self.SHIFT, self._cam0, self.PRE = {}, {}, None
        self.CARD = {"Donnie.": "FATHER", "My men go in first.": "FATHER", "Today.": "FATHER"}
        self.CARD8 = {"I arrive at five.": "FATHER"}           # his voice through the phone
        HS, H = ds.HS, ds.H
        for sid, _ in self.rows:
            if sid in INSERT:
                self.shot[sid] = {"insert": None}
                self.INS[sid] = self._ins(sid)
            else:
                heads, cam = ([HS], None) if sid.startswith("0.2") and sid != "0.2c" else (([H], None) if sid == "0.2c" else ([H], V7.CLOSE))
                self.shot[sid] = dl.shot(sid, heads, None, "", chair=False, cam=cam, ymin=150)
                self.DRAW[sid] = self._draw(sid)

    def _ins(self, sid):
        def f(sc, k, c, t, tt, n):
            if sid == "0.1":
                V7.d_phone(t, n)(k, c); return None
            if sid == "0.3":
                V7.d_booth(t)(k, c)
                return ("Donnie.",) if V7.speaking("0.3", tt) else None
            if sid == "0.5a":
                w = t - 0.95
                tp = 0.0 if w < 0 else (1.0 if w < 0.17 else max(0.0, 1.0 - (w - 0.17) / 0.17))
                V7.d_booth(t, tap=tp, jolt=2.0 if 0 <= w < 0.09 else 0.0)(k, c)
                return ("My men go in first.",) if V7.speaking("0.5", tt) else None
            w = t - 0.72
            V7.d_booth(t, down=w >= 0.17, turn=(0.35 if w < 0.085 else 0.72) if 0 <= w < 0.17 else None, jolt=3.0 if 0.17 <= w < 0.26 else 0.0)(k, c)
            return ("Today.",) if V7.speaking("0.7", tt) else None
        return f

    def _draw(self, sid):
        def f(sc, k, o, t, tt, n):
            if sid in ("0.2a", "0.2a'", "0.2b"):
                V7.d_seat(t, n, {"0.2a": "a", "0.2a'": "freeze", "0.2b": "drop"}[sid])(k, o); return
            if sid == "0.2c":
                V7.d_up(t, n)(k, o); return
            fn = {"0.4": lambda: d_call(t, tt, "happy", key="0.4", drop=min(1.0, t / 1.3)),
                  "0.5b": lambda: d_call(t, tt, "happy", face2="neutral", at2=0.75, drop=1.0),
                  "0.6": lambda: d_call(t, tt, "neutral", key="0.6", afraid="hope", drop=1.0),
                  "0.7b": lambda: d_call(t, tt, "shock", lower=t / 0.35, lit=False, afraid="o", drop=1.0, still=True)}[sid]
            fn()(k, o)
            if sid == "0.4" and V7.speaking("0.4", tt):
                o["say"] = ("Dad! Great timing!", o["mouth"])
            elif sid == "0.6" and V7.speaking("0.6", tt):
                o["say"] = ("Tomorrow?", o["mouth"])
            elif sid == "0.5b" and V7.speaking("0.5", tt):
                o["say"] = ("I arrive at five.", o["mouth"])
        return f

    def sound(self, out):
        V7.sound(out)


sc = Bridge1()
sc.shot["0.2b"]["ymin"] = 320                               # clear_signs pushed the camera for the portrait as far as his face allowed
#                                                             (150): on the seat's first lift the tag went under the title bar
sc.SHIFT = {"0.2b": (0, 0, 0.92)}                             # the seat's bounce: the price tag stays under the title bar
SET_MOVES, SET_AIR, SET_BEHIND, SET_WALKS, ENTRANCES = {}, set(), set(), set(), set()


def frame8(tt, n, hi=1):
    A3.AVOID_EXTRA[:] = []
    return E.frame(sc, tt, n, hi)


if __name__ == "__main__":
    me = sys.modules[__name__]
    if "gate" in sys.argv[1:]:
        sys.exit(1 if E.gate(sc, me, SET_MOVES, SET_AIR, SET_BEHIND, SET_WALKS, entrances=ENTRANCES) else 0)
    if "nobub" in sys.argv[1:]:
        E.NOBUB[0] = True
    E.run(sc, me, 1)
