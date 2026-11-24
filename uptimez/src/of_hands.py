"""THE OFFER (episode 13): the hand sheet (23 Nov, hand audit, decided). Every hand the film draws, each shot at its
start, middle and end, cropped from the 1080 frame and labelled with the function that drew it, so a person can look
at all the hands at once; the automatic part (one hand per wrist, a phone's thumb toward the body) is of_scenes'
hand_check, which fails the build. Run with every cut:
  python3 of_hands.py VERSION   ->  ../the-offer/of_hands_v<VERSION>.png"""
import json, math, os, sys
import cairo
from PIL import Image, ImageDraw
import kit as _kit
import of_scenes as sc
import of_cast as oc
import of_film as ff

LOG = []


def _real(c):
    return c.get_target().get_width() > 100


def _wrap():
    ch = oc.cartoon_hand
    def h(k, hx, hy, *a, **kw):
        if _real(k.c):
            LOG.append(("hand", k.c.user_to_device(hx, hy)))
        return ch(k, hx, hy, *a, **kw)
    _kit.HAND[0] = h; oc.cartoon_hand = h
    for n in ("phone_grip", "handle_grip", "clutch", "thumb_fist"):
        f = getattr(oc, n)
        def g(k, x, y, *a, _f=f, _n=n, **kw):
            if _real(k.c) and kw.get("part", "all") != "front":
                LOG.append((_n, k.c.user_to_device(x, y)))
            return _f(k, x, y, *a, **kw)
        setattr(oc, n, g)
    hl = sc.held_lighter
    def l(k, hx, hy, *a, **kw):
        if _real(k.c):
            LOG.append(("held_lighter", k.c.user_to_device(hx, hy)))
        return hl(k, hx, hy, *a, **kw)
    sc.held_lighter = l


def frame(sid, t):
    for title, where, scene, shots in sc.SCENES:
        for sh0 in shots:
            if sh0["id"] == sid:
                L = sc._timing()[sid]["len"]
                st_over, pose_over = ff.MOTION.get(sid, ff.still)(t, L)
                st_over = dict(st_over); cam_ = st_over.pop("_cam", None); cast = st_over.pop("_cast", None)
                sh = dict(sh0, state=dict(sh0["state"], **st_over))
                if cam_ is not None:
                    sh["cam"] = cam_
                if cast is not None:
                    sh["cast"] = cast
                saved = sc.POSES.get(sid)
                if pose_over:
                    base = dict(saved or {})
                    for who, ps in pose_over.items():
                        base[who] = dict(base.get(who, {}), **ps)
                    sc.POSES[sid] = base
                try:
                    return sc.render(sh, scene)[0]
                finally:
                    if saved is None:
                        sc.POSES.pop(sid, None)
                    else:
                        sc.POSES[sid] = saved


def main(ver):
    _wrap()
    tm = sc._timing()
    crops = []
    for title, where, scene, shots in sc.SCENES:
        for sh in shots:
            sid = sh["id"]; L = tm[sid]["len"]
            for t in (0.05, L / 2, max(0.05, L - 0.08)):
                del LOG[:]
                surf = frame(sid, t)
                path = "/tmp/_hands_%s.png" % sid
                surf.write_to_png(path)
                big = Image.open(path).convert("RGB")
                for fn, (x, y) in LOG:
                    x, y = 2 * x, 2 * y
                    if not (-60 < x < 1140 and -60 < y < 1980):
                        continue
                    if any(c_[0] == sid and c_[1] == fn and math.hypot(c_[2] - x, c_[3] - y) < 90 for c_ in crops):
                        continue
                    crops.append((sid, fn, x, y, round(t, 1), big.crop((int(x) - 110, int(y) - 110, int(x) + 110, int(y) + 110))))
    S, cols = 160, 10
    rows = (len(crops) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * S, rows * (S + 24)), "white"); d = ImageDraw.Draw(sheet)
    for i, (sid, fn, x, y, t, im) in enumerate(crops):
        X, Y = (i % cols) * S, (i // cols) * (S + 24)
        sheet.paste(im.resize((S, S)), (X, Y))
        d.text((X + 3, Y + S + 2), "%s t%.1f" % (sid, t), fill="black"); d.text((X + 3, Y + S + 12), fn, fill=(150, 0, 0))
    out = os.path.join(sc.OUT, "of_hands_v%s.png" % ver)
    sheet.save(out)
    print("%d hands -> %s" % (len(crops), out))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "x")
