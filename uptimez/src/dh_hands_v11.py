"""Daddy's Home v11 (26 Nov, Tomas "darom" after v10's cold test): two points both cold viewers raised.
- 0.7 "Today.": the post face down was a flat black strip half its width's height (v8-v10: "a different object, a black
  box"). Now it lies as the same post: its full width, foreshortened less (120 of 224), its back with the camera block and
  two lenses and a pale rim (One Star's phone back), drawn under his two hands, which keep holding its edges.
- the repairman's INVOICE $80: the sheet covered his hand ("fused into the paper"). Now his hand clutches the sheet's
  near edge in front of it (of_cast.clutch: the back of the hand outside, four fingers over its front).
Opt-in: install() after dh_hands_v10.install()."""
import math
import kit
import of_cast as oc

_ORIG = {}
BACK_H = 120.0                                    # the post lying face down: its height on screen, of its 224 upright


def _back(k, h, seed=4200):
    """The post's back, centred, 132 wide and h tall (booth units): dark, a pale rim, the camera block and two lenses."""
    c = k.c
    kit.rect(k, -66, -h / 2, 132, h, (0.10, 0.10, 0.12), seed, lw=2.6)
    c.set_source_rgb(0.62, 0.65, 0.72); c.set_line_width(2.2); c.rectangle(-60, -h / 2 + 5, 120, h - 10); c.stroke()
    bh = min(34.0, h * 0.30)
    c.set_source_rgb(0.30, 0.32, 0.38); c.rectangle(-56, -h / 2 + 9, 30, bh); c.fill()
    for i in range(2):
        yy = -h / 2 + 9 + bh * (0.30 + 0.42 * i)
        c.set_source_rgb(0.70, 0.74, 0.82); c.arc(-41, yy, min(6.0, bh * 0.2), 0, 2 * math.pi); c.fill()
        c.set_source_rgb(0.10, 0.11, 0.14); c.arc(-41, yy, min(3.0, bh * 0.1), 0, 2 * math.pi); c.fill()


def booth(k, seed=2500, tap=0.0, face_down=False, post="simple"):
    """The booth with its face-down post drawn as the post's back (under his hands)."""
    import dh_props as dp
    real = dp.rect

    def rect(k_, x, y, w, h, col, sd, *a, **kw):
        if (x, y, w, h) == (-66, -30, 132, 60):                    # v8's flat strip -> the post's back
            pass                                                    # (booth's own transform: centred at 262, 668, x1.7)
            return _back(k_, BACK_H, sd)
        return real(k_, x, y, w, h, col, sd, *a, **kw)
    dp.rect = rect
    try:
        return _ORIG["booth"](k, seed, tap, face_down, post)
    finally:
        dp.rect = real


def d_booth(t, tap=0.0, down=False, jolt=0.0, turn=None):
    """dh_anim1.d_booth: the turn ends on the same back the booth now draws (it no longer paints over his hands)."""
    import dh_anim1 as A
    import dh_props as dp

    def f(k, c):
        z = 1.0 + 0.035 * A.ease(t / 1.6)
        c.save(); c.translate(270, 430 + jolt); c.scale(z, z); c.translate(-270, -430)
        dp.booth(k, tap=tap, face_down=down or turn is not None)
        if turn is not None:                                       # the turn itself: v8's two drawings, ending on h 120
            u = turn
            h = 224 + (BACK_H - 224) * u; yy = 560 + (668 - 560) * u
            c.save(); c.translate(262, yy); c.rotate(0.08 * (1 - u)); c.scale(1.7, 1.7)
            _back(k, h)
            if u < 0.6:
                c.set_source_rgb(0.92, 0.95, 1.0); c.rectangle(-60, -h / 2 + 4, 120, 10 * (1 - u)); c.fill()
            c.restore()
        c.restore()
    return f


def visitor_invoice(k, x, feet, s, look=(1, 0), big=False):
    """dh_poses.visitor_invoice, then his hand clutching the sheet's near (left) edge, in front of it."""
    import dh_poses as dq
    import dh_cast as dc
    o = _ORIG["inv"](k, x, feet, s, look, big)
    hx, hy = o["hands"][1]
    sc = 1.5 if big else 1.0
    c = k.c
    c.save(); c.translate(hx + 30 * s, hy - 22 * s); c.rotate(0.10); c.scale(s, s)
    c.translate(-32 * sc, -26 * sc)                               # the sheet's left edge, where his sleeve meets it
    c.rotate(-math.pi / 2)
    oc.clutch(k, 0, 0, 26, dc.co.SKIN if hasattr(dc, "co") else (0.86, 0.66, 0.52))
    c.restore()
    return o


def install():
    if _ORIG:
        return
    import dh_props as dp
    import dh_anim1 as A
    import dh_poses as dq
    _ORIG.update(booth=dp.booth, d_booth=A.d_booth, inv=dq.visitor_invoice)
    dp.booth = booth
    A.d_booth = d_booth
    dq.visitor_invoice = visitor_invoice
