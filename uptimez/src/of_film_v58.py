"""THE OFFER v58 (26 Nov, series hands/phones plan v1): v57's five scenes with the hand canon (hands_v4.enable(phone="v4c"):
the phone grip v4c, the sheet's grab, pinch and fist). Nothing else changes. Grips v4c does not draw (a pressing thumb,
parts, the phone's back, a tilt over 0.35) keep the old grip.
  python3 of_film_v58.py [scene ...]     -> ../the-offer/of_scene{n}_v58_540.mp4, frames in /tmp/of_film/s{n}
  python3 of_film_v58.py cut             -> ../the-offer/of_roughcut_v58_540.mp4 (of_cut, G5)"""
import sys
import runpy
import hands_v4
import of_film

hands_v4.enable(phone="v4c")
of_film.VER = {n: 58 for n in range(1, 6)}

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["cut"]:
        import os
        import of_cut
        of_cut.VERSION = 58
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
