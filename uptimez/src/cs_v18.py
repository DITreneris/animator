"""ONE STAR v18 (25 Nov evening, Tomas /grill-me "what else to polish"): the cold viewers' remaining notes.
- 1.1 an in-between drawing of the toss: the phone torn out of his hands (it jumped from his hands into the air);
- 6.1 the Client holds his phone in one hand, the other hangs; no roll (a knot of arms and "a blue pole");
- 6.6a his hands lock round the phone by d5 and stay (they changed shape every drawing); the buzz zigzags outside them;
- 2.1 opens on Don, not the wall calendar; 4.2 the plan already sliding in at d0 (an empty desk); 4.4 the paddle
  turned by d2 (a blank grey sign); 6.5 her phone up over 5 drawings (3 read as a jump);
- 3.5 the follow-through: after the release his arm goes on down and bends (held out straight it read as a pole); Everything here is opt-in through install(); v17 rebuilds as before."""
import cs_scene1 as s1
import cs_scene1_v14 as v14


def s1_1(k, d):
    """1.1, 26 drawings: 0-1 his hands, 2 the in-between, then v14's 2.. shifted by one (the wide one shorter)."""
    if d < 2:
        v14.gag(k, d)
    elif d == 2:
        v14.IB[0] = True
        try:
            v14.gag(k, 2)
        finally:
            v14.IB[0] = False
    elif d < v14.NG + 1:
        v14.gag(k, d - 1)
    else:
        v14.wide(k, d - v14.NG - 1)


def install():
    import cs_v14 as V
    V.FOLLOW35[0] = (-10, 5, 40, 70)
    import cs_scene2 as s2
    import cs_scene4 as s4
    import cs_scene6 as s6
    s2.PAN21 = (-2, -1)                                                           # 2.1 opens on Don (no wall calendar first)
    s4.LEAD42[0] = 5                                                              # 4.2 the plan already sliding in at d0
    s4.FLIP44 = (0, 2)                                                            # 4.4 HUMAN✓ turned by d2 (no blank grey sign)
    s6.RISE65[0] = 5.0                                                            # 6.5 her phone up over 5 drawings
    import cs_v14c
    cs_v14c.LOCK66[0] = True
    import cs_grips
    cs_grips.POSE61[0] = (-10, 5, -30, -80)
    cs_grips.ONEHAND61[0] = lambda o: max(o["client"]["hands"], key=lambda h: -h[1])   # the raised hand holds it
    v14.NOBURST2[0] = True
    s1.N11 = v14.N11                                                              # the wide gives its last drawing to the toss:
    s1.SHOTS[:] = [("1.1", v14.N11, s1_1) if x[0] == "1.1" else x for x in s1.SHOTS]   # the film's clock stays v17's (a 1/12 s
                                                                                  # shift lost "Still one star." in the mix again)
    v14.SFX[:] = [(2, "whoosh", 0.16), (6, "tap", 0.55), (9, "key", 0.22), (10, "chime", 0.34)]
    import cs_film
    import cs_sfx as fx
    cs_film.FX[:] = [x for x in cs_film.FX if x[0] != "1.1"] + \
        [("1.1", d, (fx.tap(220.0) if n == "tap" else getattr(fx, n)()), gn) for d, n, gn in v14.SFX]
    # LINE12 stays 1.42: the star lands at 0.83 s, well before it (moving it moved the mix: "Nine o'clock." lost)
