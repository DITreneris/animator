"""OFFICE NOIR 3: beat 02 on the street, staged as camera frames (20 Nov). frames() -> eight surfaces, in order."""
import street_on3_v1 as st
import client_on3 as b
import sofia_on3 as so3
import sofia_on as son
from kit import Ctx

G = st.G
SC = 0.9
Q = SC * b.REL


def _sh(k, x, w=46):
    import math
    c = k.c
    c.save(); c.translate(x, G - 30); c.scale(w, w * 0.16); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, 0.35); c.fill()


def client(x, pose="b_walk", look=(0.8, 0), **kw):
    def d(k):
        _sh(k, x); b.boxer(k, x, G - 30, Q, pose, "hard", look, outfit="street", **kw)
    return d


def sofia(x, look=(-1, 0.3)):
    def d(k):
        _sh(k, x, 36); son.sofia_noir(k, x, G - 30, SC, face_kind="side", look=look, nails=False)
    return d


def frames():
    f = []
    f.append(st.frame("S1", [client(150)], rain=1))                                        # 2.1 he walks; the door far off
    f.append(st.frame("S1", [client(400)], car=(250, 0.0), rain=2))                        # 2.2 the car, at his knees
    f.append(st.frame("S2", [client(400, "b_fist", (0.2, 0.6))], car=(250, 0.0)))          # 2.3 one glove, raised at the black glass
    f.append(st.window_pov(1.0, 1.0, 0.0))                                                 # 2.4 his view: the hand, the folder
    f.append(st.window_pov(1.0, 1.0, 1.0))                                                 #     his gloves have it
    f.append(st.cv_insert(0.0))                                                            # 2.5 her photograph
    f.append(st.frame("S3", [sofia(690), client(450, "b_walk", (0.9, 0), )]))              # 2.6 she comes under the lamp
    f.append(st.cv_insert(1.0))                                                            # 2.7 CV, the number
    return f
