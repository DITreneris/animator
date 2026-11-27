"""ONE STAR v23 (26 Nov, Tomas: 0:09 Don's hand into the robot's head and "why are his eyes shut?"; 0:44 over-engineered,
the green tick on HUMAN; 0:47 the Client's elbow; 1:04 who holds the phone, Sofía's hands; 1:07 who holds the phone).
Opt-in through install()."""
import cs_v14 as V


def install():
    V.FACE14[0] = "grin"                                                          # 1.4: eyes open, grinning, looking off and
    V.LOOK14[0] = (1, -0.5)                                                       # up (shut eyes read as asleep)
    V.VIS14[0] = 1.12                                                             # his fingertip at the visor's edge, not in it
    V.GEO14.clear()
    import cs_v15e as E
    E.NOTICK44[0] = True
    import cs_scene6 as s6
    import cs_scene1 as s1
    s1.ONLYDON66[0] = True
    import cs_say
    cs_say.PLAN["6.5"] = dict(form="L", w=150)
    s6.SHOTS[:] = [(n, nd, s6_5 if n == "6.5" else f) for n, nd, f in s6.SHOTS]
    import cs_scene5 as s5
    s5.UP51[0] = (s5.CL_X - 78, 722)                                              # 5.1: his arm out at Pam, the elbow open


# ---- 6.5: Sofía holds a phone in her own hand ------------------------------------------------------------------------

POSE65N = ["show"]
PH65 = [2.6]
HANDS65 = []
SHOWX65, SHOWY65 = [-84], [96]                                     # the hand in, the elbow bent (elbow gate)


def _screen65(c):
    import cs_props as cp
    import cs_scene6 as s6
    cp.T(c, "UPDATE:", 0, -25, 7.2, col=cp.GRN)
    cp.T(c, "Pam found it.", 0, -16, 6.4, col=(0.55, 0.16, 0.46))
    s6.star(c, 0, 0, 10, True)
    for i in range(4):
        s6.star(c, -11 + i * 7.5, 13, 2.8, False)
    cp.T(c, "1/5", 0, 29, 11)


def s6_5(k, d):
    """6.5 (v23; Tomas: "who holds the phone, Sofía's hands, why such anatomy?"): v13's tablet thrust at us had no arm
    (a hand with red nails at its edge) and her other hand held the clipboard. Now a phone in HER hand, the series'
    phone grip, its screen to us beside her face, her arm from the shoulder; the clipboard under her other arm."""
    import math
    import cs_scene6 as s6
    import cs_scene1 as s1
    import of_cast as oc
    t = d / float(s6.DPS)
    up = s6.ease(d / s6.RISE65[0])
    talk = s6.LINE65[0] <= t <= s6.LINE65[1]
    mouth = ("A", "E", "M", "O", "E", "M")[int((t - s6.LINE65[0]) * s6.DPS / 2) % 6] if talk else None
    of = s1.sofia_fs.sofia

    def sof(*a, **kw):
        try:
            return of(*a, mouth=mouth, **kw)
        except TypeError:
            return of(*a, **kw)

    def ex(k_, o):
        HANDS65[:] = list(o["hands"])
        hx, hy = min(o["hands"], key=lambda q: q[1])
        c = k_.c
        s1.PH_DEV.append(c.user_to_device(hx, hy))
        oc.phone_grip(k_, hx, hy, PH65[0] * 0.25, screen=_screen65, ang=0.04, skin=(0.98, 0.84, 0.74),
                      body_x=hx + 40, back=False)
    import sofia_ob as so
    ot = so.tablet

    def tab(k_, x, y, ang, kind, seed=0):                                         # "show"'s form tablet: the phone is
        if kind != "form":                                                         # in that hand now (the clipboard stays
            return ot(k_, x, y, ang, kind, seed)                                   # under her other arm)
    so.tablet = tab
    op = so.POSES["show"]
    so.POSES["show"] = so._ik(-1, SHOWX65[0], so.BODY_TOP + SHOWY65[0]) + so.REST          # her hand lower: the bubble above it
    s1.sofia_fs.sofia = sof
    try:
        with s6.Breath(s1.sofia_fs, "sofia", s6.br(d, 0.6)):
            s6.S(k, s6.CAM65, auto=False, portrait=False, extra=lambda k_, o: ex(k_, o["sofia"]),
                 **s6.base(door=0.0, cl=False, rb=False, dn=False, pm=False, mm=False,
                           sf=s6.at("sofia", x=s6.SX65, pose=POSE65N[0], face="unimpressed", look=(-0.3, 0.1))))
    finally:
        s1.sofia_fs.sofia = of
        so.tablet = ot
        so.POSES["show"] = op
