"""THE OFFER v63 (26 Nov, Tomas: "the phones are not fixed, every frame carefully"): v62 with EVERY phone v4c
(hands_v4.ALL_V4C: tilted phones, the phone at the ear, the close-ups 0.4 / 2.8 / 4.1 with a pressing thumb). Was: v62 (26 Nov, series hands/phones plan v1; Tomas's /grill-me): v61 with the hand canon
(hands_v4.enable(phone="v4c"): the phone grip v4c without the sheet's forearm stub, the sheet's grab, pinch and fist).
One exception, his pick: 2.8e, the ignition key, keeps v61's old fist, because the sheet's fist hid the fingertips on
the key.
  python3 of_film_v63.py [scene ...]     -> ../the-offer/of_scene{n}_v63_540.mp4
  python3 of_film_v63.py cut             -> ../the-offer/of_roughcut_v63_540.mp4 (of_cut, G5)"""
import sys
import hands_v4
import of_film
import of_scenes

hands_v4.enable(phone="v4c")
hands_v4.ALL_V4C[0] = True
of_film.VER = {n: 63 for n in range(1, 6)}

_insert = of_scenes.insert_shot


def insert_shot(k, sh):
    """2.8e (the key) draws with the old hands; every other insert with the canon."""
    if sh["state"].get("insert") != "key":
        return _insert(k, sh)
    import hands_ps as hp
    new, hp.draw = hp.draw, hands_v4._ORIG["draw"]
    try:
        return _insert(k, sh)
    finally:
        hp.draw = new


of_scenes.insert_shot = insert_shot

_m41 = of_film.MOTION["4.1"]


def m41(t, L):
    """4.1 (v63): the thumb presses red, then lifts back to the phone's edge 0.15 s after DECLINED shows, so the
    DECLINED screen is read clear (v4c's thumb lay across it while it was held)."""
    st, ex = _m41(t, L)
    u = t - 1.1
    if u > 0.6 and st.get("thumb"):
        st = dict(st, thumb=st["thumb"] * (1.0 - of_film.ease((u - 0.6) / 0.15)))
    return st, ex


of_film.MOTION["4.1"] = m41

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["cut"]:
        import os
        import of_cut
        of_cut.VERSION = 63
        os.makedirs(of_cut.TMP, exist_ok=True)
        seq, total = of_cut.assemble()
        m1080, m540 = of_cut.encode(seq)
        r = of_cut.qa(m1080, len(seq))
        for f in r["fails"]:
            print("FAIL", f)
        print("G5: %s -> %s" % ("PASS" if not r["fails"] else "FAIL", m540))
    else:
        for n in [int(a) for a in args] or range(1, 6):
            k, dur, probs, m540, m1080 = of_film.render_scene(n)
            print("scene %d: %d frames, %.2f s -> %s  faults %d" % (n, k, dur, m540, len(probs)))
            for q in probs[:10]:
                print("FAIL", q)
