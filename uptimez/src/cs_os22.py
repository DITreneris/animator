"""ONE STAR v22 (26 Nov, Tomas: "0:11 the UptimeZ message appears unnaturally and covers the likes"):
- 1.4b the feed SCROLLS: as the company's reply comes in under the post, the post moves up 70 so its reactions row
  (48K) stays in sight above the reply, the way a feed makes room (v13-v21: the reply slid up over the row).
- 4.1 Pam's "Wait." (voice A, take a) with her STOP palm; the clown 18 % bigger; the corporate line readable;
  the scroll 96 so the header leaves whole;
- the reactions row outside 1.2 shows where 1.2 ended (48K, red), with no flying reactions: it no longer depends on
  which drawing of 1.2 was drawn last.
Opt-in through install()."""
import math
import cs_scene1 as s1
import cs_props as cp
import cs_os19 as o19

SCROLL = 96.0                                                                   # the header gone, not cut (review)
SCREEN = (58, 70, 424, 820)


def react(k, n):
    if o19.D12[0] is None:                                                        # outside 1.2: its end state, still
        born, o19.BORN[:] = list(o19.BORN), []
        o19.D12[0] = 45
        try:
            return o19.react(k, n)
        finally:
            o19.BORN[:] = born
            o19.D12[0] = None
    return o19.react(k, n)


def s1_4b(k, d):
    """16 drawings. The post at 48K; the reply comes in under it while the feed scrolls up to make room."""
    c = k.c
    ph = 2 * math.pi * (d + s1.N12) / float(s1.DPS) / s1.A.BREATH
    c.set_source_rgb(0.24, 0.22, 0.20); c.paint()
    c.save(); c.translate(270, 480); c.rotate(math.radians(0.35 * math.sin(ph))); c.translate(-270, -480 + 2.0 * math.sin(ph))
    e = s1.ease((d - 2) / 5.0)
    post = s1._phone_surface("crisis", d)
    c.set_source_surface(post, 0, 0); c.paint()                                    # the phone's body and bezel
    x, y, w, h = SCREEN
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*cp.LIGHT); c.paint()
    c.set_source_surface(post, 0, -SCROLL * e); c.paint()                          # the post, scrolled
    if e > 0:
        ry = 650 - SCROLL * e + 40                                                 # the reply's card under the row
        c.save(); c.rectangle(x, ry - 4, w, y + h - ry + 4); c.clip()
        c.set_source_rgb(*cp.LIGHT); c.paint()
        dy = -SCROLL * e + 40 + (1 - e) * 120
        c.rectangle(x, ry - 4, w, y + h + dy - ry + 4); c.clip()                    # its own screen only, not its bezel
        c.set_source_surface(s1._phone_surface("reply", d), 0, dy); c.paint_with_alpha(e)
        c.restore()
    c.restore()
    c.restore()


TAKES = "cs_voices/film_v11"


def install():
    if getattr(s1.react, "v22", False):
        return
    import importlib
    import cs_scene4 as s4
    import cs_say
    cp.CLOWN_R[0] = 19                                                             # the clown +18 % (review)
    cp.VALUE[0] = (22, 0.80)                                                       # "We value every client's journey..." readable
    s4.LINE41[0] = (0.25, 0.25 + 0.58)                                             # Pam's "Wait." with the STOP palm (d3)
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).TAKES = TAKES
    cs_say.PLAN["4.1p"] = dict(form="T", w=110)
    cs_say.LINES.clear(); cs_say.LINES.update(cs_say.lines())
    old2 = s1.s1_2

    def s1_2(k, d):
        try:
            return old2(k, d)
        finally:
            o19.D12[0] = None
    react.v22 = True
    o19.D12[0] = None
    s1.react = react
    s1.s1_2 = s1_2
    s1.SHOTS[:] = [(n, nd, s1_2 if n == "1.2" else (s1_4b if n == "1.4b" else fn)) for n, nd, fn in s1.SHOTS]
