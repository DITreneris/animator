"""OFFICE NOIR 3: beat 02 on the street, staged as camera frames (20 Nov). frames() -> eight surfaces, in order."""
import street_on3 as st
import client_on3 as b
import sofia_on3 as so3
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
        _sh(k, x, 36); st.star(k, x, G - 30, SC, "g_stand", "interested", look)
    return d


def with_folder(x):
    def d(k):
        client(x, "b_pay", (-0.8, 0.2))(k)
        st.folder(k, x + 2, G - 30 - 176 * Q, 0.62 * SC, -0.06)
    return d


def frames(door=False):
    """v3: the finger is out (it read as a wave twice; Tomas: proceed). Nine frames."""
    f = []
    f.append(st.frame("S1", [client(330)], rain=1))                                        # 2.1 he walks into the lamp's edge
    f.append(st.frame("S1", [client(400)], car=(250, 0.0), rain=2))                        # 2.2 the car, at his knees
    f.append(st.window_pov(1.0, 1.0, 0.0, door=door))                                                 # 2.4 his view: the glass down; her hand, the folder
    f.append(st.window_pov(1.0, 1.0, 0.6, door=door))                                                 #     his gloves on it; her hand still on it
    f.append(st.window_pov(0.0, 1.0, 1.0, door=door))                                                 #     he has it; the glass is up
    f.append(st.frame("S2", [with_folder(400)], car=(-190, 0.0), rain=3))                  #     the car pulls away; he holds the folder
    f.append(st.cv_insert(0.0))                                                            # 2.5 her photograph, and nothing else
    f.append(st.frame("S3", [sofia(690), with_folder(450)], rain=4))                       # 2.6 she comes under the lamp
    f.append(st.cv_insert(1.0))                                                            # 2.7 the photograph lifted: CV, her number
    return f
